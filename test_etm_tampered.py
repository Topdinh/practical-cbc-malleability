from pathlib import Path

from core.etm import decrypt_etm

ENC_KEY_PATH = Path("data/keys/aes_key.bin")
MAC_KEY_PATH = Path("data/keys/hmac_key.bin")
PACKET_PATH = Path("data/packets/phase3_etm_tampered.bin")


def main():
    enc_key = ENC_KEY_PATH.read_bytes()
    mac_key = MAC_KEY_PATH.read_bytes()

    packet = PACKET_PATH.read_bytes()

    print("=== Attempting to decrypt tampered EtM packet ===")

    try:
        pt = decrypt_etm(enc_key, mac_key, packet)
        print("Decryption succeeded (unexpected!).")
        print(pt.decode())
    except Exception as e:
        print("Decryption failed as expected.")
        print(type(e).__name__, str(e))


if __name__ == "__main__":
    main()