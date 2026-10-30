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

    # The available heroes bitfield decoded: a cleared bit means the
    # hero cannot be hired (e.g. placed in a prison on the map).
    from correspondence import H3M_HERO_NAMES
    heroes_bitfield_hex = map_data.get("Available Heroes", {}).get("Bitfield", "")
    unavailable_heroes = []
    if heroes_bitfield_hex:
        heroes_bytes = bytes.fromhex(heroes_bitfield_hex)
        for byte_index, hero_byte in enumerate(heroes_bytes):
            for bit in range(8):
                hero_id = byte_index * 8 + bit
                if not hero_byte & (1 << bit) and hero_id < len(H3M_HERO_NAMES):
                    unavailable_heroes.append(OrderedDict([
                        ("id", hero_id),
                        ("name", H3M_HERO_NAMES[hero_id]),
                    ]))
    if unavailable_heroes:
        unified["unavailableHeroes"] = unavailable_heroes

    # The AI behaviors and the custom starting heroes of the h3m
    # players (Behavior: Random, Warrior, Builder, Explorer).
    behaviors = OrderedDict()
    custom_starting_heroes = OrderedDict()
    for player in map_data.get("Players Attributes", {}).get("Players", []):
        behaviors[player.get("Color")] = player.get("Behavior")
    for hero_info in map_data.get("Player Heroes", {}).get("Player Heroes", []):
        color = hero_info.get("Color")
        if hero_info.get("Hero Type") is not None:
            hero_id = hero_info["Hero Type"]
            custom_starting_heroes[color] = OrderedDict([
                ("id", hero_id),
                ("name", H3M_HERO_NAMES[hero_id] if hero_id < len(H3M_HERO_NAMES) else None),
            ])
    if behaviors:
        unified["playerBehaviors"] = behaviors
    if custom_starting_heroes:
        unified["customStartingHeroes"] = custom_starting_heroes

    # The restriction bitfields (AB+ random artifacts, SoD allowed
    # spells and abilities) carried raw.
    if map_data.get("Random Artifacts"):
        unified["randomArtifactsBitfield"] = map_data["Random Artifacts"].get("Bitfield", "")
    if map_data.get("Allowed Spells"):
        unified["allowedSpellsBitfield"] = map_data["Allowed Spells"].get("Bitfield", "")
    if map_data.get("Allowed Abilities"):
        unified["allowedAbilitiesBitfield"] = map_data["Allowed Abilities"].get("Bitfield", "")

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
        skill = entry.get("skill")
        if skill is None:
            entry["skillName"] = None
        elif skill < len(H3M_SECONDARY_SKILL_NAMES):
            entry["skillName"] = H3M_SECONDARY_SKILL_NAMES[skill]
        else:
            entry["skillName"] = str(skill)
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
    # The map has heroes when at least one hero object exists: the
    # official Heroes III tools read this header byte to validate
    # the starting conditions of the playable players.
    unified["hasHero"] = bool(hero_object_colors)
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
        version_name = H3M_VERSION_NAMES.get(unified.get("sourceVersion"), "RoE (Restoration of Erathia)")
    else:
        # The fh2m maps encode to the RoE layout (the object encoder
        # writes the RoE object data).
        version_name = "RoE (Restoration of Erathia)"

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
    # The Heroes II defeatOtherSide (a team-based victory) has no
    # special Heroes III condition: the standard victory (defeating
    # every other side) already covers it, so it converts to None
    # like defeatEveryone.
    if victory_type in ("defeatEveryone", "defeatOtherSide"):
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

    # Rumors: the fh2m rumors carry no name; the h3m rumors need
    # one, generated as RumeurX with X incremented per rumor.
    rumors = unified.get("rumors", [])
    rumor_number = 0
    converted_rumors = []
    for r in rumors:
        name = r.get("name")
        if not name:
            rumor_number += 1
            name = "Rumeur%d" % rumor_number
        converted_rumors.append(OrderedDict([("Name", name), ("Text", r.get("text", ""))]))
    data["Rumors"] = OrderedDict([
        ("Number of Rumors", len(converted_rumors)),
        ("Rumors", converted_rumors),
    ])

    is_fh2m_source = unified.get("sourceGame") != "h3m"

    # Roads and rivers (fh2m source): the fh2m format stores them as
    # ROADS and STREAMS objects on tiles; convert them back to the
    # h3m per-tile Road/River Type fields.
    fh2m_road_tiles = set()
    fh2m_river_tiles = set()
    if is_fh2m_source:
        for tile_key, obj_list in (unified.get("objects") or {}).get("tiles", {}).items():
            parts = tile_key.split("_")
            if len(parts) != 3:
                continue
            x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
            for obj in obj_list:
                group = obj.get("group")
                if group == "ROADS":
                    fh2m_road_tiles.add((x, y, z))
                elif group == "STREAMS":
                    fh2m_river_tiles.add((x, y, z))

    terrain_by_level = []
    for level in unified.get("terrain", {}).get("levels", []):
        grid = OrderedDict()
        for cell in level.get("grid", []):
            x, y, z = cell.get("x", 0), cell.get("y", 0), cell.get("z", 0)
            if unified.get("sourceGame") == "h3m":
                terrain_name = cell.get("sourceTerrain", cell.get("terrain", "Dirt"))
                if terrain_name not in H3M_TOWN_TYPES and terrain_name not in UNIFIED_TO_H3M_TERRAINS.values():
                    terrain_name = UNIFIED_TO_H3M_TERRAINS.get(cell.get("terrain", "Dirt"), "Dirt")
                picture = cell.get("sourcePicture", 0)
                mirroring = cell.get("sourceMirroring", "0x00")
                road = cell.get("sourceRoad", "None")
                road_props = cell.get("sourceRoadProperties", 0)
                river = cell.get("sourceRiver", "None")
                river_props = cell.get("sourceRiverProperties", 0)
            else:
                terrain_name = UNIFIED_TO_H3M_TERRAINS.get(cell.get("terrain", "Grass"), "Dirt")
                # The fh2m terrain image index becomes the h3m
                # Terrain Picture: the fh2m images are numbered
                # globally by terrain range while the h3m images are
                # per-terrain variants (about 72 per terrain). The
                # position within the fh2m terrain range, modulo 72,
                # gives a valid h3m image variant.
                picture = 0
                source_terrain = cell.get("sourceTerrain", "")
                if source_terrain.startswith("terrain:"):
                    try:
                        image_index = int(source_terrain[len("terrain:"):])
                        range_start = 0
                        for start_index, name in FH2M_TERRAIN_INDEX_RANGES:
                            if name == cell.get("terrain", "Grass"):
                                break
                            range_start = start_index
                        picture = (image_index - range_start) % 72
                    except ValueError:
                        picture = 0
                mirroring = "0x00"
                road = "Dirt" if (x, y, z) in fh2m_road_tiles else "None"
                road_props = 0
                river = "Clear" if (x, y, z) in fh2m_river_tiles else "None"
                river_props = 0
            grid[(x, y)] = (z, terrain_name, picture, mirroring,
                            road, road_props, river, river_props)
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

    # Objects: an h3m source keeps its raw object section for a
    # byte-perfect round-trip; an fh2m source gets its objects
    # encoded into a fresh h3m raw section.
    version_ab = "Armageddon" in version_name or "Shadow" in version_name
    version_sod = "Shadow" in version_name
    if unified.get("sourceGame") != "h3m":
        # The h3m terrain per tile (level 0), used by the object
        # encoder to pick the terrain-dependent decorative classes
        # (mountains, volcanos, dunes).
        tile_terrains = {}
        if terrain_by_level:
            for (x, y), values in terrain_by_level[0].items():
                tile_terrains[(x, y)] = values[1]
        encoded = _encode_h3m_objects(unified, version_ab, version_sod,
                                      tile_terrains)
        if encoded:
            object_count = struct.unpack("<I", bytes.fromhex(encoded)[12:16])[0] if len(encoded) > 32 else 0
            data["Objects"] = OrderedDict([
                ("Number of Objects", object_count),
                ("Raw Data", encoded),
                ("Tiles", OrderedDict()),
            ])
    if "Objects" not in data:
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
                                  H3M_HERO_NAMES, H3M_TO_FH2M_INTERACTIVE,
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
            if resource is None:
                # Random resource (h3m class 76): the fh2m Random
                # Resource object (ADVENTURE_TREASURES index 8).
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_TREASURES"),
                    ("index", 8),
                ]))
                translated_metadata.setdefault("resourceMetadata", OrderedDict())[str(obj_id)] = OrderedDict([
                    ("count", resource_meta.get("count") or 0),
                ])
                continue
            if resource < 0 or resource >= len(FH2M_RESOURCE_ORDER):
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
                # No Heroes II equivalent: a random artifact of the
                # same Heroes III class (Treasure -> 92, Minor -> 93,
                # Major and Relic -> 94; Heroes II has no random
                # relic, the relic convert to the random major).
                from correspondence import H3M_ARTIFACT_CLASSES
                artifact_class = H3M_ARTIFACT_CLASSES.get(artifact)
                if artifact_class is None:
                    dropped_ids.append(obj_id)
                    continue
                fh2m_index = {1: 92, 2: 93, 3: 94, 4: 94}.get(artifact_class)
                if fh2m_index is None:
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
                # possible; a neutral hero (owner 255) is a prison
                # inmate - it converts to the fh2m Jail (MISC 47), the
                # Heroes II prison releasing the hero on capture.
                if owner is not None and owner < len(FH2M_PLAYER_COLORS):
                    color_id = FH2M_PLAYER_COLORS.index(
                        FH2M_PLAYER_COLORS[owner]) if False else owner
                    hero_type = 0
                else:
                    translated.append(OrderedDict([
                        ("id", obj_id),
                        ("group", "ADVENTURE_MISCELLANEOUS"),
                        ("index", 47),
                    ]))
                    continue
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
            # The h3m class (from the group name) converts to a
            # Heroes II object: the interactive classes with an
            # equivalent first (monoliths, wells, gardens, towers,
            # learning stones, water wheels, windmills), then the
            # decorative families; the classes without a mapping
            # stay dropped.
            try:
                obj_class = int(group[len("UNDEFINED_"):])
            except ValueError:
                dropped_ids.append(obj_id)
                continue
            interactive = H3M_TO_FH2M_INTERACTIVE.get(obj_class)
            if interactive is not None:
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", interactive[0]),
                    ("index", interactive[1]),
                ]))
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

    # The h3m terrain overlays (cursed ground, magic plains) are
    # passive battlefield zones with no Heroes II mechanic: their
    # tiles become plain terrain instead - the cursed grounds
    # become Dirt, the magic plains Grass.
    if is_h3m_source:
        overlay_terrains = {}
        for tile_key, obj_list in (objects_section.get("tiles") or {}).items():
            parts = tile_key.split("_")
            if len(parts) != 3:
                continue
            for obj in obj_list:
                group = obj.get("group", "")
                if group == "UNDEFINED_21":
                    overlay_terrains[(int(parts[0]), int(parts[1]))] = "Dirt"
                elif group == "UNDEFINED_46":
                    overlay_terrains[(int(parts[0]), int(parts[1]))] = "Grass"
        for (x, y), terrain_name in overlay_terrains.items():
            if (x, y) in terrain_by_position:
                terrain_index = UNIFIED_TO_FH2M_TERRAIN_INDEX.get(terrain_name, 30)
                flags = terrain_by_position[(x, y)][1]
                terrain_by_position[(x, y)] = (terrain_index, flags)
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


def _encode_h3m_objects(unified, version_ab, version_sod, tile_terrains=None):
    """
    Encode the unified objects (from an fh2m source map) into the h3m
    raw object section bytes: a sprite catalog (one def per h3m class
    and subclass, from the FH2M_TO_H3M_CATALOG reference extracted
    from real maps) followed by the object instances with their
    per-type data. The supported types cover the main game objects:
    monsters, resources, artifacts, mines, dwellings, signs, towns,
    heroes and the landscape decorative families.

    Returns the hex string of the raw section, or None when nothing
    could be encoded.
    """
    import struct
    from io import BytesIO
    from correspondence import (FH2M_TO_H3M_CATALOG,
                                  FH2M_TO_H3M_MONSTERS,
                                  FH2M_TO_H3M_ARTIFACTS,
                                  FH2M_TO_H3M_RESOURCES)

    objects_section = unified.get("objects") or {}
    tiles = objects_section.get("tiles") or {}
    monster_meta = objects_section.get("monsterMetadata") or {}
    resource_meta = objects_section.get("resourceMetadata") or {}
    artifact_meta = objects_section.get("artifactMetadata") or {}

    # --- Collect the instances to encode, in tile order ---
    instances = []
    for tile_key, obj_list in tiles.items():
        parts = tile_key.split("_")
        if len(parts) != 3:
            continue
        x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
        for obj in obj_list:
            group = obj.get("group")
            index = obj.get("index", 0)
            obj_id = obj.get("id", 0)
            meta = None
            entry = None
            if group == "MONSTERS":
                creature = index + 1
                m = monster_meta.get(str(obj_id)) or {}
                count = m.get("count") or 0
                # Random monsters (fh2m ids 67-71) map to the h3m
                # random monster classes 71-75.
                if creature in (67, 68, 69, 70, 71):
                    obj_class = 71 + (creature - 67)
                    entry = ("monster", (x, y, z), (obj_class, 0), count)
                else:
                    h3m_creature = FH2M_TO_H3M_MONSTERS.get(creature)
                    if h3m_creature is None:
                        continue
                    entry = ("monster", (x, y, z), (54, h3m_creature), count)
            elif group == "ADVENTURE_TREASURES":
                # The fh2m treasure index is the resource type
                # (0-6: wood, mercury, ore, sulfur, crystal, gems,
                # gold); the Genie's Lamp (7), the Random Resource
                # (8), the Treasure Chest (9) and the campfires
                # (10-12) map through the misc table.
                h3m_resource = FH2M_TO_H3M_RESOURCES.get(index)
                if h3m_resource is not None:
                    m = resource_meta.get(str(obj_id)) or {}
                    count = m.get("count") or 0
                    entry = ("resource", (x, y, z), (79, h3m_resource), count)
                else:
                    from correspondence import FH2M_TO_H3M_MISC
                    h3m_target = FH2M_TO_H3M_MISC.get("TREASURE_%d" % index)
                    if h3m_target is not None:
                        if h3m_target[0] == 76:
                            # Random Resource: the h3m random resource
                            # carries the same count layout as a fixed
                            # resource.
                            m = resource_meta.get(str(obj_id)) or {}
                            count = m.get("count") or 0
                            entry = ("resource", (x, y, z), (76, 0), count)
                        else:
                            entry = ("generic", (x, y, z), h3m_target, None)
            elif group == "ADVENTURE_ARTIFACTS":
                if index in (91, 92, 93, 94, 95):
                    # The fh2m random artifacts (see map_object_info.cpp,
                    # populateAdventureArtifacts) encode to the matching
                    # h3m random artifact classes; the Ultimate maps to
                    # the random relic (69).
                    entry = ("artifact", (x, y, z),
                             (65 + {91: 0, 92: 1, 93: 2, 94: 3, 95: 4}[index], 0),
                             None)
                else:
                    artifact = index + 1
                    h3m_artifact = FH2M_TO_H3M_ARTIFACTS.get(artifact)
                    if h3m_artifact is None:
                        continue
                    entry = ("artifact", (x, y, z), (5, h3m_artifact), None)
            elif group == "ADVENTURE_MISCELLANEOUS" and index == 0:
                entry = ("sign", (x, y, z), (91, 0), None)
            elif group == "KINGDOM_HEROES":
                # A hero: the object index is color * 7 + race. The
                # hero type comes from the hero pairing: the first
                # h3m hero paired to the Heroes II race. The color
                # (index // 7) converts to the h3m owner byte so the
                # playable players keep their starting heroes.
                hero_meta = (objects_section.get("heroMetadata") or {}).get(str(obj_id)) or {}
                from correspondence import FH2M_TO_H3M_HERO_RACE
                race = index % 7
                hero_type = FH2M_TO_H3M_HERO_RACE.get(race)
                if hero_type is None:
                    # A random race (6) or an unmapped race: encode
                    # a random hero (type 0xFF, sprite AH0000).
                    hero_type = 0
                hero_payload = dict(hero_meta)
                hero_payload["type"] = hero_type
                owner_color_id = index // 7
                if 0 <= owner_color_id < len(FH2M_PLAYER_COLORS):
                    owner_color = FH2M_PLAYER_COLORS[owner_color_id]
                    if owner_color in H3M_PLAYER_COLORS:
                        hero_payload["owner"] = H3M_PLAYER_COLORS.index(owner_color)
                entry = ("hero", (x, y, z), (34, hero_type), hero_payload)
            elif group == "KINGDOM_TOWNS":
                # A town: the object index encodes the race (race * 2
                # for a castle); the castleMetadata carries the
                # defenders.
                from correspondence import FH2M_TOWN_RACE_ORDER
                race_id = index // 2
                town_type = None
                if 0 <= race_id < len(FH2M_TOWN_RACE_ORDER):
                    from correspondence import H3M_TOWN_TYPE_TO_FH2M_RACE
                    for tt, race in H3M_TOWN_TYPE_TO_FH2M_RACE.items():
                        if race == FH2M_TOWN_RACE_ORDER[race_id]:
                            town_type = tt
                            break
                if town_type is not None:
                    castle_meta = (objects_section.get("castleMetadata") or {}).get(str(obj_id)) or {}
                    entry = ("town", (x, y, z), (98, town_type), castle_meta)
            elif group in ("ADVENTURE_MISCELLANEOUS", "ADVENTURE_WATER"):
                # The miscellaneous and water objects with a
                # confirmed h3m sprite map through the misc table.
                from correspondence import FH2M_TO_H3M_MISC
                h3m_key = ("MISC_%d" % index) if group == "ADVENTURE_MISCELLANEOUS" else "WATER_%d" % index
                h3m_target = FH2M_TO_H3M_MISC.get(h3m_key)
                if h3m_target is not None:
                    obj_class, obj_subclass = h3m_target
                    meta = (objects_section.get("signMetadata") or {}).get(str(obj_id)) or {}
                    entry = ("generic", (x, y, z), (obj_class, obj_subclass), meta)
            elif group == "ADVENTURE_POWER_UPS":
                # The shrine circles (index 14-16) map back to the
                # h3m shrine classes 88-90; the Gazebo (11) maps to
                # the h3m learning stone; the other power-up objects
                # have no simple h3m equivalent.
                from correspondence import FH2M_TO_H3M_SHRINES
                h3m_shrine = FH2M_TO_H3M_SHRINES.get(index)
                if h3m_shrine is not None:
                    shrine_meta = (objects_section.get("shrineMetadata") or {}).get(str(obj_id)) or {}
                    entry = ("shrine", (x, y, z), (h3m_shrine, 0), shrine_meta)
                else:
                    from correspondence import FH2M_TO_H3M_MISC
                    h3m_target = FH2M_TO_H3M_MISC.get("POWER_%d" % index)
                    if h3m_target is not None:
                        entry = ("generic", (x, y, z), h3m_target, None)
            elif group == "ADVENTURE_MINES":
                # The fh2m mine index maps to the h3m ownable mine
                # (class 53, subclass per mine type).
                from correspondence import FH2M_TO_H3M_MINES
                h3m_mine = FH2M_TO_H3M_MINES.get(index)
                if h3m_mine is not None:
                    entry = ("ownable", (x, y, z), h3m_mine, None)
            elif group == "ADVENTURE_DWELLINGS":
                # The fh2m dwelling index maps to the h3m ownable
                # dwelling (class 17, subclass = creature id).
                from correspondence import FH2M_TO_H3M_DWELLINGS
                h3m_dwelling = FH2M_TO_H3M_DWELLINGS.get(index)
                if h3m_dwelling is not None:
                    entry = ("ownable", (x, y, z), h3m_dwelling, None)
            elif group.startswith("LANDSCAPE"):
                # Decorative objects: the landscape index maps back
                # to the h3m decorative class (subclass 0). The
                # mountains pick their h3m class from the terrain of
                # the tile (the fh2m variant index formula is
                # undocumented): Lava -> volcano, Desert -> dune,
                # Dirt -> mound, others -> mountain.
                from correspondence import FH2M_LANDSCAPE_TO_H3M
                h3m_class = FH2M_LANDSCAPE_TO_H3M.get((group, index))
                if group == "LANDSCAPE_TREES" and h3m_class is not None:
                    # The tree variants pick their h3m class from
                    # the tile terrain: Swamps and Dirt -> dead
                    # vegetation (119 - the bare/dead trees), the
                    # other terrains -> trees (155).
                    tile_terrain = (tile_terrains or {}).get((x, y), "Grass")
                    h3m_class = 119 if tile_terrain in ("Swamp", "Dirt") else 155
                if group == "LANDSCAPE_MOUNTAINS" and h3m_class is not None:
                    tile_terrain = (tile_terrains or {}).get((x, y), "Grass")
                    if tile_terrain == "Lava":
                        h3m_class = 158  # volcano
                    elif tile_terrain == "Sand":
                        h3m_class = 148  # dune
                    elif tile_terrain == "Dirt":
                        h3m_class = 133  # mound
                    else:
                        h3m_class = 134  # mountain
                if h3m_class is not None:
                    entry = ("decorative", (x, y, z), (h3m_class, 0), None)
            if entry:
                instances.append(entry)

    if not instances:
        return None

    # --- Build the sprite catalog: one def per used (class, subclass) ---
    catalog_keys = []
    catalog_entries = []
    kind_of = {}
    for entry in instances:
        _, _, (obj_class, obj_subclass), _ = entry
        key = (obj_class, obj_subclass)
        if key not in kind_of:
            ref = FH2M_TO_H3M_CATALOG.get(key)
            if ref is None and obj_class == 34:
                # The hero sprites follow the AH0<type>00.DEF
                # convention (the standard hero sprite naming of the
                # h3m format); the passability matches the prison
                # sprite (the closest single-tile hero object).
                ref = ('AH0%02X00.DEF' % (obj_subclass or 0),
                       'ffffffffff3f000000000080ff01ff00',
                       '000000000000000000000000000000000000')
            if ref is None:
                continue
            kind_of[key] = len(catalog_keys)
            catalog_keys.append(key)
            catalog_entries.append(ref)

    # Drop the instances whose sprite is unknown.
    instances = [e for e in instances
                 if (e[2][0], e[2][1]) in kind_of]
    if not instances:
        return None

    buffer = BytesIO()
    buffer.write(struct.pack("<I", len(catalog_entries)))
    for i, key in enumerate(catalog_keys):
        sprite, passability, trailing = catalog_entries[i]
        name_bytes = sprite.encode("latin1")
        buffer.write(struct.pack("<i", len(name_bytes)))
        buffer.write(name_bytes)
        buffer.write(bytes.fromhex(passability))
        buffer.write(struct.pack("<II", key[0], key[1]))
        buffer.write(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    # --- Instances ---
    buffer.write(struct.pack("<I", len(instances)))
    for entry in instances:
        kind_name, (x, y, z), (obj_class, obj_subclass), payload = entry
        buffer.write(struct.pack("<BBB", x, y, z))
        buffer.write(struct.pack("<I", kind_of[(obj_class, obj_subclass)]))
        buffer.write(b"\x00" * 5)
        if kind_name == "monster":
            if version_ab:
                buffer.write(struct.pack("<I", 0))  # objectID
            buffer.write(struct.pack("<HB", payload & 0xFFFF or 1, 0))
            buffer.write(struct.pack("<B", 0))  # no treasure
            buffer.write(b"\x00" * 4)
        elif kind_name == "resource":
            buffer.write(struct.pack("<B", 0))  # not guarded
            buffer.write(struct.pack("<II", payload, 0))
        elif kind_name == "artifact":
            buffer.write(struct.pack("<B", 0))  # not guarded
        elif kind_name == "sign":
            buffer.write(struct.pack("<i", 0))  # empty message
            buffer.write(b"\x00" * 4)
        elif kind_name == "decorative":
            pass  # no per-instance data
        elif kind_name == "ownable":
            buffer.write(struct.pack("<I", 0xFFFFFF))  # neutral owner
        elif kind_name == "shrine":
            # RoE shrine: a random spell (0xFFFFFFFF).
            buffer.write(struct.pack("<I", 0xFFFFFFFF))
        elif kind_name == "generic":
            # The generic objects: signs (classes 59/91) carry a
            # message; the ownable objects (class 42 Stone Liths)
            # carry an owner; the other misc objects (windmill,
            # lean-to, water wheel, witch hut, observation tower,
            # bottle, buoy) carry no per-instance data.
            if obj_class in (59, 91):
                message = (payload or {}).get("message") or ""
                msg_bytes = message.encode("cp1252", errors="replace")
                buffer.write(struct.pack("<i", len(msg_bytes)))
                buffer.write(msg_bytes)
                buffer.write(b"\x00" * 4)
            elif obj_class == 42:
                # The Stone Liths are ownable: an owner word.
                buffer.write(struct.pack("<I", 0xFFFFFF))  # neutral
        elif kind_name == "hero":
            # RoE hero layout: owner, type, then the customization
            # flags (name, experience, face, skills, creatures,
            # formation, artifacts, patrol radius) and 16 trailing
            # unknown bytes. The fh2m heroMetadata converts: the
            # custom name, the experience, the secondary skills
            # (through the inverse secondary skill table) and the
            # army (the creature pairs).
            from correspondence import FH2M_TO_H3M_MONSTERS
            meta = payload or {}
            owner = meta.get("owner")
            buffer.write(struct.pack("<B", owner if owner is not None else 0xFF))
            hero_type = meta.get("type")
            buffer.write(struct.pack("<B", hero_type if hero_type is not None else 0xFF))
            name = meta.get("customName") or meta.get("name") or ""
            if name:
                name_bytes = name.encode("cp1252", errors="replace")
                buffer.write(struct.pack("<B", 1))
                buffer.write(struct.pack("<i", len(name_bytes)))
                buffer.write(name_bytes)
            else:
                buffer.write(struct.pack("<B", 0))
            experience = meta.get("customExperience")
            buffer.write(struct.pack("<I", experience if experience and experience > 0 else 0))
            buffer.write(struct.pack("<B", 0))  # no custom face
            # Secondary skills: convert the first non-empty fh2m
            # skills through the inverse table.
            skills = meta.get("secondarySkill") or []
            skill_levels = meta.get("secondarySkillLevel") or []
            converted_skills = []
            for i, skill_id in enumerate(skills[:8]):
                if not skill_id:
                    continue
                level = skill_levels[i] if i < len(skill_levels) else 0
                converted_skills.append((skill_id, level))
            if converted_skills:
                buffer.write(struct.pack("<B", 1))
                buffer.write(struct.pack("<I", len(converted_skills)))
                for h3_skill, level in converted_skills:
                    # The fh2m secondary skill ids map back to the
                    # h3m ids through the forward table.
                    from correspondence import H3M_TO_FH2M_SECONDARY_SKILLS
                    fh2_to_h3 = {v: k for k, v in H3M_TO_FH2M_SECONDARY_SKILLS.items()}
                    buffer.write(struct.pack("<BB", fh2_to_h3.get(h3_skill, 0), level))
            else:
                buffer.write(struct.pack("<B", 0))
            # Army: the fh2m 5 slots convert to the h3m 7 slots.
            army_types = meta.get("armyMonsterType") or []
            army_counts = meta.get("armyMonsterCount") or []
            army = []
            for i in range(min(len(army_types), 5)):
                creature = army_types[i]
                count = army_counts[i] if i < len(army_counts) else 0
                h3_creature = FH2M_TO_H3M_MONSTERS.get(creature) if creature else None
                if h3_creature is None or not count:
                    continue
                army.append((h3_creature, count))
            if army:
                buffer.write(struct.pack("<B", 1))
                for slot in range(7):
                    if slot < len(army):
                        buffer.write(struct.pack("<BH", army[slot][0], army[slot][1]))
                    else:
                        # An empty slot: creature 0xFF means none.
                        buffer.write(struct.pack("<BH", 0xFF, 0))
            else:
                buffer.write(struct.pack("<B", 0))
            buffer.write(struct.pack("<B", 0))  # formation
            # Artifacts: the fh2m worn artifacts convert through the
            # inverse artifact table.
            from correspondence import H3M_TO_FH2M_ARTIFACTS
            fh2_to_h3_art = {v: k for k, v in H3M_TO_FH2M_ARTIFACTS.items()}
            artifacts = meta.get("artifacts") or []
            converted_artifacts = []
            for art in artifacts[:18]:
                converted_artifacts.append(fh2_to_h3_art.get(art, 0) or 0)
            if any(converted_artifacts):
                buffer.write(struct.pack("<B", 1))
                for slot in range(18):
                    value = converted_artifacts[slot] if slot < len(converted_artifacts) else 0
                    buffer.write(struct.pack("<B", value & 0xFF))
                buffer.write(struct.pack("<H", 0))  # empty bag
            else:
                buffer.write(struct.pack("<B", 0))
            patrol = meta.get("isOnPatrol")
            radius = meta.get("patrolRadius") or 0
            buffer.write(struct.pack("<B", radius if patrol else 0xFF))
            buffer.write(b"\x00" * 16)
        elif kind_name == "town":
            # RoE town layout: owner, name, creatures (7 slots),
            # formation, buildings flags, spell bitfields and events.
            # The fh2m castleMetadata converts: the custom name, the
            # garrison defenders and the built buildings (the fh2m
            # flags map back through the building bit tables).
            from correspondence import (H3M_DWELLING_BITS,
                                         H3M_TOWN_BUILDING_BITS,
                                         FH2M_TO_H3M_MONSTERS)
            meta = payload or {}
            buffer.write(struct.pack("<B", 0xFF))  # owner: neutral
            name = meta.get("customName") or ""
            if name:
                name_bytes = name.encode("cp1252", errors="replace")
                buffer.write(struct.pack("<B", 1))
                buffer.write(struct.pack("<i", len(name_bytes)))
                buffer.write(name_bytes)
            else:
                buffer.write(struct.pack("<B", 0))
            # Garrison: the fh2m defenders convert to the h3m 7
            # creature slots.
            defender_types = meta.get("defenderMonsterType") or []
            defender_counts = meta.get("defenderMonsterCount") or []
            defenders = []
            for i in range(min(len(defender_types), 5)):
                creature = defender_types[i]
                count = defender_counts[i] if i < len(defender_counts) else 0
                h3_creature = FH2M_TO_H3M_MONSTERS.get(creature) if creature else None
                if h3_creature is None or not count:
                    continue
                defenders.append((h3_creature, count))
            if defenders:
                buffer.write(struct.pack("<B", 1))
                for slot in range(7):
                    if slot < len(defenders):
                        buffer.write(struct.pack("<BH", defenders[slot][0], defenders[slot][1]))
                    else:
                        buffer.write(struct.pack("<BH", 0xFF, 0))
            else:
                buffer.write(struct.pack("<B", 0))
            buffer.write(struct.pack("<B", 0))  # formation
            # Buildings: the fh2m built flags map back to the h3m
            # bitfield through the inverse of the bit tables.
            built_flags = meta.get("builtBuildings") or []
            bitfield = bytearray(6)
            flag_to_bit = {}
            for (byte_index, bit), flag in list(H3M_TOWN_BUILDING_BITS.items()) + list(H3M_DWELLING_BITS.items()):
                if flag:
                    flag_to_bit[flag] = (byte_index, bit)
            for flag in built_flags:
                position = flag_to_bit.get(flag)
                if position:
                    bitfield[position[0]] |= (1 << position[1])
            has_custom_buildings = bool(built_flags) or bool(meta.get("bannedBuildings"))
            if has_custom_buildings:
                buffer.write(struct.pack("<B", 1))
                buffer.write(bytes(bitfield))
                # Disabled buildings: the banned flags map back the
                # same way.
                banned_flags = meta.get("bannedBuildings") or []
                banned_field = bytearray(6)
                for flag in banned_flags:
                    position = flag_to_bit.get(flag)
                    if position:
                        banned_field[position[0]] |= (1 << position[1])
                buffer.write(bytes(banned_field))
            else:
                buffer.write(struct.pack("<B", 0))
                buffer.write(struct.pack("<B", 0))  # hasFort: no
            buffer.write(b"\x00" * 9)  # impossible spells: all allowed
            buffer.write(struct.pack("<I", 0))  # no events
            buffer.write(b"\x00\x00\x00")  # trailing 3 bytes

    return buffer.getvalue().hex()


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
