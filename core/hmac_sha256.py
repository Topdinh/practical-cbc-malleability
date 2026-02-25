from __future__ import annotations

from cryptography.hazmat.primitives import hashes, hmac


def hmac_sha256(key: bytes, data: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    return h.finalize()


def hmac_verify_sha256(key: bytes, data: bytes, tag: bytes) -> bool:
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data)
    try:
        h.verify(tag)
        return True
    except Exception:
        return False