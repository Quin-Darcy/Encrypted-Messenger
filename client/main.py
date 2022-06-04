#!/usr/bin/env python3
import client
import sys


def error_msg():
    print("Usage: python3 main.py {target specification}")
    print("TARGET SPECIFICATION:")
    print(f"{'Ex: python3 main.py -a 127.0.0.1:12345':>40}")
    print(f"{'-a <IP:PORT>: IP address and port number':>42}")

def parse_input(args):
    if args[1] == '-a':
        addr = args[2].split(':')
        if len(addr) == 2:
            ip = addr[0].split('.')
            port = addr[1]
            
            for n in ip:
                try:
                    if n != str(int(n)) or int(n) < 0 or int(n) > 255:
                        print(f"Failed to resolve '{addr[0]}'")
                        return False
                except:
                    return False

            try:
                if port != str(int(port)) or int(port) < 0:
                    return False
            except:
                return False

            return [addr[0], int(addr[1])]

        else:
            error_msg()
            return False
    else:
        error_msg()
        return False


def main(hostname, port):
    username = input("Username: ")
    client.Client(hostname, port, username)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        args = parse_input(sys.argv)
        if args != False:
            main(args[0], args[1])
    else:
        error_msg()
