import random


first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 
                     349, 353, 359, 367, 373, 379, 383,
                     389, 397, 401, 409, 419, 421, 431,	
                     433, 439, 443,	449, 457, 461, 463,
                     467, 479, 487, 491, 499, 503, 509, 
                     521, 523, 541, 547, 557, 563, 569,	
                     571, 577, 587, 593, 599, 601]

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def prime_factors(n):
        factors = []
        d = 2
        while n > 1:
            while n % d == 0:
                factors.append(int(d))
                n = n / d
            d = d+1
            if d*d > n:
                if n > 1: factors.append(int(n))
                break
        return factors

    def get_large_prime(self, n):
        while True:
            p = self.get_random_n_bit(n)
            p = self.initial_div_test(p, n)
            if self.rab_mil_test(p):
                return p

    def get_random_n_bit(self, n):
        return(random.randrange(2**(n-1)+1, 2**n-1))

    def initial_div_test(self, p, n):
        while True:
            for q in first_primes_list:
                if p % q == 0 and q**2 <= p:
                    break
                else: return p
            p = self.get_random_n_bit(n)

    def rab_mil_test(self, p):
        two_pow = self.get_two_pow(p)
        rmdr = p//2**two_pow

        iters = 20
        for i in range(iters):
            base = random.randint(2, p-1)
            x = pow(base, rmdr, p)
            if x == 1 or x == -1:
                continue
            else:
                next = self.repeated_squaring(base, rmdr, p, two_pow)
                if next == 0:
                    continue
                else:
                    return False
        return True            

    @staticmethod
    def repeated_squaring(base, rmdr, p, two_pow):
        for i in range(1, two_pow):
            if pow(base, 2**i * rmdr, p) == p-1:
                return 0
        return 1

    @staticmethod
    def get_two_pow(p):
        e = 1
        n = p-1
        while n % 2 == 0:
            n >>= 1
            e += 1
        return e-1
            
        
