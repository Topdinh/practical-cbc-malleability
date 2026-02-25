from __future__ import annotations

from pathlib import Path

from core.cbc import decrypt_cbc

BLOCK = 16

KEY_PATH = Path("data/keys/aes_key.bin")
PACKET_PATH = Path("data/packets/phase2_amount_999.bin")


def main() -> None:
    key = KEY_PATH.read_bytes()
    data = PACKET_PATH.read_bytes()

    iv = data[:BLOCK]
    ct = data[BLOCK:]

    pt = decrypt_cbc(key, iv, ct)

    print("Decrypted blocks (UNPADDED plaintext):")
    for i in range(0, len(pt), BLOCK):
        block = pt[i : i + BLOCK]
        print(f"Block {i//BLOCK:02d} @ offset {i:03d}: {block!r} | {block.decode('utf-8', errors='replace')}")


if __name__ == "__main__":
    main()