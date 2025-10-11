#!/bin/bash

echo "========================================"
echo "Farmer Resource Pooling System"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Run the application
echo "Starting the application..."
echo ""
echo "The application will be available at: http://localhost:3000"
echo "Press Ctrl+C to stop the server"
echo ""
python app.py
