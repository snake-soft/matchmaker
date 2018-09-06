# ranker
Table Soccer ranking web-application

There are two kinds of countings:
- Player-based --> Elo-Rating (Like in chess rankings witch little changes)
- Team-based --> Score (Win=2, draw=1, lose=0)

# Deploy for development-server (can be used in lan)
'''
git clone https://github.com/snake-soft/ranker.git

virtualenv -p python3 venv
source venv/bin/activate

cd ranker
pip install -r requirements.txt

python setup.py
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
'''

https://matchmaker.hennige-it.de/
