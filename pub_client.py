# Obs.: about subscribing to channels (see also mc_server.py)
# - I purposefully chose to implement the channel by filtering in the dictionary message
#   which channels to print to the console (see print_message() method in pub_client.py)
# - I am aware there is the alternative of subscribing to a specific channel through
#   socket.setsockopt_string(zmq.SUBSCRIBE, channel)
# - I found my approach to be more flexible and error-proof; 
#   nonetheless, I left commented code in case one wants to use the subscribe to channel approach
#   search for : ## Alternative approach. Uncomment the code below it and comment the code above it

import zmq
import pickle
import sys
from mc_server import validate_port

class PubClient():
    # initialize class
    def __init__(self, ip_address:str, port:str, channel:str):
        self.ip_address = ip_address
        self.port = port
        self.context = zmq.Context()
        self.channel = channel
    
    def connect_to_server(self):
        """ Connects to the server and subscribes to ALL channels"""
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://{self.ip_address}:{self.port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

        ## Alternative approach: subscribe to a specific channel
        # self.socket = self.context.socket(zmq.SUB)
        # self.socket.connect(f"tcp://{self.ip_address}:{self.port}")
        
        #if self.channel.lower() == "all":
        #    self.socket.setsockopt_string(zmq.SUBSCRIBE, "") 
        #else:
        #    self.socket.setsockopt_string(zmq.SUBSCRIBE, self.channel)

    def listen_to_chat(self):
        """ Listens to PUB server and deserialize messages
        """
        self.message = pickle.loads(self.socket.recv())

        ## Alternative approach: subscribe to a specific channel
        #self.message = self.socket.recv_string()

    def print_message(self):
        """Prints message received from the PUB server to the console
        if specified channel matches the channel signed by the client"""

        # if channel is 'all', always print messages and annotate the channel
        if self.channel.lower() == "all":
            print(f"{self.message['username']} ({self.message['channel']}): {self.message['message']} ({self.message['time']})")
        # if channel is not 'all', only print messages from the specified channel
        elif self.message['channel'] == self.channel:
            print(f"{self.message['username']}: {self.message['message']} ({self.message['time']})")

        ## Alternative approach: subscribe to a specific channel
        #channel, username, message, time = message.split("///")
        #print(f"{username}: {message} ({time})")
    
              
    def loop_list_and_print(self):
        """ Loop to listen to chat and print messages to console; used for multithreading
        """
        while True:
            self.listen_to_chat()
            self.print_message()
        
#-----------------------------------------
# Main 
#-----------------------------------------
if __name__ == "__main__":
    # check if three arguments were provided; if not, print usage message and exit
    if len(sys.argv) != 3:
         print("Error: Invalid number of arguments.\nUsage: python pub_client.py <ip> <port>\n")
         sys.exit(0)

    # retrieve CMD arguments
    ip_address = sys.argv[1]
    port = sys.argv[2]
    
    # check if port input is valid; if not, print error message and exit
    error_message = validate_port(port)
    if len(error_message) > 0:
        print(error_message)
        sys.exit(1)

    
    # instantiate client and try to connect to server; if connection fails, print error message and exit
    pubClient = PubClient(ip_address, port)
    try:
        pubClient.connect_to_server()
    except:
        print("Error: Could not connect to server." +
              "\nPlease make sure the server is running and that you are connecting to the right ip address and port.")
        sys.exit(0)

    # send message to server and print response
    while True:
        pubClient.listen_to_chat()
        pubClient.print_message()
    
    

