"""This is the file for all the different Cipher classes"""
import math
import os
import crypto_utils
import person

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
english_words = os.path.join(THIS_FOLDER, 'english_words.txt')

class Cipher:
    """This is the cipher superclass, that all the other ciphers inherit"""
    alphabet = [chr(i) for i in range(32, 127)]
    clear_text = ""
    cipher_key = 0

    def encode(self, message, key):
        """This methode encodes the message"""
        self.clear_text = message
        self.cipher_key = key
        return message

    def decode(self, message, key):
        """This methode decodes the message"""
        self.clear_text = message
        self.cipher_key = key
        return message

    def verify(self, message, key):
        """This methode verify if the cipher works,
        by encoding and decoding and checking the clear text"""
        encoded_message = self.encode(message, key)
        decoded_message = self.decode(encoded_message, key)
        if decoded_message == message:
            print("Verified")

    def get_possible_keys(self):
        """This methode will return all possilbe keys for the cipher
        this is implemented to make it easier to implement the hacker class"""


class CaesarCipher(Cipher):
    """This cipher uses the Caesar encryption methode"""
    def encode(self, message, key):
        super().encode(message, key)
        encrypted_message = ""
        for sign in self.clear_text:
            encrypted_message += self.alphabet[(self.alphabet.index(sign) + self.cipher_key) % 95]
        return encrypted_message

    def decode(self, message, key):
        super().decode(message, key)
        decoding_key = (95 - self.cipher_key) % 95
        decrypted_message = ""
        for sign in self.clear_text:
            decrypted_message += self.alphabet[(self.alphabet.index(sign) + decoding_key) % 95]
        return decrypted_message

    def get_possible_keys(self):
        return range(0, len(self.alphabet))


class MultiplicationCaesar(Cipher):
    """This cipher uses the multiplicationcaesar methode for encoding and decoding"""
    def encode(self, message, key):
        super().encode(message, key)
        encrypted_message = ""
        for sign in message:
            encrypted_message += self.alphabet[(self.alphabet.index(sign) * key) % 95]
        return encrypted_message

    def decode(self, message, key):
        super().decode(message, key)
        decoding_key = crypto_utils.modular_inverse(key, 95)
        decrypted_message = ""
        for sign in message:
            decrypted_message += self.alphabet[(self.alphabet.index(sign) * decoding_key) % 95]
        return decrypted_message

    def get_possible_keys(self):
        possible_keys = []
        for integer in range(100):
            if integer % 5 != 0 and integer % 19 != 0:
                possible_keys.append(integer)
        return possible_keys

class Affine(Cipher):
    """This cipher combines the regular caesar and the multiplication caesar ciphers"""
    def encode(self, message, key):
        caesar = CaesarCipher()
        multiplication_caesar = MultiplicationCaesar()
        if len(key) == 2:
            multi_encrypted_message = multiplication_caesar.encode(message, key[0])
            encrypted_message = caesar.encode(multi_encrypted_message, key[1])
            return encrypted_message
        else:
            print("To use the affine cipher you have to enter a tuple of two integers as key")

    def decode(self, message, key):
        caesar = CaesarCipher()
        multiplication_caesar = MultiplicationCaesar()
        if len(key) == 2:
            multi_decrypted_message = caesar.decode(message, key[1])
            decrypted_message = multiplication_caesar.decode(multi_decrypted_message, key[0])
            return decrypted_message
        else:
            print("To use the affine cipher you have to enter a tuple of two integers as key")

    def get_possible_keys(self):
        multiplication_caesar = MultiplicationCaesar()
        key_pairs = []
        for integer_one_multiplication in multiplication_caesar.get_possible_keys():
            for integer_two_add in range(0, len(self.alphabet)):
                key_pairs.append((integer_one_multiplication, integer_two_add))
        return key_pairs


class Unbreakable(Cipher):
    """This cipher uses a codeword as key, so not to give one-to-one symbol mapping"""
    def encode(self, message, key):
        caesar = CaesarCipher()
        multiplier = math.ceil(len(message)/len(key))
        multiplied_key = key*multiplier
        complete_key = multiplied_key[:len(message)]
        complete_key_numbered = []
        for char in complete_key:
            complete_key_numbered.append(ord(char))
        encrypted_message = ""
        for index in range(len(message)):
            encrypted_message += caesar.encode(message[index], complete_key_numbered[index])
        return encrypted_message

    def decode(self, message, key):
        caesar = CaesarCipher()
        multiplier = math.ceil(len(message)/len(key))
        multiplied_key = key*multiplier
        complete_key = multiplied_key[:len(message)]
        complete_key_numbered = []
        for char in complete_key:
            complete_key_numbered.append(ord(char))
        decrypted_message = ""
        for index in range(len(message)):
            decrypted_message += caesar.decode(message[index], complete_key_numbered[index])
        return decrypted_message

    def get_possible_keys(self):
        return open(english_words).read().split()

class RSA(Cipher):
    """This cipher uses RSA encoding and decoding"""
    def encode(self, message, key):
        integer_list = crypto_utils.blocks_from_text(message, 1)
        encrypted_integer_list = []
        for integer in integer_list:
            encrypted_integer_list.append(pow(integer, key[1], key[0]))
        return encrypted_integer_list

    def decode(self, integer_list, key):
        decrypted_integer_list = []
        for integer in integer_list:
            decrypted_integer_list.append(pow(integer, key[1], key[0]))
        decrypted_message = crypto_utils.text_from_blocks(decrypted_integer_list, 8)
        return decrypted_message

    def verify(self, message):
        receiver = person.Receiver(self)
        public_key = receiver.generate_random_rsa_primes()
        encoded_message = self.encode(message, public_key)
        decoded_message = self.decode(encoded_message, receiver.get_key())
        if decoded_message == message:
            print("Verified")
