import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import requests

from sports_py.errors import SportError, TeamError


class Match:
    def __init__(self, team1, team2, score, match_time, match_date, match_link):
        self.team1 = team1
        self.team2 = team2
        self.score = score
        self.match_time = match_time
        self.match_date = match_date
        self.match_link = match_link


def __load_xml(sport):
    try:
        url = 'http://www.scorespro.com/rss2/live-{}.xml'.format(sport)
        r = requests.get(url)
        root = ET.fromstring(r.content)
        return root
    except ParseError:
        raise SportError(sport)


def get_match_score(sport, team1, team2):
    sport = sport.lower()
    team1 = team1.replace('_', ' ')
    team2 = team2.replace('_', ' ')
    team1_pattern = re.compile(team1, re.IGNORECASE)
    team2_pattern = re.compile(team2, re.IGNORECASE)

    matches = get_sport_scores(sport)
    for match in matches:
        if re.search(team1_pattern, match.team1) and re.search(team2_pattern, match.team2):
            return match
    else:
        raise TeamError(sport, team1, team2)


def get_sport_scores(sport):
    sport = sport.lower()
    root = __load_xml(sport)

    items = []
    for child in root:
        for c in child:
            if c.tag == 'item':
                items.append(c)

    match_info = dict.fromkeys(['team1', 'team2', 'match_score', 'match_time', 'match_date', 'match_link'], '')
    matches = []
    for item in items:
        for child in item:
            if child.tag == 'title':
                title = child.text
                index_bracket = title.index(')')
                title = title[index_bracket + 1:]
                index_vs = title.index('vs')
                index_colon = title.index(':')
                match_info['team1'] = title[0:index_vs].replace('#', ' ').strip()
                match_info['team2'] = title[index_vs + 2:index_colon].replace('#', ' ').strip()
                match_info['match_score'] = title[index_colon + 1:].strip()

            if child.tag == 'description':
                match_info['match_time'] = child.text.strip()
            if child.tag == 'pubDate':
                match_info['match_date'] = child.text.strip()
            if child.tag == 'guid':
                match_info['match_link'] = child.text.strip()

        matches.append(Match(match_info['team1'], match_info['team2'], match_info['match_score'],
                             match_info['match_time'], match_info['match_date'], match_info['match_link']))

    return matches
