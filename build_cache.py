"""
Movie Data Cache Builder
Run this script once to pre-fetch and cache movies from TMDB.
Fetches from multiple sources to ensure classics and popular films are included.

Usage: python build_cache.py
"""

import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CACHE_FILE = "movies_cache.json"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_details(api_key: str, movie_id: int) -> dict:
    """Fetch full details for a single movie."""
    try:
        # Get movie details
        movie_resp = requests.get(
            f"{BASE_URL}/movie/{movie_id}",
            params={'api_key': api_key}
        )
        movie = movie_resp.json()
        
        # Get credits
        credits_resp = requests.get(
            f"{BASE_URL}/movie/{movie_id}/credits",
            params={'api_key': api_key}
        )
        credits = credits_resp.json()
        
        # Extract director
        director = None
        if credits.get('crew'):
            directors = [p for p in credits['crew'] if p['job'] == 'Director']
            if directors:
                director = directors[0]['name']
        
        # Extract cast
        cast = [p['name'] for p in credits.get('cast', [])[:5]]
        
        return {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'year': movie.get('release_date', '')[:4] if movie.get('release_date') else None,
            'overview': movie.get('overview'),
            'genres': [g['name'] for g in movie.get('genres', [])],
            'rating': movie.get('vote_average'),
            'vote_count': movie.get('vote_count'),
            'poster_url': f"{IMAGE_BASE_URL}{movie['poster_path']}" if movie.get('poster_path') else None,
            'director': director,
            'cast': cast
        }
    except Exception as e:
        return None


def fetch_movies_from_endpoint(api_key: str, endpoint: str, params: dict, 
                                max_movies: int, seen_ids: set) -> list:
    """Fetch movies from a specific TMDB endpoint."""
    movies = []
    pages_needed = (max_movies // 20) + 1
    
    for page in range(1, min(pages_needed + 1, 26)):
        request_params = {'api_key': api_key, 'page': page, **params}
        response = requests.get(f"{BASE_URL}{endpoint}", params=request_params)
        
        if response.status_code != 200:
            continue
            
        data = response.json()
        
        for movie_data in data.get('results', []):
            movie_id = movie_data['id']
            
            # Skip if we already have this movie
            if movie_id in seen_ids:
                continue
            
            movie = get_movie_details(api_key, movie_id)
            if movie and movie.get('overview') and movie.get('genres'):
                movies.append(movie)
                seen_ids.add(movie_id)
                # Use ASCII-safe printing for Windows console
                safe_title = movie['title'].encode('ascii', 'replace').decode('ascii')
                print(f"    + {safe_title} ({movie['year']})".ljust(60), end="\r")
                
            if len(movies) >= max_movies:
                break
        
        if len(movies) >= max_movies:
            break
    return movies


def search_movie_by_title(api_key: str, title: str, seen_ids: set) -> dict:
    """Search for a specific movie by title and return its details."""
    try:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={'api_key': api_key, 'query': title}
        )
        if response.status_code != 200:
            return None
        
        results = response.json().get('results', [])
        if not results:
            return None
        
        # Get the first result (best match)
        movie_id = results[0]['id']
        if movie_id in seen_ids:
            return None
        
        movie = get_movie_details(api_key, movie_id)
        if movie and movie.get('overview') and movie.get('genres'):
            seen_ids.add(movie_id)
            return movie
        return None
    except Exception:
        return None


# List of movies that should always be included
MUST_HAVE_MOVIES = [
    "Elf",
    "National Lampoon's Christmas Vacation",
    "Home Alone",
    "It's a Wonderful Life",
    "A Christmas Story",
    "The Santa Clause",
    "Miracle on 34th Street",
    "A Christmas Carol",
    "Scrooged",
    "Bad Santa",
    "The Holiday",
    "Jingle All the Way",
    "Fred Claus",
    "Four Christmases",
    # User-requested additions
    "Nobody",
    "Brokeback Mountain",
    "The Whale",
    "A Man Called Otto"
]


def build_cache():
    """
    Fetch movies from multiple TMDB sources and save to local JSON cache.
    """
    print("[*] Building comprehensive movie cache from TMDB...")
    print("This will take several minutes. Please wait...\n")
    
    # Check for API key
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("[ERROR] TMDB_API_KEY not found in .env file")
        return False
    
    all_movies = []
    seen_ids = set()
    
    # 1. TOP RATED MOVIES (includes classics like Shawshank, Godfather, etc.)
    print("\n[1/6] Fetching Top Rated movies (classics)...")
    top_rated = fetch_movies_from_endpoint(
        api_key, "/movie/top_rated", {}, 500, seen_ids  # Increased from 200
    )
    all_movies.extend(top_rated)
    print(f"\n      Fetched {len(top_rated)} top rated movies")
    
    # 2. POPULAR MOVIES (current trending)
    print("\n[2/6] Fetching Popular movies (trending)...")
    popular = fetch_movies_from_endpoint(
        api_key, "/movie/popular", {}, 300, seen_ids  # Increased from 200
    )
    all_movies.extend(popular)
    print(f"\n      Fetched {len(popular)} popular movies")
    
    # 3. HIGHLY VOTED MOVIES (broad coverage of mainstream films)
    print("\n[3/7] Fetching highly voted movies...")
    discover_voted = fetch_movies_from_endpoint(
        api_key, "/discover/movie",
        {'sort_by': 'vote_count.desc', 'vote_count.gte': 500},  # Lowered from 2000
        1000, seen_ids  # Increased from 500
    )
    all_movies.extend(discover_voted)
    print(f"\n      Fetched {len(discover_voted)} highly voted movies")
    
    # 4. DECADE-BY-DECADE COVERAGE (1970s-2020s comprehensive)
    print("\n[4/7] Fetching movies by decade...")
    decades_movies = []
    for decade_start in [1970, 1980, 1990, 2000, 2010, 2020]:
        decade_movies = fetch_movies_from_endpoint(
            api_key, "/discover/movie",
            {
                'sort_by': 'vote_count.desc',  # Changed to vote_count for wider coverage
                'vote_count.gte': 200,  # Lowered from 1000
                'primary_release_date.gte': f'{decade_start}-01-01',
                'primary_release_date.lte': f'{decade_start + 9}-12-31'
            },
            150, seen_ids  # Increased from 50
        )
        decades_movies.extend(decade_movies)
    all_movies.extend(decades_movies)
    print(f"\n      Fetched {len(decades_movies)} decade movies")
    
    # 5. CHRISTMAS/HOLIDAY MOVIES (using keyword search)
    print("\n[5/7] Fetching Christmas/Holiday movies...")
    # TMDB keyword IDs: 207317=christmas, 1445=holiday
    christmas_movies = fetch_movies_from_endpoint(
        api_key, "/discover/movie",
        {
            'with_keywords': '207317|1445|9715',  # christmas, holiday, christmas eve
            'sort_by': 'vote_count.desc',
            'vote_count.gte': 100
        },
        100, seen_ids
    )
    all_movies.extend(christmas_movies)
    print(f"\n      Fetched {len(christmas_movies)} Christmas/Holiday movies")
    
    # 6. MUST-HAVE CLASSICS (search by title)
    print("\n[6/7] Adding must-have classic movies...")
    must_have_added = 0
    for title in MUST_HAVE_MOVIES:
        movie = search_movie_by_title(api_key, title, seen_ids)
        if movie:
            all_movies.append(movie)
            must_have_added += 1
            safe_title = movie['title'].encode('ascii', 'replace').decode('ascii')
            print(f"    + {safe_title} ({movie['year']})".ljust(60), end="\r")
    print(f"\n      Added {must_have_added} must-have classics")
    
    # Summary
    print(f"\n\n[OK] Total unique movies: {len(all_movies)}")
    
    # Save to JSON
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Saved to {CACHE_FILE}")
    print(f"\n[DONE] The app will now load {len(all_movies)} movies instantly!")
    
    return True


if __name__ == "__main__":
    build_cache()
