import requests
import tweepy

from flask import request
from json import loads
from models.finished_anime import FinishedAnime
from models.anime import Anime
from os import remove
from os.path import isfile
from settings import (
    app, URL_IMAGE, CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)
from utils import RequestInfoAnime


def download_image(link: str) -> None:
    try:
        res = requests.get(link)
        file = open(URL_IMAGE, "wb")
        file.write(res.content)
        file.close()
        res.raise_for_status()

    except requests.exceptions.HTTPError as Err:
        raise Err


def get_api() -> tweepy.API:
    # Authenticate to Twitter
    consumer_key = CONSUMER_KEY
    consumer_secret = CONSUMER_SECRET
    access_token = ACCESS_TOKEN
    access_token_secret = ACCESS_TOKEN_SECRET
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def create_word_list(text: str) -> list:
    return text.split('\n')[0].split()


def status_message(text: str, length: int) -> dict:
    len_characters = 0
    list_of_words = create_word_list(text)
    last_word_position = 0
    msg = ''

    for idx in range(len(list_of_words)):
        if len_characters < length:
            msg += list_of_words[idx] + ' '
            len_characters += len(list_of_words[idx]) + 1
        else:
            last_word_position = idx
            break

    return {
        'message': msg + '...',
        'idx': last_word_position
    }


def reply_message(text: str, last_word_position: int, length: int) -> dict:
    list_of_words = create_word_list(text)[last_word_position:]
    len_characters = 0
    msg = ''
    new_last_word_position = 0
    final_idx = 0

    for idx in range(len(list_of_words)):
        len_word = len(list_of_words[idx])

        if len_characters + len_word < length:
            msg += list_of_words[idx] + ' '
            len_characters += len_word + 1
            final_idx = idx
        else:
            new_last_word_position = final_idx + last_word_position + 1
            break

    return {
        'message': msg + '...',
        'idx': new_last_word_position
    }


def post_tweet(anime: Anime) -> dict:
    api = get_api()

    name = anime.canonical_title
    rating = anime.rating
    info = status_message(anime.synopsis, length=120)
    synopsis_status = info['message']

    msg = f'{name}\nRating: {rating}\nSynopsis: {synopsis_status}'
    url_image = URL_IMAGE

    try:
        download_image(anime.image)

        if isfile(url_image):
            tweet = api.update_with_media(url_image, msg)
            remove(url_image)

            if len(anime.synopsis) > 120:
                return {
                    'tweet_id': int(tweet.id_str),
                    'idx': info['idx'],
                    'is_long': True
                }

    except tweepy.error.TweepError as Err:
        remove(url_image)
        raise Err


def reply_tweet(tweet_id: int, synopsis: str, last_word_position: int) -> None:
    api = get_api()
    msg = reply_message(synopsis, last_word_position, length=140)
    len_slice = len(create_word_list(synopsis))

    try:
        tweet = api.update_status(
            status=msg['message'],
            in_reply_to_status_id=tweet_id,
            auto_populate_reply_metadata=True
        )

        if msg['idx'] < len_slice and msg['idx'] != 0:
            reply_tweet(int(tweet.id_str), synopsis, msg['idx'])

    except tweepy.error.TweepError as Err:
        raise Err


def anime_was_published(anime: str) -> bool:
    words_list = anime.split('-')
    canonical_title = ''

    for idx in range(len(words_list)):
        word = words_list[idx]
        new_word = list(word)
        new_word[0] = word[0].upper()
        canonical_title += ''.join(new_word)

        if idx < len(words_list) - 1:
            canonical_title += ' '

    anime_viewed = FinishedAnime.query.filter_by(canonical_title=canonical_title)

    if anime_viewed.first() is None:
        return False

    return anime_viewed.first().is_published


@app.route('/<name>')
def hello_world(name: str):

    if anime_was_published(name):
        return f'This anime has already been published'

    info = RequestInfoAnime(anime=name)
    anime_data = info.get()
    anime = Anime(
        canonical_title=anime_data['canonical_title'],
        synopsis=anime_data['synopsis'],
        rating=anime_data['rating'],
        image=anime_data['image']
    )

    anime.save()

    synopsis = post_tweet(anime)

    if synopsis['is_long']:
        reply_tweet(
            tweet_id=synopsis['tweet_id'],
            synopsis=anime.synopsis,
            last_word_position=synopsis['idx']
        )

    anime_viewed = FinishedAnime(anime_data['canonical_title'])
    anime_viewed.update(published=True)

    return 'The anime has been published'


@app.route('/finished_anime/', methods=['POST'])
def finished_anime():
    name = loads(request.data.decode())['canonical_title']
    anime_viewed = FinishedAnime(canonical_title=name)
    anime_viewed.save()

    return f'You have finished watching {name}'


if __name__ == '__main__':
    app.run()
