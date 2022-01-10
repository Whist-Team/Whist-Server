"""Errors thrown by DTOs or DAOs."""


class PlayerNotCreatorError(Exception):
    """
    Is raised when a non host tries to execs creator rights.
    """
