# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the server of the DNS query.
# Written in Python v3.

import sys, threading, os, random
from socket import *

import time
import argparse
# The following two modules may be useful to implement the extra credit.
import subprocess
import re

class Server:
    def __init__(self, serverHost = "localhost", serverPort = 5001):
        self.serverHost = serverHost
        self.serverPort = serverPort
        self.DNS_FILE = "dns_mapping.txt"
        self.LOG_FILE = "dns-server-log.csv"
        self.dictionary = {}

        # TODO: Check if the DNS file already exists. Create it if it does 
        # not.
        if os.path.exists(self.DNS_FILE) == False:
            with open(self.DNS_FILE, 'w'):
                # do nothing
                pass

	    # TODO: Open and read the entire DNS file and save the cache 
        # information to a data structure that the server will use as its 
        # local cache during the time it's running.
        with open(self.DNS_FILE, 'r') as file: 
            for entry in file:
                content = entry.strip().split(",")
                hostname = content[0]
                ip = content[1]
                self.dictionary[hostname] = ip

    def run(self):
        # TODO: Create a socket object named serverSocket, SOCK_STREAM for 
        # TCP.
        with socket(AF_INET, SOCK_STREAM) as serverSocket:
            # TODO: Bind the socket to the current address on port 5001.
            serverSocket.bind((self.serverHost, self.serverPort))
            # TODO: Listen on the given socket while the allowed maximum number
            # of connections to be queued is 20.
            serverSocket.listen(20)
            # Create and start the save thread.
            save = threading.Thread(target = self.saveFile, args = [])
            save.start()
            # Create and start the monitor thread.
            monitor = threading.Thread(target = self.monitorQuit, args = [])
            monitor.start()
            
            print("Server is listening...")

            while 1:
                # Blocked until a remote machine connects to the local port.
                connectionSocket, addr = serverSocket.accept()
                server = threading.Thread(target = self.dnsQuery, args = [connectionSocket])
                server.start()
    
    def dnsQuery(self, connectionSocket):	
        response = "Host Not Found"
        resolutionMethod = "API"	
        # TODO: Read the client's query from the connection socket.
        queriedHost = connectionSocket.recv(1024).decode()
	    # TODO: Check the local cache data structure to see if the queried 
        # hostname already has an entry in it. If there is a match, then 
        # directly use the entry in the cache.
        if queriedHost in self.dictionary:
            response = self.dictionary[queriedHost]
            resolutionMethod = "CACHE"
	    # TODO: If there's no match, then query the local machine's DNS 
        # API to get the hostname resolution.
        else:
            try:
                response = connectionSocket.gethostbyname(queriedHost)
            except Exception as e:
                print(f"Host name not found {e}")
                
            # TODO: Save the newly resolved hostname and its corresponding
            # IP address(es) in the local cache data structure.
            self.dictionary[queriedHost] = response 
        
        # NOTE: If you're implementing the extra credit, then you will need 
        # to call ipSelection() at least once in this function to have an IP 
        # address properly selected. If you're not doing the extra credit,
        # then do NOT call ipSelection() at all and you can simply delete 
        # this note.
        
	    # TODO: Print the response to the terminal.
        print("HostName : " + queriedHost + ", IP : " + response)
	    # TODO: Send the response back to the client.
        connectionSocket.send(response.encode())
	    # TODO: Close the connection socket.
        connectionSocket.close()
	    # TODO: Add a new entry for this query to the log file.
        with open(self.LOG_FILE, 'a') as logFile:
            logFile.write(f"{queriedHost},{response},{resolutionMethod}")

        return


    # NOTE: This function should only be implemented if you're intending to
    # complete the extra credit part. It does NOT need to be implemented for
    # the required parts of the project.
    def ipSelection(self, ipList):
        # TODO: Check the number of IP addresses in the passed IP address
        # list. If there is only one IP address in the list, then immediately 
        # return that IP address.

        # TODO: Otherwise, if there are multiple IP addresses in the list, 
        # then return the IP address in the list that has the best performance 
        # (i.e., lowest latency) by using Ping.

        return
        
    
    def saveFile(self):
        while 1:
            # TODO: Check for updates that have been made to the local cache 
            # data structure and save all of the updates to the DNS file to 
            # keep it up-to-date.  
            
            # TODO : make this more effecient by actually chekcing for updates
            try:
                with open(self.DNS_FILE, 'w') as dnsFile:
                    for hostname, ip in self.dictionary.items():
                        dnsFile.write(f"{hostname},{ip}\n")
            except Exception as e:
                print(f"Error writing to DNS file: {e}")

            # This thread goes to sleep for 15 seconds.
            time.sleep(15)
            
    def monitorQuit(self):
        while 1:
            # Get input from the user.
            sentence = input()
            if (sentence == "exit"):
                # TODO: Write all new values from the local cache data 
                # structure to the DNS file before the server process is 
                # killed so that the most current version of the cache is 
                # persistently stored in a file.
                os.kill(os.getpid(), 9)

# The following code will be executed immediately and will allow your server
# code to run after entering 'python3 DNSServerV3.py' into the terminal.
if (__name__ == '__main__'):
    parser = argparse.ArgumentParser(description = 'Get Port.')
    parser.add_argument("-p","--port", type = int, default = 5001,
                    help = "port number")
    args = parser.parse_args()
    print("port = ", args.port)
    server = Server(serverPort = args.port)
    server.run()