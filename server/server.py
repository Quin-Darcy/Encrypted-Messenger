#!/usr/bin/env python3
import sys
import socket
import select
import pub_key


HEADER_LENGTH = 10

class Server:
    def __init__(self, hostname, port, keysize):
        self.address = (hostname, port)
        self.common_key = pub_key.PubKey(keysize).key
        self.active_sockets = []
        self.clients = dict()

        self.start()

    def start(self):
        self.create_socket()
        self.exchange_keys()
        self.get_usernames()
        self.broadcast_pub_keys()
        self.start_comms()

    def create_socket(self):
        # Create IPv4/TCP socket which reuses local socket
        # Bind socket to self.address
        # Start socket listening
        # Add socket to active_sockets list
        self.srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv_socket.bind(self.address)
        self.srv_socket.listen()
        self.active_sockets.append(self.srv_socket)
        print(f"Listening for connections on {self.address} ...")

    def accept_connections(self):
        # While number of clients is less than 2
        # * Accept connection from client
        # * Add client socket to active_sockets list
        # * Initialize dictionary entry for new client
        while len(self.clients) < 2:
            while True:
                cli_socket, cli_addr = self.srv_socket.accept()
                print(f"Established connection from {cli_addr}")
                self.active_sockets.append(cli_socket)
                self.clients[cli_socket] = {"ADDR":cli_addr, "PUB_KEY":'',
                        "USERNAME":''}
                break
                

    def send_msg(self, cli_socket, msg):
        # Checks if incoming msg is a string
        # If not it attempts to convert it to a string
        # Sends encoded message with header to given socket
        if not isinstance(msg, str):
            try:
                msg = str(msg)
            except:
                print(f"Error in converting {msg} to str type")

        msg = msg.encode("utf-8")
        header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
        cli_socket.send(header+msg)

    def recv_msg(self, cli_socket):
        # Receive message from client
        while True:
            try:
                # Receive the first HEADER_LENGTH bytes of the message
                header = cli_socket.recv(HEADER_LENGTH)

                # If client gracefully closes, there will be no header
                if not len(header):
                    return False

                # All messages come in with header containing length of 
                # message to come. Here we strip away spaces and extract 
                # message length.
                msg_len = int(header.decode("utf-8").strip())

                # Receive the remaining msg_len bytes of the message
                msg = cli_socket.recv(msg_len).decode("utf-8")

                return msg

            except Exception as e:
                # Received empty message or an abrupt disconnection occurred
                return False

            except KeyboardInterrupt:
                print("\nGoodbye.")
                for cli_socket in self.active_sockets:
                    if cli_socket != self.srv_socket:
                        cli_socket.close()

                self.srv_socket.close()
                sys.exit()

    def exchange_keys(self):
        # Connect to clients and populate active_sockets and clients lists
        self.accept_connections()

        # Loop through each client and send it the server's common key
        for cli_socket in self.active_sockets:

            # Don't send common key to server
            if cli_socket != self.srv_socket:
                while True:
                    # Send common_key
                    self.send_msg(cli_socket, self.common_key)

                    # Client sends back what it received
                    msg = self.recv_msg(cli_socket)

                    # If what it received matches, then it successfully
                    # received common_key
                    if msg == self.common_key:
                        # Tell client to stop receiving 
                        self.send_msg(cli_socket, "STOP")
                        # Receive client's public key
                        cli_key = self.recv_msg(cli_socket)
                        # Add client's public key to its info in clients list
                        self.clients[cli_socket]["PUB_KEY"] = cli_key
                        break

    def get_usernames(self):
        # Loop through clients and receive each username 
        # Add username to entry in clients list
        for cli_socket in self.active_sockets:
            if cli_socket != self.srv_socket:
                while True:
                    uname = self.recv_msg(cli_socket)
                    if len(uname) > 0:
                        self.send_msg(cli_socket, "STOP")
                        self.clients[cli_socket]["USERNAME"] = uname
                        break

    def broadcast_pub_keys(self):
        for cli_socket1 in self.active_sockets:
            if cli_socket1 != self.srv_socket:
                for cli_socket2 in self.active_sockets:
                    if cli_socket2 != self.srv_socket:
                        if cli_socket2 != cli_socket1: 
                            key = self.clients[cli_socket1]["PUB_KEY"]
                            self.send_msg(cli_socket2, key)

    def start_comms(self):
        while True:
            read_socs, _, err_socs = select.select(self.active_sockets, [], [])

            for soc in read_socs:
                msg = self.recv_msg(soc)
                uname = self.clients[soc]["USERNAME"]
                print(f"{uname} > {msg}\n")
                for cli_socket in self.clients:
                    if cli_socket != soc:
                        self.send_msg(cli_socket, msg)
