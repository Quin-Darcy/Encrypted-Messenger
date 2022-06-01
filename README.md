
# Encrypted-Messenger

---

### Summary
A simple multi-client chat program with sockets. Users can decide which public key cryptosystem they use and can view metrics on the encrypted messages. 

---



## How It Works

### pub_key.py (Server side)
This is a class which is initialized with a *num_of_bits* variable which specifies the number of bits that the user wants the modulus, $p$, of the *common_key* to be. From here the class calls the *get_large_prime()* method from __utils.py__. This method starts by generating a random number with __get_random_n_bit()__ with as many bits as *num_of_bits*. From here that number goes through 2 primality tests, only moving onto to the second if it passes the first. Test one checks divisibility by the first 110 primes. Test two is the Miller-Rabin primality test. Failing either of these tests causes a new cadidate to be selected by __get_random_n_bit()__ and the tests to start over. Having passed both tests, a *base* is then generated from __set_base()__ and chosen specifically to have a large prime order as an element of $(\mathbb{Z}/p\mathbb{Z})^{\times}$. Finally, both the modulus and base are converted to strings and appended together taking the form $p:b$ to make up the *common_key*.

### elgmal.py (Client side)
This is a script run on the client side. It is initialized with the *common_key* mentioned above. The constructor then generates a private key, $a$, which is a random integer between 0 and the modulus, $p$ in the *common_key*. A public key is then defined by evaluating $b^a(\text{mod }p)$, where $p:b$ is the *common_key*. After the private and public keys are set, then the __encrypt()__ and __decrypt()__ methods are used throughout the rest of the program. 

### The __encrypt(msg, key)__ method
This method is passed two arguments: 
* *msg* - The user's string type input;
* *key* - Another client's public key. 

Before encrypting *msg*, it first goes through some processing.  
1. *msg* is passed into the __encode_msg()__ method from *utils.py*.
2. The ASCII value of each character in the *msg* is placed into a list, *msg_bytes*
3. Depending on how many characters (or bytes) were in the message, its difference from the next largest multiple of *BLOCKSIZE* is calculated and *msg_bytes* is then filled with as many null bytes as is equal to that difference. 
4. A new list is filled by splitting *msg_bytes* into byte-sized pieces and each of those pieces is converted into Big-Endian binary bytes. Next, the list is subgrouped into *BLOCKSIZE* pieces. So if *BLOCKSIZE=4*, then each block would be $8\cdot 4=32$ bits. Finally, each block is converted to base-10. So if *BLOCKSIZE=4*, we have broken the message down into 32-bit numerical chunks, and these chunks are what is stored in the *blocks* list. 
 
After the message has been encoded, it is stored in *encoded_msg*. An *ephemeral key*, *k*, is then generated. This key is ephemeral because it is only used to encrypt a single message before a new one is generated for the next message. The ephemeral key is then used to encrypt each block in *encoded_msg*. Recall that each block is an integer, call it $m$, and with this we compute $c_1\equiv b^k(\text{mod }p)$ and $c_2\equiv m B^k(\text{mod }p)$, where $B:=$*key*. So our encrypted message is a list *crypt_msg* containing a $(c_1, c_2)$ pair for each block in *encoded_msg*. 
