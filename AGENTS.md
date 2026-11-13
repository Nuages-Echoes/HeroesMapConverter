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
  `.fh2m` / `.mp2` (fheroes2 / Olden Era — magic `h2map\0`, big-endian,
  format versions 2–13, zlib-compressed tail), through an intermediate
  unified JSON.
- Pipeline (`main.py`): `input/` → `outputjson/<name>.json` (detailed JSON,
  faithful to the source format) → `outputunified/<name>.json` (unified JSON)
  → `output/<name>.h3m` **and** `output/<name>.fh2m`. `--target h3m|fh2m`
  restricts the conversion to one format.
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

- Work on a `vibe/<short-slug>-6dc5ad` branch, push it, and open a **draft PR**.
  If a PR already exists for the task, update it in place by pushing to its
  exact head branch. Never force-push, never delete a PR branch.
- Push directly to `main` **only** when the owner explicitly asks for it.
- Commit messages: conventional style, short, English — `fix:`, `docs:`,
  `test:`, `chore:`, `feat:`.
- One logical change per commit.
- use files in input directory for tests and checks. If information or cases are 
  missing, inform user.

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
