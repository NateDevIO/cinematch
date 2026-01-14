"""
CineMatch - Movie Recommendation Streamlit App
Main application file with UI and user interactions

Coded by Nate
"""

import streamlit as st
import pandas as pd
from typing import List, Dict
from recommender import MovieRecommender
from data_loader import TMDBDataLoader
import utils


# Page configuration
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced CSS for visual improvements
st.markdown("""
    <style>
    /* Overall styling */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Primary button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #E50914 0%, #B20710 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.4);
    }
    
    /* Movie card styling */
    .movie-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        animation: fadeInUp 0.5s ease-out;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(229, 9, 20, 0.2);
        border-color: rgba(229, 9, 20, 0.3);
    }
    
    /* Fade-in animation */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Genre badges */
    .genre-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        color: white;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .genre-action { background: linear-gradient(135deg, #f12711 0%, #f5af19 100%); }
    .genre-comedy { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .genre-drama { background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%); }
    .genre-horror { background: linear-gradient(135deg, #200122 0%, #6f0000 100%); }
    .genre-scifi { background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%); }
    .genre-romance { background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%); }
    .genre-thriller { background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%); }
    .genre-animation { background: linear-gradient(135deg, #f953c6 0%, #b91d73 100%); }
    .genre-adventure { background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%); }
    .genre-fantasy { background: linear-gradient(135deg, #7f00ff 0%, #e100ff 100%); }
    
    /* Recommendation explanation */
    .recommendation-reason {
        background: rgba(229, 9, 20, 0.1);
        border-left: 3px solid #E50914;
        padding: 0.75rem 1rem;
        border-radius: 0 8px 8px 0;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Movie poster styling */
    .movie-poster {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease;
    }
    
    .movie-poster:hover {
        transform: scale(1.02);
    }
    
    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #E50914 0%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem 1rem;
        }
        
        .movie-card {
            padding: 1rem;
        }
        
        .stColumns > div {
            min-width: 100% !important;
            margin-bottom: 1rem;
        }
    }
    
    /* Search input styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid rgba(229, 9, 20, 0.3);
        padding: 0.75rem 1.25rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #E50914;
        box-shadow: 0 0 15px rgba(229, 9, 20, 0.2);
    }
    
    /* Selected movie mini-cards */
    .selected-movie {
        text-align: center;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    .selected-movie:hover {
        background: rgba(229, 9, 20, 0.1);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Trailer button */
    .trailer-btn {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%);
        color: white !important;
        text-decoration: none;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(255, 0, 0, 0.3);
    }
    
    .trailer-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.4);
    }
    
    /* Watchlist item */
    .watchlist-item {
        padding: 0.5rem;
        margin: 0.5rem 0;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        border-left: 3px solid #E50914;
    }
    </style>
    """, unsafe_allow_html=True)


# Genre color mapping
GENRE_COLORS = {
    'Action': 'genre-action',
    'Comedy': 'genre-comedy', 
    'Drama': 'genre-drama',
    'Horror': 'genre-horror',
    'Science Fiction': 'genre-scifi',
    'Sci-Fi': 'genre-scifi',
    'Romance': 'genre-romance',
    'Thriller': 'genre-thriller',
    'Animation': 'genre-animation',
    'Adventure': 'genre-adventure',
    'Fantasy': 'genre-fantasy',
}


def get_genre_badges_html(genres: List[str]) -> str:
    """Generate HTML for colorful genre badges."""
    badges = []
    for genre in genres[:4]:  # Limit to 4 genres
        css_class = GENRE_COLORS.get(genre, 'genre-badge')
        badges.append(f'<span class="genre-badge {css_class}">{genre}</span>')
    return ' '.join(badges)


@st.cache_data(ttl=3600)
def load_movie_data() -> pd.DataFrame:
    """Load and cache movie dataset from TMDB or local cache file."""
    loader = TMDBDataLoader()
    return loader.load_popular_movies(num_movies=500)


@st.cache_resource
def initialize_recommender(_movie_data: pd.DataFrame) -> MovieRecommender:
    """Initialize and cache the recommendation engine."""
    return MovieRecommender(_movie_data)


def display_movie_card(movie: Dict, explanation: str = None, delay: int = 0, card_id: str = None):
    """
    Display a styled movie card with poster, title, and details.
    
    Args:
        movie: Dictionary containing movie information
        explanation: Optional explanation for the recommendation
        delay: Animation delay in milliseconds
        card_id: Unique identifier for this card (for save button)
    """
    # Animation delay for staggered effect (applied to container if needed)
    # Note: Streamlit doesn't support wrapping dynamic content in custom HTML divs
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if movie.get('poster_url'):
            st.markdown('<div class="movie-poster">', unsafe_allow_html=True)
            st.image(movie['poster_url'], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🎬 No poster")
    
    with col2:
        # Title and year
        year = movie.get('year', 'N/A')
        title = movie['title']
        st.markdown(f"### {title} ({year})")
        
        # Rating with stars
        if movie.get('rating'):
            rating = movie['rating']
            stars = "⭐" * int(rating / 2)
            st.markdown(f"{stars} **{rating:.1f}**/10")
        
        # Genre badges
        if movie.get('genres'):
            genre_html = get_genre_badges_html(movie['genres'])
            st.markdown(genre_html, unsafe_allow_html=True)
        
        # Recommendation explanation
        if explanation:
            st.markdown(f'<div class="recommendation-reason">💡 {explanation}</div>', 
                       unsafe_allow_html=True)
        
        # Action buttons row
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            # Watch Trailer button - links to YouTube search
            trailer_query = f"{title} {year} official trailer".replace(' ', '+')
            trailer_url = f"https://www.youtube.com/results?search_query={trailer_query}"
            st.markdown(
                f'<a href="{trailer_url}" target="_blank" class="trailer-btn">'
                f'▶️ Watch Trailer</a>',
                unsafe_allow_html=True
            )
        
        with btn_col2:
            # Save For Later button
            if card_id:
                movie_key = f"{title}_{year}"
                if movie_key in st.session_state.get('watchlist', {}):
                    if st.button("✓ Saved", key=f"saved_{card_id}", disabled=True):
                        pass
                else:
                    if st.button("🔖 Save", key=f"save_{card_id}"):
                        if 'watchlist' not in st.session_state:
                            st.session_state.watchlist = {}
                        st.session_state.watchlist[movie_key] = movie
                        st.rerun()
        
        # Plot summary (expandable)
        if movie.get('overview'):
            with st.expander("📖 Plot Summary"):
                st.write(movie['overview'])
    
    # Divider between cards
    st.markdown("---")


def main():
    """Main application logic."""
    
    # Polished Header/Hero Section
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 2rem 2rem 1.5rem 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(229, 9, 20, 0.2);
        ">
            <h1 style="
                font-size: 3.5rem;
                margin: 0;
                background: linear-gradient(135deg, #E50914 0%, #ff6b6b 50%, #ffd93d 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: 800;
                letter-spacing: -1px;
            ">🎬 CineMatch</h1>
            <p style="
                font-size: 1.2rem;
                color: #a0a0a0;
                margin: 0.5rem 0 0 0;
                font-style: italic;
            ">Your AI-Powered Movie Recommendation Engine</p>
            <div style="
                margin-top: 1rem;
                display: flex;
                justify-content: center;
                gap: 1rem;
                flex-wrap: wrap;
            ">
                <span style="
                    background: rgba(229, 9, 20, 0.2);
                    color: #ff6b6b;
                    padding: 0.3rem 0.8rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                ">✨ Smart Recommendations</span>
                <span style="
                    background: rgba(102, 126, 234, 0.2);
                    color: #667eea;
                    padding: 0.3rem 0.8rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                ">🎯 Content-Based Filtering</span>
                <span style="
                    background: rgba(17, 153, 142, 0.2);
                    color: #11998e;
                    padding: 0.3rem 0.8rem;
                    border-radius: 20px;
                    font-size: 0.85rem;
                ">📚 1500+ Movies</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data with user-friendly loading message
    loading_msg = st.info("☕ First load may take 30-60 seconds. Grab a coffee!")
    with st.spinner("Loading movie database..."):
        movie_data = load_movie_data()
        recommender = initialize_recommender(movie_data)
    loading_msg.empty()
    
    st.success(f"✅ Loaded {len(movie_data)} movies")
    
    # Sidebar for settings and watchlist
    with st.sidebar:
        st.header("⚙️ Settings")
        num_recommendations = st.slider(
            "Number of recommendations",
            min_value=3,
            max_value=10,
            value=5
        )
        
        # Watchlist section
        st.markdown("---")
        st.header("🔖 My Watchlist")
        
        if 'watchlist' not in st.session_state:
            st.session_state.watchlist = {}
        
        watchlist = st.session_state.watchlist
        
        if watchlist:
            st.write(f"{len(watchlist)} movie(s) saved")
            for movie_key, movie in watchlist.items():
                st.markdown(
                    f'<div class="watchlist-item">'
                    f'<strong>{movie["title"]}</strong> ({movie.get("year", "N/A")})'
                    f'</div>',
                    unsafe_allow_html=True
                )
            
            # Clear watchlist button
            if st.button("🗑️ Clear Watchlist"):
                st.session_state.watchlist = {}
                st.rerun()
        else:
            st.write("No movies saved yet")
            st.caption("Click 'Save' on any recommendation to add it here!")
    
    st.markdown("---")
    
    # Movie selection section
    st.markdown("## 🎯 Step 1: Select Your Favorite Movies")
    st.write("Start typing a movie name to search, then select from the dropdown:")
    
    # Create searchable movie list
    movie_titles = sorted(movie_data['title'].tolist())
    selected_movies = []
    
    # Number of selections
    num_selections = st.number_input(
        "How many movies do you want to select?",
        min_value=1,
        max_value=5,
        value=3
    )
    
    # Single searchable selectbox for each movie slot
    for i in range(num_selections):
        selected = st.selectbox(
            f"🎬 Movie {i+1}",
            options=[""] + movie_titles,
            key=f"movie_{i}",
            help="Start typing to filter the list"
        )
        if selected:
            selected_movies.append(selected)
    
    # Display selected movies with styled mini-cards
    if selected_movies:
        st.markdown("### 🎥 Your Selection:")
        cols = st.columns(min(len(selected_movies), 5))
        for idx, movie_title in enumerate(selected_movies):
            movie_info = movie_data[movie_data['title'] == movie_title].iloc[0].to_dict()
            with cols[idx % len(cols)]:
                st.markdown('<div class="selected-movie">', unsafe_allow_html=True)
                if movie_info.get('poster_url'):
                    st.image(movie_info['poster_url'], use_container_width=True)
                st.caption(f"**{movie_title}**")
                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recommendation button
    if st.button("🎬 Get Recommendations", type="primary", use_container_width=True):
        if not selected_movies:
            st.error("⚠️ Please select at least one movie!")
            return
        
        if len(selected_movies) != len(set(selected_movies)):
            st.warning("⚠️ You've selected duplicate movies. Please choose different films.")
            return
        
        # Generate recommendations
        with st.spinner("✨ Finding perfect movies for you..."):
            recommendations = recommender.get_recommendations(
                selected_movies,
                n_recommendations=num_recommendations
            )
        
        # Display recommendations with animations
        if recommendations:
            st.markdown("## ✨ Recommended Movies For You")
            st.write(f"Based on your selection, here are **{len(recommendations)}** movies we think you'll love:")
            
            # Display in responsive grid
            for i, rec in enumerate(recommendations):
                display_movie_card(
                    rec['movie'],
                    explanation=rec['explanation'],
                    delay=i,
                    card_id=f"rec_{i}"
                )
        else:
            st.error("😔 Sorry, we couldn't find recommendations. Try different movies!")
    
    # How it works section
    st.markdown("---")
    with st.expander("🤔 How does this work?"):
        st.markdown("""
        ### Content-Based Filtering Algorithm
        
        This recommender uses **content-based filtering** to find similar movies:
        
        | Feature | Weight |
        |---------|--------|
        | Plot similarity (TF-IDF) | 40% |
        | Genre overlap | 30% |
        | Director match | 15% |
        | Cast overlap | 15% |
        
        **Technologies**: Python, Streamlit, scikit-learn, pandas, TMDB API
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="footer">'
        'Built with ❤️ using Streamlit | '
        '<a href="https://github.com/NateDevIO/cinematch">View Source Code</a>'
        '<br><small>Coded by Nate</small>'
        '</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
