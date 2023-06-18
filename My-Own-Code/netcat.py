import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    # Strip white space
    cmd = cmd.strip()
    # Returns if cmd is empty
    if not cmd:
        return
    # The command is parsed and split by the shell lexer and passed as an argument to the check_output function
    # The subprocess error stream is redirected to the output stream
    # Result is the bytes returned by the executed command
    output = subprocess.check_output(shlex.split(cmd), stderror=subprocess.STDOUT)
    # Bytes are decoded
    return output.decode()

class NetCat:
    # Netcat instance initiated with arguments, buffer, and socket
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Determines the appropriate function to run based on the netcat mode
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        # If data already in buffer, send it.
        if self.buffer:
            self.socket.send(self.buffer)
        # Infinite loop to send and recieve data, can be exited with keyboard interrupt
        try:
            while True:
                recv_len = 1
                response = ''
                # Take data in 4096 byte chunks, if less than 4096 bytes are sent, data has ended, break.
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                # Print response, start new buffer and send it, starting loop again.
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()


if __name__ == "__main__":
    # Creates instance of the ArgumentParser object
    # description - Sets the description that will be displayed to user when they request help
    # formatter_class - Formats the text within the description and epilog as it is written
    # epilog - The text printed at the end of the help message
    # The textwrap.dedent function is used to remove leading whitespace from every line
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.whatisup # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABCDEFGHI' | ./netcat.py -t 192.168.1.108 -p 135 # echo local text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
        '''))
    # Create arguments with short and long form command options and other options
    parser.add_argument('-c', '--command', action='store_true', help='initialize command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # Listen mode
    if args.listen:
        buffer = ''
    # Not in listen mode
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode('utf-8'))
    nc.run()
