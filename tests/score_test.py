import unittest

from sports_py import scores


class TestScores(unittest.TestCase):
    matches = scores.get_sport_scores('baseball')
    match = scores.get_match_score('baseball', matches[0].team1, matches[0].team2)
    team1 = match.team1
    team2 = match.team2
    score = match.score
    date = match.match_date

    def test_teams(self):
        if self.team1 and self.team2 is not None:
            test = True
        else:
            test = False
        self.assertEqual(test, True)

    def test_score(self):
        if self.score is not None:
            test = True
        else:
            test = False
        self.assertEqual(test, True)

    def test_date(self):
        if self.date is not None:
            test = True
        else:
            test = False
        self.assertEqual(test, True)

    def test_sport(self):
        if self.matches is not None:
            test = True
        else:
            test = False
        self.assertEqual(test, True)


if __name__ == '__main__':
    unittest.main()
