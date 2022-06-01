
# Encrypted-Messenger

---

### Summary
A simple multi-client chat program with sockets. Users can decide which public key cryptosystem they use and can view metrics on the encrypted messages. 

---

## How It Works

#### pub_key.py
This is a class which is initialized with a *num_of_bits* variable which specifies the number of bits that the user wants the modulus, $p$, of the common key to be. From here the class calls the *get_large_prime()* method from __utils.py__. This method starts by generating a random number with __get_random_n_bit()__ with as many bits as *num_of_bits*. From here that number goes through 2 primality tests, only moving onto to the second if it passes the first. Test one checks divisibility by the first 110 primes. Test two is the Miller-Rabin primality test. Failing either of these tests causes a new cadidate to be selected by __get_random_n_bit()__ and the tests to start over. Having passed both tests, a *base* is then generated from __set_base()__ and chosen specifically to have a large prime order as an element of $\mathbb{Z}^{(\*)}(p)$. Finally, both the modulus and base are converted to strings and appended together taking the form $p:b$. 
