[![PyPI](https://img.shields.io/pypi/v/sports.py.svg)](https://pypi.python.org/pypi/sports.py/1.0.2)
[![Build Status](https://travis-ci.org/evansloan082/sports.py.svg?branch=master)](https://travis-ci.org/evansloan082/sports.py)
[![License](https://img.shields.io/github/license/evansloan082/sports.py.svg)](https://github.com/evansloan082/sports.py/blob/master/LICENSE)


# sports.py
Gather live up-to-date sports scores. Baseball, basketball, football, hockey, and tennis currently functional
## Installation
Requires Python >= 3.5

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
- team1: Home team
- team2: Away team
- score: The score of the match
- match_time: Current match time
- match_date: The date of the match
- match_link: Link to an XML file containing match data

**Get multiple matches**
```python
from sports_py import scores
matches = scores.get_sport_scores('basketball')
for match in matches:
    print('{0} vs {1}: {2}'.format(match.team1, match.team2, match.score))
```

This returns a list of Match objects which contain the same properties described above

## Contributing
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
## History
*June 1st, 2017:* version 1.0.2 released
## Credits
Evan Sloan: evansloan082@gmail.com
