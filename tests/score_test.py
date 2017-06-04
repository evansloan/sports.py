import json
import unittest

from sports_py import scores


class TestScores(unittest.TestCase):
    matches = scores.get_sport_scores('baseball')
    match = scores.get_match_score('baseball', matches[0].home_team, matches[0].away_team)
    team1 = match.home_team
    team2 = match.away_team
    home_score = match.home_score
    away_score = match.away_score
    date = match.match_date
    test = False

    def test_match(self):
        if self.match is not None:
            self.test = True
        self.assertEqual(self.test, True)

    def test_teams(self):
        if self.team1 and self.team2 is not None:
            self.test = True
        self.assertEqual(self.test, True)

    def test_score(self):
        if self.home_score is not None and self.away_score is not None:
            self.test = True
        self.assertEqual(self.test, True)

    def test_date(self):
        if self.date is not None:
            self.test = True
        self.assertEqual(self.test, True)

    def test_sport(self):
        if self.matches is not None:
            self.test = True
        self.assertEqual(self.test, True)

    def test_json(self):
        try:
            json.loads(self.match.to_json())
            for match in self.matches:
                json.loads(match.to_json())
            self.test = True
        except ValueError:
            self.test = False
        self.assertEqual(self.test, True)

if __name__ == '__main__':
    unittest.main()
