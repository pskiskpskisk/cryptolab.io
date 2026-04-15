import random


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Modular inverse does not exist')
    return x % m


def modexp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result


def is_probable_prime(n, k=5):
    """Miller-Rabin probabilistic primality test.

    n: integer to test
    k: number of witness rounds (more -> more confident)
    """
    if n <= 1:
        return False
    # small primes quick check
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    # write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    def trial_composite(a):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                return False
        return True

    for _ in range(k):
        a = random.randrange(2, n - 1)
        if trial_composite(a):
            return False
    return True
