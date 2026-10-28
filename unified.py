"""
Unified map format converters.

Converts the JSON produced by h3decoder.py (parse_h3m) and h2decoder.py
(parse_fh2m) into the unified JSON format described in
heroes_json_description.english.txt. See example_unified.json for a sample.

The unified format keeps the common ground between Heroes of Might and
Magic III maps and fheroes2 native maps: identification, players, teams,
victory and loss conditions, rumors, daily events (fh2m only) and the
normalized terrain grid. Game-specific structures without a common
representation are dropped (see the description document).
"""

import struct
from collections import OrderedDict

from correspondence import (
    FH2M_ARTIFACT_NAMES,
    FH2M_RACE_DWELLING_MONSTERS,
    H3M_ARTIFACT_NAMES,
    H3M_CREATURE_NAMES,
    H3M_HERO_NAMES,
    H3M_PLAYER_COLOR_NAMES,
    H3M_SECONDARY_SKILL_NAMES,
    H3M_SPELL_NAMES,
    H3M_TO_FH2M_MONSTERS,
    FH2M_TOWN_RACE_ORDER,
    H3M_TOWN_TYPE_TO_FH2M_RACE,
    FH2M_RESOURCE_ORDER,
    FH2M_SPELL_SCROLL_ID,
    fh2m_portrait_name,
    fh2m_race_name,
    fh2m_town_race,
    fh2m_artifact_name,
    fh2m_building_name,
    fh2m_join_condition_name,
    fh2m_monster_name,
    fh2m_secondary_skill_name,
    fh2m_skill_level_name,
    fh2m_spell_name,
)

H3M_VICTORY_CONDITIONS = {
    0x0: "obtainArtifact",
    0x1: "accumulateCreatures",
    0x2: "collectGold",
    0x3: "upgradeTown",
    0x4: "buildGrail",
    0x5: "killHero",
    0x6: "captureTown",
    0x7: "defeatMonster",
    0x8: "flagDwellings",
    0x9: "flagMines",
    0xA: "transportArtifact",
}

H3M_LOSS_CONDITIONS = {
    0x0: "loseTown",
    0x1: "loseHero",
    0x2: "outOfTime",
}

FH2M_VICTORY_CONDITIONS = {
    0: "defeatEveryone",
    1: "captureTown",
    2: "killHero",
    3: "obtainArtifact",
    4: "defeatOtherSide",
    5: "collectGold",
}

FH2M_LOSS_CONDITIONS = {
    0: "loseEverything",
    1: "loseTown",
    2: "loseHero",
    3: "outOfTime",
}

FH2M_PLAYER_COLORS = ["Blue", "Green", "Red", "Yellow", "Orange", "Purple"]

# h3m town type -> unified race (Heroes II hero races)
# h3m town type -> unified race; the unified race set is the union of
# both games: Inferno, Fortress and Conflux exist in the unified format
# but have no fh2m playerRace equivalent
H3M_TOWN_RACES = {
    "Castle": "Knight",
    "Rampart": "Sorceress",
    "Tower": "Wizard",
    "Inferno": "Warlock",
    "Necropolis": "Necromancer",
    "Dungeon": "Warlock",
    "Stronghold": "Barbarian",
    "Fortress": "Barbarian",
    "Conflux": "Sorceress",
}

# fh2m race -> unified race (identity, kept explicit)
FH2M_RACES = {
    "Random": "Random",
    "Knight": "Knight",
    "Barbarian": "Barbarian",
    "Sorceress": "Sorceress",
    "Warlock": "Warlock",
    "Wizard": "Wizard",
    "Necromancer": "Necromancer",
}

# unified race -> fh2m race code
UNIFIED_TO_FH2M_RACE_CODES = {
    "Random": 0,
    "Knight": 1,
    "Barbarian": 2,
    "Sorceress": 3,
    "Warlock": 4,
    "Wizard": 5,
    "Necromancer": 6,
}

# h3m terrain -> unified terrain. The h3m Sand terrain converts
# to the Heroes II Desert terrain (and back); the unified Beach
# terrain converts back to the h3m Sand terrain.
H3M_TERRAINS = {
    "Dirt": "Dirt",
    "Sand": "Desert",
    "Grass": "Grass",
    "Snow": "Snow",
    "Swamp": "Swamp",
    "Rough": "Wasteland",
    "Subterranean": "Subterranean",
    "Lava": "Lava",
    "Water": "Water",
    "Rock": "Rock",
}

# fh2m terrain image index boundaries (see fheroes2 maps/ground.cpp:
# getGroundByImageIndex) -> unified terrain
FH2M_TERRAIN_INDEX_RANGES = (
    (30, "Water"),
    (92, "Grass"),
    (146, "Snow"),
    (208, "Swamp"),
    (262, "Lava"),
    (321, "Desert"),
    (361, "Dirt"),
    (415, "Wasteland"),
    (432, "Beach"),
    (float("inf"), "Rock"),
)


def _fh2m_terrain_name(terrain_index):
    for start_index, name in FH2M_TERRAIN_INDEX_RANGES:
        if terrain_index < start_index:
            return name
    return "Rock"


def _h3m_terrain_name(source_terrain):
    if source_terrain in H3M_TERRAINS:
        return H3M_TERRAINS[source_terrain]
    # Unknown values are kept as-is ("Unknown (0xNN)")
    return source_terrain


def _h3m_source_race(player):
    """Pick the most representative source race for an h3m player."""
    owned_towns = [town for town, owned in player.get("Owned Towns", {}).items() if owned]
    if not owned_towns or player.get("Owns Random Town", False):
        return "Random"
    if len(owned_towns) == 1:
        return owned_towns[0]
    # Several town types owned: no single faction can represent the player
    return "Multiple"


def _h3m_unified_race(source_race):
    if source_race == "Random":
        return "Random"
    return H3M_TOWN_RACES.get(source_race)


def convert_h3m_to_unified(map_data):
    """
    Convert the JSON produced by parse_h3m into the unified format.

    Args:
        map_data: Dictionary as returned by parse_h3m.

    Returns:
        OrderedDict: The map in the unified format.
    """
    unified = OrderedDict()

    basic = map_data.get("Basic Parameters", {})
    version_name = basic.get("Version", "")
    if "RoE" in version_name:
        source_version = "RoE"
    elif "AB" in version_name:
        source_version = "AB"
    elif "SoD" in version_name:
        source_version = "SoD"
    else:
        source_version = version_name

    unified["sourceGame"] = "h3m"
    unified["sourceVersion"] = source_version
    unified["name"] = basic.get("Map Name", "")
    unified["description"] = basic.get("Map Description", "")
    unified["creatorNotes"] = ""
    unified["difficulty"] = basic.get("Difficulty", "Normal")

    map_size = basic.get("Map Size", 0)
    unified["mapSize"] = OrderedDict([("width", map_size), ("height", map_size)])
    unified["hasUnderground"] = bool(basic.get("Has Underground", False))
    unified["mainLanguage"] = 0

    # Players
    players = map_data.get("Players Attributes", {}).get("Players", [])
    available = []
    human = []
    computer = []
    player_details = []
    for player in players:
        color = player.get("Color")
        human_playable = player.get("Human Playable", False)
        ai_playable = player.get("AI Playable", False)
        if human_playable or ai_playable:
            available.append(color)
        if human_playable:
            human.append(color)
        if ai_playable:
            computer.append(color)

        source_race = _h3m_source_race(player)
        detail = OrderedDict()
        detail["color"] = color
        detail["race"] = _h3m_unified_race(source_race)
        detail["sourceRace"] = source_race
        # Detailed per-town ownership and random town flag (h3m only),
        # carried independently for a faithful round-trip.
        owned_towns = OrderedDict()
        for town, owned in player.get("Owned Towns", {}).items():
            if owned:
                owned_towns[town] = True
        if owned_towns:
            detail["ownedTowns"] = owned_towns
        if player.get("Owns Random Town", False):
            detail["ownsRandomTown"] = True
        if player.get("Main Town", False):
            main_town = OrderedDict()
            main_town["generateHero"] = bool(player.get("Generate Hero At Main Town", True))
            main_town["x"] = player.get("Castle X", 0)
            main_town["y"] = player.get("Castle Y", 0)
            main_town["z"] = player.get("Castle Z", 0)
            detail["mainTown"] = main_town
        player_details.append(detail)

    unified["players"] = OrderedDict([
        ("availableColors", available),
        ("humanColors", human),
        ("computerColors", computer),
    ])
    unified["playerDetails"] = player_details

    # h3m-only global fields kept for a faithful round-trip.
    basic_hero = map_data.get("Basic Parameters", {}).get("Has Hero", False)
    unified["hasHero"] = bool(basic_hero)
    unified["availableHeroesBitfield"] = map_data.get("Available Heroes", {}).get("Bitfield", "")

    # Teams
    teams = []
    team_data = map_data.get("Teams", {})
    num_teams = team_data.get("Number of Teams", 0)
    if num_teams > 0:
        assignments = team_data.get("Team Assignments", {})
        for team_number in range(num_teams):
            team = [color for color, number in assignments.items() if number == team_number]
            teams.append(team)
    unified["teams"] = teams

    # Victory condition
    victory = OrderedDict()
    vic_type = map_data.get("Victory Condition", {}).get("Type", "None")
    if vic_type == "None":
        victory["type"] = "defeatEveryone"
        victory["allowNormalVictory"] = True
        victory["appliesToAI"] = True
        victory["metadata"] = []
    else:
        victory["type"] = H3M_VICTORY_CONDITIONS.get(int(vic_type, 16), "unknown")
        victory["allowNormalVictory"] = True
        victory["appliesToAI"] = True
        victory["metadata"] = []
    unified["victoryCondition"] = victory

    # Loss condition
    loss = OrderedDict()
    loss_type = map_data.get("Loss Condition", {}).get("Type", "None")
    if loss_type == "None":
        loss["type"] = "loseEverything"
    else:
        loss["type"] = H3M_LOSS_CONDITIONS.get(int(loss_type, 16), "unknown")
    loss["metadata"] = []
    unified["lossCondition"] = loss

    # Rumors
    rumors = []
    for rumor in map_data.get("Rumors", {}).get("Rumors", []):
        rumors.append(OrderedDict([
            ("name", rumor.get("Name", "")),
            ("text", rumor.get("Text", "")),
        ]))
    unified["rumors"] = rumors

    # No daily events in h3m
    unified["dailyEvents"] = []

    # Terrain
    levels = []
    for section_name, z in (("Surface Map", 0), ("Underground Map", 1)):
        section = map_data.get(section_name)
        if section is None:
            continue
        grid = []
        for cell in section.get("Grid", []):
            source_terrain = cell.get("Terrain Type", "Dirt")
            grid.append(OrderedDict([
                ("x", cell.get("X", 0)),
                ("y", cell.get("Y", 0)),
                ("z", z),
                ("terrain", _h3m_terrain_name(source_terrain)),
                ("sourceTerrain", source_terrain),
                ("sourcePicture", cell.get("Terrain Picture", 0)),
                ("sourceMirroring", cell.get("Mirroring", "0x00")),
                ("sourceRoad", cell.get("Road Type", "None")),
                ("sourceRoadProperties", cell.get("Road Properties", 0)),
                ("sourceRiver", cell.get("River Type", "None")),
                ("sourceRiverProperties", cell.get("River Properties", 0)),
            ]))
        levels.append(OrderedDict([("grid", grid)]))
    unified["terrain"] = OrderedDict([("levels", levels)])

    # Objects (decoded instances stored per tile, fh2m-style)
    unified["objects"] = _h3m_objects_to_unified(map_data)

    return unified


def _h3m_h3m_metadata_to_unified(kind, metadata):
    """
    Normalize one h3m object metadata entry into the unified schema.
    The h3m metadata fields keep their raw values (the h3m round-trip
    goes through Objects > Raw Data) and gain normalized names
    resolved through the correspondence tables: creatures, heroes,
    artifacts, spells, secondary skills and rewards.
    """
    entry = OrderedDict(metadata)

    def name_creatures(creatures):
        named = []
        for slot in creatures or []:
            creature_id = slot.get("creature")
            named.append(OrderedDict([
                ("creature", H3M_CREATURE_NAMES[creature_id]
                 if creature_id is not None and creature_id < len(H3M_CREATURE_NAMES) else None),
                ("sourceCreatureId", creature_id),
                ("count", slot.get("count")),
            ]))
        return named

    if kind == "garrisonMetadata":
        entry["ownerName"] = H3M_PLAYER_COLOR_NAMES.get(entry.get("owner"))
        entry["creaturesNamed"] = name_creatures(entry.get("creatures"))
    elif kind == "townMetadata":
        entry["ownerName"] = H3M_PLAYER_COLOR_NAMES.get(entry.get("owner"))
        if entry.get("garrison") is not None:
            entry["garrisonNamed"] = name_creatures(entry.get("garrison"))
    elif kind == "heroMetadata":
        hero_type = entry.get("type")
        entry["typeName"] = (H3M_HERO_NAMES[hero_type]
                             if hero_type is not None and hero_type < len(H3M_HERO_NAMES) else None)
        entry["ownerName"] = H3M_PLAYER_COLOR_NAMES.get(entry.get("owner"))
        if entry.get("skills") is not None:
            entry["skillsNamed"] = [
                OrderedDict([
                    ("skill", H3M_SECONDARY_SKILL_NAMES.get(sk.get("id"), str(sk.get("id")))),
                    ("sourceSkillId", sk.get("id")),
                    ("level", sk.get("level")),
                ])
                for sk in entry["skills"]
            ]
    elif kind == "shrineMetadata":
        spell = entry.get("spell")
        entry["spellName"] = (H3M_SPELL_NAMES[spell]
                              if spell is not None and spell < len(H3M_SPELL_NAMES) else None)
    elif kind == "witchhutMetadata":
        entry["skillName"] = H3M_SECONDARY_SKILL_NAMES.get(entry.get("skill"), str(entry.get("skill")))
    elif kind == "scholarMetadata":
        reward_names = {0: "primary skill", 1: "secondary skill", 2: "spell", 255: "random"}
        entry["rewardTypeName"] = reward_names.get(entry.get("rewardType"), str(entry.get("rewardType")))
    elif kind == "seerMetadata":
        quest_artifact = entry.get("questArtifact")
        if quest_artifact is not None and quest_artifact < len(H3M_ARTIFACT_NAMES):
            entry["questArtifactName"] = H3M_ARTIFACT_NAMES[quest_artifact]
        quest = entry.get("quest")
        if quest and quest.get("artifacts"):
            quest["artifactNames"] = [
                H3M_ARTIFACT_NAMES[a] if a < len(H3M_ARTIFACT_NAMES) else str(a)
                for a in quest["artifacts"]
            ]
        reward = entry.get("reward")
        if reward:
            artifact = reward.get("artifact")
            if artifact is not None and artifact < len(H3M_ARTIFACT_NAMES):
                reward["artifactName"] = H3M_ARTIFACT_NAMES[artifact]
            spell = reward.get("spell")
            if spell is not None and spell < len(H3M_SPELL_NAMES):
                reward["spellName"] = H3M_SPELL_NAMES[spell]
            creature = reward.get("creature")
            if creature is not None and creature < len(H3M_CREATURE_NAMES):
                reward["creatureName"] = H3M_CREATURE_NAMES[creature]
    elif kind == "eventMetadata":
        artifact = entry.get("artifact")
        if artifact is not None and artifact < len(H3M_ARTIFACT_NAMES):
            entry["artifactName"] = H3M_ARTIFACT_NAMES[artifact]
    return entry


def _h3m_objects_to_unified(map_data):
    """
    Convert the decoded h3m object instances into the unified objects
    section: objects stored per tile with metadata maps keyed by object
    id, as the fh2m format does.

    Objects whose group could not be mapped to a unified group keep
    their UNDEFINED_<class> group: the fh2m conversion maps the
    decorative classes and drops the others.
    """
    objects_section = map_data.get("Objects", {})
    tiles_data = objects_section.get("Tiles")
    if not tiles_data:
        return None

    tiles = OrderedDict()
    for tile_key, obj_list in tiles_data.get("tiles", {}).items():
        unified_objs = []
        for obj in obj_list:
            unified_objs.append(OrderedDict([
                ("id", obj.get("id")),
                ("group", obj.get("group")),
                ("index", obj.get("index")),
            ]))
        if unified_objs:
            tiles[tile_key] = unified_objs
        if unified_objs:
            tiles[tile_key] = unified_objs

    # Metadata maps are already keyed by object id and use unified-friendly
    # field names; pass them through.
    dropped_set = set()
    metadata = OrderedDict()
    for key, value_map in tiles_data.items():
        if key == "tiles":
            continue
        cleaned = OrderedDict()
        for obj_id, value in value_map.items():
            if int(obj_id) not in dropped_set:
                cleaned[obj_id] = _h3m_h3m_metadata_to_unified(key, value)
        if cleaned:
            metadata[key] = cleaned

    result = OrderedDict([("tiles", tiles)])
    result.update(metadata)
    # Raw object section bytes (h3m only), for a byte-perfect round-trip:
    # the binary writer re-encodes them verbatim.
    raw_data = objects_section.get("Raw Data", "")
    if raw_data:
        result["rawData"] = raw_data
    return result


def convert_fh2m_to_unified(map_data):
    """
    Convert the JSON produced by parse_fh2m into the unified format.

    Args:
        map_data: Dictionary as returned by parse_fh2m.

    Returns:
        OrderedDict: The map in the unified format.
    """
    unified = OrderedDict()

    unified["sourceGame"] = "fh2m"
    unified["sourceVersion"] = str(map_data.get("version", 0))
    unified["name"] = map_data.get("name", "")
    unified["description"] = map_data.get("description", "")
    unified["creatorNotes"] = map_data.get("creatorNotes", "")
    unified["difficulty"] = map_data.get("difficulty", "Normal")

    width = map_data.get("width", 0)
    unified["mapSize"] = OrderedDict([("width", width), ("height", map_data.get("height", width))])
    unified["hasUnderground"] = False
    unified["mainLanguage"] = map_data.get("mainLanguage", 0)
    translations = map_data.get("translations") or {}
    if translations:
        unified["translations"] = OrderedDict(
            (language, OrderedDict([
                ("name", entry.get("name", "")),
                ("description", entry.get("description", "")),
                ("creatorNotes", entry.get("creatorNotes", "")),
            ]))
            for language, entry in translations.items()
        )

    # Players
    def to_names(mask):
        return [FH2M_PLAYER_COLORS[bit] for bit in range(len(FH2M_PLAYER_COLORS)) if mask & (1 << bit)]

    unified["players"] = OrderedDict([
        ("availableColors", list(map_data.get("availablePlayerColors", []))),
        ("humanColors", list(map_data.get("humanPlayerColors", []))),
        ("computerColors", list(map_data.get("computerPlayerColors", []))),
    ])

    player_details = []
    races = map_data.get("playerRace", [])
    hero_object_colors = {}
    for tile in map_data.get("tiles", []):
        for obj in tile.get("objects", []):
            if obj.get("group") == "KINGDOM_HEROES":
                color_id = int(obj.get("index", 0)) // 7
                if 0 <= color_id < len(FH2M_PLAYER_COLORS):
                    color = FH2M_PLAYER_COLORS[color_id]
                    hero_object_colors[color] = obj.get("index", 0)
    race_ids = map_data.get("playerRaceId", [])
    for index, color in enumerate(FH2M_PLAYER_COLORS):
        # The race of every player is carried, available or not, so that
        # the round-trip preserves playerRace for all 6 colors. The raw
        # race id is kept for undocumented race codes.
        source_race = races[index] if index < len(races) else "Random"
        detail = OrderedDict()
        detail["color"] = color
        detail["available"] = color in unified["players"]["availableColors"]
        detail["race"] = FH2M_RACES.get(source_race)
        detail["sourceRace"] = source_race
        if index < len(race_ids):
            detail["sourceRaceId"] = race_ids[index]
        if color in hero_object_colors:
            # A starting hero object exists for this color: its race is part
            # of the object index (color * 7 + race).
            hero_race_id = int(hero_object_colors[color]) % 7
            hero_race = [name for name, code in UNIFIED_TO_FH2M_RACE_CODES.items() if code == hero_race_id]
            hero_race = hero_race[0] if hero_race else "Random"
            detail["startingHeroRace"] = hero_race
            detail["hasStartingHero"] = True
        player_details.append(detail)
    unified["playerDetails"] = player_details

    # Teams
    teams = []
    for mask in map_data.get("alliances", []):
        teams.append(to_names(mask))
    unified["teams"] = teams

    # Victory condition
    victory = OrderedDict()
    victory["type"] = FH2M_VICTORY_CONDITIONS.get(map_data.get("victoryConditionType", 0), "unknown")
    victory["allowNormalVictory"] = bool(map_data.get("allowNormalVictory", False))
    victory["appliesToAI"] = bool(map_data.get("isVictoryConditionApplicableForAI", False))
    victory["metadata"] = list(map_data.get("victoryConditionMetadata", []))
    unified["victoryCondition"] = victory

    # Loss condition
    loss = OrderedDict()
    loss["type"] = FH2M_LOSS_CONDITIONS.get(map_data.get("lossConditionType", 0), "unknown")
    loss["metadata"] = list(map_data.get("lossConditionMetadata", []))
    unified["lossCondition"] = loss

    # Rumors (no names in fh2m)
    rumors = []
    for text in map_data.get("rumors", []):
        rumors.append(OrderedDict([
            ("name", None),
            ("text", text),
        ]))
    unified["rumors"] = rumors

    # Daily events
    daily_events = []
    for event in map_data.get("dailyEvents", []):
        daily_events.append(OrderedDict([
            ("message", event.get("message", "")),
            ("humanColors", list(event.get("humanPlayerColors", []))),
            ("computerColors", list(event.get("computerPlayerColors", []))),
            ("firstOccurrenceDay", event.get("firstOccurrenceDay", 1)),
            ("repeatPeriodInDays", event.get("repeatPeriodInDays", 0)),
            ("resources", OrderedDict((name, value) for name, value in event.get("resources", {}).items())),
        ]))
    unified["dailyEvents"] = daily_events

    # Terrain
    grid = []
    width = map_data.get("width", 0)
    for index, tile in enumerate(map_data.get("tiles", [])):
        grid.append(OrderedDict([
            ("x", index % width),
            ("y", index // width),
            ("z", 0),
            ("terrain", _fh2m_terrain_name(tile.get("terrainIndex", 0))),
            ("sourceTerrain", "terrain:{}".format(tile.get("terrainIndex", 0))),
            ("flags", tile.get("terrainFlags", 0)),
        ]))
    unified["terrain"] = OrderedDict([
        ("levels", [OrderedDict([("grid", grid)])]),
    ])

    # Objects (stored per tile with metadata maps keyed by object id)
    unified["objects"] = _fh2m_objects_to_unified(map_data)

    return unified


def convert_to_unified(map_data, source_game):
    """
    Convert a parsed map into the unified format.

    Args:
        map_data: Dictionary as returned by parse_h3m or parse_fh2m.
        source_game: "h3m" or "fh2m".

    Returns:
        OrderedDict: The map in the unified format.
    """
    if source_game == "fh2m":
        return convert_fh2m_to_unified(map_data)
    return convert_h3m_to_unified(map_data)


H3M_VERSION_NAMES = {
    "RoE": "RoE (Restoration of Erathia)",
    "AB": "AB (Armageddon Blade)",
    "SoD": "SoD (Shadow of Death)",
}

H3M_PLAYER_COLORS = ["Red", "Blue", "Tan", "Green", "Orange", "Purple", "Teal", "Pink"]

H3M_TOWN_TYPES = ["Castle", "Rampart", "Tower", "Inferno", "Necropolis",
                  "Dungeon", "Stronghold", "Fortress", "Conflux"]

# unified terrain -> h3m terrain name
UNIFIED_TO_H3M_TERRAINS = {
    "Water": "Water",
    "Grass": "Grass",
    "Snow": "Snow",
    "Swamp": "Swamp",
    "Lava": "Lava",
    "Desert": "Sand",
    "Dirt": "Dirt",
    "Wasteland": "Rough",
    "Beach": "Sand",
    "Subterranean": "Subterranean",
    "Rock": "Rock",
}

# unified terrain -> default fh2m terrain image index (best-effort default,
# used when the unified terrain has no fh2m source index)
UNIFIED_TO_FH2M_TERRAIN_INDEX = {
    "Water": 0,
    "Grass": 30,
    "Snow": 92,
    "Swamp": 146,
    "Lava": 208,
    "Desert": 262,
    "Dirt": 321,
    "Wasteland": 361,
    "Beach": 415,
    "Subterranean": 321,
    "Rock": 321,
}


def _color_mask(color_names, known_colors):
    mask = 0
    for name in color_names:
        if name in known_colors:
            mask |= 1 << known_colors.index(name)
    return mask


def unified_to_h3m(unified):
    """
    Convert a map in the unified format back into the h3m JSON structure
    expected by write_h3m.

    Args:
        unified: Dictionary in the unified format.

    Returns:
        OrderedDict: The map in the h3decoder.py format.
    """
    from h3decoder import write_h3m  # noqa: F401  (documentation of the output)

    data = OrderedDict()

    if unified.get("sourceGame") == "h3m":
        version_name = H3M_VERSION_NAMES.get(unified.get("sourceVersion"), "SoD (Shadow of Death)")
    else:
        version_name = "SoD (Shadow of Death)"

    basic = OrderedDict()
    basic["Version"] = version_name
    basic["Has Hero"] = False
    map_size = unified.get("mapSize", {}).get("width", 72)
    basic["Map Size"] = map_size
    has_underground = bool(unified.get("hasUnderground", False))
    basic["Map Level"] = "Two-level" if has_underground else "Single-level"
    basic["Has Underground"] = has_underground
    basic["Map Name"] = unified.get("name", "")
    basic["Map Description"] = unified.get("description", "")
    basic["Difficulty"] = unified.get("difficulty", "Normal")
    basic["Has Hero"] = bool(unified.get("hasHero", False))
    data["Basic Parameters"] = basic

    players = unified.get("players", {})
    human_colors = set(players.get("humanColors", []))
    computer_colors = set(players.get("computerColors", []))
    details_by_color = {d.get("color"): d for d in unified.get("playerDetails", [])}

    players_list = []
    for color in H3M_PLAYER_COLORS:
        detail = details_by_color.get(color, {})
        source_race = detail.get("sourceRace", "Random")

        player = OrderedDict()
        player["Color"] = color
        player["Human Playable"] = color in human_colors
        player["AI Playable"] = color in computer_colors
        player["Behavior"] = "Random"

        owned_towns = OrderedDict((town, False) for town in H3M_TOWN_TYPES)
        detail_owned = detail.get("ownedTowns", {})
        if detail_owned:
            # Detailed per-town ownership carried by the unified format.
            for town in detail_owned:
                if town in owned_towns:
                    owned_towns[town] = True
            player["Has Defined Towns"] = True
        elif source_race in owned_towns:
            owned_towns[source_race] = True
            player["Has Defined Towns"] = True
        else:
            player["Has Defined Towns"] = False
        player["Owns Random Town"] = bool(detail.get("ownsRandomTown", False))
        player["Owned Towns"] = owned_towns

        main_town = detail.get("mainTown")
        if main_town:
            player["Main Town"] = True
            player["Generate Hero At Main Town"] = bool(main_town.get("generateHero", True))
            player["Castle X"] = main_town.get("x", 0)
            player["Castle Y"] = main_town.get("y", 0)
            player["Castle Z"] = main_town.get("z", 0)
        else:
            player["Main Town"] = False
            player["Castle X"] = None
            player["Castle Y"] = None
            player["Castle Z"] = None
        players_list.append(player)

    data["Players Attributes"] = OrderedDict([("Players", players_list)])
    data["Player Heroes"] = OrderedDict([("Player Heroes", [
        OrderedDict([("Color", color), ("Has Random Hero", False), ("Hero Type", None)])
        for color in H3M_PLAYER_COLORS
    ])])

    victory = unified.get("victoryCondition", {})
    victory_type = victory.get("type", "defeatEveryone")
    victory_codes = {name: code for code, name in H3M_VICTORY_CONDITIONS.items()}
    if victory_type == "defeatEveryone":
        data["Victory Condition"] = OrderedDict([("Type", "None")])
    else:
        data["Victory Condition"] = OrderedDict([
            ("Type", hex(victory_codes.get(victory_type, 0x6))),
        ])

    loss = unified.get("lossCondition", {})
    loss_type = loss.get("type", "loseEverything")
    loss_codes = {name: code for code, name in H3M_LOSS_CONDITIONS.items()}
    if loss_type == "loseEverything":
        data["Loss Condition"] = OrderedDict([("Type", "None")])
    else:
        data["Loss Condition"] = OrderedDict([
            ("Type", hex(loss_codes.get(loss_type, 0x0))),
        ])

    teams = unified.get("teams", [])
    team_data = OrderedDict([("Number of Teams", len(teams))])
    if teams:
        assignments = OrderedDict()
        for color in H3M_PLAYER_COLORS:
            assignments[color] = 0
            for team_number, team in enumerate(teams):
                if color in team:
                    assignments[color] = team_number
                    break
        team_data["Team Assignments"] = assignments
    data["Teams"] = team_data

    data["Available Heroes"] = OrderedDict([
        ("Bitfield", unified.get("availableHeroesBitfield", "")),
    ])
    data["Reserved Bytes"] = ""

    rumors = unified.get("rumors", [])
    data["Rumors"] = OrderedDict([
        ("Number of Rumors", len(rumors)),
        ("Rumors", [OrderedDict([("Name", r.get("name") or ""), ("Text", r.get("text", ""))]) for r in rumors]),
    ])

    terrain_by_level = []
    for level in unified.get("terrain", {}).get("levels", []):
        grid = OrderedDict()
        for cell in level.get("grid", []):
            if unified.get("sourceGame") == "h3m":
                terrain_name = cell.get("sourceTerrain", cell.get("terrain", "Dirt"))
                if terrain_name not in H3M_TOWN_TYPES and terrain_name not in UNIFIED_TO_H3M_TERRAINS.values():
                    terrain_name = UNIFIED_TO_H3M_TERRAINS.get(cell.get("terrain", "Dirt"), "Dirt")
            else:
                terrain_name = UNIFIED_TO_H3M_TERRAINS.get(cell.get("terrain", "Grass"), "Dirt")
            grid[(cell.get("x", 0), cell.get("y", 0))] = (cell.get("z", 0), terrain_name,
                                                           cell.get("sourcePicture", 0),
                                                           cell.get("sourceMirroring", "0x00"),
                                                           cell.get("sourceRoad", "None"),
                                                           cell.get("sourceRoadProperties", 0),
                                                           cell.get("sourceRiver", "None"),
                                                           cell.get("sourceRiverProperties", 0))
        terrain_by_level.append(grid)

    def build_section(z):
        level_grid = terrain_by_level[z] if z < len(terrain_by_level) else {}
        cells = []
        for y in range(map_size):
            for x in range(map_size):
                cell_z, terrain_name, picture, mirroring, road, road_props, river, river_props = level_grid.get(
                    (x, y), (z, "Dirt", 0, "0x00", "None", 0, "None", 0))
                cells.append(OrderedDict([
                    ("X", x), ("Y", y), ("Z", cell_z),
                    ("Terrain Type", terrain_name),
                    ("Terrain Picture", picture),
                    ("River Type", river), ("River Properties", river_props),
                    ("Road Type", road), ("Road Properties", road_props),
                    ("Mirroring", mirroring),
                ]))
        return OrderedDict([
            ("Size", map_size * map_size * 7),
            ("Raw Data Length", map_size * map_size * 7),
            ("Grid", cells),
        ])

    data["Surface Map"] = build_section(0)
    if has_underground:
        data["Underground Map"] = build_section(1)

    objects_section = _unified_objects_from_h3m(unified)
    if objects_section:
        raw_data = objects_section.get("rawData", "")
        if raw_data:
            object_count = struct.unpack("<I", bytes.fromhex(raw_data)[:4])[0]
        else:
            object_count = sum(len(objs) for objs in objects_section["tiles"].values())
        data["Objects"] = OrderedDict([
            ("Number of Objects", object_count),
            ("Raw Data", raw_data),
            ("Tiles", objects_section),
        ])
    else:
        data["Objects"] = OrderedDict([("Number of Objects", 0), ("Raw Data", "")])

    return data


def _translate_h3m_tile_objects(obj_list, objects_section, translated_metadata,
                               dropped_ids):
    """
    Translate h3m objects placed on one tile into fh2m objects.

    Objects with an fh2m equivalent are translated (group, index and
    metadata); the others are dropped and their ids appended to
    dropped_ids. The translated metadata entries are stored into
    translated_metadata under their fh2m map name (monsterMetadata,
    resourceMetadata, ...), keyed by object id.

    Returns the list of translated objects for the tile.
    """
    from correspondence import (FH2M_SPELL_SCROLL_ID, H3M_DECORATIVE_TO_FH2M,
                                  H3M_HERO_NAMES,
                                  H3M_RANDOM_MONSTER_CLASSES,
                                  H3M_TO_FH2M_ARTIFACTS,
                                  H3M_TO_FH2M_HEROES,
                                  H3M_TO_FH2M_MONSTERS,
                                  H3M_TO_FH2M_SECONDARY_SKILLS,
                                  H3M_TO_FH2M_SHRINES,
                                  H3M_TO_FH2M_SPELLS)

    translated = []
    for obj in obj_list:
        group = obj.get("group")
        obj_id = obj.get("id")
        if group == "MONSTERS":
            monster_meta = (objects_section.get("monsterMetadata") or {}).get(str(obj_id)) or {}
            creature = monster_meta.get("creature")
            if creature is None:
                # Random monster: the object class gives the random
                # level (RANDOM_MONSTER, RANDOM_MONSTER_L1 to L4).
                monster_class = monster_meta.get("monsterClass")
                fh2m_monster = H3M_RANDOM_MONSTER_CLASSES.get(monster_class, -1)
                if fh2m_monster < 1:
                    dropped_ids.append(obj_id)
                    continue
            else:
                fh2m_monster = H3M_TO_FH2M_MONSTERS.get(creature, -1)
                if fh2m_monster < 1:
                    dropped_ids.append(obj_id)
                    continue
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "MONSTERS"),
                ("index", fh2m_monster - 1),
            ]))
            fh2m_monster_entry = OrderedDict([
                ("count", monster_meta.get("count") or 0),
                ("joinCondition", 0),
                ("isWeeklyGrowthDisabled", False),
                ("selected", []),
            ])
            if monster_meta.get("message"):
                fh2m_monster_entry["message"] = monster_meta["message"]
            if monster_meta.get("resources"):
                fh2m_monster_entry["resources"] = OrderedDict(monster_meta["resources"])
            translated_metadata.setdefault("monsterMetadata", OrderedDict())[str(obj_id)] = fh2m_monster_entry
        elif group == "ADVENTURE_TREASURES":
            resource_meta = (objects_section.get("resourceMetadata") or {}).get(str(obj_id)) or {}
            resource = resource_meta.get("resource")
            if resource is None or resource < 0 or resource >= len(FH2M_RESOURCE_ORDER):
                dropped_ids.append(obj_id)
                continue
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "ADVENTURE_TREASURES"),
                ("index", resource),
            ]))
            translated_metadata.setdefault("resourceMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                ("count", resource_meta.get("count") or 0),
            ])
        elif group == "ADVENTURE_ARTIFACTS":
            artifact_meta = (objects_section.get("artifactMetadata") or {}).get(str(obj_id)) or {}
            artifact = artifact_meta.get("artifact")
            if artifact is None:
                # Random artifact: fh2m random artifacts follow the
                # regular ones in the ADVENTURE_ARTIFACTS group.
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_ARTIFACTS"),
                    ("index", 74),
                ]))
                translated_metadata.setdefault("artifactMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                    ("radius", 0),
                    ("captureCondition", 0),
                    ("selected", []),
                ])
                continue
            fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifact, -1)
            if fh2m_artifact < 1:
                dropped_ids.append(obj_id)
                continue
            # The fh2m ADVENTURE_ARTIFACTS group lists the artifacts
            # from the Arcane Necklace (fheroes2 id 9) up to Magic Book,
            # then the Price of Loyalty artifacts starting at Spell
            # Scroll (fheroes2 id 88). The map object index follows this
            # order (see map_object_info.cpp, populateAdventureArtifacts).
            if fh2m_artifact <= 81:
                fh2m_index = fh2m_artifact - 9
            else:
                fh2m_index = 73 + (fh2m_artifact - 88)
            if fh2m_index < 0:
                dropped_ids.append(obj_id)
                continue
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "ADVENTURE_ARTIFACTS"),
                ("index", fh2m_index),
            ]))
            translated_metadata.setdefault("artifactMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                ("radius", 0),
                ("captureCondition", 0),
                ("selected", []),
            ])
        elif group == "KINGDOM_TOWNS":
            town_meta = (objects_section.get("townMetadata") or {}).get(str(obj_id)) or {}
            # fh2m KINGDOM_TOWNS index: race * 2 (castle) or race * 2
            # + 1 (town), the race order being Knight, Barbarian,
            # Sorceress, Warlock, Wizard, Necromancer. The h3m town
            # type maps to the fh2m race through the faction pairings.
            town_type = town_meta.get("type")
            race_name = H3M_TOWN_TYPE_TO_FH2M_RACE.get(town_type)
            if race_name is None:
                # Random town or unknown type: Knight castle.
                race_id = 0
            else:
                race_id = FH2M_TOWN_RACE_ORDER.index(race_name)
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "KINGDOM_TOWNS"),
                ("index", race_id * 2),
            ]))
            translated_metadata.setdefault("castleMetadata", OrderedDict())[str(obj_id)] = _h3m_town_to_fh2m_castle(town_meta)
        elif group == "KINGDOM_HEROES":
            hero_meta = (objects_section.get("heroMetadata") or {}).get(str(obj_id)) or {}
            owner = hero_meta.get("owner")
            hero_type = hero_meta.get("type")
            if owner is None or owner >= len(FH2M_PLAYER_COLORS) or hero_type is None:
                # Random or unsupported hero: keep the color only when
                # possible, otherwise drop.
                if owner is not None and owner < len(FH2M_PLAYER_COLORS):
                    color_id = FH2M_PLAYER_COLORS.index(
                        FH2M_PLAYER_COLORS[owner]) if False else owner
                else:
                    dropped_ids.append(obj_id)
                    continue
                hero_type = 0
            fh2m_hero = H3M_TO_FH2M_HEROES.get(hero_type)
            if fh2m_hero is None:
                dropped_ids.append(obj_id)
                continue
            fh2m_race_id = _fh2m_hero_race_id(fh2m_hero)
            if fh2m_race_id is None:
                dropped_ids.append(obj_id)
                continue
            color_id = owner if owner < len(FH2M_PLAYER_COLORS) else 0
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "KINGDOM_HEROES"),
                ("index", color_id * 7 + fh2m_race_id),
            ]))
            hero_entry = _h3m_hero_to_fh2m_hero(hero_meta, hero_type, fh2m_race_id)
            translated_metadata.setdefault("heroMetadata", OrderedDict())[str(obj_id)] = hero_entry
        elif group in ("ADVENTURE_MINES", "ADVENTURE_DWELLINGS"):
            ownable_meta = (objects_section.get("ownableMetadata") or {}).get(str(obj_id)) or {}
            owner = ownable_meta.get("owner")
            owner_names = []
            if owner is not None and 0 <= owner < 8:
                h3m_colors = ["Red", "Blue", "Tan", "Green", "Orange", "Purple", "Teal", "Pink"]
                if owner < 6 and h3m_colors[owner] in FH2M_PLAYER_COLORS:
                    owner_names = [h3m_colors[owner]]
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", group),
                ("index", 0),
            ]))
            translated_metadata.setdefault("capturableObjectsMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                ("ownerColor", owner_names),
            ])
        elif group == "ADVENTURE_POWER_UPS":
            shrine_meta = (objects_section.get("shrineMetadata") or {}).get(str(obj_id)) or {}
            shrine_class = shrine_meta.get("shrineClass")
            fh2m_index = H3M_TO_FH2M_SHRINES.get(shrine_class, -1)
            if fh2m_index < 0:
                # Not a shrine: drop (other power-up objects have no
                # fh2m equivalent).
                dropped_ids.append(obj_id)
                continue
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "ADVENTURE_POWER_UPS"),
                ("index", fh2m_index),
            ]))
            spell = shrine_meta.get("spell")
            fh2m_spell = H3M_TO_FH2M_SPELLS.get(spell, -1) if spell is not None else -1
            translated_metadata.setdefault("shrineMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                ("spell", fh2m_spell if fh2m_spell and fh2m_spell > 0 else None),
            ])
        elif group == "ADVENTURE_MISCELLANEOUS":
            # Witch huts (class 113) and scholars (class 62) convert
            # to the fh2m Witch's Hut object (index 26). The fh2m
            # format carries no per-hut metadata: the engine draws
            # the secondary skill at game start.
            witch_meta = (objects_section.get("witchhutMetadata") or {}).get(str(obj_id))
            scholar_meta = (objects_section.get("scholarMetadata") or {}).get(str(obj_id))
            garrison_meta = (objects_section.get("garrisonMetadata") or {}).get(str(obj_id))
            seer_meta = (objects_section.get("seerMetadata") or {}).get(str(obj_id))
            pandora_meta = (objects_section.get("pandoraMetadata") or {}).get(str(obj_id))
            if witch_meta is not None or scholar_meta is not None:
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_MISCELLANEOUS"),
                    ("index", 26),
                ]))
            elif seer_meta is not None:
                # A seer hut converts to the fh2m Sphinx object
                # (index 31): the artifact quest becomes the riddle
                # (the artifact name being the answer) and the
                # reward converts when the fh2m sphinx supports it
                # (artifact or resources); the other h3m reward
                # types (experience, skills, spells, creatures)
                # are lost.
                sphinx_entry = _h3m_seer_to_fh2m_sphinx(seer_meta)
                if sphinx_entry is not None:
                    translated.append(OrderedDict([
                        ("id", obj_id),
                        ("group", "ADVENTURE_MISCELLANEOUS"),
                        ("index", 31),
                    ]))
                    translated_metadata.setdefault("sphinxMetadata", OrderedDict())[str(obj_id)] = sphinx_entry
                else:
                    dropped_ids.append(obj_id)
                    continue
            elif pandora_meta is not None:
                # A pandora box converts to the fh2m Sphinx object
                # (index 31): the guard message becomes the riddle
                # and the artifact or resource bonuses convert; the
                # other h3m bonuses (experience, mana, morale, luck,
                # skills, spells, creatures) and the guard fight are
                # lost.
                sphinx_entry = _h3m_pandora_to_fh2m_sphinx(pandora_meta)
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_MISCELLANEOUS"),
                    ("index", 31),
                ]))
                translated_metadata.setdefault("sphinxMetadata", OrderedDict())[str(obj_id)] = sphinx_entry
            elif garrison_meta is not None:
                # A garrison converts to a monster troop: the highest
                # level creature of the garrison (the highest h3m
                # creature id among the non-empty slots) becomes a
                # placed monster with its count. An empty garrison is
                # dropped.
                best_creature = None
                best_count = 0
                for creature_slot in (garrison_meta.get("creatures") or []):
                    creature = creature_slot.get("creature")
                    count = creature_slot.get("count") or 0
                    if creature is None or count <= 0:
                        continue
                    if best_creature is None or creature > best_creature:
                        best_creature = creature
                        best_count = count
                if best_creature is None:
                    dropped_ids.append(obj_id)
                    continue
                fh2m_monster = H3M_TO_FH2M_MONSTERS.get(best_creature, 0) or 0
                if fh2m_monster < 1:
                    dropped_ids.append(obj_id)
                    continue
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "MONSTERS"),
                    ("index", fh2m_monster - 1),
                ]))
                translated_metadata.setdefault("monsterMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                    ("count", best_count),
                    ("joinCondition", 0),
                    ("isWeeklyGrowthDisabled", False),
                    ("selected", []),
                ])
            elif (objects_section.get("eventMetadata") or {}).get(str(obj_id)):
                event_meta = objects_section["eventMetadata"][str(obj_id)]
                # Ground event: the fh2m OBJ_EVENT object
                # (ADVENTURE_MISCELLANEOUS index 38) with a full
                # adventureMapEventMetadata.
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_MISCELLANEOUS"),
                    ("index", 38),
                ]))
                translated_metadata.setdefault("adventureMapEventMetadata", OrderedDict())[str(obj_id)] = _h3m_event_to_fh2m_event(event_meta)
            else:
                sign_meta = (objects_section.get("signMetadata") or {}).get(str(obj_id))
                if sign_meta:
                    translated.append(OrderedDict([
                        ("id", obj_id),
                        ("group", "ADVENTURE_MISCELLANEOUS"),
                        ("index", 0),
                    ]))
                    translated_metadata.setdefault("signMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                        ("message", sign_meta.get("message", "")),
                    ])
                else:
                    dropped_ids.append(obj_id)
        elif group.startswith("UNDEFINED_"):
            # Decorative objects: the h3m class (from the group name)
            # converts to a representative Heroes II landscape object
            # through the decorative table; the classes without a
            # mapping stay dropped.
            try:
                obj_class = int(group[len("UNDEFINED_"):])
            except ValueError:
                dropped_ids.append(obj_id)
                continue
            decorative = H3M_DECORATIVE_TO_FH2M.get(obj_class)
            if decorative is None:
                dropped_ids.append(obj_id)
                continue
            fh2m_group, fh2m_index = decorative
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", fh2m_group),
                ("index", fh2m_index),
            ]))
        else:
            dropped_ids.append(obj_id)
    return translated


def _fh2m_hero_race_id(fh2m_hero_id):
    """
    Race id (0-6, the fh2m playerRace encoding) of a regular Heroes II
    hero: Knight 1-9, Barbarian 10-18, Sorceress 19-27, Warlock 28-36,
    Wizard 37-45, Necromancer 46-54. Returns None for campaign and
    debug heroes.
    """
    if 1 <= fh2m_hero_id <= 9:
        return 1
    if 10 <= fh2m_hero_id <= 18:
        return 2
    if 19 <= fh2m_hero_id <= 27:
        return 3
    if 28 <= fh2m_hero_id <= 36:
        return 4
    if 37 <= fh2m_hero_id <= 45:
        return 5
    if 46 <= fh2m_hero_id <= 54:
        return 6
    return None


def _h3m_pandora_to_fh2m_sphinx(pandora_meta):
    """
    Build an fh2m sphinxMetadata entry from an h3m pandora box:
    the riddle is the fixed 'Validez pour obtenir la recompense.'
    prompt with an empty valid answer, and the artifact and
    resource bonuses convert; the
    other h3m bonuses (experience, mana, morale, luck, primary and
    secondary skills, spells, creatures) and the guard fight have
    no sphinx equivalent and are lost.
    """
    from correspondence import H3M_TO_FH2M_ARTIFACTS

    riddle = "Validez pour obtenir la recompense."

    fh2m_artifact = 0
    artifacts = pandora_meta.get("artifacts") or []
    if artifacts:
        fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifacts[0], 0) or 0

    resources_meta = pandora_meta.get("resources") or OrderedDict()
    resource_names = ["wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"]
    resources = OrderedDict([
        (name, resources_meta.get(name, 0) or 0) for name in resource_names
    ])

    return OrderedDict([
        ("riddle", riddle),
        ("answers", []),
        ("artifact", fh2m_artifact),
        ("artifactMetadata", 0),
        ("resources", resources),
    ])


def _h3m_seer_to_fh2m_sphinx(seer_meta):
    """
    Build an fh2m sphinxMetadata entry from an h3m seer hut (RoE
    artifact quest or AB+ quest): the riddle is the fixed
    'Validez pour obtenir la recompense.' prompt with an empty
    valid answer, and the reward converts when the fh2m sphinx
    supports it (an artifact or resources); the other h3m reward
    types (experience, morale, luck, primary and secondary skills,
    spells, creatures) have no sphinx equivalent and are lost.
    Returns None when the seer carries no quest.
    """
    from correspondence import H3M_TO_FH2M_ARTIFACTS

    quest = seer_meta.get("quest")
    quest_artifact = seer_meta.get("questArtifact")
    if quest is None and quest_artifact is None:
        return None

    riddle = "Validez pour obtenir la recompense."
    answers = []

    reward = seer_meta.get("reward") or {}
    fh2m_artifact = 0
    artifact_metadata = 0
    resources = OrderedDict([
        ("wood", 0), ("mercury", 0), ("ore", 0), ("sulfur", 0),
        ("crystal", 0), ("gems", 0), ("gold", 0),
    ])
    reward_type = reward.get("type")
    if reward_type == 8:
        artifact = reward.get("artifact")
        fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifact, 0) or 0
    elif reward_type == 5:
        resource_names = ["wood", "mercury", "ore", "sulfur",
                         "crystal", "gems", "gold"]
        resource_index = reward.get("resourceType", 0)
        if 0 <= resource_index < len(resource_names):
            resources[resource_names[resource_index]] = reward.get("amount", 0)

    return OrderedDict([
        ("riddle", riddle),
        ("answers", answers),
        ("artifact", fh2m_artifact),
        ("artifactMetadata", artifact_metadata),
        ("resources", resources),
    ])


def _h3m_event_to_fh2m_event(event_meta):
    """
    Build an fh2m adventureMapEventMetadata entry from an h3m ground
    event: message, player colors, resources, primary skills,
    experience, the first secondary skill, the first artifact (the
    Spell Scroll spell through the artifact metadata) and the first
    creature. The h3m event removes itself after visit when
    removeAfterVisit is set: the fh2m event is recurring otherwise.
    """
    from correspondence import (FH2M_SPELL_SCROLL_ID,
                                  H3M_TO_FH2M_ARTIFACTS,
                                  H3M_TO_FH2M_MONSTERS,
                                  H3M_TO_FH2M_SECONDARY_SKILLS,
                                  H3M_TO_FH2M_SPELLS)

    h3m_color_names = ["Red", "Blue", "Tan", "Green", "Orange", "Purple",
                       "Teal", "Pink"]
    fh2m_colors = ["Blue", "Green", "Red", "Yellow", "Orange", "Purple"]
    players_mask = event_meta.get("players") or 0
    human_colors = []
    computer_colors = []
    for bit in range(8):
        if players_mask & (1 << bit):
            color = h3m_color_names[bit]
            if color in fh2m_colors:
                if event_meta.get("applyToComputer"):
                    computer_colors.append(color)
                else:
                    human_colors.append(color)
    # No color enabled at all means every player.
    if not human_colors and not computer_colors:
        human_colors = list(fh2m_colors)

    artifact = event_meta.get("artifacts") or [None]
    artifact = artifact[0] if artifact else None
    fh2m_artifact = 0
    artifact_metadata = 0
    if artifact is not None:
        fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifact, 0) or 0
        if fh2m_artifact == FH2M_SPELL_SCROLL_ID:
            spells = event_meta.get("spells") or []
            if spells:
                fh2m_spell = H3M_TO_FH2M_SPELLS.get(spells[0], 0) or 0
                artifact_metadata = fh2m_spell

    skills = event_meta.get("secondarySkills") or []
    fh2m_skill = 0
    fh2m_skill_level = 0
    if skills:
        fh2m_skill = H3M_TO_FH2M_SECONDARY_SKILLS.get(skills[0].get("id"), 0)
        fh2m_skill_level = skills[0].get("level", 0)

    creatures = event_meta.get("creatures") or []
    fh2m_creature = 0
    creature_count = 0
    if creatures and creatures[0].get("creature") is not None:
        fh2m_creature = H3M_TO_FH2M_MONSTERS.get(creatures[0]["creature"], 0) or 0
        creature_count = creatures[0].get("count", 0)

    resources = event_meta.get("resources") or {}
    primaries = event_meta.get("primarySkills") or {}

    return OrderedDict([
        ("message", event_meta.get("message", "")),
        ("humanPlayerColors", human_colors),
        ("computerPlayerColors", computer_colors),
        ("isRecurringEvent", not bool(event_meta.get("removeAfterVisit"))),
        ("artifact", fh2m_artifact),
        ("artifactMetadata", artifact_metadata),
        ("resources", OrderedDict([
            ("wood", resources.get("wood", 0)),
            ("mercury", resources.get("mercury", 0)),
            ("ore", resources.get("ore", 0)),
            ("sulfur", resources.get("sulfur", 0)),
            ("crystal", resources.get("crystal", 0)),
            ("gems", resources.get("gems", 0)),
            ("gold", resources.get("gold", 0)),
        ])),
        ("attack", primaries.get("attack", 0)),
        ("defense", primaries.get("defense", 0)),
        ("knowledge", primaries.get("knowledge", 0)),
        ("spellPower", primaries.get("spellPower", 0)),
        ("experience", event_meta.get("experience") or 0),
        ("secondarySkill", fh2m_skill),
        ("secondarySkillLevel", fh2m_skill_level),
        ("monsterType", fh2m_creature),
        ("monsterCount", creature_count),
    ])


def _h3m_hero_to_fh2m_hero(hero_meta, hero_type, fh2m_race_id):
    """
    Build a complete fh2m heroMetadata entry from an h3m hero
    object: name, experience, primary skills, secondary skills, army,
    artifacts and patrol state are converted; the h3m fields with no
    Heroes II equivalent (biography, face, gender, spells bitfield)
    are dropped.
    """
    from correspondence import (H3M_HERO_NAMES, H3M_TO_FH2M_ARTIFACTS,
                                  H3M_TO_FH2M_MONSTERS,
                                  H3M_TO_FH2M_SECONDARY_SKILLS,
                                  H3M_TO_FH2M_SPELLS)

    # Secondary skills: up to 8. The skills with a Heroes II
    # equivalent convert through the table; the others become the
    # random skill (id 0, the game draws one on hire), keeping their
    # level.
    skills = [0] * 8
    skill_levels = [0] * 8
    slot = 0
    for sk in (hero_meta.get("skills") or []):
        if slot >= 8:
            break
        fh2m_skill = H3M_TO_FH2M_SECONDARY_SKILLS.get(sk.get("id"), 0)
        skills[slot] = fh2m_skill
        skill_levels[slot] = sk.get("level", 0)
        slot += 1

    # Army: up to 5 slots from the 7 h3m creature slots.
    army_types = [0, 0, 0, 0, 0]
    army_counts = [0, 0, 0, 0, 0]
    slot = 0
    for creature_slot in (hero_meta.get("creatures") or []):
        creature = creature_slot.get("creature")
        count = creature_slot.get("count") or 0
        if creature is None or count <= 0 or slot >= 5:
            continue
        fh2m_monster = H3M_TO_FH2M_MONSTERS.get(creature, -1)
        if fh2m_monster < 1:
            continue
        army_types[slot] = fh2m_monster
        army_counts[slot] = count
        slot += 1

    # Artifacts: the 18/19 h3m slots map to the 14 fh2m slots. The
    # first 16 h3m slots (worn + war machines) map one-to-one to the
    # fh2m worn slots; the backpack items follow.
    artifacts = [0] * 14
    artifact_meta = [0] * 14
    h3m_artifacts = hero_meta.get("artifacts") or []
    worn_count = min(len(h3m_artifacts), 16, 14)
    for slot in range(worn_count):
        artifact = h3m_artifacts[slot]
        if artifact in (0xFF, 0xFFFF):
            continue
        fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifact, -1)
        if fh2m_artifact and fh2m_artifact > 0:
            artifacts[slot] = fh2m_artifact
    bag = hero_meta.get("artifactBag") or []
    bag_slot = worn_count
    for artifact in bag:
        if bag_slot >= 14:
            break
        fh2m_artifact = H3M_TO_FH2M_ARTIFACTS.get(artifact, -1)
        if fh2m_artifact and fh2m_artifact > 0:
            artifacts[bag_slot] = fh2m_artifact
            bag_slot += 1

    # Spells: the h3m spells bitfield converts to the fh2m spell ids.
    available_spells = []
    spells_hex = hero_meta.get("spells")
    if isinstance(spells_hex, str) and spells_hex:
        spell_bytes = bytes.fromhex(spells_hex)
        for byte_index, spell_byte in enumerate(spell_bytes):
            for bit in range(8):
                if spell_byte & (1 << bit):
                    h3m_spell = byte_index * 8 + bit
                    fh2m_spell = H3M_TO_FH2M_SPELLS.get(h3m_spell)
                    if fh2m_spell and fh2m_spell > 0:
                        available_spells.append(fh2m_spell)
    elif isinstance(spells_hex, int) and 0 <= spells_hex < 70:
        fh2m_spell = H3M_TO_FH2M_SPELLS.get(spells_hex)
        if fh2m_spell and fh2m_spell > 0:
            available_spells.append(fh2m_spell)

    patrol_radius = hero_meta.get("patrolRadius")
    experience = hero_meta.get("experience")
    primaries = hero_meta.get("primarySkills") or {}

    return OrderedDict([
        ("customName", hero_meta.get("name") or (H3M_HERO_NAMES[hero_type]
                                                 if hero_type is not None and hero_type < len(H3M_HERO_NAMES) else "")),
        ("customPortrait", 0),
        ("armyMonsterType", army_types),
        ("armyMonsterCount", army_counts),
        ("artifacts", artifacts),
        ("artifactMetadata", artifact_meta),
        ("availableSpells", available_spells),
        ("isOnPatrol", patrol_radius is not None and patrol_radius != 0xFF),
        ("patrolRadius", patrol_radius if patrol_radius is not None and patrol_radius != 0xFF else 0),
        ("secondarySkill", skills),
        ("secondarySkillLevel", skill_levels),
        ("customLevel", -1),
        ("customExperience", experience if experience is not None else -1),
        ("customAttack", primaries.get("attack", -1) if primaries else -1),
        ("customDefense", primaries.get("defense", -1) if primaries else -1),
        ("customKnowledge", primaries.get("knowledge", -1) if primaries else -1),
        ("customSpellPower", primaries.get("spellPower", -1) if primaries else -1),
        ("magicPoints", -1),
        ("raceId", 0x01 << (fh2m_race_id - 1) if 1 <= fh2m_race_id <= 6 else 0),
    ])


def _h3m_town_to_fh2m_castle(town_meta):
    """
    Build an fh2m castleMetadata entry from an h3m townMetadata. The
    garrison creatures become the castle defenders (the first five
    non-empty slots); the built and disabled h3m building bitfields
    convert to the fh2m building flags for the buildings with a
    Heroes II equivalent.
    """
    from correspondence import H3M_DWELLING_BITS, H3M_TOWN_BUILDING_BITS

    defender_types = [0, 0, 0, 0, 0]
    defender_counts = [0, 0, 0, 0, 0]
    garrison = town_meta.get("garrison") or []
    slot = 0
    for creature_slot in garrison:
        creature = creature_slot.get("creature")
        count = creature_slot.get("count") or 0
        if creature is None or count <= 0 or slot >= 5:
            continue
        fh2m_monster = H3M_TO_FH2M_MONSTERS.get(creature, -1)
        if fh2m_monster < 1:
            continue
        defender_types[slot] = fh2m_monster
        defender_counts[slot] = count
        slot += 1

    def bitfield_to_flags(hex_value):
        flags = []
        if not hex_value:
            return flags
        raw = bytes.fromhex(hex_value)
        for byte_index in range(min(len(raw), 6)):
            for bit in range(8):
                if raw[byte_index] & (1 << bit):
                    flag = H3M_TOWN_BUILDING_BITS.get((byte_index, bit))
                    if flag is None:
                        flag = H3M_DWELLING_BITS.get((byte_index, bit))
                    if flag:
                        flags.append(flag)
        return flags

    built_flags = bitfield_to_flags(town_meta.get("builtBuildings"))
    banned_flags = bitfield_to_flags(town_meta.get("disabledBuildings"))

    return OrderedDict([
        ("customName", town_meta.get("customName") or ""),
        ("defenderMonsterType", defender_types),
        ("defenderMonsterCount", defender_counts),
        ("customBuildings", bool(built_flags or banned_flags)),
        ("builtBuildings", built_flags),
        ("bannedBuildings", banned_flags),
        ("mustHaveSpells", OrderedDict()),
        ("bannedSpells", []),
        ("availableToHireMonsterCount", [-1, 0, 0, 0, 0, 0]),
    ])


def unified_to_fh2m(unified):
    """
    Convert a map in the unified format back into the fh2m JSON structure
    expected by write_fh2m.

    Args:
        unified: Dictionary in the unified format.

    Returns:
        OrderedDict: The map in the h2decoder.py format.
    """
    if unified.get("hasUnderground", False):
        raise ValueError(
            "Heroes of Might and Magic 2 ne permet pas de jouer avec le sous-sol, "
            "la carte {} ne peut pas être convertie".format(unified.get("name", "")))

    # Heroes II supports at most 6 players: a map with more than 6
    # available colors cannot be converted.
    available_colors = (unified.get("players") or {}).get("availableColors") or []
    if len(available_colors) > 6:
        raise ValueError(
            "Le nombre de factions est limité à 6 dans H2, "
            "impossible de convertir la carte {}".format(unified.get("name", "")))

    data = OrderedDict()

    if unified.get("sourceGame") == "fh2m":
        version = int(unified.get("sourceVersion", 13))
    else:
        version = 13
    data["version"] = version
    data["isCampaign"] = False
    data["difficulty"] = unified.get("difficulty", "Normal")

    players = unified.get("players", {})
    data["availablePlayerColors"] = list(players.get("availableColors", []))
    data["humanPlayerColors"] = list(players.get("humanColors", []))
    data["computerPlayerColors"] = list(players.get("computerColors", []))

    data["alliances"] = [_color_mask(team, FH2M_PLAYER_COLORS) for team in unified.get("teams", [])]

    details_by_color = {d.get("color"): d for d in unified.get("playerDetails", [])}
    race_reverse = UNIFIED_TO_FH2M_RACE_CODES
    race_ids = []
    race_names = []
    for color in FH2M_PLAYER_COLORS:
        detail = details_by_color.get(color, {})
        source_race = detail.get("sourceRace")
        if source_race is None:
            # Fall back to the normalized race when no source race exists.
            source_race = detail.get("race") or "Random"
        source_race_id = detail.get("sourceRaceId")
        if source_race_id is None:
            source_race_id = race_reverse.get(source_race, 0)
        race_ids.append(source_race_id)
        race_names.append(source_race)
    data["playerRaceId"] = race_ids
    data["playerRace"] = race_names

    victory = unified.get("victoryCondition", {})
    victory_codes = {name: code for code, name in FH2M_VICTORY_CONDITIONS.items()}
    # The unified victory types with no Heroes II equivalent
    # (accumulateCreatures, buildGrail, defeatMonster, flagDwellings,
    # flagMines, transportArtifact, upgradeTown) fall back to
    # VICTORY_DEFEAT_EVERYONE (code 0).
    data["victoryConditionType"] = victory_codes.get(victory.get("type", "defeatEveryone"), 0)
    data["isVictoryConditionApplicableForAI"] = bool(victory.get("appliesToAI", False))
    data["allowNormalVictory"] = bool(victory.get("allowNormalVictory", False))
    data["victoryConditionMetadata"] = list(victory.get("metadata", []))

    loss = unified.get("lossCondition", {})
    loss_codes = {name: code for code, name in FH2M_LOSS_CONDITIONS.items()}
    data["lossConditionType"] = loss_codes.get(loss.get("type", "loseEverything"), 0)
    data["lossConditionMetadata"] = list(loss.get("metadata", []))

    width = unified.get("mapSize", {}).get("width", 0)
    data["width"] = width
    data["height"] = unified.get("mapSize", {}).get("height", width)
    data["mainLanguage"] = unified.get("mainLanguage", 0)
    data["name"] = unified.get("name", "")
    data["description"] = unified.get("description", "")
    data["creatorNotes"] = unified.get("creatorNotes", "")
    if version >= 11:
        data["translations"] = OrderedDict(
            (language, OrderedDict([
                ("name", entry.get("name", "")),
                ("description", entry.get("description", "")),
                ("creatorNotes", entry.get("creatorNotes", "")),
            ]))
            for language, entry in (unified.get("translations") or {}).items()
        )

    data["additionalInfo"] = []

    terrain_by_position = {}
    for level in unified.get("terrain", {}).get("levels", []):
        for cell in level.get("grid", []):
            if cell.get("z", 0) == 0:
                source_terrain = cell.get("sourceTerrain", "")
                if source_terrain.startswith("terrain:"):
                    terrain_index = int(source_terrain[len("terrain:"):])
                else:
                    terrain_index = UNIFIED_TO_FH2M_TERRAIN_INDEX.get(cell.get("terrain", "Grass"), 30)
                terrain_by_position[(cell.get("x", 0), cell.get("y", 0))] = (terrain_index, cell.get("flags", 0))

    # Objects placed on tiles, from the unified objects section.
    objects_by_tile = {}
    objects_section = unified.get("objects") or {}
    is_h3m_source = unified.get("sourceGame") == "h3m"
    translated_metadata = {}
    dropped_ids = []
    for tile_key, obj_list in objects_section.get("tiles", {}).items():
        parts = tile_key.split("_")
        if len(parts) != 3:
            continue
        x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
        if z != 0:
            continue
        if not is_h3m_source:
            objects_by_tile[(x, y)] = [OrderedDict(obj) for obj in obj_list]
            continue
        translated = _translate_h3m_tile_objects(obj_list, objects_section,
                                                  translated_metadata,
                                                  dropped_ids)
        if translated:
            objects_by_tile[(x, y)] = translated
    if dropped_ids:
        objects_section = OrderedDict(objects_section)
        objects_section["dropped"] = dropped_ids

    default_terrain = (UNIFIED_TO_FH2M_TERRAIN_INDEX.get("Grass", 30), 0)

    # Roads and rivers (h3m source only): the h3m format stores the
    # road/river type per tile; the directions are derived from the
    # neighboring tiles and encoded as the fheroes2 bitfield
    # (TOP_LEFT=1, TOP=2, TOP_RIGHT=4, RIGHT=8, BOTTOM_RIGHT=16,
    # BOTTOM=32, BOTTOM_LEFT=64, LEFT=128).
    road_tiles = {}
    river_tiles = {}
    if is_h3m_source:
        _h3m_direction_bits = [(-1, -1, 1), (0, -1, 2), (1, -1, 4),
                                (1, 0, 8), (1, 1, 16), (0, 1, 32),
                                (-1, 1, 64), (-1, 0, 128)]
        for level in unified.get("terrain", {}).get("levels", []):
            for cell in level.get("grid", []):
                if cell.get("z", 0) != 0:
                    continue
                pos = (cell.get("x", 0), cell.get("y", 0))
                if cell.get("sourceRoad") and cell.get("sourceRoad") != "None":
                    road_tiles[pos] = cell.get("sourceRoad")
                if cell.get("sourceRiver") and cell.get("sourceRiver") != "None":
                    river_tiles[pos] = cell.get("sourceRiver")

        def _direction_bitfield(present_set, x, y):
            bits = 0
            for dx, dy, bit in _h3m_direction_bits:
                if (x + dx, y + dy) in present_set:
                    bits |= bit
            return bits

        next_road_id = 100000
        for (x, y) in road_tiles:
            bits = _direction_bitfield(road_tiles, x, y)
            obj = OrderedDict([
                ("id", next_road_id),
                ("group", "ROADS"),
                ("index", bits),
            ])
            next_road_id += 1
            objects_by_tile.setdefault((x, y), []).insert(0, obj)
        next_river_id = 200000
        for (x, y) in river_tiles:
            bits = _direction_bitfield(river_tiles, x, y)
            obj = OrderedDict([
                ("id", next_river_id),
                ("group", "STREAMS"),
                ("index", bits),
            ])
            next_river_id += 1
            objects_by_tile.setdefault((x, y), []).insert(0, obj)

    tiles = []
    for y in range(data["height"]):
        for x in range(width):
            terrain_index, terrain_flags = terrain_by_position.get((x, y), default_terrain)
            tiles.append(OrderedDict([
                ("terrainIndex", terrain_index),
                ("terrainFlags", terrain_flags),
                ("objects", objects_by_tile.get((x, y), [])),
            ]))

    # Starting heroes: an fh2m hero is an object of the KINGDOM_HEROES group
    # placed on a tile. The object index is color * 7 + race (see the
    # populateKingdomHeroes function of the fheroes2 engine: 6 colors x 7
    # races, race 6 being a random race). When the unified map already
    # carries a KINGDOM_HEROES object for the color (converted from an
    # fh2m map), it is kept as is; only missing ones are generated.
    existing_hero_colors = set()
    existing_ids = set()
    for tile in tiles:
        for obj in tile["objects"]:
            existing_ids.add(obj.get("id", 0))
            if obj.get("group") == "KINGDOM_HEROES":
                hero_color_id = int(obj.get("index", 0)) // 7
                if 0 <= hero_color_id < len(FH2M_PLAYER_COLORS):
                    existing_hero_colors.add(FH2M_PLAYER_COLORS[hero_color_id])

    next_object_id = (max(existing_ids) + 1) if existing_ids else 1
    for detail in unified.get("playerDetails", []):
        color = detail.get("color")
        if color not in FH2M_PLAYER_COLORS:
            continue
        if color not in data["availablePlayerColors"]:
            continue
        if color in existing_hero_colors:
            continue
        race = detail.get("race") or "Random"
        race_id = UNIFIED_TO_FH2M_RACE_CODES.get(race, 0)
        color_id = FH2M_PLAYER_COLORS.index(color)
        hero_object_index = color_id * 7 + race_id

        # Place the hero near the main town when it exists, otherwise at the
        # first tile of the map edge.
        main_town = detail.get("mainTown")
        if main_town:
            x = min(max(int(main_town.get("x", 0)), 0), width - 1)
            y = min(max(int(main_town.get("y", 0)) - 1, 0), data["height"] - 1)
        else:
            x = 0
            y = data["height"] - 1

        tiles[y * width + x]["objects"].append(OrderedDict([
            ("id", next_object_id),
            ("group", "KINGDOM_HEROES"),
            ("index", hero_object_index),
        ]))
        next_object_id += 1

    data["tiles"] = tiles

    daily_events = []
    for event in unified.get("dailyEvents", []):
        daily_events.append(OrderedDict([
            ("message", event.get("message", "")),
            ("humanPlayerColors", list(event.get("humanColors", []))),
            ("computerPlayerColors", list(event.get("computerColors", []))),
            ("firstOccurrenceDay", event.get("firstOccurrenceDay", 1)),
            ("repeatPeriodInDays", event.get("repeatPeriodInDays", 0)),
            ("resources", OrderedDict((name, value) for name, value in event.get("resources", {}).items())),
        ]))
    data["dailyEvents"] = daily_events

    data["rumors"] = [r.get("text", "") for r in unified.get("rumors", [])]

    data["castleMetadata"] = OrderedDict()
    data["heroMetadata"] = OrderedDict()
    data["sphinxMetadata"] = OrderedDict()
    data["signMetadata"] = OrderedDict()
    data["adventureMapEventMetadata"] = OrderedDict()
    data["selectionObjectMetadata"] = OrderedDict()

    if version > 8:
        data["capturableObjectsMetadata"] = OrderedDict()
    if version < 10:
        data["standardObjectMetadata"] = OrderedDict()
    if version > 9:
        data["monsterMetadata"] = OrderedDict()
        data["artifactMetadata"] = OrderedDict()
        data["resourceMetadata"] = OrderedDict()
    if version >= 11:
        value_map = objects_section.get("translationInfo")
        if value_map:
            data["translationInfo"] = OrderedDict(value_map)
        else:
            data["translationInfo"] = OrderedDict()

    # Metadata maps keyed by object id, from the unified objects section,
    # overriding the empty defaults above.
    for key in ("castleMetadata", "heroMetadata", "sphinxMetadata",
                "signMetadata", "adventureMapEventMetadata",
                "selectionObjectMetadata", "capturableObjectsMetadata",
                "monsterMetadata", "artifactMetadata", "resourceMetadata"):
        translated_map = translated_metadata.get(key)
        if translated_map:
            # Objects translated from an h3m source: use the metadata
            # built by the translation.
            data[key] = OrderedDict(translated_map)
            continue
        if is_h3m_source:
            # Raw h3m metadata has a different structure; do not feed
            # it to the fh2m writer.
            continue
        value_map = objects_section.get(key)
        if value_map:
            data[key] = OrderedDict(
                (obj_id, _unified_metadata_to_fh2m(key, entry))
                for obj_id, entry in value_map.items()
            )
    if version < 10:
        value_map = objects_section.get("standardObjectMetadata")
        if value_map:
            data["standardObjectMetadata"] = OrderedDict(value_map)

    return data


def convert_from_unified(unified, source_game):
    """
    Convert a map in the unified format into the JSON structure of the
    given game, ready to be written by write_h3m or write_fh2m.

    Args:
        unified: Dictionary in the unified format.
        source_game: "h3m" or "fh2m".

    Returns:
        OrderedDict: The map in the game-specific format.
    """
    if source_game == "fh2m":
        return unified_to_fh2m(unified)
    return unified_to_h3m(unified)


def _fh2m_metadata_to_unified(kind, metadata, obj=None):
    """
    Normalize one fh2m object metadata entry into the unified schema.

    The normalized fields carry readable names (monsters, artifacts,
    spells, secondary skills, join conditions) resolved through the
    correspondence tables. The raw fh2m identifiers and every
    source-only field are kept in the returned entry so that
    _unified_metadata_to_fh2m can rebuild the exact original
    structure and the binary round-trip stays byte-perfect.
    """
    entry = OrderedDict(metadata)

    if kind == "castleMetadata":
        entry["defenders"] = [
            OrderedDict([
                ("monster", fh2m_monster_name(monster_type)),
                ("sourceMonsterId", monster_type),
                ("count", count),
            ])
            for monster_type, count in zip(metadata.get("defenderMonsterType", []),
                                           metadata.get("defenderMonsterCount", []))
        ]
        built = [fh2m_building_name(building) for building in metadata.get("builtBuildings", [])]
        banned = [fh2m_building_name(building) for building in metadata.get("bannedBuildings", [])]
        entry["builtBuildingNames"] = built
        entry["bannedBuildingNames"] = banned
        entry["mustHaveSpellNames"] = OrderedDict(
            (position, fh2m_spell_name(spell))
            for position, spell in metadata.get("mustHaveSpells", {}).items()
        )
        entry["bannedSpellNames"] = [fh2m_spell_name(spell) for spell in metadata.get("bannedSpells", [])]
        town_race = None
        if obj is not None:
            town_race = fh2m_town_race(obj.get("index", -1))
        if town_race:
            dwelling_monsters = FH2M_RACE_DWELLING_MONSTERS.get(town_race, [])
            entry["raceName"] = fh2m_race_name(town_race)
            entry["availableToHire"] = [
                OrderedDict([
                    ("monster", fh2m_monster_name(dwelling_monsters[position])
                     if position < len(dwelling_monsters) else None),
                    ("sourceMonsterId", dwelling_monsters[position]
                     if position < len(dwelling_monsters) else None),
                    ("count", count),
                ])
                for position, count in enumerate(metadata.get("availableToHireMonsterCount", []))
            ]
    elif kind == "heroMetadata":
        entry["army"] = [
            OrderedDict([
                ("monster", fh2m_monster_name(monster_type)),
                ("sourceMonsterId", monster_type),
                ("count", count),
            ])
            for monster_type, count in zip(metadata.get("armyMonsterType", []),
                                           metadata.get("armyMonsterCount", []))
        ]
        entry["artifactNames"] = [fh2m_artifact_name(artifact) for artifact in metadata.get("artifacts", [])]
        entry["availableSpellNames"] = [fh2m_spell_name(spell) for spell in metadata.get("availableSpells", [])]
        entry["secondarySkills"] = [
            OrderedDict([
                ("skill", fh2m_secondary_skill_name(skill)),
                ("sourceSkillId", skill),
                ("level", fh2m_skill_level_name(level)),
                ("sourceLevelId", level),
            ])
            for skill, level in zip(metadata.get("secondarySkill", []),
                                     metadata.get("secondarySkillLevel", []))
        ]
        entry["primarySkills"] = OrderedDict([
            ("attack", metadata.get("customAttack")),
            ("defense", metadata.get("customDefense")),
            ("knowledge", metadata.get("customKnowledge")),
            ("spellPower", metadata.get("customSpellPower")),
        ])
        entry["portraitName"] = fh2m_portrait_name(metadata.get("customPortrait", 0))
        entry["patrol"] = OrderedDict([
            ("enabled", bool(metadata.get("isOnPatrol"))),
            ("radius", metadata.get("patrolRadius", 0)),
        ])
        entry["progression"] = OrderedDict([
            ("level", None if metadata.get("customLevel", -1) < 0 else metadata.get("customLevel")),
            ("experience", None if metadata.get("customExperience", -1) < 0 else metadata.get("customExperience")),
            ("mana", None if metadata.get("magicPoints", -1) < 0 else metadata.get("magicPoints")),
        ])
        entry["raceName"] = fh2m_race_name(metadata.get("raceId", 0))
    elif kind == "sphinxMetadata":
        entry["artifactName"] = fh2m_artifact_name(metadata.get("artifact", 0))
        if metadata.get("artifact") == FH2M_SPELL_SCROLL_ID:
            entry["artifactMetadataName"] = fh2m_spell_name(metadata.get("artifactMetadata", 0))
    elif kind == "adventureMapEventMetadata":
        entry["artifactName"] = fh2m_artifact_name(metadata.get("artifact", 0))
        if metadata.get("artifact") == FH2M_SPELL_SCROLL_ID:
            entry["artifactMetadataName"] = fh2m_spell_name(metadata.get("artifactMetadata", 0))
        entry["secondarySkillName"] = fh2m_secondary_skill_name(metadata.get("secondarySkill", 0))
        entry["secondarySkillLevelName"] = fh2m_skill_level_name(metadata.get("secondarySkillLevel", 0))
        entry["monsterName"] = fh2m_monster_name(metadata.get("monsterType", 0))
        entry["primarySkillBonus"] = OrderedDict([
            ("attack", metadata.get("attack", 0)),
            ("defense", metadata.get("defense", 0)),
            ("knowledge", metadata.get("knowledge", 0)),
            ("spellPower", metadata.get("spellPower", 0)),
        ])
    elif kind == "monsterMetadata":
        entry["joinConditionName"] = fh2m_join_condition_name(metadata.get("joinCondition", 0))
    elif kind == "artifactMetadata":
        entry["selectedNames"] = [fh2m_artifact_name(item) for item in metadata.get("selected", [])]
    elif kind == "selectionObjectMetadata":
        # The item type depends on the placed object: Witch's Hut
        # (ADVENTURE_MISCELLANEOUS index 26) selects secondary skills,
        # Pyramid (index 29) selects level 5 spells (world_loadmap.cpp).
        index = obj.get("index") if obj is not None else None
        if index == 26:
            entry["selectedItemNames"] = [
                fh2m_secondary_skill_name(item) for item in metadata.get("selectedItems", [])
            ]
        elif index == 29:
            entry["selectedItemNames"] = [
                fh2m_spell_name(item) for item in metadata.get("selectedItems", [])
            ]
    return entry


def _unified_metadata_to_fh2m(kind, entry):
    """
    Rebuild one fh2m object metadata entry from its unified form, as
    expected by write_fh2m. The raw fh2m identifiers kept by
    _fh2m_metadata_to_unified are used, so the rebuilt structure is
    identical to the original one.
    """
    metadata = OrderedDict(entry)
    metadata.pop("defenders", None)
    metadata.pop("builtBuildingNames", None)
    metadata.pop("bannedBuildingNames", None)
    metadata.pop("mustHaveSpellNames", None)
    metadata.pop("bannedSpellNames", None)
    metadata.pop("army", None)
    metadata.pop("artifactNames", None)
    metadata.pop("availableSpellNames", None)
    metadata.pop("secondarySkills", None)
    metadata.pop("artifactName", None)
    metadata.pop("artifactMetadataName", None)
    metadata.pop("secondarySkillName", None)
    metadata.pop("secondarySkillLevelName", None)
    metadata.pop("monsterName", None)
    metadata.pop("primarySkillBonus", None)
    metadata.pop("primarySkills", None)
    metadata.pop("portraitName", None)
    metadata.pop("patrol", None)
    metadata.pop("progression", None)
    metadata.pop("availableToHire", None)
    metadata.pop("isOnPatrolName", None)
    metadata.pop("raceName", None)
    metadata.pop("selectedNames", None)
    metadata.pop("selectedItemNames", None)
    metadata.pop("joinConditionName", None)
    return metadata


def _fh2m_objects_to_unified(map_data):
    """
    Convert the fh2m object instances into the unified objects section.
    The fh2m storage is already the unified one: objects per tile with
    metadata maps keyed by object id. The metadata maps are normalized
    through _fh2m_metadata_to_unified; the raw fh2m fields are kept so
    that the round-trip remains byte-perfect.
    """
    tiles = OrderedDict()
    width = map_data.get("width", 0)
    for tile_index, tile in enumerate(map_data.get("tiles", [])):
        objects = tile.get("objects", [])
        if not objects:
            continue
        x = tile_index % width
        y = tile_index // width
        tile_key = "{}_{}_{}".format(x, y, 0)
        unified_objs = []
        for obj in objects:
            unified_objs.append(OrderedDict([
                ("id", obj.get("id")),
                ("group", obj.get("group")),
                ("index", obj.get("index")),
            ]))
        tiles[tile_key] = unified_objs

    result = OrderedDict([("tiles", tiles)])
    translation_info = map_data.get("translationInfo") or {}
    if translation_info:
        result["translationInfo"] = OrderedDict(translation_info)

    # Metadata maps keyed by object id, normalized into the unified
    # schema; the raw fh2m fields are kept for the byte-perfect
    # round-trip.
    # Objects sharing an id (a castle and its decoration parts): keep
    # the first object of each relevant group per id.
    objects_by_id = {}
    for obj_list in tiles.values():
        for obj in obj_list:
            obj_id = str(obj.get("id"))
            group = obj.get("group")
            if group in ("KINGDOM_TOWNS", "ADVENTURE_MISCELLANEOUS"):
                objects_by_id.setdefault(obj_id, {}).setdefault(group, obj)
    for key in ("castleMetadata", "heroMetadata", "sphinxMetadata",
                "signMetadata", "adventureMapEventMetadata",
                "selectionObjectMetadata", "capturableObjectsMetadata",
                "monsterMetadata", "artifactMetadata", "resourceMetadata",
                "standardObjectMetadata"):
        value_map = map_data.get(key)
        if value_map:
            expected_group = "KINGDOM_TOWNS" if key == "castleMetadata" else (
                "ADVENTURE_MISCELLANEOUS" if key == "selectionObjectMetadata" else None)
            def _lookup(obj_id):
                if expected_group is None:
                    return None
                return (objects_by_id.get(str(obj_id)) or {}).get(expected_group)
            result[key] = OrderedDict(
                (obj_id, _fh2m_metadata_to_unified(key, metadata, _lookup(obj_id)))
                for obj_id, metadata in value_map.items()
            )

    return result


def _unified_objects_from_h3m(unified):
    """
    Convert the unified objects section back into the h3decoder.py
    structure expected by write_h3m. The h3m binary writer does not
    re-encode object instances yet, so the objects are carried in the
    JSON structure only (Objects > Tiles) for round-tripping.
    """
    objects_section = unified.get("objects")
    if not objects_section:
        return None

    tiles = OrderedDict()
    for tile_key, obj_list in objects_section.get("tiles", {}).items():
        tiles[tile_key] = [OrderedDict(obj) for obj in obj_list]

    result = OrderedDict()
    result["tiles"] = tiles
    for key, value_map in objects_section.items():
        if key in ("tiles", "dropped", "rawData"):
            continue
        result[key] = OrderedDict(value_map)
    raw_data = objects_section.get("rawData")
    if raw_data:
        result["rawData"] = raw_data
    return result
