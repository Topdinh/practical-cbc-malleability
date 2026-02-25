from pathlib import Path

ORIG = Path("data/packets/phase1_cbc_only.bin")
PATCHED = Path("data/packets/phase2_amount_999.bin")

def main():
    orig = ORIG.read_bytes()
    patched = PATCHED.read_bytes()

    print("Comparing offsets 16–31 (C1 block):")
    print()

    for i in range(16, 32):
        print(
            f"Offset {i}: "
            f"orig={orig[i]:02x}  patched={patched[i]:02x}  "
            f"{'CHANGED' if orig[i] != patched[i] else ''}"
        )

if __name__ == "__main__":
    main()