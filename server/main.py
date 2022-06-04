#!/usr/bin/env python3
import server
import sys


def error_msg():
    print("Usage: python3 main.py {target specification} [keysize]")
    print("TARGET SPECIFICATION:")
    print(f"{'Ex: python3 main.py -a 127.0.0.1:12345':>40}")
    print(f"{'-a <IP:PORT>: IP address and port number':>42}")
    print("KEYSIZE:")
    print(f"{'Ex: python3 main.py -a 127.0.0.1:12345 -k 256':>47}")
    print(f"{'-k <num_of_bits>: Size of common key in bits':>46}")

def parse_input(args):
    addr = []
    key = None
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

        else:
            error_msg()
            return False
    else:
        error_msg()
        return False

    if len(args) == 5:
        if args[3] == '-k':
            key = args[4]
            try:
                if key != str(int(key)) or int(key) < 0:
                    error_msg()
                    return False
            except:
                return False
        else:
            return False

        return [addr[0], int(addr[1]), int(key)]
    else:
        return [addr[0], int(addr[1])]

def main(hostname, port, keysize=128):
    server.Server(hostname, port, keysize)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        args = parse_input(sys.argv)
        if args != False:
            if len(args) == 3:
                main(args[0], args[1], args[2])
            else:
                main(args[0], args[1])
    else:
        error_msg()

