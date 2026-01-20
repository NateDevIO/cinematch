"""
Add more hidden gems with expanded criteria:
- Rating threshold: 7.0+ (down from 7.5)
- Pages: 150 (up from 75)
"""
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('TMDB_API_KEY')

# Load existing cache
with open('cinematch-js/movies_cache.json', 'r', encoding='utf-8') as f:
    existing = json.load(f)

existing_ids = {m['id'] for m in existing}
print(f'Existing movies: {len(existing)}')

# Fetch more hidden gems with expanded criteria
print('Fetching expanded hidden gems (7.0+ rating, 100-5000 votes, 150 pages)...')
new_movies = []
for page in range(1, 151):  # 150 pages
    url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}&sort_by=vote_average.desc&vote_average.gte=7.0&vote_count.gte=100&vote_count.lte=5000&page={page}'
    resp = requests.get(url)
    if resp.status_code != 200:
        print(f'Error on page {page}: {resp.status_code}')
        break
    data = resp.json()
    for m in data.get('results', []):
        if m['id'] not in existing_ids:
            existing_ids.add(m['id'])
            new_movies.append({
                'id': m['id'],
                'title': m['title'],
                'year': m.get('release_date', '')[:4],
                'overview': m.get('overview', ''),
                'genres': [],
                'rating': m.get('vote_average'),
                'vote_count': m.get('vote_count'),
                'poster_url': f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get('poster_path') else None,
                'director': None,
                'cast': []
            })
    if page % 20 == 0:
        print(f'  Page {page}/150 - Found {len(new_movies)} new movies so far...')

print(f'New movies found: {len(new_movies)}')

# Merge and save
all_movies = existing + new_movies
with open('cinematch-js/movies_cache.json', 'w', encoding='utf-8') as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=2)

# Also update the root cache
with open('movies_cache.json', 'w', encoding='utf-8') as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=2)

print(f'Total movies now: {len(all_movies)}')
print('Done!')
