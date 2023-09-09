# mc_client.py: uses the services of PostClient and PubClient classes to implement an interactive client that can
# - send messages server to a specified channel interactively through the command line
# - listen to the chat and print to the console messages sent by all clients to the server on the specified channel

import sys
import threading
from pub_client import PubClient
from post_client import PostClient

    
if __name__ == "__main__":
    # check for correct number of arguments
    if len(sys.argv) != 6:
        print("Usage: python mc_client.py <ip_address> <post_port> <pub_port> <channel> <username>")
        sys.exit(0)

    ip_address= sys.argv[1]
    post_port = sys.argv[2]
    pub_port = sys.argv[3]
    channel = sys.argv[4]
    username = sys.argv[5]

    # instantiate client and try to connect to server; if connection fails, print error message and exit
    post_client = PostClient(ip_address, post_port, username, channel)
    pub_client = PubClient(ip_address, pub_port, channel)
    try:
        post_client.connect_to_server()
        pub_client.connect_to_server()
    except:
        print("Error: Could not connect to server. Please check the port, IP address and if the server is running")
        sys.exit(0)

    # thread to listen to chat and print messages to the console indefinitely
    listen_thread = threading.Thread(target=pub_client.loop_list_and_print, daemon=True)
    listen_thread.start()

    # loop to send messages to the server and receive responses
    # if client is listening to all channels, cannot send messages
    while True:
        if channel.lower() != "all":
            message = input("")
            post_client.send_message(message)
            # receive responses from server to be able to send more messages
            post_client.receive_message()
    
