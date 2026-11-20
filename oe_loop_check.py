"""
Full-loop check for the Olden Era conversion.

For every .h3m/.fh2m map in input/, converts it to an Olden Era .map via
the unified JSON (written to outputloop/<name>.map), converts that .map
back to the original format (outputloop/<name>.h3m/.fh2m), and compares
the object inventories of the original and the round-tripped map:

- type level: h3m classes (group, class, subclass) for h3m sources,
  (group, index) for fh2m sources;
- reference level: the h3m (class, subtype) each unified object resolves
  to through unified._unified_obj_h3m_ref, which normalizes away the
  scenery variant collapses (many H2/H3 sprite variants share one OE
  sid);
- sprite variants of h3m sources are counted separately.

It also collects unified.HOMMOE_UNMAPPED_OBJECTS, the objects dropped when
writing the .map because the OE correspondence has no equivalent for their
type (see no_olden_era_equivalent.english.txt).

Usage: python3 oe_loop_check.py [substring ...]
"""

import collections
import os
import sys

from h2decoder import parse_fh2m, write_fh2m
from h3decoder import parse_h3m, write_h3m
from hommoedecoder import parse_hommoe, write_hommoe
import unified as U
from unified import convert_to_unified, convert_from_unified

INPUT_DIR = "input"
LOOP_DIR = "outputloop"


def inventories(unified):
    """(type inventory, reference-level inventory, sprite variants)."""
    types = collections.Counter()
    refs = collections.Counter()
    variants = collections.Counter()
    tbp = {}
    for level in (unified.get("terrain") or {}).get("levels", []):
        for cell in level.get("grid", []):
            tbp[(cell.get("x"), cell.get("y"))] = cell.get("terrain", "Grass")
    for tile_key, obj_list in (unified.get("objects") or {}).get("tiles", {}).items():
        parts = tile_key.split("_")
        terrain = "Grass"
        if len(parts) == 3:
            terrain = tbp.get((int(parts[0]), int(parts[1])), "Grass")
        for obj in obj_list:
            if obj.get("class") is not None:
                key = (obj.get("group"), "class=%s" % obj.get("class"),
                       "sub=%s" % obj.get("subclass"))
                variants[(key, "sprite=%s" % obj.get("sprite"))] += 1
            else:
                key = (obj.get("group"), "index=%s" % obj.get("index"))
            types[key] += 1
            ref = U._unified_obj_h3m_ref(obj, terrain)
            refs[("h3", ref[0], ref[1]) if ref else key] += 1
    return types, refs, variants


def main():
    os.makedirs(LOOP_DIR, exist_ok=True)
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    total_lost = collections.Counter()
    total_unmapped = collections.Counter()
    for file_name in sorted(os.listdir(INPUT_DIR)):
        lower = file_name.lower()
        if lower.endswith(".h3m"):
            game, parse, write = "h3m", parse_h3m, write_h3m
        elif lower.endswith((".fh2m", ".mp2")):
            game, parse, write = "fh2m", parse_fh2m, write_fh2m
        else:
            continue
        if only and not any(o in file_name for o in only):
            continue
        base = os.path.splitext(file_name)[0]
        src = parse(os.path.join(INPUT_DIR, file_name))
        u_src = convert_to_unified(src, game)
        write_hommoe(convert_from_unified(u_src, "hommoe"),
                     os.path.join(LOOP_DIR, base + ".map"))
        for o in U.HOMMOE_UNMAPPED_OBJECTS:
            ref = U._unified_obj_h3m_ref(o)
            key = ("h3 class %s" % ref[0]) if ref else (o.get("group"), o.get("index"))
            total_unmapped[key] += 1
        u_oe = convert_to_unified(parse_hommoe(os.path.join(LOOP_DIR, base + ".map")),
                                  "hommoe")
        back_ext = ".h3m" if game == "h3m" else ".fh2m"
        write(convert_from_unified(u_oe, game),
              os.path.join(LOOP_DIR, base + back_ext))
        u_back = convert_to_unified(parse(os.path.join(LOOP_DIR, base + back_ext)),
                                    game)

        types_src, refs_src, var_src = inventories(u_src)
        types_back, refs_back, var_back = inventories(u_back)
        lost = refs_src - refs_back
        gained = refs_back - refs_src
        var_lost = var_src - var_back
        print("== %s (%s): objects %d -> %d, lost ref-types %d (%d objs), "
              "gained %d (%d objs), sprite variants changed %d" % (
                  file_name, game, sum(types_src.values()), sum(types_back.values()),
                  len(lost), sum(lost.values()), len(gained), sum(gained.values()),
                  sum(var_lost.values())))
        for key, n in lost.most_common(15):
            name = U.OE_H3_NAMES.get(str(key[1]), "") if key[0] == "h3" else ""
            print("   LOST %5d  %s %s" % (n, key, name))
            total_lost[key] += n
        if len(lost) > 15:
            print("   ... %d more lost types" % (len(lost) - 15))

    print("\n== TOTAL lost reference types across all maps ==")
    for key, n in total_lost.most_common(40):
        name = U.OE_H3_NAMES.get(str(key[1]), "") if key[0] == "h3" else ""
        print("%6d  %s %s" % (n, key, name))
    print("\n== TOTAL objects dropped when writing .map (no OE equivalent) ==")
    for key, n in total_unmapped.most_common(40):
        print("%6d  %s" % (n, key))
    return 0


if __name__ == "__main__":
    sys.exit(main())
