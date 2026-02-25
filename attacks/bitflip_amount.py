from __future__ import annotations

from pathlib import Path

INFILE = Path("data/packets/phase1_cbc_only.bin")
OUTFILE = Path("data/packets/phase2_amount_999.bin")

# We want to change the amount in the plaintext block starting at offset 32:
#   Block @ offset 32: b'UNT=000100;CURRE'
# The digits "000100" are at indices 4..9 within that block.
#
# CBC rule:
#   To change plaintext block Pi, flip bytes in previous ciphertext block C{i-1}.
#
# Packet format:
#   [IV 16B][C1 16B][C2 16B][C3 ...]
#
# The plaintext block starting at offset 32 corresponds to Pi where the previous
# ciphertext block starts at packet offset 32 (C2).
#
# We only change the last 3 digits: "100" -> "999"
#   '1'(0x31) -> '9'(0x39)  delta = 0x08
#   '0'(0x30) -> '9'(0x39)  delta = 0x09
#   '0'(0x30) -> '9'(0x39)  delta = 0x09
#
# Those digits are at indices 7, 8, 9 in the block (offsets 39, 40, 41 overall).
# Therefore patch offsets in PACKET FILE:
#   C2_start = 32
#   32+7=39, 32+8=40, 32+9=41
PATCHES = [
    (39, 0x08),  # '1' -> '9'
    (40, 0x09),  # '0' -> '9'
    (41, 0x09),  # '0' -> '9'
]


def apply_patches(data: bytes) -> bytes:
    b = bytearray(data)
    for off, x in PATCHES:
        if off < 0 or off >= len(b):
            raise ValueError(f"Offset out of range: {off}")
        b[off] ^= x
    return bytes(b)


def main() -> None:
    data = INFILE.read_bytes()
    out = apply_patches(data)
    OUTFILE.parent.mkdir(parents=True, exist_ok=True)
    OUTFILE.write_bytes(out)
    print(f"[+] Wrote tampered packet: {OUTFILE}")


if __name__ == "__main__":
    main()