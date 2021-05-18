import unittest

from app import status_message, reply_message


class TestAppFunctions(unittest.TestCase):

    def test_status_message(self):
        text = "Raku Ichijou, a first-year student at Bonyari High School, " \
               "is the sole heir to an intimidating yakuza family. Ten years ago, " \
               "Raku promised his childhood friend that they would get married when " \
               "they reunite as teenagers. To seal the deal, the girl had given Raku " \
               "a closed locket, the key to which she took with her when she left him." \
               "\nNow, years later, Raku has grown into a typical teenager, and all he " \
               "wants is to remain as uninvolved in his yakuza background as possible " \
               "while spending his school days alongside his middle school crush Kosaki " \
               "Onodera. However, when the American Bee Hive Gang invades his family's turf, " \
               "Raku's idyllic romantic dreams are sent for a toss as he is dragged into a " \
               "frustrating conflict: Raku is to pretend that he is in a romantic relationship " \
               "with Chitoge Kirisaki, the beautiful daughter of the Bee Hive's chief, so as to " \
               "reduce the friction between the two groups. Unfortunately, reality could not be " \
               "farther from this whopping lie—Raku and Chitoge fall in hate at first sight, as " \
               "the girl is convinced he is a pathetic pushover, and in Raku's eyes, " \
               "Chitoge is about as attractive as a savage gorilla. Nisekoi follows " \
               "the daily antics of this mismatched couple who have been forced to get along for " \
               "the sake of maintaining the city's peace. With many more girls popping up his life, " \
               "all involved with Raku's past somehow, his search for the girl who holds his heart " \
               "and his promise leads him in more unexpected directions than he expects." \
               "\n[Written by MAL Rewrite]"

        got = status_message(text, 120)

        msg = 'Raku Ichijou, a first-year student at Bonyari High School, ' \
              'is the sole heir to an intimidating yakuza family. Ten years '
        last_word_position = 20

        want = {
               'message': msg + '...',
               'idx': last_word_position
        }

        self.assertEqual(got, want)

    def test_reply_message(self):
        text = "Raku Ichijou, a first-year student at Bonyari High School, " \
               "is the sole heir to an intimidating yakuza family. Ten years ago, " \
               "Raku promised his childhood friend that they would get married when " \
               "they reunite as teenagers. To seal the deal, the girl had given Raku " \
               "a closed locket, the key to which she took with her when she left him." \
               "\nNow, years later, Raku has grown into a typical teenager, and all he " \
               "wants is to remain as uninvolved in his yakuza background as possible " \
               "while spending his school days alongside his middle school crush Kosaki " \
               "Onodera. However, when the American Bee Hive Gang invades his family's turf, " \
               "Raku's idyllic romantic dreams are sent for a toss as he is dragged into a " \
               "frustrating conflict: Raku is to pretend that he is in a romantic relationship " \
               "with Chitoge Kirisaki, the beautiful daughter of the Bee Hive's chief, so as to " \
               "reduce the friction between the two groups. Unfortunately, reality could not be " \
               "farther from this whopping lie—Raku and Chitoge fall in hate at first sight, as " \
               "the girl is convinced he is a pathetic pushover, and in Raku's eyes, " \
               "Chitoge is about as attractive as a savage gorilla. Nisekoi follows " \
               "the daily antics of this mismatched couple who have been forced to get along for " \
               "the sake of maintaining the city's peace. With many more girls popping up his life, " \
               "all involved with Raku's past somehow, his search for the girl who holds his heart " \
               "and his promise leads him in more unexpected directions than he expects." \
               "\n[Written by MAL Rewrite]"
        last_word_position = 20

        got = reply_message(text, last_word_position, length=140)

        msg = 'ago, Raku promised his childhood friend that they would get married when ' \
              'they reunite as teenagers. To seal the deal, the girl had given '

        new_last_word_position = 44

        want = {
               'message': msg + '...',
               'idx': new_last_word_position
        }

        self.assertEqual(got, want)
