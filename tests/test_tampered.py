from __future__ import annotations

from pathlib import Path

from core.cbc import decrypt_cbc

KEY_PATH = Path("data/keys/aes_key.bin")
TAMPERED_PACKET = Path("data/packets/phase2_amount_999.bin")  # <-- changed


def load_packet(path: Path) -> tuple[bytes, bytes]:
    data = path.read_bytes()
    if len(data) < 16:
        raise ValueError("Packet too short (need at least 16 bytes IV)")
    return data[:16], data[16:]


def main() -> None:
    if not KEY_PATH.exists():
        raise FileNotFoundError(f"Missing key file: {KEY_PATH}")

    if not TAMPERED_PACKET.exists():
        raise FileNotFoundError(f"Missing packet file: {TAMPERED_PACKET}")

    key = KEY_PATH.read_bytes()
    iv, ct = load_packet(TAMPERED_PACKET)

    print("=== Attempting to decrypt tampered packet ===")
    try:
        pt = decrypt_cbc(key, iv, ct)
        print("Decryption succeeded.")
        print(pt.decode("utf-8", errors="replace"))
    except Exception as e:
        print("Decryption failed with error:")
        print(type(e).__name__, str(e))


if __name__ == "__main__":
    main()