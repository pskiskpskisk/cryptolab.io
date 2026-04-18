# CMAC Implementation - Exercise 4 Enhancement

## Overview
This document describes the CMAC (Cipher-based Message Authentication Code) implementation added to Exercise 4 of the Cryptography Lab project.

## What is CMAC?

CMAC is a message authentication code (MAC) algorithm based on block ciphers, specifically AES. It provides:
- **Message Authentication**: Verifies that the message hasn't been tampered with
- **Integrity Protection**: Detects any changes to the message
- **Non-repudiation**: Proves the message came from the holder of the shared key

Unlike hashing (MD5), CMAC uses a secret key, making it suitable for authentication in secure communication channels.

## Files Added/Modified

### 1. **cmac_logic.py** (NEW)
Complete CMAC implementation with detailed intermediate steps.

**Key Components:**

#### CMACComputation Class
- `__init__(key)`: Initialize with AES key (16/24/32 bytes)
- `_generate_subkeys()`: Generate K1 and K2 from AES encryption of zero block
- `compute_cmac(message, mac_length)`: Main computation with all steps logged
- Helper methods for XOR, left shift, and step logging

**Algorithm Steps Shown:**

**Step 1: Subkey Generation**
- Encrypt zero block with AES to get L
- Check MSB (Most Significant Bit) of L
- If MSB=1: K1 = LS(L) ⊕ Rb, where Rb = 0x87 for AES
- If MSB=0: K1 = LS(L) (left shift)
- Similarly generate K2 from K1

**Step 2: Message Analysis**
- Calculate message length in bits
- Determine if last block is complete (message bits are multiple of 128)
- Calculate number of blocks needed

**Step 3: Message Processing**
- For complete last block: XOR with K1
- For incomplete last block: Pad with 0x80 + zeros, then XOR with K2
- Show intermediate block values

**Step 4: CBC-MAC Computation**
- Chain AES encryptions (CBC mode)
- For each block: X = AES(X ⊕ Block)
- Show encrypted values after each block

**Step 5: MAC Truncation**
- Truncate final encrypted block to desired MAC length (1-16 bytes)

**Functions:**
- `generate_cmac_with_steps()`: Public function to generate CMAC
- `verify_cmac()`: Verify a MAC against message and key

### 2. **routes.py** (MODIFIED)
Added new route `/cmac` that:
- Accepts POST requests with message and optional key
- Handles both hex and text key input
- Generates random key if not provided
- Pads/truncates key to valid AES sizes (16/24/32 bytes)
- Allows configurable MAC length (1-16 bytes)
- Returns MAC and all intermediate computation steps

### 3. **cmac.html** (NEW)
Beautiful web interface showing:
- Input fields for message, AES key, and MAC length
- Algorithm overview explaining CMAC steps
- Generated MAC in hex format
- Key and message statistics
- **Detailed intermediate steps visualization** with:
  - Step number and name
  - Description of what's happening
  - Hexadecimal values at each stage

Styling includes color-coded sections, code formatting, and responsive layout.

### 4. **md5.html** (MODIFIED)
Updated sidebar navigation to include link to CMAC route

### 5. **requirements.txt** (MODIFIED)
Added `pycryptodome>=3.15.0` dependency for AES encryption

## Algorithm Flow Diagram

```
Message Input
    ↓
[Step 1] Generate Subkeys (K1, K2)
    ├─ L = AES-Encrypt(00...00)
    ├─ K1 = LS(L) or LS(L)⊕Rb (based on MSB)
    └─ K2 = LS(K1) or LS(K1)⊕Rb (based on MSB)
    ↓
[Step 2] Analyze Message
    ├─ Calculate total length
    ├─ Check if complete blocks
    └─ Determine padding needs
    ↓
[Step 3] Message Padding & Processing
    ├─ If complete: Block ⊕ K1
    └─ If incomplete: Pad with 0x80+zeros, Block ⊕ K2
    ↓
[Step 4] CBC-MAC Encryption Chain
    ├─ X₀ = 00...00
    ├─ For each block: X ← AES(X ⊕ Block)
    └─ Final X = MAC (full length)
    ↓
[Step 5] Truncate MAC
    └─ MAC = First N bytes of final X
    ↓
Output: MAC (in hex)
```

## Usage Examples

### Example 1: Basic CMAC Generation
```
Message: "Hello, World!"
Key: (auto-generated 128-bit)
MAC Length: 16 bytes

Output: Generated 16-byte MAC with all intermediate steps
```

### Example 2: With Custom Key
```
Message: "Important message"
Key: 000102030405060708090A0B0C0D0E0F (in hex)
MAC Length: 8 bytes

Output: 8-byte MAC (typically used in practice)
```

### Example 3: Key Padding
```
Message: "Test"
Key: "mykey" (text, will be padded to 16 bytes)
MAC Length: 16 bytes

Internally: "mykey" → "mykey\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
```

## Intermediate Steps Explanation

Each computation shows:

1. **Subkey Generation Steps**
   - L value (plaintext encryption)
   - K1 calculation with MSB decision
   - K2 calculation with MSB decision

2. **Message Processing Steps**
   - Input message length
   - Number of blocks calculated
   - Last block handling (complete vs incomplete)
   - XOR with K1 or K2

3. **CBC-MAC Chain Steps**
   - Initial X (all zeros)
   - XOR operation before each encryption
   - AES encryption result
   - Shows how chain builds up

4. **Final MAC Truncation**
   - Full 128-bit result
   - Truncated to specified length

## Key Properties

- **Block Size**: 128 bits (16 bytes) - standard for AES
- **Key Sizes Supported**: 128, 192, 256 bits (16, 24, 32 bytes)
- **Output Length**: Variable 1-16 bytes
- **Security**: Depends on AES strength (currently considered secure)

## Important Notes

1. **Key Management**: Keys should be generated securely and transmitted safely
2. **Random Keys**: Generated using `Crypto.Random` for cryptographic security
3. **MAC Length**: While up to 16 bytes supported, 8-16 bytes recommended for security
4. **Message Format**: UTF-8 encoded string messages
5. **Standard Reference**: RFC 4493 (CMAC with AES)

## Technical Implementation Details

### Subkey Generation Mathematics
```
L = AES-Encrypt(0x00000000000000000000000000000000)

If L[0] & 0x80:  # MSB is set
    K1 = LeftShift(L) ⊕ Rb
Else:
    K1 = LeftShift(L)

Similar logic for K2 from K1
where Rb = 0x00000000000000000000000000000087 for AES
```

### CBC-MAC Computation
```
X ← 0
For i = 1 to n:
    X ← AES-Encrypt(X ⊕ M[i])
Return X
```

### Padding Logic
```
If message_length % 16 == 0:
    Last_block = Last_block ⊕ K1
Else:
    Last_block = Pad(Last_block)
    Last_block = Last_block ⊕ K2

Padding = 0x80 followed by 0x00 bytes
```

## Integration with Cryptolab

The CMAC implementation integrates seamlessly with the existing cryptolab:
- Exercise 4 now contains both hashing (MD5) and authentication (CMAC)
- Follows the same UI/UX patterns as other exercises
- Uses Flask blueprints for modular design
- Responsive HTML/CSS styling

## Testing

To test the CMAC implementation:

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask app**:
   ```bash
   python app.py
   ```

3. **Navigate to** `/ex4/cmac` in your browser

4. **Try examples**:
   - Empty message with auto key
   - Various MAC lengths
   - Different key inputs (hex and text)
   - Long messages to see multi-block processing

## Security Considerations

1. **Key Length**: 128-bit keys are standard; 256-bit recommended for high security
2. **MAC Truncation**: Full output is 16 bytes; truncated MACs have reduced security
3. **Key Reuse**: Same key with different messages is secure (unlike ECB mode)
4. **IV/Nonce**: Not needed for CMAC (unlike CBC mode encryption)
5. **Uniqueness**: MAC should change for any message change (verified by algorithm)

## Future Enhancements

Possible additions:
- Batch MAC verification
- Compare two MACs
- Key generation utilities
- Performance statistics
- Implementation in other cipher modes
- Integration with RSA for digital signatures

---

**Author**: Enhanced for Cryptolab Exercise 4  
**Date**: 2024  
**Standard**: RFC 4493 (CMAC: The AES-CMAC Algorithm)
