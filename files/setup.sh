#!/bin/bash

# Movie Recommender Setup Script
# Run this script to set up the project quickly

echo "🎬 Setting up Movie Recommender App..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "⚠️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Set up environment file
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your TMDB API key!"
    echo "   Get your free API key at: https://www.themoviedb.org/settings/api"
else
    echo "⚠️  .env file already exists"
fi

# Create data directory (if using local datasets)
mkdir -p data

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your TMDB API key"
echo "2. Run the app with: streamlit run app.py"
echo "3. Open http://localhost:8501 in your browser"
echo ""
echo "Need help? Check README.md for detailed instructions."
