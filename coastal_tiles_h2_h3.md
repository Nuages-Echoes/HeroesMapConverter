# Table d'équivalence des tuiles côtières H2 (fh2m) -> H3 (h3m)

Générée depuis `input/My map.fh2m` -> `output/My map.h3m` (île simple).

- `fh2m index` = terrainIndex brut dans le fh2m ; `offset` = index dans la plage du terrain.
- `flags` = terrainFlags fh2m (bits miroir H/V).
- `masque voisins` = directions (N,NE,E,SE,S,SW,W,NW) des voisins **de l'autre** côté : terre pour les tuiles eau, eau pour les tuiles terre.
- `h3m picture`/`mirroring` = ce que produit actuellement le convertisseur.

| côté | fh2m terrain | fh2m index | offset | flags | masque voisins | nb | h3m type | h3m picture | h3m mirroring | ex (x,y) |
|---|---|---|---|---|---|---|---|---|---|---|
| Beach | Beach | 415 | 0 | 0 | NEESE/NNEESENW/NNENW/NNEWNW/SE/SW | 9 | Sand | 0 | 0x40 | 15,2 |
| Beach | Beach | 416 | 1 | 0 | NEESE/NNENW/NNEWNW/SESSW/SW | 7 | Sand | 1 | 0x40 | 12,2 |
| Beach | Beach | 417 | 2 | 0 | ESESSW/NE/NNEESENW/NNENW/SESSWW/SWWNW | 10 | Sand | 2 | 0x40 | 13,2 |
| Beach | Beach | 418 | 3 | 0 | NEESE/NNENW/SSW | 3 | Sand | 3 | 0x40 | 21,2 |
| Beach | Beach | 419 | 4 | 0 | ESESSW/NEESES/NEESESSW/NNW/SES/SESSW | 7 | Sand | 4 | 0x40 | 11,3 |
| Beach | Beach | 420 | 5 | 0 | NNE/NNENW/NW/SESSW/SWW/SWWNW | 7 | Sand | 5 | 0x40 | 20,2 |
| Beach | Beach | 421 | 6 | 0 | NEESE/NNENW/SES/SESSWWNW/SW/SWWNW | 8 | Sand | 6 | 0x40 | 16,2 |
| Beach | Beach | 422 | 7 | 0 | ESE/NEESE/NNW/SE/SSWWNW | 5 | Sand | 7 | 0x40 | 9,4 |
| Beach | Beach | 423 | 8 | 0 | NEESE | 1 | Sand | 8 | 0x40 | 24,3 |
| Beach | Beach | 424 | 9 | 0 | SESSW | 1 | Sand | 9 | 0x40 | 20,16 |
| Beach | Beach | 425 | 10 | 0 | NW | 1 | Sand | 10 | 0x40 | 10,4 |
| Beach | Beach | 426 | 11 | 0 | NEE/SESSW | 2 | Sand | 11 | 0x40 | 24,10 |
| Beach | Beach | 427 | 12 | 0 | NNENW/SESSW | 2 | Sand | 12 | 0x40 | 23,2 |
| Beach | Beach | 428 | 13 | 0 | NNENW | 1 | Sand | 13 | 0x40 | 17,2 |
| Beach | Beach | 430 | 15 | 0 | NNESWWNW | 1 | Sand | 15 | 0x40 | 8,4 |
| Beach | Beach | 431 | 16 | 0 | SESSW | 1 | Sand | 16 | 0x40 | 17,16 |
| WATER | WATER | 0 | 0 | 0 | NNE | 1 | Water | 8 | 0x00 | 10,16 |
| WATER | WATER | 0 | 0 | 1 | SES | 1 | Water | 9 | 0x01 | 8,3 |
| WATER | WATER | 1 | 1 | 0 | NNENW | 2 | Water | 8 | 0x00 | 17,17 |
| WATER | WATER | 1 | 1 | 1 | SES/SESSW/SSW | 7 | Water | 9 | 0x01 | 12,1 |
| WATER | WATER | 2 | 2 | 0 | NNENW/NNW | 6 | Water | 8 | 0x00 | 24,16 |
| WATER | WATER | 2 | 2 | 1 | SES/SESSW | 4 | Water | 9 | 0x01 | 17,1 |
| WATER | WATER | 3 | 3 | 0 | NNE/NNENW/NNW | 4 | Water | 8 | 0x00 | 23,16 |
| WATER | WATER | 3 | 3 | 1 | SESSW/SSW | 4 | Water | 9 | 0x01 | 13,1 |
| WATER | WATER | 4 | 4 | 0 | NNEESENW | 1 | Water | 16 | 0x00 | 11,16 |
| WATER | WATER | 4 | 4 | 1 | ESESSW | 1 | Water | 17 | 0x01 | 9,3 |
| WATER | WATER | 5 | 5 | 0 | NNEESE | 1 | Water | 16 | 0x00 | 8,7 |
| WATER | WATER | 5 | 5 | 2 | NNEWNW | 1 | Water | 16 | 0x02 | 22,16 |
| WATER | WATER | 6 | 6 | 0 | NNEE | 1 | Water | 16 | 0x00 | 9,15 |
| WATER | WATER | 6 | 6 | 2 | NNEWNW | 1 | Water | 16 | 0x02 | 16,17 |
| WATER | WATER | 7 | 7 | 1 | ESESSW | 1 | Water | 17 | 0x01 | 11,2 |
| WATER | WATER | 7 | 7 | 2 | NSWWNW | 1 | Water | 16 | 0x02 | 26,13 |
| WATER | WATER | 7 | 7 | 3 | SESSWWNW | 1 | Water | 17 | 0x03 | 25,10 |
| WATER | WATER | 8 | 8 | 0 | NEE/NEESE | 3 | Water | 4 | 0x00 | 8,10 |
| WATER | WATER | 8 | 8 | 2 | SWW/SWWNW | 5 | Water | 4 | 0x02 | 25,2 |
| WATER | WATER | 9 | 9 | 0 | NEE/NEESE | 2 | Water | 4 | 0x00 | 7,5 |
| WATER | WATER | 9 | 9 | 2 | SWWNW/WNW | 2 | Water | 4 | 0x02 | 25,8 |
| WATER | WATER | 10 | 10 | 0 | ESE/NEESE | 3 | Water | 4 | 0x00 | 7,4 |
| WATER | WATER | 10 | 10 | 2 | SWWNW | 2 | Water | 4 | 0x02 | 25,7 |
| WATER | WATER | 11 | 11 | 0 | NEE/NEESE | 3 | Water | 4 | 0x00 | 8,8 |
| WATER | WATER | 11 | 11 | 2 | SWW/SWWNW/WNW | 3 | Water | 4 | 0x02 | 25,6 |
| WATER | WATER | 12 | 12 | 1 | SE | 2 | Water | 19 | 0x01 | 9,2 |
| WATER | WATER | 13 | 13 | 0 | NE | 1 | Water | 18 | 0x00 | 9,16 |
| WATER | WATER | 13 | 13 | 2 | NW | 2 | Water | 18 | 0x02 | 27,13 |
| WATER | WATER | 14 | 14 | 0 | NE | 3 | Water | 18 | 0x00 | 7,7 |
| WATER | WATER | 14 | 14 | 3 | SW | 1 | Water | 19 | 0x03 | 25,1 |
| WATER | WATER | 15 | 15 | 1 | SE | 1 | Water | 19 | 0x01 | 11,1 |
| WATER | WATER | 15 | 15 | 2 | NW | 2 | Water | 18 | 0x02 | 22,17 |
| WATER | WATER | 15 | 15 | 3 | SW | 1 | Water | 19 | 0x03 | 27,10 |
