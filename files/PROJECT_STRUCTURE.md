# 📦 Movie Recommender Starter Package

This package contains everything you need to build a portfolio-quality movie recommendation app.

## 📄 What's Included

### Core Documentation
1. **`movie_recommender_sop.md`** ⭐ START HERE
   - Complete Standard Operating Procedure
   - Technical specifications
   - Development phases
   - Acceptance criteria
   
2. **`QUICKSTART.md`**
   - Quick reference guide
   - Common issues & solutions
   - Testing checklist
   - Success criteria

3. **`README.md`**
   - User-facing documentation
   - Installation instructions
   - Project overview
   - Update with your personal info before deploying

### Application Files
4. **`app.py`**
   - Main Streamlit application
   - UI/UX implementation
   - User interaction flow
   
5. **`recommender.py`**
   - Recommendation engine
   - Content-based filtering algorithm
   - TF-IDF and cosine similarity
   
6. **`data_loader.py`**
   - TMDB API integration
   - Movie data loading
   - Caching logic
   
7. **`utils.py`**
   - Helper functions
   - Validation and formatting
   - Data processing utilities

### Configuration Files
8. **`requirements.txt`**
   - Python package dependencies
   - Use with: `pip install -r requirements.txt`
   
9. **`.env.example`**
   - Environment variables template
   - Copy to `.env` and add your TMDB API key
   
10. **`.streamlit/config.toml`**
    - Streamlit theme configuration
    - Customize colors and settings

### Setup Scripts
11. **`setup.sh`**
    - Automated setup script
    - Creates virtual environment
    - Installs dependencies
    - Run with: `bash setup.sh`

---

## 🚀 How to Use This Package

### For Developers (Manual Setup)

1. **Create project directory**
   ```bash
   mkdir movie-recommender
   cd movie-recommender
   ```

2. **Copy all files into your project directory**

3. **Get TMDB API key**
   - Sign up at https://www.themoviedb.org/
   - Go to Settings → API
   - Copy your API key

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

5. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

### For AI Assistants (Claude, GPT, etc.)

**Option 1: Hand over the SOP**
```
"Here's an SOP for a movie recommender app. Build Phase 1 (MVP) 
following the specifications in movie_recommender_sop.md. All 
starter code is provided in the accompanying files."
```

**Option 2: Use Claude Code**
```
claudecode

# In the terminal:
"Build a movie recommender following movie_recommender_sop.md. 
Use the provided starter templates as a foundation."
```

**Option 3: Step-by-step development**
```
"Let's build the movie recommender app. First, review the SOP in 
movie_recommender_sop.md and tell me what Phase 1 tasks we need 
to complete."
```

---

## 📂 Recommended Project Structure

After setup, your project should look like this:

```
movie-recommender/
├── app.py                          # Main app
├── recommender.py                  # Engine
├── data_loader.py                  # Data source
├── utils.py                        # Helpers
├── requirements.txt                # Dependencies
├── README.md                      # Documentation
├── .env                           # Your API key (create this)
├── .env.example                   # Template
├── setup.sh                       # Setup script
├── .streamlit/
│   └── config.toml               # Theme config
├── movie_recommender_sop.md      # Full SOP
├── QUICKSTART.md                 # Quick ref
├── PROJECT_STRUCTURE.md          # This file
└── data/                         # (Optional) Local datasets
```

---

## ✅ Quick Start Checklist

Before you begin development:

- [ ] Copy all files to your project directory
- [ ] Get TMDB API key from themoviedb.org
- [ ] Create `.env` file with your API key
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Read `movie_recommender_sop.md` for full specifications
- [ ] Read `QUICKSTART.md` for tips and common issues

---

## 🎯 Development Roadmap

### Phase 1: MVP (Priority)
Focus: Get a working app with basic recommendations

**Key files to modify:**
- `data_loader.py`: Test API connection, load ~250 movies
- `recommender.py`: Verify algorithm works
- `app.py`: Basic UI with movie selection and results

**Success:** User can select 3 movies and get 5 recommendations

### Phase 2: Polish
Focus: Improve UX and add explanations

**Key files to modify:**
- `app.py`: Better UI, loading states, error handling
- `recommender.py`: Add explanation generation
- `README.md`: Update with screenshots

**Success:** App looks professional, recommendations are explained

### Phase 3: Enhancement (Optional)
Focus: Additional features

**Key files to modify:**
- `app.py`: Add filters, visualizations, "How It Works"
- `utils.py`: Add export functionality
- Deployment to Streamlit Cloud

**Success:** App has standout features for portfolio

---

## 💡 Tips for Success

### 1. Start Simple
- Don't try to implement everything at once
- Get Phase 1 working first
- Iterate based on testing

### 2. Test Early, Test Often
- Test with different movie combinations
- Check edge cases (1 movie, 5 movies, obscure titles)
- Verify recommendations make sense

### 3. Focus on Code Quality
- Add docstrings to functions
- Handle errors gracefully
- Use type hints
- Comment complex logic

### 4. Make It Yours
- Customize the theme colors
- Add your personal branding
- Update README with your info
- Create unique features

---

## 🔧 Troubleshooting

### API Issues
**Problem**: "API key not found"
**Solution**: Make sure `.env` exists and contains `TMDB_API_KEY=your_key`

### Slow Performance
**Problem**: Recommendations take >5 seconds
**Solution**: Reduce dataset size to 250 movies initially, check caching

### Poor Recommendations
**Problem**: Recommendations don't make sense
**Solution**: Adjust weights in `recommender.py`, test with different movies

### Import Errors
**Problem**: "Module not found"
**Solution**: Activate virtual environment, reinstall requirements

---

## 📞 Getting Help

If you encounter issues:

1. Check `QUICKSTART.md` for common issues
2. Review the SOP for specifications
3. Test individual components (data loading, similarity calculation)
4. Ask specific questions with error messages

---

## 🎓 Learning Resources

Want to understand the tech better?

- **Content-Based Filtering**: [Wikipedia](https://en.wikipedia.org/wiki/Recommender_system#Content-based_filtering)
- **TF-IDF**: [sklearn docs](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- **Cosine Similarity**: [sklearn docs](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- **Streamlit**: [Official docs](https://docs.streamlit.io)

---

## ✨ Final Notes

This starter package provides:
- ✅ Complete SOP with specifications
- ✅ Fully commented starter code
- ✅ Configuration files
- ✅ Documentation templates
- ✅ Quick reference guides

**What you need to add:**
- 🔑 Your TMDB API key
- 🎨 Your personal branding
- 🧪 Testing and refinement
- 🚀 Deployment

**Time estimate:**
- Phase 1 (MVP): 1-2 days
- Phase 2 (Polish): 1-2 days
- Phase 3 (Enhancement): 2-3 days

Good luck building your portfolio project! 🎬✨
