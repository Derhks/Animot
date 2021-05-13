import flask
import os

from datetime import datetime
from utils import get, postgres_execute


class Anime:
    anime_id = 0

    def __init__(self, name: str):
        self.name = name
        self.canonical_title = ''
        self.synopsis = ''
        self.rating = ''
        self.image = ''
        self.published_at = datetime.now()

    def search_anime_id(self, url: str) -> int:
        obtain_anime_data = get(url=url)
        next_page = True if 'next' in obtain_anime_data['links'] else False

        for idx in range(len(obtain_anime_data['data'])):
            slug = obtain_anime_data['data'][idx]['attributes']['slug']
            if slug == self.name:
                self.anime_id = obtain_anime_data['data'][idx]['id']
                break

        if next_page:
            if self.anime_id == 0:
                url_next_page = obtain_anime_data['links']['next']
                self.search_anime_id(url=url_next_page)

        return self.anime_id

    @staticmethod
    def get_anime_data(id_anime: int) -> dict:
        url = os.environ['URL_ANIMES']
        full_url = f'{url}/{id_anime}'

        return get(url=full_url)

    def info_anime(self):
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        anime_number = self.search_anime_id(url=full_url)

        if anime_number == 0:
            msg_error = os.environ['ERROR_MESSAGE']
            flask.abort(404, msg_error)

        data = self.get_anime_data(id_anime=int(anime_number))

        self.canonical_title = data['data']['attributes']['canonicalTitle']
        self.synopsis = data['data']['attributes']['synopsis']
        self.rating = data['data']['attributes']['averageRating']
        self.image = data['data']['attributes']['posterImage']['large']

    def save(self):
        postgres_insert_query = """
            INSERT INTO animes_viewed (canonical_title, synopsis, rating, image, published_at)
            VALUES (%s,%s,%s,%s,%s)
        """
        record_to_insert = (
            self.canonical_title,
            self.synopsis,
            self.rating,
            self.image,
            self.published_at
        )

        postgres_execute(postgres_insert_query, record_to_insert)
