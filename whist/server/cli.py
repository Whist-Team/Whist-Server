"""CLI entrypoint"""
import uvicorn

from whist.server import app




def main():
    """Main function."""
    uvicorn.run(app, host=HOST_ADDR, port=HOST_PORT)
