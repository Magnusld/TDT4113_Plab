"""This is the main class that runs/ tests the encrypt and decrypt"""
import cipher
import person

def __main__():
    caesarcipher = cipher.CaesarCipher()
    caesarcipher.verify("Hallo", 2)
    multiplicationcaesar = cipher.MultiplicationCaesar()
    multiplicationcaesar.verify("Hallo", 2)
    affine = cipher.Affine()
    affine.verify("Hallo", (2, 2))
    unbreakable = cipher.Unbreakable()
    unbreakable.verify("Hallo", "Hei")
    rsa = cipher.RSA()
    rsa.verify("Hallo")
    sender = person.Sender(rsa)
    receiver = person.Receiver(rsa)
    #hacker = person.Hacker(unbreakable)
    #sender.set_key("abbot")
    #receiver.set_key("abbot")
    public_key = receiver.generate_random_rsa_primes()
    sender.set_key(public_key)
    encrypted = sender.operate_cipher()
    #print(hacker.brute_force_hack(encrypted))
    print(receiver.operate_cipher(encrypted))


if __name__ == '__main__':
    __main__()
