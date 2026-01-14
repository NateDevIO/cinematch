"""
Movie Recommendation Engine
Implements content-based filtering using TF-IDF and cosine similarity
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st


class MovieRecommender:
    """
    Content-based movie recommendation system.
    
    Uses weighted features:
    - Plot descriptions (40%): TF-IDF vectorization
    - Genres (30%): Binary overlap
    - Director (15%): Exact match
    - Cast (15%): Member overlap
    """
    
    def __init__(self, movie_data: pd.DataFrame):
        """
        Initialize the recommender with movie data.
        
        Args:
            movie_data: DataFrame with columns: title, overview, genres, director, cast, etc.
        """
        self.movie_data = movie_data.copy()
        self.tfidf_matrix = None
        self.tfidf_vectorizer = None
        
        # Precompute TF-IDF matrix for plot descriptions
        self._build_tfidf_matrix()
    
    def _build_tfidf_matrix(self):
        """Build TF-IDF matrix from movie plot descriptions."""
        # Combine overview with genres for richer text features
        self.movie_data['combined_features'] = (
            self.movie_data['overview'].fillna('') + ' ' +
            self.movie_data['genres'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
        )
        
        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams for better context
            min_df=2  # Minimum document frequency
        )
        
        # Fit and transform
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
            self.movie_data['combined_features']
        )
    
    def _calculate_plot_similarity(self, movie_indices: List[int]) -> np.ndarray:
        """
        Calculate cosine similarity based on plot descriptions.
        
        Args:
            movie_indices: List of movie indices to compare against
            
        Returns:
            Array of similarity scores for all movies
        """
        # Get TF-IDF vectors for selected movies
        selected_vectors = self.tfidf_matrix[movie_indices]
        
        # Calculate cosine similarity with all movies
        similarities = cosine_similarity(selected_vectors, self.tfidf_matrix)
        
        # Average similarity across selected movies
        avg_similarity = similarities.mean(axis=0)
        
        return avg_similarity
    
    def _calculate_genre_similarity(self, movie_indices: List[int]) -> np.ndarray:
        """
        Calculate genre overlap similarity.
        
        Args:
            movie_indices: List of movie indices to compare against
            
        Returns:
            Array of genre similarity scores (Jaccard similarity)
        """
        similarities = np.zeros(len(self.movie_data))
        
        # Get genres of selected movies
        selected_genres = []
        for idx in movie_indices:
            genres = self.movie_data.iloc[idx]['genres']
            if isinstance(genres, list):
                selected_genres.extend(genres)
        selected_genres = set(selected_genres)
        
        # Calculate Jaccard similarity for each movie
        for pos, (i, row) in enumerate(self.movie_data.iterrows()):
            movie_genres = set(row['genres']) if isinstance(row['genres'], list) else set()
            
            if not movie_genres or not selected_genres:
                similarities[pos] = 0
            else:
                intersection = len(selected_genres.intersection(movie_genres))
                union = len(selected_genres.union(movie_genres))
                similarities[pos] = intersection / union if union > 0 else 0
        
        return similarities
    
    def _calculate_director_similarity(self, movie_indices: List[int]) -> np.ndarray:
        """
        Calculate director match similarity (binary: 1 if match, 0 otherwise).
        
        Args:
            movie_indices: List of movie indices to compare against
            
        Returns:
            Array of director similarity scores
        """
        similarities = np.zeros(len(self.movie_data))
        
        # Get directors of selected movies
        selected_directors = set()
        for idx in movie_indices:
            director = self.movie_data.iloc[idx]['director']
            if pd.notna(director):
                selected_directors.add(director)
        
        # Check each movie's director
        for pos, (i, row) in enumerate(self.movie_data.iterrows()):
            if pd.notna(row['director']) and row['director'] in selected_directors:
                similarities[pos] = 1.0
        
        return similarities
    
    def _calculate_cast_similarity(self, movie_indices: List[int]) -> np.ndarray:
        """
        Calculate cast overlap similarity.
        
        Args:
            movie_indices: List of movie indices to compare against
            
        Returns:
            Array of cast similarity scores
        """
        similarities = np.zeros(len(self.movie_data))
        
        # Get cast members of selected movies
        selected_cast = []
        for idx in movie_indices:
            cast = self.movie_data.iloc[idx]['cast']
            if isinstance(cast, list):
                selected_cast.extend(cast[:5])  # Top 5 cast members
        selected_cast = set(selected_cast)
        
        # Calculate overlap for each movie
        for pos, (i, row) in enumerate(self.movie_data.iterrows()):
            movie_cast = set(row['cast'][:5]) if isinstance(row['cast'], list) else set()
            
            if not movie_cast or not selected_cast:
                similarities[pos] = 0
            else:
                overlap = len(selected_cast.intersection(movie_cast))
                similarities[pos] = overlap / 5.0  # Normalize by max possible overlap
        
        return similarities
    
    def _generate_explanation(self, selected_movies: List[str], 
                              movie_indices: List[int],
                              recommended_movie: pd.Series,
                              similarity_components: Dict[str, float]) -> str:
        """
        Generate a human-readable explanation for why a movie was recommended.
        
        Args:
            selected_movies: List of selected movie titles
            movie_indices: Indices of selected movies in the dataframe
            recommended_movie: Series containing recommended movie data
            similarity_components: Dictionary with component similarities
            
        Returns:
            Explanation string
        """
        explanations = []
        
        # Get recommended movie's attributes
        rec_director = recommended_movie.get('director')
        rec_cast = set(recommended_movie.get('cast', [])[:5]) if isinstance(recommended_movie.get('cast'), list) else set()
        rec_genres = set(recommended_movie.get('genres', [])) if isinstance(recommended_movie.get('genres'), list) else set()
        
        # Track which selected movie matches for each component
        director_match_movie = None
        cast_match_movie = None
        genre_match_movie = None
        best_genre_overlap = []
        
        # Check each selected movie for matches
        for i, idx in enumerate(movie_indices):
            selected_movie_data = self.movie_data.iloc[idx]
            sel_director = selected_movie_data.get('director')
            sel_cast = set(selected_movie_data.get('cast', [])[:5]) if isinstance(selected_movie_data.get('cast'), list) else set()
            sel_genres = set(selected_movie_data.get('genres', [])) if isinstance(selected_movie_data.get('genres'), list) else set()
            
            # Director match
            if rec_director and sel_director and rec_director == sel_director:
                director_match_movie = selected_movies[i]
            
            # Cast overlap
            if rec_cast and sel_cast and len(rec_cast.intersection(sel_cast)) > 0:
                cast_match_movie = selected_movies[i]
            
            # Genre overlap - track best match
            genre_overlap = rec_genres.intersection(sel_genres)
            if len(genre_overlap) > len(best_genre_overlap):
                best_genre_overlap = list(genre_overlap)
                genre_match_movie = selected_movies[i]
        
        # Find strongest component
        strongest = max(similarity_components.items(), key=lambda x: x[1])
        
        # Determine which movie to attribute the match to based on strongest signal
        if strongest[0] == 'director' and director_match_movie:
            matched_movie = director_match_movie
        elif strongest[0] == 'cast' and cast_match_movie:
            matched_movie = cast_match_movie
        elif strongest[0] == 'genre' and genre_match_movie:
            matched_movie = genre_match_movie
        elif director_match_movie:
            matched_movie = director_match_movie
        elif cast_match_movie:
            matched_movie = cast_match_movie
        elif genre_match_movie:
            matched_movie = genre_match_movie
        else:
            matched_movie = selected_movies[0]  # Default to first
        
        # Generate explanation based on signals
        if similarity_components.get('genre', 0) > 0.5 and best_genre_overlap:
            explanations.append(f"Shares genres: {', '.join(best_genre_overlap[:2])}")
        
        if similarity_components.get('director', 0) > 0.9:
            explanations.append(f"Same director: {recommended_movie['director']}")
        
        if similarity_components.get('cast', 0) > 0.2:
            explanations.append("Features similar actors")
        
        if similarity_components.get('plot', 0) > 0.3:
            explanations.append("Similar themes and storytelling")
        
        if not explanations:
            explanations.append("Strong overall match based on multiple factors")
        
        # Use the matched movie in the explanation
        base_text = f"Because you liked {matched_movie}"
        explanation_text = " → " + "; ".join(explanations)
        
        return base_text + explanation_text
    
    def get_recommendations(self, selected_titles: List[str], 
                          n_recommendations: int = 5) -> List[Dict]:
        """
        Generate movie recommendations based on user selections.
        
        Args:
            selected_titles: List of movie titles the user likes
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommendation dictionaries with movie info and explanations
        """
        # Get indices of selected movies
        movie_indices = []
        for title in selected_titles:
            matching_movies = self.movie_data[self.movie_data['title'] == title]
            if not matching_movies.empty:
                movie_indices.append(matching_movies.index[0])
        
        if not movie_indices:
            return []
        
        # Calculate component similarities with weights
        plot_sim = self._calculate_plot_similarity(movie_indices) * 0.40
        genre_sim = self._calculate_genre_similarity(movie_indices) * 0.30
        director_sim = self._calculate_director_similarity(movie_indices) * 0.15
        cast_sim = self._calculate_cast_similarity(movie_indices) * 0.15
        
        # Combine into final similarity score
        combined_similarity = plot_sim + genre_sim + director_sim + cast_sim
        
        # Exclude already selected movies
        for idx in movie_indices:
            combined_similarity[idx] = -1
        
        # Get top N recommendations
        top_indices = np.argsort(combined_similarity)[::-1][:n_recommendations]
        
        # Build recommendation list with explanations
        recommendations = []
        for idx in top_indices:
            if combined_similarity[idx] > 0:  # Only include positive matches
                movie = self.movie_data.iloc[idx]
                
                # Store component scores for explanation
                component_scores = {
                    'plot': plot_sim[idx] / 0.40,
                    'genre': genre_sim[idx] / 0.30,
                    'director': director_sim[idx] / 0.15,
                    'cast': cast_sim[idx] / 0.15
                }
                
                recommendations.append({
                    'movie': movie.to_dict(),
                    'similarity_score': combined_similarity[idx],
                    'explanation': self._generate_explanation(
                        selected_titles,
                        movie_indices,
                        movie,
                        component_scores
                    )
                })
        
        return recommendations
