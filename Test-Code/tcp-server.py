import socket
import threading

IP = "0.0.0.0"
PORT = 9998

def main():
    # socket object is returned
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    # IP and Port are binded to socket object
    server.bind((IP, PORT))
    # Sets the number of connections that the server will accept into the queue
    server.listen(5)
    print(f"[*] Listening on {IP}:{PORT}")

    while(True):
        # server.accept() is blocking execution of program until connection is made
        # Once a client connects the client object and address are set
        client, address = server.accept()
        print(f"[*] Accepted from {address[0]}:{address[1]}")
        # Client handler is created
        # The threading.Thread method takes a function pointer that will be called with the client object as a parameter
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    # Context manager will close socket automatically
    with client_socket as sock:
        request = sock.recv(1024)
        print(f"[*] Received: {request.decode('UTF-8')}")
        sock.send(b"ACK")

if __name__ == "__main__":
    main()
