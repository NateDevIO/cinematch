"""
Data Loader Module
Handles loading movie data from TMDB API or local datasets
"""

import pandas as pd
import requests
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()


class TMDBDataLoader:
    """
    Loads movie data from The Movie Database (TMDB) API.
    
    Get your free API key at: https://www.themoviedb.org/settings/api
    """
    
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TMDB data loader.
        
        Args:
            api_key: TMDB API key (if None, reads from environment variable)
        """
        self.api_key = api_key or os.getenv("TMDB_API_KEY")
        
        # Check if API key is missing or is the placeholder value
        if not self.api_key or self.api_key == "your_api_key_here":
            self.api_key = None  # Reset to None to trigger sample dataset
            st.warning(
                "⚠️ TMDB API key not found. Using sample dataset. "
                "For full functionality, add your API key to .env file."
            )
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make authenticated request to TMDB API.
        
        Args:
            endpoint: API endpoint (e.g., '/movie/popular')
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        if not self.api_key:
            return {}
        
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
            return {}
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Get detailed information for a specific movie.
        
        Args:
            movie_id: TMDB movie ID
            
        Returns:
            Dictionary with movie details including cast and crew
        """
        movie = self._make_request(f"/movie/{movie_id}")
        credits = self._make_request(f"/movie/{movie_id}/credits")
        
        # Extract director
        director = None
        if credits.get('crew'):
            directors = [person for person in credits['crew'] if person['job'] == 'Director']
            if directors:
                director = directors[0]['name']
        
        # Extract top cast
        cast = []
        if credits.get('cast'):
            cast = [person['name'] for person in credits['cast'][:5]]
        
        return {
            'id': movie.get('id'),
            'title': movie.get('title'),
            'year': movie.get('release_date', '')[:4] if movie.get('release_date') else None,
            'overview': movie.get('overview'),
            'genres': [g['name'] for g in movie.get('genres', [])],
            'rating': movie.get('vote_average'),
            'vote_count': movie.get('vote_count'),
            'poster_url': f"{self.IMAGE_BASE_URL}{movie['poster_path']}" if movie.get('poster_path') else None,
            'director': director,
            'cast': cast
        }
    
    def load_popular_movies(self, num_movies: int = 500) -> pd.DataFrame:
        """
        Load popular movies from TMDB.
        
        Args:
            num_movies: Target number of movies to load
            
        Returns:
            DataFrame with movie information
        """
        if not self.api_key:
            # Fallback to sample dataset if no API key
            return self._load_sample_dataset()
        
        movies = []
        pages_needed = (num_movies // 20) + 1  # TMDB returns 20 movies per page
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for page in range(1, min(pages_needed + 1, 26)):  # TMDB limits to 500 pages
            status_text.text(f"Loading movies... Page {page}/{pages_needed}")
            progress_bar.progress(page / pages_needed)
            
            response = self._make_request("/movie/popular", {'page': page})
            
            if not response.get('results'):
                break
            
            for movie_data in response['results']:
                try:
                    # Get full details for each movie
                    movie = self.get_movie_details(movie_data['id'])
                    movies.append(movie)
                    
                    if len(movies) >= num_movies:
                        break
                except Exception as e:
                    st.warning(f"Failed to load movie {movie_data.get('title')}: {e}")
                    continue
            
            if len(movies) >= num_movies:
                break
        
        progress_bar.empty()
        status_text.empty()
        
        df = pd.DataFrame(movies)
        
        # If we got no data from API, fall back to sample dataset
        if df.empty:
            st.warning("⚠️ Could not load movies from TMDB API. Using sample dataset.")
            return self._load_sample_dataset()
        
        # Clean data - only drop if columns exist
        if 'overview' in df.columns and 'genres' in df.columns:
            df = df.dropna(subset=['overview', 'genres'])
        if 'vote_count' in df.columns:
            df = df[df['vote_count'] >= 100]
        
        # Final fallback if filtering removed all data
        if df.empty:
            st.warning("⚠️ No valid movies after filtering. Using sample dataset.")
            return self._load_sample_dataset()
        
        return df
    
    def _load_sample_dataset(self) -> pd.DataFrame:
        """
        Load a sample dataset for demonstration when API key is not available.
        
        Returns:
            DataFrame with sample movie data
        """
        # This is a small sample dataset for testing without API key
        # In production, you might load from a CSV or use IMDb dataset
        sample_movies = [
            {
                'id': 1,
                'title': 'The Shawshank Redemption',
                'year': '1994',
                'overview': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'genres': ['Drama', 'Crime'],
                'rating': 8.7,
                'vote_count': 2000000,
                'poster_url': None,
                'director': 'Frank Darabont',
                'cast': ['Tim Robbins', 'Morgan Freeman']
            },
            {
                'id': 2,
                'title': 'The Godfather',
                'year': '1972',
                'overview': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'genres': ['Drama', 'Crime'],
                'rating': 8.7,
                'vote_count': 1500000,
                'poster_url': None,
                'director': 'Francis Ford Coppola',
                'cast': ['Marlon Brando', 'Al Pacino']
            },
            {
                'id': 3,
                'title': 'The Dark Knight',
                'year': '2008',
                'overview': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.',
                'genres': ['Action', 'Crime', 'Drama'],
                'rating': 9.0,
                'vote_count': 2500000,
                'poster_url': None,
                'director': 'Christopher Nolan',
                'cast': ['Christian Bale', 'Heath Ledger', 'Aaron Eckhart']
            },
            {
                'id': 4,
                'title': 'Inception',
                'year': '2010',
                'overview': 'A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
                'genres': ['Action', 'Sci-Fi', 'Thriller'],
                'rating': 8.8,
                'vote_count': 2200000,
                'poster_url': None,
                'director': 'Christopher Nolan',
                'cast': ['Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Elliot Page']
            },
            {
                'id': 5,
                'title': 'Pulp Fiction',
                'year': '1994',
                'overview': 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.',
                'genres': ['Crime', 'Drama'],
                'rating': 8.9,
                'vote_count': 1900000,
                'poster_url': None,
                'director': 'Quentin Tarantino',
                'cast': ['John Travolta', 'Uma Thurman', 'Samuel L. Jackson']
            },
            {
                'id': 6,
                'title': 'Forrest Gump',
                'year': '1994',
                'overview': 'The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75.',
                'genres': ['Drama', 'Romance'],
                'rating': 8.8,
                'vote_count': 1950000,
                'poster_url': None,
                'director': 'Robert Zemeckis',
                'cast': ['Tom Hanks', 'Robin Wright', 'Gary Sinise']
            },
            {
                'id': 7,
                'title': 'The Matrix',
                'year': '1999',
                'overview': 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.',
                'genres': ['Action', 'Sci-Fi'],
                'rating': 8.7,
                'vote_count': 1850000,
                'poster_url': None,
                'director': 'Lana Wachowski',
                'cast': ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss']
            },
            {
                'id': 8,
                'title': 'Interstellar',
                'year': '2014',
                'overview': 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity\'s survival.',
                'genres': ['Adventure', 'Drama', 'Sci-Fi'],
                'rating': 8.6,
                'vote_count': 1800000,
                'poster_url': None,
                'director': 'Christopher Nolan',
                'cast': ['Matthew McConaughey', 'Anne Hathaway', 'Jessica Chastain']
            },
            {
                'id': 9,
                'title': 'Fight Club',
                'year': '1999',
                'overview': 'An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.',
                'genres': ['Drama'],
                'rating': 8.8,
                'vote_count': 2000000,
                'poster_url': None,
                'director': 'David Fincher',
                'cast': ['Brad Pitt', 'Edward Norton', 'Helena Bonham Carter']
            },
            {
                'id': 10,
                'title': 'Goodfellas',
                'year': '1990',
                'overview': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners.',
                'genres': ['Crime', 'Drama'],
                'rating': 8.7,
                'vote_count': 1100000,
                'poster_url': None,
                'director': 'Martin Scorsese',
                'cast': ['Robert De Niro', 'Ray Liotta', 'Joe Pesci']
            },
            {
                'id': 11,
                'title': 'The Silence of the Lambs',
                'year': '1991',
                'overview': 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.',
                'genres': ['Crime', 'Drama', 'Thriller'],
                'rating': 8.6,
                'vote_count': 1300000,
                'poster_url': None,
                'director': 'Jonathan Demme',
                'cast': ['Jodie Foster', 'Anthony Hopkins']
            },
            {
                'id': 12,
                'title': 'Gladiator',
                'year': '2000',
                'overview': 'A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.',
                'genres': ['Action', 'Adventure', 'Drama'],
                'rating': 8.5,
                'vote_count': 1400000,
                'poster_url': None,
                'director': 'Ridley Scott',
                'cast': ['Russell Crowe', 'Joaquin Phoenix', 'Connie Nielsen']
            },
            {
                'id': 13,
                'title': 'The Prestige',
                'year': '2006',
                'overview': 'After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have.',
                'genres': ['Drama', 'Mystery', 'Sci-Fi'],
                'rating': 8.5,
                'vote_count': 1250000,
                'poster_url': None,
                'director': 'Christopher Nolan',
                'cast': ['Christian Bale', 'Hugh Jackman', 'Scarlett Johansson']
            },
            {
                'id': 14,
                'title': 'The Departed',
                'year': '2006',
                'overview': 'An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.',
                'genres': ['Crime', 'Drama', 'Thriller'],
                'rating': 8.5,
                'vote_count': 1200000,
                'poster_url': None,
                'director': 'Martin Scorsese',
                'cast': ['Leonardo DiCaprio', 'Matt Damon', 'Jack Nicholson']
            },
            {
                'id': 15,
                'title': 'Saving Private Ryan',
                'year': '1998',
                'overview': 'Following the Normandy Landings, a group of U.S. soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.',
                'genres': ['Drama', 'War'],
                'rating': 8.6,
                'vote_count': 1300000,
                'poster_url': None,
                'director': 'Steven Spielberg',
                'cast': ['Tom Hanks', 'Matt Damon', 'Tom Sizemore']
            }
        ]
        
        st.info(
            "📝 Using sample dataset. For full functionality with 500+ movies, "
            "add your TMDB API key to the .env file."
        )
        
        return pd.DataFrame(sample_movies)
    
    def search_movies(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for movies by title.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching movies
        """
        if not self.api_key:
            return []
        
        response = self._make_request("/search/movie", {'query': query})
        results = response.get('results', [])[:limit]
        
        movies = []
        for movie_data in results:
            try:
                movie = self.get_movie_details(movie_data['id'])
                movies.append(movie)
            except Exception:
                continue
        
        return movies


class IMDbDataLoader:
    """
    Alternative data loader using IMDb non-commercial datasets.
    
    Download datasets from: https://datasets.imdbws.com/
    Required files: title.basics.tsv.gz, title.ratings.tsv.gz
    """
    
    def __init__(self, data_path: str = "./data"):
        """
        Initialize IMDb data loader.
        
        Args:
            data_path: Path to directory containing IMDb TSV files
        """
        self.data_path = data_path
    
    def load_movies(self, min_votes: int = 1000, limit: int = 500) -> pd.DataFrame:
        """
        Load movies from IMDb datasets.
        
        Args:
            min_votes: Minimum number of votes for a movie
            limit: Maximum number of movies to load
            
        Returns:
            DataFrame with movie information
        """
        # Load basics
        basics = pd.read_csv(
            f"{self.data_path}/title.basics.tsv.gz",
            sep='\t',
            low_memory=False
        )
        
        # Load ratings
        ratings = pd.read_csv(
            f"{self.data_path}/title.ratings.tsv.gz",
            sep='\t'
        )
        
        # Filter for movies only
        movies = basics[basics['titleType'] == 'movie'].copy()
        
        # Merge with ratings
        movies = movies.merge(ratings, on='tconst', how='inner')
        
        # Filter by votes and sort by rating
        movies = movies[movies['numVotes'] >= min_votes]
        movies = movies.sort_values('averageRating', ascending=False)
        
        # Limit results
        movies = movies.head(limit)
        
        # Rename columns to match our schema
        movies = movies.rename(columns={
            'primaryTitle': 'title',
            'startYear': 'year',
            'genres': 'genres',
            'averageRating': 'rating',
            'numVotes': 'vote_count'
        })
        
        # Process genres (split comma-separated string into list)
        movies['genres'] = movies['genres'].apply(
            lambda x: x.split(',') if pd.notna(x) and x != '\\N' else []
        )
        
        # Add placeholder columns
        movies['overview'] = ''  # IMDb basic dataset doesn't include overviews
        movies['director'] = None
        movies['cast'] = []
        movies['poster_url'] = None
        
        return movies[['title', 'year', 'overview', 'genres', 'rating', 
                      'vote_count', 'poster_url', 'director', 'cast']]
