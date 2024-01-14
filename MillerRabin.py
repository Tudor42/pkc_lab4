import random


def miller_rabin(n, k):
    """
    The Miller-Rabin test: we will get the number n that we will calculate whether it is (probably) prime or not
    The number k is the number of bases we are going to test the primality with. If the end result is true we will have
    a probability of 1-1/(4^k) of the number being prime. If the
    end result is false we have a guarantee that our number is composite

    Input : n - integer, n >= 2
            k - number of iterations, how many bases we will try the Miller-Rabin test
                with (it will give us the end probability)

    Output : n is prime or not
    """
    if not n % 2:
        return False
    base_list = []
    N = n - 1
    s = 0
    while N % 2 == 0:
        N = N // 2
        s = s + 1
    t = N

    if k > n - 2:
        raise ValueError("'k' value cannot be this large")

    for i in range(k):
        valid = 0
        base = random.randrange(2, n - 1)
        while base in base_list:
            base = random.randrange(2, n - 1)
        # print(base)
        base_list.append(base)
        # print(t)
        for iteration in range(s + 1):
            result = modular_exponentiation(base, t * pow(2, iteration), n)
            if result == 1 and (iteration == 0 or valid == 1):
                valid = 1
            elif result == n - 1:
                valid = 1
            else:
                continue
        if valid == 0:
            return False
    return True


def modular_exponentiation(base, exp, n):
    """
    In: b, m, n - (large) integers
        b - base of the modular exponentiation
        m - the power to which we want to raise, the exponent in the modular exponentiation
        n - the modulus, we want the final result to be modulo n

    Out: a - the result of the modular exponentiation b^m modulo n

    modular exponentiation algorithm - computing b^m modulo n step by step
    """
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            exp = exp - 1
            result = (result * base) % n
        exp = exp // 2
        base = (base * base) % n
    return result
