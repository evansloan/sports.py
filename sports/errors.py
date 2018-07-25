class MatchError(Exception):
    def __init__(self, sport, teams):
        self.sport = sport
        self.teams = teams

    def __str__(self):
        return '{} match not found for {}'.format(self.sport, ', '.join(self.teams))


class SportError(Exception):
    def __init__(self, sport):
        self.sport = sport

    def __str__(self):
        return 'Sport not found for {}'.format(self.sport)


class StatsNotFound(Exception):
    def __init__(self, sport):
        self.sport = sport

    def __str__(self):
        return 'Extra stats not yet supported for {}'.format(self.sport)


class TeamNotFoundError(Exception):
    def __init__(self, sport, team):
        self.sport = sport
        self.team = team

    def __str__(self):
        return 'Team {} not found for sport {}'.format(self.team, self.sport)
