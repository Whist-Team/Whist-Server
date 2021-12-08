"""Main entrypoint"""
import argparse

from whist.server.cli import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Whist Server')
    parser.add_argument('host_addr', type=str, help='Local address of the Whist Server.')
    parser.add_argument('host_port', type=int, help='Local port of the Whist Server.')
    args = parser.parse_args()
    main(host=args.host_addr, port=args.host_port)
