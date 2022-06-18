"""CLI entrypoint"""
import uvicorn
from whist.server import app
from whist.server.const import HOST_ADDR, HOST_PORT, ADMIN_NAME, ADMIN_PASSWORD
from whist.server.database.user import UserInDb
from whist.server.services.password import PasswordService
from whist.server.services.user_db_service import UserDatabaseService


def main(host=HOST_ADDR, port=HOST_PORT, admin_name=ADMIN_NAME, admin_pwd=ADMIN_PASSWORD,
         reload=False):
    """Main function."""
    if admin_name is not None and admin_pwd is not None:
        user_service = UserDatabaseService()
        password_service = PasswordService()
        admin = UserInDb(username=admin_name, hashed_password=password_service.hash(admin_pwd))
        user_service.add(admin)
    uvicorn.run(app, host=host, port=port, reload=reload is not None and reload)
