import unittest

import sports


class TestScores(unittest.TestCase):
    hockey_data = {
        'league': 'NHL',
        'home_team': 'Pittsburgh Penguins',
        'away_team': 'Nashville Predators',
        'match_score': '2-0',
        'match_date': 'Sat, 19 Aug 2017 02:12:05 GMT',
        'match_time': 'Game Finished',
        'match_link': 'test',
    }

    hockey_match = sports.scores.Match(sports.HOCKEY, hockey_data)

    def test_xml(self):
        try:
            sports.scores._request_xml(sports.BASEBALL)
        except sports.errors.SportError:
            self.fail('XML request raised SportError')

        self.assertRaises(sports.errors.SportError, sports.scores._request_xml, 'fake sport')

    def test_match(self):
        self.assertIsNotNone(self.hockey_match)
        self.assertEqual(str(self.hockey_match), 'Pittsburgh Penguins 2-0 Nashville Predators')
        self.assertEqual(repr(self.hockey_match), 'Pittsburgh Penguins 2-0 Nashville Predators')

        self.assertIsNotNone(sports.all_matches())

    def test_teams(self):
        self.assertEqual(self.hockey_match.home_team, 'Pittsburgh Penguins')
        self.assertEqual(self.hockey_match.away_team, 'Nashville Predators')

    def test_score(self):
        self.assertEqual(self.hockey_match.home_score, 2)
        self.assertEqual(self.hockey_match.away_score, 0)

    def test_date(self):
        self.assertIsNotNone(self.hockey_match.match_date)

    def test_sport(self):
        self.assertEqual(self.hockey_match.sport, sports.HOCKEY)
        self.assertIsNone(sports.get_sport(sports.SOCCER))


if __name__ == '__main__':
    unittest.main()
