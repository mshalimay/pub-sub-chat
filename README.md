## Short description
A multithreaded multi-user interactive chat using the pub-sub model and ZMQ for communication.

Clients can post messages to a channel under a specific topic. Clients can register to specific channels and see the messages published in that channel. 

A single server is responsible for receiving messages from the multiple clients and posting the messages to the channels. 

Posting and publishing are implemented using multiple threads to allow for concurrency (that is, so that one action does not block the other).

## Instructions
To deploy the server, execute
`python mc_server.py <ip> <post_port> <pub_port>`

- `ip`: the IP of the server managing the chat
- `post_port`: the port to receive messages
- `pub_port`: the port to publish received messages

To deploy the client, execute
`python3 mc_client.py <server-ip> <post_port> <pub_port> <channel-name> <client-name>`

- `server-ip`: the IP of the server holding the desired chat
- `post_port`: the port to send messages to
- `pub_port`: the port to listen to messages
- `channel-name`: the channel to listen for messages or to post to. If `all`, can listen to all channels but cannot post messages.
- `client-name`: the identifier for the client posting messages

## Usage example

1) Open CMD 1 and run:
`python mc_server.py 0.0.0.0 9000 9001`

This will deploy the multichannel server, listening to messages in port 9000 and publishing messages in port 9001


2) Open CMD 2 and run:
`python mc_client.py 0.0.0.0 9000 9001 all moises`

This will launch a client that listen to all channels, but is unable to send messages.


3) Open CMD 3 and run:

 `python mc_client.py 0.0.0.0 9000 9001 sports amanda`

This will launch a client that listen and send messages to the 'sports' channel


4) Open CMD 4 and run:

`python mc_client.py 0.0.0.0 9000 9001 sports chard`

This will launch another client that listen and send messages to the 'sports' channel


5) Open CMD 5 and run:

`python mc_client.py 0.0.0.0 9000 9001 news john`

This will launch a client that listen and send messages to the 'news' channel

To test the functionality:
1) Send a "hi" using CMD 3 and "hello" using CMD 4. You should see both messages in both consoles AND in CMD2 (the "all" channel) 
but not in CMD 5, since this client only listen to 'news' channel

2) Send "world" using CMD 5. You should see "world" in CMD5 and CMD2 (the "all" channel), but not in CMD 3 and 4,
since these clients only listen to 'sports' channel

3) Try sending a message using CMD 2. You should see no message in none of the consoles, since this client signed for all channels and is read-only





