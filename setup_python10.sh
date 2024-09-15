#!/bin/bash

# Install Python 3.10 using pyenv if not already installed
pyenv install -s 3.10.0

# Set local Python version to 3.10.0
pyenv local 3.10.0

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# Print Python version to confirm
python --version

echo "Python 3.10 environment is now activated!"