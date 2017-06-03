import json


class Match:
    def __init__(self, team1, team2, score, match_time, match_date, match_link):
        self.team1 = team1
        self.team2 = team2
        self.score = score
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
                'team1': self.team1,
                'team2': self.team2,
                'score': self.score,
                'time': self.match_time,
                'date': self.match_date,
                'link': self.match_link
            }
        }
        json_data = json.dumps(data)

        return json_data
