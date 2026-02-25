from __future__ import annotations

from pathlib import Path

from core.cbc import encrypt_cbc, decrypt_cbc
from core.utils import rand_bytes

PACKET_PATH = Path("data/packets/phase1_cbc_only.bin")
KEY_PATH = Path("data/keys/aes_key.bin")


def build_fixed_message(amount_6digits: str = "000100") -> bytes:
    """
    Fixed-length key=value message so we can do CBC bitflipping later.
    Keep lengths stable: pad names with underscores/spaces.
    """
    if len(amount_6digits) != 6 or not amount_6digits.isdigit():
        raise ValueError("amount_6digits must be exactly 6 digits, e.g. '000100'")

    msg = (
        "FROM=ALICE____;"
        "TO=BOB______ ;"
        f"AMOUNT={amount_6digits};"
        "CURRENCY=USD;"
        "NOTE=HELLO__________;"
    )
    return msg.encode("utf-8")


def load_or_create_key(path: Path, nbytes: int = 32) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return path.read_bytes()
    key = rand_bytes(nbytes)
    path.write_bytes(key)
    return key


def save_packet(path: Path, iv: bytes, ciphertext: bytes) -> None:
    """
    Packet format (Phase 1):
      [16B IV] + [ciphertext...]
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(iv + ciphertext)


def load_packet(path: Path) -> tuple[bytes, bytes]:
    data = path.read_bytes()
    if len(data) < 16:
        raise ValueError("Packet too short")
    return data[:16], data[16:]


def main() -> None:
    key = load_or_create_key(KEY_PATH, 32)

    plaintext = build_fixed_message("000100")
    print("=== PLAINTEXT (original) ===")
    print(plaintext.decode("utf-8"))

    iv, ct = encrypt_cbc(key, plaintext)
    save_packet(PACKET_PATH, iv, ct)
    print(f"\n[+] Saved packet: {PACKET_PATH}")

    iv2, ct2 = load_packet(PACKET_PATH)
    recovered = decrypt_cbc(key, iv2, ct2)

    print("\n=== PLAINTEXT (decrypted) ===")
    print(recovered.decode("utf-8"))


if __name__ == "__main__":
    main()