# progress.md — Work done on HeroesMapConverter

This document describes the work accomplished so far. For the current
inputs/outputs and pipeline layout, see [Progress.md](Progress.md); for usage,
see [README.md](README.md).

## Goal

Command-line tool (Python 3.12, standard library only, no UI) that converts
maps between Heroes of Might and Magic games. First target: Heroes II /
fheroes2 (Olden Era, `.fh2m` / `.mp2`) and Heroes III (`.h3m`). The design
routes every conversion through a common **unified JSON** format, so a map
from any supported game can be converted to any other without writing a
direct converter for every pair of formats.

## 1. H3 → JSON (and back)

- `h3decoder.py` implements `parse_h3m()`: reads gzip-compressed `.h3m`
  files and recognizes the RoE (`0x0E`), AB (`0x15`) and SoD (`0x1C`)
  header variants with version-aware parsing.
- `write_h3m()` serializes the parsed structure back to a valid `.h3m`
  (lossless round-trip; generated fh2m→h3m conversions are emitted as
  RoE/AB/SoD variants matching the source).
- Each `.h3m` in `input/` is decoded to a detailed, source-faithful JSON in
  `outputjson/<name>.json`, documented in `h3m_description.english.txt`
  (binary format) and `h3m_json_description.english.txt` (JSON schema).

## 2. H2 → JSON (and back)

- `h2decoder.py` implements `parse_fh2m()` for fheroes2 / Olden Era maps:
  magic `h2map\0`, big-endian integers, format versions 2–13, plain base
  parameters followed by a single zlib-compressed section. `.mp2` files
  are recognized as Heroes II maps too.
- `write_fh2m()` writes the structure back to `.fh2m`.
- Each H2 map in `input/` is decoded to a detailed JSON in
  `outputjson/<name>.json`, documented in `h2m_description.english.txt` and
  `h2m_json_description.english.txt`.

## 3. Detailed JSON → unified JSON

- `unified.py` provides `convert_to_unified()` with
  `convert_h3m_to_unified()` and `convert_fh2m_to_unified()`, normalizing a
  detailed JSON into the common schema written to
  `outputunified/<name>.json`. The schema is documented in
  `heroes_json_description.english.txt`, with a concrete example in
  `example_unified.json`.
- Game-specific identifiers (towns, monsters, artifacts, spells, heroes,
  landscape objects, terrains…) are translated through the correspondence
  tables in `correspondence.py`, documented field by field in
  `heroes_field_correspondence.english.txt`.
- Parsers stay lossless: raw source IDs/fields are kept in the unified JSON
  so the target writers can rebuild the exact original structure, and anchor
  shifts between the H2 and H3 conventions are carried explicitly
  (`anchorShift`) so each writer restores its own anchor placement.

## 4. Unified JSON → H2 or H3

- `convert_from_unified()` (`unified_to_h3m()` / `unified_to_fh2m()`)
  rebuilds a game-specific structure from the unified JSON, then
  `write_h3m()` / `write_fh2m()` serialize the binaries into `output/`.
- By default every input map is converted to **both** `.h3m` and `.fh2m`;
  `--target h3m|fh2m` restricts the output to a single format
  (`main.py` orchestrates the whole pipeline).

```
input/*.{h3m,fh2m,mp2}
   → outputjson/<name>.json     (detailed JSON, faithful to the source format)
   → outputunified/<name>.json  (unified JSON, common to both games)
   → output/<name>.h3m + output/<name>.fh2m   (regenerated/converted maps)
```

## 5. Content conversion work (H2 ↔ H3 fidelity)

Beyond the pipeline skeleton, most of the effort went into making the
converted maps actually match the target game:

- **Terrains, coasts, rivers, roads**: per-terrain picture layouts, coast
  bits and mirror flags, sea-border sprites computed from the tile
  neighborhood, and H2→H3 sprite selection driven by learned link tables
  (`coastal_link.json`, `road_link.json`, `river_link.json`, documented in
  `coastal_tiles_h2_h3.md`), including H2 diagonal roads → editor-style H3
  bends and road-end stubs, and land–land terrain borders.
- **Landscape objects**: footprint-exact, terrain-faithful conversion of
  trees (incl. forests, lava/dead/snow variants), mountains, rocks, misc
  and water objects; unconvertible objects are fanned out into
  same-terrain H3 defs or dropped when no counterpart exists.
- **Towns, dwellings, altars**: real H3 def names per dwelling/altar, town
  entrance alignment (+2,0 shift), random town as class 77, starting
  conditions (player colors, castle owners, main town, available heroes).
- **Heroes**: starting heroes, prisons ↔ jail, hero classes/sprites/def
  names matching the real game archives, generated missing starting heroes
  for h3m sources.
- **Monsters and artifacts**: fixed and random monsters, fixed artifacts,
  random artifact classes (incl. the h3m 65–69 ↔ fh2m 91–95 mapping), and
  unmapped artifacts falling back to a random artifact of the same class.
- **Ownables and interactive objects**: mines (per-appearance defs),
  windmills, witch huts, alchemist labs, mercenary camps, obelisks,
  observation towers, gazebo, boats, teleportation portals, border gates
  (barrier), keymaster's tent (traveller's tent), magic well, wagon,
  summoning altars, power-ups, signs, resources, and more.
- **Victory/defeat conditions**: H2 conditions mapped to H3 equivalents
  (e.g. defeatOtherSide → None, ultimate artifact → buildGrail).

## 6. Verification

- `verify_roundtrip.py` checks every `input/` map against its regenerated
  `output/` file of the same extension: byte-perfect equality for h3m
  (gunzipped content), and content-level equality for fh2m (decompressed
  zlib section), plus equality of the parsed structures. Must exit 0.
- `make_variant.py` generates `.h3m` variants of a converted map (e.g.
  without a class of objects) from `outputunified/` to isolate load issues.
- CI was intentionally removed; verification is manual:
  `python main.py` then `python verify_roundtrip.py`.

## 7. Known limitations

- H3 maps with an underground level cannot be converted to H2 (no
  underground in H2): the conversion fails on purpose.
- Neutral heroes from H3 disappear in H2 output (no neutral heroes in H2).

## Reference maps

`input/` holds the reference maps used for development and verification:
`all for one.h3m` (H3) plus `4_dimensions.fh2m`, `5Kings1Ring.fh2m`,
`Barbarian vs Wizard.fh2m`, `Full Backpack.fh2m`, `Mymaptest.fh2m` and
`Tetra_conflict.fh2m` (H2).
