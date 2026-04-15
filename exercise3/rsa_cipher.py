import random

# ================= MATH UTILITIES =================

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

def mod_inverse(e, phi):
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise Exception('No modular inverse')
    return (x % phi + phi) % phi

def modexp(b, exp, mod):
    result = 1
    b = b % mod
    while exp > 0:
        if (exp % 2) == 1:
            result = (result * b) % mod
        exp = exp >> 1
        b = (b * b) % mod
    return result

# ================= FERMAT'S PRIMALITY TEST =================

def fermat_primality_test(n, k=5):
    if n <= 1: return False
    if n <= 3: return True
    for _ in range(k):
        a = random.randint(2, n - 2)
        if modexp(a, n - 1, n) != 1:
            return False
    return True

# ================= RSA KEY GEN (With Steps) =================

def generate_keys_with_steps(p, q):
    steps = []
    
    # 1. Check Primality
    steps.append(f"Input: p={p}, q={q}")
    if not fermat_primality_test(p):
        raise ValueError(f"Number {p} is NOT prime (Fermat test failed).")
    if not fermat_primality_test(q):
        raise ValueError(f"Number {q} is NOT prime (Fermat test failed).")
    steps.append("Primality Check: Both p and q are prime.")
        
    # 2. Calculate n
    n = p * q
    steps.append(f"Calculate n = p * q = {p} * {q} = {n}")
    
    # 3. Calculate Phi
    phi = (p - 1) * (q - 1)
    steps.append(f"Calculate phi(n) = (p-1)*(q-1) = {p-1} * {q-1} = {phi}")
    
    # 4. Select e
    possible_e = [3, 5, 7, 11, 13, 17, 65537]
    e = None
    
    steps.append("Selecting e (must be coprime to phi):")
    for candidate in possible_e:
        if candidate < phi and gcd(candidate, phi) == 1:
            e = candidate
            steps.append(f"  -> Checked {e}: GCD({e}, {phi}) == 1. Selected.")
            break
            
    if e is None:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
        steps.append(f"  -> Fallback selection found e={e}")

    # 5. Calculate d
    steps.append(f"Calculate d = mod_inverse({e}, {phi})")
    try:
        d = mod_inverse(e, phi)
        steps.append(f"  -> Result: d = {d}")
        steps.append(f"  -> Verify: ({e} * {d}) % {phi} = {(e*d)%phi}")
    except:
        raise ValueError("Could not find modular inverse.")
    
    return {
        'public': (e, n),
        'private': (d, n),
        'steps': steps
    }

# ================= ENCRYPT/DECRYPT (With Steps) =================

def encrypt_string(plain_text, public_key):
    e, n = public_key
    cipher = []
    steps = []
    
    steps.append(f"Encrypting with Public Key (e={e}, n={n})")
    steps.append(f"Formula: C = M^{e} mod {n}")
    
    for char in plain_text:
        m = ord(char)
        c = modexp(m, e, n)
        cipher.append(c)
        steps.append(f"Char '{char}' (ASCII {m}): {m}^{e} mod {n} = {c}")
        
    return " ".join(map(str, cipher)), steps

def decrypt_string(cipher_text, private_key):
    d, n = private_key
    steps = []
    steps.append(f"Decrypting with Private Key (d={d}, n={n})")
    steps.append(f"Formula: M = C^{d} mod {n}")
    
    try:
        cipher_list = [int(x) for x in cipher_text.split()]
    except ValueError:
        raise ValueError("Invalid format.")
        
    plain = ''
    for num in cipher_list:
        m = modexp(num, d, n)
        char = chr(m)
        plain += char
        steps.append(f"Cipher {num}: {num}^{d} mod {n} = {m} ('{char}')")
        
    return plain, steps