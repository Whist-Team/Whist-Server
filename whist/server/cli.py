"""CLI entrypoint"""
import uvicorn

from whist.server import app


def main():
    """Main function."""
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
