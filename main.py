import argparse
import json
import os

from h2decoder import parse_fh2m, write_fh2m
from h3decoder import parse_h3m, write_h3m
import shutil

from hommoedecoder import parse_hommoe, write_hommoe, write_hommoe_sidecar
from unified import convert_to_unified, convert_from_unified

INPUT_DIR = "input"
OUTPUT_DIR = "output"
OUTPUT_JSON_DIR = "outputjson"
OUTPUT_UNIFIED_DIR = "outputunified"

SKIP_DISPLAY_KEYS = {"Surface Map", "Underground Map", "Objects"}

H2_EXTENSIONS = (".fh2m", ".mp2")
OE_EXTENSIONS = (".map",)
MAP_EXTENSIONS = (".h3m",) + H2_EXTENSIONS + OE_EXTENSIONS


def write_target(unified_data, target_game, base_name):
    """Convertit le JSON unifié vers le format cible et écrit le fichier.

    Retourne le chemin du fichier écrit, ou None avec un message
    d'erreur affiché.
    """
    map_data = convert_from_unified(unified_data, target_game)

    if target_game == "fh2m":
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.fh2m")
        write_fh2m(map_data, output_path)
        print(f"FH2M file written to {output_path}")
    elif target_game == "hommoe":
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.map")
        write_hommoe(map_data, output_path)
        print(f"HOMMOE file written to {output_path}")
        sidecar = write_hommoe_sidecar(map_data, output_path)
        if sidecar:
            print(f"HOMMOE sidecar written to {sidecar}")
    else:
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.h3m")
        write_h3m(map_data, output_path)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convertit les cartes Heroes vers le format unifié puis vers tous les formats cibles.")
    parser.add_argument("--target", choices=["h3m", "fh2m"], default=None,
                        help="Format cible unique de la conversion. Par défaut, "
                             "toutes les cartes sont converties vers les deux formats (H2 et H3).")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
    os.makedirs(OUTPUT_UNIFIED_DIR, exist_ok=True)

    map_files = sorted(f for f in os.listdir(INPUT_DIR) if f.lower().endswith(MAP_EXTENSIONS))

    if not map_files:
        print(f"Aucun fichier .h3m, .fh2m, .mp2 ou .map trouvé dans le dossier '{INPUT_DIR}'.")
        return

    for file_name in map_files:
        map_file_path = os.path.join(INPUT_DIR, file_name)
        print(f"\n=== Conversion de '{file_name}' ===")

        try:
            # Étape 1 : lecture de la carte et écriture du JSON dans le dossier outputjson
            is_h2_map = file_name.lower().endswith(H2_EXTENSIONS)
            is_oe_map = file_name.lower().endswith(OE_EXTENSIONS)
            if is_h2_map:
                result = parse_fh2m(map_file_path)
            elif is_oe_map:
                result = parse_hommoe(map_file_path)
            else:
                result = parse_h3m(map_file_path)

            base_name = os.path.splitext(file_name)[0]
            json_file_path = os.path.join(OUTPUT_JSON_DIR, f"{base_name}.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, indent=4, ensure_ascii=False)
            print(f"JSON écrit dans '{json_file_path}'")

            if is_oe_map:
                # Olden Era (.map) maps go through the unified JSON like the
                # other formats; the binary output is still regenerated from
                # the detailed JSON (no unified -> hommoe writer yet).
                unified_result = convert_to_unified(result, "hommoe")
                unified_file_path = os.path.join(OUTPUT_UNIFIED_DIR, f"{base_name}.json")
                with open(unified_file_path, "w", encoding="utf-8") as json_file:
                    json.dump(unified_result, json_file, indent=4, ensure_ascii=False)
                print(f"JSON unifié écrit dans '{unified_file_path}'")
                output_path = os.path.join(OUTPUT_DIR, f"{base_name}.map")
                write_hommoe(result, output_path)
                # The scenario sidecar .json is the editor's own file, kept
                # verbatim when the input has one (the game ignores it; it
                # only needs to match the input byte-for-byte); otherwise
                # it is regenerated from block 4, when it has content.
                input_sidecar = os.path.splitext(map_file_path)[0] + ".json"
                output_sidecar = os.path.splitext(output_path)[0] + ".json"
                if os.path.exists(input_sidecar):
                    shutil.copyfile(input_sidecar, output_sidecar)
                    print(f"HOMMOE sidecar copied verbatim to {output_sidecar}")
                else:
                    sidecar = write_hommoe_sidecar(result, output_path)
                    if sidecar:
                        print(f"HOMMOE sidecar written to {sidecar}")
                print(f"HOMMOE file written to {output_path}")
                continue

            # Étape 1b : conversion au format unifié dans le dossier outputunified
            source_game = "fh2m" if is_h2_map else "h3m"
            unified_result = convert_to_unified(result, source_game)
            unified_file_path = os.path.join(OUTPUT_UNIFIED_DIR, f"{base_name}.json")
            with open(unified_file_path, "w", encoding="utf-8") as json_file:
                json.dump(unified_result, json_file, indent=4, ensure_ascii=False)
            print(f"JSON unifié écrit dans '{unified_file_path}'")

            # Étape 2 : lecture du JSON unifié et écriture des fichiers cibles
            with open(unified_file_path, "r", encoding="utf-8") as json_file:
                unified_data = json.load(json_file)

            if args.target is not None:
                targets = [{"map": "hommoe"}.get(args.target, args.target)]
            else:
                targets = ["h3m", "fh2m", "hommoe"]

            for target_game in targets:
                try:
                    write_target(unified_data, target_game, base_name)
                except Exception as e:
                    print(f"Erreur lors de la conversion de '{file_name}' "
                          f"vers {target_game.upper()}: {e}")
        except Exception as e:
            print(f"Erreur lors de la conversion de '{file_name}': {e}")
            continue


if __name__ == "__main__":
    main()
