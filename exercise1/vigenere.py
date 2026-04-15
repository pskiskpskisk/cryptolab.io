# Simple Vigenere cipher utilities
def _clean_key(key):
    k = ''.join([c.upper() for c in key if c.isalpha()])
    if not k:
        raise ValueError('Key must contain alphabetic characters.')
    return k

def vigenere_encrypt(plaintext, key):
    key = _clean_key(key)
    result_chars = []
    logs = []
    ki = 0
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            p = ord(ch.upper()) - 65
            shift = ord(key[ki % len(key)]) - 65
            c = (p + shift) % 26
            cipher_char = chr(c + 65)
            cipher_char = cipher_char if is_upper else cipher_char.lower()
            logs.append({'pos': ki, 'plain': ch, 'key_char': key[ki % len(key)], 'cipher': cipher_char})
            result_chars.append(cipher_char)
            ki += 1
        else:
            result_chars.append(ch)

    return ''.join(result_chars), logs

def vigenere_decrypt(ciphertext, key):
    key = _clean_key(key)
    result_chars = []
    logs = []
    ki = 0
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            c = ord(ch.upper()) - 65
            shift = ord(key[ki % len(key)]) - 65
            p = (c - shift) % 26
            plain_char = chr(p + 65)
            plain_char = plain_char if is_upper else plain_char.lower()
            logs.append({'pos': ki, 'cipher': ch, 'key_char': key[ki % len(key)], 'plain': plain_char})
            result_chars.append(plain_char)
            ki += 1
        else:
            result_chars.append(ch)

    return ''.join(result_chars), logs
