# Virtual Environment Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip
- virtualenv (optional)

## Setup Instructions

### 1. Create Virtual Environment
```bash
# Navigate to the project directory
cd /path/to/MCP

# Create virtual environment
python3 -m venv .venv
```

### 2. Activate Virtual Environment
#### On macOS/Linux:
```bash
source .venv/bin/activate
```

#### On Windows:
```cmd
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Install the project in editable mode
pip install -e .

# Optional: Install development dependencies
pip install -e .[dev]

# Optional: Install machine learning dependencies
pip install -e .[ml]
```

### 4. Deactivate Virtual Environment
```bash
deactivate
```

## Troubleshooting
- Ensure you have the correct Python version installed
- Check that all dependencies are compatible
- Verify your system's Python path

## IDE Integration
Most IDEs (VSCode, PyCharm) can automatically detect and use the `.venv` virtual environment.
