# 🎬 CineMatch

A portfolio-quality movie recommendation system built with Streamlit, using content-based filtering and machine learning to suggest films based on user preferences.

*Coded by Nate*

![App Screenshot](screenshot.png)
*Add your screenshot here*

## 🌟 Features

- **Smart Recommendations**: Content-based filtering using TF-IDF and cosine similarity
- **Rich Metadata**: Integrates with TMDB API for movie posters, cast, and plot information
- **Explainable AI**: Clear explanations for why each movie was recommended
- **Flexible Input**: Select 1-5 favorite movies to get personalized suggestions
- **Professional UI**: Clean, responsive design with visual movie cards
- **Performance Optimized**: Caching for sub-2-second recommendation generation

## 🎯 Technical Highlights

This project demonstrates:

- **Data Science**: Content-based recommendation algorithm with weighted feature engineering
- **Machine Learning**: TF-IDF vectorization and cosine similarity calculations using scikit-learn
- **API Integration**: TMDB API for real-time movie data
- **Software Engineering**: Modular code architecture with separation of concerns
- **User Experience**: Intuitive interface with visual feedback and explanations

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- TMDB API key (free at [themoviedb.org](https://www.themoviedb.org/settings/api))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/movie-recommender.git
   cd movie-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your TMDB API key
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

## 🔧 Configuration

### TMDB API Key

1. Sign up at [TMDB](https://www.themoviedb.org/signup)
2. Go to Settings → API
3. Request an API key (choose "Developer" option)
4. Add to `.env` file:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

### Streamlit Theme

Customize the look in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#E50914"
backgroundColor = "#141414"
secondaryBackgroundColor = "#2D2D2D"
textColor = "#FFFFFF"
font = "sans serif"
```

## 📊 How It Works

### Algorithm Overview

The recommendation engine uses **content-based filtering** with the following approach:

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
   - Return top N recommendations

### Example

If you select:
- "Inception" (2010)
- "Interstellar" (2014)
- "The Prestige" (2006)

The app will:
1. Identify common themes (Christopher Nolan, complex narratives, sci-fi)
2. Calculate similarity to all movies in database
3. Recommend similar films like "Arrival", "Shutter Island", "Memento"

## 🏗️ Project Structure

```
movie-recommender/
├── app.py                  # Main Streamlit application
├── recommender.py          # Recommendation engine logic
├── data_loader.py          # TMDB API integration
├── utils.py                # Helper functions
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .env.example           # Environment variables template
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── tests/                 # Unit tests (optional)
    └── test_recommender.py
```

## 🧪 Testing

Run unit tests:
```bash
pytest tests/
```

Test the app with diverse movie selections:
- Single movie input
- 5 movies from different genres
- Movies from same franchise
- Obscure titles

## 📈 Performance

- **Initial load**: < 3 seconds (with caching)
- **Recommendation generation**: < 2 seconds
- **Dataset size**: 500 movies (configurable)
- **API calls**: Cached for 1 hour

## 🚀 Deployment

### Streamlit Community Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your repository
4. Add `TMDB_API_KEY` as a secret in the dashboard

### Alternative Platforms

- **Heroku**: Use `setup.sh` and `Procfile`
- **AWS/GCP**: Deploy with Docker
- **Vercel**: Use serverless deployment

## 🎨 Customization

### Add New Features

1. **Mood Filters** (Phase 3)
   - Edit `app.py` to add checkboxes for moods
   - Update `recommender.py` to filter by mood tags

2. **Data Visualizations**
   - Add Plotly charts to show genre distributions
   - Compare user preferences vs. recommendations

3. **User Accounts**
   - Integrate Streamlit authentication
   - Save user preferences and history

### Modify Algorithm

Edit `recommender.py` to adjust:
- **Feature weights**: Change the 40/30/15/15 split
- **Similarity metric**: Try Pearson correlation instead of cosine
- **Additional features**: Add movie runtime, budget, keywords

## 📝 Future Enhancements

- [ ] Collaborative filtering (user-based recommendations)
- [ ] Hybrid approach (content + collaborative)
- [ ] Movie watchlist functionality
- [ ] Export recommendations to PDF
- [ ] Integration with streaming services (show where to watch)
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for the excellent movie database API
- [Streamlit](https://streamlit.io/) for the intuitive web framework
- [scikit-learn](https://scikit-learn.org/) for ML tools

## 📧 Contact

**Your Name**
- Portfolio: [yourportfolio.com](https://yourportfolio.com)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- GitHub: [github.com/yourusername](https://github.com/yourusername)

---

⭐ If you found this project helpful, please consider giving it a star!
