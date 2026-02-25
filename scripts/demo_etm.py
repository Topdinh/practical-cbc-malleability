from __future__ import annotations

import os
from pathlib import Path

from cbc_malleability.core.etm import encrypt_etm, decrypt_etm

ENC_KEY_PATH = Path("data/keys/aes_key.bin")
MAC_KEY_PATH = Path("data/keys/hmac_key.bin")
PACKET_PATH = Path("data/packets/phase3_etm.bin")

BLOCK = 16


def build_message() -> bytes:
    msg = (
        "FROM=ALICE____;"
        "TO=BOB______ ;"
        "AMOUNT=000100;"
        "CURRENCY=USD;"
        "NOTE=HELLO__________;"
    )
    return msg.encode("utf-8")


def ensure_mac_key() -> None:
    if not MAC_KEY_PATH.exists():
        MAC_KEY_PATH.parent.mkdir(parents=True, exist_ok=True)
        MAC_KEY_PATH.write_bytes(os.urandom(32))


def main() -> None:
    ensure_mac_key()

    enc_key = ENC_KEY_PATH.read_bytes()
    mac_key = MAC_KEY_PATH.read_bytes()

    plaintext = build_message()

    print("=== Encrypting with Encrypt-then-MAC ===")
    packet = encrypt_etm(enc_key, mac_key, plaintext)
    PACKET_PATH.parent.mkdir(parents=True, exist_ok=True)
    PACKET_PATH.write_bytes(packet)
    print(f"[+] Saved packet: {PACKET_PATH}")

    print("\n=== Attempting normal decrypt ===")
    pt = decrypt_etm(enc_key, mac_key, packet)
    print("Decryption succeeded.")
    print(pt.decode("utf-8"))


if __name__ == "__main__":
    main()