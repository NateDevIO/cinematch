/**
 * CineMatch - Recommendation Engine (JavaScript)
 * Implements TF-IDF vectorization and cosine similarity for movie recommendations
 */

class MovieRecommender {
    constructor(movies) {
        this.movies = movies;
        this.vocabulary = new Map();
        this.idf = new Map();
        this.tfidfVectors = [];
        this._buildVocabulary();
        this._calculateIDF();
        this._buildTFIDFVectors();
    }

    /**
     * Tokenize and normalize text
     */
    _tokenize(text) {
        if (!text) return [];
        return text.toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length > 2);
    }

    /**
     * Build vocabulary from all movie overviews
     */
    _buildVocabulary() {
        let wordIndex = 0;
        for (const movie of this.movies) {
            const tokens = this._tokenize(movie.overview);
            for (const token of tokens) {
                if (!this.vocabulary.has(token)) {
                    this.vocabulary.set(token, wordIndex++);
                }
            }
        }
    }

    /**
     * Calculate Inverse Document Frequency for each term
     */
    _calculateIDF() {
        const docCount = this.movies.length;
        const termDocCounts = new Map();

        // Count documents containing each term
        for (const movie of this.movies) {
            const tokens = new Set(this._tokenize(movie.overview));
            for (const token of tokens) {
                termDocCounts.set(token, (termDocCounts.get(token) || 0) + 1);
            }
        }

        // Calculate IDF
        for (const [term, count] of termDocCounts) {
            this.idf.set(term, Math.log(docCount / (1 + count)));
        }
    }

    /**
     * Build TF-IDF vectors for all movies
     */
    _buildTFIDFVectors() {
        for (const movie of this.movies) {
            const tokens = this._tokenize(movie.overview);
            const termFreq = new Map();

            // Calculate term frequency
            for (const token of tokens) {
                termFreq.set(token, (termFreq.get(token) || 0) + 1);
            }

            // Build sparse vector
            const vector = new Map();
            for (const [term, freq] of termFreq) {
                const tf = freq / tokens.length;
                const idf = this.idf.get(term) || 0;
                vector.set(term, tf * idf);
            }

            this.tfidfVectors.push(vector);
        }
    }

    /**
     * Calculate cosine similarity between two TF-IDF vectors
     */
    _cosineSimilarity(vec1, vec2) {
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;

        // Calculate dot product and norms
        for (const [term, val1] of vec1) {
            norm1 += val1 * val1;
            if (vec2.has(term)) {
                dotProduct += val1 * vec2.get(term);
            }
        }

        for (const [, val2] of vec2) {
            norm2 += val2 * val2;
        }

        if (norm1 === 0 || norm2 === 0) return 0;
        return dotProduct / (Math.sqrt(norm1) * Math.sqrt(norm2));
    }

    /**
     * Calculate plot similarity for a set of selected movies
     */
    _calculatePlotSimilarity(selectedIndices) {
        const similarities = new Array(this.movies.length).fill(0);

        for (let i = 0; i < this.movies.length; i++) {
            if (selectedIndices.includes(i)) continue;

            let maxSim = 0;
            for (const selIdx of selectedIndices) {
                const sim = this._cosineSimilarity(this.tfidfVectors[selIdx], this.tfidfVectors[i]);
                maxSim = Math.max(maxSim, sim);
            }
            similarities[i] = maxSim;
        }

        return similarities;
    }

    /**
     * Calculate genre similarity using Jaccard index
     */
    _calculateGenreSimilarity(selectedIndices) {
        const similarities = new Array(this.movies.length).fill(0);

        // Get all genres from selected movies
        const selectedGenres = new Set();
        for (const idx of selectedIndices) {
            const genres = this.movies[idx].genres || [];
            genres.forEach(g => selectedGenres.add(g));
        }

        for (let i = 0; i < this.movies.length; i++) {
            const movieGenres = new Set(this.movies[i].genres || []);

            if (movieGenres.size === 0 || selectedGenres.size === 0) {
                similarities[i] = 0;
            } else {
                const intersection = [...movieGenres].filter(g => selectedGenres.has(g)).length;
                const union = new Set([...movieGenres, ...selectedGenres]).size;
                similarities[i] = union > 0 ? intersection / union : 0;
            }
        }

        return similarities;
    }

    /**
     * Calculate director similarity (binary match)
     */
    _calculateDirectorSimilarity(selectedIndices) {
        const similarities = new Array(this.movies.length).fill(0);

        const selectedDirectors = new Set();
        for (const idx of selectedIndices) {
            if (this.movies[idx].director) {
                selectedDirectors.add(this.movies[idx].director);
            }
        }

        for (let i = 0; i < this.movies.length; i++) {
            if (this.movies[i].director && selectedDirectors.has(this.movies[i].director)) {
                similarities[i] = 1.0;
            }
        }

        return similarities;
    }

    /**
     * Calculate cast similarity based on overlapping actors
     */
    _calculateCastSimilarity(selectedIndices) {
        const similarities = new Array(this.movies.length).fill(0);

        const selectedCast = new Set();
        for (const idx of selectedIndices) {
            const cast = this.movies[idx].cast || [];
            cast.slice(0, 5).forEach(c => selectedCast.add(c));
        }

        for (let i = 0; i < this.movies.length; i++) {
            const movieCast = new Set((this.movies[i].cast || []).slice(0, 5));

            if (movieCast.size === 0 || selectedCast.size === 0) {
                similarities[i] = 0;
            } else {
                const intersection = [...movieCast].filter(c => selectedCast.has(c)).length;
                similarities[i] = intersection / movieCast.size;
            }
        }

        return similarities;
    }

    /**
     * Find which selected movie matches the recommendation
     */
    _findMatchedMovie(selectedTitles, selectedIndices, recMovie) {
        let matchedMovie = selectedTitles[0];

        const recDirector = recMovie.director;
        const recCast = new Set((recMovie.cast || []).slice(0, 5));
        const recGenres = new Set(recMovie.genres || []);

        let bestGenreOverlap = [];

        for (let i = 0; i < selectedIndices.length; i++) {
            const selMovie = this.movies[selectedIndices[i]];
            const selDirector = selMovie.director;
            const selCast = new Set((selMovie.cast || []).slice(0, 5));
            const selGenres = new Set(selMovie.genres || []);

            // Director match (highest priority)
            if (recDirector && selDirector && recDirector === selDirector) {
                return { matched: selectedTitles[i], reason: 'director', detail: recDirector };
            }

            // Cast overlap
            const castOverlap = [...recCast].filter(c => selCast.has(c));
            if (castOverlap.length > 0) {
                matchedMovie = selectedTitles[i];
            }

            // Genre overlap
            const genreOverlap = [...recGenres].filter(g => selGenres.has(g));
            if (genreOverlap.length > bestGenreOverlap.length) {
                bestGenreOverlap = genreOverlap;
                if (castOverlap.length === 0) {
                    matchedMovie = selectedTitles[i];
                }
            }
        }

        return { matched: matchedMovie, genres: bestGenreOverlap };
    }

    /**
     * Generate explanation for recommendation
     */
    _generateExplanation(selectedTitles, selectedIndices, recMovie, scores) {
        const explanations = [];
        const matchInfo = this._findMatchedMovie(selectedTitles, selectedIndices, recMovie);

        if (scores.genre > 0.5 && matchInfo.genres && matchInfo.genres.length > 0) {
            explanations.push(`Shares genres: ${matchInfo.genres.slice(0, 2).join(', ')}`);
        }

        if (scores.director > 0.9) {
            explanations.push(`Same director: ${recMovie.director}`);
        }

        if (scores.cast > 0.2) {
            explanations.push('Features similar actors');
        }

        if (scores.plot > 0.3) {
            explanations.push('Similar themes and storytelling');
        }

        if (explanations.length === 0) {
            explanations.push('Strong overall match based on multiple factors');
        }

        return `Because you liked ${matchInfo.matched} → ${explanations.join('; ')}`;
    }

    /**
     * Get movie recommendations based on selected titles
     */
    getRecommendations(selectedTitles, numRecommendations = 5) {
        // Find indices of selected movies
        const selectedIndices = [];
        for (const title of selectedTitles) {
            const idx = this.movies.findIndex(m => m.title === title);
            if (idx !== -1) selectedIndices.push(idx);
        }

        if (selectedIndices.length === 0) return [];

        // Calculate component similarities
        const plotSim = this._calculatePlotSimilarity(selectedIndices);
        const genreSim = this._calculateGenreSimilarity(selectedIndices);
        const directorSim = this._calculateDirectorSimilarity(selectedIndices);
        const castSim = this._calculateCastSimilarity(selectedIndices);

        // Combine with weights
        const combined = this.movies.map((_, i) => {
            if (selectedIndices.includes(i)) return -1;
            return (plotSim[i] * 0.40) + (genreSim[i] * 0.30) +
                (directorSim[i] * 0.15) + (castSim[i] * 0.15);
        });

        // Get top recommendations
        const indices = combined
            .map((score, i) => ({ score, i }))
            .filter(x => x.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, numRecommendations)
            .map(x => x.i);

        // Build recommendation objects
        const recommendations = indices.map(idx => {
            const movie = this.movies[idx];
            const scores = {
                plot: plotSim[idx] / 0.40,
                genre: genreSim[idx] / 0.30,
                director: directorSim[idx] / 0.15,
                cast: castSim[idx] / 0.15
            };

            return {
                movie,
                score: combined[idx],
                explanation: this._generateExplanation(selectedTitles, selectedIndices, movie, scores)
            };
        });

        return recommendations;
    }
}

// Export for use in app.js
window.MovieRecommender = MovieRecommender;
