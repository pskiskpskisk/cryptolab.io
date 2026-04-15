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
    # Initialize MD5 Variables (Magic Numbers)
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    # Pre-compute K constants and shifts
    K = [int((1 << 32) * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
    shifts = [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]

    # Process chunks returned by your specific logic
    chunks = split_into_blocks(message)

    for block in chunks:
        # EXPLICIT CHECK: Ensure each block output by the function is EXACTLY 512 bits
        block_size_in_bits = len(block) * 8
        if block_size_in_bits != 512:
            raise ValueError(f"Block check failed: Expected 512 bits, got {block_size_in_bits} bits!")

        # Unpack 64-byte block into 16 x 32-bit integers WITHOUT struct
        M = []
        for k in range(16):
            chunk_4bytes = block[k*4 : (k+1)*4]
            M.append(int.from_bytes(chunk_4bytes, byteorder='little'))

        # Initialize hash values for this block
        A, B, C, D = a0, b0, c0, d0

        # Main loop: 64 operations
        for j in range(64):
            if 0 <= j <= 15:
                f_val = F(B, C, D)
                g_idx = j
            elif 16 <= j <= 31:
                f_val = G(B, C, D)
                g_idx = (5 * j + 1) % 16
            elif 32 <= j <= 47:
                f_val = H(B, C, D)
                g_idx = (3 * j + 5) % 16
            elif 48 <= j <= 63:
                f_val = I(B, C, D)
                g_idx = (7 * j) % 16

            # Core MD5 mixing formula
            # f_val calculation includes adding A, K[j], and M[g_idx]
            temp = (f_val + A + K[j] + M[g_idx]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + left_rotate(temp, shifts[j])) & 0xFFFFFFFF

        # Add this block's hash to the cumulative sum
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # --- 4. Final Output ---
    final_hash = bytearray()
    final_hash.extend(a0.to_bytes(4, byteorder='little'))
    final_hash.extend(b0.to_bytes(4, byteorder='little'))
    final_hash.extend(c0.to_bytes(4, byteorder='little'))
    final_hash.extend(d0.to_bytes(4, byteorder='little'))

    return final_hash.hex()