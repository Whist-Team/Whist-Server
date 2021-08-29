[![codecov](https://codecov.io/gh/Whist-Team/Whist-Server/branch/main/graph/badge.svg)](https://codecov.io/gh/Whist-Team/Whist-Server)
# Whist-Server

## Run tests
```bash
# Create venv
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel

# Install with 'testing' extras
pip install -e .[testing]

# Run tests
python -m pytest
```
