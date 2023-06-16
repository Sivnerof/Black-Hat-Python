import socket

HOST = "127.0.0.1"
PORT = 9997

client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

client.sendto(b"random data to be sent", (HOST, PORT))

data, addr = client.recvfrom(4096)

print(data.decode())

client.close()
