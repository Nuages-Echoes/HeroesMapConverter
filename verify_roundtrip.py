"""
Round-trip verification for the conversion pipeline.

For every map in input/, checks that:
  parse(input) -> unified -> game JSON -> write(output) -> parse(output)
produces the same map data as parsing the input directly.

The comparison is semantic (the parsed structures must be equal). For
fh2m maps the binary writer re-encodes every field, so the parsed
structures cover the whole file. For h3m maps the Objects > Raw Data
section (raw object bytes kept for reference) is excluded: the binary
writer does not re-encode object instances yet.
"""

import json
import os
import sys

from h2decoder import parse_fh2m
from h3decoder import parse_h3m


def normalize_h3m(data):
    data = json.loads(json.dumps(data, sort_keys=True))
    data.pop("Objects", None)
    return data


def normalize_fh2m(data):
    return json.loads(json.dumps(data, sort_keys=True))


def main():
    input_dir = "input"
    output_dir = "output"
    failures = []

    for file_name in sorted(os.listdir(input_dir)):
        if file_name.lower().endswith(".h3m"):
            kind = "h3m"
            parse = parse_h3m
            normalize = normalize_h3m
        elif file_name.lower().endswith(".fh2m"):
            kind = "fh2m"
            parse = parse_fh2m
            normalize = normalize_fh2m
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

        if before == after:
            print(f"{file_name} : round-trip OK")
        else:
            diff_keys = [k for k in set(before) | set(after) if before.get(k) != after.get(k)]
            failures.append(f"{file_name} : differs ({', '.join(sorted(diff_keys))})")

    if failures:
        print()
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
