# matchmaker
[![Build Status](https://travis-ci.org/snake-soft/matchmaker.svg?branch=master)](https://travis-ci.org/snake-soft/matchmaker)
[![Coverage Status](https://coveralls.io/repos/github/snake-soft/matchmaker/badge.svg?branch=master)](https://coveralls.io/github/snake-soft/matchmaker?branch=master)

Table Soccer ranking web-application

There are two kinds of countings:
- Player-based --> Elo-Rating (Like in chess rankings witch little changes)
- Team-based --> Score (Win=2, draw=1, lose=0)

# Deploy for development-server (can be used in lan)
```
git clone https://github.com/snake-soft/matchmaker.git

virtualenv -p python3 venv
source venv/bin/activate

cd ranker
pip install -r requirements.txt

python setup.py
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
# Or use it online
https://matchmaker.hennige-it.de/
