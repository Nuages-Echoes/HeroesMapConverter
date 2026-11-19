"""
HOMMOE File Parser/Writer for Heroes of Might and Magic: Olden Era

This module reads and writes native .map files from the Olden Era edition
(by Unfrozen) and converts them to/from a structured dictionary format
based on the specification in hommoe_description.english.txt.

A .map file is a single gzip stream. After decompression, the layout is:

    1 byte   hashLen, then hashLen bytes (a 32-char hex digest)
    1 byte   verLen,  then verLen bytes  (version string, e.g. "0.82.08")
    2 bytes  separator (observed 05 00 for 3-block maps, 0D 00 when a
             fourth scripting block is present: bit 0x08 of the first
             byte is the "scripts embedded" flag)
    N times  unsigned LEB128 varint (byte length) + that many bytes of
             UTF-8 JSON (N is usually 3 or 4; blocks are read until the
             end of the decompressed data)
    optional opaque trailing bytes, preserved verbatim

The canonical names of the JSON blocks, in file order, are "scenario",
"adventure", "dialogQuestData" and "commentAiData".

Each block is kept both as its exact raw JSON text ("raw", so the writer can
re-emit the decompressed content byte-identically) and as its parsed content
("data").

Format documented from the reference implementations (local copies under
/workspace/references/):
- map-editor-json-tool: src/lib/map-parser.ts, src/lib/map-write.ts
  (https://github.com/mimiasei/map-editor-json-tool)
- olden-era-map-vs-code-inspector: src/parser.js, docs/map-format.md
  (https://github.com/IgorIziyoAlhasov/olden-era-map-vs-code-inspector)
"""

import gzip
import json
import struct
import zlib
from collections import OrderedDict

GZIP_MAGIC = b"\x1f\x8b"

# Gzip header fields observed on every real .map sample (game and editor
# resources alike): FLG=0, MTIME=0, XFL=0, OS=10. The deflate stream is
# zlib level 6, memLevel 8, default strategy, raw (wbits=-15): recompressing
# the payload with those settings reproduces the original file byte-for-byte.
DEFAULT_GZIP_HEADER = {"flg": 0, "mtime": 0, "xfl": 0, "os": 10}
DEFLATE_LEVEL = 6
DEFLATE_MEM_LEVEL = 8

BLOCK_NAMES = ["scenario", "adventure", "dialogQuestData", "commentAiData"]

SCRIPTS_FLAG = 0x08


def read_varint(data, pos):
    """Read an unsigned LEB128 varint from data at pos. Returns (value, next_pos)."""
    result = 0
    shift = 0
    while True:
        if pos >= len(data):
            raise ValueError(f"Varint overrun at offset {pos}")
        byte = data[pos]
        pos += 1
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            return result, pos
        shift += 7
        if shift > 35:
            raise ValueError("Varint too long")


def write_varint(value):
    """Encode a non-negative integer as an unsigned LEB128 varint."""
    if value < 0:
        raise ValueError("Varint cannot be negative")
    out = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            out.append(byte | 0x80)
        else:
            out.append(byte)
            return bytes(out)


def block_name(index):
    """Canonical name of the JSON block at the given 0-based index."""
    if index < len(BLOCK_NAMES):
        return BLOCK_NAMES[index]
    return f"block{index + 1}"


def parse_gzip_header(compressed):
    """Extract the gzip header fields and any optional header bytes.

    Returns (header_dict, deflate_offset): header_dict holds "flg", "mtime",
    "xfl", "os" and "extra" (hex string of the optional FEXTRA/FNAME/FCOMMENT/
    FHCRC bytes between the fixed 10-byte header and the deflate stream);
    deflate_offset is where the deflate stream starts.
    """
    if compressed[:len(GZIP_MAGIC)] != GZIP_MAGIC or len(compressed) < 18:
        raise ValueError("Not an Olden Era map file: expected a gzip stream")
    flg = compressed[3]
    mtime = struct.unpack("<I", compressed[4:8])[0]
    xfl = compressed[8]
    os_byte = compressed[9]
    pos = 10
    if flg & 4:
        xlen = struct.unpack("<H", compressed[pos:pos + 2])[0]
        pos += 2 + xlen
    if flg & 8:
        pos = compressed.index(b"\x00", pos) + 1
    if flg & 16:
        pos = compressed.index(b"\x00", pos) + 1
    if flg & 2:
        pos += 2
    if pos > len(compressed) - 8:
        raise ValueError("Truncated .map file: incomplete gzip header")
    header = OrderedDict([
        ("flg", flg),
        ("mtime", mtime),
        ("xfl", xfl),
        ("os", os_byte),
        ("extra", compressed[10:pos].hex()),
    ])
    return header, pos


def write_gzip(payload, gzip_header):
    """Compress payload into a gzip stream matching the game's convention:
    stored header fields, raw deflate at level 6 / memLevel 8 / default
    strategy, CRC32 + ISIZE trailer."""
    header = gzip_header or {}
    out = bytearray()
    out += GZIP_MAGIC
    out.append(8)
    out.append(header.get("flg", DEFAULT_GZIP_HEADER["flg"]))
    out += struct.pack("<I", header.get("mtime", DEFAULT_GZIP_HEADER["mtime"]))
    out.append(header.get("xfl", DEFAULT_GZIP_HEADER["xfl"]))
    out.append(header.get("os", DEFAULT_GZIP_HEADER["os"]))
    out += bytes.fromhex(header.get("extra") or "")
    compressor = zlib.compressobj(DEFLATE_LEVEL, zlib.DEFLATED, -15,
                                   DEFLATE_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY)
    out += compressor.compress(payload) + compressor.flush()
    out += struct.pack("<II", zlib.crc32(payload) & 0xFFFFFFFF,
                       len(payload) & 0xFFFFFFFF)
    return bytes(out)


def parse_hommoe(file_path):
    """
    Parse an Olden Era native map file (.map).

    Args:
        file_path: Path to the .map file

    Returns:
        OrderedDict: A structured dictionary containing map information:
        "headerHash" (str), "version" (str), "separator" (list of 2 ints),
        "blocks" (list of {"name", "raw", "data"} entries; "raw" holds the
        exact JSON text of the block, "data" its parsed content, {} for an
        empty block and None if the text is not valid JSON) and
        "trailingData" (hex string of any opaque bytes after the last
        block, "" if none).
    """
    with open(file_path, "rb") as f:
        compressed = f.read()

    gzip_header, _ = parse_gzip_header(compressed)
    data = gzip.decompress(compressed)

    pos = 0
    hash_len, pos = read_varint(data, pos)
    if pos + hash_len > len(data):
        raise ValueError("Truncated .map header: incomplete hash")
    header_hash = data[pos:pos + hash_len].decode("latin-1")
    pos += hash_len

    version_len, pos = read_varint(data, pos)
    if pos + version_len > len(data):
        raise ValueError("Truncated .map header: incomplete version")
    version = data[pos:pos + version_len].decode("utf-8")
    pos += version_len

    if pos + 2 > len(data):
        raise ValueError("Truncated .map header: missing separator")
    separator = [data[pos], data[pos + 1]]
    pos += 2

    blocks = []
    while pos < len(data):
        block_start = pos
        length, pos = read_varint(data, pos)
        if pos + length > len(data):
            pos = block_start
            break
        raw = data[pos:pos + length].decode("utf-8")
        pos += length
        if raw == "":
            parsed = {}
        else:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = None
        blocks.append(OrderedDict([
            ("name", block_name(len(blocks))),
            ("raw", raw),
            ("data", parsed),
        ]))

    trailing_data = data[pos:].hex() if pos < len(data) else ""

    return OrderedDict([
        ("gzipHeader", gzip_header),
        ("headerHash", header_hash),
        ("version", version),
        ("separator", separator),
        ("blocks", blocks),
        ("trailingData", trailing_data),
    ])


def write_hommoe(map_data, output_path):
    """
    Write an Olden Era native map file (.map) from a structured dictionary,
    as produced by parse_hommoe and the JSON files in outputjson/.

    Each block is re-emitted from its "raw" text verbatim when present, so
    the decompressed content stays byte-identical to the source; blocks
    without "raw" are serialized from "data" with json.dumps.

    Args:
        map_data: Dictionary containing map information.
        output_path: Path of the .map file to write.
    """
    header_hash = map_data["headerHash"].encode("latin-1")
    version = map_data["version"].encode("utf-8")
    separator = bytes(map_data["separator"])
    if len(separator) != 2:
        raise ValueError("Separator must be exactly 2 bytes")

    container = bytearray()
    container += write_varint(len(header_hash))
    container += header_hash
    container += write_varint(len(version))
    container += version
    container += separator

    for block in map_data.get("blocks", []):
        raw = block.get("raw")
        if raw is None:
            raw = json.dumps(block.get("data", {}), ensure_ascii=False)
        payload = raw.encode("utf-8")
        container += write_varint(len(payload))
        container += payload

    trailing_data = map_data.get("trailingData") or ""
    if trailing_data:
        container += bytes.fromhex(trailing_data)

    with open(output_path, "wb") as f:
        f.write(write_gzip(bytes(container), map_data.get("gzipHeader")))
