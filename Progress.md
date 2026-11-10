# Progress.md — Fonctionnement actuel de HeroesMapConverter

Document décrivant l'état actuel du projet (branche `main`, commit `0c157e3`) :
quelles sont les entrées, les sorties, et ce qui se passe entre les deux.

## Objectif

Outil en ligne de commande (Python, sans UI) qui convertit des cartes entre
jeux *Heroes of Might and Magic*. Le passage par un format JSON unifié doit
permettre à terme de convertir n'importe quel format vers n'importe quel autre
(premier objectif : Olden Era / fheroes2, puis d'autres jeux Heroes).

## Entrées

`main.py` scanne le dossier `input/` et traite tout fichier dont l'extension
est `.h3m`, `.fh2m` ou `.mp2` (par ordre alphabétique). Deux formats binaires
sont supportés :

- **H3M (Heroes III)** — fichier gzip ; les variantes d'en-tête RoE (`0x0E`),
  AB (`0x15`) et SoD (`0x1C`) sont reconnues. Parsing : `h3decoder.parse_h3m()`.
- **FH2M / MP2 (fheroes2, Heroes II / Olden Era)** — magic `h2map\0`, versions
  de format 2 à 13 ; entiers en big-endian ; paramètres de base en clair, puis
  une unique section compressée zlib. Parsing : `h2decoder.parse_fh2m()`.

Cartes de test embarquées dans `input/` : 4 cartes `.h3m` (`all for one`,
`ascension`, `divided loyalties`, `free for all`) et 4 cartes H2
(`BROKENA.MP2`, `Good,_Bad,_Magne.fh2m`, `My map.fh2m`, `Tetra_conflict.fh2m`).

## Fonctionnement entre les deux (pipeline)

Pour chaque fichier de `input/`, `main.py` applique trois étapes :

1. **Binaire → JSON détaillé.** `parse_h3m()` ou `parse_fh2m()` produit un
   dictionnaire fidèle au format source, écrit dans `outputjson/<nom>.json`.
   Les schémas de ces JSON sont documentés dans `h3m_json_description.english.txt`
   et `h2m_json_description.english.txt` (les formats binaires eux-mêmes dans
   `h3m_description.english.txt` et `h2m_description.english.txt`).
2. **JSON détaillé → JSON unifié.** `unified.convert_to_unified()` normalise la
   carte vers un schéma commun (`convert_h3m_to_unified()` /
   `convert_fh2m_to_unified()`), écrit dans `outputunified/<nom>.json`. Schéma
   documenté dans `heroes_json_description.english.txt`, exemple dans
   `example_unified.json`. Les identifiants spécifiques à chaque jeu (monstres,
   artefacts, sorts, héros, villes, mines, objets de paysage…) sont traduits
   via les tables de `correspondence.py`, dont les équivalences sont listées
   dans `heroes_field_correspondence.english.txt`.
3. **JSON unifié → formats cibles.** Le JSON unifié est relu, puis
   `convert_from_unified()` le retransforme en structure propre à chaque jeu
   (`unified_to_h3m()` / `unified_to_fh2m()`) et `write_h3m()` / `write_fh2m()`
   sérialisent le binaire dans `output/`. Par défaut, chaque carte est produite
   dans **les deux** formats (`<nom>.h3m` et `<nom>.fh2m`) ; l'option
   `--target h3m|fh2m` restreint la conversion à une seule cible.

En résumé :

```
input/*.{h3m,fh2m,mp2}
   → outputjson/<nom>.json     (JSON détaillé, fidèle au format source)
   → outputunified/<nom>.json  (JSON unifié, commun aux deux jeux)
   → output/<nom>.h3m + output/<nom>.fh2m   (cartes régénérées/converties)
```

## Sorties

- `outputjson/<nom>.json` — représentation détaillée du fichier source
  (dossier créé à l'exécution, non versionné).
- `outputunified/<nom>.json` — format unifié commun (idem).
- `output/<nom>.h3m` et `output/<nom>.fh2m` — cartes produites dans les deux
  formats, versionnées et utilisées comme référence de vérification.

## Vérification

- CI (`.github/workflows/ci.yml`) : `python -m compileall` sur les modules,
  `python main.py`, contrôle de la présence de chaque JSON dans `outputjson/`,
  puis `python verify_roundtrip.py`.
- `verify_roundtrip.py` : pour chaque carte, compare `parse(input)` et
  `parse(output)` de la même extension — égalité binaire quand c'est possible,
  sinon égalité du contenu logique (section zlib décompressée pour fh2m,
  contenu gzip décompressé pour h3m) et des structures parsées.
- `make_variant.py` : outil de test qui génère des variantes `.h3m` d'une carte
  convertie (ex. suppression de classes d'objets) à partir de
  `outputunified/<nom>.json`, pour isoler des problèmes de chargement.

## Points de fonctionnement notables

- Conversion fh2m → h3m des tuiles côtières : calcul des sprites de bordure de
  mer selon l'orientation des voisins (bit de côte + flags miroir), inventorié
  dans `coastal_tiles_h2_h3.md` avec les planches SVG de `coastal_h2/`.
- Pour les sources fh2m, la ville principale d'un joueur est pointée sur la
  case d'entrée de la ville.
- Limites connues (README) : une carte H3 avec souterrain ne peut pas être
  convertie en H2 (pas de souterrain en H2) ; les héros neutres H3 disparaissent
  dans les cartes H2.

## Organisation du code

| Fichier | Rôle |
|---|---|
| `main.py` | CLI et orchestration du pipeline (input → outputjson → outputunified → output) |
| `h2decoder.py` | lecture/écriture binaire `.fh2m` / `.mp2` (big-endian, zlib) |
| `h3decoder.py` | lecture/écriture binaire `.h3m` (gzip, RoE/AB/SoD) |
| `unified.py` | conversions vers/depuis le JSON unifié |
| `correspondence.py` | tables de correspondance H2 ↔ H3 (ID et noms) |
| `verify_roundtrip.py` | vérification aller-retour parse → convert → write → parse |
| `make_variant.py` | génération de variantes de test |
| `*_description.english.txt`, `heroes_field_correspondence.english.txt` | spécifications des formats binaires, des JSON et des équivalences de valeurs |
| `coastal_tiles_h2_h3.md`, `coastal_h2/` | inventaire des tuiles côtières H2/H3 |
