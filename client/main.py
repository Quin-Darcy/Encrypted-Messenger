#!/usr/bin/env python3
import client


PORT = 12345
HOSTNAME = "127.0.0.1"

def main():
    username = input("Username: ")
    client.Client(HOSTNAME, PORT, username)

if __name__ == "__main__":
    main()
