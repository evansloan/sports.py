import unittest

import sports


class TestScores(unittest.TestCase):
    match_data = {
        'league': 'NHL',
        'home_team': 'Pittsburgh Penguins',
        'away_team': 'Nashville Predators',
        'match_score': '2-0',
        'match_date': 'Sat, 19 Aug 2017 02:12:05 GMT',
        'match_time': 'Game Finished',
        'match_link': 'test',
    }

    match = sports.scores.Match(sports.HOCKEY, match_data)
    matches = sports.get_sport(sports.BASEBALL)

    def test_xml(self):
        try:
            sports.scores._request_xml(sports.BASEBALL)
        except sports.errors.SportError:
            self.fail('XML request raised SportError')

        self.assertRaises(sports.errors.SportError, sports.scores._request_xml, 'fake sport')

    def test_match(self):
        self.assertIsNotNone(self.match)
        self.assertEqual(str(self.match), 'Pittsburgh Penguins 2-0 Nashville Predators')
        self.assertEqual(repr(self.match), 'Pittsburgh Penguins 2-0 Nashville Predators')

    def test_teams(self):
        self.assertEqual(self.match.home_team, 'Pittsburgh Penguins')
        self.assertEqual(self.match.away_team, 'Nashville Predators')

    def test_score(self):
        self.assertEqual(self.match.home_score, 2)
        self.assertEqual(self.match.away_score, 0)

    def test_date(self):
        self.assertIsNotNone(self.match.match_date)

    def test_sport(self):
        self.assertEqual(self.match.sport, sports.HOCKEY)


if __name__ == '__main__':
    unittest.main()
