#!/usr/bin/python

import socket

# Server

# Create a TCP socket.
ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# Flush on every send.
ss.setscockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# We will accept connections from all IPs on port 10101
ss.bind(('0.0.0.0', 10101))
# We will accept all connections with zero backlog.
ss.listen(0)
# This blocks until we accept a client connection, `cs` is the client socket.
# Probably needs a separate thread?
cs, client_addr = ss.accept()
# Not block on read if nothing has been sent by the client, fail with exception.
cs.setblocking(False)
# Send smth. to the client.
cs.send('c')
# Try reading a char from the client, continue if nothing sent.
try:
    cs.recv(1)
except socket.error:
    pass
# Kill the client connection.
cs.shutdown(socket.SHUT_RDWR)
# Kill the server socket.
ss.shutdown(socket.SHUT_RDWR)

# Client
# Create a TCP socket.
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# Flush on every send.
cs.setscockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
# Not block on read if nothing has been sent by the server, fail with exception.
cs.setblocking(False)
# Connect to the server on `localhost:10101`.
cs.connect(('127.0.0.1', 10101))
# Send smth. to the server.
cs.send('c')
# Try reading a char from the server, continue if nothing sent.
try:
    cs.recv(1)
except socket.error:
    pass
# Kill the server connection.
cs.shutdown(socket.SHUT_RDWR)
