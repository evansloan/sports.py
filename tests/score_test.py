import unittest

from sports_py import scores


class TestHockeyScores(unittest.TestCase):
    match1 = scores.get_match_score('hockey', 'penguins', 'predators')
    match2 = scores.get_match_score('hockey', 'pittsburgh', 'nashville')

    def test_teams(self):
        self.assertEqual(self.match1.team1, 'Pittsburgh Penguins')
        self.assertEqual(self.match1.team2, 'Nashville Predators')
        self.assertEqual(self.match2.team1, 'Pittsburgh Penguins')
        self.assertEqual(self.match2.team2, 'Nashville Predators')

    def test_score(self):
        self.assertEqual(self.match1.score, '4-1')

    def test_date(self):
        date = 'Thu, 1 Jun 2017 03:10:14 GMT'
        self.assertEqual(self.match1.game_date, date)


if __name__ == '__main__':
    unittest.main()
