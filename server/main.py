#!/usr/bin/env python3
import server


PORT = 12345
HOSTNAME = "127.0.0.1"

KEYSIZE = 128

def main():
    server.Server(HOSTNAME, PORT, KEYSIZE)

if __name__ == "__main__":
    main()
