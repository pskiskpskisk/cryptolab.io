"""DES-CMAC implementation for Exercise 4.

This implementation follows CMAC subkey generation and final-block processing:
- Generate L = E_K(0^64)
- Generate K1 = dbl(L)
- Generate K2 = dbl(K1)
- If last block is complete, xor with K1; otherwise pad and xor with K2
"""

from pathlib import Path
import importlib.util


def _load_des_cipher_module():
    """Load exercise2/des_cipher.py directly without importing exercise2 package."""
    repo_root = Path(__file__).resolve().parents[1]
    des_path = repo_root / 'exercise2' / 'des_cipher.py'
    spec = importlib.util.spec_from_file_location('exercise2_des_cipher', str(des_path))
    module = importlib.util.module_from_spec(spec)
    if spec is None or spec.loader is None:
        raise ImportError('Unable to load DES implementation from exercise2/des_cipher.py')
    spec.loader.exec_module(module)
    return module


des_cipher = _load_des_cipher_module()

BLOCK_SIZE_BYTES = 8  # DES block size (64 bits)
RB_64 = 0x1B  # CMAC Rb constant for 64-bit block ciphers


def _normalize_des_key_hex(key_input: str) -> str:
    """Normalize user key input into 16-hex-character DES key.

    Accepted formats:
    - 16 hex chars directly, e.g. 133457799BBCDFF1
    - plain text, which will be UTF-8 encoded, padded/truncated to 8 bytes, then hex encoded
    """
    if key_input is None:
        key_input = ""

    key_input = key_input.strip()
    if not key_input:
        raise ValueError("Key is required (16 hex chars or plain text).")

    # Try as hex first
    try:
        kb = bytes.fromhex(key_input)
        if len(kb) == 8:
            return kb.hex().upper()
    except Exception:
        pass

    # Fallback to text
    kb = key_input.encode("utf-8")
    if len(kb) < 8:
        kb = kb.ljust(8, b"\x00")
    else:
        kb = kb[:8]
    return kb.hex().upper()


def _xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _left_shift_64(value: int) -> int:
    return (value << 1) & 0xFFFFFFFFFFFFFFFF


def _cmac_dbl_64(block8: bytes) -> bytes:
    """CMAC doubling over GF(2^64) used for DES-CMAC subkeys."""
    val = int.from_bytes(block8, "big")
    msb_set = (val & 0x8000000000000000) != 0
    doubled = _left_shift_64(val)
    if msb_set:
        doubled ^= RB_64
    return doubled.to_bytes(BLOCK_SIZE_BYTES, "big")


def _cmac_dbl_64_with_trace(block8: bytes):
    """Return doubled block and trace data for explanation output."""
    val = int.from_bytes(block8, "big")
    msb_set = (val & 0x8000000000000000) != 0
    shifted = _left_shift_64(val)
    reduced = shifted ^ RB_64 if msb_set else shifted
    return reduced.to_bytes(BLOCK_SIZE_BYTES, "big"), {
        "in_hex": block8.hex().upper(),
        "msb": 1 if msb_set else 0,
        "shifted_hex": shifted.to_bytes(BLOCK_SIZE_BYTES, "big").hex().upper(),
        "rb_applied": "yes" if msb_set else "no",
        "out_hex": reduced.to_bytes(BLOCK_SIZE_BYTES, "big").hex().upper(),
    }


def _encrypt_block_hex(block_hex: str, key_hex: str) -> str:
    """Encrypt a single 64-bit block (hex) with DES using exercise2 primitives."""
    subkeys, _ = des_cipher.generate_subkeys_with_logs(key_hex)
    block_bin = des_cipher.hex2bin(block_hex)
    cipher_bin, _ = des_cipher.encrypt_block_with_logs(block_bin, subkeys)
    return des_cipher.bin2hex(cipher_bin)


def _derive_subkeys(key_hex: str):
    zero_block_hex = "0000000000000000"
    l_hex = _encrypt_block_hex(zero_block_hex, key_hex)
    l_bytes = bytes.fromhex(l_hex)
    k1, k1_trace = _cmac_dbl_64_with_trace(l_bytes)
    k2, k2_trace = _cmac_dbl_64_with_trace(k1)
    return l_hex, k1.hex().upper(), k2.hex().upper(), k1_trace, k2_trace


def _build_cmac_blocks(message_bytes: bytes):
    """Prepare CMAC blocks and final-block status/key choice."""
    msg_len = len(message_bytes)
    if msg_len != 0 and msg_len % BLOCK_SIZE_BYTES == 0:
        blocks = [message_bytes[i:i + BLOCK_SIZE_BYTES] for i in range(0, msg_len, BLOCK_SIZE_BYTES)]
        return blocks, True

    full_blocks = [
        message_bytes[i:i + BLOCK_SIZE_BYTES]
        for i in range(0, msg_len - (msg_len % BLOCK_SIZE_BYTES), BLOCK_SIZE_BYTES)
    ]
    tail = message_bytes[len(full_blocks) * BLOCK_SIZE_BYTES:]
    padded_last = tail + b"\x80" + b"\x00" * (BLOCK_SIZE_BYTES - len(tail) - 1)
    return full_blocks + [padded_last], False


def generate_cmac_with_steps(message: str, key_input: str) -> dict:
    """Generate DES-CMAC (8 bytes) with clear intermediate steps.

    Returns:
        {
            'mac_hex': '16 hex chars',
            'key_hex': '16 hex chars',
            'message_len': int,
            'mac_length': 8,
            'steps': list[dict]
        }
    """
    if message is None:
        message = ""

    key_hex = _normalize_des_key_hex(key_input)
    message_bytes = message.encode("utf-8")

    l_hex, k1_hex, k2_hex, k1_trace, k2_trace = _derive_subkeys(key_hex)
    blocks, last_block_complete = _build_cmac_blocks(message_bytes)

    selected_subkey_hex = k1_hex if last_block_complete else k2_hex

    if not blocks:
        # Safety fallback (should not happen because _build_cmac_blocks always returns >=1).
        blocks = [b"\x80" + b"\x00" * 7]

    if last_block_complete:
        m_last = _xor_bytes(blocks[-1], bytes.fromhex(k1_hex))
    else:
        m_last = _xor_bytes(blocks[-1], bytes.fromhex(k2_hex))

    x = b"\x00" * BLOCK_SIZE_BYTES
    chain_blocks = blocks[:-1]

    intermediate = []
    for block in chain_blocks:
        y = _xor_bytes(x, block)
        x_hex = _encrypt_block_hex(y.hex().upper(), key_hex)
        x = bytes.fromhex(x_hex)
        intermediate.append((block.hex().upper(), y.hex().upper(), x_hex))

    y_last = _xor_bytes(x, m_last)
    mac_hex = _encrypt_block_hex(y_last.hex().upper(), key_hex)

    steps = []
    steps.append({
        "name": "Input",
        "description": "Message and normalized DES key",
        "data": (
            f"message_text={message}\n"
            f"message_bytes={len(message_bytes)}\n"
            f"message_hex={message_bytes.hex().upper() if message_bytes else '(empty)'}\n"
            f"key_hex={key_hex}"
        )
    })

    raw_blocks = [
        message_bytes[i:i + BLOCK_SIZE_BYTES]
        for i in range(0, len(message_bytes), BLOCK_SIZE_BYTES)
    ]
    raw_lines = []
    if raw_blocks:
        for i, blk in enumerate(raw_blocks, start=1):
            raw_lines.append(f"raw_block_{i}={blk.hex().upper()} ({len(blk)} bytes)")
    else:
        raw_lines.append("raw_block_1=(empty)")

    if not last_block_complete:
        tail = message_bytes[(len(raw_blocks) - 1) * BLOCK_SIZE_BYTES:] if raw_blocks else b""
        padded = blocks[-1]
        raw_lines.append(f"tail_before_padding={tail.hex().upper() if tail else '(empty)'}")
        raw_lines.append(f"padding_rule=append 80 then 00... to 8 bytes")
        raw_lines.append(f"padded_last_block={padded.hex().upper()}")

    steps.append({
        "name": "Block Preparation",
        "description": "Split message into 8-byte blocks and apply CMAC padding when needed",
        "data": "\n".join(raw_lines)
    })

    steps.append({
        "name": "CMAC Subkey Generation",
        "description": "Compute L, then derive K1 and K2 (dbl operation in GF(2^64))",
        "data": (
            f"L=E_K(0^64)={l_hex}\n"
            f"K1=dbl(L): in={k1_trace['in_hex']} msb={k1_trace['msb']} shifted={k1_trace['shifted_hex']} "
            f"Rb_applied={k1_trace['rb_applied']} out={k1_trace['out_hex']}\n"
            f"K2=dbl(K1): in={k2_trace['in_hex']} msb={k2_trace['msb']} shifted={k2_trace['shifted_hex']} "
            f"Rb_applied={k2_trace['rb_applied']} out={k2_trace['out_hex']}"
        )
    })

    steps.append({
        "name": "Last Block Decision",
        "description": "Check if final message block is complete (8 bytes)",
        "data": (
            f"last_block_complete={'yes' if last_block_complete else 'no'}\n"
            f"selected_subkey={'K1' if last_block_complete else 'K2'}={selected_subkey_hex}\n"
            f"M_last_raw={blocks[-1].hex().upper()}\n"
            f"M_last=M_last_raw XOR selected_subkey={m_last.hex().upper()}"
        )
    })

    for i, (blk_hex, y_hex, x_hex) in enumerate(intermediate, start=1):
        x_prev = "0000000000000000" if i == 1 else intermediate[i - 2][2]
        steps.append({
            "name": f"Block {i}",
            "description": "CMAC chaining for non-final block",
            "data": (
                f"X{i-1}={x_prev}\n"
                f"M{i}={blk_hex}\n"
                f"Y{i}=X{i-1} XOR M{i}={y_hex}\n"
                f"X{i}=E_K(Y{i})={x_hex}"
            )
        })

    last_input_hex = y_last.hex().upper()
    m_last_hex = m_last.hex().upper()
    raw_last_hex = blocks[-1].hex().upper()
    steps.append({
        "name": "Final Block",
        "description": "Apply selected subkey to last block and compute tag",
        "data": (
            f"M_last_raw={raw_last_hex}\n"
            f"M_last={m_last_hex}\n"
            f"X_prev={x.hex().upper()}\n"
            f"Y_last=X_prev XOR M_last={last_input_hex}\n"
            f"T=E_K(Y_last)={mac_hex}"
        )
    })

    steps.append({
        "name": "Final MAC",
        "description": "DES-CMAC tag (8 bytes)",
        "data": f"MAC={mac_hex}"
    })

    return {
        "mac_hex": mac_hex,
        "key_hex": key_hex,
        "message_len": len(message.encode("utf-8")),
        "mac_length": 8,
        "k1_hex": k1_hex,
        "k2_hex": k2_hex,
        "last_block_complete": last_block_complete,
        "selected_subkey": "K1" if last_block_complete else "K2",
        "steps": steps,
    }
