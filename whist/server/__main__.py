"""Main entrypoint"""
import argparse

from whist.server.cli import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Whist Server')
    parser.add_argument('host_addr', type=str, help='Local address of the Whist Server.')
    parser.add_argument('host_port', type=int, help='Local port of the Whist Server.')
    parser.add_argument('--admin_name', type=str, help="Admin's username")
    parser.add_argument('--admin_pwd', type=str,
                        help="Admin's inital password. Must be changed after deployment.")
    parser.add_argument('--reload', action='store_true',
                        help='Enable debug reloading for the uvicorn server')
    args = parser.parse_args()
    main(host=args.host_addr, port=args.host_port, admin_name=args.admin_name,
         admin_pwd=args.admin_pwd, reload=args.reload)
