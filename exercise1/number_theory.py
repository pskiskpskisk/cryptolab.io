import random


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def gcd_with_steps(a, b):
    """Return gcd and step-by-step state for the Euclidean algorithm."""
    steps = []
    orig_a, orig_b = a, b
    while b:
        q = a // b
        r = a % b
        steps.append({'a': a, 'b': b, 'q': q, 'r': r})
        a, b = b, r
    steps.append({'result_gcd': a, 'input': f'{orig_a}, {orig_b}'})
    return a, steps


def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return (g, x, y)


def extended_gcd_with_steps(a, b):
    """Iterative extended gcd with steps returned for display."""
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    steps.append({'old_r': old_r, 'r': r, 'old_s': old_s, 's': s, 'old_t': old_t, 't': t})
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        steps.append({'q': q, 'old_r': old_r, 'r': r, 'old_s': old_s, 's': s, 'old_t': old_t, 't': t})
    # old_r is gcd, coefficients are old_s, old_t
    return old_r, old_s, old_t, steps


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


def modexp_with_steps(base, exp, mod):
    """Fast modular exponentiation (binary) with intermediate steps."""
    steps = []
    result = 1
    base = base % mod
    steps.append({'stage': 'start', 'base': base, 'exp': exp, 'result': result})
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
            steps.append({'action': 'multiply', 'base': base, 'exp_bit': 1, 'result': result})
        else:
            steps.append({'action': 'skip_multiply', 'base': base, 'exp_bit': 0, 'result': result})
        base = (base * base) % mod
        steps.append({'action': 'square', 'new_base': base})
        exp >>= 1
        steps.append({'action': 'shift', 'exp_remaining': exp})
    steps.append({'stage': 'end', 'result': result})
    return result, steps


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


def is_probable_prime_with_steps(n, k=5):
    """Miller-Rabin with step logging. Returns (is_prime, steps)."""
    steps = []
    if n <= 1:
        steps.append({'reason': 'n <= 1', 'result': False})
        return False, steps
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    for p in small_primes:
        if n == p:
            steps.append({'found_small_prime': p, 'result': True})
            return True, steps
        if n % p == 0:
            steps.append({'divisible_by': p, 'result': False})
            return False, steps

    # write n-1 as d * 2^s
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    steps.append({'decompose': f'n-1 = {d} * 2^{s}'})

    def trial_composite_steps(a):
        local_steps = []
        x = pow(a, d, n)
        local_steps.append({'a': a, 'x': x})
        if x == 1 or x == n - 1:
            local_steps.append({'witness_check': 'passed'})
            return False, local_steps
        for _ in range(s - 1):
            x = (x * x) % n
            local_steps.append({'square': x})
            if x == n - 1:
                local_steps.append({'witness_check': 'passed_after_squares'})
                return False, local_steps
        local_steps.append({'witness_check': 'composite_found'})
        return True, local_steps

    for i in range(k):
        a = random.randrange(2, n - 1)
        composite, local = trial_composite_steps(a)
        steps.append({'round': i + 1, 'a': a, 'local_steps': local})
        if composite:
            steps.append({'result': False})
            return False, steps
    steps.append({'result': True})
    return True, steps
