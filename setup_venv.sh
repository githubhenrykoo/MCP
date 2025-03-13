#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install the project in editable mode
pip install -e .

# Optional: Install development dependencies
pip install -e .[dev]

# Optional: Install machine learning dependencies
pip install -e .[ml]

# Display installed packages
pip list

# Deactivate virtual environment (optional, comment out if you want to remain in venv)
# deactivate
