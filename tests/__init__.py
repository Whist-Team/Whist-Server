from pathlib import Path

from dotenv import load_dotenv

test_env_path = Path('test.env')
load_dotenv(dotenv_path=test_env_path)
