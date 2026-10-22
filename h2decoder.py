"""
FH2M File Parser for fheroes2 (Heroes of Might and Magic II)

This module reads native .fh2m map files from the fheroes2 engine
(https://github.com/ihhub/fheroes2) and extracts information into a structured
dictionary format based on the specification from h2m_description.english.txt
and the reference implementation in src/fheroes2/maps/map_format_info.cpp.

The FH2M format uses BIG-ENDIAN for multi-byte integers.
Only the base map parameters are stored uncompressed: the rest of the file is
a single zlib (deflate) compressed blob without a length prefix.
"""

import struct
import zlib
from collections import OrderedDict
from io import BytesIO

MAGIC_WORD = b"h2map\x00"
MIN_FILE_SIZE = 512

MINIMUM_SUPPORTED_VERSION = 2
CURRENT_SUPPORTED_VERSION = 13

DIFFICULTY_MAP = {0: "Easy", 1: "Normal", 2: "Hard", 3: "Expert", 4: "Impossible"}

PLAYER_COLOR_NAMES = ["Blue", "Green", "Red", "Yellow", "Orange", "Purple"]

RACE_MAP = {0: "Random", 1: "Knight", 2: "Barbarian", 3: "Sorceress",
            4: "Warlock", 5: "Wizard", 6: "Necromancer"}

RACE_MAP_REVERSE = {name: value for value, name in RACE_MAP.items()}

DIFFICULTY_MAP_REVERSE = {name: value for value, name in DIFFICULTY_MAP.items()}

OBJECT_GROUP_NAMES = [
    "NONE", "ROADS", "STREAMS", "LANDSCAPE_MOUNTAINS", "LANDSCAPE_ROCKS",
    "LANDSCAPE_TREES", "LANDSCAPE_WATER", "LANDSCAPE_MISCELLANEOUS",
    "LANDSCAPE_TOWN_BASEMENTS", "LANDSCAPE_FLAGS", "ADVENTURE_ARTIFACTS",
    "ADVENTURE_DWELLINGS", "ADVENTURE_MINES", "ADVENTURE_POWER_UPS",
    "ADVENTURE_TREASURES", "ADVENTURE_WATER", "ADVENTURE_MISCELLANEOUS",
    "KINGDOM_HEROES", "KINGDOM_TOWNS", "MONSTERS", "MAP_EXTRAS",
]

RESOURCE_NAMES = ["wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"]


def read_string(buffer):
    """Read a length-prefixed (4 bytes, big-endian) string from buffer."""
    length = read_u32(buffer)
    if length <= 0:
        return ""
    raw = buffer.read(length)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", errors="replace")


def read_u8(buffer):
    data = buffer.read(1)
    if len(data) < 1:
        raise ValueError("Unexpected end of file")
    return data[0]


def read_u16(buffer):
    data = buffer.read(2)
    if len(data) < 2:
        raise ValueError("Unexpected end of file")
    return struct.unpack(">H", data)[0]


def read_u32(buffer):
    data = buffer.read(4)
    if len(data) < 4:
        raise ValueError("Unexpected end of file")
    return struct.unpack(">I", data)[0]


def read_i8(buffer):
    return struct.unpack(">b", buffer.read(1))[0]


def read_i16(buffer):
    data = buffer.read(2)
    if len(data) < 2:
        raise ValueError("Unexpected end of file")
    return struct.unpack(">h", data)[0]


def read_i32(buffer):
    data = buffer.read(4)
    if len(data) < 4:
        raise ValueError("Unexpected end of file")
    return struct.unpack(">i", data)[0]


def read_list(buffer, read_item):
    """Read a u32-count-prefixed list of items."""
    count = read_u32(buffer)
    return [read_item(buffer) for _ in range(count)]


def read_map(buffer, read_key, read_value):
    """Read a u32-count-prefixed map of key/value pairs."""
    count = read_u32(buffer)
    result = OrderedDict()
    for _ in range(count):
        key = read_key(buffer)
        result[key] = read_value(buffer)
    return result


def read_funds(buffer):
    """Read a Funds (resource) structure: 7 big-endian int32 values."""
    funds = OrderedDict()
    for name in RESOURCE_NAMES:
        funds[name] = read_i32(buffer)
    return funds


def color_names(mask):
    """Convert a player color bit mask into a list of color names."""
    names = []
    for bit, name in enumerate(PLAYER_COLOR_NAMES):
        if mask & (1 << bit):
            names.append(name)
    return names


def object_group_name(group_id):
    if 0 <= group_id < len(OBJECT_GROUP_NAMES):
        return OBJECT_GROUP_NAMES[group_id]
    return "UNKNOWN_{}".format(group_id)


def read_tile_object(buffer):
    obj = OrderedDict()
    obj["id"] = read_u32(buffer)
    group_id = read_u8(buffer)
    obj["group"] = object_group_name(group_id)
    obj["index"] = read_u32(buffer)
    return obj


def read_tile(buffer):
    tile = OrderedDict()
    tile["terrainIndex"] = read_u16(buffer)
    tile["terrainFlags"] = read_u8(buffer)
    tile["objects"] = read_list(buffer, read_tile_object)
    return tile


def read_daily_event(buffer):
    event = OrderedDict()
    event["message"] = read_string(buffer)
    event["humanPlayerColors"] = color_names(read_u8(buffer))
    event["computerPlayerColors"] = color_names(read_u8(buffer))
    event["firstOccurrenceDay"] = read_u32(buffer)
    event["repeatPeriodInDays"] = read_u32(buffer)
    event["resources"] = read_funds(buffer)
    return event


def read_castle_metadata(buffer):
    metadata = OrderedDict()
    metadata["customName"] = read_string(buffer)
    metadata["defenderMonsterType"] = read_list(buffer, read_i32)
    metadata["defenderMonsterCount"] = read_list(buffer, read_i32)
    metadata["customBuildings"] = read_u8(buffer) != 0
    metadata["builtBuildings"] = read_list(buffer, read_u32)
    metadata["bannedBuildings"] = read_list(buffer, read_u32)
    metadata["mustHaveSpells"] = read_map(buffer, read_u8, read_i32)
    metadata["bannedSpells"] = read_list(buffer, read_i32)
    metadata["availableToHireMonsterCount"] = read_list(buffer, read_i32)
    return metadata


def read_hero_metadata(buffer):
    metadata = OrderedDict()
    metadata["customName"] = read_string(buffer)
    metadata["customPortrait"] = read_i32(buffer)
    metadata["armyMonsterType"] = read_list(buffer, read_i32)
    metadata["armyMonsterCount"] = read_list(buffer, read_i32)
    metadata["artifacts"] = read_list(buffer, read_i32)
    metadata["artifactMetadata"] = read_list(buffer, read_i32)
    metadata["availableSpells"] = read_list(buffer, read_i32)
    metadata["isOnPatrol"] = read_u8(buffer) != 0
    metadata["patrolRadius"] = read_u8(buffer)
    metadata["secondarySkill"] = read_list(buffer, read_i8)
    metadata["secondarySkillLevel"] = read_list(buffer, read_u8)
    metadata["customLevel"] = read_i16(buffer)
    metadata["customExperience"] = read_i32(buffer)
    metadata["customAttack"] = read_i16(buffer)
    metadata["customDefense"] = read_i16(buffer)
    metadata["customKnowledge"] = read_i16(buffer)
    metadata["customSpellPower"] = read_i16(buffer)
    metadata["magicPoints"] = read_i16(buffer)
    race_id = read_u8(buffer)
    metadata["raceId"] = race_id
    metadata["race"] = RACE_MAP.get(race_id, "Unknown")
    return metadata


def read_sphinx_metadata(buffer):
    metadata = OrderedDict()
    metadata["riddle"] = read_string(buffer)
    metadata["answers"] = read_list(buffer, read_string)
    metadata["artifact"] = read_i32(buffer)
    metadata["artifactMetadata"] = read_i32(buffer)
    metadata["resources"] = read_funds(buffer)
    return metadata


def read_sign_metadata(buffer):
    metadata = OrderedDict()
    metadata["message"] = read_string(buffer)
    return metadata


def read_adventure_map_event_metadata(buffer):
    metadata = OrderedDict()
    metadata["message"] = read_string(buffer)
    metadata["humanPlayerColors"] = color_names(read_u8(buffer))
    metadata["computerPlayerColors"] = color_names(read_u8(buffer))
    metadata["isRecurringEvent"] = read_u8(buffer) != 0
    metadata["artifact"] = read_i32(buffer)
    metadata["artifactMetadata"] = read_i32(buffer)
    metadata["resources"] = read_funds(buffer)
    metadata["attack"] = read_i16(buffer)
    metadata["defense"] = read_i16(buffer)
    metadata["knowledge"] = read_i16(buffer)
    metadata["spellPower"] = read_i16(buffer)
    metadata["experience"] = read_i32(buffer)
    metadata["secondarySkill"] = read_u8(buffer)
    metadata["secondarySkillLevel"] = read_u8(buffer)
    metadata["monsterType"] = read_i32(buffer)
    metadata["monsterCount"] = read_i32(buffer)
    return metadata


def read_selection_object_metadata(buffer):
    metadata = OrderedDict()
    metadata["selectedItems"] = read_list(buffer, read_i32)
    return metadata


def read_capturable_object_metadata(buffer):
    metadata = OrderedDict()
    metadata["ownerColor"] = color_names(read_u8(buffer))
    return metadata


def read_monster_metadata(buffer):
    metadata = OrderedDict()
    metadata["count"] = read_i32(buffer)
    metadata["joinCondition"] = read_i32(buffer)
    metadata["isWeeklyGrowthDisabled"] = read_u8(buffer) != 0
    metadata["selected"] = read_list(buffer, read_i32)
    return metadata


def read_artifact_metadata(buffer):
    metadata = OrderedDict()
    metadata["radius"] = read_i32(buffer)
    metadata["captureCondition"] = read_i32(buffer)
    metadata["selected"] = read_list(buffer, read_i32)
    return metadata


def read_resource_metadata(buffer):
    metadata = OrderedDict()
    metadata["count"] = read_i32(buffer)
    return metadata


def read_standard_object_metadata(buffer):
    metadata = OrderedDict()
    metadata["metadata"] = read_list(buffer, read_i32)
    return metadata


def read_translation_sphinx_metadata(buffer):
    metadata = OrderedDict()
    metadata["riddle"] = read_string(buffer)
    metadata["answers"] = read_list(buffer, read_string)
    return metadata


def read_translation_base_map_metadata(buffer):
    metadata = OrderedDict()
    metadata["name"] = read_string(buffer)
    metadata["description"] = read_string(buffer)
    metadata["creatorNotes"] = read_string(buffer)
    return metadata


def read_translation_format(buffer):
    metadata = OrderedDict()
    metadata["dailyEvents"] = read_list(buffer, read_string)
    metadata["rumors"] = read_list(buffer, read_string)
    metadata["castleMetadata"] = read_map(buffer, read_u32, read_string)
    metadata["heroMetadata"] = read_map(buffer, read_u32, read_string)
    metadata["sphinxMetadata"] = read_map(buffer, read_u32, read_translation_sphinx_metadata)
    metadata["signMetadata"] = read_map(buffer, read_u32, read_string)
    metadata["adventureMapEventMetadata"] = read_map(buffer, read_u32, read_string)
    return metadata


def parse_base_map(buffer, data, version):
    """Read the uncompressed BaseMapFormat part of the file."""
    data["isCampaign"] = read_u8(buffer) != 0
    data["difficulty"] = DIFFICULTY_MAP.get(read_u8(buffer), "Unknown")
    data["availablePlayerColors"] = color_names(read_u8(buffer))
    data["humanPlayerColors"] = color_names(read_u8(buffer))
    data["computerPlayerColors"] = color_names(read_u8(buffer))
    data["alliances"] = read_list(buffer, read_u8)
    race_ids = read_list(buffer, read_u8)
    data["playerRaceId"] = race_ids
    data["playerRace"] = [RACE_MAP.get(race, "Unknown") for race in race_ids]
    data["victoryConditionType"] = read_u8(buffer)
    data["isVictoryConditionApplicableForAI"] = read_u8(buffer) != 0
    data["allowNormalVictory"] = read_u8(buffer) != 0
    data["victoryConditionMetadata"] = read_list(buffer, read_u32)
    data["lossConditionType"] = read_u8(buffer)
    data["lossConditionMetadata"] = read_list(buffer, read_u32)

    width = read_i32(buffer)
    if width <= 0:
        raise ValueError("Invalid map size: {}".format(width))
    data["width"] = width
    data["height"] = width

    data["mainLanguage"] = read_u8(buffer)
    data["name"] = read_string(buffer)
    data["description"] = read_string(buffer)

    if version >= 9:
        data["creatorNotes"] = read_string(buffer)

    if version >= 11:
        data["translations"] = read_map(buffer, read_u8, read_translation_base_map_metadata)


def parse_compressed_section(buffer, data, version):
    """Read the zlib-compressed MapFormat part of the file."""
    data["additionalInfo"] = read_list(buffer, read_u32)

    tile_count = data["width"] * data["height"]
    data["tiles"] = read_list(buffer, read_tile)
    if len(data["tiles"]) != tile_count:
        raise ValueError("Invalid number of tiles: expected {}, got {}".format(tile_count, len(data["tiles"])))

    data["dailyEvents"] = read_list(buffer, read_daily_event)
    data["rumors"] = read_list(buffer, read_string)

    standard_metadata = None
    if version < 10:
        standard_metadata = read_map(buffer, read_u32, read_standard_object_metadata)

    data["castleMetadata"] = read_map(buffer, read_u32, read_castle_metadata)
    data["heroMetadata"] = read_map(buffer, read_u32, read_hero_metadata)
    data["sphinxMetadata"] = read_map(buffer, read_u32, read_sphinx_metadata)
    data["signMetadata"] = read_map(buffer, read_u32, read_sign_metadata)
    data["adventureMapEventMetadata"] = read_map(buffer, read_u32, read_adventure_map_event_metadata)
    data["selectionObjectMetadata"] = read_map(buffer, read_u32, read_selection_object_metadata)

    if version > 8:
        data["capturableObjectsMetadata"] = read_map(buffer, read_u32, read_capturable_object_metadata)

    if version > 9:
        data["monsterMetadata"] = read_map(buffer, read_u32, read_monster_metadata)
        data["artifactMetadata"] = read_map(buffer, read_u32, read_artifact_metadata)
        data["resourceMetadata"] = read_map(buffer, read_u32, read_resource_metadata)
    else:
        # In versions below 10, monster/artifact/resource information was
        # stored in a single deprecated StandardObjectMetadata map.
        data["standardObjectMetadata"] = standard_metadata

    if version >= 11:
        data["translationInfo"] = read_map(buffer, read_u8, read_translation_format)


def parse_fh2m(file_path):
    """
    Parse a fheroes2 native map file (.fh2m).

    Supports map format versions 2 to 13.

    Args:
        file_path: Path to the .fh2m file

    Returns:
        OrderedDict: A structured dictionary containing map information.
    """
    with open(file_path, "rb") as f:
        all_data = f.read()

    if len(all_data) < MIN_FILE_SIZE:
        raise ValueError("File is too small to be a valid FH2M map")

    if all_data[:len(MAGIC_WORD)] != MAGIC_WORD:
        raise ValueError("Not a FH2M map file: invalid magic word")

    buffer = BytesIO(all_data)
    buffer.seek(len(MAGIC_WORD))

    version = read_u16(buffer)
    if version < MINIMUM_SUPPORTED_VERSION or version > CURRENT_SUPPORTED_VERSION:
        raise ValueError("Unsupported map format version: {}".format(version))

    data = OrderedDict()
    data["version"] = version

    parse_base_map(buffer, data, version)

    compressed_data = buffer.read()
    if not compressed_data:
        raise ValueError("Missing compressed data section")

    try:
        decompressed = zlib.decompress(compressed_data)
    except zlib.error as e:
        raise ValueError("Failed to decompress map data: {}".format(e))

    parse_compressed_section(BytesIO(decompressed), data, version)

    return data


def write_string(out, value):
    """Write a length-prefixed (4 bytes, big-endian) string."""
    encoded = value.encode("utf-8")
    out += struct.pack(">I", len(encoded))
    out += encoded


def write_u8(out, value):
    out += struct.pack(">B", value)


def write_u16(out, value):
    out += struct.pack(">H", value)


def write_u32(out, value):
    out += struct.pack(">I", value)


def write_i8(out, value):
    out += struct.pack(">b", value)


def write_i16(out, value):
    out += struct.pack(">h", value)


def write_i32(out, value):
    out += struct.pack(">i", value)


def write_list(out, items, write_item):
    """Write a u32-count-prefixed list of items."""
    write_u32(out, len(items))
    for item in items:
        write_item(out, item)


def write_map(out, mapping, write_key, write_value):
    """Write a u32-count-prefixed map of key/value pairs."""
    write_u32(out, len(mapping))
    for key, value in mapping.items():
        if isinstance(key, str) and key.isdigit():
            key = int(key)
        write_key(out, key)
        write_value(out, value)


def color_mask(names):
    """Convert a list of color names into a player color bit mask."""
    mask = 0
    for name in names:
        try:
            mask |= 1 << PLAYER_COLOR_NAMES.index(name)
        except ValueError:
            pass
    return mask


def object_group_id(group_name):
    try:
        return OBJECT_GROUP_NAMES.index(group_name)
    except ValueError:
        return 0


def write_tile_object(out, obj):
    write_u32(out, obj["id"])
    write_u8(out, object_group_id(obj["group"]))
    write_u32(out, obj["index"])


def write_tile(out, tile):
    write_u16(out, tile["terrainIndex"])
    write_u8(out, tile["terrainFlags"])
    write_list(out, tile["objects"], write_tile_object)


def write_daily_event(out, event):
    write_string(out, event["message"])
    write_u8(out, color_mask(event["humanPlayerColors"]))
    write_u8(out, color_mask(event["computerPlayerColors"]))
    write_u32(out, event["firstOccurrenceDay"])
    write_u32(out, event["repeatPeriodInDays"])
    write_funds(out, event["resources"])


def write_funds(out, funds):
    for name in RESOURCE_NAMES:
        write_i32(out, funds[name])


def write_castle_metadata(out, metadata):
    write_string(out, metadata["customName"])
    write_list(out, metadata["defenderMonsterType"], write_i32)
    write_list(out, metadata["defenderMonsterCount"], write_i32)
    write_u8(out, 1 if metadata["customBuildings"] else 0)
    write_list(out, metadata["builtBuildings"], write_u32)
    write_list(out, metadata["bannedBuildings"], write_u32)
    write_map(out, metadata["mustHaveSpells"], write_u8, write_i32)
    write_list(out, metadata["bannedSpells"], write_i32)
    write_list(out, metadata["availableToHireMonsterCount"], write_i32)


def write_hero_metadata(out, metadata):
    write_string(out, metadata["customName"])
    write_i32(out, metadata["customPortrait"])
    write_list(out, metadata["armyMonsterType"], write_i32)
    write_list(out, metadata["armyMonsterCount"], write_i32)
    write_list(out, metadata["artifacts"], write_i32)
    write_list(out, metadata["artifactMetadata"], write_i32)
    write_list(out, metadata["availableSpells"], write_i32)
    write_u8(out, 1 if metadata["isOnPatrol"] else 0)
    write_u8(out, metadata["patrolRadius"])
    write_list(out, metadata["secondarySkill"], write_i8)
    write_list(out, metadata["secondarySkillLevel"], write_u8)
    write_i16(out, metadata["customLevel"])
    write_i32(out, metadata["customExperience"])
    write_i16(out, metadata["customAttack"])
    write_i16(out, metadata["customDefense"])
    write_i16(out, metadata["customKnowledge"])
    write_i16(out, metadata["customSpellPower"])
    write_i16(out, metadata["magicPoints"])
    write_u8(out, metadata.get("raceId", RACE_MAP_REVERSE.get(metadata["race"], 0)))


def write_sphinx_metadata(out, metadata):
    write_string(out, metadata["riddle"])
    write_list(out, metadata["answers"], write_string)
    write_i32(out, metadata["artifact"])
    write_i32(out, metadata["artifactMetadata"])
    write_funds(out, metadata["resources"])


def write_sign_metadata(out, metadata):
    write_string(out, metadata["message"])


def write_adventure_map_event_metadata(out, metadata):
    write_string(out, metadata["message"])
    write_u8(out, color_mask(metadata["humanPlayerColors"]))
    write_u8(out, color_mask(metadata["computerPlayerColors"]))
    write_u8(out, 1 if metadata["isRecurringEvent"] else 0)
    write_i32(out, metadata["artifact"])
    write_i32(out, metadata["artifactMetadata"])
    write_funds(out, metadata["resources"])
    write_i16(out, metadata["attack"])
    write_i16(out, metadata["defense"])
    write_i16(out, metadata["knowledge"])
    write_i16(out, metadata["spellPower"])
    write_i32(out, metadata["experience"])
    write_u8(out, metadata["secondarySkill"])
    write_u8(out, metadata["secondarySkillLevel"])
    write_i32(out, metadata["monsterType"])
    write_i32(out, metadata["monsterCount"])


def write_selection_object_metadata(out, metadata):
    write_list(out, metadata["selectedItems"], write_i32)


def write_capturable_object_metadata(out, metadata):
    write_u8(out, color_mask(metadata["ownerColor"]))


def write_monster_metadata(out, metadata):
    write_i32(out, metadata["count"])
    write_i32(out, metadata["joinCondition"])
    write_u8(out, 1 if metadata["isWeeklyGrowthDisabled"] else 0)
    write_list(out, metadata["selected"], write_i32)


def write_artifact_metadata(out, metadata):
    write_i32(out, metadata["radius"])
    write_i32(out, metadata["captureCondition"])
    write_list(out, metadata["selected"], write_i32)


def write_resource_metadata(out, metadata):
    write_i32(out, metadata["count"])


def write_standard_object_metadata(out, metadata):
    write_list(out, metadata["metadata"], write_i32)


def write_translation_sphinx_metadata(out, metadata):
    write_string(out, metadata["riddle"])
    write_list(out, metadata["answers"], write_string)


def write_translation_base_map_metadata(out, metadata):
    write_string(out, metadata["name"])
    write_string(out, metadata["description"])
    write_string(out, metadata["creatorNotes"])


def write_translation_format(out, metadata):
    write_list(out, metadata["dailyEvents"], write_string)
    write_list(out, metadata["rumors"], write_string)
    write_map(out, metadata["castleMetadata"], write_u32, write_string)
    write_map(out, metadata["heroMetadata"], write_u32, write_string)
    write_map(out, metadata["sphinxMetadata"], write_u32, write_translation_sphinx_metadata)
    write_map(out, metadata["signMetadata"], write_u32, write_string)
    write_map(out, metadata["adventureMapEventMetadata"], write_u32, write_string)


def write_base_map(out, data):
    """Write the uncompressed BaseMapFormat part of the file."""
    version = data["version"]
    write_u16(out, version)
    write_u8(out, 1 if data["isCampaign"] else 0)
    write_u8(out, DIFFICULTY_MAP_REVERSE.get(data["difficulty"], 1))
    write_u8(out, color_mask(data["availablePlayerColors"]))
    write_u8(out, color_mask(data["humanPlayerColors"]))
    write_u8(out, color_mask(data["computerPlayerColors"]))
    write_list(out, data["alliances"], write_u8)
    if "playerRaceId" in data:
        race_ids = data["playerRaceId"]
    else:
        race_ids = [RACE_MAP_REVERSE.get(race, 0) for race in data["playerRace"]]
    write_list(out, race_ids, write_u8)
    write_u8(out, data["victoryConditionType"])
    write_u8(out, 1 if data["isVictoryConditionApplicableForAI"] else 0)
    write_u8(out, 1 if data["allowNormalVictory"] else 0)
    write_list(out, data["victoryConditionMetadata"], write_u32)
    write_u8(out, data["lossConditionType"])
    write_list(out, data["lossConditionMetadata"], write_u32)
    write_i32(out, data["width"])
    write_u8(out, data["mainLanguage"])
    write_string(out, data["name"])
    write_string(out, data["description"])
    if version >= 9:
        write_string(out, data["creatorNotes"])
    if version >= 11:
        write_map(out, data["translations"], write_u8, write_translation_base_map_metadata)


def write_compressed_section(out, data):
    """Write the zlib-compressed MapFormat part of the file."""
    version = data["version"]
    write_list(out, data["additionalInfo"], write_u32)
    write_list(out, data["tiles"], write_tile)
    write_list(out, data["dailyEvents"], write_daily_event)
    write_list(out, data["rumors"], write_string)

    if version < 10:
        write_map(out, data.get("standardObjectMetadata", {}), write_u32, write_standard_object_metadata)

    write_map(out, data["castleMetadata"], write_u32, write_castle_metadata)
    write_map(out, data["heroMetadata"], write_u32, write_hero_metadata)
    write_map(out, data["sphinxMetadata"], write_u32, write_sphinx_metadata)
    write_map(out, data["signMetadata"], write_u32, write_sign_metadata)
    write_map(out, data["adventureMapEventMetadata"], write_u32, write_adventure_map_event_metadata)
    write_map(out, data["selectionObjectMetadata"], write_u32, write_selection_object_metadata)

    if version > 8:
        write_map(out, data["capturableObjectsMetadata"], write_u32, write_capturable_object_metadata)

    if version > 9:
        write_map(out, data["monsterMetadata"], write_u32, write_monster_metadata)
        write_map(out, data["artifactMetadata"], write_u32, write_artifact_metadata)
        write_map(out, data["resourceMetadata"], write_u32, write_resource_metadata)

    if version >= 11:
        write_map(out, data["translationInfo"], write_u8, write_translation_format)


def write_fh2m(map_data, output_path):
    """
    Write a fheroes2 native map file (.fh2m) from a structured dictionary,
    as produced by parse_fh2m and the JSON files in outputjson/.

    Args:
        map_data: Dictionary containing map information.
        output_path: Path of the .fh2m file to write.
    """
    version = map_data.get("version", CURRENT_SUPPORTED_VERSION)
    map_data = dict(map_data)
    map_data["version"] = version

    if version < MINIMUM_SUPPORTED_VERSION or version > CURRENT_SUPPORTED_VERSION:
        raise ValueError("Unsupported map format version: {}".format(version))

    base = bytearray()
    write_base_map(base, map_data)

    compressed_section = bytearray()
    write_compressed_section(compressed_section, map_data)

    content = MAGIC_WORD + bytes(base) + zlib.compress(bytes(compressed_section), 6)
    if len(content) < MIN_FILE_SIZE:
        content += b"\x00" * (MIN_FILE_SIZE - len(content))

    with open(output_path, "wb") as f:
        f.write(content)
