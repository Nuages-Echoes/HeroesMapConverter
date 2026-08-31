import gzip
import struct
from collections import OrderedDict

def read_string(file, length):
    return file.read(length).decode('utf-8', errors='ignore').strip('\x00')

def parse_h3m(file_path):
    with gzip.open(file_path, 'rb') as file:
        data = OrderedDict()

        # --- Lire les informations de base ---
        # Lire l'identifiant du format (4 octets)
        format_id = file.read(4)
        data['Format Identifier'] = format_id.hex().upper()

        # Vérifier la version du jeu
        if format_id == b'\x0E\x00\x00\x00':
            data['Version'] = 'RoE'
        elif format_id == b'\x15\x00\x00\x00':
            data['Version'] = 'AB'
        elif format_id == b'\x1C\x00\x00\x00':
            data['Version'] = 'SoD'
        else:
            data['Version'] = 'Unknown'

        # Lire s'il y a au moins un héros sur la carte (1 octet)
        has_hero = struct.unpack('B', file.read(1))[0]
        data['Has Hero'] = bool(has_hero)

        # Lire la hauteur et la largeur de la carte (4 octets)
        map_size = struct.unpack('i', file.read(4))[0]
        data['Map Size'] = map_size

        # Lire le niveau de la carte (1 octet)
        map_level = struct.unpack('B', file.read(1))[0]
        data['Map Level'] = 'Two-level' if map_level else 'Single-level'

        # Lire la longueur du nom de la carte (4 octets)
        name_length = struct.unpack('i', file.read(4))[0]
        data['Map Name'] = read_string(file, name_length)

        # Lire la longueur de la description de la carte (4 octets)
        desc_length = struct.unpack('i', file.read(4))[0]
        data['Map Description'] = read_string(file, desc_length)

        # Lire la difficulté de la carte (1 octet)
        difficulty = struct.unpack('B', file.read(1))[0]
        difficulty_levels = {0: 'Easy', 1: 'Normal', 2: 'Hard', 3: 'Expert', 4: 'Impossible'}
        data['Difficulty'] = difficulty_levels.get(difficulty, 'Unknown')

        # --- Lire les attributs des joueurs ---
        players = ['Red', 'Blue', 'Tan', 'Green', 'Orange', 'Purple', 'Teal', 'Pink']
        players_data = []

        for player in players:
            player_data = OrderedDict()
            player_data['Color'] = player
            player_data['Heroes Mastery Level Cap'] = struct.unpack('B', file.read(1))[0]
            player_data['Human Playable'] = bool(struct.unpack('B', file.read(1))[0])
            player_data['AI Playable'] = bool(struct.unpack('B', file.read(1))[0])
            behavior = struct.unpack('B', file.read(1))[0]
            behavior_types = {0: 'Random', 1: 'Warrior', 2: 'Builder', 3: 'Explorer'}
            player_data['Behavior'] = behavior_types.get(behavior, 'Unknown')
            player_data['Has Defined Towns'] = bool(struct.unpack('B', file.read(1))[0])
            player_data['Owned Towns'] = struct.unpack('H', file.read(2))[0]
            players_data.append(player_data)

        data['Players'] = players_data

        # --- Lire les données du terrain ---
        # Chaque case est représentée par 1 octet pour le terrain
        terrain_types = {
            0x00: "Dirt", 0x01: "Sand", 0x02: "Grass", 0x03: "Snow",
            0x04: "Swamp", 0x05: "Rough", 0x06: "Subterranean", 0x07: "Lava",
            0x08: "Water", 0x09: "Rock", 0x0A: "Tree", 0x0B: "Jungle",
            # Ajoutez d'autres types de terrain si nécessaire
        }

        # Lire les données du terrain (supposons que la carte est carrée)
        terrain_data = []
        for _ in range(map_size * map_size):  # Supposons que la carte est carrée
            terrain_byte = struct.unpack('B', file.read(1))[0]
            terrain_type = terrain_types.get(terrain_byte, f"Unknown (0x{terrain_byte:02X})")
            terrain_data.append(terrain_type)

        data['Terrain'] = terrain_data

        # --- Lire les objets sur la carte ---
        # Supposons que chaque objet est représenté par 5 octets (exemple simplifié)
        # Cela peut varier selon le format exact du fichier H3M
        objects_data = []
        for _ in range(100):  # Exemple : lire jusqu'à 100 objets (à ajuster)
            try:
                obj_type = struct.unpack('B', file.read(1))[0]
                obj_x = struct.unpack('B', file.read(1))[0]
                obj_y = struct.unpack('B', file.read(1))[0]
                obj_unknown1 = struct.unpack('B', file.read(1))[0]
                obj_unknown2 = struct.unpack('B', file.read(1))[0]
                objects_data.append({
                    'Type': obj_type,
                    'X': obj_x,
                    'Y': obj_y,
                    'Unknown1': obj_unknown1,
                    'Unknown2': obj_unknown2
                })
            except struct.error:
                break  # Fin des objets

        data['Objects'] = objects_data

        return data

# Exemple d'utilisation :
# result = parse_h3m('votre_fichier.h3m')
# print(result)