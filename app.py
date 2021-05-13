import os
import requests
import tweepy

from dotenv import load_dotenv
from flask import Flask
from models.anime import Anime
from os import remove
from os.path import isfile

load_dotenv()  # take environment variables from .env

app = Flask(__name__)


def download_image(link: str) -> None:
    try:
        res = requests.get(link)
        file = open(os.environ['URL_IMAGE'], "wb")
        file.write(res.content)
        file.close()
        res.raise_for_status()

    except requests.exceptions.HTTPError as Err:
        raise Err


def get_api() -> tweepy.API:
    # Authenticate to Twitter
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
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
    url_image = os.environ['URL_IMAGE']

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


@app.route('/<name>')
def hello_world(name: str):
    anime = Anime(name)
    anime.info_anime()
    synopsis = post_tweet(anime)

    if synopsis['is_long']:
        reply_tweet(
            tweet_id=synopsis['tweet_id'],
            synopsis=anime.synopsis,
            last_word_position=synopsis['idx']
        )

    anime.save()

    return 'The anime has been published'


if __name__ == '__main__':
    app.run()
