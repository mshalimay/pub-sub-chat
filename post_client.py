import zmq
import pickle
import sys
from datetime import datetime
from dateutil import tz
from mc_server import validate_port

class PostClient():
    # initialize class
    def __init__(self, ip_address:str, port:str, username:str, channel:str):
        self.ip_address = ip_address
        self.port = port
        self.username = username
        self.context = zmq.Context()
        self.channel = channel
    
    def connect_to_server(self):
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{self.ip_address}:{self.port}")

    def send_message(self, message:str):
        # send username, message and timestamp to server as a dictionary        
        self.socket.send(pickle.dumps({"username": self.username, "time": datetime.now(tz.tzlocal()).strftime("%H:%M:%S"), "message": message, "channel": self.channel}))

    def receive_message(self):
        message = pickle.loads(self.socket.recv())
        return message


def print_usage() -> None:
    print("Error: Invalid number of arguments.\nUsage: python client.py <ip> <port> <username> <message>\n")

#-----------------------------------------
# Main 
#-----------------------------------------
if __name__ == "__main__":
    # check if three arguments were provided; if not, print usage message and exit
    if len(sys.argv) != 5:
        print_usage()
        sys.exit(1)

    # retrieve CMD arguments
    ip_address = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    message = sys.argv[4]
    # ip_address = "127.0.0.0"
    # port = "8080"
    # username = "arnold"
    # message = "helloa again"

    # check if port input is valid; if not, print error message and exit
    error_message = validate_port(port)
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)

    
    # instantiate client and try to connect to server; if connection fails, print error message and exit
    client = PostClient(ip_address, port, username)
    try:
        client.connect_to_server()
    except:
        print("Error: Could not connect to server." +
              "\nPlease make sure the server is running and that you are connecting to the right ip address and port.")
        sys.exit(0)

    # send message to server and print response
    client.send_message(message)
    print(client.receive_message())
    
   

