from pathlib import Path

INFILE = Path("data/packets/phase3_etm.bin")
OUTFILE = Path("data/packets/phase3_etm_tampered.bin")


def main():
    data = bytearray(INFILE.read_bytes())

    # Flip a single byte inside ciphertext region
    # (skip first 16 bytes IV, so flip at offset 20 for example)
    data[20] ^= 0x01

    OUTFILE.write_bytes(bytes(data))
    print(f"[+] Wrote tampered EtM packet: {OUTFILE}")


if __name__ == "__main__":
    main()