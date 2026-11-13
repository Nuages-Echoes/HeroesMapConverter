# HeroesMapConverter
Tool used to convert maps from different Heroes of Might and Magic. Objective first is to be able to convert maps to Olden Era, and then to other Horeos games.

To parse H3 files, I used the description found here 
https://github.com/HeroWO-js/h3m2json/blob/master/references/h3m_description.english.txt

I decided to not reuse the project directly as I intend to use python and not php.
Also, I am also using this project as test for vibe coding, so bug may abound.

How it works :
- the project reads the files in the `input/` directory (`.h3m`, `.fh2m`, `.mp2`)
- each file is parsed to a detailed JSON stored in the `outputjson/` directory
- the detailed JSON is converted to a common unified JSON stored in the `outputunified/` directory
- the unified JSON is then converted to each target format and written to the `output/` directory (both `.h3m` and `.fh2m` by default; use `--target h3m|fh2m` to pick a single one)

Why all the bother ?
Because by using the unified JSON format, a map from any supported Heroes game can be converted to any other through the common JSON file, instead of writing a direct converter for every pair of formats (heroesX -> heroesY).

## Usage

```bash
python main.py                  # convert every map in input/ to both .h3m and .fh2m
python main.py --target fh2m    # convert only to fheroes2 (.fh2m) maps
python verify_roundtrip.py      # check that each output/ file round-trips with its input/
```

See [Progress.md](Progress.md) for a description of the current inputs, outputs and pipeline, and the `*_description.english.txt` files for the binary and JSON format specifications.

Can I help ?
Yes you can, it's a pet project feel free to modify or clone it. Just don't sell it or make money out of it.

No UI ?
No, not yet. I'd like to make it work first and then think about UI. Also, I don't much about UI so it's harder for me to review or correct UI related bugs. Even if the project is vibe coded (because honestly setting up the parsing sucks) doesn't mean I don't look at it and modify it by hand.

Known Limitations
Converting maps with subterranean map to H2 ends in failure (no underground in H2)
Neutral heroes from H3 disappear in H2 maps (no neutral heroes in the game)
More info on limitations in the `*_description.english.txt` files.
