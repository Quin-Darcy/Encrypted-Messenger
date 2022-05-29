#!/usr/bin/env python3


# Messages will be encrypted in 4 byte (32 bit) blocks
BLOCKSIZE = 4

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def QR(a, b):
        return [a, b, (a-a%b)//b, a%b]

    def eucl_algo(self, a, b):
        decomps = [self.QR(a, b)]
        k = len(decomps)-1
        r = decomps[k][1]
        while r != 0:
            decomps.append(self.QR(decomps[k][1], decomps[k][3]))
            r = decomps[k+1][3]
            k += 1
        print(decomps[len(decomps)-2][3])

    @staticmethod
    def get_bin(n) -> str:
        # Decimal number comes in and returns Big-Endian
        # binary representation
        bnry = ''
        for i in range(8):
            diff = n-pow(2, 7-i)
            if diff < 0:
                bnry += '0'
            else:
                bnry += '1'
                n = diff
        return bnry 

    @staticmethod
    def get_dec(bnry) -> int:
        # Binary number as a string comes in and decimal 
        # representation as an int is returned
        dec = 0
        two_pow = len(bnry)
        for i in range(two_pow):
            dec += int(bnry[i])*pow(2, two_pow-i-1)
        return dec

    @staticmethod
    def encrypt(enc_block, C, k, g, p) -> list:
        # Implements Elgamal encryption scheme on the given 
        # encoded block enc_block. C is client's public value
        # k is client's private key, g is base of public key
        # p is modulus of public key
        c1 = pow(g, k, p)
        c2 = enc_block*pow(C, k, p)
        return [c1, c2]

    def encode_msg(self, msg) -> list:
        # Full message string comes in and it is parsed into 
        # chunks of BLOCKSIZE many bytes. The binary representation
        # of each block is obtained, then the decimal representation
        # of each binary block is obtained. 
        # A list of len(msg)//BLOCKSIZE many encoded blocks is 
        # returned.
        msg_bytes = []
        blocks = []
        for ch in msg:
            msg_bytes.append(ord(ch))

        k = 0
        rmdr = len(msg_bytes) % BLOCKSIZE
        if rmdr != 0:
            k = BLOCKSIZE*(1+(len(msg_bytes)-1)//BLOCKSIZE)-len(msg_bytes)
            for i in range(k):
                msg_bytes.append(0)

        for i in range(len(msg_bytes)//BLOCKSIZE):
            block = ''
            for j in range(BLOCKSIZE):
                block += self.get_bin(msg_bytes[i*BLOCKSIZE+j])
            blocks.append(self.get_dec(block))

        return blocks
