from __future__ import annotations

import argparse
from pathlib import Path


def flip_byte(data: bytes, offset: int, xor_value: int) -> bytes:
    if offset < 0 or offset >= len(data):
        raise ValueError("Offset out of range")

    if xor_value < 0 or xor_value > 255:
        raise ValueError("xor_value must be 0..255")

    modified = bytearray(data)
    modified[offset] ^= xor_value
    return bytes(modified)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tamper with packet by flipping one byte.")
    parser.add_argument("--infile", required=True, help="Input packet file")
    parser.add_argument("--outfile", required=True, help="Output tampered packet file")
    parser.add_argument("--offset", type=int, required=True, help="Byte offset to flip")
    parser.add_argument("--xor", type=int, required=True, help="XOR value (0-255)")

    args = parser.parse_args()

    data = Path(args.infile).read_bytes()
    tampered = flip_byte(data, args.offset, args.xor)
    Path(args.outfile).write_bytes(tampered)

    print(f"[+] Tampered packet saved to: {args.outfile}")


if __name__ == "__main__":
    main()