[![PyPI](https://img.shields.io/pypi/v/sports.py.svg)](https://pypi.python.org/pypi/sports.py/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sports.py.svg)](https://pypi.python.org/pypi/sports.py/)

[![Build Status](https://travis-ci.org/evansloan/sports.py.svg?branch=master)](https://travis-ci.org/evansloan/sports.py)
[![Coveralls github branch](https://img.shields.io/coveralls/github/evansloan/sports.py/master.svg)](https://coveralls.io/github/evansloan/sports.py?branch=master)
[![License](https://img.shields.io/github/license/evansloan/sports.py.svg)](https://github.com/evansloan/sports.py/blob/master/LICENSE)


# sports.py
Gather live up-to-date sports scores. Baseball, basketball, cricket, football, handball, hockey, rugby, soccer, tennis, and volleyball currently functional

Scrapes data from:
- [scorespro.com](https://www.scorespro.com/)
- [pro-football-reference.com](https://www.pro-football-reference.com/)
- [baseball-reference.com](https://www.baseball-reference.com/)
- [basketball-reference.com](https://www.basketball-reference.com/)
- [hockey-reference.com](https://www.hockey-reference.com/)

## Installation
Python >= 3.5

`pip install sports.py`

## Usage

```python
import sports
```

Valid sports:
- Baseball: `sports.BASEBALL`
- Basketball: `sports.BASKETBALL`
- Cricket: `sports.CRICKET`
- Football: `sports.FOOTBALL`
- Handball: `sports.HANDBALL`
- Hockey: `sports.HOCKEY`
- Rugby Union: `sports.RUGBY_U`
- Rugby League: `sports.RUGBY_L`
- Soccer: `sports.SOCCER`
- Tennis: `sports.TENNIS`
- Volleyball: `sports.VOLLEYBALL`

**Get a single match**

`get_match()` takes three parameters:

- `sport`: Name of sport being played (see above for a list of valid sports)
- `team1`: Name of city or team in a match (Not case-sensitive)
- `team2`: Name of city or team in a match (Not case-sensitive)

`get_match()` returns a single Match object which contains the following properties:
- `sport`: Sport of the match
- `league`: League of the match
- `home_team`: Home team
- `away_team`: Away team
- `home_score`: Home team score
- `away_score`: Away team score
- `match_time`: Current match time
- `match_date`: Date the match was played
- `match_link`: Link to an XML file containing match data

```python
match = sports.get_match(sports.TENNIS, 'Murray', 'Federer')
```

**Get multiple matches**

`get_sport()` takes one parameter:
- `sport`: Name of sport (see above for list of valid sports)

`get_sport()` returns a list of Match objects which contain the same properties described above

```python
matches = sports.get_sport(sports.BASKETBALL)
```

**Get all live matches**

`all_matches()` returns a dictionary of Match objects grouped by sport conatining data from all live matches.

```python
all_matches = sports.all_matches()
baseball = all_matches['baseball']
```

**Get extra team info**

*Only works with MLB, NBA, NFL, and NHL teams*

Get team information including overall record, championships won and more.

`get_team()` takes two parameters:
- `sport`: Sport of the team the find
- `team`: Name of city or team to find (Not case-sensitive)

Properties available to all valid teams/sports:
- `name`: Name of the team
- `seasons`: Total number of seasons played
- `record`: Overall regular season record
- `champs`: Number of total championships (Includes pre-merger champs for NFL)
- `leaders`: Overall team leaders for certain statistical categories
- `raw`: Dictionary containing all gathered info

Properties available to only MLB teams:
- `pennants`: Total number of AL/NL championships

Properties available to only NFL teams:
- `super_bowls`: Total number of Super Bowls

Properties available to only NHL teams:
- `points`: Total number of regular season points earned

Properties available to both NFL/NHL teams:
- `playoff_record`: Overall playoff record

Properties available to MLB, NBA, NHL teams:
- `playoff_app`: Total number of playoff appearances

```python
pirates = sports.get_team_info(sports.BASEBALL, 'pirates')
print(pirates.pennants)

penguins = sports.get_team_info(sports.HOCKEY, 'penguins')
print(penguins.points)

steelers = sports.get_team_info(sports.FOOTBALL, 'steelers')
print(steelers.super_bowls)

sixers = sports.get_team_info(sports.BASKETBALL, '76ers')
print(sixers.playoff_app)
```
