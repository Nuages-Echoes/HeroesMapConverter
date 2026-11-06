import argparse
import copy
import json
import os

import correspondence
from correspondence import (FH2M_LANDSCAPE_TO_H3M, FH2M_TO_H3M_ARTIFACTS,
                            FH2M_TO_H3M_DWELLINGS, FH2M_TO_H3M_HERO_RACE,
                            FH2M_TO_H3M_MINES, FH2M_TO_H3M_MISC,
                            FH2M_TO_H3M_MONSTERS, FH2M_TO_H3M_RESOURCES,
                            FH2M_TO_H3M_SHRINES, FH2M_TOWN_RACE_ORDER,
                            H3M_TOWN_TYPE_TO_FH2M_RACE)
from h3decoder import write_h3m
from unified import convert_from_unified


def h3m_class_of(obj):
    """h3m object class an unified (fh2m-style) tile object encodes to.

    Mirrors the group dispatch of unified._encode_h3m_objects; groups
    that are not h3m object instances (ROADS/STREAMS -> terrain) return
    None.
    """
    group = obj.get("group")
    index = obj.get("index", 0)
    if group == "KINGDOM_HEROES":
        race = index % 7
        hero_type = FH2M_TO_H3M_HERO_RACE.get(race) or 0
        return 34
    if group == "MONSTERS":
        creature = index + 1
        if creature in (67, 68, 69, 70, 71):
            return 71 + (creature - 67)
        if FH2M_TO_H3M_MONSTERS.get(creature) is not None:
            return 54
        return None
    if group == "ADVENTURE_TREASURES":
        if FH2M_TO_H3M_RESOURCES.get(index) is not None:
            return 79
        target = FH2M_TO_H3M_MISC.get("TREASURE_%d" % index)
        if target is None:
            return None
        return 76 if target[0] == 76 else target[0]
    if group == "ADVENTURE_ARTIFACTS":
        if index in (91, 92, 93, 94, 95):
            return 65 + {91: 0, 92: 1, 93: 2, 94: 3, 95: 4}[index]
        if FH2M_TO_H3M_ARTIFACTS.get(index + 1) is not None:
            return 5
        return None
    if group == "ADVENTURE_MISCELLANEOUS" and index == 0:
        return 91
    if group == "KINGDOM_TOWNS":
        race_id = index // 2
        if 0 <= race_id < len(FH2M_TOWN_RACE_ORDER):
            for tt, race in H3M_TOWN_TYPE_TO_FH2M_RACE.items():
                if race == FH2M_TOWN_RACE_ORDER[race_id]:
                    return 98
        return None
    if group in ("ADVENTURE_MISCELLANEOUS", "ADVENTURE_WATER"):
        key = ("MISC_%d" % index) if group == "ADVENTURE_MISCELLANEOUS" else ("WATER_%d" % index)
        target = FH2M_TO_H3M_MISC.get(key)
        return target[0] if target is not None else None
    if group == "ADVENTURE_POWER_UPS":
        shrine = FH2M_TO_H3M_SHRINES.get(index)
        if shrine is not None:
            return shrine
        target = FH2M_TO_H3M_MISC.get("POWER_%d" % index)
        return target[0] if target is not None else None
    if group == "ADVENTURE_MINES":
        target = FH2M_TO_H3M_MINES.get(index)
        return target[0] if target is not None else None
    if group == "ADVENTURE_DWELLINGS":
        target = FH2M_TO_H3M_DWELLINGS.get(index)
        return target[0] if target is not None else None
    if group.startswith("LANDSCAPE"):
        if group in ("LANDSCAPE_TREES", "LANDSCAPE_MOUNTAINS"):
            return None  # terrain-dependent class, keep
        target = FH2M_LANDSCAPE_TO_H3M.get((group, index))
        return target if target is not None else None
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
    parser.add_argument("--no-objects", action="store_true",
                        help="Supprime toutes les instances d'objets (garde terrain, "
                             "en-têtes, joueurs, etc.) pour isoler la section en cause.")
    parser.add_argument("--exclude-groups", default="",
                        help="Groupes fh2m à retirer entièrement, séparés par des "
                             "virgules (ex. LANDSCAPE_TREES,LANDSCAPE_MOUNTAINS).")
    parser.add_argument("--hero-def-doc", action="store_true",
                        help="Renomme les defs classe 34 (héros) du catalogue selon la "
                             "convention de la doc: AH0<sub>00.DEF au lieu de "
                             "ah<sub>_e.def.")
    parser.add_argument("--hero-def-name", default=None,
                        help="Remplace le nom de toutes les defs classe 34 du "
                             "catalogue par ce nom (ex. AVXprsn0.def).")
    args = parser.parse_args()

    excluded = sorted({int(x) for x in args.exclude.split(",") if x.strip()})
    if args.no_objects:
        suffix = args.suffix or "noobj"
    else:
        suffix = args.suffix or "no" + "_".join(str(c) for c in excluded)

    with open(os.path.join("outputunified", args.map_name + ".json"),
              encoding="utf-8") as f:
        unified = json.load(f)

    variant = copy.deepcopy(unified)
    tiles = variant["objects"]["tiles"]
    removed = []
    if args.no_objects:
        for tile_key, obj_list in tiles.items():
            removed.extend((tile_key, o.get("id"), o.get("group"),
                            o.get("index"), h3m_class_of(o)) for o in obj_list)
        for tile_key in list(tiles.keys()):
            tiles[tile_key] = []
    excluded_groups = {g.strip() for g in args.exclude_groups.split(",") if g.strip()}
    for tile_key in list(tiles.keys()):
        kept = []
        for obj in tiles[tile_key]:
            cls = h3m_class_of(obj)
            if obj.get("group") in excluded_groups or cls in excluded:
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

    if args.hero_def_doc or args.hero_def_name:
        import struct
        obj_hex = map_data["Objects"]["Raw Data"]
        raw = bytes.fromhex(obj_hex)
        n = struct.unpack("<I", raw[:4])[0]
        out = bytearray(raw[:4])
        off = 4
        renamed = []
        for _ in range(n):
            nl = struct.unpack("<i", raw[off:off + 4])[0]
            name = raw[off + 4:off + 4 + nl].decode("latin1")
            body = raw[off + 4 + nl:off + 4 + nl + 42]
            cls, sub = struct.unpack("<II", body[16:24])
            if cls == 34:
                if args.hero_def_name:
                    new_name = args.hero_def_name.encode("latin1")
                else:
                    new_name = ("AH0%02d00.DEF" % sub).encode("latin1")
                renamed.append((name, new_name.decode()))
                out += struct.pack("<i", len(new_name)) + new_name + body
            else:
                out += raw[off:off + 4 + nl + 42]
            off += 4 + nl + 42
        out += raw[off:]
        map_data["Objects"]["Raw Data"] = out.hex()
        print(f"Defs classe 34 renommées: {renamed}")

    out_path = os.path.join("output", f"{args.map_name}_{suffix}.h3m")
    write_h3m(map_data, out_path)

    print(f"Objets retirés ({len(removed)}):")
    for tile_key, obj_id, group, index, cls in removed:
        print(f"  tile={tile_key} id={obj_id} group={group} index={index} -> h3m class {cls}")
    print(f"Variante écrite dans {out_path}")


if __name__ == "__main__":
    main()
