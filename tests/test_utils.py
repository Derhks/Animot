import os
import unittest

from utils import RequestInfoAnime


class TestRequestInfoAnime(unittest.TestCase):

    def test_search_anime_id_first_page(self):
        anime_name = 'naruto'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '11'

        got = RequestInfoAnime.search_anime_id(RequestInfoAnime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_second_page(self):
        anime_name = 'berserk'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '24'

        got = RequestInfoAnime.search_anime_id(RequestInfoAnime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_third_page(self):
        anime_name = 'shuffle'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = '58'

        got = RequestInfoAnime.search_anime_id(RequestInfoAnime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_search_anime_id_fail(self):
        anime_name = 'kuroshitsuji'
        url = os.environ['URL_ANIMES']
        more_data = os.environ['URL_MORE_DATA']

        full_url = f'{url}?{more_data}'

        want = 0

        got = RequestInfoAnime.search_anime_id(RequestInfoAnime(anime_name), url=full_url)

        self.assertEqual(want, got)

    def test_get_anime_data(self):
        anime_id = '11'

        want = 'Naruto'

        got = RequestInfoAnime.get_anime_data(int(anime_id))

        self.assertEqual(want, got['data']['attributes']['canonicalTitle'])

    def test_info_anime(self):
        anime_name = 'naruto'
        want = 'Naruto'

        got = RequestInfoAnime(anime_name).get()

        self.assertEqual(want, got['canonical_title'])

    def test_info_anime_fail(self):
        anime_name = 'kuroshitsuji'
        want = 404

        try:
            RequestInfoAnime(anime_name).get()
        except Exception as Err:
            self.assertEqual(want, Err.code)


if __name__ == '__main__':
    unittest.main()
