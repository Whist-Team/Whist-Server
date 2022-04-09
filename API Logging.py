import logging
import sys
import socket

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(levelname)s:%(message)s")
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.INFO)

#function that will log localhost, and available port
def port_scan(port):
    try:
        s.connect((target_ip, port))
        return available_port == True
    except:
        return available_port == False

#function that will log username
def log_user(route):
    tokens = route.split("/")
    return " " + tokens[2] + " has been created"


# call functions
user_route = str(input("Enter a route: "))
user_name = log_user(user_route)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = "localhost"
target_ip = socket.gethostbyname(target)
available_port = False
port_count = 0

while available_port == False:
    port_scan(port_count)
    if available_port == True:
        break
    else:
        port_count += 1

logger.info(user_name)
logger.info(" " + target_ip + ":" + str(port_count) + " - " + user_route)
