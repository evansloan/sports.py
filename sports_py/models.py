import json
import uuid
from datetime import datetime


class Match:
    def __init__(self, sport, match_info):
        score = match_info['match_score'].split('-')
        self.sport = sport
        self.league = match_info['league']
        self.home_team = match_info['home_team']
        self.away_team = match_info['away_team']
        self.home_score = score[0]
        self.away_score = score[1]
        self.match_time = match_info['match_time']
        self.match_date = datetime.strptime(match_info['match_date'], '%a, %d %b %Y %H:%M:%S %Z')
        self.match_link = match_info['match_link']
        self.uuid = str(uuid.uuid4().hex)

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
                'link': self.match_link
            }
        }
        return json.dumps(data)


class Team:
    def __init__(self, info):
        self.name = info['name']
        self.seasons = info['seasons']
        self.record = info['record']
        self.champs = info['champs']
        self.leaders = info['leaders']
        self.raw = info

    def __str__(self):
        return 'Name: {}\nAll-time record: {}\nChampionships: {}'.format(self.name, self.record, self.champs)


class FootballTeam(Team):
    def __init__(self, info):
        super().__init__(info)
        self.super_bowls = info['super_bowls']
        self.playoff_record = info['playoff_record']


class HockeyTeam(Team):
    def __init__(self, info):
        super().__init__(info)
        self.playoff_app = info['playoff_app']
        self.playoff_record = info['playoff_record']
        self.points = info['points']


class BaseballTeam(Team):
    def __init__(self, info):
        super().__init__(info)
        self.playoff_app = info['playoff_app']
        self.pennants = info['pennants']

