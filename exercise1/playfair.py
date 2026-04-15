def _prepare_key(key):
    key = ''.join([c.upper() for c in key if c.isalpha()])
    key = key.replace('J', 'I')
    seen = []
    for ch in key:
        if ch not in seen:
            seen.append(ch)

    for ch in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if ch not in seen:
            seen.append(ch)

    # 5x5 matrix as list of lists
    matrix = [seen[i*5:(i+1)*5] for i in range(5)]
    return matrix

def _coords(matrix, ch):
    if ch == 'J': ch = 'I'
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    raise ValueError('Character not in matrix')

def _preprocess_text(text):
    txt = ''.join([c.upper() for c in text if c.isalpha()])
    txt = txt.replace('J', 'I')
    digraphs = []
    i = 0
    while i < len(txt):
        a = txt[i]
        b = txt[i+1] if i+1 < len(txt) else 'X'
        if a == b:
            digraphs.append((a, 'X'))
            i += 1
        else:
            digraphs.append((a, b))
            i += 2
    return digraphs

def playfair_encrypt(plaintext, key):
    matrix = _prepare_key(key)
    digraphs = _preprocess_text(plaintext)
    result = []
    logs = {'matrix': matrix, 'steps': []}

    for a, b in digraphs:
        ra, ca = _coords(matrix, a)
        rb, cb = _coords(matrix, b)
        if ra == rb:
            ca2 = (ca + 1) % 5
            cb2 = (cb + 1) % 5
            ca_char = matrix[ra][ca2]
            cb_char = matrix[rb][cb2]
        elif ca == cb:
            ra2 = (ra + 1) % 5
            rb2 = (rb + 1) % 5
            ca_char = matrix[ra2][ca]
            cb_char = matrix[rb2][cb]
        else:
            ca_char = matrix[ra][cb]
            cb_char = matrix[rb][ca]

        result.append(ca_char)
        result.append(cb_char)
        logs['steps'].append({'pair': (a, b), 'out': (ca_char, cb_char)})

    return ''.join(result), logs

def playfair_decrypt(ciphertext, key):
    matrix = _prepare_key(key)
    # assume ciphertext contains only letters
    pairs = [(ciphertext[i], ciphertext[i+1]) for i in range(0, len(ciphertext), 2)]
    result = []
    logs = {'matrix': matrix, 'steps': []}

    for a, b in pairs:
        ra, ca = _coords(matrix, a)
        rb, cb = _coords(matrix, b)
        if ra == rb:
            ca2 = (ca - 1) % 5
            cb2 = (cb - 1) % 5
            ca_char = matrix[ra][ca2]
            cb_char = matrix[rb][cb2]
        elif ca == cb:
            ra2 = (ra - 1) % 5
            rb2 = (rb - 1) % 5
            ca_char = matrix[ra2][ca]
            cb_char = matrix[rb2][cb]
        else:
            ca_char = matrix[ra][cb]
            cb_char = matrix[rb][ca]

        result.append(ca_char)
        result.append(cb_char)
        logs['steps'].append({'pair': (a, b), 'out': (ca_char, cb_char)})

    return ''.join(result), logs
