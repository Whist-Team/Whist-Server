"""Errors thrown by DTOs or DAOs."""


class PlayerNotCreatorError(Exception):
    """
    Is raised when a non host tries to execs creator rights.
    """


class PlayerNotJoinedError(Exception):
    """
    Is raised when a player must be joined, but isn't.
    """
