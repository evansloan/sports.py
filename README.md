[![PyPI](https://img.shields.io/pypi/v/sports.py.svg)](https://pypi.python.org/pypi/sports.py/)
[![Build Status](https://travis-ci.org/evansloan082/sports.py.svg?branch=master)](https://travis-ci.org/evansloan082/sports.py)
[![License](https://img.shields.io/github/license/evansloan082/sports.py.svg)](https://github.com/evansloan082/sports.py/blob/master/LICENSE)


# sports.py
Gather live up-to-date sports scores. Baseball, basketball, cricket, football, handball, hockey, rugby, soccer, tennis, and volleyball currently functional

## Installation
Requires Python 2.7 or Python >= 3.5

`pip install sports.py`

## Usage

List of valid sports:
- Baseball: `baseball`
- Basketball: `basketball`
- Cricket: `cricket`
- Football: `football`
- Handball: `handball`
- Hockey: `hockey`
- Rugby: `rugby-union` or `rugby-league`
- Soccer: `soccer`
- Tennis: `tennis`
- Volleyball: `volleyball`

**Get a single match**

`get_match_score()` takes three parameters:

- `sport`: Name of sport being played (see above for a list of valid sports)
- `team1`: Name of city of a team in a match (Not case-sensitive)
- `team2`: Name of city of a team in a match (Not case-sensitive)

```python
import sports_py

match = sports_py.get_match_score('tennis', 'Murray', 'Federer')
print('{}-{}'.format(match.home_score, match.away_score))
```

This returns a single Match object which contains the following properties:
- `sport`: Sport of the match
- `league`: League of the match
- `home_team`: Home team
- `away_team`: Away team
- `home_score`: Home team score
- `away_score`: Away team score
- `match_time`: Current match time
- `match_date`: datetime object: date the match was played
- `match_link`: Link to an XML file containing match data

**Get multiple matches**

`get_sport_scores()` takes one parameter:
- `sport`: Name of sport (see above for list of valid sports)

```python
import sports_py

matches = sports_py.get_sport_scores('basketball')
for match in matches:
    print('{} vs {}: {}-{}'.format(match.home_team, match.away_team,
                                       match.home_score, match.away_score))
```
This returns a list of Match objects which contain the same properties described above

**Get all live matches**
```python
import sports_py

all_matches = sports_py.get_all_matches()
for sport in all_matches:
    for match in sport:
            print('{} vs {}: {}-{}'.format(match.home_team, match.away_team,
                                               match.home_score, match.away_score))
```

**Convert Match objects to JSON**
```python
import sports_py

pens_json = sports_py.get_match_score('hockey', 'panguins', 'predators').to_json()
print(pens_game)
```

**Get extra team info**

*Only works with MLB, NFL, and NHL teams*

Get team information including overall record, championships won and more.

`get_team_info()` takes two parameters:
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

Properties available to both MLB/NHL teams:
- `playoff_app`: Total number of playoff appearances

```python
import sports_py

pirates = sports_py.get_team_info('baseball', 'pirates')
print(pirates.pennants)

penguins = sports_py.get_team_info('hockey', 'penguins')
print(penguins.points)

steelers = sports_py.get_team_info('football', 'steelers')
print(steelers.super_bowls)
```

## Credits
Evan Sloan: evansloan082@gmail.com
