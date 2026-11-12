# Lien tuiles côtières H2 -> H3 (fh2m -> h3m)


Masque voisins = directions (N,NE,E,SE,S,SW,W,NW) des voisins de l'autre côté de la côte : terre pour les tuiles eau, eau pour les tuiles terre.

## Tableau 3 — lien H2 -> H3 (définitif, appris des cartes de référence)

Pour chaque `H2-xx` (kind + masque de `labels.csv`), la variante H3 correspondante
(même masque exact, variante la plus fréquente dans `input/*.h3m`).

| id H2 | kind | masque | id H3 | h3m terrain | picture | mirroring | nb ref |
|---|---|---|---|---|---|---|---|
| H2-01 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-02 | SAND | N+NE+W+NW | H3-70 | Sand | 11 | 0x40 | 1 |
| H2-03 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-04 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-05 | SAND | N+NW | H3-66 | Sand | 6 | 0x40 | 1 |
| H2-06 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-07 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-08 | SAND | N+NW | H3-66 | Sand | 6 | 0x40 | 1 |
| H2-09 | SAND | NE+E+SE | H3-61 | Sand | 1 | 0x40 | 2 |
| H2-10 | SAND | SE+S+SW | H3-24 | Sand/land | 28 | 0x42 | 14 |
| H2-11 | SAND | NW | H3-63 | Sand | 3 | 0x40 | 2 |
| H2-12 | SAND | NE+E | H3-62 | Sand | 2 | 0x40 | 1 |
| H2-13 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-14 | SAND | N+NE+NW | H3-63 | Sand | 3 | 0x40 | 1 |
| H2-15 | SAND | N+NE+SW+W+NW | H3-62 | Sand | 2 | 0x40 | 1 |
| H2-16 | SAND | SE+S+SW | H3-24 | Sand/land | 28 | 0x42 | 14 |
| H2-17 | WATER | N+NE | H3-133 | Water | 11 | 0x00 | 13 |
| H2-18 | WATER | SE+S | H3-131 | Water | 9 | 0x02 | 15 |
| H2-19 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00 | 16 |
| H2-20 | WATER | SE+S | H3-131 | Water | 9 | 0x02 | 15 |
| H2-21 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00 | 16 |
| H2-22 | WATER | SE+S+SW | H3-132 | Water | 10 | 0x02 | 19 |
| H2-23 | WATER | N+NE+NW | H3-133 | Water | 11 | 0x00 | 16 |
| H2-24 | WATER | SE+S+SW | H3-132 | Water | 10 | 0x02 | 19 |
| H2-25 | WATER | N+NE+E+SE+NW | H3-122 | Water | 0 | 0x01 | 3 |
| H2-26 | WATER | E+SE+S+SW | H3-138 | Water | 16 | 0x03 | 14 |
| H2-27 | WATER | N+NE+E+SE | H3-138 | Water | 16 | 0x01 | 19 |
| H2-28 | WATER | N+NE+W+NW | H3-139 | Water | 17 | 0x00 | 12 |
| H2-29 | WATER | N+NE+E | H3-138 | Water | 16 | 0x01 | 15 |
| H2-30 | WATER | N+NE+W+NW | H3-139 | Water | 17 | 0x00 | 12 |
| H2-31 | WATER | E+SE+S+SW | H3-138 | Water | 16 | 0x03 | 14 |
| H2-32 | WATER | N+SW+W+NW | H3-139 | Water | 17 | 0x00 | 19 |
| H2-33 | WATER | SE+S+SW+W+NW | H3-122 | Water | 0 | 0x02 | 4 |
| H2-34 | WATER | NE+E+SE | H3-128 | Water | 6 | 0x01 | 12 |
| H2-35 | WATER | SW+W | H3-127 | Water | 5 | 0x00 | 13 |
| H2-36 | WATER | NE+E+SE | H3-128 | Water | 6 | 0x01 | 12 |
| H2-37 | WATER | SW+W+NW | H3-128 | Water | 6 | 0x00 | 16 |
| H2-38 | WATER | E+SE | H3-129 | Water | 7 | 0x01 | 16 |
| H2-39 | WATER | SW+W+NW | H3-128 | Water | 6 | 0x00 | 16 |
| H2-40 | WATER | NE+E+SE | H3-128 | Water | 6 | 0x01 | 12 |
| H2-41 | WATER | SW+W+NW | H3-128 | Water | 6 | 0x00 | 16 |
| H2-42 | WATER | SE | H3-140 | Water | 18 | 0x00 | 57 |
| H2-43 | WATER | NE | H3-141 | Water | 19 | 0x02 | 47 |
| H2-44 | WATER | NW | H3-141 | Water | 19 | 0x03 | 52 |
| H2-45 | WATER | NE | H3-141 | Water | 19 | 0x02 | 47 |
| H2-46 | WATER | SW | H3-140 | Water | 18 | 0x01 | 52 |
| H2-47 | WATER | SE | H3-140 | Water | 18 | 0x00 | 57 |
| H2-48 | WATER | NW | H3-141 | Water | 19 | 0x03 | 52 |
| H2-49 | WATER | SW | H3-140 | Water | 18 | 0x01 | 52 |
