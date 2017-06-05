import json


class Match:
    def __init__(self, sport, league, team1, team2, score, match_time, match_date, match_link):
        score = score.split('-')
        self.sport = sport
        self.league = league
        self.home_team = team1
        self.away_team = team2
        self.home_score = score[0]
        self.away_score = score[1]
        self.match_time = match_time
        self.match_date = match_date
        self.match_link = match_link

    def to_json(self):
        """
        Convert match object into JSON
        :return: JSON data containing match info
        """
        data = {
            'match': {
                'sport': self.sport,
                'home_team': self.home_team,
                'away_team': self.away_team,
                'home_score': self.home_score,
                'away_score': self.away_score,
                'time': self.match_time,
                'date': self.match_date,
                'link': self.match_link
            }
        }
        return json.dumps(data)
