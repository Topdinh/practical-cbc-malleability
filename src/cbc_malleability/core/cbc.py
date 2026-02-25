from __future__ import annotations

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .utils import pkcs7_pad, pkcs7_unpad, rand_bytes


AES_BLOCK_SIZE = 16


def encrypt_cbc(key: bytes, plaintext: bytes) -> tuple[bytes, bytes]:
    """
    Insecure AES-CBC encryption (no integrity protection).
    Returns (iv, ciphertext).
    """

    if len(key) not in (16, 24, 32):
        raise ValueError("AES key must be 16, 24, or 32 bytes")

    iv = rand_bytes(AES_BLOCK_SIZE)

    padded = pkcs7_pad(plaintext, AES_BLOCK_SIZE)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded) + encryptor.finalize()

    return iv, ciphertext


def decrypt_cbc(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    """
    Insecure AES-CBC decryption.
    Raises ValueError if padding invalid.
    """

    if len(iv) != AES_BLOCK_SIZE:
        raise ValueError("IV must be 16 bytes")

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded = decryptor.update(ciphertext) + decryptor.finalize()

    return pkcs7_unpad(padded, AES_BLOCK_SIZE)