import re
from datetime import datetime

import requests
from defusedxml import ElementTree as ET

from sports import constants, errors


class Match:
    def __init__(self, sport, match_info):
        self.sport = sport
        self.match_date = datetime.strptime(match_info['match_date'], '%a, %d %b %Y %H:%M:%S %Z')
        self.raw = match_info

        for key, value in match_info.items():
            if key != 'match_date':
                setattr(self, key, value)

        if sport != constants.CRICKET:
            self.home_score = int(self.home_score)
            self.away_score = int(self.away_score)

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
    try:
        r = requests.get(url)
        return _load_xml(r.content)
    except ET.ParseError:
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


def _parse_match_info(match, regex, soccer=False):
    """
    Parse string containing info of a specific match

    :param match: Match data
    :type match: string
    :param regex: Match data pattern
    :type regex: Regex object
    :param soccer: Set to true if match contains soccer data, defaults to False
    :type soccer: bool, optional
    :return: Dictionary containing match information
    :rtype: dict
    """
    match = regex.search(match)

    match_info = {
        'league': match.group(1),
        'home_team': match.group(2),
        'away_team': match.group(3),
        'home_score': match.group(4),
        'away_score': match.group(5)
    }

    if match_info['home_score'] is None:
        match_info['home_score'] = '0'
    if match_info['away_score'] is None:
        match_info['away_score'] = '0'

    if soccer:
        match_info['match_time'] = match[6]

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

    cricket_regex = re.compile(r'\(([^)]+)\) #([.,\'"\-\w\d\s]+) vs #([.,\'"\-\w\d\s]+): ([\d/]+\s\([^)]+\))? ?- ([\d/]+\s\([^)]+\))?')
    soccer_regex = re.compile(r'\(([^)]+)\) #([.,\'"\-\w\d\s]+) vs #([.,\'"\-\w\d\s]+): (\d+)-(\d+)\. ([\w\s]+)')
    regex = re.compile(r'\(([^)]+)\) #([.,\'"\-\w\d\s]+) vs #([.,\'"\-\w\d\s]+): (\d+)-(\d+)')

    matches = []
    for match in data:
        if sport == constants.SOCCER:
            try:
                match_string = match.find('description').text
                match_info = _parse_match_info(match_string, soccer_regex, soccer=True)
            except (AttributeError, TypeError):
                match_string = match.find('title').text
                match_info = _parse_match_info(match_string, regex)
        else:
            if sport == constants.CRICKET:
                regex = cricket_regex
            match_string = match.find('title').text
            match_info = _parse_match_info(match_string, regex)
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
