import fastapi
from passlib.context import CryptContext


class PasswordService:

    def __init__(self):
        self._password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_password, hashed_password):
        try:
            return self._password_context.verify(plain_password, hashed_password)
        except:
            return False

    def hash(self, password):
        return self._password_context.hash(password)


def singleton(func):
    def inner(*args, **kwargs):
        value = None

        def get_value():
            if value is None:
                value = func(*args, **kwargs)
            return value

        return fastapi.Depends(get_value)

    return inner


"""
class PasswordServiceDep:
    def __call__(self, *args, **kwargs):
        if self.service is None:
            self.service = PasswordService()
        return self.service
"""


@singleton
def password_service():
    return PasswordService()
