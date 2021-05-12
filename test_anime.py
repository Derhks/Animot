import os
import unittest

from models.anime import Anime


class TestClassAnime(unittest.TestCase):

    def test_search_anime_id_first_page(self):
        anime_name = 'naruto'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '11'

        got = Anime.search_anime_id(Anime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_second_page(self):
        anime_name = 'berserk'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '24'

        got = Anime.search_anime_id(Anime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_third_page(self):
        anime_name = 'shuffle'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '58'

        got = Anime.search_anime_id(Anime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_fail(self):
        anime_name = 'kuroshitsuji'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = 0

        got = Anime.search_anime_id(Anime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_get_anime_data(self):
        anime_id = '11'

        want = 'Naruto'

        got = Anime.get_anime_data(int(anime_id))

        self.assertEqual(want, got['data']['attributes']['canonicalTitle'])

    def test_info_anime(self):
        anime_name = 'naruto'
        want = 'Naruto'

        got = Anime(anime_name)

        got.info_anime()

        self.assertEqual(want, got.canonical_title)

    def test_info_anime_fail(self):
        anime_name = 'kuroshitsuji'
        want = 404

        got = Anime(anime_name)

        try:
            got.info_anime()
        except Exception as Err:
            self.assertEqual(want, Err.code)


if __name__ == '__main__':
    unittest.main()
