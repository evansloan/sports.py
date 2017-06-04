import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import requests

from sports_py.errors import MatchError, SportError
from sports_py.match import Match


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
        raise SportError(sport)


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

    match_info = dict.fromkeys(['team1', 'team2', 'match_score', 'match_time', 'match_date', 'match_link'], '')
    matches = []
    for item in items:
        for child in item:
            if sport == 'soccer':
                if child.tag == 'description':
                    title = child.text
                    index_bracket = title.index(')')
                    title = title[index_bracket+1:]
                    index_vs = title.index('vs')
                    index_colon = title.index(':')
                    index_hyph = title.index('-')
                    match_info['team1'] = title[0:index_vs].replace('#', ' ').strip()
                    match_info['team2'] = title[index_vs+2:index_colon].replace('#', ' ').strip()
                    match_info['match_score'] = title[index_colon + 1:index_hyph].strip()
                    match_info['match_time'] = title[index_hyph+1:].strip()
            else:
                if child.tag == 'title':
                    title = child.text
                    index_bracket = title.index(')')
                    title = title[index_bracket+1:]
                    index_vs = title.index('vs')
                    index_colon = title.index(':')
                    match_info['team1'] = title[0:index_vs].replace('#', ' ').strip()
                    match_info['team2'] = title[index_vs+2:index_colon].replace('#', ' ').strip()
                    match_info['match_score'] = title[index_colon+1:].strip()

            if child.tag == 'description':
                match_info['match_time'] = child.text.strip()
            if child.tag == 'pubDate':
                match_info['match_date'] = child.text.strip()
            if child.tag == 'guid':
                match_info['match_link'] = child.text.strip()

        matches.append(Match(match_info['team1'], match_info['team2'], match_info['match_score'],
                             match_info['match_time'], match_info['match_date'], match_info['match_link']))

    return matches


def get_match_score(sport, home_team, away_team):
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
    team1_pattern = re.compile(home_team, re.IGNORECASE)
    team2_pattern = re.compile(away_team, re.IGNORECASE)

    matches = get_sport_scores(sport)
    for match in matches:
        if re.search(team1_pattern, match.home_team) or re.search(team1_pattern, match.away_team) \
                and re.search(team2_pattern, match.away_team) or re.search(team2_pattern, match.home_team):
            return match
        else:
            raise MatchError(sport, home_team, away_team)
