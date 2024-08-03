# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the client of the DNS query.
# Written in Python v3.

import sys
from socket import *

class Client:
    def __init__(self, serverHost = "localhost", serverPort = 5001):
        self.serverHost = serverHost
        self.serverPort = serverPort

    def query(self, name):
        # Create a socket object, SOCK_STREAM for TCP.
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
        # Handle exception.
        except error as message:
            clientSocket = None

        try:
            clientSocket.connect((self.serverHost, self.serverPort))
        # Handle exception.
        except error as message:
            clientSocket = None
        # If the socket cannot be opened, then quit the program.
        if clientSocket is None:
            print("Error: cannot open socket")
            sys.exit(1)
        # Otherwise, send the input to the server.
        clientSocket.send(name.encode())
        # Receive response from the server. This is Python3 specific code.
        data = clientSocket.recv(1024).decode() 
        clientSocket.close()
        return data

    def run(self):
        while 1:
            print("Type in a domain name to query, or 'q' to quit:")
            while 1:
                # Get input from the user.
                st = input()
                if (st == ""):
                    continue
                else:
                    break
            # If input is "q" or "Q", then quit the program.
            if ((st == "q") or (st == "Q")):
                sys.exit(1)
            
            data = self.query(st)
            # Print out the received response.
            print(f"Received: {data}\n")

# The following code will be executed immediately and will allow your client
# code to run after entering 'python3 DNSClientV3.py' into the terminal.
if (__name__ == '__main__'):
    client = Client()
    client.run()