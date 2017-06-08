[![PyPI](https://img.shields.io/pypi/v/sports.py.svg)](https://pypi.python.org/pypi/sports.py/)
[![Build Status](https://travis-ci.org/evansloan082/sports.py.svg?branch=master)](https://travis-ci.org/evansloan082/sports.py)
[![License](https://img.shields.io/github/license/evansloan082/sports.py.svg)](https://github.com/evansloan082/sports.py/blob/master/LICENSE)


# sports.py
Gather live up-to-date sports scores. Baseball, basketball, cricket, football, handball, hockey, rugby, soccer, tennis, and volleyball currently functional

## Installation
Requires Python 2.7 or Python >= 3.5

`pip install sports_py`

## Usage

sports.py uses two simple functions to get the scores that you want.
 
**Get a single match**

```python
from sports_py import scores
 
match = scores.get_match_score('tennis', 'Murray', 'Federer')
print(match.score)
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
```python
from sports_py import scores
 
matches = scores.get_sport_scores('basketball')
for match in matches:
    print('{0} vs {1}: {2}-{3}'.format(match.home_team, match.away_team,
                                       match.home_score, match.away_score))
```
This returns a list of Match objects which contain the same properties described above

**Get all live matches**
```python
from sports_py import scores
 
all_matches = scores.get_all_matches()
for sport in all_matches:
    for match in sport:
            print('{0} vs {1}: {2}-{3}'.format(match.home_team, match.away_team,
                                               match.home_score, match.away_score))
```

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

**Convert Match objects to JSON**
```python
import json
from sports_py import scores
 
matches = scores.get_sport_scores('hockey')
for match in matches:
    json_data = json.loads(match.to_json())
    print(json_data)
    
pens_game = json.loads(scores.get_match_score('hockey', 'panguins', 'predators').to_json())
print(pens_game)
```

## Credits
Evan Sloan: evansloan082@gmail.com
