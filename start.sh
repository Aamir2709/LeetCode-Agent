#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "✅ Installing Playwright browsers..."
playwright install --with-deps
pip install -r requirements.txt

echo "🚀 Running main.py..."
python main.py
