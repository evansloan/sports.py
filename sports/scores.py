import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime

import requests

from sports import constants, errors


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

    def __repr__(self):
        return '{} {}-{} {}'.format(self.home_team, self.home_score,
                                    self.away_score, self.away_team)

    def __str__(self):
        return '{} {}-{} {}'.format(self.home_team, self.home_score,
                                    self.away_score, self.away_team)

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


def _load_xml(sport):
    """
    Parse XML file containing match details using ElementTree
    :param sport: sport being played
    :type sport: string
    :return: ElementTree object containing data from XML file
    """
    try:
        url = 'http://www.scorespro.com/rss2/live-{}.xml'.format(sport)
        r = requests.get(url)
        return ET.fromstring(r.content)
    except ET.ParseError:
        raise errors.SportError(sport)


def get_sport_scores(sport):
    """
    Get live scores for all matches in a particular sport
    :param sport: the sport being played
    :type sport: string
    :return: List containing Match objects
    """
    sport = sport.lower()
    root = _load_xml(sport)

    items = []
    for child in root:
        for c in child:
            if c.tag == 'item':
                items.append(c)

    match_info = {}
    matches = []
    for item in items:
        for child in item:
            if sport == constants.SOCCER:
                if child.tag == 'description':
                    title = child.text
                    i_open = title.index('(')
                    i_close = title.index(')')
                    match_info['league'] = title[i_open + 1:i_close].strip()
                    title = title[i_close + 1:]
                    i_vs = title.index('vs')
                    i_colon = title.index(':')
                    match_info['home_team'] = title[0:i_vs].replace('#', ' ').strip()
                    match_info['away_team'] = title[i_vs + 2:i_colon].replace('#', ' ').strip()
                    title = title[i_colon:]
                    i_hyph = title.index('-')
                    match_info['match_score'] = title[1:i_hyph + 2].strip()
                    title = title[i_hyph + 1:]
                    i_hyph = title.index('-')
                    match_info['match_time'] = title[i_hyph + 1:].strip()
            else:
                if child.tag == 'title':
                    title = child.text
                    i_open = title.index('(')
                    i_close = title.index(')')
                    match_info['league'] = title[i_open + 1:i_close].strip()
                    title = title[i_close + 1:]
                    i_vs = title.index('vs')
                    i_colon = title.index(':')
                    match_info['home_team'] = title[0:i_vs].replace('#', ' ').strip()
                    match_info['away_team'] = title[i_vs + 2:i_colon].replace('#', ' ').strip()
                    match_info['match_score'] = title[i_colon + 1:].strip()

                if child.tag == 'description':
                    match_info['match_time'] = child.text.strip()

            if child.tag == 'pubDate':
                match_info['match_date'] = child.text.strip()
            if child.tag == 'guid':
                match_info['match_link'] = child.text.strip()

        matches.append(Match(sport, match_info))

    return matches


def match(sport, team1, team2):
    """
    Get live scores for a single match
    :param sport: the sport being played
    :param team1: first team participating in the match
    :param team2: second team participating in the match
    :type sport: string
    :type team1: string
    :type team2: string
    :return: Match object
    """
    sport = sport.lower()
    team1_pattern = re.compile(team1, re.I)
    team2_pattern = re.compile(team2, re.I)

    matches = get_sport_scores(sport)
    for match in matches:
        if re.search(team1_pattern, match.home_team) or re.search(team1_pattern, match.away_team) \
                and re.search(team2_pattern, match.away_team) or re.search(team2_pattern, match.home_team):
            return match

    raise errors.MatchError(sport, [team1, team2])


def all_matches():
    """
    Get a list of lists containing all live matches.
    Each sport is contained within its own list
    :return: List containing lists of match objects
    """
    sports = ['baseball', 'basketball', 'hockey', 'football', 'rugby-union',
              'rugby-league', 'tennis', 'soccer', 'handball', 'volleyball']

    matches = {}
    for sport in sports:
        matches[sport] = get_sport_scores(sport)
    return matches
