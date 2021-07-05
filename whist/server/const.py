import os

TEST_DATABASE = 'test_database'

DATABASE_NAME = os.getenv('DATABASE_NAME', TEST_DATABASE)
