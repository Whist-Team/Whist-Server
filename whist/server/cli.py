"""CLI entrypoint"""
import uvicorn

from whist.server import app

from whist.server.const import HOST_ADDR, HOST_PORT


def main(host=HOST_ADDR, port=HOST_PORT):
    """Main function."""
    uvicorn.run(app, host=host, port=port)
