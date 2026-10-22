import json
import os

from h3decoder import parse_h3m

INPUT_DIR = "input"
OUTPUT_DIR = "output"

SKIP_DISPLAY_KEYS = {"Surface Map", "Underground Map", "Objects"}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    h3m_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".h3m")]

    if not h3m_files:
        print(f"Aucun fichier .h3m trouvé dans le dossier '{INPUT_DIR}'.")
        return

    for file_name in h3m_files:
        h3m_file_path = os.path.join(INPUT_DIR, file_name)
        print(f"\n=== Conversion de '{file_name}' ===")

        try:
            result = parse_h3m(h3m_file_path)
        except Exception as e:
            print(f"Erreur lors de la conversion de '{file_name}': {e}")
            continue

        # Afficher les résultats sous forme lisible
        print("--- Informations de base ---")
        for key, value in result.items():
            if key not in SKIP_DISPLAY_KEYS:
                print(f"{key}: {value}")

        print("\n--- Attributs des joueurs ---")
        for player in result["Players Attributes"]["Players"]:
            print(f"\nJoueur: {player['Color']}")
            for attr, val in player.items():
                print(f"  {attr}: {val}")

        # Enregistrer les résultats dans un fichier JSON
        base_name = os.path.splitext(file_name)[0]
        json_file_path = os.path.join(OUTPUT_DIR, f"{base_name}.json")
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(result, json_file, indent=4, ensure_ascii=False)

        print(f"\nLes données ont été enregistrées dans '{json_file_path}'.")


if __name__ == "__main__":
    main()
