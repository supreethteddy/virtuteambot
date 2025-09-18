#!/bin/bash

# VirtuTeams Control Panel Startup Script

echo "🚀 Starting VirtuTeams Control Panel..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install requirements if needed
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers if needed
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium

# Start the Flask application
echo "🎯 Starting the web application..."
echo "📱 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python3 app.py
