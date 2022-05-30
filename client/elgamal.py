#!/usr/bin/env python3
import utils
import random


class Elgamal:
    def __init__(self, common_key):
        self.common_key = [int(x) for x in common_key.split(":")]
        self.prv_key = random.randint(1, self.common_key[0])
        self.pub_key = self.get_pub_key()

    def get_pub_key(self):
        return pow(self.common_key[1], self.prv_key, self.common_key[0])

    def encrypt(self, msg, key) -> list:
        crypt_msg = ''
        encoded_msg = utils.Utils().encode_msg(msg)

        for block in encoded_msg:
            k = random.randint(1, self.common_key[0])
            c1 = pow(self.common_key[1], k, self.common_key[0])
            c2 = block*pow(int(key), k, self.common_key[0])
            crypt_msg += str(c1)+":"+str(c2)+"-"

        crypt_msg = crypt_msg[:-1]

        return crypt_msg

    def decrypt(self, msg):
        ciphers = [[int(x.split(":")[0]), int(x.split(":")[1])] for x in msg.split("-")] 
        blocks = []
        for i in range(len(ciphers)):
            c1 = ciphers[i][0]
            c2 = ciphers[i][1]
            d = pow(c1, self.common_key[0]-1-self.prv_key, self.common_key[0])*c2
            d = utils.Utils().get_bin(d % self.common_key[0])
            blocks.append(d)

        
        return blocks
