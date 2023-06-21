import socket
import sys

HOST = "www.google.com"
PORT = 80

# The AF_INET parameter specifies the address family as IPv4
# The SOCK_STREAM parameter specifies a TCP socket
# Both are passed into the socket method as named parameters as opposed to positional parameters
# Returns server object
try:
    server_object = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    print("Socket successfuly created.")
except socket.error as err:
    sys.exit(f"Socket creation failed with error: {err}", 1)

# The connect method takes a host and port as a tuple
server_object.connect((HOST, PORT))

# Send data as bytes
server_object.send(b"GET / HTTP/1.1\r\nHOST: google.com\r\n\r\n")

# Get data back from server
server_response = server_object.recv(4096)

# Decode server_response bytes object to UTF-8
print(server_response.decode("UTF-8"))

server_object.close()
