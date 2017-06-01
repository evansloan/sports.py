class TeamError(Exception):
    def __init__(self, sport, team1, team2):
        self.sport = sport
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        return '{} match not found for {} vs {}'.format(self.sport, self.team1, self.team2)


class SportError(Exception):
    def __init__(self, sport):
        self.sport = sport

    def __str__(self):
        return 'Sport not found for {}'.format(self.sport)
