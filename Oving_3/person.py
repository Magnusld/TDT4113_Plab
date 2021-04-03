"""This file contains the different person classes"""
import math
import os
import random
import crypto_utils

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
word_file = os.path.join(THIS_FOLDER, 'english_words.txt')
english_words = open(word_file).read().split()

class Person:
    """This is the person superclass that defines the methodes a person needs"""
    key = None
    crypto_cipher = None

    def __init__(self, crypto_cipher):
        self.crypto_cipher = crypto_cipher

    def set_key(self, key):
        """This sets the key that the person uses"""
        self.key = key

    def get_key(self):
        """This gets the key that the person uses"""
        return self.key

    def operate_cipher(self):
        """This methode apply the cipher to the persons message"""


class Sender(Person):
    """This is the person that sends the message"""
    def __init__(self, crypto_cipher):
        super().__init__(crypto_cipher)

    def operate_cipher(self):
        message = input("Write the message you want to send: ")
        return self.crypto_cipher.encode(message, self.key)


class Receiver(Person):
    """This is the person that receives the message"""
    def __init__(self, crypto_cipher):
        super().__init__(crypto_cipher)

    def operate_cipher(self, message):
        return self.crypto_cipher.decode(message, self.key)

    def generate_random_rsa_primes(self, bits=8):
        """Generate the public and private keys for the RSA encryption/decryption"""
        prime_one = crypto_utils.generate_random_prime(bits)
        prime_two = crypto_utils.generate_random_prime(bits)
        while prime_one == prime_two:
            prime_two = crypto_utils.generate_random_prime(bits)
        n = prime_one*prime_two
        ø = (prime_one-1)*(prime_two-1)
        e = random.randint(3, ø-1)
        while math.gcd(e, ø) != 1:
            e = random.randint(3, ø-1)
        d = crypto_utils.modular_inverse(e, ø)
        self.set_key((n, d))
        return n, e


class Hacker(Person):
    """A person that will try to brute force hack the encoded message"""
    def __init__(self, crypto_cipher):
        super().__init__(crypto_cipher)

    def brute_force_hack(self, message):
        """Brute force checks if it can decode the message"""
        keys = self.crypto_cipher.get_possible_keys()
        for key in keys:
            guess = self.crypto_cipher.decode(message, key)
            words = guess.split(" ")
            words_stripped = []
            for word in words:
                words_stripped.append(word.strip(" ,.!?").lower())
            accepted = True
            for word in words_stripped:
                if word not in english_words:
                    accepted = False
            if accepted:
                return guess
        return None
