# SOP: Movie Recommendation Streamlit App Development

## Project Overview
Build a portfolio-quality movie recommendation web application using Streamlit that demonstrates data science, API integration, and user experience design skills. This app should impress hiring managers for Sales Engineer, Data Analyst, and Developer roles.

---

## Target Audience & Portfolio Goals
- **Primary viewers**: Technical recruiters, hiring managers, potential employers
- **Key impression**: "This person understands recommendation systems, APIs, clean code, and user-centered design"
- **Differentiators**: Goes beyond basic filtering; shows algorithmic thinking and polish

---

## Core Functional Requirements

### 1. Movie Input System
- **Search interface**: Autocomplete search bar (NOT dropdown) using Streamlit's `selectbox` with searchable option
- **Flexible quantity**: Allow users to select 1-5 movies (not locked to 3)
- **Validation**: Handle cases where users select duplicate movies
- **Fallback**: If a movie isn't found, provide helpful error message with suggestions

### 2. Recommendation Engine
**Algorithm Requirements:**
- Use **content-based filtering** with cosine similarity
- Calculate similarity based on:
  - Genres (weighted: 30%)
  - Plot descriptions via TF-IDF (weighted: 40%)
  - Director (weighted: 15%)
  - Cast overlap (weighted: 15%)
  
**Output:**
- Return 5-10 recommendations (user-adjustable via slider)
- Exclude movies the user already selected
- Sort by similarity score (highest first)

### 3. Recommendation Explanation
For each recommended movie, display:
- **Match percentage**: "87% match"
- **Reason**: "Because you liked Inception → Similar director (Christopher Nolan), cerebral sci-fi themes"
- **Key attributes**: Shared genres, director, top 2 cast members

---

## Data Requirements

### Dataset Options (in order of preference):
1. **TMDB API** (The Movie Database) - *PREFERRED*
   - Free API with 5000 requests/day
   - Rich metadata: posters, plots, cast, directors
   - Real-time data
   
2. **IMDb Dataset** (backup)
   - Use IMDb Non-Commercial Datasets (freely available)
   - Will need to supplement with poster images

### Required Data Fields:
- Movie title, year, genres
- Plot summary/overview (for TF-IDF)
- Director name
- Top 5 cast members
- User rating (for display, not matching)
- Poster image URL

---

## Technical Implementation Specifications

### Tech Stack:
- **Framework**: Streamlit
- **Data processing**: pandas, numpy
- **NLP/Similarity**: scikit-learn (TfidfVectorizer, cosine_similarity)
- **API calls**: requests library (for TMDB)
- **Caching**: Streamlit's @st.cache_data decorator

### Architecture:
```
movie-recommender/
├── app.py                  # Main Streamlit app
├── recommender.py          # Recommendation engine logic
├── data_loader.py          # API calls or dataset loading
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
└── .env.example           # Example environment variables
```

### Performance Requirements:
- Initial load time: < 3 seconds
- Recommendation generation: < 2 seconds
- Use caching for:
  - Movie dataset/API results
  - TF-IDF matrix
  - Similarity calculations

---

## UI/UX Requirements

### Layout Structure:
1. **Header Section**
   - App title: "🎬 What Movie Should I Watch?"
   - Subtitle: Brief explanation (1-2 sentences)
   - Optional: Your name/portfolio link

2. **Input Section**
   - Search bar(s) for movie selection
   - Visual confirmation of selected movies (show posters in a row)
   - "Get Recommendations" button

3. **Results Section**
   - Display recommendations in a clean grid (3 columns recommended)
   - Each movie card shows:
     - Poster image
     - Title + year
     - Match percentage badge
     - Brief explanation of match
     - Rating (if available)

4. **Optional: "How It Works" Expander**
   - Collapsible section explaining the algorithm
   - Shows you understand the tech behind it

5. **Optional: Filters/Mood Selector**
   - Checkboxes for: "Family friendly," "Hidden gems (< 10k ratings)," "Recent (post-2020)"
   - This is a "nice to have" - don't let it delay MVP

### Design Guidelines:
- **Color scheme**: Dark mode friendly (use Streamlit theme customization)
- **Responsive**: Should work on desktop and tablet
- **Professional**: Clean, minimal, no clutter
- **Visual hierarchy**: Clear separation between input and results

---

## Portfolio Presentation Features

### Must-Haves:
1. **README.md** with:
   - Project description
   - Demo screenshot or GIF
   - Technical approach explanation
   - How to run locally
   - Technologies used

2. **Code Quality:**
   - Clear function names and docstrings
   - Modular code (separate concerns)
   - Comments explaining complex logic
   - Type hints (Python 3.9+)

3. **Error Handling:**
   - Graceful API failures
   - User-friendly error messages
   - Input validation

### Nice-to-Haves:
- **Data Visualization**: Show genre distribution comparison (user picks vs. recommendations)
- **Metrics Dashboard**: "Recommendation confidence," "diversity score"
- **Export Feature**: "Save my recommendations" to CSV/PDF

---

## Development Phases

### Phase 1: MVP (Core Functionality)
- [ ] Set up Streamlit app structure
- [ ] Integrate TMDB API or load IMDb dataset
- [ ] Implement basic content-based filtering
- [ ] Display recommendations with posters
- [ ] Deploy to Streamlit Cloud

### Phase 2: Polish
- [ ] Add recommendation explanations
- [ ] Improve UI/UX (styling, layout)
- [ ] Add caching for performance
- [ ] Write comprehensive README

### Phase 3: Portfolio Enhancement
- [ ] Add "How It Works" section
- [ ] Optional: Data visualizations
- [ ] Optional: Mood/filter options
- [ ] Test on multiple devices

---

## Acceptance Criteria

**The app is complete when:**
1. User can search and select 1-5 movies
2. App returns relevant recommendations in < 2 seconds
3. Each recommendation includes poster, match %, and explanation
4. Code is clean, modular, and well-documented
5. App is deployed and shareable via URL
6. README explains the project professionally

**The app impresses when:**
- Recommendations actually make sense (test with diverse movie selections)
- UI is polished and professional
- Loading states/spinners are present (no janky experience)
- Error cases are handled gracefully

---

## Testing Checklist

Test the app with these scenarios:
- [ ] Select 1 movie (edge case: minimal input)
- [ ] Select 5 movies with very different genres
- [ ] Select 3 movies from same franchise (e.g., all Marvel)
- [ ] Search for obscure movie not in dataset
- [ ] Rapid clicking/submission (stress test)
- [ ] View on mobile device

---

## Deployment Instructions
- **Platform**: Streamlit Community Cloud (free)
- **Custom domain**: Optional but recommended (link from portfolio site)
- **Environment variables**: Store TMDB API key securely

---

## Success Metrics
When sharing this portfolio piece, you should be able to say:
- "I built a movie recommender using content-based filtering with TF-IDF and cosine similarity"
- "The app uses the TMDB API for real-time data"
- "I optimized for performance with caching, achieving sub-2-second recommendations"
- "I designed it with UX in mind - searchable interface, visual feedback, clear explanations"

---

## Quick Start Guide for AI Development

When handing this to an AI assistant, say:

**"Build this Streamlit app following this SOP. Prioritize Phase 1 first (MVP), then we'll iterate on polish. Start with the provided starter template files."**

The starter template includes:
- `app.py` - Main application with UI structure
- `recommender.py` - Recommendation engine with similarity calculations
- `data_loader.py` - TMDB API integration
- `utils.py` - Helper functions
- `requirements.txt` - All necessary dependencies
- `README.md` - Documentation template

---

**END OF SOP**
