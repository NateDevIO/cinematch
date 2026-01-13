"""
Utility Functions
Helper functions for data processing, validation, and formatting
"""

import pandas as pd
from typing import List, Dict, Optional
import re


def validate_movie_selection(selected_movies: List[str], 
                            available_movies: List[str]) -> tuple[bool, str]:
    """
    Validate user's movie selection.
    
    Args:
        selected_movies: List of movies selected by user
        available_movies: List of all available movie titles
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not selected_movies:
        return False, "Please select at least one movie"
    
    if len(selected_movies) > 5:
        return False, "Please select no more than 5 movies"
    
    # Check for duplicates
    if len(selected_movies) != len(set(selected_movies)):
        return False, "You've selected duplicate movies. Please choose different films."
    
    # Check if all movies exist in dataset
    for movie in selected_movies:
        if movie not in available_movies:
            return False, f"Movie '{movie}' not found in database"
    
    return True, ""


def format_runtime(minutes: Optional[int]) -> str:
    """
    Format movie runtime in human-readable format.
    
    Args:
        minutes: Runtime in minutes
        
    Returns:
        Formatted string (e.g., "2h 30m")
    """
    if not minutes or minutes <= 0:
        return "N/A"
    
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{mins}m"


def format_currency(amount: Optional[float]) -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount in dollars
        
    Returns:
        Formatted string (e.g., "$150.5M")
    """
    if not amount or amount <= 0:
        return "N/A"
    
    if amount >= 1_000_000_000:
        return f"${amount/1_000_000_000:.1f}B"
    elif amount >= 1_000_000:
        return f"${amount/1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount/1_000:.1f}K"
    else:
        return f"${amount:.0f}"


def clean_text(text: str) -> str:
    """
    Clean text for display (remove extra whitespace, special characters).
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 150, suffix: str = "...") -> str:
    """
    Truncate text to specified length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    
    # Try to break at last space
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + suffix


def calculate_diversity_score(recommendations: List[Dict]) -> float:
    """
    Calculate diversity score of recommendations (0-1).
    Higher score means more diverse genres represented.
    
    Args:
        recommendations: List of recommendation dictionaries
        
    Returns:
        Diversity score between 0 and 1
    """
    if not recommendations:
        return 0.0
    
    all_genres = set()
    for rec in recommendations:
        movie = rec.get('movie', {})
        genres = movie.get('genres', [])
        if isinstance(genres, list):
            all_genres.update(genres)
    
    # Normalize by maximum possible unique genres (typically ~20 in movie databases)
    return min(len(all_genres) / 10.0, 1.0)


def get_genre_distribution(movies: List[Dict]) -> Dict[str, int]:
    """
    Calculate genre distribution across a list of movies.
    
    Args:
        movies: List of movie dictionaries
        
    Returns:
        Dictionary mapping genre to count
    """
    genre_counts = {}
    
    for movie in movies:
        genres = movie.get('genres', [])
        if isinstance(genres, list):
            for genre in genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    return dict(sorted(genre_counts.items(), key=lambda x: x[1], reverse=True))


def create_movie_fingerprint(movie: Dict) -> str:
    """
    Create a unique fingerprint for a movie based on key attributes.
    Useful for deduplication and caching.
    
    Args:
        movie: Movie dictionary
        
    Returns:
        Fingerprint string
    """
    title = movie.get('title', '').lower().strip()
    year = movie.get('year', '')
    director = movie.get('director', '').lower().strip()
    
    return f"{title}_{year}_{director}"


def filter_by_rating(movies: pd.DataFrame, 
                     min_rating: float = 0.0,
                     max_rating: float = 10.0) -> pd.DataFrame:
    """
    Filter movies by rating range.
    
    Args:
        movies: DataFrame of movies
        min_rating: Minimum rating (0-10)
        max_rating: Maximum rating (0-10)
        
    Returns:
        Filtered DataFrame
    """
    return movies[
        (movies['rating'] >= min_rating) & 
        (movies['rating'] <= max_rating)
    ].copy()


def filter_by_year(movies: pd.DataFrame,
                   start_year: Optional[int] = None,
                   end_year: Optional[int] = None) -> pd.DataFrame:
    """
    Filter movies by release year range.
    
    Args:
        movies: DataFrame of movies
        start_year: Minimum year (inclusive)
        end_year: Maximum year (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    filtered = movies.copy()
    
    if start_year:
        filtered = filtered[filtered['year'] >= str(start_year)]
    
    if end_year:
        filtered = filtered[filtered['year'] <= str(end_year)]
    
    return filtered


def filter_family_friendly(movies: pd.DataFrame) -> pd.DataFrame:
    """
    Filter for family-friendly movies (G, PG, PG-13 ratings).
    Note: Requires 'rating_mpaa' field in dataset.
    
    Args:
        movies: DataFrame of movies
        
    Returns:
        Filtered DataFrame
    """
    if 'rating_mpaa' in movies.columns:
        family_ratings = ['G', 'PG', 'PG-13']
        return movies[movies['rating_mpaa'].isin(family_ratings)].copy()
    else:
        # Fallback: filter by genre
        return movies[
            movies['genres'].apply(
                lambda x: any(g in ['Animation', 'Family', 'Adventure'] 
                            for g in x if isinstance(x, list))
            )
        ].copy()


def export_recommendations_csv(recommendations: List[Dict], 
                              filepath: str = "recommendations.csv"):
    """
    Export recommendations to CSV file.
    
    Args:
        recommendations: List of recommendation dictionaries
        filepath: Output file path
    """
    records = []
    for rec in recommendations:
        movie = rec.get('movie', {})
        records.append({
            'title': movie.get('title'),
            'year': movie.get('year'),
            'rating': movie.get('rating'),
            'genres': ', '.join(movie.get('genres', [])),
            'match_score': rec.get('similarity_score', 0) * 100,
            'explanation': rec.get('explanation', '')
        })
    
    df = pd.DataFrame(records)
    df.to_csv(filepath, index=False)
    
    return filepath


def get_decade(year: str) -> Optional[str]:
    """
    Get the decade from a year string.
    
    Args:
        year: Year as string (e.g., "1994")
        
    Returns:
        Decade string (e.g., "1990s") or None
    """
    try:
        year_int = int(year)
        decade = (year_int // 10) * 10
        return f"{decade}s"
    except (ValueError, TypeError):
        return None


def calculate_confidence_score(similarity_score: float,
                              vote_count: int,
                              min_votes: int = 100) -> float:
    """
    Calculate confidence score for a recommendation.
    Considers both similarity and popularity (vote count).
    
    Args:
        similarity_score: Similarity score (0-1)
        vote_count: Number of user votes/ratings
        min_votes: Minimum votes for full confidence
        
    Returns:
        Confidence score (0-1)
    """
    # Normalize vote count (capped at min_votes for full confidence)
    vote_confidence = min(vote_count / min_votes, 1.0)
    
    # Weighted combination (80% similarity, 20% popularity)
    confidence = (0.8 * similarity_score) + (0.2 * vote_confidence)
    
    return confidence
