from pathlib import Path

BLOCK = 16
PACKET = Path("data/packets/phase1_cbc_only.bin")


def main():
    data = PACKET.read_bytes()

    print("Total packet length:", len(data))
    print()

    iv = data[:BLOCK]
    print("IV block (offset 0-15):", iv)
    print()

    ciphertext = data[BLOCK:]

    for i in range(0, len(ciphertext), BLOCK):
        block = ciphertext[i:i+BLOCK]
        print(f"C{i//BLOCK+1} (packet offset {BLOCK+i}-{BLOCK+i+15}): {block}")


if __name__ == "__main__":
    main()