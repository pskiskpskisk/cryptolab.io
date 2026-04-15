import random

def modexp(b, exp, mod):
    """User provided modular exponentiation"""
    result = 1
    b = b % mod

    power = 1
    squares = {}
    squares[1] = b

    temp = exp >> 1
    while temp > 0:
        b = (b * b) % mod
        power *= 2
        squares[power] = b
        temp >>= 1

    temp = exp
    bit_pos = 0
    while temp > 0:
        if temp & 1:
            result = (result * squares[2**bit_pos]) % mod
        bit_pos += 1
        temp >>= 1

    return result

def fermat_primality_test(n, k=10):
    if n < 2:    return False
    if n == 2:   return True
    if n == 3:   return True
    if n % 2 == 0: return False

    carmichael = {561,1105,1729,2465,2821,6601,8911,10585,15841,29341}
    if n in carmichael:
        return False

    for _ in range(k):
        a = random.randint(2, n-2)
        if modexp(a, n-1, n) != 1:
            return False

    return True

def get_prime_factors(n):
    factors = set()
    while n % 2 == 0:
        factors.add(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 2
    if n > 2:
        factors.add(n)
    return factors

def is_primitive_root(g, p):
    """Checks if g is a primitive root modulo p."""
    # 1. Check if p is prime
    if not fermat_primality_test(p):
        return False

    # 2. Check range
    if g < 2 or g >= p:
        return False

    # 3. Check order
    phi = p - 1
    prime_factors = get_prime_factors(phi)

    for factor in prime_factors:
        power = phi // factor
        if modexp(g, power, p) == 1:
            return False # g is not a primitive root

    return True

def generate_public_key(p, g, private_key):
    return modexp(g, private_key, p)

def compute_shared_secret(received_key, private_key, p):
    return modexp(received_key, private_key, p)