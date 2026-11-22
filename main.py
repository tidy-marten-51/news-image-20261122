#!/usr/bin/env python3
"""The World Today — Sunday 22 November 2026.

The front page is drawn ahead of time and shipped in this repository
as entry.png (1024x1024, 131,375 bytes, rendered deterministically
from draw_frontpage.py). This program only checks that image against
the competition's gate and copies it byte for byte to the output
directory, so the grader's two runs produce identical bytes.

Standard library only: no Pillow, no fonts, no network, no
randomness, no timestamps, nothing read from outside the repo.

Usage (as the grader runs it):
    MAKEFUN_OUTPUT_DIR=/output python3 -P -s /bot/main.py
"""

import os
import struct
import sys
import zlib
from pathlib import Path

MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def fail(message):
    """Report a gate failure on stderr and exit non-zero."""
    print("main.py: " + message, file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Validate the shipped image; return (width, height).

    Walks every chunk, verifying CRCs, and reads the dimensions from
    IHDR, so a truncated or corrupt file is rejected here instead of
    being copied to the output directory.
    """
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        fail(SOURCE_NAME + " is not a PNG file (bad signature)")

    if len(data) > MAX_BYTES:
        fail("%s is %d bytes, over the 1 MiB limit"
             % (SOURCE_NAME, len(data)))

    offset = 8
    width = None
    height = None
    saw_iend = False
    while offset < len(data):
        if offset + 8 > len(data):
            fail(SOURCE_NAME + " ends in the middle of a chunk header")
        chunk_len = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 12 + chunk_len
        if end > len(data):
            fail(SOURCE_NAME + " ends in the middle of a chunk")
        body = data[offset + 8:offset + 8 + chunk_len]
        stored_crc = struct.unpack(">I", data[end - 4:end])[0]
        actual_crc = zlib.crc32(chunk_type + body) & 0xFFFFFFFF
        if stored_crc != actual_crc:
            fail("chunk %r has a bad CRC" % chunk_type.decode("latin-1"))
        if chunk_type == b"IHDR":
            if chunk_len != 13:
                fail("IHDR chunk has the wrong length")
            width, height = struct.unpack(">II", body[:8])
        if chunk_type == b"IEND":
            saw_iend = True
            break
        offset = end

    if width is None or height is None:
        fail(SOURCE_NAME + " has no IHDR chunk")
    if not saw_iend:
        fail(SOURCE_NAME + " has no IEND chunk")
    if width > MAX_WIDTH or height > MAX_HEIGHT:
        fail("%s is %dx%d, over the %dx%d limit"
             % (SOURCE_NAME, width, height, MAX_WIDTH, MAX_HEIGHT))
    return width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        fail(SOURCE_NAME + " is missing from the repository")

    data = source.read_bytes()
    width, height = check_png(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = Path(out_dir) / OUTPUT_NAME
    target.write_bytes(data)
    print("wrote %s (%dx%d, %d bytes, byte-identical copy)"
          % (target, width, height, len(data)))


if __name__ == "__main__":
    main()
