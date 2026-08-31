from h3decoder import parse_h3m
import json

def main():
    # Chemin vers le fichier H3M à parser
    h3m_file_path = "all for one.h3m"  # Remplacez par le chemin de votre fichier H3M

    # Parser le fichier H3M
    result = parse_h3m(h3m_file_path)

    # Afficher les résultats sous forme lisible
    print("=== Informations de base ===")
    for key, value in result.items():
        if key != "Players" and key != "Terrain" and key != "Objects":
            print(f"{key}: {value}")

    print("\n=== Attributs des joueurs ===")
    for player in result["Players"]:
        print(f"\nJoueur: {player['Color']}")
        for attr, val in player.items():
            print(f"  {attr}: {val}")

    # Optionnel : Enregistrer les résultats dans un fichier JSON
    with open("h3m_data.json", "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=4, ensure_ascii=False)

    print("\nLes données ont été enregistrées dans 'h3m_data.json'.")

if __name__ == "__main__":
    main()