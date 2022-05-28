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
        crypt_msg = []
        encoded_msg = utils.Utils().encode_msg(msg)

        for block in encoded_msg:
            k = random.randint(1, self.common_key[0])
            c1 = pow(self.common_key[1], k, self.common_key[0])
            c2 = block*pow(int(key), k, self.common_key[0])
            crypt_msg.append([c1, c2])

        return crypt_msg


