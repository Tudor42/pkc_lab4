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
