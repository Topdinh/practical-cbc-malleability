from __future__ import annotations

from core.utils import pkcs7_pad

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


def main() -> None:
    pt = build_message()
    padded = pkcs7_pad(pt, BLOCK)

    # --- Original functionality (kept) ---
    print("Total length:", len(padded))
    print()

    for i in range(0, len(padded), BLOCK):
        block = padded[i : i + BLOCK]
        print(
            f"Block {i//BLOCK:02d} @ offset {i:03d}: {block!r} | "
            f"{block.decode('utf-8', errors='replace')}"
        )

    # --- Added: precise byte index mapping (for correct bitflip offsets) ---
    print("\nByte index mapping (UNPADDED plaintext):")
    text = pt.decode("utf-8", errors="replace")
    for idx, ch in enumerate(text):
        print(f"{idx:03d}: {ch}")

    # --- Added: locate the amount substring precisely ---
    needle = "AMOUNT=000100;"
    pos = text.find(needle)
    print("\nFind substring:", needle)
    print("Start index:", pos)
    if pos != -1:
        for j, ch in enumerate(needle):
            print(f"  idx {pos + j:03d}: {ch}")


if __name__ == "__main__":
    main()