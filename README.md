## Short description
A multithreaded multi-user interactive chat using the pub-sub model and ZMQ for communication.

Clients can post messages to a channel under a specific topic. Clients can register to specific channels and see the messages published in that channel. 

A single server is responsible for receiving messages from the multiple clients and posting the messages to the channels. 

Posting and publishing are implemented using multiple threads to allow for concurrency (that is, so that one action does not block the other).

## Instructions






