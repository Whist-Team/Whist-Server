"""Utility functions for the API"""
from fastapi import HTTPException


def create_http_error(message: str, status_code: int) -> HTTPException:
    """
    Creates a HTTP Exception from a message and the status code.
    :param message: Custom message to be displayed.
    :param status_code: HTTP Status Code of the error
    :return: final error to be raised
    """
    return HTTPException(
        status_code=status_code,
        detail=message,
        headers={'WWW-Authenticate': 'Bearer'})
