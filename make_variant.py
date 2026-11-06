import argparse
import copy
import json
import os

import correspondence
from correspondence import (FH2M_TO_H3M_MISC, FH2M_TO_H3M_MONSTERS,
                            FH2M_TO_H3M_SHRINES)
from h3decoder import write_h3m
from unified import convert_from_unified


def h3m_class_of(obj):
    """h3m object class an unified (fh2m-style) tile object encodes to.

    Mirrors the group dispatch of unified._encode_h3m_objects for the
    groups that can produce the classes we want to exclude; every other
    group returns None (kept).
    """
    group = obj.get("group")
    index = obj.get("index", 0)
    if group == "KINGDOM_HEROES":
        return 34
    if group == "MONSTERS":
        creature = index + 1
        if creature in (67, 68, 69, 70, 71):
            return 71 + (creature - 67)
        return 54
    if group == "ADVENTURE_POWER_UPS":
        shrine = FH2M_TO_H3M_SHRINES.get(index)
        if shrine is not None:
            return shrine
        target = FH2M_TO_H3M_MISC.get("POWER_%d" % index)
        if target is not None:
            return target[0]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Génère une variante h3m d'une carte convertie, sans les "
                    "objets des classes h3m indiquées (utile pour isoler un "
                    "crash au chargement).")
    parser.add_argument("map_name", help="Nom de base de la carte (ex. Tetra_conflict), "
                                         "lu depuis outputunified/<map_name>.json")
    parser.add_argument("--exclude", default="34,54,56",
                        help="Classes h3m à retirer, séparées par des virgules "
                             "(défaut: 34,54,56).")
    parser.add_argument("--strip-unused-monster-defs", action="store_true",
                        help="Ne garder dans le catalogue que les defs classe 54 "
                             "référencées par les instances restantes (les defs "
                             "auto-ajoutées pour toutes les créatures 0-144 sont "
                             "retirées).")
    parser.add_argument("--suffix", default=None,
                        help="Suffixe du fichier de sortie (défaut: no<classes>).")
    args = parser.parse_args()

    excluded = sorted({int(x) for x in args.exclude.split(",")})
    suffix = args.suffix or "no" + "_".join(str(c) for c in excluded)

    with open(os.path.join("outputunified", args.map_name + ".json"),
              encoding="utf-8") as f:
        unified = json.load(f)

    variant = copy.deepcopy(unified)
    tiles = variant["objects"]["tiles"]
    removed = []
    for tile_key in list(tiles.keys()):
        kept = []
        for obj in tiles[tile_key]:
            cls = h3m_class_of(obj)
            if cls in excluded:
                removed.append((tile_key, obj.get("id"), obj.get("group"),
                                obj.get("index"), cls))
            else:
                kept.append(obj)
        tiles[tile_key] = kept

    if args.strip_unused_monster_defs:
        used_creatures = set()
        for obj_list in tiles.values():
            for obj in obj_list:
                if obj.get("group") == "MONSTERS":
                    creature = obj.get("index", 0) + 1
                    if creature not in (67, 68, 69, 70, 71):
                        h3m_creature = FH2M_TO_H3M_MONSTERS.get(creature)
                        if h3m_creature is not None:
                            used_creatures.add(h3m_creature)
        correspondence.H3M_CREATURE_DEF_NAMES = {
            cid: name for cid, name in correspondence.H3M_CREATURE_DEF_NAMES.items()
            if cid in used_creatures
        }
        print(f"Catalogue classe 54 restreint aux créatures utilisées: "
              f"{sorted(used_creatures) or 'aucune'}")

    map_data = convert_from_unified(variant, "h3m")
    out_path = os.path.join("output", f"{args.map_name}_{suffix}.h3m")
    write_h3m(map_data, out_path)

    print(f"Objets retirés ({len(removed)}):")
    for tile_key, obj_id, group, index, cls in removed:
        print(f"  tile={tile_key} id={obj_id} group={group} index={index} -> h3m class {cls}")
    print(f"Variante écrite dans {out_path}")


if __name__ == "__main__":
    main()
