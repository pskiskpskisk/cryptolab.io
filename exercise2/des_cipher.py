# exercise2/des_cipher.py

IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8, 57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
E_TABLE = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
P_TABLE = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10, 2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
S_BOXES = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7], [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8], [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0], [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10], [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5], [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15], [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8], [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1], [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7], [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15], [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9], [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4], [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9], [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6], [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14], [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11], [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8], [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6], [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1], [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6], [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2], [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7], [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2], [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8], [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]
IV_CBC = "0000000000000000"

def hex2bin(hex_str):
    mp = {'0':"0000", '1':"0001", '2':"0010", '3':"0011", '4':"0100", '5':"0101", '6':"0110", '7':"0111", '8':"1000", '9':"1001", 'A':"1010", 'B':"1011", 'C':"1100", 'D':"1101", 'E':"1110", 'F':"1111"}
    return ''.join(mp.get(c, "0000") for c in hex_str.upper())

def bin2hex(bin_str):
    mp = {"0000":'0', "0001":'1', "0010":'2', "0011":'3', "0100":'4', "0101":'5', "0110":'6', "0111":'7', "1000":'8', "1001":'9', "1010":'A', "1011":'B', "1100":'C', "1101":'D', "1110":'E', "1111":'F'}
    if len(bin_str) % 4 != 0: bin_str = bin_str.zfill(len(bin_str) + (4 - len(bin_str) % 4))
    return ''.join(mp.get(bin_str[i:i+4], '?') for i in range(0, len(bin_str), 4))

def str2bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin2str(bin_str):
    chars = []
    for i in range(0, len(bin_str), 8):
        byte = bin_str[i:i+8]
        if len(byte) < 8: break 
        val = int(byte, 2)
        if val == 0: break 
        chars.append(chr(val))
    return "".join(chars)

def permute(bits, table):
    if len(bits) < max(table): bits = bits.ljust(max(table), '0')
    return ''.join(bits[x - 1] for x in table)

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def shift_left(bits, n):
    return bits[n:] + bits[:n]

# ================= PART 3: KEY GEN (UPDATED FOR LOGS) =================
def generate_subkeys_with_logs(key_hex):
    key_bin = hex2bin(key_hex)
    
    # PC-1 Permutation
    key_permuted = permute(key_bin, PC1)
    
    C = key_permuted[:28]
    D = key_permuted[28:]
    
    subkeys = []
    logs = []
    
    # Log PC-1 result
    logs.append({
        'type': 'PC1',
        'pc1_out': key_permuted,
        'C0': C,
        'D0': D
    })
    
    for i in range(16):
        shift = SHIFT_SCHEDULE[i]
        C = shift_left(C, shift)
        D = shift_left(D, shift)
        
        # Combine C and D
        CD = C + D
        
        # PC-2 Permutation
        subkey = permute(CD, PC2)
        subkeys.append(subkey)
        
        logs.append({
            'type': 'Round',
            'round': i+1,
            'shift': shift,
            'C': C,
            'D': D,
            'pc2_out': bin2hex(subkey) # Subkey IS the result of PC2
        })
        
    return subkeys, logs

def feistel_function(R, subkey):
    expanded_R = permute(R, E_TABLE)
    xored = xor(expanded_R, subkey)
    sbox_output = ""
    for i in range(8):
        chunk = xored[i*6 : (i+1)*6]
        row = int(chunk[0] + chunk[5], 2)
        col = int(chunk[1:5], 2)
        val = S_BOXES[i][row][col]
        sbox_output += format(val, '04b')
    return permute(sbox_output, P_TABLE)

# --- CORE WITH LOGS (CLEANED UP S-BOX DETAILS) ---
def encrypt_block_with_logs(block_bin, subkeys):
    logs = []
    block = permute(block_bin, IP)
    L, R = block[:32], block[32:]
    logs.append({'type': 'init', 'L': bin2hex(L), 'R': bin2hex(R)})
    
    for i in range(16):
        prev_L, prev_R = L, R
        expanded_R = permute(R, E_TABLE)
        k = subkeys[i]
        xored = xor(expanded_R, k)
        
        # S-Box logic without detailed logging per box
        sbox_out_bin = ""
        for b in range(8):
            chunk = xored[b*6 : (b+1)*6]
            row = int(chunk[0] + chunk[5], 2)
            col = int(chunk[1:5], 2)
            val = S_BOXES[b][row][col]
            sbox_out_bin += format(val, '04b')
            
        p_out = permute(sbox_out_bin, P_TABLE)
        new_R = xor(L, p_out)
        new_L = prev_R
        L, R = new_L, new_R
        
        logs.append({
            'type': 'round',
            'round': i+1,
            'L': bin2hex(L),
            'R': bin2hex(R),
            'key': bin2hex(k),
            'expansion': bin2hex(expanded_R),
            'xor_k': bin2hex(xored),
            'sbox_out': bin2hex(sbox_out_bin),
            'p_out': bin2hex(p_out)
        })
        
    final_block = permute(R + L, IP_INV)
    return final_block, logs

def decrypt_block(block_bin, subkeys):
    block = permute(block_bin, IP)
    L, R = block[:32], block[32:]
    rev_keys = subkeys[::-1]
    for i in range(16):
        L, R = R, xor(L, feistel_function(R, rev_keys[i]))
    return permute(R + L, IP_INV)

# ================= PART 4: PUBLIC =================
def des_encrypt(plaintext, key_hex, mode="ECB"):
    if len(key_hex) != 16: raise ValueError("Key must be 16 Hex characters.")
    
    subkeys, key_logs = generate_subkeys_with_logs(key_hex)
    
    bin_data = str2bin(plaintext)
    remainder = len(bin_data) % 64
    if remainder != 0: bin_data += '0' * (64 - remainder)
    blocks = [bin_data[i:i+64] for i in range(0, len(bin_data), 64)]
    final_hex = ""
    prev_cipher_bin = hex2bin(IV_CBC)
    all_logs = []
    
    for idx, block in enumerate(blocks):
        curr_input = block
        if mode == "CBC": curr_input = xor(curr_input, prev_cipher_bin)
        cipher_bin, block_logs = encrypt_block_with_logs(curr_input, subkeys)
        final_hex += bin2hex(cipher_bin)
        prev_cipher_bin = cipher_bin
        all_logs.append({'block_id': idx + 1, 'steps': block_logs})
        
    return final_hex, all_logs, key_logs

def des_decrypt(ciphertext_hex, key_hex, mode="ECB"):
    if len(key_hex) != 16: raise ValueError("Key must be 16 Hex characters.")
    
    subkeys, key_logs = generate_subkeys_with_logs(key_hex)
    
    cipher_bin = hex2bin(ciphertext_hex)
    if len(cipher_bin) % 64 != 0: raise ValueError("Invalid ciphertext length.")
    blocks = [cipher_bin[i:i+64] for i in range(0, len(cipher_bin), 64)]
    plain_bin_total = ""
    prev_cipher_bin = hex2bin(IV_CBC)
    all_logs = []
    rev_keys = subkeys[::-1]
    
    for idx, block in enumerate(blocks):
        decrypted_raw, block_logs = encrypt_block_with_logs(block, rev_keys)
        if mode == "CBC":
            decrypted_text = xor(decrypted_raw, prev_cipher_bin)
            prev_cipher_bin = block
        else:
            decrypted_text = decrypted_raw
        plain_bin_total += decrypted_text
        all_logs.append({'block_id': idx + 1, 'steps': block_logs})
        
    return bin2str(plain_bin_total), all_logs, key_logs