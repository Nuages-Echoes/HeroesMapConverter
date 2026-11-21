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

# Validation limits and header rules, aligned with the local reference
# olden-era-map-vs-code-inspector (src/parser.js): input file up to 32 MiB,
# decompressed payload up to 64 MiB, at most 250,000 placed objects, a
# 32-hex-char header hash, a N.N.N version string and a 2-byte separator
# of 05 00 (3 blocks) or 0d 00 (4 blocks). The other local reference
# (map-editor-json-tool, src/lib/map-parser.ts) reads the hash/version
# length prefixes as a single byte instead of a varint - identical for
# every real map (both lengths are < 128); we keep the varint reading.
INPUT_LIMIT = 32 * 1024 * 1024
OUTPUT_LIMIT = 64 * 1024 * 1024
OBJECT_LIMIT = 250000
KNOWN_VERSIONS = ("0.72.30", "0.80.47", "0.82.08")
VALID_SEPARATORS = ([0x05, 0x00], [0x0D, 0x00])


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
    import re as _re

    with open(file_path, "rb") as f:
        compressed = f.read()
    if len(compressed) > INPUT_LIMIT:
        raise ValueError("Compressed .map exceeds %d bytes" % INPUT_LIMIT)

    gzip_header, _ = parse_gzip_header(compressed)
    data = gzip.decompress(compressed)
    if len(data) > OUTPUT_LIMIT:
        raise ValueError("Decompressed .map exceeds %d bytes" % OUTPUT_LIMIT)

    warnings = []

    pos = 0
    hash_len, pos = read_varint(data, pos)
    if pos + hash_len > len(data):
        raise ValueError("Truncated .map header: incomplete hash")
    header_hash = data[pos:pos + hash_len].decode("utf-8")
    pos += hash_len
    if not _re.match(r"^[a-f0-9]{32}$", header_hash, _re.IGNORECASE):
        warnings.append("header hash is not 32 hex chars: %r" % header_hash)

    version_len, pos = read_varint(data, pos)
    if pos + version_len > len(data):
        raise ValueError("Truncated .map header: incomplete version")
    version = data[pos:pos + version_len].decode("utf-8")
    pos += version_len
    if not _re.match(r"^\d+\.\d+\.\d+$", version):
        warnings.append("version does not look like N.N.N: %r" % version)
    elif version not in KNOWN_VERSIONS:
        warnings.append("unverified game version %s (known: %s)"
                        % (version, ", ".join(KNOWN_VERSIONS)))

    if pos + 2 > len(data):
        raise ValueError("Truncated .map header: missing separator")
    separator = [data[pos], data[pos + 1]]
    pos += 2
    if separator not in VALID_SEPARATORS:
        warnings.append("unsupported separator %s (expected 05 00 or 0d 00)"
                        % bytes(separator).hex())
    expected_blocks = 4 if separator == [0x0D, 0x00] else 3

    blocks = []
    while pos < len(data):
        block_start = pos
        length, pos = read_varint(data, pos)
        if pos + length > len(data):
            warnings.append("block %d truncated at offset %d; rest kept as trailing data"
                            % (len(blocks) + 1, block_start))
            pos = block_start
            break
        raw = data[pos:pos + length].decode("utf-8")
        pos += length
        name = block_name(len(blocks))
        if raw == "":
            parsed = {}
        else:
            parse_text = raw[1:] if raw.startswith("\ufeff") else raw
            try:
                parsed = json.loads(parse_text)
            except json.JSONDecodeError:
                parsed = None
                warnings.append("block %s is not valid JSON; raw text kept" % name)
            else:
                if parsed is None or isinstance(parsed, (list, str, int, float, bool)):
                    warnings.append("block %s is not a JSON object" % name)
        blocks.append(OrderedDict([
            ("name", name),
            ("raw", raw),
            ("data", parsed),
        ]))

    if len(blocks) < expected_blocks:
        for i in range(len(blocks), expected_blocks):
            warnings.append("missing observed block %s" % block_name(i))
    elif len(blocks) > expected_blocks:
        warnings.append("%d extra block(s) beyond the separator's %d"
                        % (len(blocks) - expected_blocks, expected_blocks))

    trailing_data = data[pos:].hex() if pos < len(data) else ""
    if trailing_data:
        warnings.append("preserved %d opaque trailing byte(s)" % (len(trailing_data) // 2))

    # Structural checks on the adventure block (mirrors the inspector's
    # object-column validation, as warnings so nothing is ever dropped).
    for block in blocks:
        if block["name"] != "adventure" or not isinstance(block["data"], dict):
            continue
        adventure = block["data"]
        objects = adventure.get("objects")
        if objects is not None and not isinstance(objects, list):
            warnings.append("adventure.objects is not an array")
            objects = None
        total = 0
        if objects is not None:
            for group_index, group in enumerate(objects):
                if not isinstance(group, dict):
                    warnings.append("invalid object group %d" % group_index)
                    continue
                sid, ids = group.get("sid"), group.get("ids")
                columns = [group.get(k) for k in ("nodes", "rotations", "levels")]
                if not isinstance(sid, str) or not isinstance(ids, list) \
                        or not all(isinstance(c, list) and len(c) == len(ids) for c in columns):
                    warnings.append("invalid object columns at group %d" % group_index)
                    continue
                total += len(ids)
                for row, oid in enumerate(ids):
                    # ids/nodes/rotations are integers; levels is a float
                    # column on real maps (heights like -1.5, 0.5).
                    vals = [oid, columns[0][row], columns[1][row]]
                    if not all(isinstance(v, int) and not isinstance(v, bool) for v in vals) \
                            or not isinstance(columns[2][row], (int, float)) \
                            or isinstance(columns[2][row], bool):
                        warnings.append("invalid object column value at group %d, row %d"
                                        % (group_index, row))
                        break
            if total > OBJECT_LIMIT:
                warnings.append("object count %d exceeds %d" % (total, OBJECT_LIMIT))
        props = adventure.get("objectsProperties")
        if isinstance(props, dict):
            prs = props.get("propRandomSquads")
            if prs is not None and not isinstance(prs, list):
                warnings.append("propRandomSquads is not an array")
            elif isinstance(prs, list):
                for row in prs:
                    if not isinstance(row, dict) or not isinstance(row.get("id"), int):
                        warnings.append("invalid propRandomSquads row id")
                        break

    return OrderedDict([
        ("gzipHeader", gzip_header),
        ("headerHash", header_hash),
        ("version", version),
        ("separator", separator),
        ("blocks", blocks),
        ("trailingData", trailing_data),
        ("warnings", warnings),
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
