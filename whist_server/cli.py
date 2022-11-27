"""CLI entrypoint"""
import argparse

import uvicorn

from whist_server.const import HOST_ADDR, HOST_PORT, ADMIN_NAME, ADMIN_PASSWORD
from whist_server.database.user import UserInDb
from whist_server.services.error import UserExistsError
from whist_server.services.password import PasswordService
from whist_server.services.splunk_service import SplunkService, SplunkEvent
from whist_server.services.user_db_service import UserDatabaseService


def main():
    """
    Main entrypoint
    """
    parser = argparse.ArgumentParser(description='Whist Server')
    parser.add_argument('host_addr', type=str, help='Local address of the Whist Server.')
    parser.add_argument('host_port', type=int, help='Local port of the Whist Server.')
    parser.add_argument('--admin_name', type=str, help="Admin's username")
    parser.add_argument('--admin_pwd', type=str,
                        help="Admin's initial password. Must be changed after deployment.")
    parser.add_argument('--reload', action='store_true',
                        help='Enable debug reloading for the uvicorn server')
    args = parser.parse_args()
    _main(host=args.host_addr, port=args.host_port, admin_name=args.admin_name,
          admin_pwd=args.admin_pwd, reload=args.reload)


def _main(host=HOST_ADDR, port=HOST_PORT, admin_name=ADMIN_NAME, admin_pwd=ADMIN_PASSWORD,
          reload=False):
    if admin_name is not None and admin_pwd is not None:
        user_service = UserDatabaseService()
        password_service = PasswordService()
        admin = UserInDb(username=admin_name, hashed_password=password_service.hash(admin_pwd))
        try:
            user_service.add(admin)
        except UserExistsError:
            pass

        splunk_service = SplunkService()
        if splunk_service.available:
            event = SplunkEvent(f'Host: {host}, Port:{port}', source='Whist-Server',
                                source_type='Server Start')
            splunk_service.write_event(event)

    debug_mode = reload is not None and reload
    uvicorn.run('whist_server:app', host=host, port=port, reload=debug_mode,
                log_level='debug' if debug_mode else 'info')
