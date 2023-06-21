import sys
import socket
import threading

# List comprehension used to store a string of all printable ASCII characters in range 0-256 or a period if it is not printable.
# len(repr(chr(i))) is used to get the length of the string representation of every character.
# repr(chr(191)) returns "'¿'", excluding the double quotes, the length is 3.
# repr(chr(30)) returns "'\\x1e'", exluding the double quotes, the length is 7 so in the code '.' is used to replace it.
HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    # If a byte string was passed as src it is returned as a decoded string
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    # Increments through the data in 16 byte steps (default) or the length user chose
    for i in range(0, len(src), length):
        # Grabs 16 byte word (default) and converts it to string
        word = str(src[i:i+length])
        # The HEX_FILTER  string is used as the translation table for the translate method.
        # The result is a printable "word" where characters are represented as is and non-printable's are shown as periods.
        printable = word.translate(HEX_FILTER)
        # List comprehension is used to convert the Unicode code point for every character in word into hexadecimal.
        # ord(c) returns the Unicode code point of the character
        # :02X specifies to format this as two hexadecimal characters and apply 0's as padding if needed.
        hexa = ' '.join([f'{ord(c):02X}' for c in word])
        # Multiplied by 3 to account for the two characters plus a space.
        hexwidth = length*3
        # {i:04x} Byte index represented in hexadecimal
        # {hexa:<{hexwidth}} Hex representation of word
        # {printable} Actual word
        results.append(f'{i:04x}  {hexa:<{hexwidth}}  {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    buffer = b""
    connection.settimeout(10)
    try:
        # Recieve data until there is none left.
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        print('error ', e)
        pass
    # Return byte string
    return buffer


def request_handler(buffer):
    # perform packet modifications
    return buffer


def response_handler(buffer):
    # perform packet modifications
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    # All the code below is similar to the code in the previous projects
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            # remote_buffer = response_handler(remote_buffer)
            # client_socket.send(remote_buffer)
            # print("[==>] Sent to local.")

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("[<==] Received %d bytes from local." % len(local_buffer))
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote." % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[==>] Sent to local.")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions.")
        print(e)
        sys.exit(0)

    print("[*] Listening on %s:%d" % (local_host, local_port))
    server.listen(5)
    while True:
        client_socket, addr = server.accept()
        # Print out the local connection information
        print("> Received incoming connection from %s:%d" % (addr[0], addr[1]))
        # Start a thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host,
                  remote_port, receive_first))
        proxy_thread.start()


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port,
                remote_host, remote_port, receive_first)


if __name__ == '__main__':
    main()

