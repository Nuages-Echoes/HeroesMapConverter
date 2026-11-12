# Tuiles côtières : inventaire H2 et H3

Deux tableaux pour établir le tableau de lien H2 -> H3 :
- **Tableau 1** : toutes les tuiles côtières H2 présentes dans `input/My map.fh2m` (île 36x36).
- **Tableau 2** : toutes les variantes de tuiles côtières H3 réellement utilisées dans les cartes de référence (`input/*.h3m`).

Masque voisins = directions (N,NE,E,SE,S,SW,W,NW) des voisins de l'autre côté de la côte : terre pour les tuiles eau, eau pour les tuiles terre.

## Tableau 1 — tuiles côtières H2 (fh2m), source `My map.fh2m`

`kind` et `masque` viennent de `coastal_h2/labels.csv` (étiquetage manuel, vérifié contre les données).

| id H2 | kind | fh2m terrain | fh2m index | offset | flags | masque (labels.csv) | autres masques observés | nb tuiles | ex (x,y) |
|---|---|---|---|---|---|---|---|---|---|
| H2-01 | SAND | Beach | 415 | 0 | 0 | N+NE+NW | NEESE / NNEESENW / NNEWNW / SE / SW / SWWNW | 9 | 15,2 |
| H2-02 | SAND | Beach | 416 | 1 | 0 | N+NE+W+NW | NEESE / NNENW / SESSW / SW | 7 | 12,2 |
| H2-03 | SAND | Beach | 417 | 2 | 0 | N+NE+NW | ESESSW / NE / NNEESENW / SESSWW / SWWNW | 10 | 13,2 |
| H2-04 | SAND | Beach | 418 | 3 | 0 | N+NE+NW | NEESE / SSW | 3 | 21,2 |
| H2-05 | SAND | Beach | 419 | 4 | 0 | N+NW | ESESSW / NEESES / NEESESSW / SES / SESSW / SSWWNW | 7 | 11,3 |
| H2-06 | SAND | Beach | 420 | 5 | 0 | N+NE+NW | NNE / NW / SESSW / SWW / SWWNW | 7 | 20,2 |
| H2-07 | SAND | Beach | 421 | 6 | 0 | N+NE+NW | NEESE / SES / SESSWWNW / SW / SWWNW | 8 | 16,2 |
| H2-08 | SAND | Beach | 422 | 7 | 0 | N+NW | ESE / NEESE / SE / SSWWNW | 5 | 9,4 |
| H2-09 | SAND | Beach | 423 | 8 | 0 | NE+E+SE | - | 1 | 24,3 |
| H2-10 | SAND | Beach | 424 | 9 | 0 | SE+S+SW | - | 1 | 20,16 |
| H2-11 | SAND | Beach | 425 | 10 | 0 | NW | - | 1 | 10,4 |
| H2-12 | SAND | Beach | 426 | 11 | 0 | NE+E | SESSW | 2 | 24,10 |
| H2-13 | SAND | Beach | 427 | 12 | 0 | N+NE+NW | SESSW | 2 | 23,2 |
| H2-14 | SAND | Beach | 428 | 13 | 0 | N+NE+NW | - | 1 | 17,2 |
| H2-15 | SAND | Beach | 430 | 15 | 0 | N+NE+SW+W+NW | - | 1 | 8,4 |
| H2-16 | SAND | Beach | 431 | 16 | 0 | SE+S+SW | - | 1 | 17,16 |
| H2-17 | WATER | Water | 0 | 0 | 0 | N+NE | - | 1 | 10,16 |
| H2-18 | WATER | Water | 0 | 0 | 1 | SE+S | - | 1 | 8,3 |
| H2-19 | WATER | Water | 1 | 1 | 0 | N+NE+NW | - | 2 | 17,17 |
| H2-20 | WATER | Water | 1 | 1 | 1 | SE+S | SESSW / SSW | 7 | 12,1 |
| H2-21 | WATER | Water | 2 | 2 | 0 | N+NE+NW | NNW | 6 | 24,16 |
| H2-22 | WATER | Water | 2 | 2 | 1 | SE+S+SW | SES | 4 | 17,1 |
| H2-23 | WATER | Water | 3 | 3 | 0 | N+NE+NW | NNE / NNW | 4 | 23,16 |
| H2-24 | WATER | Water | 3 | 3 | 1 | SE+S+SW | SSW | 4 | 13,1 |
| H2-25 | WATER | Water | 4 | 4 | 0 | N+NE+E+SE+NW | - | 1 | 11,16 |
| H2-26 | WATER | Water | 4 | 4 | 1 | E+SE+S+SW | - | 1 | 9,3 |
| H2-27 | WATER | Water | 5 | 5 | 0 | N+NE+E+SE | - | 1 | 8,7 |
| H2-28 | WATER | Water | 5 | 5 | 2 | N+NE+W+NW | - | 1 | 22,16 |
| H2-29 | WATER | Water | 6 | 6 | 0 | N+NE+E | - | 1 | 9,15 |
| H2-30 | WATER | Water | 6 | 6 | 2 | N+NE+W+NW | - | 1 | 16,17 |
| H2-31 | WATER | Water | 7 | 7 | 1 | E+SE+S+SW | - | 1 | 11,2 |
| H2-32 | WATER | Water | 7 | 7 | 2 | N+SW+W+NW | - | 1 | 26,13 |
| H2-33 | WATER | Water | 7 | 7 | 3 | SE+S+SW+W+NW | - | 1 | 25,10 |
| H2-34 | WATER | Water | 8 | 8 | 0 | NE+E+SE | NEE | 3 | 8,10 |
| H2-35 | WATER | Water | 8 | 8 | 2 | SW+W | SWWNW | 5 | 25,2 |
| H2-36 | WATER | Water | 9 | 9 | 0 | NE+E+SE | NEE | 2 | 7,5 |
| H2-37 | WATER | Water | 9 | 9 | 2 | SW+W+NW | WNW | 2 | 25,8 |
| H2-38 | WATER | Water | 10 | 10 | 0 | E+SE | NEESE | 3 | 7,4 |
| H2-39 | WATER | Water | 10 | 10 | 2 | SW+W+NW | - | 2 | 25,7 |
| H2-40 | WATER | Water | 11 | 11 | 0 | NE+E+SE | NEE | 3 | 8,8 |
| H2-41 | WATER | Water | 11 | 11 | 2 | SW+W+NW | SWW / WNW | 3 | 25,6 |
| H2-42 | WATER | Water | 12 | 12 | 1 | SE | - | 2 | 9,2 |
| H2-43 | WATER | Water | 13 | 13 | 0 | NE | - | 1 | 9,16 |
| H2-44 | WATER | Water | 13 | 13 | 2 | NW | - | 2 | 27,13 |
| H2-45 | WATER | Water | 14 | 14 | 0 | NE | - | 3 | 7,7 |
| H2-46 | WATER | Water | 14 | 14 | 3 | SW | - | 1 | 25,1 |
| H2-47 | WATER | Water | 15 | 15 | 1 | SE | - | 1 | 11,1 |
| H2-48 | WATER | Water | 15 | 15 | 2 | NW | - | 2 | 22,17 |
| H2-49 | WATER | Water | 15 | 15 | 3 | SW | - | 1 | 27,10 |

## Tableau 2 — tuiles côtières H3 (h3m), cartes de référence

| id H3 | h3m terrain | picture | mirrorings vus | masques voisins vus | nb tuiles | ex (carte, x,y) |
|---|---|---|---|---|---|---|
| H3-01 | Dirt | 1 | 0x42 | SSWWNW | 1 | all for one.h3m,22,42 |
| H3-02 | Dirt | 2 | 0x40 | NSWWNW | 1 | divided loyalties.h3m,63,13 |
| H3-03 | Dirt | 4 | 0x40 / 0x41 | ESE / NEESE / SWW / WNW | 8 | all for one.h3m,22,41 |
| H3-04 | Dirt | 5 | 0x40 | SWWNW / WNW | 4 | all for one.h3m,17,23 |
| H3-05 | Dirt | 6 | 0x40 / 0x41 | ESE / SWWNW / WNW | 4 | all for one.h3m,18,21 |
| H3-06 | Dirt | 7 | 0x40 | WNW | 1 | divided loyalties.h3m,63,14 |
| H3-07 | Dirt | 8 | 0x40 / 0x42 | NNE / NNW / SES | 3 | all for one.h3m,10,24 |
| H3-08 | Dirt | 9 | 0x40 / 0x42 | NNENW / SESSW | 3 | all for one.h3m,18,39 |
| H3-09 | Dirt | 10 | 0x40 / 0x42 | NNENW / NNW / SES | 5 | all for one.h3m,16,24 |
| H3-10 | Dirt | 11 | 0x40 / 0x42 | NNE / NNENW / NNW / SESSW / SSW | 8 | all for one.h3m,12,25 |
| H3-11 | Dirt | 15 | 0x43 | NW | 1 | all for one.h3m,17,24 |
| H3-12 | Dirt | 16 | 0x40 / 0x41 / 0x42 / 0x43 | ESES / NEESES / NNEENW / NNEWNW / NSWWNW / NWNW / SSWW / SSWWNW | 16 | all for one.h3m,11,24 |
| H3-13 | Dirt | 17 | 0x40 / 0x43 | ESES / ESESSW / NEESES / NNEWNW / NSWWNW / NWNW | 17 | all for one.h3m,17,22 |
| H3-14 | Dirt | 18 | 0x40 / 0x41 / 0x43 | NW / SE / SW | 25 | all for one.h3m,18,22 |
| H3-15 | Dirt | 19 | 0x40 / 0x41 / 0x42 / 0x43 | NE / NW / SE / SW | 13 | all for one.h3m,11,25 |
| H3-16 | Grass | 20 | 0x40 / 0x41 | NNEESENW / NNESWWNW | 2 | ascension.h3m,42,2 |
| H3-17 | Grass | 21 | 0x40 / 0x41 / 0x42 / 0x43 | NEESES / NNEESENW / NNESWW / NW / SESSWWNW / SWWNW / WNW | 8 | ascension.h3m,24,10 |
| H3-18 | Grass | 22 | 0x40 / 0x42 / 0x43 | ESESSW / NEESSW / NNESWWNW / SESSWW / SESSWWNW | 8 | ascension.h3m,40,4 |
| H3-19 | Grass | 23 | 0x41 / 0x42 | NNEESENW / SESSWWNW | 2 | ascension.h3m,20,6 |
| H3-20 | Grass | 24 | 0x40 / 0x41 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 32 | ascension.h3m,9,12 |
| H3-21 | Grass | 25 | 0x40 / 0x41 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 36 | ascension.h3m,42,3 |
| H3-22 | Grass | 26 | 0x40 / 0x41 | E / ESE / NEE / NEESE / SWW / SWWNW / WNW | 32 | ascension.h3m,40,5 |
| H3-23 | Grass | 27 | 0x40 / 0x41 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 36 | ascension.h3m,8,6 |
| H3-24 | Grass | 28 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW / SSW | 38 | ascension.h3m,46,3 |
| H3-25 | Grass | 29 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW / SSW | 22 | ascension.h3m,48,2 |
| H3-26 | Grass | 30 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW / SSW | 38 | ascension.h3m,49,2 |
| H3-27 | Grass | 31 | 0x40 / 0x42 | NNE / NNENW / NNW / S / SES / SESSW / SSW | 38 | ascension.h3m,51,1 |
| H3-28 | Grass | 32 | 0x40 / 0x41 / 0x43 | NW / SE / SW | 4 | ascension.h3m,61,15 |
| H3-29 | Grass | 33 | 0x41 / 0x43 | NW / SW | 3 | ascension.h3m,42,4 |
| H3-30 | Grass | 34 | 0x40 / 0x42 / 0x43 | NE / NW / SE | 3 | ascension.h3m,24,12 |
| H3-31 | Grass | 35 | 0x40 / 0x41 / 0x42 / 0x43 | NE / NW / SE / SW | 4 | ascension.h3m,41,7 |
| H3-32 | Grass | 36 | 0x40 / 0x41 / 0x42 / 0x43 | ESES / ESESSW / NEESES / NNEE / NNEENW / NNEESE / NNEWNW / NSWWNW | 108 | ascension.h3m,43,2 |
| H3-33 | Grass | 37 | 0x40 / 0x41 / 0x42 / 0x43 | ESES / ESESSW / NEESES / NNEE / NNEENW / NNEESE / NNEWNW / NSWWNW | 101 | ascension.h3m,50,1 |
| H3-34 | Grass | 38 | 0x40 / 0x41 / 0x42 / 0x43 / 0x61 | NE / NW / SE / SW | 108 | ascension.h3m,50,2 |
| H3-35 | Grass | 39 | 0x40 / 0x41 / 0x42 / 0x43 | NE / NW / SE / SW | 92 | ascension.h3m,52,2 |
| H3-36 | Grass | 41 | 0x40 / 0x4C | SE | 2 | ascension.h3m,36,34 |
| H3-37 | Grass | 43 | 0x41 / 0x43 | NE / SE | 2 | ascension.h3m,60,42 |
| H3-38 | Grass | 44 | 0x40 / 0x42 | NE / SE | 2 | all for one.h3m,9,24 |
| H3-39 | Grass | 45 | 0x40 / 0x41 | SE / SW | 2 | ascension.h3m,34,38 |
| H3-40 | Grass | 46 | 0x41 / 0x43 | NW / SW | 3 | ascension.h3m,31,35 |
| H3-41 | Grass | 47 | 0x40 / 0x41 / 0x42 / 0x43 | ESE / NEE / NEESE / SWW / WNW | 12 | ascension.h3m,31,32 |
| H3-42 | Grass | 48 | 0x40 / 0x41 / 0x42 / 0x43 | NNENW / NNW / SES / SESSW | 5 | ascension.h3m,27,35 |
| H3-43 | Rough | 20 | 0x41 | NNEESE | 1 | ascension.h3m,60,39 |
| H3-44 | Rough | 22 | 0x40 | NSWWNW | 1 | ascension.h3m,1,43 |
| H3-45 | Rough | 23 | 0x43 | NEESES | 1 | ascension.h3m,62,48 |
| H3-46 | Rough | 24 | 0x41 | ESE / NEE / NEESE | 3 | all for one.h3m,57,11 |
| H3-47 | Rough | 25 | 0x41 | NEESE | 2 | all for one.h3m,56,8 |
| H3-48 | Rough | 26 | 0x41 | SE | 1 | all for one.h3m,58,38 |
| H3-49 | Rough | 27 | 0x41 | NEE / NEESE | 2 | ascension.h3m,60,40 |
| H3-50 | Rough | 28 | 0x40 | NNE | 1 | all for one.h3m,53,5 |
| H3-51 | Rough | 29 | 0x40 | NNE | 1 | all for one.h3m,59,13 |
| H3-52 | Rough | 30 | 0x40 | NNE | 1 | all for one.h3m,51,4 |
| H3-53 | Rough | 36 | 0x41 / 0x42 | NNEE / NNEENW / SSWW / SSWWNW | 4 | ascension.h3m,1,44 |
| H3-54 | Rough | 37 | 0x41 / 0x42 / 0x43 | NE / NNEE / NNEENW / NNEESE / SSWW | 9 | ascension.h3m,3,46 |
| H3-55 | Rough | 38 | 0x41 / 0x42 | NE / SW | 8 | ascension.h3m,2,44 |
| H3-56 | Rough | 39 | 0x42 | NE | 2 | all for one.h3m,54,6 |
| H3-57 | Rough | 43 | 0x40 / 0x41 / 0x43 | NE / SE / SW | 3 | ascension.h3m,4,46 |
| H3-58 | Rough | 46 | 0x42 / 0x43 | NE / NW | 2 | ascension.h3m,59,39 |
| H3-59 | Rough | 47 | 0x40 / 0x42 | ESE / NEE | 3 | ascension.h3m,60,41 |
| H3-60 | Sand | 0 | 0x40 | ESE / ESES / NNEESE / SE / SES / SESSWW / SESSWWNW / SSWW | 14 | all for one.h3m,63,0 |
| H3-61 | Sand | 1 | 0x40 | NEESE / NW / SSW / SSWW / SSWWNW | 7 | all for one.h3m,67,6 |
| H3-62 | Sand | 2 | 0x40 | ESES / NE / NEE / NNEENW / NNEESE / NNESWWNW / SENW | 7 | all for one.h3m,57,1 |
| H3-63 | Sand | 3 | 0x40 | ESE / NEE / NEESES / NNEENW / NNENW / NW / SSWWNW / SWWNW | 9 | ascension.h3m,48,34 |
| H3-64 | Sand | 4 | 0x40 | ESES / NE / NEESE / NEESES / NNEESE / NNEESENW / NNEWNW / NWNW | 10 | all for one.h3m,65,5 |
| H3-65 | Sand | 5 | 0x40 | ESESSW / NEESES / NESW / NW / SSWW / SWW / SWWNW | 7 | all for one.h3m,58,2 |
| H3-66 | Sand | 6 | 0x40 | NNEENW / NNEESE / NNW / NW / SE | 5 | all for one.h3m,66,31 |
| H3-67 | Sand | 7 | 0x40 | ESE / NE / NEESE / NEESESSW / NESW / SESSWW | 7 | all for one.h3m,69,8 |
| H3-68 | Sand | 9 | 0x40 | NNESWWNW / SW | 2 | all for one.h3m,65,3 |
| H3-69 | Sand | 10 | 0x40 | NEESE | 1 | all for one.h3m,64,28 |
| H3-70 | Sand | 11 | 0x40 | NE / NNEWNW / SSW | 3 | all for one.h3m,66,20 |
| H3-71 | Sand | 12 | 0x40 | NNEENW / NSWWNW | 2 | all for one.h3m,18,43 |
| H3-72 | Sand | 13 | 0x40 | NEESES / NEESESSW / SW | 3 | all for one.h3m,69,7 |
| H3-73 | Sand | 14 | 0x40 | NNEESE / NNESWWNW / NSWWNW / SESSWW / SSWWNW | 6 | all for one.h3m,66,6 |
| H3-74 | Sand | 16 | 0x40 | NNEWNW / NWNW / SE / SESSWW / SSWWNW | 6 | all for one.h3m,65,23 |
| H3-75 | Sand | 17 | 0x40 | NNW | 1 | all for one.h3m,65,71 |
| H3-76 | Sand | 18 | 0x40 | WNW | 1 | all for one.h3m,69,66 |
| H3-77 | Sand | 19 | 0x40 | NEESESSW / SW | 2 | all for one.h3m,66,5 |
| H3-78 | Sand | 20 | 0x40 | NEESESSW / NNEE / NNEESE / SESSWW | 4 | all for one.h3m,59,3 |
| H3-79 | Sand | 21 | 0x40 | NEESES / NNEENW / NSWWNW / SE / SW | 6 | all for one.h3m,68,6 |
| H3-80 | Sand | 22 | 0x40 | ESESSW / NESW / NNEESE / SW / SWWNW | 5 | ascension.h3m,48,35 |
| H3-81 | Sand | 23 | 0x40 | NESW / NNE / NNESWWNW | 3 | all for one.h3m,63,16 |
| H3-82 | Snow | 24 | 0x40 | WNW | 1 | free for all.h3m,57,6 |
| H3-83 | Snow | 25 | 0x40 | SWW / WNW | 2 | free for all.h3m,50,11 |
| H3-84 | Snow | 26 | 0x40 / 0x41 | ESE / SWWNW / WNW | 3 | all for one.h3m,51,0 |
| H3-85 | Snow | 27 | 0x40 / 0x41 | ESE / SWWNW / W | 3 | all for one.h3m,50,2 |
| H3-86 | Snow | 28 | 0x40 | NNENW / NNW | 2 | free for all.h3m,63,2 |
| H3-87 | Snow | 29 | 0x40 | NNENW / NNW | 3 | free for all.h3m,66,1 |
| H3-88 | Snow | 31 | 0x40 | NNENW / NNW | 4 | free for all.h3m,65,1 |
| H3-89 | Snow | 34 | 0x43 | NW | 1 | free for all.h3m,67,1 |
| H3-90 | Snow | 36 | 0x40 | NNEWNW / NSWWNW / NWNW | 8 | free for all.h3m,64,1 |
| H3-91 | Snow | 37 | 0x40 / 0x42 / 0x43 | NEESES / NNEWNW / NSWWNW / NWNW / SSWWNW | 6 | all for one.h3m,51,1 |
| H3-92 | Snow | 38 | 0x40 / 0x41 / 0x43 | NW / SE / SW | 9 | all for one.h3m,50,1 |
| H3-93 | Snow | 39 | 0x43 | NW | 4 | free for all.h3m,64,2 |
| H3-94 | Snow | 47 | 0x40 / 0x41 | NEE / WNW | 2 | all for one.h3m,50,3 |
| H3-95 | Swamp | 20 | 0x43 | NEESESSW | 2 | all for one.h3m,63,64 |
| H3-96 | Swamp | 21 | 0x41 / 0x43 | NEESESSW / NNEESENW | 3 | ascension.h3m,42,57 |
| H3-97 | Swamp | 22 | 0x41 / 0x42 / 0x43 | NEESESSW / NNEESENW / SESSWWNW | 4 | all for one.h3m,69,56 |
| H3-98 | Swamp | 23 | 0x41 / 0x42 | NNEESENW / SESSWWNW | 2 | ascension.h3m,26,65 |
| H3-99 | Swamp | 24 | 0x40 / 0x41 | ESE / NEE / NEESE / SWWNW / WNW | 10 | ascension.h3m,13,56 |
| H3-100 | Swamp | 25 | 0x40 / 0x41 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 17 | all for one.h3m,68,52 |
| H3-101 | Swamp | 26 | 0x40 / 0x41 | ESE / NEE / SWW / SWWNW / WNW | 7 | ascension.h3m,41,54 |
| H3-102 | Swamp | 27 | 0x40 / 0x41 | ESE / NEE / NEESE / SWW / WNW | 17 | ascension.h3m,41,55 |
| H3-103 | Swamp | 28 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW / SSW | 23 | ascension.h3m,41,57 |
| H3-104 | Swamp | 29 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW | 25 | ascension.h3m,40,57 |
| H3-105 | Swamp | 30 | 0x40 / 0x42 | NNE / NNENW / SES / SESSW / SSW | 19 | ascension.h3m,16,62 |
| H3-106 | Swamp | 31 | 0x40 / 0x42 | NNE / NNENW / NNW / SES / SESSW / SSW | 19 | ascension.h3m,37,59 |
| H3-107 | Swamp | 32 | 0x41 / 0x42 | NE / SW | 2 | all for one.h3m,67,53 |
| H3-108 | Swamp | 33 | 0x40 / 0x41 / 0x42 | NE / SE / SW | 6 | ascension.h3m,26,63 |
| H3-109 | Swamp | 34 | 0x40 | SE | 2 | all for one.h3m,60,58 |
| H3-110 | Swamp | 35 | 0x40 / 0x41 / 0x42 / 0x43 | NE / NW / SE / SW | 5 | all for one.h3m,60,55 |
| H3-111 | Swamp | 36 | 0x40 / 0x41 / 0x42 / 0x43 | ESES / ESESSW / NEESES / NNEE / NNEENW / NNEESE / NNEWNW / NSWWNW | 44 | ascension.h3m,25,35 |
| H3-112 | Swamp | 37 | 0x40 / 0x41 / 0x42 / 0x43 | ESES / ESESSW / NEESES / NNEENW / NNEESE / NNEWNW / NSWWNW / SESSWW | 33 | ascension.h3m,24,36 |
| H3-113 | Swamp | 38 | 0x40 / 0x41 / 0x42 / 0x43 / 0x70 | NE / NW / SE / SW | 21 | ascension.h3m,12,59 |
| H3-114 | Swamp | 39 | 0x40 / 0x41 / 0x42 / 0x43 / 0x70 | NE / NW / SE / SW | 36 | ascension.h3m,25,36 |
| H3-115 | Swamp | 41 | 0x40 | SE | 2 | divided loyalties.h3m,46,18 |
| H3-116 | Swamp | 42 | 0x40 / 0x42 | NESW / SENW | 5 | all for one.h3m,64,59 |
| H3-117 | Swamp | 43 | 0x42 / 0x43 | NE / NW | 2 | all for one.h3m,58,43 |
| H3-118 | Swamp | 44 | 0x41 / 0x42 | NW / SE | 3 | ascension.h3m,41,53 |
| H3-119 | Swamp | 47 | 0x41 / 0x42 / 0x43 | ESE / SWW / SWWNW / WNW | 5 | ascension.h3m,31,33 |
| H3-120 | Swamp | 48 | 0x40 / 0x41 / 0x42 | NNENW / NNW / SES / SESSW / SSW | 7 | ascension.h3m,26,35 |
| H3-121 | Swamp | 76 | 0x40 | NWNW | 1 | divided loyalties.h3m,48,30 |
| H3-122 | Water | 0 | 0x00 / 0x01 / 0x02 / 0x03 | NEESESSW / NNEESENW / NNESWWNW / SESSWWNW / SESWNW | 13 | ascension.h3m,62,16 |
| H3-123 | Water | 1 | 0x00 / 0x01 / 0x02 / 0x03 | NEESESSW / NNEESENW / NNESWWNW / SESSWWNW | 12 | ascension.h3m,54,24 |
| H3-124 | Water | 2 | 0x00 / 0x01 / 0x02 / 0x03 | ESESSW / NEESESSW / NESENW / NNEESENW / NNESWWNW / SESSWWNW | 8 | ascension.h3m,40,8 |
| H3-125 | Water | 3 | 0x00 / 0x01 / 0x02 / 0x03 | NEESESSW / NNEESENW / NNESWWNW / SESSWWNW | 11 | ascension.h3m,41,3 |
| H3-126 | Water | 4 | 0x00 / 0x01 | E / ESE / NEE / NEESE / SWW / SWWNW / WNW | 64 | ascension.h3m,41,2 |
| H3-127 | Water | 5 | 0x00 / 0x01 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 65 | ascension.h3m,66,9 |
| H3-128 | Water | 6 | 0x00 / 0x01 | E / ESE / NEE / NEESE / SWW / SWWNW / WNW | 76 | ascension.h3m,21,6 |
| H3-129 | Water | 7 | 0x00 / 0x01 | ESE / NEE / NEESE / SWW / SWWNW / WNW | 73 | ascension.h3m,6,7 |
| H3-130 | Water | 8 | 0x00 / 0x02 | NNE / NNENW / NNW / SES / SESSW / SSW | 74 | ascension.h3m,54,1 |
| H3-131 | Water | 9 | 0x00 / 0x02 | NNE / NNENW / NNW / SES / SESSW / SSW | 67 | ascension.h3m,50,0 |
| H3-132 | Water | 10 | 0x00 / 0x02 | NNE / NNENW / NNW / SES / SESSW / SSW | 67 | ascension.h3m,43,1 |
| H3-133 | Water | 11 | 0x00 / 0x02 | N / NNE / NNENW / NNW / SES / SESSW / SSW | 80 | ascension.h3m,51,0 |
| H3-134 | Water | 12 | 0x00 / 0x01 / 0x03 | NW / SE / SW | 9 | ascension.h3m,39,3 |
| H3-135 | Water | 13 | 0x00 / 0x01 / 0x02 / 0x03 | NE / NW / SE / SW | 10 | ascension.h3m,13,30 |
| H3-136 | Water | 14 | 0x00 / 0x01 / 0x02 / 0x03 | NE / NW / SE / SW | 6 | ascension.h3m,38,8 |
| H3-137 | Water | 15 | 0x00 / 0x01 / 0x02 / 0x03 | NE / NW / SE / SW | 8 | ascension.h3m,41,1 |
| H3-138 | Water | 16 | 0x00 / 0x01 / 0x02 / 0x03 | ESES / ESESSW / NEESES / NNEE / NNEENW / NNEESE / NNEWNW / NSWWNW | 185 | ascension.h3m,44,2 |
| H3-139 | Water | 17 | 0x00 / 0x01 / 0x02 / 0x03 | ESES / ESESSW / NEESES / NNEE / NNEENW / NNEESE / NNEWNW / NSWWNW | 191 | ascension.h3m,49,1 |
| H3-140 | Water | 18 | 0x00 / 0x01 / 0x02 / 0x03 | NE / NW / SE / SW | 202 | ascension.h3m,49,0 |
| H3-141 | Water | 19 | 0x00 / 0x01 / 0x02 / 0x03 | NE / NW / SE / SW | 198 | ascension.h3m,53,0 |


## Tableau 3 — lien H2 -> H3 (PROPOSITION auto à corriger)

| id H2 | kind | masque | id H3 proposé | h3m terrain | picture | mirroring |
|---|---|---|---|---|---|---|
| H2-01 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-02 | SAND | N+NE+NW+W | H3-64 | Sand | 4 | 0x40 |
| H2-03 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-04 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-05 | SAND | N+NW | H3-66 | Sand | 6 | 0x40 |
| H2-06 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-07 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-08 | SAND | N+NW | H3-66 | Sand | 6 | 0x40 |
| H2-09 | SAND | E+NE+SE | H3-64 | Sand | 4 | 0x40 |
| H2-10 | SAND | S+SE+SW | H3-24 | Grass | 28 | 0x40/0x42 |
| H2-11 | SAND | NW | H3-63 | Sand | 3 | 0x40 |
| H2-12 | SAND | E+NE | H3-63 | Sand | 3 | 0x40 |
| H2-13 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-14 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 |
| H2-15 | SAND | N+NE+NW+SW+W | H3-62 | Sand | 2 | 0x40 |
| H2-16 | SAND | S+SE+SW | H3-24 | Grass | 28 | 0x40/0x42 |
| H2-17 | WATER | N+NE | H3-133 | Water | 11 | 0x00/0x02 |
| H2-18 | WATER | S+SE | H3-133 | Water | 11 | 0x00/0x02 |
| H2-19 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00/0x02 |
| H2-20 | WATER | S+SE | H3-133 | Water | 11 | 0x00/0x02 |
| H2-21 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00/0x02 |
| H2-22 | WATER | S+SE+SW | H3-133 | Water | 11 | 0x00/0x02 |
| H2-23 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00/0x02 |
| H2-24 | WATER | S+SE+SW | H3-133 | Water | 11 | 0x00/0x02 |
| H2-25 | WATER | E+N+NE+NW+SE | H3-122 | Water | 0 | 0x00/0x01/0x02/0x03 |
| H2-26 | WATER | E+S+SE+SW | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-27 | WATER | E+N+NE+SE | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-28 | WATER | N+NE+NW+W | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-29 | WATER | E+N+NE | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-30 | WATER | N+NE+NW+W | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-31 | WATER | E+S+SE+SW | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-32 | WATER | N+NW+SW+W | H3-139 | Water | 17 | 0x00/0x01/0x02/0x03 |
| H2-33 | WATER | NW+S+SE+SW+W | H3-122 | Water | 0 | 0x00/0x01/0x02/0x03 |
| H2-34 | WATER | E+NE+SE | H3-128 | Water | 6 | 0x00/0x01 |
| H2-35 | WATER | SW+W | H3-128 | Water | 6 | 0x00/0x01 |
| H2-36 | WATER | E+NE+SE | H3-128 | Water | 6 | 0x00/0x01 |
| H2-37 | WATER | NW+SW+W | H3-128 | Water | 6 | 0x00/0x01 |
| H2-38 | WATER | E+SE | H3-128 | Water | 6 | 0x00/0x01 |
| H2-39 | WATER | NW+SW+W | H3-128 | Water | 6 | 0x00/0x01 |
| H2-40 | WATER | E+NE+SE | H3-128 | Water | 6 | 0x00/0x01 |
| H2-41 | WATER | NW+SW+W | H3-128 | Water | 6 | 0x00/0x01 |
| H2-42 | WATER | SE | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-43 | WATER | NE | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-44 | WATER | NW | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-45 | WATER | NE | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-46 | WATER | SW | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-47 | WATER | SE | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-48 | WATER | NW | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
| H2-49 | WATER | SW | H3-140 | Water | 18 | 0x00/0x01/0x02/0x03 |
