#!/usr/bin/env python3
import elgamal

COMMON_KEY = "291252186408071182051568160209375916289:245702311742099933709919151784068185776"
TEST = "This is a sentence."

pkc1 = elgamal.Elgamal(COMMON_KEY)
pkc2 = elgamal.Elgamal(COMMON_KEY)

pub_key1 = pkc1.pub_key
pub_key2 = pkc2.pub_key

enc_msg = pkc1.encrypt(TEST, pub_key2)

print(pkc1.decrypt(enc_msg))

