import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import requests

from sports_py import errors, models


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
        root = ET.fromstring(r.content)
        return root
    except ParseError:
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
            if sport == 'soccer':
                if child.tag == 'description':
                    title = child.text
                    index_open = title.index('(')
                    index_close = title.index(')')
                    match_info['league'] = title[index_open+1:index_close].strip()
                    title = title[index_close+1:]
                    index_vs = title.index('vs')
                    index_colon = title.index(':')
                    match_info['home_team'] = title[0:index_vs].replace('#', ' ').strip()
                    match_info['away_team'] = title[index_vs+2:index_colon].replace('#', ' ').strip()
                    title = title[index_colon:]
                    index_hyph = title.index('-')
                    match_info['match_score'] = title[1:index_hyph+2].strip()
                    title = title[index_hyph+1:]
                    index_hyph = title.index('-')
                    match_info['match_time'] = title[index_hyph+1:].strip()
            else:
                if child.tag == 'title':
                    title = child.text
                    index_open = title.index('(')
                    index_close = title.index(')')
                    match_info['league'] = title[index_open+1:index_close].strip()
                    title = title[index_close+1:]
                    index_vs = title.index('vs')
                    index_colon = title.index(':')
                    match_info['home_team'] = title[0:index_vs].replace('#', ' ').strip()
                    match_info['away_team'] = title[index_vs+2:index_colon].replace('#', ' ').strip()
                    match_info['match_score'] = title[index_colon+1:].strip()

                if child.tag == 'description':
                    match_info['match_time'] = child.text.strip()

            if child.tag == 'pubDate':
                match_info['match_date'] = child.text.strip()
            if child.tag == 'guid':
                match_info['match_link'] = child.text.strip()

        matches.append(models.Match(sport, match_info))

    return matches


def get_match_score(sport, team1, team2):
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
    team1_pattern = re.compile(team1, re.IGNORECASE)
    team2_pattern = re.compile(team2, re.IGNORECASE)

    matches = get_sport_scores(sport)
    for match in matches:
        if re.search(team1_pattern, match.home_team) or re.search(team1_pattern, match.away_team) \
                and re.search(team2_pattern, match.away_team) or re.search(team2_pattern, match.home_team):
            return match

    raise errors.MatchError(sport, [team1, team2])


def get_all_matches():
    """
    Get a list of lists containing all live matches.
    Each sport is contained within its own list
    :return: List containing lists of match objects
    """
    sports = ['baseball', 'basketball', 'hockey', 'football', 'rugby-union',
              'rugby-league', 'tennis', 'soccer', 'handball', 'volleyball']

    all_matches = []
    for sport in sports:
        all_matches.append(get_sport_scores(sport))

    return all_matches
