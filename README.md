[![codecov](https://codecov.io/gh/Whist-Team/Whist-Server/branch/main/graph/badge.svg)](https://codecov.io/gh/Whist-Team/Whist-Server)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![PyPI](https://img.shields.io/pypi/v/whist-server)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whist-server)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/whist-server)
![GitHub repo size](https://img.shields.io/github/repo-size/whist-team/whist-server)
![Lines of code](https://img.shields.io/tokei/lines/github/whist-team/whist-server)
![PyPI - Downloads](https://img.shields.io/pypi/dm/whist-server)
![PyPI - License](https://img.shields.io/pypi/l/whist-server)

# Whist-Server

This is the REST API server of a Whist game. It provides user management, session organization and
a convenient interface for the rules' implementation of
[Whist-Core](https://github.com/Whist-Team/Whist-Core).

## Development

### Setup
You need [Poetry](https://python-poetry.org/) for development.
```bash
# Create venv and install deps
poetry install
```
The Python virtual environment will be created in the `.venv` directory.

### Run tests/lint
```bash
# Run tests (in venv)
python -m pytest # or pylint...
# OR
poetry run python -m pytest
```

### Build
Generates `sdist` and `bdist_wheel`.
```bash
poetry build
```

### Publish

You need the environment variable `POETRY_PYPI_TOKEN_PYPI` filled with a PyPI token.

```bash
poetry build
poetry publish
# OR
poetry publish --build
```

### Run

In order to use GitHub SSO you need to set two environment variables. At the moment they are
mandatory.

```dotenv
GITHUB_CLIENT_ID # This is the GitHub Identifier
GITHUB_CLIENT_SECRET # During creation this secret is generated.
GITHUB_REDIRECT_URL=http://HOST:PORT/oauth2/github/ # Only required for Browser Application with the ability to redirect.
```

If you want to use Splunk you require an environment variable with the authentication token: 
`SPLUNK_TOKEN` and you have to start the server with optional arguments `--splunk_host` and 
`--splunk-port`.

In order to run the application it must be started like this:

```shell
python -m whist_server --reload --admin_name=root --admin_pwd=password 0.0.0.0 8080
```

:warning: A mongodb instance is required to run before launching the `Whist-Server`.
