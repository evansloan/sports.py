import re

import requests
from bs4 import BeautifulSoup, SoupStrainer

from sports_py import errors, models


def get_team_info(sport, team):
    """
    Get extra info that pertains to a certain team.
        Info available to all teams:
            - name: Name of the team
            - seasons: Number of seasons played
            - record: Overall record
            - champs: Number of championships won
            - leaders: Statistical leaders

        Info specific to baseball teams:
            - pennants: Number of times a team has won AL/NL league

        Info specific to football teams:
            - super_bowls: Number of Super Bowls won

        Info specific to hockey teams:
            - points: Number of overall points gained throughout all seasons played

        Info specific to baseball/hockey teams:
            - playoff_app: Total number of playoff appearances

        Info specific to football/hockey teams:
            - playoff_record: Overall record in the playoffs

    :param sport: The sport of the team to look for (baseball, football, hockey)
    :param team: The name/city of the team to look for
    :return: Team object containing information described above
    """
    team_pattern = re.compile(team, re.IGNORECASE)

    supported_sports = ['baseball', 'football', 'hockey']
    if sport not in supported_sports:
        raise errors.StatsNotFound(sport)
    elif sport == 'football':
        return _get_football_team_info(team_pattern, team)

    base_url = 'https://www.{}-reference.com/teams/'.format(sport)
    table_id = 'active_franchises' if sport == 'hockey' else 'teams_active'
    links = SoupStrainer('table', {'id': table_id})
    soup = BeautifulSoup(requests.get(base_url).content, 'html.parser', parse_only=links)

    team_info_raw = _get_team_info_raw(soup, base_url, team_pattern, team, sport)

    if sport == 'baseball':
        team_info = {
            'name': team_info_raw[0],
            'record': team_info_raw[9].strip(),
            'seasons': ' '.join(team_info_raw[5:7]),
            'playoff_app': team_info_raw[11].strip(),
            'pennants': team_info_raw[13].strip(),
            'champs': team_info_raw[15].strip(),
            'leaders': ' '.join(team_info_raw[16:18])
        }
        return models.BaseballTeam(team_info)

    elif sport == 'hockey':
        team_info = {
            'name': team_info_raw[0],
            'record': team_info_raw[9].strip(),
            'points': team_info_raw[10][1:-1],
            'seasons': team_info_raw[2].split()[1],
            'playoff_app': team_info_raw[3].split()[3],
            'playoff_record': team_info_raw[7].split()[2],
            'champs': team_info_raw[5],
            'leaders': [
                team_info_raw[11:13],
                ' '.join(team_info_raw[13:15]),
                ' '.join(team_info_raw[15:17])
            ]
        }
        return models.HockeyTeam(team_info)


def _get_football_team_info(team_pattern, team):
    """
    Parses through raw data about NFL teams

    :param team_pattern: Cpomiled regex pattern of team name/city
    :param team: Name of the team that is being searched for
    :param sport: Sport that is being searched for (always football)
    :return: FootballTeam object.
    """
    base_url = 'https://www.pro-football-reference.com/teams/'
    links = SoupStrainer('table', {'id': 'teams_active'})
    soup = BeautifulSoup(requests.get(base_url).content, 'html.parser', parse_only=links)

    team_info_raw = _get_team_info_raw(soup, base_url, team_pattern, team, 'football')

    team_info = {
        'name': team_info_raw[0],
        'seasons': team_info_raw[2].split()[1],
        'record': team_info_raw[4],
        'playoff_record': team_info_raw[5].split()[2],
        'super_bowls': team_info_raw[7].strip(),
        'champs': team_info_raw[10],
        'leaders': team_info_raw[11:17]
    }

    return models.FootballTeam(team_info)


def _get_team_info_raw(soup, base_url, team_pattern, team, sport):
    """
    Parses through html page to gather raw data about team

    :param soup: BeautifulSoup object containing html to be parsed
    :param base_url: Pre-formatted url that is formatted depending on sport
    :param team_pattern: Compiled regex pattern of team name/city
    :param team: Name of the team that is being searched for
    :param sport: Sport that is being searched for
    :return: List containing raw data of team
    """
    team_url = None
    team_name = None
    for link in soup.find_all('a'):
        if re.search(team_pattern, link.string):
            team_url = base_url.replace('/teams/', '') + link['href']
            team_name = link.string

    if team_url is not None and team_name is not None:
        team_soup = BeautifulSoup(requests.get(team_url).content, 'html.parser')
        team_info_raw = team_soup.find('div', id='meta').contents[3].get_text().split('\n')
        team_info_raw = [x.replace('\t', '') for x in team_info_raw]
        team_info_raw = [x for x in team_info_raw if x != '']
        team_info_raw[0] = team_name
    else:
        raise errors.TeamNotFoundError(sport, team)

    return team_info_raw
