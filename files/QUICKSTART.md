# Quick Reference Guide

## 🚀 Getting Started

### For AI Assistants
If you're an AI assistant building this app, start here:

1. **Read the SOP**: `movie_recommender_sop.md` contains complete specifications
2. **Review starter code**: All files are structured and commented
3. **Priority**: Build Phase 1 (MVP) first, then iterate

### Development Phases

**Phase 1 - MVP (Week 1)**
- [ ] Set up project structure ✅ (provided)
- [ ] Get TMDB API key and test connection
- [ ] Implement basic recommendation engine
- [ ] Create simple UI with movie selection
- [ ] Display recommendations with posters
- [ ] Test with 3-5 different movie combinations

**Phase 2 - Polish (Week 2)**
- [ ] Add recommendation explanations
- [ ] Improve UI/UX (styling, responsive design)
- [ ] Add performance caching
- [ ] Write comprehensive README
- [ ] Add error handling for edge cases

**Phase 3 - Enhancements (Week 3+)**
- [ ] "How It Works" section
- [ ] Data visualizations (genre comparisons)
- [ ] Optional filters (mood, year range)
- [ ] Export recommendations feature

## 📁 File Overview

| File | Purpose | What to Focus On |
|------|---------|------------------|
| `app.py` | Main UI | User interaction flow, layout |
| `recommender.py` | Core algorithm | Similarity calculations, weighting |
| `data_loader.py` | Data source | API integration, caching |
| `utils.py` | Helpers | Validation, formatting |
| `requirements.txt` | Dependencies | Keep minimal |
| `README.md` | Documentation | Update with your info |

## 🎯 Key Implementation Points

### 1. Recommendation Algorithm
```python
# Weighted similarity calculation
plot_similarity (TF-IDF + cosine) → 40%
genre_overlap (Jaccard) → 30%
director_match (binary) → 15%
cast_overlap (Jaccard) → 15%
```

### 2. TMDB API Usage
```python
# Rate limits: 5000 requests/day
# Cache aggressively: @st.cache_data(ttl=3600)
# Handle failures gracefully
```

### 3. Performance Targets
- Initial load: < 3 seconds
- Recommendations: < 2 seconds
- Use caching for TF-IDF matrix

### 4. User Experience
- Search (not dropdown) for movie selection
- Show visual feedback (posters)
- Clear explanations for recommendations
- Loading spinners for async operations

## 🧪 Testing Checklist

Test with these scenarios before considering MVP complete:

- [ ] **Single movie**: Select 1 movie, get 5 recommendations
- [ ] **Diverse genres**: Select action + comedy + drama
- [ ] **Same franchise**: Select 3 Marvel movies
- [ ] **Classics**: Select old movies (pre-2000)
- [ ] **Recent**: Select movies from 2023-2024
- [ ] **Obscure movie**: Try a movie not in dataset
- [ ] **Rapid clicks**: Stress test the UI
- [ ] **Mobile view**: Check responsive design

## 💡 Common Issues & Solutions

### Issue: API rate limiting
**Solution**: Increase cache TTL, load fewer movies initially (250 instead of 500)

### Issue: Slow recommendations
**Solution**: Precompute TF-IDF matrix, use @st.cache_resource for recommender

### Issue: Poor recommendation quality
**Solution**: Adjust feature weights, require minimum similarity threshold (e.g., 0.2)

### Issue: Empty results
**Solution**: Lower similarity threshold, increase dataset size

## 🎨 Customization Quick Tips

### Change color scheme
Edit `.streamlit/config.toml`:
```toml
primaryColor = "#YOUR_COLOR"  # Buttons, accents
backgroundColor = "#YOUR_BG"   # Main background
```

### Adjust recommendation weights
Edit `recommender.py`:
```python
plot_sim * 0.40  # ← Change these
genre_sim * 0.30
director_sim * 0.15
cast_sim * 0.15
```

### Modify UI layout
Edit `app.py`:
```python
st.columns([1, 2])  # ← Adjust column ratios
num_recommendations = st.slider(...)  # ← Change defaults
```

## 📝 Code Quality Checklist

Before submitting/deploying:

- [ ] All functions have docstrings
- [ ] Type hints added (Python 3.9+)
- [ ] Error handling for API failures
- [ ] Input validation for user selections
- [ ] No hardcoded values (use constants)
- [ ] Logging added for debugging
- [ ] Tests written (at least basic ones)
- [ ] README updated with your info
- [ ] Screenshots added
- [ ] Code formatted (black, pylint)

## 🚢 Deployment Checklist

- [ ] TMDB API key in Streamlit secrets
- [ ] requirements.txt is minimal
- [ ] .env.example provided (no real keys!)
- [ ] README has deployment instructions
- [ ] App tested on deployed environment
- [ ] Custom domain configured (optional)
- [ ] Analytics added (optional)

## 📚 Resources

### TMDB API
- Docs: https://developers.themoviedb.org/3
- Get API key: https://www.themoviedb.org/settings/api
- Rate limits: 40 requests/10 seconds

### Streamlit
- Docs: https://docs.streamlit.io
- Deployment: https://share.streamlit.io
- Components: https://streamlit.io/components

### scikit-learn
- TF-IDF: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
- Cosine similarity: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

## 🎯 Success Criteria

Your app is portfolio-ready when:

1. ✅ Recommendations make sense (test subjectively)
2. ✅ UI is polished (clean, professional)
3. ✅ Performance is good (< 2s for recommendations)
4. ✅ Code is clean (documented, modular)
5. ✅ Deployed and accessible via URL
6. ✅ README explains approach clearly

## 📞 Need Help?

When asking for help, provide:
- What you tried
- Error messages (full traceback)
- Example movie selections that fail
- Your Python/package versions

---

**Remember**: Focus on Phase 1 first. A working MVP is better than a half-finished feature-rich app!
