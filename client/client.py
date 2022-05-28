#!/usr/bin/env python3
import random
import elgamal
import socket
import sys


HEADER_LENGTH = 10

class Client:
    def __init__(self, hostname, port, username):
        self.address = (hostname, port)
        self.username = username

        self.start()

    def start(self):
        self.create_socket()
        self.exchange_keys()
        self.send_username()
        self.receive_pub_key()
        self.begin_comms()

    def create_socket(self):
        self.comms_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comms_socket.connect(self.address)

    def recv_msg(self):
        while True:
            try:
                header = self.comms_socket.recv(HEADER_LENGTH)
                if not len(header):
                    continue

                msg_len = int(header.decode("utf-8").strip())
                msg = self.comms_socket.recv(msg_len).decode("utf-8")

                return msg

            except Exception as e:
                print("Reading error: {}".format(str(e)))
                self.comms_socket.close()
                sys.exit()

            except KeyboardInterrupt:
                print("\nGoodbye.")
                self.comms_socket.close()
                sys.exit()

    def send_msg(self, msg):
        if not isinstance(msg, str):
            try:
                msg = str(msg)
            except:
                print(f"Error in converting {msg} to str type")
        msg = msg.encode("utf-8")
        header = f"{len(msg):<{HEADER_LENGTH}}".encode("utf-8")
        self.comms_socket.send(header+msg)

    def exchange_keys(self):
        while True:
            msg = self.recv_msg()
            if msg == "STOP":
                self.common_key = srv_key
                self.pkc = elgamal.Elgamal(self.common_key)
                self.pub_key = self.pkc.pub_key
                self.send_msg(self.pub_key)
                break
            srv_key = msg
            self.send_msg(srv_key)

    def send_username(self):
        while True:
            self.send_msg(self.username)
            msg = self.recv_msg()
            if msg == "STOP":
                break

    def receive_pub_key(self):
        while True:
            msg = self.recv_msg()
            if not msg:
                continue
            self.enc_key = msg
            break

    def begin_comms(self):
        while True:
            msg = input(f"{self.username} > ")
            msg = self.pkc.encrypt(msg, self.enc_key)
            enc_msg = ''
            for cipher in msg:
                enc_msg += str(cipher[0])+str(cipher[1])

            self.send_msg(enc_msg)

            while True:
                msg = self.recv_msg()
                print(f"{msg}")

