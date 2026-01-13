"""
Movie Recommendation Streamlit App
Main application file with UI and user interactions
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
from recommender import MovieRecommender
from data_loader import TMDBDataLoader
import utils


# Page configuration
st.set_page_config(
    page_title="What Movie Should I Watch?",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling (optional - customize as needed)
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #E50914;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def load_movie_data() -> pd.DataFrame:
    """Load and cache movie dataset from TMDB or local source."""
    loader = TMDBDataLoader()
    return loader.load_popular_movies(num_movies=500)


@st.cache_resource
def initialize_recommender(_movie_data: pd.DataFrame) -> MovieRecommender:
    """Initialize and cache the recommendation engine."""
    return MovieRecommender(_movie_data)


def display_movie_card(movie: Dict, match_score: float = None, explanation: str = None):
    """
    Display a single movie card with poster, title, and details.
    
    Args:
        movie: Dictionary containing movie information
        match_score: Optional similarity score (0-100)
        explanation: Optional explanation for the recommendation
    """
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display poster image
            if movie.get('poster_url'):
                st.image(movie['poster_url'], use_column_width=True)
            else:
                st.info("No poster available")
        
        with col2:
            # Title and year
            st.subheader(f"{movie['title']} ({movie.get('year', 'N/A')})")
            
            # Match score badge (if provided)
            if match_score is not None:
                st.markdown(f"**🎯 {match_score:.0f}% Match**")
            
            # Rating
            if movie.get('rating'):
                st.write(f"⭐ {movie['rating']:.1f}/10")
            
            # Genres
            if movie.get('genres'):
                st.write(f"**Genres:** {', '.join(movie['genres'][:3])}")
            
            # Explanation (for recommendations)
            if explanation:
                st.info(explanation)
            
            # Plot summary (expandable)
            if movie.get('overview'):
                with st.expander("📖 Plot Summary"):
                    st.write(movie['overview'])


def main():
    """Main application logic."""
    
    # Header
    st.title("🎬 What Movie Should I Watch?")
    st.markdown(
        "Select movies you love, and we'll recommend similar films using "
        "content-based filtering and machine learning."
    )
    
    # Load data
    with st.spinner("Loading movie database..."):
        movie_data = load_movie_data()
        recommender = initialize_recommender(movie_data)
    
    st.success(f"✅ Loaded {len(movie_data)} movies")
    
    # Sidebar for optional filters (Phase 3 enhancement)
    with st.sidebar:
        st.header("⚙️ Settings")
        num_recommendations = st.slider(
            "Number of recommendations",
            min_value=3,
            max_value=10,
            value=5
        )
        
        # Optional filters (implement in Phase 3)
        # st.checkbox("Family friendly")
        # st.checkbox("Hidden gems (< 50k votes)")
        # year_range = st.slider("Release year", 1980, 2024, (2000, 2024))
    
    st.markdown("---")
    
    # Movie selection section
    st.header("🎯 Step 1: Select Your Favorite Movies")
    st.write("Choose 1-5 movies you really enjoyed:")
    
    # Create movie selection UI
    movie_titles = movie_data['title'].tolist()
    selected_movies = []
    
    # Allow up to 5 movie selections
    num_selections = st.number_input(
        "How many movies do you want to select?",
        min_value=1,
        max_value=5,
        value=3
    )
    
    for i in range(num_selections):
        selected = st.selectbox(
            f"Movie {i+1}",
            options=[""] + movie_titles,
            key=f"movie_{i}",
            help="Start typing to search for a movie"
        )
        if selected:
            selected_movies.append(selected)
    
    # Display selected movies with posters
    if selected_movies:
        st.subheader("Your Selected Movies:")
        cols = st.columns(min(len(selected_movies), 5))
        for idx, movie_title in enumerate(selected_movies):
            movie_info = movie_data[movie_data['title'] == movie_title].iloc[0].to_dict()
            with cols[idx % len(cols)]:
                if movie_info.get('poster_url'):
                    st.image(movie_info['poster_url'], use_column_width=True)
                st.caption(movie_title)
    
    st.markdown("---")
    
    # Recommendation button
    if st.button("🎬 Get Recommendations", type="primary", use_container_width=True):
        if not selected_movies:
            st.error("⚠️ Please select at least one movie!")
            return
        
        # Check for duplicates
        if len(selected_movies) != len(set(selected_movies)):
            st.warning("⚠️ You've selected duplicate movies. Please choose different films.")
            return
        
        # Generate recommendations
        with st.spinner("Finding perfect movies for you..."):
            recommendations = recommender.get_recommendations(
                selected_movies,
                n_recommendations=num_recommendations
            )
        
        # Display recommendations
        if recommendations:
            st.header("✨ Recommended Movies For You:")
            st.write(f"Based on your selection, here are {len(recommendations)} movies we think you'll love:")
            
            # Display in grid format (3 columns)
            for i in range(0, len(recommendations), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(recommendations):
                        rec = recommendations[i + j]
                        with col:
                            display_movie_card(
                                rec['movie'],
                                match_score=rec['similarity_score'] * 100,
                                explanation=rec['explanation']
                            )
                            st.markdown("---")
        else:
            st.error("😔 Sorry, we couldn't find any recommendations. Try different movies!")
    
    # How it works section (expandable)
    st.markdown("---")
    with st.expander("🤔 How does this work?"):
        st.markdown("""
        ### Content-Based Filtering Algorithm
        
        This recommender uses **content-based filtering** to find movies similar to your selections:
        
        1. **Feature Extraction**: We analyze each movie's:
           - Plot description (using TF-IDF vectorization)
           - Genres
           - Director
           - Cast members
        
        2. **Similarity Calculation**: We use **cosine similarity** to measure how close movies are in this feature space
        
        3. **Weighted Scoring**:
           - Plot similarity: 40%
           - Genre overlap: 30%
           - Director match: 15%
           - Cast overlap: 15%
        
        4. **Ranking**: We combine scores from your selected movies and return the highest-ranked films you haven't seen yet!
        
        **Technologies used**: Python, Streamlit, scikit-learn, pandas, TMDB API
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit | "
        "[View Source Code](https://github.com/yourusername/movie-recommender) | "
        "[Portfolio](https://yourportfolio.com)"
    )


if __name__ == "__main__":
    main()
