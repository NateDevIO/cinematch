/**
 * CineMatch - Main Application
 * Handles UI interactions, movie selection, and recommendation display
 */

let movies = [];
let recommender = null;
let selectedMovies = [];
let watchlist = {};

// DOM Elements
const loadingEl = document.getElementById('loading');
const mainContentEl = document.getElementById('main-content');
const statusMessageEl = document.getElementById('status-message');
const numMoviesInput = document.getElementById('num-movies');
const movieSelectorsEl = document.getElementById('movie-selectors');
const selectedMoviesEl = document.getElementById('selected-movies');
const selectedMoviesGridEl = document.getElementById('selected-movies-grid');
const getRecommendationsBtn = document.getElementById('get-recommendations');
const recommendationsSection = document.getElementById('recommendations-section');
const recommendationsIntro = document.getElementById('recommendations-intro');
const recommendationsGrid = document.getElementById('recommendations-grid');
const watchlistSidebar = document.getElementById('watchlist-sidebar');
const toggleWatchlistBtn = document.getElementById('toggle-watchlist');
const watchlistCountEl = document.getElementById('watchlist-count');
const watchlistItemsEl = document.getElementById('watchlist-items');
const clearWatchlistBtn = document.getElementById('clear-watchlist');

/**
 * Initialize the application
 */
async function init() {
    try {
        // Load movies
        const response = await fetch('movies_cache.json');
        movies = await response.json();

        // Initialize recommender
        recommender = new MovieRecommender(movies);

        // Load watchlist from localStorage
        loadWatchlist();

        // Hide loading, show content
        loadingEl.style.display = 'none';
        mainContentEl.style.display = 'block';

        // Show success message
        showStatus(`Loaded ${movies.length.toLocaleString()} movies. Ready to recommend!`);

        // Set up event listeners
        setupEventListeners();

        // Create initial movie selectors
        updateMovieSelectors();

    } catch (error) {
        console.error('Error loading movies:', error);
        loadingEl.innerHTML = `
            <p style="color: #ff6b6b;">Failed to load movie database.</p>
            <p>Please make sure movies_cache.json is available.</p>
        `;
    }
}

/**
 * Show status message
 */
function showStatus(message) {
    statusMessageEl.textContent = message;
    statusMessageEl.classList.add('visible');
    setTimeout(() => {
        statusMessageEl.classList.remove('visible');
    }, 3000);
}

/**
 * Set up event listeners
 */
function setupEventListeners() {
    numMoviesInput.addEventListener('change', updateMovieSelectors);
    getRecommendationsBtn.addEventListener('click', handleGetRecommendations);
    toggleWatchlistBtn.addEventListener('click', toggleWatchlist);
    clearWatchlistBtn.addEventListener('click', clearWatchlist);
}

/**
 * Update movie selector dropdowns based on number input
 */
function updateMovieSelectors() {
    const numSelectors = parseInt(numMoviesInput.value) || 3;
    movieSelectorsEl.innerHTML = '';
    selectedMovies = [];

    // Sort movies alphabetically once
    const sortedMovies = [...movies].sort((a, b) => a.title.localeCompare(b.title));

    for (let i = 0; i < numSelectors; i++) {
        const selectorDiv = document.createElement('div');
        selectorDiv.className = 'movie-selector';

        const label = document.createElement('label');
        label.textContent = `Movie ${i + 1}:`;
        label.htmlFor = `movie-search-${i}`;

        // Create searchable input container
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';

        const input = document.createElement('input');
        input.type = 'text';
        input.id = `movie-search-${i}`;
        input.className = 'movie-search-input';
        input.placeholder = 'Type to search movies...';
        input.autocomplete = 'off';

        const dropdown = document.createElement('div');
        dropdown.className = 'search-dropdown';
        dropdown.id = `dropdown-${i}`;

        // Handle input typing
        input.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            if (query.length < 1) {
                dropdown.innerHTML = '';
                dropdown.classList.remove('visible');
                return;
            }

            // Filter movies matching query
            const matches = sortedMovies
                .filter(m => m.title.toLowerCase().includes(query))
                .slice(0, 10); // Limit to 10 results

            if (matches.length > 0) {
                dropdown.innerHTML = matches.map(movie => `
                    <div class="search-option" data-title="${movie.title.replace(/"/g, '&quot;')}" data-index="${i}">
                        <span class="option-title">${highlightMatch(movie.title, query)}</span>
                        <span class="option-year">(${movie.year || 'N/A'})</span>
                    </div>
                `).join('');
                dropdown.classList.add('visible');

                // Add click handlers to options
                dropdown.querySelectorAll('.search-option').forEach(option => {
                    option.addEventListener('click', () => {
                        selectMovie(i, option.dataset.title);
                        input.value = option.dataset.title;
                        dropdown.classList.remove('visible');
                    });
                });
            } else {
                dropdown.innerHTML = '<div class="search-option no-results">No movies found</div>';
                dropdown.classList.add('visible');
            }
        });

        // Handle keyboard navigation
        input.addEventListener('keydown', (e) => {
            const options = dropdown.querySelectorAll('.search-option:not(.no-results)');
            const activeOption = dropdown.querySelector('.search-option.active');

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (!activeOption && options.length > 0) {
                    options[0].classList.add('active');
                } else if (activeOption && activeOption.nextElementSibling) {
                    activeOption.classList.remove('active');
                    activeOption.nextElementSibling.classList.add('active');
                }
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (activeOption && activeOption.previousElementSibling) {
                    activeOption.classList.remove('active');
                    activeOption.previousElementSibling.classList.add('active');
                }
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (activeOption) {
                    selectMovie(i, activeOption.dataset.title);
                    input.value = activeOption.dataset.title;
                    dropdown.classList.remove('visible');
                }
            } else if (e.key === 'Escape') {
                dropdown.classList.remove('visible');
            }
        });

        // Close dropdown when clicking outside
        input.addEventListener('blur', () => {
            setTimeout(() => dropdown.classList.remove('visible'), 200);
        });

        // Show dropdown on focus if there's text
        input.addEventListener('focus', () => {
            if (input.value.length >= 1) {
                input.dispatchEvent(new Event('input'));
            }
        });

        searchContainer.appendChild(input);
        searchContainer.appendChild(dropdown);
        selectorDiv.appendChild(label);
        selectorDiv.appendChild(searchContainer);
        movieSelectorsEl.appendChild(selectorDiv);
    }

    updateSelectedMoviesDisplay();
}

/**
 * Highlight matching text in search results
 */
function highlightMatch(title, query) {
    const index = title.toLowerCase().indexOf(query);
    if (index === -1) return title;
    return title.slice(0, index) +
        '<strong>' + title.slice(index, index + query.length) + '</strong>' +
        title.slice(index + query.length);
}

/**
 * Select a movie by index and title
 */
function selectMovie(index, title) {
    const movie = movies.find(m => m.title === title);
    if (!movie) return;

    // Store selection
    const currentSelections = getCurrentSelections();
    currentSelections[index] = movie;

    // Update selected movies array (no duplicates)
    selectedMovies = Object.values(currentSelections).filter(m => m);

    updateSelectedMoviesDisplay();
}

/**
 * Get current selections from inputs
 */
function getCurrentSelections() {
    const selections = {};
    const inputs = movieSelectorsEl.querySelectorAll('.movie-search-input');
    inputs.forEach((input, i) => {
        if (input.value) {
            const movie = movies.find(m => m.title === input.value);
            if (movie) {
                selections[i] = movie;
            }
        }
    });
    return selections;
}

/**
 * Handle movie selection changes
 */
function handleMovieSelection() {
    selectedMovies = [];
    const selects = movieSelectorsEl.querySelectorAll('select');

    for (const select of selects) {
        if (select.value) {
            const movie = movies.find(m => m.title === select.value);
            if (movie && !selectedMovies.find(m => m.title === movie.title)) {
                selectedMovies.push(movie);
            }
        }
    }

    updateSelectedMoviesDisplay();
}

/**
 * Update the selected movies display
 */
function updateSelectedMoviesDisplay() {
    if (selectedMovies.length > 0) {
        selectedMoviesEl.classList.add('visible');
        selectedMoviesGridEl.innerHTML = selectedMovies.map(movie => `
            <div class="selected-movie-card">
                <img src="${movie.poster_url || 'https://via.placeholder.com/120x180?text=No+Poster'}" 
                     alt="${movie.title}" 
                     onerror="this.src='https://via.placeholder.com/120x180?text=No+Poster'">
                <div class="title">${movie.title}</div>
            </div>
        `).join('');
    } else {
        selectedMoviesEl.classList.remove('visible');
        selectedMoviesGridEl.innerHTML = '';
    }

    // Update button state
    getRecommendationsBtn.disabled = selectedMovies.length === 0;
}

/**
 * Handle get recommendations button click
 */
function handleGetRecommendations() {
    if (selectedMovies.length === 0) return;

    const selectedTitles = selectedMovies.map(m => m.title);
    const recommendations = recommender.getRecommendations(selectedTitles, 5);

    displayRecommendations(recommendations);
}

/**
 * Display recommendations
 */
function displayRecommendations(recommendations) {
    if (recommendations.length === 0) {
        recommendationsSection.style.display = 'block';
        recommendationsIntro.textContent = 'No recommendations found. Try selecting different movies.';
        recommendationsGrid.innerHTML = '';
        return;
    }

    recommendationsSection.style.display = 'block';
    recommendationsIntro.textContent = `Based on your selection, here are ${recommendations.length} movies we think you'll love:`;

    recommendationsGrid.innerHTML = recommendations.map((rec, index) => {
        const movie = rec.movie;
        const genres = movie.genres || [];
        const genreBadges = genres.map(g => {
            const className = getGenreClass(g);
            return `<span class="genre-badge ${className}">${g}</span>`;
        }).join('');

        const year = movie.year || 'N/A';
        const rating = movie.rating ? movie.rating.toFixed(1) : 'N/A';
        const stars = movie.rating ? '⭐'.repeat(Math.round(movie.rating / 2)) : '';

        const trailerQuery = encodeURIComponent(`${movie.title} ${year} official trailer`);
        const trailerUrl = `https://www.youtube.com/results?search_query=${trailerQuery}`;

        const movieKey = `${movie.title}_${year}`;
        const isSaved = watchlist[movieKey] != null;

        return `
            <div class="recommendation-card" style="animation-delay: ${index * 0.1}s">
                <img class="poster" 
                     src="${movie.poster_url || 'https://via.placeholder.com/150x225?text=No+Poster'}" 
                     alt="${movie.title}"
                     onerror="this.src='https://via.placeholder.com/150x225?text=No+Poster'">
                <div class="details">
                    <h3>${movie.title} (${year})</h3>
                    <div class="rating">${stars} <strong>${rating}</strong>/10</div>
                    <div class="genre-badges">${genreBadges}</div>
                    <div class="recommendation-reason">💡 ${rec.explanation}</div>
                    <div class="action-buttons">
                        <a href="${trailerUrl}" target="_blank" class="trailer-btn">▶️ Watch Trailer</a>
                        <button class="save-btn ${isSaved ? 'saved' : ''}" 
                                onclick="toggleSaveMovie('${movieKey.replace(/'/g, "\\'")}', ${JSON.stringify(movie).replace(/"/g, '&quot;')})">
                            ${isSaved ? '✓ Saved' : '🔖 Save'}
                        </button>
                    </div>
                    <details class="plot-summary">
                        <summary>📖 Plot Summary</summary>
                        <p>${movie.overview || 'No plot summary available.'}</p>
                    </details>
                </div>
            </div>
        `;
    }).join('');

    // Scroll to recommendations
    recommendationsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Get CSS class for genre badge
 */
function getGenreClass(genre) {
    const genreLower = genre.toLowerCase().replace(/\s+/g, '-');
    const knownGenres = ['action', 'comedy', 'drama', 'horror', 'science-fiction',
        'romance', 'thriller', 'animation', 'adventure', 'fantasy'];
    return knownGenres.includes(genreLower) ? `genre-${genreLower}` : '';
}

/**
 * Toggle watchlist sidebar
 */
function toggleWatchlist() {
    watchlistSidebar.classList.toggle('open');
}

/**
 * Load watchlist from localStorage
 */
function loadWatchlist() {
    try {
        const saved = localStorage.getItem('cinematch-watchlist');
        if (saved) {
            watchlist = JSON.parse(saved);
        }
    } catch (e) {
        console.error('Error loading watchlist:', e);
        watchlist = {};
    }
    updateWatchlistDisplay();
}

/**
 * Save watchlist to localStorage
 */
function saveWatchlist() {
    try {
        localStorage.setItem('cinematch-watchlist', JSON.stringify(watchlist));
    } catch (e) {
        console.error('Error saving watchlist:', e);
    }
    updateWatchlistDisplay();
}

/**
 * Toggle save movie to watchlist
 */
function toggleSaveMovie(movieKey, movie) {
    if (watchlist[movieKey]) {
        delete watchlist[movieKey];
    } else {
        watchlist[movieKey] = movie;
    }
    saveWatchlist();

    // Update button state
    const btn = document.querySelector(`button[onclick*="${movieKey.replace(/'/g, "\\'")}"]`);
    if (btn) {
        if (watchlist[movieKey]) {
            btn.classList.add('saved');
            btn.textContent = '✓ Saved';
        } else {
            btn.classList.remove('saved');
            btn.textContent = '🔖 Save';
        }
    }
}

/**
 * Update watchlist display
 */
function updateWatchlistDisplay() {
    const count = Object.keys(watchlist).length;

    if (count > 0) {
        watchlistCountEl.textContent = `${count} movie${count !== 1 ? 's' : ''} saved`;
        clearWatchlistBtn.style.display = 'block';

        watchlistItemsEl.innerHTML = Object.entries(watchlist).map(([key, movie]) => `
            <div class="watchlist-item">
                <strong>${movie.title}</strong> (${movie.year || 'N/A'})
            </div>
        `).join('');
    } else {
        watchlistCountEl.textContent = 'No movies saved yet';
        clearWatchlistBtn.style.display = 'none';
        watchlistItemsEl.innerHTML = '<p style="font-size: 0.85rem; color: var(--text-secondary);">Click "Save" on any recommendation to add it here!</p>';
    }
}

/**
 * Clear watchlist
 */
function clearWatchlist() {
    if (confirm('Are you sure you want to clear your watchlist?')) {
        watchlist = {};
        saveWatchlist();

        // Update all save buttons on page
        document.querySelectorAll('.save-btn.saved').forEach(btn => {
            btn.classList.remove('saved');
            btn.textContent = '🔖 Save';
        });
    }
}

// Make toggleSaveMovie available globally
window.toggleSaveMovie = toggleSaveMovie;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);
