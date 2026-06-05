#!/bin/bash
set -e

echo "Setting up Nike_Explorer virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -e ".[test]"

echo "Installing playwright browsers..."
playwright install

echo "Setup complete! To run the application:"
echo "source venv/bin/activate"
echo "chainlit run ui/app.py"
