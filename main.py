import random
from sympy import primitive_root
from math import gcd
from utils import *
from MillerRabin import miller_rabin, modular_exponentiation


def generate_keys(g, p):
    """
    Generating the public and private keys for Alice, the person who is going to decrypt
    """
    a = random.randrange(2, p - 2)  # private key
    g_a = modular_exponentiation(g, a, p)
    return {'public_key': [p, g, g_a], 'private_key': a}


def generate_g_and_p():
    p = random.getrandbits(128)
    while not miller_rabin(p, 4):
        p = random.getrandbits(128)
    g = primitive_root(p)
    return g, p


def generate_signature(private_key, g, p, message):
    """
    generating the signature based on the public key and on the string m
    """
    s = 0
    r = 0
    while s == 0:
        k = random.randrange(2, p - 2)
        while gcd(k, p - 1) != 1:
            k = random.randrange(1, p - 2)
        r = pow(g, k, p)
        h_m = toy_hash(message)
        s = pow(k, -1, p - 1) * (h_m - private_key * r) % (p - 1)
    signature = [r, s]
    return signature


def verify_signature(public_key, signature, message):
    """
    public_key
    signature - tuple in the form (r, s)
    m - Ciphertext for which

    Does the proper validations corresponding to ElGamal signature scheme requirements

    Note: For simplification purposes I chose ToyHash for the hashing function
    """
    p = public_key[0]

    r = signature[0]
    s = signature[1]

    h_m = toy_hash(message)

    if not (0 < r < p and 0 < s < p - 1):
        return False

    v1 = pow(public_key[2], r, p) * pow(r, s, p) % p
    v2 = pow(public_key[1], h_m, p)

    if v1 != v2:
        return False
    return True


def decrypt(ciphertext, their_public_key, my_private_key):
    """
    decrypt based on ciphertext and the private and public keys
    :param ciphertext:
    :param their_public_key: the public key they generated
    :param my_private_key: the private key i generated
    :return: decrypted message
    """
    p = their_public_key[0]
    alpha = ciphertext[0]
    beta = ciphertext[1]
    m = pow(alpha, -1 * my_private_key, p) * beta % p
    return num_to_text(m)


def encrypt(message, their_public_key, my_private_key):
    """
    encrypts the message with el gamal algorithm
    :param message:
    :param their_public_key: the public key they generated
    :param my_private_key: the private key i generated
    :return: encrypted message
    """
    p = their_public_key[0]
    num = text_to_num(message)
    if num >= p:
        raise Exception("p is too small for this message")
    return [pow(their_public_key[1], my_private_key, p),
            (num * pow(their_public_key[2], my_private_key, p)) % p]


def main():
    g, p = generate_g_and_p()

    # Alice
    alice_keys = generate_keys(g, p)

    # Bob
    bob_keys = generate_keys(g, p)
    bobs_message = "HELLO ALICE"
    bobs_signature = generate_signature(bob_keys['private_key'], g, p, bobs_message)
    bobs_encrypted_message = encrypt(bobs_message, alice_keys['public_key'], bob_keys['private_key'])

    # Alice
    alice_decrypted_message = decrypt(bobs_encrypted_message, bob_keys['public_key'], alice_keys['private_key'])

    if not verify_signature(bob_keys['public_key'], bobs_signature, alice_decrypted_message):
        raise Exception("Bobs signature is invalid")
    print("Bobs signature is valid")
    print("Message: " + alice_decrypted_message)


if __name__ == "__main__":
    main()
