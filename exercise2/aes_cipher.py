# exercise2/aes_cipher.py

# ================= PART 1: CONSTANTS =================
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]
INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]
RCON = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x00, 0x00, 0x00, 0x00, 0x00]
IV_CBC = [0] * 16

# ================= PART 2: HELPERS =================
def hex2bytes(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
def bytes2hex(byte_arr):
    return ''.join(f'{b:02X}' for b in byte_arr)
def str2bytes(text):
    return [ord(c) for c in text]
def bytes2str(byte_arr):
    res = ""
    for b in byte_arr:
        if b == 0: break
        res += chr(b)
    return res

def gmul(a, b):
    p = 0
    for _ in range(8):
        if (b & 1): p ^= a
        hi_bit_set = (a & 0x80)
        a = (a << 1) & 0xFF
        if hi_bit_set: a ^= 0x1B
        b >>= 1
    return p

def to_matrix(state_1d):
    display_list = []
    for r in range(4):
        for c in range(4):
            display_list.append(f"{state_1d[r + c*4]:02x}")
    return display_list

# ================= PART 3: KEY & TRANSFORMS =================
def key_expansion_with_logs(key_bytes):
    w = list(key_bytes)
    logs = []
    
    # Init Round Key 0
    logs.append({'round': 0, 'key': bytes2hex(w[0:16])})
    
    current_details = None # To store details for the start of the round
    
    for i in range(4, 44):
        temp = w[(i-1)*4 : i*4]
        
        if i % 4 == 0:
            # Complex step: Rot -> Sub -> Rcon
            before = list(temp)
            temp = temp[1:] + temp[:1] # RotWord
            rot_val = list(temp)
            temp = [S_BOX[b] for b in temp] # SubWord
            sub_val = list(temp)
            rcon_val = RCON[i // 4]
            temp[0] ^= rcon_val
            rcon_xor_val = list(temp)
            
            # Save details
            current_details = {
                'word_idx': i,
                'before': bytes2hex(before),
                'rot': bytes2hex(rot_val),
                'sub': bytes2hex(sub_val),
                'rcon': f"{rcon_val:02X}000000",
                'after_xor': bytes2hex(rcon_xor_val)
            }
            
        w_prev = w[(i-4)*4 : (i-3)*4]
        w_new = [x ^ y for x, y in zip(w_prev, temp)]
        w.extend(w_new)
        
        # Log when a round key is complete (every 4 words: 7, 11, 15...)
        if i % 4 == 3:
            round_idx = i // 4
            start_idx = round_idx * 16
            end_idx = start_idx + 16
            key_segment = w[start_idx : end_idx]
            
            logs.append({
                'round': round_idx, 
                'key': bytes2hex(key_segment), 
                'details': current_details
            })
            current_details = None # Reset for next round
            
    return w, logs

def sub_bytes(state): return [S_BOX[b] for b in state]
def inv_sub_bytes(state): return [INV_S_BOX[b] for b in state]

def shift_rows(s):
    new_s = [0]*16
    new_s[0], new_s[4], new_s[8], new_s[12] = s[0], s[4], s[8], s[12]
    new_s[1], new_s[5], new_s[9], new_s[13] = s[5], s[9], s[13], s[1]
    new_s[2], new_s[6], new_s[10], new_s[14] = s[10], s[14], s[2], s[6]
    new_s[3], new_s[7], new_s[11], new_s[15] = s[15], s[3], s[7], s[11]
    return new_s

def inv_shift_rows(s):
    new_s = [0]*16
    new_s[0], new_s[4], new_s[8], new_s[12] = s[0], s[4], s[8], s[12]
    new_s[5], new_s[9], new_s[13], new_s[1] = s[1], s[5], s[9], s[13]
    new_s[10], new_s[14], new_s[2], new_s[6] = s[2], s[6], s[10], s[14]
    new_s[15], new_s[3], new_s[7], new_s[11] = s[3], s[7], s[11], s[15]
    return new_s

def mix_columns(s):
    new_s = [0]*16
    for c in range(4):
        idx = c * 4
        b0, b1, b2, b3 = s[idx], s[idx+1], s[idx+2], s[idx+3]
        new_s[idx]   = gmul(b0,2) ^ gmul(b1,3) ^ gmul(b2,1) ^ gmul(b3,1)
        new_s[idx+1] = gmul(b0,1) ^ gmul(b1,2) ^ gmul(b2,3) ^ gmul(b3,1)
        new_s[idx+2] = gmul(b0,1) ^ gmul(b1,1) ^ gmul(b2,2) ^ gmul(b3,3)
        new_s[idx+3] = gmul(b0,3) ^ gmul(b1,1) ^ gmul(b2,1) ^ gmul(b3,2)
    return new_s

def inv_mix_columns(s):
    new_s = [0]*16
    for c in range(4):
        idx = c * 4
        b0, b1, b2, b3 = s[idx], s[idx+1], s[idx+2], s[idx+3]
        new_s[idx]   = gmul(b0, 0x0e) ^ gmul(b1, 0x0b) ^ gmul(b2, 0x0d) ^ gmul(b3, 0x09)
        new_s[idx+1] = gmul(b0, 0x09) ^ gmul(b1, 0x0e) ^ gmul(b2, 0x0b) ^ gmul(b3, 0x0d)
        new_s[idx+2] = gmul(b0, 0x0d) ^ gmul(b1, 0x09) ^ gmul(b2, 0x0e) ^ gmul(b3, 0x0b)
        new_s[idx+3] = gmul(b0, 0x0b) ^ gmul(b1, 0x0d) ^ gmul(b2, 0x09) ^ gmul(b3, 0x0e)
    return new_s

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

# ================= PART 4: CORE LOGIC =================

def encrypt_block_with_logs(block, expanded_key):
    steps = []
    state = block
    steps.append({'type': 'init', 'label': 'Input State', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    
    k0 = expanded_key[0:16]
    state = add_round_key(state, k0)
    steps.append({'type': 'round_0', 'label': 'Round 0', 'key': bytes2hex(k0), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    
    for r in range(1, 10):
        round_data = {'round': r, 'ops': []}
        state = sub_bytes(state)
        round_data['ops'].append({'label': 'SubBytes', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        state = shift_rows(state)
        round_data['ops'].append({'label': 'ShiftRows', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        state = mix_columns(state)
        round_data['ops'].append({'label': 'MixColumns', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        k = expanded_key[r*16 : (r+1)*16]
        state = add_round_key(state, k)
        round_data['ops'].append({'label': 'AddRoundKey', 'key': bytes2hex(k), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        steps.append(round_data)

    round_data = {'round': 10, 'ops': []}
    state = sub_bytes(state)
    round_data['ops'].append({'label': 'SubBytes', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    state = shift_rows(state)
    round_data['ops'].append({'label': 'ShiftRows', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    k = expanded_key[160:176]
    state = add_round_key(state, k)
    round_data['ops'].append({'label': 'AddRoundKey', 'key': bytes2hex(k), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    steps.append(round_data)
    
    return state, steps

def decrypt_block_with_logs(block, expanded_key):
    steps = []
    state = block
    steps.append({'type': 'init', 'label': 'Input Cipher State', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    
    k10 = expanded_key[160:176]
    state = add_round_key(state, k10)
    steps.append({'type': 'round_0', 'label': 'Round 0 (AddKey 10)', 'key': bytes2hex(k10), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    
    for r in range(9, 0, -1):
        round_data = {'round': 10-r, 'ops': []}
        state = inv_shift_rows(state)
        round_data['ops'].append({'label': 'InvShiftRows', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        state = inv_sub_bytes(state)
        round_data['ops'].append({'label': 'InvSubBytes', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        k = expanded_key[r*16 : (r+1)*16]
        state = add_round_key(state, k)
        round_data['ops'].append({'label': f'AddRoundKey {r}', 'key': bytes2hex(k), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        state = inv_mix_columns(state)
        round_data['ops'].append({'label': 'InvMixColumns', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
        steps.append(round_data)
        
    round_data = {'round': 10, 'ops': []}
    state = inv_shift_rows(state)
    round_data['ops'].append({'label': 'InvShiftRows', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    state = inv_sub_bytes(state)
    round_data['ops'].append({'label': 'InvSubBytes', 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    k0 = expanded_key[0:16]
    state = add_round_key(state, k0)
    round_data['ops'].append({'label': 'AddRoundKey 0', 'key': bytes2hex(k0), 'hex': bytes2hex(state), 'matrix': to_matrix(state)})
    steps.append(round_data)
    
    return state, steps

# ================= PART 5: PUBLIC INTERFACE =================
def aes_encrypt(plaintext, key_hex, mode="ECB"):
    if len(key_hex) != 32: raise ValueError("Key must be 32 Hex chars (16 bytes).")
    key_bytes = hex2bytes(key_hex)
    # Get Key Logs
    expanded_key, key_logs = key_expansion_with_logs(key_bytes)
    
    data = str2bytes(plaintext)
    while len(data) % 16 != 0: data.append(0) 
    
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    final_output = []
    prev_cipher = list(IV_CBC)
    all_logs = []
    
    for idx, block in enumerate(blocks):
        curr = block
        if mode == "CBC": curr = [b ^ iv for b, iv in zip(curr, prev_cipher)]
        enc, block_logs = encrypt_block_with_logs(curr, expanded_key)
        final_output.extend(enc)
        prev_cipher = enc
        all_logs.append({'block_id': idx + 1, 'steps': block_logs})
        
    return bytes2hex(final_output), all_logs, key_logs

def aes_decrypt(ciphertext_hex, key_hex, mode="ECB"):
    if len(key_hex) != 32: raise ValueError("Key must be 32 Hex chars.")
    key_bytes = hex2bytes(key_hex)
    # Get Key Logs
    expanded_key, key_logs = key_expansion_with_logs(key_bytes)
    
    cipher_bytes = hex2bytes(ciphertext_hex)
    blocks = [cipher_bytes[i:i+16] for i in range(0, len(cipher_bytes), 16)]
    decrypted_bytes = []
    prev_cipher = list(IV_CBC)
    all_logs = []
    
    for idx, block in enumerate(blocks):
        dec, block_logs = decrypt_block_with_logs(block, expanded_key)
        if mode == "CBC":
            final = [d ^ iv for d, iv in zip(dec, prev_cipher)]
            prev_cipher = block
        else:
            final = dec
        decrypted_bytes.extend(final)
        all_logs.append({'block_id': idx + 1, 'steps': block_logs})
        
    return bytes2str(decrypted_bytes), all_logs, key_logs