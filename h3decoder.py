"""
H3M File Parser and Writer for Heroes of Might and Magic III

This module reads and writes .h3m files (which are gzip-compressed) and extracts/stores
information into a structured dictionary format based on the specification from
h3m_description.english.txt and the reference implementation from the VCMI project.

The H3M format uses LITTLE-ENDIAN for multi-byte integers.
Header layout differs between RoE, AB and SoD versions and is handled accordingly.
"""

import gzip
import struct
import zlib
from collections import OrderedDict
from io import BytesIO


def read_string(buffer, length):
    """Read a string of specified length from buffer."""
    if length <= 0:
        return ""
    raw = buffer.read(length)
    if len(raw) < length:
        raw = raw.ljust(length, b'\x00')
    cleaned = raw.rstrip(b'\x00')
    try:
        return cleaned.decode('cp1252')
    except:
        return cleaned.decode('latin-1', errors='replace')


def safe_read(buffer, size, default=b'\x00'):
    """Safely read bytes from buffer, return default if EOF."""
    data = buffer.read(size)
    if len(data) < size:
        data = data.ljust(size, default[:size])
    return data


def parse_h3m(file_path):
    """
    Parse a Heroes of Might and Magic III map file (.h3m).

    Supports the RoE, AB and SoD header variants.

    Args:
        file_path: Path to the .h3m file

    Returns:
        OrderedDict: A structured dictionary containing map information.
    """
    data = OrderedDict()

    DIFFICULTY_MAP = {0: 'Easy', 1: 'Normal', 2: 'Hard', 3: 'Expert', 4: 'Impossible'}
    BEHAVIOR_MAP = {0: 'Random', 1: 'Warrior', 2: 'Builder', 3: 'Explorer'}

    TERRAIN_MAP = {
        0x00: "Dirt", 0x01: "Sand", 0x02: "Grass", 0x03: "Snow",
        0x04: "Swamp", 0x05: "Rough", 0x06: "Subterranean", 0x07: "Lava",
        0x08: "Water", 0x09: "Rock"
    }

    RIVER_MAP = {0x00: "None", 0x01: "Clear", 0x02: "Icy", 0x03: "Muddy", 0x04: "Lava"}
    ROAD_MAP = {0x00: "None", 0x01: "Dirt", 0x02: "Gravel", 0x03: "Cobblestone"}

    PLAYER_COLORS = ['Red', 'Blue', 'Tan', 'Green', 'Orange', 'Purple', 'Teal', 'Pink']
    TOWN_TYPES = ['Castle', 'Rampart', 'Tower', 'Inferno', 'Necropolis',
                  'Dungeon', 'Stronghold', 'Fortress', 'Conflux']

    MAX_RUMORS = 100
    MAX_OBJECTS = 10000
    MAX_HEROES_PER_PLAYER = 768

    with gzip.open(file_path, 'rb') as f:
        all_data = f.read()

    buffer = BytesIO(all_data)

    # === Format version ===
    format_id = safe_read(buffer, 4)
    version = struct.unpack('<I', format_id)[0]
    if version == 0x0E:
        level_ab = False
        level_sod = False
        version_name = 'RoE (Restoration of Erathia)'
        factions_bytes = 1
        heroes_bytes = 16
        artifacts_bytes = 0
        spells_bytes = 0
        skills_bytes = 0
        artifact_id_bytes = 1
        creature_id_bytes = 1
        artifact_slots = 18
    elif version == 0x15:
        level_ab = True
        level_sod = False
        version_name = 'AB (Armageddon Blade)'
        factions_bytes = 2
        heroes_bytes = 20
        artifacts_bytes = 17
        spells_bytes = 0
        skills_bytes = 0
        artifact_id_bytes = 2
        creature_id_bytes = 2
        artifact_slots = 18
    elif version == 0x1C:
        level_ab = True
        level_sod = True
        version_name = 'SoD (Shadow of Death)'
        factions_bytes = 2
        heroes_bytes = 20
        artifacts_bytes = 18
        spells_bytes = 9
        skills_bytes = 4
        artifact_id_bytes = 2
        creature_id_bytes = 2
        artifact_slots = 19
    else:
        raise ValueError("Unsupported map format identifier: " + format_id.hex().upper())

    towns_in_format = 8 if not level_ab else 9

    # === Basic Map Parameters ===
    section_basic = OrderedDict()
    section_basic['Format Identifier'] = format_id.hex().upper()
    section_basic['Version'] = version_name

    section_basic['Has Hero'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
    map_size = struct.unpack('<i', safe_read(buffer, 4))[0]
    section_basic['Map Size'] = map_size
    map_level = struct.unpack('<B', safe_read(buffer, 1))[0]
    section_basic['Map Level'] = 'Two-level' if map_level else 'Single-level'
    section_basic['Has Underground'] = bool(map_level)

    name_length = struct.unpack('<i', safe_read(buffer, 4))[0]
    section_basic['Map Name'] = read_string(buffer, name_length)

    desc_length = struct.unpack('<i', safe_read(buffer, 4))[0]
    section_basic['Map Description'] = read_string(buffer, desc_length)

    difficulty = struct.unpack('<B', safe_read(buffer, 1))[0]
    section_basic['Difficulty'] = DIFFICULTY_MAP.get(difficulty, 'Unknown')

    if level_ab:
        section_basic['Heroes Mastery Level Cap'] = struct.unpack('<B', safe_read(buffer, 1))[0]

    data['Basic Parameters'] = section_basic

    # === Players' Attributes (includes each player's main hero) ===
    section_players = OrderedDict()
    players_list = []
    section_heroes = OrderedDict()
    player_heroes_list = []

    for color in PLAYER_COLORS:
        player = OrderedDict()
        player['Color'] = color
        hero_info = OrderedDict()
        hero_info['Color'] = color
        player['Human Playable'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        player['AI Playable'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        behavior = struct.unpack('<B', safe_read(buffer, 1))[0]
        player['Behavior'] = BEHAVIOR_MAP.get(behavior, 'Unknown')

        if level_sod:
            safe_read(buffer, 1)  # whether factions are selectable

        owned_towns_bits = struct.unpack('<H', safe_read(buffer, factions_bytes).ljust(2, b'\x00'))[0]
        player['Has Defined Towns'] = owned_towns_bits != 0
        player['Owned Towns'] = OrderedDict()
        for i in range(towns_in_format):
            player['Owned Towns'][TOWN_TYPES[i]] = bool(owned_towns_bits & (1 << i))

        player['Owns Random Town'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])

        player['Main Town'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        if player['Main Town']:
            if level_ab:
                player['Generate Hero At Main Town'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
                safe_read(buffer, 1)  # unused starting town type
            player['Castle X'] = struct.unpack('<B', safe_read(buffer, 1))[0]
            player['Castle Y'] = struct.unpack('<B', safe_read(buffer, 1))[0]
            player['Castle Z'] = struct.unpack('<B', safe_read(buffer, 1))[0]
        else:
            player['Castle X'] = None
            player['Castle Y'] = None
            player['Castle Z'] = None

        hero_info['Has Random Hero'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        hero_type = struct.unpack('<B', safe_read(buffer, 1))[0]
        hero_info['Hero Type'] = hero_type if hero_type != 0xFF else None

        if hero_type != 0xFF:
            hero_info['Hero Face'] = struct.unpack('<B', safe_read(buffer, 1))[0]
            name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
            hero_info['Hero Name'] = read_string(buffer, name_len)
            safe_read(buffer, 1)  # unknown byte

        if level_ab:
            safe_read(buffer, 1)  # number of hero placeholders (unused)
            num_heroes = struct.unpack('<I', safe_read(buffer, 4))[0]
            hero_info['Number of Heroes'] = num_heroes
            num_heroes = min(num_heroes, MAX_HEROES_PER_PLAYER)
            for _ in range(num_heroes):
                safe_read(buffer, 1)  # hero identifier
                name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
                read_string(buffer, name_len)

        players_list.append(player)
        player_heroes_list.append(hero_info)

    section_players['Players'] = players_list
    data['Players Attributes'] = section_players
    section_heroes['Player Heroes'] = player_heroes_list
    data['Player Heroes'] = section_heroes

    # === Special Victory Condition ===
    vic_type = struct.unpack('<b', safe_read(buffer, 1, b'\xff'))[0]
    if vic_type == -1:
        data['Victory Condition'] = OrderedDict([('Type', 'None')])
    else:
        safe_read(buffer, 2)  # allow normal victory + applies to AI
        detail_size = {
            0: artifact_id_bytes, 1: creature_id_bytes + 4, 2: 5,
            3: 5, 4: 3, 5: 3, 6: 3, 7: 3, 8: 0, 9: 0, 10: 4
        }.get(vic_type, 6)
        safe_read(buffer, detail_size)
        data['Victory Condition'] = OrderedDict([('Type', hex(vic_type))])

    # === Special Loss Condition ===
    loss_type = struct.unpack('<b', safe_read(buffer, 1, b'\xff'))[0]
    if loss_type == -1:
        data['Loss Condition'] = OrderedDict([('Type', 'None')])
    else:
        detail_size = {0: 3, 1: 3, 2: 2}.get(loss_type, 3)
        safe_read(buffer, detail_size)
        data['Loss Condition'] = OrderedDict([('Type', hex(loss_type))])

    # === Teams ===
    num_teams = struct.unpack('<B', safe_read(buffer, 1))[0]
    teams = OrderedDict([('Number of Teams', num_teams)])
    if num_teams > 0:
        assignments = OrderedDict()
        for color in PLAYER_COLORS:
            assignments[color] = struct.unpack('<B', safe_read(buffer, 1))[0]
        teams['Team Assignments'] = assignments
    data['Teams'] = teams

    # === Available Heroes ===
    avail_bytes = safe_read(buffer, heroes_bytes)
    data['Available Heroes'] = OrderedDict([('Bitfield', avail_bytes.hex())])
    if level_ab:
        placeholders_qty = struct.unpack('<I', safe_read(buffer, 4))[0]
        for _ in range(min(placeholders_qty, 156)):
            safe_read(buffer, 1)  # reserved campaign hero identifier

    # === Disposed Heroes (SoD only) ===
    if level_sod:
        disposed = struct.unpack('<B', safe_read(buffer, 1))[0]
        for _ in range(disposed):
            safe_read(buffer, 2)  # hero identifier + portrait
            name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
            read_string(buffer, name_len)
            safe_read(buffer, 1)  # players bitfield

    # === Reserved Bytes ===
    reserved = safe_read(buffer, 31)
    data['Reserved Bytes'] = reserved.hex()

    # === Random Artifacts (AB and later) ===
    if level_ab:
        artifacts_bytes_data = safe_read(buffer, artifacts_bytes)
        data['Random Artifacts'] = OrderedDict([('Bitfield', artifacts_bytes_data.hex())])

    # === Allowed Spells and Abilities (SoD only) ===
    if level_sod:
        spells_mask = safe_read(buffer, spells_bytes)
        skills_mask = safe_read(buffer, skills_bytes)
        data['Allowed Spells'] = OrderedDict([('Bitfield', spells_mask.hex())])
        data['Allowed Abilities'] = OrderedDict([('Bitfield', skills_mask.hex())])

    # === Rumors ===
    num_rumors = struct.unpack('<I', safe_read(buffer, 4))[0]
    num_rumors = min(num_rumors, MAX_RUMORS)
    rumors_list = []
    for _ in range(num_rumors):
        name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
        name = read_string(buffer, name_len)
        text_len = struct.unpack('<I', safe_read(buffer, 4))[0]
        text = read_string(buffer, text_len)
        rumors_list.append(OrderedDict([('Name', name), ('Text', text)]))
    data['Rumors'] = OrderedDict([('Number of Rumors', num_rumors), ('Rumors', rumors_list)])

    # === Predefined Heroes (SoD only) ===
    if level_sod:
        for _ in range(156):
            has_settings = struct.unpack('<B', safe_read(buffer, 1))[0]
            if not has_settings:
                continue
            has_exp = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_exp:
                safe_read(buffer, 4)
            has_sec_skills = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_sec_skills:
                skill_count = struct.unpack('<I', safe_read(buffer, 4))[0]
                safe_read(buffer, skill_count * 2)
            has_art_set = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_art_set:
                safe_read(buffer, artifact_slots * artifact_id_bytes)
                bag_count = struct.unpack('<H', safe_read(buffer, 2))[0]
                safe_read(buffer, bag_count * artifact_id_bytes)
            has_custom_bio = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_custom_bio:
                bio_len = struct.unpack('<I', safe_read(buffer, 4))[0]
                read_string(buffer, bio_len)
            safe_read(buffer, 1)  # gender
            has_custom_spells = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_custom_spells:
                safe_read(buffer, spells_bytes)
            has_custom_prim_skills = struct.unpack('<B', safe_read(buffer, 1))[0]
            if has_custom_prim_skills:
                safe_read(buffer, 4)
        data['Hero Settings'] = OrderedDict([('Note', 'Skipped for performance')])

    # === Surface Map ===
    section_surface = OrderedDict()
    surface_size = map_size * map_size * 7
    surface_raw = safe_read(buffer, surface_size)

    section_surface['Size'] = surface_size
    section_surface['Raw Data Length'] = len(surface_raw)

    grid = []
    cells_to_parse = min(map_size * map_size, len(surface_raw) // 7)
    for i in range(cells_to_parse):
        offset = i * 7
        cell = OrderedDict()
        cell['X'] = i % map_size
        cell['Y'] = i // map_size
        cell['Z'] = 0
        cell['Terrain Type'] = TERRAIN_MAP.get(surface_raw[offset], 'Unknown (0x' + format(surface_raw[offset], '02X') + ')')
        cell['Terrain Picture'] = surface_raw[offset + 1]
        cell['River Type'] = RIVER_MAP.get(surface_raw[offset + 2], 'Unknown (0x' + format(surface_raw[offset + 2], '02X') + ')')
        cell['River Properties'] = surface_raw[offset + 3]
        cell['Road Type'] = ROAD_MAP.get(surface_raw[offset + 4], 'Unknown (0x' + format(surface_raw[offset + 4], '02X') + ')')
        cell['Road Properties'] = surface_raw[offset + 5]
        cell['Mirroring'] = '0x' + format(surface_raw[offset + 6], '02X')
        grid.append(cell)

    section_surface['Grid'] = grid
    data['Surface Map'] = section_surface

    # === Underground Map ===
    if section_basic['Has Underground']:
        section_underground = OrderedDict()
        underground_size = map_size * map_size * 7
        underground_raw = safe_read(buffer, underground_size)

        section_underground['Size'] = underground_size
        section_underground['Raw Data Length'] = len(underground_raw)

        grid = []
        cells_to_parse = min(map_size * map_size, len(underground_raw) // 7)
        for i in range(cells_to_parse):
            offset = i * 7
            cell = OrderedDict()
            cell['X'] = i % map_size
            cell['Y'] = i // map_size
            cell['Z'] = 1
            cell['Terrain Type'] = TERRAIN_MAP.get(underground_raw[offset], 'Unknown (0x' + format(underground_raw[offset], '02X') + ')')
            cell['Terrain Picture'] = underground_raw[offset + 1]
            cell['River Type'] = RIVER_MAP.get(underground_raw[offset + 2], 'Unknown (0x' + format(underground_raw[offset + 2], '02X') + ')')
            cell['River Properties'] = underground_raw[offset + 3]
            cell['Road Type'] = ROAD_MAP.get(underground_raw[offset + 4], 'Unknown (0x' + format(underground_raw[offset + 4], '02X') + ')')
            cell['Road Properties'] = underground_raw[offset + 5]
            cell['Mirroring'] = '0x' + format(underground_raw[offset + 6], '02X')
            grid.append(cell)

        section_underground['Grid'] = grid
        data['Underground Map'] = section_underground

    # === Objects ===
    num_objects_data = safe_read(buffer, 4)
    if len(num_objects_data) == 4:
        num_objects = struct.unpack('<I', num_objects_data)[0]
        data['Objects'] = OrderedDict([
            ('Number of Objects', num_objects),
            ('Raw Data', (num_objects_data + safe_read(buffer, buffer.getbuffer().nbytes - buffer.tell())).hex())
        ])
    else:
        data['Objects'] = OrderedDict([('Note', 'End of file')])

    return data


def print_map_summary(map_data):
    """Print a summary of the map data."""
    basic = map_data.get('Basic Parameters', {})

    print("=" * 60)
    print("H3M MAP SUMMARY")
    print("=" * 60)
    print("Version: " + str(basic.get('Version', 'Unknown')))
    print("Map Name: " + str(basic.get('Map Name', 'Unknown')))
    print("Map Size: " + str(basic.get('Map Size', 'Unknown')) + "x" + str(basic.get('Map Size', 'Unknown')))
    print("Map Level: " + str(basic.get('Map Level', 'Unknown')))
    print("Difficulty: " + str(basic.get('Difficulty', 'Unknown')))
    print()

    players = map_data.get('Players Attributes', {}).get('Players', [])
    print("Players: " + str(len(players)))
    for p in players:
        print("  " + str(p.get('Color')) + ": Human=" + str(p.get('Human Playable')) + ", AI=" + str(p.get('AI Playable')))
    print()

    surface = map_data.get('Surface Map', {})
    print("Terrain cells (surface): " + str(len(surface.get('Grid', []))))
    if 'Underground Map' in map_data:
        print("Terrain cells (underground): " + str(len(map_data['Underground Map'].get('Grid', []))))


def write_h3m(map_data, output_path):
    """
    Write map data to a Heroes of Might and Magic III map file (.h3m).

    Mirrors the layout expected by parse_h3m for the map's format version.

    Args:
        map_data: OrderedDict containing map information (from parse_h3m)
        output_path: Path to save the .h3m file

    Returns:
        None
    """
    VERSION_INVERSE = {
        'RoE (Restoration of Erathia)': b'\x0E\x00\x00\x00',
        'AB (Armageddon Blade)': b'\x15\x00\x00\x00',
        'SoD (Shadow of Death)': b'\x1C\x00\x00\x00'
    }

    DIFFICULTY_INVERSE = {'Easy': 0, 'Normal': 1, 'Hard': 2, 'Expert': 3, 'Impossible': 4}
    BEHAVIOR_INVERSE = {'Random': 0, 'Warrior': 1, 'Builder': 2, 'Explorer': 3}

    TERRAIN_INVERSE = {
        'Dirt': 0x00, 'Sand': 0x01, 'Grass': 0x02, 'Snow': 0x03,
        'Swamp': 0x04, 'Rough': 0x05, 'Subterranean': 0x06, 'Lava': 0x07,
        'Water': 0x08, 'Rock': 0x09
    }

    RIVER_INVERSE = {'None': 0x00, 'Clear': 0x01, 'Icy': 0x02, 'Muddy': 0x03, 'Lava': 0x04}
    ROAD_INVERSE = {'None': 0x00, 'Dirt': 0x01, 'Gravel': 0x02, 'Cobblestone': 0x03}

    PLAYER_COLORS = ['Red', 'Blue', 'Tan', 'Green', 'Orange', 'Purple', 'Teal', 'Pink']
    TOWN_TYPES = ['Castle', 'Rampart', 'Tower', 'Inferno', 'Necropolis',
                  'Dungeon', 'Stronghold', 'Fortress', 'Conflux']

    buffer = BytesIO()

    basic = map_data.get('Basic Parameters', {})
    players_attr = map_data.get('Players Attributes', {}).get('Players', [])
    player_heroes = map_data.get('Player Heroes', {}).get('Player Heroes', [])
    heroes_by_color = {ph.get('Color'): ph for ph in player_heroes}

    version_str = basic.get('Version', 'RoE (Restoration of Erathia)')
    format_id = VERSION_INVERSE.get(version_str, b'\x0E\x00\x00\x00')
    version = struct.unpack('<I', format_id)[0]
    level_ab = version >= 0x15
    level_sod = version >= 0x1C
    factions_bytes = 1 if version == 0x0E else 2
    heroes_bytes = 16 if version == 0x0E else 20
    artifacts_bytes = {0x0E: 0, 0x15: 17, 0x1C: 18}.get(version, 18)
    spells_bytes = 9 if level_sod else 0
    skills_bytes = 4 if level_sod else 0
    towns_in_format = 8 if not level_ab else 9

    # === Basic Map Parameters ===
    buffer.write(format_id)
    buffer.write(struct.pack('<B', 1 if basic.get('Has Hero', False) else 0))
    buffer.write(struct.pack('<i', basic.get('Map Size', 72)))
    has_underground = basic.get('Has Underground', False)
    buffer.write(struct.pack('<B', 1 if has_underground else 0))

    map_name = basic.get('Map Name', '')
    name_bytes = map_name.encode('cp1252', errors='replace')
    buffer.write(struct.pack('<i', len(name_bytes)))
    buffer.write(name_bytes)

    map_desc = basic.get('Map Description', '')
    desc_bytes = map_desc.encode('cp1252', errors='replace')
    buffer.write(struct.pack('<i', len(desc_bytes)))
    buffer.write(desc_bytes)

    buffer.write(struct.pack('<B', DIFFICULTY_INVERSE.get(basic.get('Difficulty', 'Normal'), 1)))

    if level_ab:
        buffer.write(struct.pack('<B', basic.get('Heroes Mastery Level Cap', 0)))

    # === Players' Attributes ===
    for player in players_attr:
        buffer.write(struct.pack('<B', 1 if player.get('Human Playable', False) else 0))
        buffer.write(struct.pack('<B', 1 if player.get('AI Playable', False) else 0))
        buffer.write(struct.pack('<B', BEHAVIOR_INVERSE.get(player.get('Behavior', 'Random'), 0)))

        if level_sod:
            buffer.write(struct.pack('<B', 1 if player.get('Has Defined Towns', False) else 0))

        owned_towns = player.get('Owned Towns', {})
        towns_bits = 0
        for i in range(towns_in_format):
            if owned_towns.get(TOWN_TYPES[i], False):
                towns_bits |= (1 << i)
        buffer.write(towns_bits.to_bytes(factions_bytes, 'little'))

        buffer.write(struct.pack('<B', 1 if player.get('Owns Random Town', False) else 0))

        main_town = player.get('Main Town', False)
        buffer.write(struct.pack('<B', 1 if main_town else 0))
        if main_town:
            if level_ab:
                buffer.write(struct.pack('<B', 1 if player.get('Generate Hero At Main Town', True) else 0))
                buffer.write(struct.pack('<B', 0))
            buffer.write(struct.pack('<B', player.get('Castle X', 0) or 0))
            buffer.write(struct.pack('<B', player.get('Castle Y', 0) or 0))
            buffer.write(struct.pack('<B', player.get('Castle Z', 0) or 0))

        ph = heroes_by_color.get(player.get('Color'), {})
        buffer.write(struct.pack('<B', 1 if ph.get('Has Random Hero', False) else 0))

        hero_type = ph.get('Hero Type', None)
        hero_type_byte = 0xFF if hero_type is None else hero_type
        buffer.write(struct.pack('<B', hero_type_byte))

        if hero_type is not None:
            buffer.write(struct.pack('<B', ph.get('Hero Face', 0xFF)))
            hero_name = ph.get('Hero Name', '')
            hero_name_bytes = hero_name.encode('cp1252', errors='replace')
            buffer.write(struct.pack('<I', len(hero_name_bytes)))
            buffer.write(hero_name_bytes)
            buffer.write(struct.pack('<B', 0))

        if level_ab:
            buffer.write(struct.pack('<B', 0))
            buffer.write(struct.pack('<I', ph.get('Number of Heroes', 0) or 0))

    # === Special Victory Condition ===
    vic = map_data.get('Victory Condition', {})
    vic_type = vic.get('Type', 'None')
    if vic_type == 'None':
        buffer.write(struct.pack('<B', 0xFF))
    else:
        if isinstance(vic_type, str) and vic_type.startswith('0x'):
            vic_byte = int(vic_type, 16)
        else:
            vic_byte = 0
        buffer.write(struct.pack('<B', vic_byte))
        buffer.write(b'\x00\x00')
        artifact_id_bytes = 1 if not level_ab else 2
        creature_id_bytes = 1 if not level_ab else 2
        detail_size = {
            0: artifact_id_bytes, 1: creature_id_bytes + 4, 2: 5,
            3: 5, 4: 3, 5: 3, 6: 3, 7: 3, 8: 0, 9: 0, 10: 4
        }.get(vic_byte, 6)
        buffer.write(b'\x00' * detail_size)

    # === Special Loss Condition ===
    loss = map_data.get('Loss Condition', {})
    loss_type = loss.get('Type', 'None')
    if loss_type == 'None':
        buffer.write(struct.pack('<B', 0xFF))
    else:
        if isinstance(loss_type, str) and loss_type.startswith('0x'):
            loss_byte = int(loss_type, 16)
        else:
            loss_byte = 0
        buffer.write(struct.pack('<B', loss_byte))
        detail_size = {0: 3, 1: 3, 2: 2}.get(loss_byte, 3)
        buffer.write(b'\x00' * detail_size)

    # === Teams ===
    teams = map_data.get('Teams', {})
    num_teams = teams.get('Number of Teams', 0)
    buffer.write(struct.pack('<B', num_teams))

    if num_teams > 0:
        assignments = teams.get('Team Assignments', {})
        for color in PLAYER_COLORS:
            buffer.write(struct.pack('<B', assignments.get(color, 0)))

    # === Available Heroes ===
    avail_heroes = map_data.get('Available Heroes', {})
    bitfield = avail_heroes.get('Bitfield', '')
    if bitfield:
        buffer.write(bytes.fromhex(bitfield).ljust(heroes_bytes, b'\x00')[:heroes_bytes])
    else:
        buffer.write(b'\x00' * heroes_bytes)

    if level_ab:
        buffer.write(struct.pack('<I', 0))

    # === Disposed Heroes (SoD only) ===
    if level_sod:
        buffer.write(struct.pack('<B', 0))

    # === Reserved Bytes ===
    reserved = map_data.get('Reserved Bytes', '')
    if reserved:
        buffer.write(bytes.fromhex(reserved).ljust(31, b'\x00')[:31])
    else:
        buffer.write(b'\x00' * 31)

    # === Random Artifacts (AB and later) ===
    if level_ab:
        rand_artifacts = map_data.get('Random Artifacts', {})
        bitfield = rand_artifacts.get('Bitfield', '')
        if bitfield:
            buffer.write(bytes.fromhex(bitfield).ljust(artifacts_bytes, b'\x00')[:artifacts_bytes])
        else:
            buffer.write(b'\x00' * artifacts_bytes)

    # === Allowed Spells and Abilities (SoD only) ===
    if level_sod:
        spells = map_data.get('Allowed Spells', {}).get('Bitfield', '')
        if spells:
            buffer.write(bytes.fromhex(spells).ljust(spells_bytes, b'\x00')[:spells_bytes])
        else:
            buffer.write(b'\x00' * spells_bytes)
        skills = map_data.get('Allowed Abilities', {}).get('Bitfield', '')
        if skills:
            buffer.write(bytes.fromhex(skills).ljust(skills_bytes, b'\x00')[:skills_bytes])
        else:
            buffer.write(b'\x00' * skills_bytes)

    # === Rumors ===
    rumors = map_data.get('Rumors', {})
    rumors_list = rumors.get('Rumors', [])
    buffer.write(struct.pack('<I', len(rumors_list)))

    for rumor in rumors_list:
        name = rumor.get('Name', '')
        name_bytes = name.encode('cp1252', errors='replace')
        buffer.write(struct.pack('<I', len(name_bytes)))
        buffer.write(name_bytes)

        text = rumor.get('Text', '')
        text_bytes = text.encode('cp1252', errors='replace')
        buffer.write(struct.pack('<I', len(text_bytes)))
        buffer.write(text_bytes)

    # === Predefined Heroes (SoD only) ===
    if level_sod:
        for _ in range(156):
            buffer.write(struct.pack('<B', 0))

    # === Terrain grids ===
    def write_grid(grid, default_z):
        cell_map = OrderedDict()
        for cell in grid:
            x = cell.get('X', 0)
            y = cell.get('Y', 0)
            cell_map[(x, y)] = cell
        map_size = basic.get('Map Size', 72)
        for y in range(map_size):
            for x in range(map_size):
                cell = cell_map.get((x, y), OrderedDict())
                terrain_str = cell.get('Terrain Type', 'Dirt')
                terrain = TERRAIN_INVERSE.get(terrain_str, 0x00)
                if isinstance(terrain_str, str) and '0x' in terrain_str:
                    try:
                        terrain = int(terrain_str.split('0x')[1].split(')')[0], 16)
                    except:
                        terrain = 0x00
                buffer.write(struct.pack('<B', terrain))
                buffer.write(struct.pack('<B', cell.get('Terrain Picture', 0)))
                river_str = cell.get('River Type', 'None')
                river = RIVER_INVERSE.get(river_str, 0x00)
                if isinstance(river_str, str) and '0x' in river_str:
                    try:
                        river = int(river_str.split('0x')[1].split(')')[0], 16)
                    except:
                        river = 0x00
                buffer.write(struct.pack('<B', river))
                buffer.write(struct.pack('<B', cell.get('River Properties', 0)))
                road_str = cell.get('Road Type', 'None')
                road = ROAD_INVERSE.get(road_str, 0x00)
                if isinstance(road_str, str) and '0x' in road_str:
                    try:
                        road = int(road_str.split('0x')[1].split(')')[0], 16)
                    except:
                        road = 0x00
                buffer.write(struct.pack('<B', road))
                buffer.write(struct.pack('<B', cell.get('Road Properties', 0)))
                mirroring_str = cell.get('Mirroring', '0x00')
                if isinstance(mirroring_str, str) and mirroring_str.startswith('0x'):
                    mirroring = int(mirroring_str, 16)
                else:
                    mirroring = 0
                buffer.write(struct.pack('<B', mirroring))

    surface = map_data.get('Surface Map', {})
    write_grid(surface.get('Grid', []), 0)

    if has_underground:
        underground = map_data.get('Underground Map', {})
        write_grid(underground.get('Grid', []), 1)

    # === Objects ===
    objects = map_data.get('Objects', {})
    raw_data = objects.get('Raw Data', '')
    if raw_data:
        buffer.write(bytes.fromhex(raw_data))
    else:
        num_objects = objects.get('Number of Objects', 0)
        buffer.write(struct.pack('<I', num_objects))

    all_data = buffer.getvalue()

    compressor = zlib.compressobj(6, zlib.DEFLATED, -15)
    deflated = compressor.compress(all_data) + compressor.flush()
    crc = zlib.crc32(all_data) & 0xFFFFFFFF

    with open(output_path, 'wb') as f:
        f.write(b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b')
        f.write(deflated)
        f.write(struct.pack('<II', crc, len(all_data) & 0xFFFFFFFF))

    print("H3M file written to " + output_path)
