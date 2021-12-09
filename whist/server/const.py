"""Constants at runtime"""
import os

HOST_ADDR = os.getenv('HOST_ADDR')
HOST_PORT = os.getenv('HOST_PORT')

HEX_32_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

TEST_DATABASE = 'localhost'

ALGORITHM = os.getenv('ALGORITHM', 'HS256')
DATABASE_NAME = os.getenv('DATABASE_NAME', TEST_DATABASE)
SECRET_KEY = os.getenv('SECRET_KEY', HEX_32_KEY)

INITIAL_RATING = 1200
