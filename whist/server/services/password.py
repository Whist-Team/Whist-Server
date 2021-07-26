from passlib.context import CryptContext


class PasswordService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PasswordService, cls).__new__(cls)
            cls._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return cls._instance

    @classmethod
    def verify(cls, plain_password, hashed_password):
        try:
            return cls._password_context.verify(plain_password, hashed_password)
        except:
            return False

    @classmethod
    def hash(cls, password):
        return cls._password_context.hash(password)
