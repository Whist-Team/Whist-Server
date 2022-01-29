[![codecov](https://codecov.io/gh/Whist-Team/Whist-Server/branch/main/graph/badge.svg)](https://codecov.io/gh/Whist-Team/Whist-Server) [![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

# Whist-Server

This is the REST API server of a Whist game. It provides user management, session organization and
a convenient interface for the rules' implementation of
[Whist-Core](https://github.com/Whist-Team/Whist-Core).

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
