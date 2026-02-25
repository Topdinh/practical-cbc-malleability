from __future__ import annotations

import os


def rand_bytes(n: int) -> bytes:
    return os.urandom(n)


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    if block_size <= 0 or block_size >= 256:
        raise ValueError("block_size must be in 1..255")

    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len]) * pad_len


def pkcs7_unpad(padded: bytes, block_size: int = 16) -> bytes:
    if not padded or len(padded) % block_size != 0:
        raise ValueError("Invalid padded length")

    pad_len = padded[-1]

    if pad_len == 0 or pad_len > block_size:
        raise ValueError("Invalid PKCS7 padding")

    if padded[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Invalid PKCS7 padding")

    return padded[:-pad_len]