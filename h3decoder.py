"""
H3M File Parser for Heroes of Might and Magic III

This module reads .h3m files (which are gzip-compressed) and extracts information
into a structured dictionary format based on the specification from h3m_description.english.txt.

The H3M format uses LITTLE-ENDIAN for multi-byte integers.
"""

import gzip
import struct
from collections import OrderedDict
from io import BytesIO


def read_string(buffer, length):
    """Read a string of specified length from buffer."""
    if length <= 0:
        return ""
    raw = buffer.read(length)
    if len(raw) < length:
        # Pad with null bytes if we reach EOF
        raw = raw.ljust(length, b'\x00')
    cleaned = raw.rstrip(b'\x00')
    try:
        return cleaned.decode('utf-8', errors='replace')
    except:
        return cleaned.decode('latin-1', errors='replace')


def safe_read(buffer, size, default=b'\x00'):
    """Safely read bytes from buffer, return default if EOF."""
    data = buffer.read(size)
    if len(data) < size:
        # Pad with default bytes
        data = data.ljust(size, default[:size])
    return data


def parse_h3m(file_path):
    """
    Parse a Heroes of Might and Magic III map file (.h3m).
    
    Args:
        file_path: Path to the .h3m file
        
    Returns:
        OrderedDict: A structured dictionary containing map information.
    """
    data = OrderedDict()
    
    VERSION_MAP = {
        b'\x0E\x00\x00\x00': 'RoE (Restoration of Erathia)',
        b'\x15\x00\x00\x00': 'AB (Armageddon Blade)',
        b'\x1C\x00\x00\x00': 'SoD (Shadow of Death)'
    }
    
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
    
    MAX_HEROES_PER_PLAYER = 255
    MAX_CUSTOM_HEROES = 100
    MAX_RUMORS = 100
    MAX_OBJECTS = 10000
    
    # Read entire decompressed file into memory
    with gzip.open(file_path, 'rb') as f:
        all_data = f.read()
    
    # Create a buffer for parsing
    buffer = BytesIO(all_data)
    
    # === Basic Map Parameters ===
    section_basic = OrderedDict()
    
    format_id = safe_read(buffer, 4)
    section_basic['Format Identifier'] = format_id.hex().upper()
    section_basic['Version'] = VERSION_MAP.get(format_id, 'Unknown')
    
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
    
    data['Basic Parameters'] = section_basic
    
    # === Players' Attributes ===
    section_players = OrderedDict()
    players_list = []
    
    for color in PLAYER_COLORS:
        player = OrderedDict()
        player['Color'] = color
        player['Heroes Mastery Level Cap'] = struct.unpack('<B', safe_read(buffer, 1))[0]
        player['Human Playable'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        player['AI Playable'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        behavior = struct.unpack('<B', safe_read(buffer, 1))[0]
        player['Behavior'] = BEHAVIOR_MAP.get(behavior, 'Unknown')
        player['Has Defined Towns'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        
        owned_towns_bits = struct.unpack('<H', safe_read(buffer, 2))[0]
        player['Owned Towns'] = OrderedDict()
        for i, town in enumerate(TOWN_TYPES):
            player['Owned Towns'][town] = bool(owned_towns_bits & (1 << i))
        
        player['Owns Random Town'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        player['Main Town'] = bool(struct.unpack('<B', safe_read(buffer, 1))[0])
        
        create_hero = struct.unpack('<B', safe_read(buffer, 1))[0]
        if create_hero:
            town_type = struct.unpack('<B', safe_read(buffer, 1))[0]
            player['Town Type'] = town_type if town_type != 0xFF else 'Random'
            player['Castle X'] = struct.unpack('<B', safe_read(buffer, 1))[0]
            player['Castle Y'] = struct.unpack('<B', safe_read(buffer, 1))[0]
            player['Castle Z'] = struct.unpack('<B', safe_read(buffer, 1))[0]
        else:
            player['Town Type'] = None
            player['Castle X'] = None
            player['Castle Y'] = None
            player['Castle Z'] = None
        
        players_list.append(player)
    
    section_players['Players'] = players_list
    data['Players Attributes'] = section_players
    
    # === Player's Available Heroes ===
    section_heroes = OrderedDict()
    player_heroes_list = []
    
    for color in PLAYER_COLORS:
        hero_info = OrderedDict()
        hero_info['Color'] = color
        
        has_random = struct.unpack('<B', safe_read(buffer, 1))[0]
        hero_info['Has Random Hero'] = bool(has_random)
        
        hero_type = struct.unpack('<B', safe_read(buffer, 1))[0]
        hero_info['Hero Type'] = hero_type
        
        # Only read face/name if hero_type != 0xFF
        if hero_type != 0xFF:
            safe_read(buffer, 1)  # Hero face
            name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
            read_string(buffer, name_len)  # Hero name
            safe_read(buffer, 1)  # Unknown byte
        
        num_heroes = struct.unpack('<I', safe_read(buffer, 4))[0]
        hero_info['Number of Heroes'] = num_heroes
        
        # Limit number of heroes to prevent issues
        num_heroes = min(num_heroes, MAX_HEROES_PER_PLAYER)
        
        # Skip all hero details
        for j in range(num_heroes):
            safe_read(buffer, 1)  # ID
            name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
            read_string(buffer, name_len)
        
        player_heroes_list.append(hero_info)
    
    section_heroes['Player Heroes'] = player_heroes_list
    data['Player Heroes'] = section_heroes
    
    # === Special Victory Condition ===
    vic_type = struct.unpack('<B', safe_read(buffer, 1))[0]
    data['Victory Condition'] = OrderedDict([('Type', 'None' if vic_type == 0xFF else hex(vic_type))])
    safe_read(buffer, 6)  # Skip details
    
    # === Special Loss Condition ===
    loss_type = struct.unpack('<B', safe_read(buffer, 1))[0]
    data['Loss Condition'] = OrderedDict([('Type', 'None' if loss_type == 0xFF else hex(loss_type))])
    safe_read(buffer, 4)  # Skip details
    
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
    avail_bytes = safe_read(buffer, 20)
    data['Available Heroes'] = OrderedDict([('Bitfield', avail_bytes.hex())])
    safe_read(buffer, 4)  # 4 empty bytes
    
    # Skip custom heroes
    num_custom = struct.unpack('<B', safe_read(buffer, 1))[0]
    num_custom = min(num_custom, MAX_CUSTOM_HEROES)
    for i in range(num_custom):
        safe_read(buffer, 7)  # ID + Portrait + name length + players bitfield
        name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
        safe_read(buffer, name_len)
    
    # === Random Artifacts ===
    artifacts_bytes = safe_read(buffer, 18)
    data['Random Artifacts'] = OrderedDict([('Bitfield', artifacts_bytes.hex())])
    
    # === Rumors ===
    num_rumors = struct.unpack('<I', safe_read(buffer, 4))[0]
    num_rumors = min(num_rumors, MAX_RUMORS)
    rumors_list = []
    for i in range(num_rumors):
        name_len = struct.unpack('<I', safe_read(buffer, 4))[0]
        name = read_string(buffer, name_len)
        text_len = struct.unpack('<I', safe_read(buffer, 4))[0]
        text = read_string(buffer, text_len)
        rumors_list.append(OrderedDict([('Name', name), ('Text', text)]))
    data['Rumors'] = OrderedDict([('Number of Rumors', num_rumors), ('Rumors', rumors_list)])
    
    # === Hero Settings (skip) ===
    for i in range(156):
        has_settings_data = safe_read(buffer, 1)
        has_settings = struct.unpack('<B', has_settings_data)[0]
        if has_settings:
            safe_read(buffer, 50)  # Skip settings
    data['Hero Settings'] = OrderedDict([('Note', 'Skipped for performance')])
    
    # === Reserved Bytes ===
    reserved = safe_read(buffer, 31)
    data['Reserved Bytes'] = reserved.hex()
    
    # === Surface Map ===
    section_surface = OrderedDict()
    surface_size = map_size * map_size * 7
    surface_raw = safe_read(buffer, surface_size)
    
    section_surface['Size'] = surface_size
    section_surface['Raw Data Length'] = len(surface_raw)
    
    # Parse grid
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
        num_objects = min(num_objects, MAX_OBJECTS)
        data['Objects'] = OrderedDict([('Number of Objects', num_objects)])
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
    print("Surface Map: " + str(surface.get('Size', 0)) + " bytes, " + str(len(surface.get('Grid', []))) + " cells")
    if basic.get('Has Underground'):
        underground = map_data.get('Underground Map', {})
        print("Underground Map: " + str(underground.get('Size', 0)) + " bytes, " + str(len(underground.get('Grid', []))) + " cells")
    
    objects = map_data.get('Objects', {})
    print("Objects: " + str(objects.get('Number of Objects', 'Unknown')))
    
    rumors = map_data.get('Rumors', {})
    print("Rumors: " + str(rumors.get('Number of Rumors', 0)))
    print("=" * 60)


def get_terrain_grid(map_data):
    """Extract the surface terrain grid as a 2D array."""
    surface = map_data.get('Surface Map', {})
    grid = surface.get('Grid', [])
    map_size = map_data.get('Basic Parameters', {}).get('Map Size', 0)
    
    if not grid or map_size == 0:
        return []
    
    terrain_2d = []
    for y in range(map_size):
        row = []
        for x in range(map_size):
            idx = y * map_size + x
            if idx < len(grid):
                row.append(grid[idx]['Terrain Type'])
            else:
                row.append('Unknown')
        terrain_2d.append(row)
    
    return terrain_2d


def save_to_json(map_data, output_path):
    """Save map data to a JSON file."""
    import json
    
    def convert_dict(d):
        if isinstance(d, OrderedDict):
            return {k: convert_dict(v) for k, v in d.items()}
        elif isinstance(d, list):
            return [convert_dict(item) for item in d]
        elif isinstance(d, bytes):
            return d.hex()
        else:
            return d
    
    json_data = convert_dict(map_data)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print("Map data saved to " + output_path)
