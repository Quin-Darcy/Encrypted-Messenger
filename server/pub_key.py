import utils
import random

util = utils.Utils()

class PubKey:
    def __init__(self, num_of_bits):
        self.num_of_bits = num_of_bits
        self.modulus = util.get_large_prime(self.num_of_bits)
        self.base = None
        self.key = None
        
        self.set_base()
        self.set_key()

    def set_base(self):
        order = max(util.prime_factors(self.modulus-1))
        a = random.randint(2, self.modulus)
        self.base = pow(a, (self.modulus-1)//order, self.modulus)

    def set_key(self):
        self.key = str(self.modulus)+":"+str(self.base)
