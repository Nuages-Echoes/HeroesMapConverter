import json
import os
import tempfile

from h3decoder import parse_h3m, write_h3m

INPUT_DIR = "input"
OUTPUT_DIR = "output"

SKIP_DISPLAY_KEYS = {"Surface Map", "Underground Map", "Objects"}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(prefix="h3m_json_")

    h3m_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".h3m")]

    if not h3m_files:
        print(f"Aucun fichier .h3m trouvé dans le dossier '{INPUT_DIR}'.")
        return

    for file_name in h3m_files:
        h3m_file_path = os.path.join(INPUT_DIR, file_name)
        print(f"\n=== Conversion de '{file_name}' ===")

        try:
            # Étape 1 : lecture de la carte et écriture du JSON dans le dossier temporaire
            result = parse_h3m(h3m_file_path)

            base_name = os.path.splitext(file_name)[0]
            json_file_path = os.path.join(temp_dir, f"{base_name}.json")
            with open(json_file_path, "w", encoding="utf-8") as json_file:
                json.dump(result, json_file, indent=4, ensure_ascii=False)
            print(f"JSON écrit dans '{json_file_path}'")

            # Étape 2 : lecture du JSON et écriture du .h3m dans le dossier output
            with open(json_file_path, "r", encoding="utf-8") as json_file:
                map_data = json.load(json_file)

            h3m_output_path = os.path.join(OUTPUT_DIR, f"{base_name}.h3m")
            write_h3m(map_data, h3m_output_path)
        except Exception as e:
            print(f"Erreur lors de la conversion de '{file_name}': {e}")
            continue


if __name__ == "__main__":
    main()
