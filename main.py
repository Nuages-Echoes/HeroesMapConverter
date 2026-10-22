import json
import os

from h2decoder import parse_fh2m
from h3decoder import parse_h3m, write_h3m

INPUT_DIR = "input"
OUTPUT_DIR = "output"
OUTPUT_JSON_DIR = "outputjson"

SKIP_DISPLAY_KEYS = {"Surface Map", "Underground Map", "Objects"}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)

    map_files = sorted(f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".h3m", ".fh2m")))

    if not map_files:
        print(f"Aucun fichier .h3m ou .fh2m trouvé dans le dossier '{INPUT_DIR}'.")
        return

    for file_name in map_files:
        map_file_path = os.path.join(INPUT_DIR, file_name)
        print(f"\n=== Conversion de '{file_name}' ===")

        try:
            # Étape 1 : lecture de la carte et écriture du JSON dans le dossier outputjson
            if file_name.lower().endswith(".fh2m"):
                result = parse_fh2m(map_file_path)
            else:
                result = parse_h3m(map_file_path)

            base_name = os.path.splitext(file_name)[0]
            json_file_path = os.path.join(OUTPUT_JSON_DIR, f"{base_name}.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, indent=4, ensure_ascii=False)
            print(f"JSON écrit dans '{json_file_path}'")

            # Étape 2 : lecture du JSON et écriture du .h3m dans le dossier output
            # (uniquement pour les cartes Heroes III, il n'y a pas encore d'écrivain .fh2m)
            if file_name.lower().endswith(".h3m"):
                with open(json_file_path, "r", encoding="utf-8") as json_file:
                    map_data = json.load(json_file)

                h3m_output_path = os.path.join(OUTPUT_DIR, f"{base_name}.h3m")
                write_h3m(map_data, h3m_output_path)
        except Exception as e:
            print(f"Erreur lors de la conversion de '{file_name}': {e}")
            continue


if __name__ == "__main__":
    main()
