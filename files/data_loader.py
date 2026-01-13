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
        
        if not self.api_key:
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
        
        # Clean data
        df = df.dropna(subset=['overview', 'genres'])  # Remove movies without essential data
        df = df[df['vote_count'] >= 100]  # Filter out obscure movies
        
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
            # Add more sample movies as needed
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
