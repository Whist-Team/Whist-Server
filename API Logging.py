import logging
import sys

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s:%(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

def log_user(route):
    if "/" in route:
        # splitting the route string into a list based on forward slashes
        tokens = route.split("/")
        # AT&T Unix Route
        if tokens[1] == "usr":
            logger.info(tokens[2])
        # Unix Derived Routes
        elif tokens[2] == "users":
            logger.info(tokens[3])
        elif tokens[1] == "u01":
            logger.info(tokens[2])
        elif tokens[1] == "user":
            logger.info(tokens[2])
        elif tokens[1] == "users":
            logger.info(tokens[2])
        # Unix-based Route
        elif tokens[1] == "home":
            logger.info(tokens[2])
        # SunOS Route
        elif tokens[2] == "home":
            logger.info(tokens[3])
        # macOS Route
        elif tokens[1] == "Users":
            logger.info(tokens[2])
    elif "\\" in route:
        # splitting the route string into a list based on back slashes
        tokens = route.split("\\")
        # Microsoft Windows NT Route
        if tokens[2] == "Profiles":
            logger.info(tokens[3])
        # Microsoft Windows 2000, XP and 2003 Route
        elif tokens[1] == "Documents and Settings":
            logger.info(tokens[2])
        # Microsoft Windows Vista, 7, 8, 10 and 11 Route
        elif tokens[1] == "Users":
            logger.info(tokens[2])
    
# call function
user_route = str(input("Enter a route: "))
log_user(user_route)
