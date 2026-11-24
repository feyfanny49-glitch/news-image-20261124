#!/usr/bin/env python3
"""Validate the shipped PNG exactly the way the competition gate describes.

Checks: signature, IHDR, every chunk's CRC, IEND, the dimension cap and the
one-megabyte cap. Prints bytes, dimensions and sha256 for the build record.
"""

import hashlib
import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "entry.png"
MAX_BYTES = 1048576
MAX_SIDE = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("INVALID:", message)
    raise SystemExit(1)


def main():
    data = TARGET.read_bytes()
    if not data.startswith(SIGNATURE):
        fail("bad PNG signature")
    if len(data) > MAX_BYTES:
        fail(f"{len(data)} bytes exceeds {MAX_BYTES}")

    pos = len(SIGNATURE)
    width = height = None
    seen_ihdr = seen_iend = False
    chunks = []
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        length = struct.unpack_from(">I", data, pos)[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            fail(f"truncated chunk {kind!r}")
        body = data[pos + 8:pos + 8 + length]
        stored = struct.unpack_from(">I", data, pos + 8 + length)[0]
        actual = zlib.crc32(kind + body) & 0xFFFFFFFF
        if stored != actual:
            fail(f"CRC mismatch in {kind!r}")
        chunks.append(kind.decode("latin-1"))
        if not seen_ihdr:
            if kind != b"IHDR" or length != 13:
                fail("first chunk is not a 13-byte IHDR")
            width, height, depth, colour, comp, filt, interlace = struct.unpack(
                ">IIBBBBB", body)
            if not (1 <= width <= MAX_SIDE and 1 <= height <= MAX_SIDE):
                fail(f"dimensions {width}x{height} exceed {MAX_SIDE}x{MAX_SIDE}")
            if comp or filt or interlace:
                fail("unsupported compression, filter or interlace")
            seen_ihdr = True
        pos = end
        if kind == b"IEND":
            if length != 0:
                fail("IEND is not empty")
            seen_iend = True
            break

    if not seen_ihdr:
        fail("no IHDR")
    if not seen_iend:
        fail("no IEND")
    if pos != len(data):
        fail("trailing bytes after IEND")

    print("VALID PNG")
    print(f"bytes: {len(data)}")
    print(f"dimensions: {width}x{height}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(f"chunks: {len(chunks)} (first {chunks[0]}, last {chunks[-1]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
