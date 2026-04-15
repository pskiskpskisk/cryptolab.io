import math


def _egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = _egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def mod_inverse(a, m):
    g, x, y = _egcd(a, m)
    if g != 1:
        raise ValueError(f'No modular inverse for a={a} mod {m}')
    return x % m


def affine_encrypt(plaintext, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError('Coefficient a must be coprime with 26')

    result = []
    logs = []
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            x = ord(ch.upper()) - 65
            y = (a * x + b) % 26
            c = chr(y + 65)
            cipher_char = c if is_upper else c.lower()
            logs.append({'plain': ch, 'a': a, 'b': b, 'cipher': cipher_char})
            result.append(cipher_char)
        else:
            result.append(ch)

    return ''.join(result), logs


def affine_decrypt(ciphertext, a, b):
    if math.gcd(a, 26) != 1:
        raise ValueError('Coefficient a must be coprime with 26')
    a_inv = mod_inverse(a, 26)
    result = []
    logs = []
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            y = ord(ch.upper()) - 65
            x = (a_inv * (y - b)) % 26
            p = chr(x + 65)
            plain_char = p if is_upper else p.lower()
            logs.append({'cipher': ch, 'a_inv': a_inv, 'plain': plain_char})
            result.append(plain_char)
        else:
            result.append(ch)

    return ''.join(result), logs
