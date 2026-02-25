from __future__ import annotations

from pathlib import Path
from typing import Tuple

from core.cbc import encrypt_cbc, decrypt_cbc
from core.hmac_sha256 import hmac_sha256, hmac_verify_sha256

BLOCK = 16
TAG_LEN = 32  # SHA256 output size


def encrypt_etm(enc_key: bytes, mac_key: bytes, plaintext: bytes) -> bytes:
    """
    Encrypt-then-MAC:
      1) CBC encrypt -> (iv, ciphertext)
      2) tag = HMAC(mac_key, iv || ciphertext)
      3) return iv || ciphertext || tag
    """
    iv, ciphertext = encrypt_cbc(enc_key, plaintext)

    data = iv + ciphertext
    tag = hmac_sha256(mac_key, data)

    return data + tag


def decrypt_etm(enc_key: bytes, mac_key: bytes, packet: bytes) -> bytes:
    """
    1) Split packet into iv || ciphertext || tag
    2) Verify HMAC
    3) If valid -> decrypt CBC
    """
    if len(packet) < BLOCK + TAG_LEN:
        raise ValueError("Packet too short")

    data = packet[:-TAG_LEN]
    tag = packet[-TAG_LEN:]

    if not hmac_verify_sha256(mac_key, data, tag):
        raise ValueError("AUTHENTICATION FAILED")

    iv = data[:BLOCK]
    ciphertext = data[BLOCK:]

    return decrypt_cbc(enc_key, iv, ciphertext)