import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

titles = ['Upgrade', 'Revanche', 'The Station Agent', 'Fresh', 'The Red Violin', 'Mass', 'The Train']

for title in titles:
    r = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}')
    results = r.json().get('results', [])
    if results:
        m = results[0]
        print(f"{m['title']} ({m.get('release_date','')[:4]}): Rating={m['vote_average']}, Votes={m['vote_count']}")
    else:
        print(f"{title}: NOT FOUND")
