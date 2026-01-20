# 🎬 CineMatch

A portfolio-quality movie recommendation system using content-based filtering and machine learning to suggest films based on user preferences.

*Coded by Nate*

## 🌟 Features

- **Smart Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **4500+ Movies**: Comprehensive database including classics, blockbusters, and hidden gems
- **Rich Metadata**: Integrates with TMDB API for movie posters, cast, and plot information
- **Explainable AI**: Clear explanations for why each movie was recommended
- **Searchable Input**: Type-ahead search to quickly find any movie
- **Watchlist**: Save movies for later (persisted in browser)
- **Professional UI**: Dark theme with gradients, animations, and responsive design
- **Static Hosting**: Pure HTML/CSS/JS - no server required, no sleeping apps

## 🎯 Technical Highlights

This project demonstrates:

- **Data Science**: Content-based recommendation algorithm with weighted feature engineering
- **Machine Learning**: TF-IDF vectorization and cosine similarity calculations in JavaScript
- **API Integration**: TMDB API for movie data and automated weekly updates
- **Frontend Development**: Vanilla JavaScript with custom searchable dropdowns
- **DevOps**: GitHub Actions for automated cache updates

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Recommendation Engine** | Custom TF-IDF + Cosine Similarity (JS) |
| **Data Source** | TMDB API |
| **DevOps** | GitHub Actions (automated weekly updates) |
| **Deployment** | Vercel / Netlify / GitHub Pages |

## 🚀 Quick Start

### Option 1: Static Version (Recommended)

The `cinematch-js` folder contains the pure HTML/CSS/JavaScript version:

```bash
cd cinematch-js
python -m http.server 8080
# Open http://localhost:8080
```

### Option 2: Streamlit Version (Legacy)

The root folder contains the original Streamlit version:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 How It Works

### Algorithm Overview

The recommendation engine uses **content-based filtering**:

1. **Feature Extraction**
   - Plot descriptions → TF-IDF vectors
   - Genres → Binary feature vectors
   - Director → Exact match indicator
   - Cast → Overlap calculation

2. **Similarity Calculation**
   - Weighted combination of features:
     - Plot similarity (TF-IDF + cosine): 40%
     - Genre overlap (Jaccard): 30%
     - Director match: 15%
     - Cast overlap: 15%

3. **Ranking & Filtering**
   - Exclude already-selected movies
   - Sort by combined similarity score
   - Return top 5 recommendations with explanations

## 🏗️ Project Structure

```
movie-recommender/
├── cinematch-js/           # Static JavaScript version
│   ├── index.html          # Main HTML page
│   ├── styles.css          # Dark theme styling
│   ├── app.js              # UI interactions
│   ├── recommender.js      # TF-IDF recommendation engine
│   └── movies_cache.json   # 4500+ movie database
├── .github/workflows/
│   └── update-cache.yml    # Weekly auto-update workflow
├── build_cache.py          # Script to refresh movie database
├── app.py                  # Streamlit version (legacy)
├── recommender.py          # Python recommendation engine
└── README.md
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push the `cinematch-js` folder to GitHub
2. Connect to Vercel
3. Set root directory to `cinematch-js`
4. Deploy - no build step needed!

### GitHub Pages

1. Go to repo Settings → Pages
2. Set source to `cinematch-js` folder
3. Save and deploy

### Automated Updates

The GitHub Actions workflow runs weekly to fetch new movies. Add your `TMDB_API_KEY` as a repository secret for it to work.

## 📈 Performance

- **Initial load**: ~2 seconds (4.5MB database)
- **Recommendation generation**: < 1 second
- **Database**: 4,500+ movies with weekly updates
- **No server required**: Static files only

## 📝 Future Enhancements

- [ ] Collaborative filtering (user-based recommendations)
- [ ] Integration with streaming services
- [ ] Multi-language support
- [ ] Mobile app version

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for the excellent movie database API
- Data refreshed automatically via GitHub Actions

---

⭐ If you found this project helpful, please consider giving it a star!
