#!/usr/bin/env python3
import elgamal
import socket
import sys
import select
import threading


HEADER_LENGTH = 10


class KeyboardThread(threading.Thread):

    def __init__(self, input_cbk = None, exit_cbk = None, name='keyboard-input-thread'):
        self.input_cbk = input_cbk
        self.exit_cbk = exit_cbk
        super(KeyboardThread, self).__init__(name=name)
        self.start()

    def run(self):
        while True:
            try:
                self.input_cbk(input()) #waits to get input + Return
            except EOFError as eof:
                print("Exiting chat. Goodbye!")
                self.exit_cbk()


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
        keyboard_thread = KeyboardThread(self.process_keyboard_input, self.close_session)
        self.begin_comms()

    def create_socket(self):
        self.comms_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comms_socket.connect(self.address)

    def close_session(self):
        print("\nGoodbye.")
        self.comms_socket.close()
        sys.exit()

    def recv_msg(self):
        while True:
            try:
                header = self.comms_socket.recv(HEADER_LENGTH)
                
                if not len(header):
                    print("Connection closed by server")
                    self.close_session()

                msg_len = int(header.decode("utf-8").strip())
                msg = self.comms_socket.recv(msg_len).decode("utf-8")

                return msg

            except Exception as e:
                print("Reading error: {}".format(str(e)))
                self.close_session()

            except KeyboardInterrupt:
                self.close_session()

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
            self.enc_key = msg
            break

    def begin_comms(self):
        while True:
            try:
                socks_list = [self.comms_socket]
                r_socs, w, e = select.select(socks_list, [], [])
                
                for socs in r_socs:
                    if socs == self.comms_socket:
                        uname = self.recv_msg()
                        msg = self.recv_msg()
                        msg = self.pkc.decrypt(msg)
                        print(uname+msg)
            
            except KeyboardInterrupt:
                self.close_session()
        
    def process_keyboard_input(self, msg):
        # print("\r")
        sys.stdout.flush()
        print(f"{self.username} > ", msg)

        enc_msg = self.pkc.encrypt(msg, self.enc_key)

        uname = self.username+" > "
        self.send_msg(uname)
        self.send_msg(enc_msg)
