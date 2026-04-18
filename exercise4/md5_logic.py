import math

# --- 1. The 4 core MD5 functions using (b, c, d) ---
def F(b, c, d): return (b & c) | ((~b & 0xFFFFFFFF) & d)
def G(b, c, d): return (b & d) | (c & (~d & 0xFFFFFFFF))
def H(b, c, d): return b ^ c ^ d
def I(b, c, d): return c ^ (b | (~d & 0xFFFFFFFF))

# Helper to left-rotate a 32-bit integer
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# --- 2. Custom Block Splitting Logic ---
def split_into_blocks(st: bytes):
    data = bytearray(st)
    blocks = []

    l = len(data)           # Total length in bytes
    orig_len_bits = l * 8   # Total length in bits

    no = l // 64            # Number of full 64-byte (512-bit) blocks

    # 1. Slice out all full 512-bit blocks
    for i in range(no):
        s = i * 64
        e = s + 64
        blocks.append(data[s:e])

    # 2. Handle the leftover padding
    rem = l % 64                  # Remainder in bytes
    leftover = data[no * 64 : l]  # Extract the leftover bytes

    # Check if remainder is < 56 bytes (which is 448 bits) -> ext = 1
    if rem < 56:
        new_b = bytearray(leftover)
        new_b.append(0x80)  # Append "1" bit (0x80 is 10000000)

        while len(new_b) < 56:      # 56 bytes = 448 bits
            new_b.append(0x00)      # Append "0" bits

        # Append 64-bit length (8 bytes) natively without struct
        new_b.extend(orig_len_bits.to_bytes(8, byteorder='little'))
        blocks.append(new_b)

    # Else remainder is >= 56 bytes -> ext = 2 (we need 2 blocks to finish)
    else:
        # First block: finish the current 512-bit block
        new_b1 = bytearray(leftover)
        new_b1.append(0x80) # Append "1" bit
        while len(new_b1) < 64:     # 64 bytes = 512 bits
            new_b1.append(0x00)

        # Second block: 448 bits of zeros, plus the length
        new_b2 = bytearray()
        while len(new_b2) < 56:     # 56 bytes = 448 bits
            new_b2.append(0x00)

        # Append 64-bit length (8 bytes) natively without struct
        new_b2.extend(orig_len_bits.to_bytes(8, byteorder='little'))

        blocks.append(new_b1)
        blocks.append(new_b2)

    return blocks

# --- 3. Main MD5 Implementation ---
def md5_hash(message: bytes) -> str:
    # For backward compatibility call the verbose version and return only the hash
    res = md5_hash_with_steps(message)
    return res['hash']


def md5_hash_with_steps(message: bytes, log_rounds: bool = True) -> dict:
    """Compute MD5 and provide intermediate steps for educational display.

    Returns a dict: {
        'hash': hexstring,
        'steps': [ {name, description, data}, ... ]
    }
    """
    steps = []

    # Initialize MD5 Variables (Magic Numbers)
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    steps.append({'name': 'Init', 'description': 'Initial state (a0,b0,c0,d0)',
                  'data': f"a0={a0:08x} b0={b0:08x} c0={c0:08x} d0={d0:08x}"})

    # Pre-compute K constants and shifts
    K = [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
    shifts = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]

    steps.append({'name': 'Constants', 'description': 'K and shift arrays prepared', 'data': f"K[0]={K[0]:08x} ... K[63]={K[63]:08x}"})

    chunks = split_into_blocks(message)
    steps.append({'name': 'Blocks', 'description': f'Number of 512-bit blocks: {len(chunks)}', 'data': ''})

    # Working copies of state
    a_cur, b_cur, c_cur, d_cur = a0, b0, c0, d0

    for blk_idx, block in enumerate(chunks):
        block_bits = len(block) * 8
        if block_bits != 512:
            raise ValueError(f"Block check failed: Expected 512 bits, got {block_bits} bits!")

        # Unpack block into 16 little-endian 32-bit words
        M = [int.from_bytes(block[k*4:(k+1)*4], byteorder='little') for k in range(16)]
        steps.append({'name': f'Block {blk_idx+1}', 'description': 'Block bytes (hex)', 'data': block.hex().upper()})
        steps.append({'name': f'Block {blk_idx+1} - Words', 'description': 'M[0..15] (32-bit little-endian words)',
                      'data': ' '.join([f"M[{i}]={M[i]:08x}" for i in range(16)])})

        A, B, C, D = a_cur, b_cur, c_cur, d_cur
        steps.append({'name': f'Block {blk_idx+1} - Start State', 'description': 'A,B,C,D at start of block',
                      'data': f"A={A:08x} B={B:08x} C={C:08x} D={D:08x}"})

        for j in range(64):
            if 0 <= j <= 15:
                f_val = F(B, C, D)
                g_idx = j
                f_name = 'F'
            elif 16 <= j <= 31:
                f_val = G(B, C, D)
                g_idx = (5 * j + 1) % 16
                f_name = 'G'
            elif 32 <= j <= 47:
                f_val = H(B, C, D)
                g_idx = (3 * j + 5) % 16
                f_name = 'H'
            else:
                f_val = I(B, C, D)
                g_idx = (7 * j) % 16
                f_name = 'I'

            temp = (f_val + A + K[j] + M[g_idx]) & 0xFFFFFFFF
            A, D, C, B = D, C, B, (B + left_rotate(temp, shifts[j])) & 0xFFFFFFFF

            if log_rounds:
                steps.append({'name': f'Block {blk_idx+1} Round {j+1}',
                              'description': f'Function {f_name}, g={g_idx}, shift={shifts[j]}',
                              'data': f"K={K[j]:08x} M[g]={M[g_idx]:08x} temp={temp:08x} A={A:08x} B={B:08x} C={C:08x} D={D:08x}"})

        a_cur = (a_cur + A) & 0xFFFFFFFF
        b_cur = (b_cur + B) & 0xFFFFFFFF
        c_cur = (c_cur + C) & 0xFFFFFFFF
        d_cur = (d_cur + D) & 0xFFFFFFFF

        steps.append({'name': f'Block {blk_idx+1} - End State', 'description': 'Updated a0,b0,c0,d0 after block',
                      'data': f"a0={a_cur:08x} b0={b_cur:08x} c0={c_cur:08x} d0={d_cur:08x}"})

    final_hash = bytearray()
    final_hash.extend(a_cur.to_bytes(4, byteorder='little'))
    final_hash.extend(b_cur.to_bytes(4, byteorder='little'))
    final_hash.extend(c_cur.to_bytes(4, byteorder='little'))
    final_hash.extend(d_cur.to_bytes(4, byteorder='little'))
    final_hex = final_hash.hex()

    steps.append({'name': 'Final', 'description': 'Final MD5 digest (hex)', 'data': final_hex})

    return {'hash': final_hex, 'steps': steps}