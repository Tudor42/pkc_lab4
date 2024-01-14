import random
from sympy import primitive_root
from math import gcd

from MillerRabin import miller_rabin, modular_exponentiation

# Using ElGamal signature scheme - Verificati


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


def toy_hash(m):
    """
    Implementation of ToyHash:  -gets a string m as parameter
                                -computes h_m a number equal to number of
                                vowels^2 + vowels*consonants + number of words modulo 19
    """
    def count_vowels(s):
        return sum(1 for char in s if char.lower() in 'aeiou')

    def count_consonants(s):
        return sum(1 for char in s if char.isalpha() and char.lower() not in 'aeiou')

    v = count_vowels(m)
    c = count_consonants(m)
    w = len(m.split())

    h_m = (pow(v, 2) + c * v + w) % 19

    return h_m


def text_to_num(message: str):
    """
    message to num
    :param message:
    :return: number generated
    """
    numbers = list(map(lambda x: 0 if x == " " else ord(x) - ord("A") + 1, message))
    res = 0
    base = 27
    for i in range(len(numbers)):
        if numbers[i] >= 27:
            raise Exception("not a space or a letter A-Z")
        res = res + numbers[i] * (base ** i)
    return res


def num_to_text(num: int):
    """
    num to text
    :param num:
    :return:
    """
    base = 27
    res = []
    while num != 0:
        res.append(num % base)
        num = num // base
    return ''.join(list(map(lambda x: " " if x == 0 else chr(x + ord("A") - 1), res)))


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
    num = text_to_num(message) % p
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
