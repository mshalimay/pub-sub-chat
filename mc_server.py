# Obs.: about subscribing to channels (see also pub_client.py)
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

class Server():
    # class constructor
    def __init__(self, ip_address:str, post_port:str, pub_port:str):
        self.ip_address = ip_address
        self.post_port = post_port
        self.pub_port = pub_port
        self.context = zmq.Context()
        self.messages = {}

    def start_post_server(self):
        """ Create and bind to ZMQ socket for POST server (REP type)
        """
        self.post_socket = self.context.socket(zmq.REP)
        self.post_socket.bind(f"tcp://{self.ip_address}:{self.post_port}")

    def start_pub_server(self):
        """ Create and bind to ZMQ socket for PUB server (PUB type)
        """
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind(f"tcp://{self.ip_address}:{self.pub_port}")
        
    def send_message(self, message):
        """Serialize message object and send to client
        Args:
            message (any): a Python object to be sent to client
        """
        self.post_socket.send(pickle.dumps(message))

    def receive_message(self):
        """Deserialize message object and store in self.message for further processing
        """
        self.message = pickle.loads(self.post_socket.recv())

    def add_to_messages(self):
        """ Record messages sent by clients in dictionary indexed by the channel
        """
        channel = self.message["channel"]
        if channel not in self.messages:
            self.messages[channel] = []
        self.messages[channel].append(
            {"username": self.message["username"], "message": self.message["message"], 
             "time": self.message["time"]})

    def pub_message(self):
        """Deserialize message object and Publishto all subscribers"""
        self.pub_socket.send(pickle.dumps(self.message))
        ## Alternative approach: subscribe to a specific channel
        #self.pub_socket.send_string(f"{self.message['channel']}///{self.message['username']}///{self.message['message']}///{self.message['time']})")
        
        

def validate_port(port:str) -> str:
    """ Validates the port number inputed by user, returning an error message if it is invalid
    Valid port number = integer between 1024 and 65535
    """
    if not port.isdigit() or int(port) < 1024 or int(port) > 65535:
        return "Please enter a port number between 1024 and 65535."
    return ""

#-----------------------------------------
# Main 
#-----------------------------------------
if __name__ == "__main__":
    # check if two arguments were provided; if not, print usage message and exit
    if len(sys.argv) != 4:
        print("Usage: python interactive_server.py <ip_address> <post_port> <pub_port>")
        sys.exit(0)

    # # retrieve CMD arguments, removing spaces
    ip_address = sys.argv[1].replace(" ", "")
    post_port = sys.argv[2].replace(" ", "")
    pub_port = sys.argv[3].replace(" ", "")

    # check if port input is valid; if not, print error message and exit
    error_message = validate_port(post_port) + validate_port(pub_port)
    if len(error_message) > 0:
        print(error_message)
        sys.exit(0)

    
    # instantiate client and try to connect to server; if connection fails, print error message and exit
    server = Server(ip_address, post_port, pub_port)
    try:
        server.start_post_server()
        server.start_pub_server()
    except:
        print("Error: Could not initialize the server." +
              "\nPlease make sure you are connecting to appropriate ip address and port.")
        sys.exit(0)

    while True:
        # receive message and persist into server
        server.receive_message()
        server.add_to_messages()
        # send message to client to allow it to send more messages
        server.send_message("message received")
        # publish messages to chat
        server.pub_message()
        
    
    

