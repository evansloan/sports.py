import json
from datetime import datetime


class Match:
    def __init__(self, sport, match_info):
        score = match_info['match_score'].split('-')
        self.sport = sport
        self.home_score = score[0]
        self.away_score = score[1]
        self.match_date = datetime.strptime(match_info['match_date'], '%a, %d %b %Y %H:%M:%S %Z')

        for key, value in match_info.items():
            if key not in ('match_score', 'match_date'):
                setattr(self, key, value)

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
                'match_time': self.match_time,
                'match_link': self.match_link
            }
        }
        return json.dumps(data)


class Team:
    def __init__(self, info):
        for key, value in info.items():
            setattr(self, key, value)

        self.raw = info

    def __str__(self):
        return 'Name: {}\nAll-time record: {}\nChampionships: {}'.format(self.name, self.record, self.champs)
