"""CLI entrypoint"""
import uvicorn
from whist.server import app
from whist.server.const import HOST_ADDR, HOST_PORT
from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService


def main(host=HOST_ADDR, port=HOST_PORT, admin_name=None, admin_pwd=None):
    """Main function."""
    uvicorn.run(app, host=host, port=port)
    if admin_name and admin_pwd:
        user_service = UserDatabaseService()
        password_service = PasswordService()
        admin = UserInDb(username=admin_name, hashed_password=password_service.hash(admin_pwd))
        user_service.add(admin)
