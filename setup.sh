#!/bin/bash

# Resume ATS Tool Setup Script
echo "Setting up Resume ATS Tool..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo ""
echo "To use the Resume ATS Tool:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the tool: python resume_ats.py [resume_file]"
echo ""
echo "Example usage:"
echo "  python resume_ats.py sample_resume.txt"
echo "  python resume_ats.py resume.pdf --keywords python javascript react"
echo "  python resume_ats.py resume.docx --output analysis.json"