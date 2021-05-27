import unittest

from models.finished_anime import FinishedAnime


class TestFinishedAnime(unittest.TestCase):
    def test_get_canonical_title_one_word_lowercase(self):
        anime_slug = 'naruto'

        want = 'Naruto'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_two_words_lowercase(self):
        anime_slug = 'one-piece'

        want = 'One Piece'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_three_words_lowercase(self):
        anime_slug = 'prince-of-tennis'

        want = 'Prince of Tennis'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_four_words_lowercase(self):
        anime_slug = 'ghost-in-the-shell'

        want = 'Ghost in the Shell'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_one_word_uppercase(self):
        anime_slug = 'NARUTO'

        want = 'Naruto'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_two_words_uppercase(self):
        anime_slug = 'ONE-PIECE'

        want = 'One Piece'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_three_words_uppercase(self):
        anime_slug = 'PRINCE-OF-TENNIS'

        want = 'Prince of Tennis'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_four_words_uppercase(self):
        anime_slug = 'GHOST-IN-THE-SHELL'

        want = 'Ghost in the Shell'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_one_word_with_lower_and_upper_letters(self):
        anime_slug = 'NaRuTo'

        want = 'Naruto'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_two_words_with_lower_and_upper_letters(self):
        anime_slug = 'OnE-PiEcE'

        want = 'One Piece'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_get_canonical_title_three_words_with_lower_and_upper_letters(self):
        anime_slug = 'PrInCe-Of-TEnNiS'

        want = 'Prince of Tennis'

        got = FinishedAnime(anime_name=anime_slug).canonical_title

        self.assertEqual(want, got)

    def test_attributes(self):
        anime = 'Naruto'
        finished_anime = FinishedAnime(anime)

        self.assertTrue(hasattr(finished_anime, "id"))
        self.assertTrue(hasattr(finished_anime, "canonical_title"))
        self.assertTrue(hasattr(finished_anime, "finished_at"))
        self.assertTrue(hasattr(finished_anime, "is_published"))

    def test_repr(self):
        anime = 'naruto'
        finished_anime = FinishedAnime(anime)

        want = f'<Anime viewed: Naruto>'

        got = str(finished_anime)

        self.assertEqual(want, got)


if __name__ == '__main__':
    unittest.main()
