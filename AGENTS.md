# AGENTS.md — Rules for AI agents working on HeroesMapConverter

Instructions for AI coding agents (Codex, Copilot, Cursor, Claude Code, Vibe, …).
Any tool that supports the [agents.md](https://agents.md) convention picks this
file up automatically from the repo root. Follow these rules unless the user
explicitly overrides one.

## Project overview

- Python 3.12, **standard library only** (no `pip install`): `struct`, `zlib`,
  `gzip`, `json`, `argparse`, `os`.
- CLI tool, **no UI**. It converts Heroes of Might and Magic maps between
  `.h3m` (Heroes III — gzip, headers RoE `0x0E` / AB `0x15` / SoD `0x1C`) and
  `.fh2m` / `.mp2` (fheroes2 — magic `h2map\0`, big-endian,
  format versions 2–13, zlib-compressed tail) and `.map` (Heroes of
  Might and Magic: Olden Era — a single gzip stream of varint-framed
  JSON blocks, read/written by `hommoedecoder.py`), through an
  intermediate unified JSON.
- Pipeline (`main.py`): `input/` → `outputjson/<name>.json` (detailed JSON,
  faithful to the source format) → `outputunified/<name>.json` (unified JSON)
  → `output/<name>.h3m`, `output/<name>.fh2m` **and** `output/<name>.map`.
  `--target h3m|fh2m|map` restricts the conversion to one format. `.map`
  (Olden Era) inputs are parsed to `outputjson/`, converted to
  `outputunified/` (`convert_hommoe_to_unified`) and regenerated to
  `output/<name>.map` from the detailed JSON; H2/H3 inputs are converted to
  `.map` via `unified_to_hommoe()` (H2/H3 events become OE quest triggers).
- Read `README.md` and `Progress.md` first. Binary/JSON format specs live in
  the `*_description.english.txt` files; ID correspondences between the two
  games live in `correspondence.py` (documented in
  `heroes_field_correspondence.english.txt`).

## Golden rule: keep the round-trip faithful

After any code change, run:

```bash
python main.py               # regenerate outputjson/, outputunified/, output/
python verify_roundtrip.py   # MUST exit 0: parse(input) == parse(output) per map
```

Never break `verify_roundtrip.py`. Binary equality is ideal; at minimum the
logical content must match (decompressed zlib section for `.fh2m`, gunzipped
content for `.h3m`).

## Workflow

- Commit messages: conventional style, short, English — `fix:`, `docs:`,
  `test:`, `chore:`, `feat:`.
- One logical change per commit.
- use files in input directory for tests and checks. If information or cases are 
  missing, inform user.
- Unless specified otherwise, merge directly into main and do not create branch
- when working on object placement, prioritize footprint over anchor tile

## Map-object terminology

When discussing object placement, use these terms consistently:

- **Anchor tile** (or **object position**): the single coordinate stored in
  the map file that identifies where the whole item sits (h3m object
  `x,y,z`; fh2m tile the object is attached to).
- **Footprint**: the full set of tiles the item occupies/blocks
  (impassable). In h3m this is the 6-byte passability mask relative to the
  anchor; in fh2m it is implicit in the object definition.
- **Activation tiles** (or **interaction tiles**): the 1-2 visitable tiles
  where a hero triggers the object (enter a mine, pick up a resource,
  read a sign). In h3m this is the actionability/visitable mask; in fh2m
  it is the object's action cell(s).

The conversion translates only the anchor. For fh2m sources the
  fh2m -> unified step applies the anchor shifts (the unified JSON stores
  h3m-convention anchors plus an `anchorShift` field per shifted object);
  the h3m writer places instances at the unified positions as-is and the
  fh2m writer restores the original anchors with the stored shift.
  Footprints and activation tiles are implicit per game, so an anchor
  mismatch shifts the footprint and the activation tiles together.

## Code conventions

- Keep parsers **lossless**: when normalizing to the unified format, retain the
  raw source IDs/fields so `write_h3m` / `write_fh2m` can rebuild the exact
  original structure.
- New binary fields must follow the existing version gates in `h2decoder.py`
  (fh2m versions 2–13) and `h3decoder.py` (RoE / AB / SoD variants).
- Code identifiers and commit messages in English; user-facing docs may be in
  French.
- `input/` holds the test maps; `output/` holds the regenerated reference
  maps. `make_variant.py` builds debug variants from `outputunified/` to
  isolate load crashes — prefer it over hand-editing maps.

## Known limitations — do not "fix" silently

- H3 maps with an underground level **cannot** be converted to H2 (no
  underground in H2): the conversion fails on purpose.
- Neutral heroes from H3 disappear in H2 output (no neutral heroes in H2).

## House rules

- Pet project: never add monetization, telemetry, or phone-home code.
- The CI workflow was intentionally removed — verification is manual
  (`python verify_roundtrip.py`).
