import re
from datetime import datetime

import requests
from defusedxml import ElementTree as ET

from sports import constants, errors


class Match:
    def __init__(self, sport, match_info):
        score = match_info['match_score'].split('-')
        self.sport = sport

        try:
            self.home_score = int(score[0])
            self.away_score = int(score[1])
        except ValueError:
            self.home_score = 0
            self.away_score = 0

        self.match_date = datetime.strptime(match_info['match_date'], '%a, %d %b %Y %H:%M:%S %Z')
        self.raw = match_info

        for key, value in match_info.items():
            if key not in ('match_score', 'match_date'):
                setattr(self, key, value)

    def __repr__(self):
        return '{} {}-{} {}'.format(self.home_team, self.home_score,
                                    self.away_score, self.away_team)

    def __str__(self):
        return '{} {}-{} {}'.format(self.home_team, self.home_score,
                                    self.away_score, self.away_team)


def _request_xml(sport):
    """
    Request XML data from scorespro.com

    :param sport: sport being played
    :type sport: string
    :return: XML data
    :rtype: string
    """
    url = 'http://www.scorespro.com/rss2/live-{}.xml'.format(sport)
    r = requests.get(url)
    if r.ok:
        return _load_xml(r.content)
    else:
        raise errors.SportError(sport)


def _load_xml(xml_data):
    """
    Parse XML file containing match details using ElementTree

    :param xml_data: Data containing match info for a specific sport
    :type xml_data: string
    :return: ElementTree instance containing data from XML file
    :rtype: ElementTree instance
    """
    return ET.fromstring(xml_data).find('channel').findall('item')


def _parse_match_info(match, soccer=False):
    """
    Parse string containing info of a specific match

    :param match: Match data
    :type match: string
    :param soccer: Set to true if match contains soccer data, defaults to False
    :type soccer: bool, optional
    :return: Dictionary containing match information
    :rtype: dict
    """
    match_info = {}

    i_open = match.index('(')
    i_close = match.index(')')
    match_info['league'] = match[i_open + 1:i_close].strip()

    match = match[i_close + 1:]
    i_vs = match.index('vs')
    i_colon = match.index(':')
    match_info['home_team'] = match[0:i_vs].replace('#', ' ').strip()
    match_info['away_team'] = match[i_vs + 2:i_colon].replace('#', ' ').strip()
    match = match[i_colon:]
    i_hyph = match.index('-')
    match_info['match_score'] = match[1:i_hyph + 2].strip()

    return match_info


def get_sport(sport):
    """
    Get live scores for all matches in a particular sport

    :param sport: the sport being played
    :type sport: string
    :return: List containing Match objects
    :rtype: list
    """
    sport = sport.lower()
    data = _request_xml(sport)

    matches = []
    for match in data:
        desc = match.find('title').text
        match_info = _parse_match_info(desc)
        match_info['match_time'] = match.find('description').text
        match_info['match_date'] = match.find('pubDate').text
        match_info['match_link'] = match.find('guid').text

        matches.append(Match(sport, match_info))

    return matches


def get_match(sport, team1, team2):
    """
    Get live scores for a single match

    :param sport: the sport being played
    :type sport: string
    :param team1: first team participating in the match
    :ttype team1: string
    :param team2: second team participating in the match
    :type team2: string
    :return: A specific match
    :rtype: Match
    """
    sport = sport.lower()
    team1_pattern = re.compile(team1, re.I)
    team2_pattern = re.compile(team2, re.I)

    matches = get_sport(sport)
    for match in matches:
        if re.search(team1_pattern, match.home_team) or re.search(team1_pattern, match.away_team) \
                and re.search(team2_pattern, match.away_team) or re.search(team2_pattern, match.home_team):
            return match

    raise errors.MatchError(sport, [team1, team2])


def all_matches():
    """
    Get a dictionary of all live and recently concluded matches.
    Each entry in the dictionary is a list containing the matches for a
    specific sport.

    :return: Dict containing match objects grouped by sport
    :rtype: dict
    """
    return {sport: get_sport(sport) for sport in constants.SPORTS}
