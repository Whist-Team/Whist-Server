"""Service for passwords."""
from bcrypt import checkpw, gensalt, hashpw

class PasswordService:
    """
    Handles verification and hashing of passwords.
    """
    _instance = None

    def __new__(cls):
        """Creates a new instance of this service singleton."""
        if cls._instance is None:
            cls._instance = super(PasswordService, cls).__new__(cls)
            cls._salt = gensalt()
        return cls._instance

    @classmethod
    def verify(cls, plain_password, hashed_password):
        """
        Verifies a password by a hash.
        :param plain_password: The password sent in the request in plain text
        :param hashed_password: The saved password hash
        :return: True if verified else False.
        """
        password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        return checkpw(password_bytes, hashed_password_bytes)


    @classmethod
    def hash(cls, password):
        """
        Generates a password hash for plain passphrase.
        :param password: in plain text
        :return: hash of the password
        """
        password_bytes = password.encode('utf-8')
        return hashpw(password_bytes, cls._salt)
