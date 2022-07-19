"""Service for passwords."""
from passlib.context import CryptContext
from passlib.exc import UnknownHashError


class PasswordService:
    """
    Handles verification and hashing of passwords.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PasswordService, cls).__new__(cls)
            cls._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return cls._instance

    @classmethod
    def verify(cls, plain_password, hashed_password):
        """
        Verifies a password by a hash.
        :param plain_password: The password sent in the request in plain text
        :param hashed_password: The saved password hash
        :return: True if verified else False.
        """
        try:
            return cls._password_context.verify(plain_password, hashed_password)
        except UnknownHashError:
            return False

    @classmethod
    def hash(cls, password):
        """
        Generates a password hash for plain passphrase.
        :param password: in plain text
        :return: hash of the password
        """
        return cls._password_context.hash(password)
