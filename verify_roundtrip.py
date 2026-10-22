"""
Round-trip verification for the conversion pipeline.

For every map in input/, checks that the file regenerated in output/
carries the exact same data as the input:

- binary equality (byte-to-byte) when both files were produced by the
  same zlib build;
- otherwise, equality of the logical content: the fh2m base section and
  the decompressed zlib section must be identical byte-to-byte (the
  deflate stream itself depends on the zlib version that wrote it);
- for h3m, the gzipped content must be identical byte-to-byte.

Additionally the parsed structures must be equal: for fh2m they cover
the whole file; for h3m the Objects > Raw Data reference bytes are
compared through the regenerated file itself.
"""

import gzip
import json
import os
import re
import sys
import zlib

from h2decoder import parse_fh2m
from h3decoder import parse_h3m


def normalize_h3m(data):
    data = json.loads(json.dumps(data, sort_keys=True))
    data.pop("Objects", None)
    return data


def normalize_fh2m(data):
    return json.loads(json.dumps(data, sort_keys=True))


def content_equal_fh2m(input_path, output_path):
    """Compare the logical content of two .fh2m files."""
    with open(input_path, "rb") as f:
        a = f.read()
    with open(output_path, "rb") as f:
        b = f.read()
    if a == b:
        return True, "binary identical"
    # Locate the zlib stream (header 78 9c) in both files.
    pa = [m.start() for m in re.finditer(b"\x78\x9c", a)]
    pb = [m.start() for m in re.finditer(b"\x78\x9c", b)]
    if not pa or not pb:
        return False, "zlib stream not found"
    if a[:pa[0]] != b[:pb[0]]:
        return False, "base section differs"
    ca = zlib.decompress(a[pa[0]:])
    cb = zlib.decompress(b[pb[0]:])
    if ca != cb:
        return False, "decompressed section differs"
    return True, "logical content identical (zlib streams differ)"


def content_equal_h3m(input_path, output_path):
    """Compare the gzipped content of two .h3m files."""
    with gzip.open(input_path, "rb") as f:
        a = f.read()
    with gzip.open(output_path, "rb") as f:
        b = f.read()
    if a == b:
        return True, "content identical"
    return False, "decompressed content differs"


def main():
    input_dir = "input"
    output_dir = "output"
    failures = []

    for file_name in sorted(os.listdir(input_dir)):
        if file_name.lower().endswith(".h3m"):
            kind = "h3m"
            parse = parse_h3m
            normalize = normalize_h3m
            content_equal = content_equal_h3m
        elif file_name.lower().endswith(".fh2m"):
            kind = "fh2m"
            parse = parse_fh2m
            normalize = normalize_fh2m
            content_equal = content_equal_fh2m
        else:
            continue

        input_path = os.path.join(input_dir, file_name)
        output_path = os.path.join(output_dir, file_name)
        if not os.path.exists(output_path):
            failures.append(f"{file_name}: missing output file")
            continue

        try:
            before = normalize(parse(input_path))
            after = normalize(parse(output_path))
        except Exception as e:
            failures.append(f"{file_name}: {e}")
            continue

        if before != after:
            diff_keys = [k for k in set(before) | set(after) if before.get(k) != after.get(k)]
            failures.append(f"{file_name} : parsed data differs ({', '.join(sorted(diff_keys))})")
            continue

        ok, message = content_equal(input_path, output_path)
        if ok:
            print(f"{file_name} : round-trip OK ({message})")
        else:
            failures.append(f"{file_name} : {message}")

    if failures:
        print()
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
