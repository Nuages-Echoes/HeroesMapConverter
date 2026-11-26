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

import random as _random
import struct
import uuid as _uuid
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

# fh2m calls its third player color "Yellow"; Heroes III calls the same
# slot "Tan" (index 2). Alias used when mapping fh2m colors to h3m ones.
FH2M_TO_H3M_COLOR_ALIAS = {"Yellow": "Tan"}

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

# h3m terrain -> unified terrain. The h3m Rough terrain converts
# to the Heroes II Desert terrain (and back); the unified Beach
# terrain converts back to the h3m Sand terrain.
H3M_TERRAINS = {
    "Dirt": "Dirt",
    "Sand": "Desert",
    "Grass": "Grass",
    "Snow": "Snow",
    "Swamp": "Swamp",
    "Rough": "Desert",
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
        # h3m sources: keep the raw detail bytes so the writer can
        # restore them verbatim (round-trip fidelity).
        vic_detail = map_data.get("Victory Condition", {}).get("Detail")
        victory["metadata"] = list(bytes.fromhex(vic_detail)) if vic_detail else []
    unified["victoryCondition"] = victory

    # Loss condition
    loss = OrderedDict()
    loss_type = map_data.get("Loss Condition", {}).get("Type", "None")
    if loss_type == "None":
        loss["type"] = "loseEverything"
    else:
        loss["type"] = H3M_LOSS_CONDITIONS.get(int(loss_type, 16), "unknown")
    loss_detail = map_data.get("Loss Condition", {}).get("Detail")
    loss["metadata"] = list(bytes.fromhex(loss_detail)) if loss_detail else []
    unified["lossCondition"] = loss

    # Rumors
    rumors = []
    for rumor in map_data.get("Rumors", {}).get("Rumors", []):
        rumors.append(OrderedDict([
            ("name", rumor.get("Name", "")),
            ("text", rumor.get("Text", "")),
        ]))
    unified["rumors"] = rumors

    # Timed events (the h3m global events table at the end of the file).
    # The h3m players mask is a bitmask over H3M_PLAYER_COLORS; the
    # applies-to-human/computer flags select which kind of controller the
    # masked players must be (RoE/AB records carry no human flag: the mask
    # alone selects the players and only the computer flag applies). The
    # h3m first occurrence is 0-based (0 = calendar day 1); the unified
    # firstOccurrenceDay is 1-based, like fh2m.
    daily_events = []
    events_section = map_data.get("Events") or {}
    has_human_flag = events_section.get("Human Flag Present", True)
    for event in events_section.get("Events", []):
        mask = event.get("Players Mask", 0)
        colors = [H3M_PLAYER_COLORS[bit] for bit in range(8) if mask & (1 << bit)]
        if has_human_flag:
            human_colors = list(colors) if event.get("Applies to Human") else []
        else:
            human_colors = list(colors)
        computer_colors = list(colors) if event.get("Applies to Computer") else []
        daily_events.append(OrderedDict([
            ("name", event.get("Name", "")),
            ("message", event.get("Message", "")),
            ("humanColors", human_colors),
            ("computerColors", computer_colors),
            ("firstOccurrenceDay", event.get("First Occurrence Day", 0) + 1),
            ("repeatPeriodInDays", event.get("Repeat Period In Days", 0)),
            ("resources", OrderedDict((name, value) for name, value in event.get("Resources", {}).items())),
        ]))
    unified["dailyEvents"] = daily_events

    # Terrain
    levels = []
    # Original fh2m road indices carried by an h3m produced by this
    # converter (in-memory side table; the h3m binary tile record has
    # no room for them): "x_y_z" -> original ROADS index.
    road_index_side = map_data.get("fh2mRoadIndex") or {}
    for section_name, z in (("Surface Map", 0), ("Underground Map", 1)):
        section = map_data.get(section_name)
        if section is None:
            continue
        grid = []
        for cell in section.get("Grid", []):
            source_terrain = cell.get("Terrain Type", "Dirt")
            entry = OrderedDict([
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
            ])
            side_key = "{}_{}_{}".format(cell.get("X", 0), cell.get("Y", 0), z)
            if side_key in road_index_side:
                entry["sourceRoadIndex"] = road_index_side[side_key]
            grid.append(entry)
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
                    ("skill", (H3M_SECONDARY_SKILL_NAMES[sk.get("id")]
                               if sk.get("id") is not None
                               and sk.get("id") < len(H3M_SECONDARY_SKILL_NAMES)
                               else str(sk.get("id")))),
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
            unified_obj = OrderedDict([
                ("id", obj.get("id")),
                ("group", obj.get("group")),
                ("index", obj.get("index")),
            ])
            # The h3m catalog entry of the instance: the sprite name
            # carries the terrain variant of the multi-def classes
            # (the class 53 mines) and the subclass is the object
            # subtype within the class; both are needed by the
            # h3m -> fh2m mine translation.
            for extra in ("sprite", "class", "subclass"):
                if obj.get(extra) is not None:
                    unified_obj[extra] = obj[extra]
            unified_objs.append(unified_obj)
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
            ("name", None),
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
    road_index_by_pos = {}
    for index, tile in enumerate(map_data.get("tiles", [])):
        for obj in tile.get("objects", []):
            if obj.get("group") == "ROADS":
                road_index_by_pos[(index % width, index // width)] = obj.get("index", 0)
    for index, tile in enumerate(map_data.get("tiles", [])):
        cell = OrderedDict([
            ("x", index % width),
            ("y", index // width),
            ("z", 0),
            ("terrain", _fh2m_terrain_name(tile.get("terrainIndex", 0))),
            ("sourceTerrain", "terrain:{}".format(tile.get("terrainIndex", 0))),
            ("flags", tile.get("terrainFlags", 0)),
        ])
        # The original fh2m ROADS index (connection bitfield plus the
        # 256 * visual variant), carried on the terrain cell so the
        # unified JSON keeps the exact H2 road segment and the h3m ->
        # fh2m writer can restore it instead of re-deriving it.
        road_index = road_index_by_pos.get((index % width, index // width))
        if road_index is not None:
            cell["sourceRoadIndex"] = road_index
        grid.append(cell)
    unified["terrain"] = OrderedDict([
        ("levels", [OrderedDict([("grid", grid)])]),
    ])

    # Objects (stored per tile with metadata maps keyed by object id)
    unified["objects"] = _fh2m_objects_to_unified(map_data)

    return unified


# Olden Era (hommoe) player colors: a spawn's colorId indexes this list
# when >= 0; every sample carries colorId=-1, in which case the spawn
# order is used instead.
HOMMOE_PLAYER_COLORS = ["Blue", "Green", "Red", "Yellow", "Orange", "Purple", "Tan", "Teal", "Pink"]

# Olden Era faction sid -> display name (Core.zip DB/fractions; see the
# faction table in /workspace/references/map-editor-json-tool/src/lib/factions.ts).
# OE factions have no Heroes II/III equivalent, so they keep their own
# names in the unified race set.
HOMMOE_FACTION_NAMES = {
    "human": "Temple",
    "undead": "Necropolis",
    "dungeon": "Dungeon",
    "nature": "Grove",
    "demons": "Hive",
    "unfrozen": "Schism",
    "neutral": "Neutral",
}

# unified race -> Olden Era factionSid (Races table, HOMMOE column of
# heroes_field_correspondence.english.txt, given there as OE display names;
# sids via HOMMOE_FACTION_NAMES): Knight/Barbarian -> Temple ("human"),
# Sorceress/Conflux -> Grove ("nature"), Warlock -> Dungeon ("dungeon"),
# Wizard -> Schism ("unfrozen"), Necromancer -> Necropolis ("undead"),
# Inferno/Fortress -> Hive ("demons"), Random -> "" (empty on real maps).
UNIFIED_TO_HOMMOE_FACTION_SID = {
    "Random": "",
    "Knight": "human",
    "Barbarian": "human",
    "Sorceress": "nature",
    "Warlock": "dungeon",
    "Wizard": "unfrozen",
    "Necromancer": "undead",
    "Inferno": "demons",
    "Fortress": "demons",
    "Conflux": "nature",
}
# OE display names (unified race of a hommoe source) map back to their sid.
for _sid, _display in HOMMOE_FACTION_NAMES.items():
    UNIFIED_TO_HOMMOE_FACTION_SID[_display] = _sid

# Olden Era tilesMap biome id -> unified terrain (biome ids from Core.zip
# DB/map/tiles/tiles.json: 1=Grass, 2=Sand, 3=Deathland, 4=Snow, 5=Autumn,
# 6=Lava, 7=Dirt; see /workspace/references/map-editor-json-tool/src/lib/map-grid/terrain-colors.ts).
# Water is not a tilesMap value: a nonzero waterMap id means "Water".
HOMMOE_TILE_TERRAINS = {
    1: "Grass",
    2: "Desert",
    3: "Wasteland",
    4: "Snow",
    5: "Swamp",
    6: "Lava",
    7: "Dirt",
}

# H3 battlefield-terrain object classes -> Olden Era biome (user-provided
# mapping). Olden Era has no battlefield-terrain object layer: a battle
# uses the biome of the tile it is fought on, so these objects convert by
# repainting their tile's tilesMap biome; the object itself has no OE sid
# and is not emitted (it is recorded in HOMMOE_BATTLEFIELD_PAINTED instead
# of HOMMOE_UNMAPPED_OBJECTS). Biome names resolve to tilesMap ids through
# UNIFIED_TO_HOMMOE_TILE. h3 141 (Magical Terrain) is NOT in this table
# and stays dropped.
HOMMOE_BATTLEFIELD_CLASS_TO_BIOME = {
    21: "Wasteland", 223: "Wasteland",   # Cursed Ground
    46: "Grass", 230: "Grass",           # Magic Plains
    224: "Lava",                          # Evil Fog
    225: "Grass",                         # Favorable Winds
    226: "Lava",                          # Fiery Fields
    227: "Grass",                         # Holy Ground
    228: "Grass",                         # Lucid Pools
    229: "Grass",                         # Magic Clouds
    231: "Dirt",                          # Rocklands
}

# Battlefield-terrain objects converted into a tilesMap biome repaint by
# unified_to_hommoe; reset on each call, consumed by oe_loop_check.py.
HOMMOE_BATTLEFIELD_PAINTED = []

# H3 random dwelling classes (216/217/218). OE dwellings have no city link
# and no random flag (all 69 barracks_* templates are fixed faction/tier/
# units, DB/objects_logic/hires/barracks.json), so the converter resolves
# the random choice at conversion time: faction from castle_absod_id (the
# target town's faction) or from the towns alignment bitfield, tier from
# min/max level; the owner (player link) is kept as a propOwners row.
# Evidence: not_converted_yet.english.txt 1d-note2b/2c/2d.
HOMMOE_RANDOM_DWELLING_CLASSES = {216, 217, 218}

# Random dwellings converted by unified_to_hommoe; reset on each call,
# consumed by oe_loop_check.py.
HOMMOE_RANDOM_DWELLINGS = []


def _hommoe_owner_prop_value(owner, color_owner):
    """h3m owner byte (color index 0-7, 255 = none) -> propOwners.owner
    value (0-based player index, the GME convention; -1/absent = neutral),
    through the compact 1-based owner numbering built for block 1 spawns.
    Returns None when the object stays neutral (no propOwners row)."""
    if not isinstance(owner, int) or owner < 0 or owner >= 8:
        return None
    if owner >= len(H3M_PLAYER_COLORS):
        return None
    compact = color_owner.get(H3M_PLAYER_COLORS[owner])
    if compact is None:
        return None
    return compact - 1


def _hommoe_random_dwelling_sid(obj, objects):
    """Resolve an h3 random dwelling (class 216/217/218) to a fixed OE
    barracks_<faction>_<tier> sid, resolving the h3 "random" at conversion
    time: faction from castle_absod_id (target town's faction) or the
    towns alignment bitfield, else fully random; tier from min/max level
    (0-based levels -> tiers 1-7), else random. Recorded in
    HOMMOE_RANDOM_DWELLINGS."""
    from correspondence import H3M_TOWN_TYPE_TO_FH2M_RACE
    rd = (objects.get("randomDwellingMetadata") or {}).get(str(obj.get("id"))) or {}
    faction_sid = None
    resolved_from = None
    absod = rd.get("castleAbsodId")
    if absod:
        town_meta = objects.get("townMetadata") or {}
        target = None
        for _tile_key, obj_list in (objects.get("tiles") or {}).items():
            for t in obj_list:
                if t.get("group") != "KINGDOM_TOWNS":
                    continue
                tm = town_meta.get(str(t.get("id"))) or {}
                # AB/SoD: castle_absod_id references the town's absod
                # objectID; RoE: it references the object index.
                if tm.get("objectID") == absod or t.get("id") == absod:
                    target = (t, tm)
                    break
            if target:
                break
        if target is not None:
            t, tm = target
            town_type = tm.get("type")
            if town_type is None and t.get("class") == 98:
                town_type = t.get("subclass")
            race = H3M_TOWN_TYPE_TO_FH2M_RACE.get(town_type) if town_type is not None else None
            if race:
                faction_sid = UNIFIED_TO_HOMMOE_FACTION_SID.get(race)
                resolved_from = "town:%s" % absod
    if faction_sid is None:
        bf = rd.get("townBitfield")
        bits = [i for i in range(9) if isinstance(bf, int) and (bf & (1 << i))]
        if bits:
            race = H3M_TOWN_TYPE_TO_FH2M_RACE.get(_random.choice(bits))
            if race:
                faction_sid = UNIFIED_TO_HOMMOE_FACTION_SID.get(race)
                resolved_from = "bitfield"
    if faction_sid is None:
        # class 218 (or unresolved link): fully random faction
        faction_sid = _random.choice(list(HOMMOE_FACTION_NAMES))
        resolved_from = "random"
    if rd.get("minLevel") is not None and rd.get("maxLevel") is not None:
        lo = max(0, min(6, int(rd["minLevel"])))
        hi = max(lo, min(6, int(rd["maxLevel"])))
        tier = _random.randint(lo, hi) + 1
    else:
        tier = _random.randint(1, 7)
    sid = "barracks_%s_%d" % (faction_sid, tier)
    HOMMOE_RANDOM_DWELLINGS.append(OrderedDict([
        ("id", obj.get("id")),
        ("class", obj.get("class")),
        ("sid", sid),
        ("factionSid", faction_sid),
        ("tier", tier),
        ("resolvedFrom", resolved_from),
        ("owner", rd.get("owner")),
    ]))
    return sid

# Olden Era win conditions: adventure.settings.mapWinConditions[] entries,
# keyed by typeWinCondition. Enum from the game's own RMG (see
# /workspace/references/map-editor-json-tool/src/lib/rmg/win-conditions.ts
# and map-write.ts's patchWinConditions: a fresh map ships 0,2,1):
#   0 classic, 1 desertion, 2 hero lighting, 3 capital hold (editor
#   "LostStartCity"), 4 guardian's demise ("LostStartHero"), 5 final
#   battle, 8 city hold, 9 tournament. Unknown ids map to "unknown" and
#   keep their raw int in metadata. OE has no structured loss-condition
#   list: loss is "lose everything" unless the script uses GameLose /
#   SideLose actions (block commentAiData).
HOMMOE_WIN_CONDITIONS = {
    0: "defeatEveryone",
    1: "desertion",
    2: "heroLighting",
    3: "captureTown",
    4: "killHero",
    5: "finalBattle",
    8: "captureTown",
    9: "tournament",
}


def _hommoe_script_actions(blocks):
    """Collect the action names ("a" fields) used in the scripting block."""
    actions = set()

    def walk(node):
        if isinstance(node, dict):
            action = node.get("a")
            if isinstance(action, str):
                actions.add(action)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(blocks.get("commentAiData") or {})
    return actions


# Sid fragments identifying adventure-map objects (checked before scenery).
_HOMMOE_ADVENTURE_MISC_TOKENS = (
    "portal", "market", "trading", "shrine", "altar", "magic_amplifier", "magic_wheel",
    "storage", "windmill", "prison", "arena", "dragon", "mana_well", "observatory",
    "learning", "wise_owl", "mystical_tower", "knowledge", "lost_library",
    "circle_of_life", "unit_trade", "random-hire", "monty", "grave", "scroll",
)
# Sid fragments identifying decorative scenery.
_HOMMOE_SCENERY_TOKENS = (
    "tree", "palm", "mushroom", "stones", "stone", "hill", "ground", "grass",
    "flowers", "weed", "fish", "camp_fire", "thorns", "gallows", "pool", "fx_",
    "dead_", "desert_", "dirt_", "cactus", "rock", "mountain", "campaign_fx",
    "cart", "gardener", "spider", "bridge", "reed", "stump", "bones", "chick",
)


# ---------------------------------------------------------------------------
# Olden Era object correspondence, learned from the local reference
# references/map-editor-json-tool (h3-import/h3-object-mapping.json plus
# h3-object-mapping.ts's resolveObjectSid() and H3_TERRAIN_BIOME): h3m
# object class -> OE sid, with subtype / def-name / token dispatch and the
# scenery role -> biome -> sid tables. oe_object_correspondence.json is the
# normalized copy of that data checked in at the repository root.
# ---------------------------------------------------------------------------
import json as _json
import os as _os

with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                        "oe_object_correspondence.json"), encoding="utf-8") as _f:
    OE_OBJECT_CORRESPONDENCE = _json.load(_f)

OE_EMIT_SID = OE_OBJECT_CORRESPONDENCE["emit"]
OE_DISPATCH = OE_OBJECT_CORRESPONDENCE["dispatch"]
OE_SCENERY_ROLE = OE_OBJECT_CORRESPONDENCE["scenery"]
OE_SCENERY_DISPATCH = OE_OBJECT_CORRESPONDENCE["scenery_dispatch"]
OE_SCENERY_DISPATCH_SUBTYPE = OE_OBJECT_CORRESPONDENCE["scenery_dispatch_subtype"]
OE_ROLE_BIOME_SID = OE_OBJECT_CORRESPONDENCE["role_biome_sid"]
OE_DEF_TO_SID = OE_OBJECT_CORRESPONDENCE["def_to_sid"]
OE_SUPPLEMENT_SCENERY = OE_OBJECT_CORRESPONDENCE["supplement_scenery"]
OE_CREATURE_EQUIVALENTS = OE_OBJECT_CORRESPONDENCE["creature_equivalents"]
OE_SUPPLEMENT_EMIT = OE_OBJECT_CORRESPONDENCE["supplement_emit"]
# OE scroll boxes (Core.zip DB/map/objects/6_artifacts.json). User
# decision: h3 93 Spell Scroll -> a RANDOM one of these (a specific spell
# is not expressible - there is no custom scroll sid, the scroll boxes
# grant a random scroll item of their tier); the reverse maps each box
# sid back to h3 93.
OE_SCROLL_BOX_SIDS = ("scroll_box", "enchanted_scroll_box", "mythic_scroll_box")
# h3m artifact id -> OE artifact sid and h3m secondary skill id -> OE
# skill sid, learned from the game's own Core.zip (DB/items/items/*.json +
# DB/heroes_skills/skills/skills.json + Lang/english display names, exact
# name matches); see core_zip_not_converted.english.txt for the rest.
OE_ARTIFACT_EQUIVALENTS = OE_OBJECT_CORRESPONDENCE["artifact_equivalents"]
OE_SKILL_EQUIVALENTS = OE_OBJECT_CORRESPONDENCE["skill_equivalents"]
# OE artifact item sids bucketed by propRandomItems rarity bin
# (Treasure/Common=0, Minor/Rare=1, Major/Epic=2, Relic/Legendary=3),
# extracted from Core.zip DB/items/items/*.json (rarity field).
OE_ARTIFACT_SIDS_BY_RARITY = OE_OBJECT_CORRESPONDENCE.get(
    "oe_artifact_sids_by_rarity") or {}
# h3 artifact class (H3M_ARTIFACT_CLASSES 1-4) -> rarity bin 0-3
_H3_ART_CLASS_TO_RARITY_BIN = {1: "0", 2: "1", 3: "2", 4: "3"}


def _hommoe_artifact_sid(h3_art):
    """h3m artifact id -> OE artifact item sid for a GiveItemHero action:
    exact Core.zip name match when one of the 20 exists, else a random OE
    artifact sid of the same rarity bin (user decision: artifacts random
    is good). Returns None when nothing is known."""
    sid = OE_ARTIFACT_EQUIVALENTS.get(str(h3_art))
    if sid:
        return sid
    from correspondence import H3M_ARTIFACT_CLASSES
    bin_ = _H3_ART_CLASS_TO_RARITY_BIN.get(H3M_ARTIFACT_CLASSES.get(h3_art, 4), "3")
    pool = OE_ARTIFACT_SIDS_BY_RARITY.get(bin_) or []
    if not pool:
        pool = [s for b in OE_ARTIFACT_SIDS_BY_RARITY.values() for s in b]
    return _random.choice(pool) if pool else None
OE_ARTIFACT_SID_TO_H3 = {}
for _aid, _asid in OE_ARTIFACT_EQUIVALENTS.items():
    OE_ARTIFACT_SID_TO_H3.setdefault(_asid, int(_aid))
# OE unit sid -> h3m creature id (reverse of creatureEquivalents).
# OE units have a second upgrade variant (<base>_upg_alt, e.g.
# esquire_upg_alt = Sun's Aegis) that H3 does not have: both _upg and
# _upg_alt map to the same (single) H3 upgraded creature.
OE_UNIT_SID_TO_H3_CREATURE = {}
for _cid, _usid in OE_CREATURE_EQUIVALENTS.items():
    OE_UNIT_SID_TO_H3_CREATURE.setdefault(_usid, int(_cid))
for _usid, _cid in list(OE_UNIT_SID_TO_H3_CREATURE.items()):
    if _usid.endswith("_upg"):
        OE_UNIT_SID_TO_H3_CREATURE.setdefault(_usid + "_alt", _cid)
# OE skill sid -> h3m secondary skill id (reverse of OE_SKILL_EQUIVALENTS),
# used when decoding OE quest actions back into eventMetadata.
OE_SKILL_SID_TO_H3 = {}
for _sid_h3, _sid in OE_SKILL_EQUIVALENTS.items():
    OE_SKILL_SID_TO_H3.setdefault(_sid, int(_sid_h3))
# All OE skill sids (Core.zip DB/heroes_skills/skills/skills.json + Lang
# display names, oe_skill_names). User decision: the OE faction skills
# (skill_faction_*) are EXCLUDED from conversion in both directions - they
# are never emitted H3->OE and decode to None OE->H3 (this also drops the
# former h3 12 Necromancy <-> skill_faction_undead exact match). Every
# OTHER skill conversion is random: an unmapped h3 skill gets a random
# convertible OE sid (_oe_skill_sid), an OE-only non-faction skill gets a
# random h3 skill (_h3_skill_from_oe_sid).
OE_SKILL_NAMES = OE_OBJECT_CORRESPONDENCE.get("oe_skill_names") or {}
OE_SKILL_SIDS = set(OE_SKILL_NAMES)
OE_SKILL_EXCLUDED_PREFIX = "skill_faction_"
OE_SKILL_SIDS_CONVERTIBLE = sorted(
    s for s in OE_SKILL_SIDS if not s.startswith(OE_SKILL_EXCLUDED_PREFIX))


def _h3_skill_from_oe_sid(sid):
    """OE skill sid -> h3m secondary skill id: exact Core.zip name match
    when mapped, else a random h3 skill for OE-only non-faction sids (user
    decision: all other conversions are random). Returns None for the
    excluded skill_faction_* sids and for unknown sids."""
    if sid.startswith(OE_SKILL_EXCLUDED_PREFIX):
        return None
    if sid in OE_SKILL_SID_TO_H3:
        return OE_SKILL_SID_TO_H3[sid]
    if sid in OE_SKILL_SIDS:
        return _random.randrange(len(H3M_SECONDARY_SKILL_NAMES))
    return None


def _oe_skill_sid(h3_skill):
    """h3m secondary skill id -> OE skill sid: exact Core.zip name match
    when mapped, else a random convertible OE skill sid (user decision:
    unmapped skills convert randomly; skill_faction_* are never emitted).
    Returns None only when the convertible pool is empty."""
    sid = OE_SKILL_EQUIVALENTS.get(str(h3_skill))
    if sid and not sid.startswith(OE_SKILL_EXCLUDED_PREFIX):
        return sid
    if OE_SKILL_SIDS_CONVERTIBLE:
        return _random.choice(OE_SKILL_SIDS_CONVERTIBLE)
    return None
# Spell catalog from Core.zip DB/magics + Lang magic.json (see
# oe_object_correspondence.json spell_equivalents / oe_spell_sids):
# 11 exact English-name matches h3 spell id -> OE spell sid; the other OE
# sids carry school/rank/name for the random-same-rank fallback (user
# decision: spell rewards are NOT converted 1:1 - an unmatched spell
# becomes a random OE spell of the same rank, and vice versa).
OE_SPELL_EQUIVALENTS = {int(k): v for k, v in
                        (OE_OBJECT_CORRESPONDENCE.get("spell_equivalents") or {}).items()}
OE_SPELL_SID_TO_H3 = {v: k for k, v in OE_SPELL_EQUIVALENTS.items()}
OE_SPELL_INFO = OE_OBJECT_CORRESPONDENCE.get("oe_spell_sids") or {}
# OE base (non "_special"/masterful) spell sids bucketed by rank 1-5
OE_SPELL_BY_RANK = {}
for _sid, _info in OE_SPELL_INFO.items():
    if _sid.endswith("_special"):
        continue
    _rank = _info.get("rank")
    if isinstance(_rank, int):
        OE_SPELL_BY_RANK.setdefault(_rank, []).append(_sid)
# h3 spell ids bucketed by level (H3M_SPELL_LEVELS, SPTRAITS order)
from correspondence import H3M_SPELL_LEVELS
H3_SPELL_BY_LEVEL = {}
for _i, _lv in enumerate(H3M_SPELL_LEVELS):
    H3_SPELL_BY_LEVEL.setdefault(_lv, []).append(_i)


def _hommoe_spell_sid(h3_spell):
    """h3 spell id -> OE spell sid: exact Core.zip name match when one of
    the 11 exists, else a random OE spell of the same rank (user decision).
    Returns None when no candidate exists."""
    if h3_spell in OE_SPELL_EQUIVALENTS:
        return OE_SPELL_EQUIVALENTS[h3_spell]
    if 0 <= h3_spell < len(H3M_SPELL_LEVELS):
        rank = H3M_SPELL_LEVELS[h3_spell]
    else:
        rank = 1
    cands = OE_SPELL_BY_RANK.get(rank) or []
    if not cands:
        cands = [sid for sid in OE_SPELL_INFO if not sid.endswith("_special")]
    return _random.choice(cands) if cands else None


def _h3_spell_from_oe_sid(sid):
    """OE spell sid -> h3 spell id: exact match when known, else a random
    h3 spell of the same level (mirror of the forward fallback).
    Returns None for unknown sids."""
    if sid in OE_SPELL_SID_TO_H3:
        return OE_SPELL_SID_TO_H3[sid]
    info = OE_SPELL_INFO.get(sid)
    if not info:
        return None
    rank = info.get("rank")
    cands = H3_SPELL_BY_LEVEL.get(rank) if isinstance(rank, int) else None
    if not cands:
        cands = list(range(len(H3M_SPELL_LEVELS)))
    return _random.choice(cands)
# OE catalog hero sid -> standard startMagics spell sids (Core.zip
# DB/heroes/**/*.json, startMagics[].sidConfig; 133 of 177 hero defs).
# User decision: hero starting spells are the standard spells of each
# hero, so the way back to H3/H2 builds the hero spell bitfield from
# these instead of trying to carry a per-map custom spell list.
OE_HERO_START_MAGICS = OE_OBJECT_CORRESPONDENCE.get("oe_hero_start_magics") or {}
# OE altar_of_magic_* <-> H3 shrine classes 88/89/90, converted to each
# other RANDOMLY (user decision; see altar_of_magic_shrines in
# oe_object_correspondence.json for the Core.zip evidence).
_ALTAR_SHRINE = OE_OBJECT_CORRESPONDENCE.get("altar_of_magic_shrines") or {}
HOMMOE_ALTAR_SIDS = list(_ALTAR_SHRINE.get("altar_sids") or [])
HOMMOE_CUSTOM_ALTAR_SIDS = list(_ALTAR_SHRINE.get("custom_altar_sids") or [])
HOMMOE_ALTAR_ALL_SIDS = HOMMOE_ALTAR_SIDS + HOMMOE_CUSTOM_ALTAR_SIDS
HOMMOE_ALTAR_H3_CLASSES = [str(c) for c in (_ALTAR_SHRINE.get("h3_shrine_classes")
                                             or [88, 89, 90])]
# Sids for which the game editor always seeds an (empty) propRewardParams
# row: the altar_of_magic_* sids plus the per-user-mapped ones
# (reward_params_only_sids, e.g. beer_fountain for h3 14 Swan Pond) -
# all in the reference map-write.ts SIDS_WITH_REWARD_PARAMS_ONLY.
HOMMOE_REWARD_PARAMS_SIDS = HOMMOE_ALTAR_SIDS + list(
    OE_OBJECT_CORRESPONDENCE.get("reward_params_only_sids") or [])


def _h3_hero_spells_bitfield(hero_sid):
    """OE catalog hero sid -> SoD 9-byte H3 spells bitfield (hex), built
    from the hero def's standard startMagics (OE_HERO_START_MAGICS), each
    OE spell sid mapped through _h3_spell_from_oe_sid (exact match else a
    random H3 spell of the same level). Returns None when the hero has no
    known starting spell."""
    bits = 0
    for sid in OE_HERO_START_MAGICS.get(hero_sid) or []:
        h3_spell = _h3_spell_from_oe_sid(sid)
        if h3_spell is not None and 0 <= h3_spell < 72:
            bits |= 1 << h3_spell
    if not bits:
        return None
    return bits.to_bytes(9, "little").hex()


OE_H3_TERRAIN_BIOME = OE_OBJECT_CORRESPONDENCE["h3_terrain_biome"]
OE_OMIT_CLASSES = {str(o["h3Id"]) for o in OE_OBJECT_CORRESPONDENCE["omit"]}

# h3m terrain name -> h3m terrain id (h3decoder TERRAIN_MAP), used to pick
# the scenery biome bucket.
H3M_TERRAIN_ID_BY_NAME = {
    "Dirt": 0, "Sand": 1, "Grass": 2, "Snow": 3, "Swamp": 4, "Rough": 5,
    "Subterranean": 6, "Lava": 7, "Water": 8, "Rock": 9,
}

# Reverse index: OE sid -> list of (h3m class, subtype, def name) that
# resolve to it (first entry is the canonical one).
OE_SID_TO_H3 = {}


def _index_hommoe_sid(sid, h3_id, subtype=None, def_name=None):
    OE_SID_TO_H3.setdefault(sid, []).append((int(h3_id), subtype, def_name))


for _h3, _row in OE_EMIT_SID.items():
    _index_hommoe_sid(_row["sid"], _h3)
for _h3, _d in OE_DISPATCH.items():
    for _sub, _sid in (_d.get("subtypes") or {}).items():
        _index_hommoe_sid(_sid, _h3, subtype=int(_sub) if str(_sub).isdigit() else None)
    for _def, _sid in (_d.get("exact") or {}).items():
        _index_hommoe_sid(_sid, _h3, def_name=_def)
    for _tok, _sid in (_d.get("tokens") or {}).items():
        # h3m class 79 (Resource) dispatches on the resource token of the
        # def name; the token is the resource subtype (FH2M_RESOURCE_ORDER).
        _sub = {"wood": 0, "merc": 1, "ore": 2, "sulf": 3,
                "crys": 4, "gems": 5, "gold": 6}.get(_tok)
        _index_hommoe_sid(_sid, _h3, subtype=_sub)
    if _d.get("default"):
        _index_hommoe_sid(_d["default"], _h3)
    _fc = _d.get("freeChoice")
    if _fc:
        for _sub in _fc.get("subtypes", []):
            _index_hommoe_sid(_fc["sid"], _h3, subtype=_sub)
for _h3, _exact in OE_SCENERY_DISPATCH.items():
    for _def, _sid in _exact.items():
        _index_hommoe_sid(_sid, _h3, def_name=_def)

# Creature-bank OE sids (H3 classes 16/24/25/84/85; user-provided mapping in
# oe_object_correspondence.json dispatch subtypes - see
# not_converted_yet.english.txt section 6). The game editor always seeds
# propVariants + propRewardParams rows for these sids (reference
# map-write.ts SIDS_WITH_VARIANTS_AND_REWARD_PARAMS).
# OE sids that get propVariants + propRewardParams rows seeded on fresh
# placement (the game editor's SIDS_WITH_VARIANTS_AND_REWARD_PARAMS):
# the creature-bank classes (16/24/25/84/85), the seer/sphinx sid
# monty_hall (user mapping h3 83 -> monty_hall) and the witch-hut sid
# wise_owl (user mapping h3 113 -> wise_owl).
HOMMOE_BANK_SIDS = set()
for _cls in (16, 24, 25, 84, 85, 83, 113):
    _h = str(_cls)
    if _h in OE_DISPATCH:
        HOMMOE_BANK_SIDS.update((OE_DISPATCH[_h].get("subtypes") or {}).values())
    if _h in OE_EMIT_SID:
        HOMMOE_BANK_SIDS.add(OE_EMIT_SID[_h]["sid"])

OE_H3_NAMES = OE_OBJECT_CORRESPONDENCE["h3_names"]


def _alnum(s):
    import re as _re
    return _re.sub(r"[^a-z0-9]+", "", s.lower())


def _common_substring_len(a, b):
    # longest common substring length between two lowercase alnum strings
    best = 0
    for i in range(len(a)):
        for j in range(len(b)):
            k = 0
            while i + k < len(a) and j + k < len(b) and a[i + k] == b[j + k]:
                k += 1
            if k > best:
                best = k
    return best


for _role, _by_biome in OE_ROLE_BIOME_SID.items():
    for _biome, _sid in _by_biome.items():
        _cands = [int(_h3) for _h3, _r in OE_SCENERY_ROLE.items() if _r == _role]
        _cands += [int(_h3) for _h3, _r in OE_SUPPLEMENT_SCENERY.items() if _r == _role]
        _cands += [int(_h3) for _h3, _subs in OE_SCENERY_DISPATCH_SUBTYPE.items()
                   if _role in _subs.values()]
        if not _cands:
            continue
        # Prefer the candidate class whose name best matches the sid stem
        # (pinetree_* -> 137 "Pine Trees", flowers_* -> 120 "Flowers"...),
        # so the way back recovers the original class when possible.
        _stem = _alnum(_sid)
        _best = max(_cands, key=lambda c: _common_substring_len(
            _stem, _alnum(OE_H3_NAMES.get(str(c), ""))))
        _index_hommoe_sid(_sid, _best)
        for _c in _cands:
            if _c != _best:
                _index_hommoe_sid(_sid, _c)
for _h3, _row in OE_SUPPLEMENT_EMIT.items():
    _index_hommoe_sid(_row["sid"], _h3)
# Reverse of the Spell Scroll mapping (user decision): each OE scroll box
# sid -> h3 93 (inserted first so the boxes do not reverse to the shrine
# classes 88-90 like the reference's emit table had them).
for _sid in OE_SCROLL_BOX_SIDS:
    OE_SID_TO_H3.setdefault(_sid, []).insert(0, (93, 0, None))

# Reverse table for scenery sids: OE sid -> a representative unified
# (group, index) of the landscape family that produces it. Built by running
# the forward resolution over the known fh2m landscape indices and terrain
# variants; first hit wins (groups in order, indices ascending, terrains in
# H3M_TERRAIN_ID_BY_NAME order), so it is deterministic. OE scenery sids are
# coarser than the H2/H3 variants (many defs share one sid), so the way
# back recovers the family, not necessarily the exact original variant.
OE_SID_LANDSCAPE_REVERSE = {}


def _build_oe_sid_landscape_reverse():
    groups = ("LANDSCAPE_TREES", "LANDSCAPE_MOUNTAINS", "LANDSCAPE_ROCKS",
              "LANDSCAPE_MISCELLANEOUS", "LANDSCAPE_WATER", "ADVENTURE_WATER")
    terrains = list(H3M_TERRAIN_ID_BY_NAME)
    candidates = {}
    for group in groups:
        for index in range(256):
            for terrain in terrains:
                try:
                    ref = _unified_obj_h3m_ref({"group": group, "index": index},
                                               terrain)
                except Exception:
                    ref = None
                if ref is None:
                    continue
                sid = _resolve_hommoe_sid(ref[0], ref[2], ref[1], terrain)
                # Only claim the sid for this group when the sid's own
                # token family agrees, so rock sids are not claimed by a
                # tree index that happens to resolve to them.
                if sid and _hommoe_sid_group(sid) == group:
                    candidates.setdefault(sid, []).append((group, index, ref[0]))
    for sid, cands in candidates.items():
        # Prefer the (group, index) whose h3m class is the name-matched
        # best candidate for the sid (first entry of OE_SID_TO_H3), so the
        # way back recovers the original scenery class when possible.
        best_class = (OE_SID_TO_H3.get(sid) or [(None,)])[0][0]
        for group, index, cls in cands:
            if cls == best_class:
                OE_SID_LANDSCAPE_REVERSE[sid] = (group, index)
                break
        else:
            OE_SID_LANDSCAPE_REVERSE[sid] = cands[0][0], cands[0][1]


# Objects dropped by unified_to_hommoe because the reference mapping has no
# Olden Era equivalent for their type; reset on each unified_to_hommoe
# call, consumed by oe_loop_check.py to build the no-equivalent listing.
HOMMOE_UNMAPPED_OBJECTS = []


def _hommoe_biome_for_terrain(terrain_name):
    terrain_id = H3M_TERRAIN_ID_BY_NAME.get(terrain_name or "Grass", 2)
    return OE_H3_TERRAIN_BIOME.get(str(terrain_id), "grass")


def _resolve_hommoe_sid(h3_id, anim, subtype, terrain_name):
    """Port of the reference resolveObjectSid(): h3m object (class,
    animation, subtype) placed on a terrain -> OE sid, or None when the
    reference mapping omits the object (no Olden Era equivalent)."""
    h3 = str(h3_id)
    if h3 == "5":
        # Artifact: use the exact Core.zip name match when there is one,
        # else the stock random-item (lossy, see no_olden_era_equivalent).
        art_sid = OE_ARTIFACT_EQUIVALENTS.get(str(subtype or 0))
        if art_sid:
            return art_sid
    if h3 in HOMMOE_ALTAR_H3_CLASSES:
        # User decision: the H3 shrines 88/89/90 convert to a RANDOM
        # OE altar_of_magic_* (no 1:1 - the OE altars are per-school while
        # the H3 shrines are per-level). The shrine's fixed spell, when
        # the source had one, is dropped: the altar draws a random spell
        # of its own school/rank (see altar_of_magic_shrines note).
        return _random.choice(HOMMOE_ALTAR_SIDS) if HOMMOE_ALTAR_SIDS else None
    if h3 == "93":
        # User decision: Spell Scroll -> a RANDOM OE scroll box (a specific
        # spell is not expressible, no custom scroll sid); the spell id
        # stays in the unified artifactMetadata only.
        return _random.choice(OE_SCROLL_BOX_SIDS)
    if h3 in OE_EMIT_SID:
        return OE_EMIT_SID[h3]["sid"]
    known = (h3 in OE_DISPATCH or h3 in OE_SCENERY_ROLE
             or h3 in OE_SCENERY_DISPATCH or h3 in OE_SCENERY_DISPATCH_SUBTYPE)
    if anim and not known:
        # The class itself is unmapped, but the exact def is in one of the
        # reference's exact tables (e.g. class 155 defs listed under 199).
        exact_sid = OE_DEF_TO_SID.get(anim.lower())
        if exact_sid:
            return exact_sid
    if h3 in OE_SCENERY_ROLE or h3 in OE_SUPPLEMENT_SCENERY:
        role = OE_SCENERY_ROLE.get(h3) or OE_SUPPLEMENT_SCENERY.get(h3)
        return (OE_ROLE_BIOME_SID.get(role) or {}).get(
            _hommoe_biome_for_terrain(terrain_name))
    if h3 in OE_SCENERY_DISPATCH:
        return OE_SCENERY_DISPATCH[h3].get((anim or "").lower())
    if h3 in OE_SCENERY_DISPATCH_SUBTYPE:
        role = (OE_SCENERY_DISPATCH_SUBTYPE[h3] or {}).get(str(subtype or 0))
        if role:
            return (OE_ROLE_BIOME_SID.get(role) or {}).get(
                _hommoe_biome_for_terrain(terrain_name))
        return None
    if h3 in OE_DISPATCH:
        d = OE_DISPATCH[h3]
        fc = d.get("freeChoice")
        if fc and (subtype or 0) in fc.get("subtypes", []):
            return fc["sid"]
        by_sub = (d.get("subtypes") or {}).get(str(subtype or 0))
        if by_sub:
            return by_sub
        if anim:
            anim_l = anim.lower()
            exact = (d.get("exact") or {}).get(anim_l)
            if exact:
                return exact
            for token, sid in (d.get("tokens") or {}).items():
                if token in anim_l:
                    return sid
        if d.get("default"):
            return d["default"]
        return None
    if h3 in OE_SUPPLEMENT_EMIT:
        # Evidence-backed supplement (see oe_object_correspondence.json
        # "supplement_emit" for the per-class local evidence).
        return OE_SUPPLEMENT_EMIT[h3]["sid"]
    return None


def _unified_obj_h3m_ref(obj, terrain_name=None):
    """Resolve a unified object to an h3m reference (class, subtype,
    animation def name). h3m sources carry class/subclass/sprite
    directly; fh2m sources go through the same correspondence tables the
    h3m object encoder uses. Returns None when the object has no h3m
    reference (roads, streams, markers...)."""
    if obj.get("class") is not None:
        return (int(obj["class"]), obj.get("subclass") or 0,
                (obj.get("sprite") or "").lower() or None)
    from correspondence import (
        FH2M_TO_H3M_MONSTERS, FH2M_TO_H3M_ARTIFACTS, FH2M_TO_H3M_RESOURCES,
        FH2M_TO_H3M_MISC, FH2M_TO_H3M_MINES, FH2M_TO_H3M_DWELLINGS,
        FH2M_TO_H3M_SHRINES, FH2M_TO_H3M_COLOR_INDEX, FH2M_TO_H3M_HERO_RACE,
        FH2M_TOWN_RACE_ORDER, H3M_TOWN_TYPE_TO_FH2M_RACE,
        H3M_CREATURE_DEF_NAMES, H3M_DWELLING_DEFS, FH2M_LANDSCAPE_TO_H3M,
        H3M_DEF_OBJECT_CLASS,
        fh2m_tree_h3m_class, fh2m_tree_def_name, fh2m_mountain_h3m_class,
        fh2m_mountain_def_name, fh2m_mine_def_name, fh2m_landscape_def)
    group = obj.get("group")
    index = obj.get("index", 0) or 0
    terrain = terrain_name or "Grass"

    def _target(target):
        if target is None:
            return None
        anim = target[2].lower() if len(target) > 2 and target[2] else None
        cls = target[0]
        if anim:
            # Prefer the class of the actual def: the correspondence
            # tables sometimes route through a generic class (155 Trees,
            # 29 Flotsam) that the OE mapping omits, while the def's own
            # class (119/137/134...) is mapped.
            cls = H3M_DEF_OBJECT_CLASS.get(anim, cls)
        return (cls, target[1], anim)

    if group == "MONSTERS":
        creature = index + 1
        if 67 <= creature <= 71:
            return (71 + (creature - 67), 0, None)
        h3 = FH2M_TO_H3M_MONSTERS.get(creature)
        if h3 is None:
            return None
        return (54, h3, (H3M_CREATURE_DEF_NAMES.get(h3) or "").lower() or None)
    if group == "ADVENTURE_TREASURES":
        if index in FH2M_TO_H3M_RESOURCES:
            # h3m class 79 dispatches on the resource token of the def
            # name (avtwood0.def, avtgold0.def, ...).
            token = ("wood", "merc", "ore", "sulf", "crys", "gems", "gold")[index]
            return (79, index, token)
        return _target(FH2M_TO_H3M_MISC.get("TREASURE_%d" % index))
    if group == "ADVENTURE_ARTIFACTS":
        if index in (91, 92, 93, 94, 95):
            return (65 + {91: 0, 92: 1, 93: 2, 94: 3, 95: 4}[index], 0, None)
        if index <= 72:
            artifact = index + 9
        elif index == 73:
            artifact = 82
        else:
            artifact = index + 13
        h3 = FH2M_TO_H3M_ARTIFACTS.get(artifact)
        return (5, h3, None) if h3 is not None else None
    if group == "ADVENTURE_MINES":
        mine = FH2M_TO_H3M_MINES.get(index)
        if mine is None:
            return None
        return (mine[0], mine[1], fh2m_mine_def_name(index).lower())
    if group == "ADVENTURE_DWELLINGS":
        dw = FH2M_TO_H3M_DWELLINGS.get(index)
        if dw is None:
            return None
        anim = dw[2].lower() if len(dw) > 2 and dw[2] else None
        if anim is None and dw[1] in H3M_DWELLING_DEFS:
            anim = H3M_DWELLING_DEFS[dw[1]][0].lower()
        return (dw[0], dw[1], anim)
    if group == "KINGDOM_TOWNS":
        if index in (12, 13):
            return (77, 0, "avcranx0.def")
        race_id = index // 2
        if 0 <= race_id < len(FH2M_TOWN_RACE_ORDER):
            for tt, race in H3M_TOWN_TYPE_TO_FH2M_RACE.items():
                if race == FH2M_TOWN_RACE_ORDER[race_id]:
                    return (98, tt, None)
        return (98, 0, None)
    if group == "KINGDOM_HEROES":
        race = index % 7
        hero_type = FH2M_TO_H3M_HERO_RACE.get(race) or 0
        return (34, (hero_type or 0) // 8, None)
    if group == "ADVENTURE_POWER_UPS":
        shrine = FH2M_TO_H3M_SHRINES.get(index)
        if shrine is not None:
            return (shrine, 0, None)
        return _target(FH2M_TO_H3M_MISC.get("POWER_%d" % index))
    if group in ("ADVENTURE_MISCELLANEOUS", "ADVENTURE_WATER"):
        if group == "ADVENTURE_MISCELLANEOUS" and 51 <= index <= 58:
            return (9, FH2M_TO_H3M_COLOR_INDEX[index - 51], None)
        if group == "ADVENTURE_MISCELLANEOUS" and 59 <= index <= 66:
            return (10, FH2M_TO_H3M_COLOR_INDEX[index - 59], None)
        key = ("MISC_%d" % index) if group == "ADVENTURE_MISCELLANEOUS" else ("WATER_%d" % index)
        return _target(FH2M_TO_H3M_MISC.get(key))
    if group == "LANDSCAPE_TREES":
        cls = fh2m_tree_h3m_class(index, terrain)
        if cls is None:
            return None
        anim = fh2m_tree_def_name(cls, terrain, index).lower()
        return (H3M_DEF_OBJECT_CLASS.get(anim, cls), 0, anim)
    if group == "LANDSCAPE_MOUNTAINS":
        cls = fh2m_mountain_h3m_class(index, terrain)
        if cls is None:
            return None
        anim = fh2m_mountain_def_name(index, cls, terrain).lower()
        return (H3M_DEF_OBJECT_CLASS.get(anim, cls), 0, anim)
    if group in ("LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS", "LANDSCAPE_WATER"):
        entry = fh2m_landscape_def(group, index, terrain)
        if entry is not None:
            cls, anim = entry[0], entry[1].lower()
            cls = H3M_DEF_OBJECT_CLASS.get(anim, cls)
        else:
            # No footprint-matched def, but the class table still knows
            # the h3m class of this fh2m index (cactus, crater, ...).
            cls = FH2M_LANDSCAPE_TO_H3M.get((group, index))
            anim = None
        if cls is None:
            return None
        return (cls, 0, anim)
    return None


def _hommoe_sid_to_group_index(sid):
    """Reverse of the h3m -> OE sid correspondence: OE sid -> unified
    (group, index). The index is None when it cannot be recovered (the
    caller then falls back to a per-group counter); the group is None
    when the sid is not in the correspondence table."""
    from h3decoder import H3M_CLASS_TO_GROUP
    from correspondence import (
        H3M_TO_FH2M_MONSTERS, H3M_TO_FH2M_ARTIFACTS, H3M_TO_FH2M_DWELLINGS,
        FH2M_TO_H3M_MINES, H3M_TREE_DEF_TO_FH2M_INDEX,
        H3M_MOUNTAIN_DEF_TO_FH2M_INDEX, H3M_TOWN_TYPE_TO_FH2M_RACE,
        FH2M_TOWN_RACE_ORDER, H3M_RANDOM_MONSTER_CLASSES)
    if sid in OE_ARTIFACT_SID_TO_H3:
        # Exact Core.zip artifact: recover the h3m artifact id, then the
        # fh2m ADVENTURE_ARTIFACTS index (same rules as the class-5 branch).
        h3_art = OE_ARTIFACT_SID_TO_H3[sid]
        fh2m_art = H3M_TO_FH2M_ARTIFACTS.get(h3_art)
        if fh2m_art is not None:
            if 9 <= fh2m_art <= 81:
                return "ADVENTURE_ARTIFACTS", fh2m_art - 9
            if fh2m_art == 82:
                return "ADVENTURE_ARTIFACTS", 73
            return "ADVENTURE_ARTIFACTS", fh2m_art - 13
        return "ADVENTURE_ARTIFACTS", None
    if sid in HOMMOE_ALTAR_ALL_SIDS:
        # OE altar_of_magic_* / custom_altar_of_magic_* -> a RANDOM H3
        # shrine class 88/89/90 (user decision): expressed as a random
        # fh2m shrine-circle index; the caller maps it to the h3m class
        # through FH2M_TO_H3M_SHRINES.
        return "ADVENTURE_POWER_UPS", _random.choice((14, 15, 16))
    candidates = OE_SID_TO_H3.get(sid)
    if not candidates:
        return None, None
    h3_id, subtype, def_name = candidates[0]
    group = H3M_CLASS_TO_GROUP.get(h3_id) or "UNDEFINED_%d" % h3_id
    if group.startswith("UNDEFINED_"):
        # Classes outside H3M_CLASS_TO_GROUP (chest 101, ...) still have
        # an fh2m object through the misc table: invert it.
        from correspondence import FH2M_TO_H3M_MISC
        misc_reverse = {(v[0], v[1]): k for k, v in FH2M_TO_H3M_MISC.items()}
        key = misc_reverse.get((h3_id, subtype or 0))
        if key is None:
            key = misc_reverse.get((h3_id, None))
        if key is not None:
            prefix, _, num = key.partition("_")
            group = {"TREASURE": "ADVENTURE_TREASURES", "WATER": "ADVENTURE_WATER",
                     "MISC": "ADVENTURE_MISCELLANEOUS", "POWER": "ADVENTURE_POWER_UPS"}.get(prefix)
            if group and num.isdigit():
                return group, int(num)
    index = None
    if group == "MONSTERS":
        if h3_id in H3M_RANDOM_MONSTER_CLASSES:
            index = H3M_RANDOM_MONSTER_CLASSES[h3_id] - 1
        elif subtype is not None:
            fh2m_monster = H3M_TO_FH2M_MONSTERS.get(subtype)
            if fh2m_monster:
                index = fh2m_monster - 1
    elif group == "ADVENTURE_TREASURES":
        if h3_id == 76:
            index = 8  # fh2m random resource
        else:
            index = subtype
    elif group == "ADVENTURE_ARTIFACTS":
        if 65 <= h3_id <= 69:
            index = {65: 91, 66: 92, 67: 93, 68: 94, 69: 95}[h3_id]
        elif subtype is not None:
            fh2m_art = H3M_TO_FH2M_ARTIFACTS.get(subtype)
            if fh2m_art is not None:
                if 9 <= fh2m_art <= 81:
                    index = fh2m_art - 9
                elif fh2m_art == 82:
                    index = 73
                else:
                    index = fh2m_art - 13
    elif group == "ADVENTURE_MINES" and subtype is not None:
        for fh2m_index, target in FH2M_TO_H3M_MINES.items():
            if target[0] == h3_id and target[1] == subtype:
                index = fh2m_index
                break
    elif group == "ADVENTURE_DWELLINGS" and subtype is not None:
        index = H3M_TO_FH2M_DWELLINGS.get(subtype)
    elif group == "ADVENTURE_DWELLINGS" and def_name:
        # barracks_* sid: the dispatch exact tables key h3m defs to barracks
        # sids; the same def is the class-17 catalog entry in
        # H3M_DWELLING_DEFS, so the def recovers the dwelling subtype (and
        # with it the faction) instead of a per-group counter.
        from correspondence import H3M_DWELLING_DEFS
        def_to_sub = {v[0].lower(): k for k, v in H3M_DWELLING_DEFS.items()}
        sub = def_to_sub.get((def_name or "").lower())
        if sub is not None:
            index = H3M_TO_FH2M_DWELLINGS.get(sub)
    elif group == "ADVENTURE_MISCELLANEOUS":
        # Misc interactables (witch hut 113 -> MISC_26, ...): invert the
        # fh2m misc table so a hommoe-sourced object lands back on its
        # original fh2m index.
        from correspondence import FH2M_TO_H3M_MISC
        misc_reverse = {(v[0], v[1]): k for k, v in FH2M_TO_H3M_MISC.items()}
        key = misc_reverse.get((h3_id, subtype or 0)) or misc_reverse.get((h3_id, None))
        if key is not None and key.startswith("MISC_") and key[5:].isdigit():
            index = int(key[5:])
    elif group == "LANDSCAPE_TREES" and def_name:
        index = H3M_TREE_DEF_TO_FH2M_INDEX.get(def_name)
    elif group == "LANDSCAPE_MOUNTAINS" and def_name:
        index = H3M_MOUNTAIN_DEF_TO_FH2M_INDEX.get(def_name)
    elif group == "KINGDOM_TOWNS" and subtype is not None:
        race = H3M_TOWN_TYPE_TO_FH2M_RACE.get(subtype)
        if race in FH2M_TOWN_RACE_ORDER:
            index = FH2M_TOWN_RACE_ORDER.index(race) * 2
    if index is None:
        alt = OE_SID_LANDSCAPE_REVERSE.get(sid)
        if alt is not None:
            return alt
    return group, index


def _hommoe_sid_group(sid):
    """Map an Olden Era object sid to a unified (fh2m-style) object group."""
    s = sid.lower()
    if s in ("city-spawner", "random-city", "random-town") or s.startswith("town"):
        return "KINGDOM_TOWNS"
    if s in ("hero-spawner", "random-hero"):
        return "KINGDOM_HEROES"
    if s.startswith("mine"):
        return "ADVENTURE_MINES"
    if s.startswith("dwelling") or s.startswith("barracks"):
        return "ADVENTURE_DWELLINGS"
    if s.startswith(("chest", "resource", "random-item", "pandora", "random-res")) or s.endswith("_artifact"):
        return "ADVENTURE_TREASURES"
    if s == "random-squad" or s.startswith("squad"):
        return "MONSTERS"
    if any(token in s for token in _HOMMOE_ADVENTURE_MISC_TOKENS):
        return "ADVENTURE_MISCELLANEOUS"
    if any(token in s for token in _HOMMOE_SCENERY_TOKENS):
        if "tree" in s or "palm" in s:
            return "LANDSCAPE_TREES"
        if "mountain" in s:
            return "LANDSCAPE_MOUNTAINS"
        return "LANDSCAPE_MISCELLANEOUS"
    return "UNMAPPED"


_build_oe_sid_landscape_reverse()


def _hommoe_main_town(spawn, adventure, width):
    """Resolve a spawn entry's main town (spawnPointType 0 = city spawner).

    The link goes spawn.owner -> objectsProperties.propSpawns (owner) ->
    object id -> the city-spawner group's node for that id.
    """
    props = adventure.get("objectsProperties") or {}
    owner = spawn.get("owner")
    spawn_id = None
    for row in props.get("propSpawns") or []:
        if isinstance(row, dict) and row.get("owner") == owner:
            spawn_id = row.get("id")
            break
    if spawn_id is None:
        return None
    node = None
    for group in adventure.get("objects", []):
        ids = group.get("ids") or []
        if spawn_id in ids:
            j = ids.index(spawn_id)
            nodes = group.get("nodes") or []
            if j < len(nodes):
                node = nodes[j]
            break
    if node is None:
        return None
    generate_hero = True
    for row in props.get("propCities") or []:
        if isinstance(row, dict) and row.get("id") == spawn_id:
            generate_hero = bool(row.get("spawnHero", True))
            break
    return OrderedDict([
        ("generateHero", generate_hero),
        ("x", int(node) % width if width else 0),
        ("y", int(node) // width if width else 0),
        ("z", 0),
    ])


def _to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _oe_unit_sid_for_h3(creature):
    """OE unit sid for an h3m creature id; OE has two upgrades per unit
    (<base>_upg and <base>_upg_alt) while H3 has one, so pick one at
    random (same rule as the monster writer branch)."""
    sid = OE_CREATURE_EQUIVALENTS.get(str(creature))
    if sid and sid.endswith("_upg") \
            and (sid + "_alt") in OE_UNIT_SID_TO_H3_CREATURE:
        sid = _random.choice((sid, sid + "_alt"))
    return sid


def _hommoe_scholar_to_pandora_meta(sch):
    """h3m scholarMetadata -> a pandoraMetadata-shaped dict so the h3
    Scholar (class 81, user mapping -> OE pandora_box) keeps its reward
    under the normal pandora conversion rules. rewardType: 0 = primary
    skill (rewardValue = skill index 0-3, h3m2json.php
    Reward_ScholarPrimarySkill), 1 = secondary skill (SSTRAITS index),
    2 = spell id, 0xFF = random."""
    resources = OrderedDict((n, 0) for n in
                            ("wood", "mercury", "ore", "sulfur",
                             "crystal", "gems", "gold"))
    primaries = OrderedDict((n, 0) for n in
                            ("attack", "defense", "spellPower", "knowledge"))
    pm = OrderedDict([
        ("guard", None),
        ("experience", 0), ("mana", 0), ("morale", 0), ("luck", 0),
        ("resources", resources),
        ("primarySkills", primaries),
        ("artifacts", []), ("secondarySkills", []), ("spells", []),
        ("creatures", []),
    ])
    rt = sch.get("rewardType")
    rv = sch.get("rewardValue")
    if rt == 0 and isinstance(rv, int) and 0 <= rv <= 3:
        primaries[("attack", "defense", "spellPower", "knowledge")[rv]] = 1
    elif rt == 1 and isinstance(rv, int) and rv != 0xFF:
        pm["secondarySkills"] = [OrderedDict([("id", rv), ("level", 1)])]
    elif rt == 2 and isinstance(rv, int) and rv != 0xFF:
        pm["spells"] = [rv]
    # 0xFF random: everything stays zero/empty (empty parameters row).
    return pm


def _hommoe_pandora_props(prop_rows, oid, pm):
    """Emit the objectsProperties rows for an OE pandora_box placement
    from an h3m pandoraMetadata entry (mirror of _hommoe_pandora_to_metadata).

    Evidence: propVariants.selectedVar -1 = random logic variant (shape of
    the real rows in Broken_Alliance); propSquads.unitProps is the guard
    stack (real row in all_cats_go_to_heaven); propRewardParams.parameters
    slots are "-", "resource:amount" or a bare item/skill sid (reference
    map-editor-json-tool reward-params.ts, confirmed on real maps);
    propActionsAfter carries script actions (all_cats, c_M1) - used here
    for everything a slot cannot express (message, experience, mana,
    stats, creatures), with the action parameter shapes from the
    reference actions.ts. Spells and artifact/skill ids without an OE sid
    cannot be represented yet (no H3<->OE spell table; only 20/143
    artifacts and 16/28 skills have one) and stay in the unified
    pandoraMetadata only.
    """
    prop_rows.setdefault("propVariants", []).append(OrderedDict([
        ("type", 0), ("id", oid), ("selectedVar", -1),
        ("typeVariant", 0), ("fraction", 0), ("unitVersion", 0),
    ]))
    guard = pm.get("guard") or {}
    unit_props = []
    for slot in (guard.get("creatures") or []):
        creature = slot.get("creature")
        count = slot.get("count") or 0
        if creature is None or count <= 0:
            continue
        unit_sid = _oe_unit_sid_for_h3(creature)
        if unit_sid:
            unit_props.append(OrderedDict([
                ("sid", unit_sid), ("count", int(count)),
            ]))
    if unit_props:
        prop_rows.setdefault("propSquads", []).append(OrderedDict([
            ("type", 0), ("id", oid), ("isMainGuard", False),
            ("isStartBattleImmediately", False), ("reactionType", 2),
            ("weeklyIncrementBonus", 0.0), ("unitProps", unit_props),
        ]))
    params = []
    resources = pm.get("resources") or {}
    for name in ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"):
        amount = resources.get(name) or 0
        if amount:
            params.append("%s:%d" % (UNIFIED_TO_HOMMOE_RESOURCE[name], amount))
    for art in (pm.get("artifacts") or []):
        art_sid = OE_ARTIFACT_EQUIVALENTS.get(str(art))
        if art_sid:
            params.append(art_sid)
    for sk in (pm.get("secondarySkills") or []):
        # exact name match, else a random convertible OE skill sid (user
        # decision: unmapped skills convert randomly, skill_faction_* never)
        sk_sid = _oe_skill_sid(sk.get("id"))
        if sk_sid:
            params.append(sk_sid)
    for sp in (pm.get("spells") or []):
        # Spell reward (pandora box HeroMagicMassAdditionReward / scholar
        # type 2): bare OE spell sid in parameters; exact for the 11 name
        # matches, else random same rank (user decision).
        sp_sid = _hommoe_spell_sid(sp) if isinstance(sp, int) else None
        if sp_sid:
            params.append(sp_sid)
    if params:
        prop_rows.setdefault("propRewardParams", []).append(OrderedDict([
            ("type", 0), ("id", oid), ("parameters", params),
        ]))
    actions = []
    message = guard.get("message") or ""
    if message:
        actions.append(OrderedDict([
            ("comment", ""), ("p", [message]), ("a", "Print"),
        ]))
    exp = pm.get("experience") or 0
    if exp:
        actions.append(OrderedDict([
            ("comment", ""), ("p", [str(exp), ""]), ("a", "GiveExpHero"),
        ]))
    mana = pm.get("mana") or 0
    if mana:
        actions.append(OrderedDict([
            ("comment", ""), ("p", ["", str(mana)]), ("a", "GiveManaHero"),
        ]))
    primaries = pm.get("primarySkills") or {}
    stat_map = {"attack": "offence", "defense": "defence",
                "spellPower": "spellPower", "knowledge": "intelligence"}
    for h3_name, oe_stat in stat_map.items():
        amount = primaries.get(h3_name) or 0
        if amount:
            actions.append(OrderedDict([
                ("comment", ""), ("p", [oe_stat, "", str(amount)]),
                ("a", "GiveStatsHero"),
            ]))
    if pm.get("morale"):
        actions.append(OrderedDict([
            ("comment", ""), ("p", ["moral", "", str(pm["morale"])]),
            ("a", "GiveStatsHero"),
        ]))
    if pm.get("luck"):
        actions.append(OrderedDict([
            ("comment", ""), ("p", ["luck", "", str(pm["luck"])]),
            ("a", "GiveStatsHero"),
        ]))
    for cr in (pm.get("creatures") or []):
        creature = cr.get("creature")
        count = cr.get("count") or 0
        if creature is None or count <= 0:
            continue
        unit_sid = _oe_unit_sid_for_h3(creature)
        if unit_sid:
            actions.append(OrderedDict([
                ("comment", ""), ("p", [unit_sid, str(count), ""]),
                ("a", "GiveUnitHero"),
            ]))
    if actions:
        prop_rows.setdefault("propActionsAfter", []).append(OrderedDict([
            ("type", 0), ("id", oid), ("repeat", False), ("sides", ""),
            ("actions", actions),
        ]))


def _hommoe_pandora_to_metadata(props):
    """Build an h3m-style pandoraMetadata entry from an OE pandora_box's
    objectsProperties rows (mirror of _hommoe_pandora_props)."""
    import re
    meta = OrderedDict()
    guard = None
    squad_row = props.get("propSquads")
    if squad_row:
        slots = []
        for u in (squad_row.get("unitProps") or [])[:7]:
            slots.append(OrderedDict([
                ("creature", OE_UNIT_SID_TO_H3_CREATURE.get(u.get("sid"))),
                ("count", _to_int(u.get("count"))),
            ]))
        while len(slots) < 7:
            slots.append(OrderedDict([("creature", None), ("count", 0)]))
        guard = OrderedDict([("message", ""), ("creatures", slots)])
    meta["guard"] = guard
    meta["experience"] = 0
    meta["mana"] = 0
    meta["morale"] = 0
    meta["luck"] = 0
    resources = OrderedDict((n, 0) for n in
                            ("wood", "mercury", "ore", "sulfur",
                             "crystal", "gems", "gold"))
    primaries = OrderedDict((n, 0) for n in
                            ("attack", "defense", "spellPower", "knowledge"))
    artifacts = []
    skills = []
    creatures = []
    source_spell_sids = []
    rp = props.get("propRewardParams")
    if rp:
        oe_to_h3_res = {v: k for k, v in UNIFIED_TO_HOMMOE_RESOURCE.items()}
        for slot in (rp.get("parameters") or []):
            if not slot or slot == "-":
                continue
            m = re.match(r"^([A-Za-z]+):(\d+)$", slot)
            if m:
                h3_name = oe_to_h3_res.get(m.group(1))
                if h3_name:
                    resources[h3_name] = int(m.group(2))
                continue
            if slot in OE_ARTIFACT_SID_TO_H3:
                artifacts.append(OE_ARTIFACT_SID_TO_H3[slot])
            elif slot in OE_SKILL_SIDS:
                # exact name match, else a random h3 skill (user decision:
                # OE-only skills have no H3 counterpart and are randomized)
                h3_skill = _h3_skill_from_oe_sid(slot)
                if h3_skill is not None:
                    skills.append(OrderedDict([
                        ("id", h3_skill), ("level", 1),
                    ]))
            else:
                # OE spell sid (day_3_magic_haste...): no H3<->OE spell
                # id table yet, keep the raw sid.
                source_spell_sids.append(slot)
    stat_to_h3 = {"offence": ("primaries", "attack"),
                  "defence": ("primaries", "defense"),
                  "spellPower": ("primaries", "spellPower"),
                  "intelligence": ("primaries", "knowledge"),
                  "moral": ("morale", None), "luck": ("luck", None)}
    for table in ("propActionsBefore", "propActionsAfter"):
        row = props.get(table)
        for act in ((row or {}).get("actions") or []):
            name = act.get("a")
            p = act.get("p") or []
            if name == "Print" and p and guard is not None:
                guard["message"] = p[0]
            elif name == "GiveExpHero" and p:
                meta["experience"] = _to_int(p[0])
            elif name in ("GiveManaHero", "ChangeManaHero") and len(p) >= 2:
                meta["mana"] = _to_int(p[1])
            elif name == "GiveStatsHero" and len(p) >= 3:
                key = stat_to_h3.get(p[0])
                if key:
                    bucket, field = key
                    if field:
                        primaries[field] = _to_int(p[2])
                    else:
                        meta[bucket] = _to_int(p[2])
            elif name == "GiveUnitHero" and len(p) >= 2:
                creatures.append(OrderedDict([
                    ("creature", OE_UNIT_SID_TO_H3_CREATURE.get(p[0])),
                    ("count", _to_int(p[1])),
                ]))
            elif name in ("AddSkillHero", "AddSkillAll") and p \
                    and str(p[0]) in OE_SKILL_SIDS:
                h3_skill = _h3_skill_from_oe_sid(str(p[0]))
                if h3_skill is not None:
                    skills.append(OrderedDict([
                        ("id", h3_skill), ("level", 1),
                    ]))
            elif name == "GiveItemHero" and p and p[0] in OE_ARTIFACT_SID_TO_H3:
                artifacts.append(OE_ARTIFACT_SID_TO_H3[p[0]])
    meta["resources"] = resources
    meta["primarySkills"] = primaries
    meta["secondarySkills"] = skills
    meta["artifacts"] = artifacts
    meta["spells"] = []
    meta["creatures"] = creatures
    if source_spell_sids:
        meta["sourceSpellSids"] = source_spell_sids
    variants = props.get("propVariants")
    if variants and variants.get("selectedVar") is not None:
        meta["sourceSelectedVar"] = variants.get("selectedVar")
    return meta


def _hommoe_objects_to_unified(adventure, width):
    """
    Convert the adventure block's object groups into the unified objects
    section: objects stored per tile ("x_y_z" -> list), each carrying its
    raw sid, node, rotation, level and its objectsProperties rows.
    """
    props = adventure.get("objectsProperties") or {}
    prop_rows_by_id = {}
    for table, rows in props.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("id"), int):
                prop_rows_by_id.setdefault(row["id"], {})[table] = row

    tiles = OrderedDict()
    group_counters = {}
    artifact_metadata = {}

    def add_object(oid, group_name, sid, node, rotation, level, index=None):
        x = int(node) % width if width else 0
        y = int(node) // width if width else 0
        if index is None:
            index = group_counters.get(group_name, 0)
            group_counters[group_name] = index + 1
        entry = OrderedDict([
            ("id", oid),
            ("group", group_name),
            ("index", index),
            ("sourceSid", sid),
            ("sourceNode", node),
        ])
        if rotation is not None:
            entry["rotation"] = rotation
        if level is not None:
            entry["level"] = level
        rows = prop_rows_by_id.get(oid)
        if rows:
            entry["properties"] = rows
        tiles.setdefault("{}_{}_0".format(x, y), []).append(entry)

    for group in adventure.get("objects", []):
        sid = group.get("sid")
        sid_str = sid if isinstance(sid, str) else (",".join(sid) if isinstance(sid, list) else str(sid))
        group_name = _hommoe_sid_group(sid_str)
        # The h3m-class correspondence gives a more precise group and the
        # real subtype index when the sid is in the table (mines,
        # resources, monsters, ...); scenery sids stay with the
        # token-based group and a per-group counter.
        ref_group, ref_index = _hommoe_sid_to_group_index(sid_str)
        if ref_group and not ref_group.startswith("UNDEFINED_"):
            group_name = ref_group
        ids = group.get("ids") or []
        nodes = group.get("nodes") or []
        rotations = group.get("rotations") or []
        levels = group.get("levels") or []
        for j, oid in enumerate(ids):
            if j >= len(nodes) or nodes[j] is None:
                continue
            add_object(oid, group_name, sid_str, nodes[j],
                       rotations[j] if j < len(rotations) else None,
                       levels[j] if j < len(levels) else None,
                       ref_index)
            if sid_str in OE_ARTIFACT_SID_TO_H3:
                # Exact Core.zip artifact: keep the h3m artifact id so the
                # h3m/fh2m writers can place the same artifact back.
                artifact_metadata[str(oid)] = OrderedDict([
                    ("artifact", OE_ARTIFACT_SID_TO_H3[sid_str]),
                    ("radius", 0), ("captureCondition", 0), ("selected", []),
                ])

    # Fixed squads live in a separate id namespace but are monster
    # placements, so they join the MONSTERS group.
    for squad in adventure.get("squads", []):
        sid = squad.get("sid") or ""
        ids = squad.get("ids") or []
        nodes = squad.get("nodes") or []
        for j, oid in enumerate(ids):
            if j < len(nodes) and nodes[j] is not None:
                add_object(oid, "MONSTERS", sid, nodes[j], None, None)

    # Editor zone markers become MAP_EXTRAS entries.
    for marker in adventure.get("markers", []):
        node = marker.get("node")
        if node is not None:
            add_object(marker.get("id"), "MAP_EXTRAS", marker.get("sid") or "", node, None, None)

    # Squad properties recover the monster type: propSquads rows carry the
    # units (OE unit sid -> h3m creature id -> fh2m monster index),
    # propRandomSquads rows carry a tier (h3m random monster class 71-75,
    # fh2m monsters 67-71).
    from correspondence import H3M_TO_FH2M_MONSTERS, H3M_RANDOM_MONSTER_CLASSES
    monster_metadata = OrderedDict()
    witchhut_metadata = OrderedDict()
    shrine_metadata = OrderedDict()
    hero_metadata = OrderedDict()
    for tile_key, obj_list in tiles.items():
        for entry in obj_list:
            if entry.get("group") != "MONSTERS":
                continue
            props = entry.get("properties") or {}
            oid = entry.get("id")
            squad_row = props.get("propSquads")
            random_row = props.get("propRandomSquads")
            if squad_row:
                units = squad_row.get("unitProps") or []
                count = sum(int(u.get("count", 0)) for u in units)
                h3_creature = None
                if units:
                    h3_creature = OE_UNIT_SID_TO_H3_CREATURE.get(units[0].get("sid"))
                if h3_creature is not None:
                    fh2m_monster = H3M_TO_FH2M_MONSTERS.get(h3_creature)
                    if fh2m_monster:
                        entry["index"] = fh2m_monster - 1
                monster_metadata[str(oid)] = OrderedDict([
                    ("count", count),
                    ("joinCondition", 0),
                    ("isWeeklyGrowthDisabled", False),
                    ("selected", []),
                ])
                if h3_creature is not None:
                    monster_metadata[str(oid)]["creature"] = h3_creature
            elif random_row:
                tier = int(random_row.get("tier", 0) or 0)
                monster_class = 70 + tier
                fh2m_monster = H3M_RANDOM_MONSTER_CLASSES.get(monster_class)
                if fh2m_monster:
                    entry["index"] = fh2m_monster - 1
                monster_metadata[str(oid)] = OrderedDict([
                    ("count", 0),
                    ("joinCondition", 0),
                    ("isWeeklyGrowthDisabled", False),
                    ("selected", []),
                    ("monsterClass", monster_class),
                ])
    # Random-item objects: recover the H3 random-artifact class from the
    # propRandomItems rarity bin (Treasure/Common=0 .. Relic/Legendary=3).
    for obj_list in tiles.values():
        for entry in obj_list:
            if entry.get("sourceSid") != "random-item":
                continue
            row = (entry.get("properties") or {}).get("propRandomItems")
            if not row:
                continue
            cls = HOMMOE_RARITY_TO_RANDOM_ARTIFACT_CLASS.get(int(row.get("rarity", 0) or 0))
            if cls is not None:
                entry["class"] = cls
                entry["index"] = {66: 92, 67: 93, 68: 94, 69: 95}[cls]
    # Pandora's Box objects (sid pandora_box): recover the h3m class 6 and
    # a pandoraMetadata entry from the objectsProperties rows, so the box
    # content survives the trip to h3m/fh2m as well.
    pandora_metadata = OrderedDict()
    for obj_list in tiles.values():
        for entry in obj_list:
            sid = entry.get("sourceSid")
            if sid == "pandora_box":
                entry["class"] = 6
                entry["subclass"] = 0
                pandora_metadata[str(entry.get("id"))] = _hommoe_pandora_to_metadata(
                    entry.get("properties") or {})
            elif sid in HOMMOE_ALTAR_ALL_SIDS:
                # Altar of Magic <-> H3 shrine: the shrine class is the
                # random one picked by _hommoe_sid_to_group_index (the
                # entry index 14-16 maps through FH2M_TO_H3M_SHRINES);
                # the shrine spell is random (0xFF) - the altar's own
                # school/rank (or custom spell list) has no shrine slot.
                from correspondence import FH2M_TO_H3M_SHRINES
                shrine_cls = FH2M_TO_H3M_SHRINES.get(entry.get("index")) \
                    or _random.choice((88, 89, 90))
                entry["class"] = shrine_cls
                entry["subclass"] = 0
                shrine_metadata[str(entry.get("id"))] = OrderedDict([
                    ("spell", None), ("shrineClass", shrine_cls),
                ])
            elif sid in HOMMOE_BANK_SIDS:
                # Bank / variant sid: recover the h3m class/subtype from the
                # correspondence (first indexed candidate).
                cands = OE_SID_TO_H3.get(sid) or []
                if cands:
                    entry["class"] = cands[0][0]
                    entry["subclass"] = cands[0][1] or 0
                if sid == "wise_owl":
                    # Witch hut: the taught skill rides in propRewardParams
                    # parameters as a bare OE skill sid (random when empty).
                    rp = (entry.get("properties") or {}).get("propRewardParams") or {}
                    params = rp.get("parameters") or []
                    skill = None
                    if params and str(params[0]) in OE_SKILL_SIDS:
                        # exact name match, else a random h3 skill (user
                        # decision: OE-only skills are randomized)
                        skill = _h3_skill_from_oe_sid(str(params[0]))
                    witchhut_metadata[str(entry.get("id"))] = OrderedDict([
                        ("skill", skill)])
    # Placed heroes (propHeroes rows on hero-spawner / city-spawner /
    # random-city / ... objects): the starting spells are the catalog
    # hero's standard startMagics (Core.zip DB/heroes/**, user decision),
    # carried into H3 as the SoD spells bitfield (and into H2 as
    # availableSpells) - see _h3_hero_spells_bitfield.
    for obj_list in tiles.values():
        for entry in obj_list:
            row = (entry.get("properties") or {}).get("propHeroes")
            if not isinstance(row, dict):
                continue
            hero_sid = row.get("heroSid") or ""
            if not hero_sid or hero_sid == "random" or not row.get("isDefined"):
                continue
            hm = OrderedDict([("sourceHeroSid", hero_sid)])
            bits_hex = _h3_hero_spells_bitfield(hero_sid)
            if bits_hex:
                hm["spells"] = bits_hex
            hero_metadata[str(entry.get("id"))] = hm
    # Prop rows whose id matches no placed object/squad/marker ("orphan"
    # rows, e.g. left over from deleted objects): kept raw under
    # sourceOrphanProps so unified -> .map re-emits them (5d).
    known_ids = set()
    for group in adventure.get("objects", []) or []:
        known_ids.update(group.get("ids") or [])
    for squad in adventure.get("squads", []) or []:
        known_ids.update(squad.get("ids") or [])
    for marker in adventure.get("markers", []) or []:
        if isinstance(marker.get("id"), int):
            known_ids.add(marker["id"])
    orphan_props = OrderedDict()
    all_props = adventure.get("objectsProperties") or {}
    for table, rows in all_props.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("id"), int) \
                    and row["id"] not in known_ids:
                orphan_props.setdefault(table, []).append(row)
    result = OrderedDict([("tiles", tiles)])
    if orphan_props:
        result["sourceOrphanProps"] = orphan_props
    if monster_metadata:
        result["monsterMetadata"] = monster_metadata
    if artifact_metadata:
        result["artifactMetadata"] = artifact_metadata
    if pandora_metadata:
        result["pandoraMetadata"] = pandora_metadata
    if witchhut_metadata:
        result["witchhutMetadata"] = witchhut_metadata
    if shrine_metadata:
        result["shrineMetadata"] = shrine_metadata
    if hero_metadata:
        result["heroMetadata"] = hero_metadata
    # Raw adventure-level data with no unified equivalent, kept as-is.
    if adventure.get("rivers"):
        result["sourceRivers"] = adventure["rivers"]
    if adventure.get("areas"):
        result["sourceAreas"] = adventure["areas"]
    return result


def _hommoe_owners_to_unified(unified):
    """Recover h3m-style ownableMetadata owners from propOwners rows.
    propOwners.owner is a 0-based player index while block 1 spawns (and
    unified playerDetails) are 1-based, so stored owner o maps to
    playerDetails[o]; -1/absent means neutral and needs no row on the h3m
    side (owner 0xFF). Only dwelling/mine objects carry it in practice
    (random-city/random-hero use propOwners too, but they are not ownable
    h3m classes). Evidence: not_converted_yet.english.txt 1d-note2c/2d."""
    objects = unified.get("objects") or {}
    tiles = objects.get("tiles") or {}
    details = unified.get("playerDetails") or []
    if not details or not tiles:
        return
    ownable = OrderedDict()
    for _tile_key, obj_list in tiles.items():
        for entry in obj_list:
            if entry.get("group") not in ("ADVENTURE_DWELLINGS", "ADVENTURE_MINES"):
                continue
            row = (entry.get("properties") or {}).get("propOwners")
            if not isinstance(row, dict):
                continue
            stored = row.get("owner")
            if not isinstance(stored, int) or stored < 0 or stored >= len(details):
                continue
            color = FH2M_TO_H3M_COLOR_ALIAS.get(details[stored].get("color"),
                                                details[stored].get("color"))
            if color in H3M_PLAYER_COLORS:
                ownable[str(entry.get("id"))] = OrderedDict([
                    ("owner", H3M_PLAYER_COLORS.index(color)),
                ])
    if ownable:
        objects["ownableMetadata"] = ownable


_HOMMOE_STAT_ACTION_TO_FIELD = {
    "offence": ("primarySkills", "attack"),
    "defence": ("primarySkills", "defense"),
    "spellPower": ("primarySkills", "spellPower"),
    "intelligence": ("primarySkills", "knowledge"),
    "luck": ("luck", None),
    "moral": ("morale", None),
}

# OE Dialog* action types: p[0] is a dialog flow sid resolved from the
# game's Core.zip (DB/dialogs/dialogs/...), never from the .map itself
# (block 3 dialogQuestData is an empty shell in every shipped map, and
# the game runs quests from block 4 - see map-write.ts embedScenarioInContainer).
HOMMOE_DIALOG_ACTIONS = ("Dialog", "DialogOne", "DialogIfHero", "DialogIfRes",
                         "DialogIfCounter", "DialogIfItem", "DialogOneIfHero",
                         "DialogOneIfRes", "DialogOneIfCounter", "RandomDialog")
# OE local-counter actions (p = [counterSid, ...]): H2/H3 have no counters,
# so these only ever surface as notes on the decoded event.
HOMMOE_COUNTER_ACTIONS = ("CounterSet", "CounterPlus", "CounterMinus", "CounterSetRandom")


def _hommoe_structured_condition(c):
    if not isinstance(c, dict):
        return c
    out = OrderedDict([
        ("type", str(c.get("c", ""))),
        ("params", [str(v) for v in (c.get("p") or [])]),
        ("comment", str(c.get("comment") or "")),
    ])
    if "counter" in c:
        out["counter"] = c["counter"]
    return out


def _hommoe_structured_action(a):
    if not isinstance(a, dict):
        return a
    out = OrderedDict([
        ("type", str(a.get("a", ""))),
        ("params", [str(v) for v in (a.get("p") or [])]),
        ("comment", str(a.get("comment") or "")),
    ])
    if "break" in a:
        out["break"] = a["break"]
    return out


def _hommoe_structured_trigger(t):
    return OrderedDict([
        ("comment", str(t.get("comment") or "")),
        ("repeat", bool(t.get("repeat", False))),
        ("conditionsLogic", str(t.get("conditionsLogic") or "And")),
        ("conditions", [_hommoe_structured_condition(c) for c in (t.get("conditions") or [])]),
        ("actions", [_hommoe_structured_action(a) for a in (t.get("actions") or [])]),
    ])


def _hommoe_structured_quest(q):
    return OrderedDict([
        ("sid", str(q.get("sid") or "")),
        ("name", str(q.get("name") or "")),
        ("desc", str(q.get("desc") or "")),
        ("main", bool(q.get("main", False))),
        ("hidden", bool(q.get("hidden", False))),
        ("activeOnStart", bool(q.get("activeOnStart", False))),
        ("comment", str(q.get("comment") or "")),
        ("sharing", str(q.get("sharing") or "")),
        ("subQuestGroups", q.get("subQuestGroups") or []),
        ("subQuests", [OrderedDict([
            ("sid", str(s.get("sid") or "")),
            ("name", str(s.get("name") or "")),
            ("desc", str(s.get("desc") or "")),
            ("hidden", bool(s.get("hidden", False))),
            ("activeOnStart", bool(s.get("activeOnStart", False))),
            ("comment", str(s.get("comment") or "")),
            ("triggers", [_hommoe_structured_trigger(t) for t in (s.get("triggers") or [])]),
        ]) for s in (q.get("subQuests") or []) if isinstance(s, dict)]),
    ])


def _hommoe_structured_interruption(i):
    return OrderedDict([
        ("sid", str(i.get("sid") or "")),
        ("interruption", str(i.get("interruption") or "")),
        ("activeOnStart", bool(i.get("activeOnStart", False))),
        ("params", [str(v) for v in (i.get("p") or [])]),
        ("actions", [_hommoe_structured_action(a) for a in (i.get("actions") or [])]),
    ])


def _hommoe_scripting_to_structured(scripts):
    """Readable, normalized view of the raw .map scripting blocks
    (dialogQuestData + commentAiData): counters, interruptions and quests
    with every trigger condition/action type, params and comment decoded.
    The raw blocks stay in unified["scripts"] for the lossless .map->.map
    passthrough; this key is the inspection / H2-H3 mapping view."""
    out = OrderedDict()
    b4 = scripts.get("commentAiData")
    if isinstance(b4, dict):
        out["comment"] = b4.get("comment", "")
        out["aiRolesId"] = b4.get("aiRolesId", "")
        out["counters"] = [OrderedDict([
            ("sid", str(c.get("sid") or "")),
            ("value", c.get("value", 0)),
            ("comment", str(c.get("comment") or "")),
            ("sharing", str(c.get("sharing") or "")),
            ("minValue", c.get("minValue", -2147483648)),
            ("maxValue", c.get("maxValue", 2147483647)),
        ]) for c in (b4.get("counters") or []) if isinstance(c, dict)]
        out["interruptions"] = [_hommoe_structured_interruption(i)
                                for i in (b4.get("interruptions") or []) if isinstance(i, dict)]
        out["quests"] = [_hommoe_structured_quest(q)
                         for q in (b4.get("quests") or []) if isinstance(q, dict)]
    b3 = scripts.get("dialogQuestData")
    if isinstance(b3, dict):
        dialogs = b3.get("dialogs") or {}
        out["dialogLines"] = dialogs.get("lines") or []
        quests = b3.get("quests") or {}
        qlist = quests.get("quests") if isinstance(quests, dict) else quests
        out["dialogQuests"] = [_hommoe_structured_quest(q)
                               for q in (qlist or []) if isinstance(q, dict)]
    return out


def _hommoe_actions_to_event(actions, repeat):
    """Decode one quest trigger's actions into an h3m eventMetadata entry
    (the reverse of _hommoe_event_actions)."""
    evt = OrderedDict([
        ("message", ""),
        ("experience", None),
        ("mana", 0),
        ("morale", 0),
        ("luck", 0),
        ("resources", OrderedDict((n, 0) for n in
            ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"))),
        ("primarySkills", OrderedDict((n, 0) for n in
            ("attack", "defense", "spellPower", "knowledge"))),
        ("secondarySkills", []),
        ("artifacts", []),
        ("spells", []),
        ("creatures", []),
        ("players", 0xFF),
        ("applyToComputer", True),
        ("removeAfterVisit", not repeat),
    ])
    msgs = []
    unconverted = []
    for a in actions:
        if not isinstance(a, dict):
            continue
        name = a.get("a")
        p = a.get("p") or []
        if name == "Print" and p:
            msgs.append(str(p[0]))
        elif name in HOMMOE_DIALOG_ACTIONS and p:
            # dialog flow sid resolved from the game's Core.zip, not from
            # the .map - keep it as a message marker
            msgs.append("dialog:%s" % p[0])
        elif name in HOMMOE_COUNTER_ACTIONS and p:
            # H2/H3 events have no counters; note the counter op instead
            unconverted.append("%s:%s" % (name, ",".join(str(x) for x in p)))
        elif name == "GiveRes" and len(p) >= 2:
            res = HOMMOE_TO_UNIFIED_RESOURCE.get(str(p[0]))
            if res:
                evt["resources"][res] = int(p[1])
            else:
                unconverted.append("GiveRes:%s" % p[0])
        elif name == "GiveItemHero" and p:
            sid = str(p[0])
            if sid in OE_ARTIFACT_SID_TO_H3:
                evt["artifacts"].append(OE_ARTIFACT_SID_TO_H3[sid])
            else:
                unconverted.append("GiveItemHero:%s" % sid)
        elif name in ("AddSkillAll", "AddSkillHero") and p:
            sid = str(p[0])
            if sid in OE_SKILL_SIDS:
                level = 0
                cmt = str(a.get("comment") or "")
                if cmt.startswith("level ") and cmt[6:].isdigit():
                    level = int(cmt[6:])
                # exact name match, else a random h3 skill (user decision:
                # all other skill conversions are random); None = the
                # excluded skill_faction_* sids
                h3_skill = _h3_skill_from_oe_sid(sid)
                if h3_skill is not None:
                    evt["secondarySkills"].append(OrderedDict([
                        ("id", h3_skill), ("level", level)]))
                else:
                    unconverted.append("AddSkill:%s" % sid)
            else:
                unconverted.append("AddSkill:%s" % sid)
        elif name == "GiveExpHero" and p:
            evt["experience"] = int(p[0])
        elif name in ("GiveManaHero", "ChangeManaHero") and len(p) >= 2:
            evt["mana"] = int(p[1])
        elif name == "GiveStatsHero" and len(p) >= 3:
            mapping = _HOMMOE_STAT_ACTION_TO_FIELD.get(str(p[0]))
            if mapping:
                section, field = mapping
                if field:
                    evt[section][field] = int(p[2])
                else:
                    evt[section] = int(p[2])
            else:
                unconverted.append("GiveStatsHero:%s" % p[0])
        elif name == "AddSpellHero" and p:
            sid = str(p[0])
            h3_spell = _h3_spell_from_oe_sid(sid)
            if h3_spell is not None:
                # exact name match, or a random h3 spell of the same level
                # (mirror of the forward fallback)
                evt["spells"].append(h3_spell)
            else:
                unconverted.append("AddSpellHero:%s" % sid)
        elif name == "DeleteEntity" and p:
            # our generated event quests delete the event entity when the
            # source event had removeAfterVisit
            evt["removeAfterVisit"] = True
        elif name == "GiveUnitHero" and len(p) >= 2:
            sid = str(p[0])
            if sid in OE_UNIT_SID_TO_H3_CREATURE:
                evt["creatures"].append(OrderedDict([
                    ("creature", OE_UNIT_SID_TO_H3_CREATURE[sid]),
                    ("count", int(p[1]))]))
            else:
                unconverted.append("GiveUnitHero:%s" % sid)
        elif name:
            unconverted.append(str(name))
    evt["message"] = "\n".join(msgs)
    if unconverted:
        evt["comment"] = "unconverted actions: " + ", ".join(unconverted)
    return evt


def _hommoe_actions_to_daily(actions, week, day, repeat):
    """Decode a StartTurn "daily_event_<i>" quest into a unified dailyEvents
    entry (the reverse of the daily-event quests _hommoe_generate_scripts
    writes). The repeat period is lost forward (only repeat/no-repeat is
    kept), so a repeating quest maps back to a 7-day period."""
    entry = OrderedDict([
        ("name", ""),
        ("message", ""),
        ("humanColors", list(H3M_PLAYER_COLORS)),
        ("computerColors", list(H3M_PLAYER_COLORS)),
        ("firstOccurrenceDay", (week - 1) * 7 + day),
        ("repeatPeriodInDays", 7 if repeat else 0),
        ("resources", OrderedDict((n, 0) for n in
            ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"))),
    ])
    msgs = []
    for a in actions:
        if not isinstance(a, dict):
            continue
        name = a.get("a")
        p = a.get("p") or []
        if name == "Print" and p:
            msgs.append(str(p[0]))
        elif name in HOMMOE_DIALOG_ACTIONS and p:
            msgs.append("dialog:%s" % p[0])
        elif name == "GiveRes" and len(p) >= 2:
            res = HOMMOE_TO_UNIFIED_RESOURCE.get(str(p[0]))
            if res:
                entry["resources"][res] = int(p[1])
    entry["message"] = "\n".join(msgs)
    return entry


def _hommoe_quests_to_events(unified):
    """Reverse of _hommoe_generate_scripts: decode the commentAiData /
    dialogQuestData quests back into unified eventMetadata (h3m class 26
    ground events on the objects whose propEntities sid the quest triggers
    on) and dailyEvents (the StartTurn "daily_event_<i>" quests).

    Only quests carrying the sids our own forward pass generates
    ("event_<id>" entities, "daily_event_<i>" quest sids) are converted;
    native OE scripts stay raw in unified["scripts"] and are decoded into
    the structured unified["oeScripting"] view by
    _hommoe_scripting_to_structured."""
    objects = unified.get("objects") or {}
    tiles = objects.get("tiles") or {}
    scripts = unified.get("scripts") or {}
    obj_by_id = {}
    for tile_key, obj_list in tiles.items():
        for o in obj_list:
            if o.get("id") is not None:
                obj_by_id[int(o["id"])] = o
    entity_to_oid = {}
    for oid, o in obj_by_id.items():
        pe = (o.get("properties") or {}).get("propEntities")
        if isinstance(pe, dict) and pe.get("sid"):
            entity_to_oid[str(pe["sid"])] = oid
    event_metadata = objects.setdefault("eventMetadata", OrderedDict())
    daily = unified.setdefault("dailyEvents", [])
    for block_name in ("commentAiData", "dialogQuestData"):
        block = scripts.get(block_name)
        if not isinstance(block, dict):
            continue
        quests = block.get("quests") or []
        if isinstance(quests, dict):
            quests = quests.get("quests") or []
        for q in quests:
            if not isinstance(q, dict):
                continue
            qsid = str(q.get("sid") or "")
            for sub in q.get("subQuests") or []:
                if not isinstance(sub, dict):
                    continue
                for trig in sub.get("triggers") or []:
                    if not isinstance(trig, dict):
                        continue
                    conds = trig.get("conditions") or []
                    actions = trig.get("actions") or []
                    repeat = bool(trig.get("repeat"))
                    for cond in conds:
                        if not isinstance(cond, dict):
                            continue
                        if cond.get("c") == "ObjectInteractionAfter":
                            p = cond.get("p") or []
                            entity = str(p[0]) if p else ""
                            if not (entity.startswith("event_")
                                    and entity[6:].isdigit()):
                                continue
                            oid = entity_to_oid.get(entity)
                            if oid is None or oid not in obj_by_id:
                                continue
                            evt = _hommoe_actions_to_event(actions, repeat)
                            extra = [str(c.get("c")) for c in conds
                                     if isinstance(c, dict) and c is not cond]
                            if extra:
                                note = "extra conditions: " + ", ".join(extra)
                                evt["comment"] = (evt["comment"] + "; " if evt.get("comment") else "") + note
                            event_metadata[str(oid)] = evt
                            o = obj_by_id[oid]
                            # The forward pass emitted the event object under
                            # the generic misc fallback sid; restore the h3m
                            # class 26 identity here.
                            o["class"] = 26
                            o["subclass"] = 0
                            o["sprite"] = "AVZevnt0.def"
                            o["group"] = "ADVENTURE_MISCELLANEOUS"
                        elif cond.get("c") == "StartTurn" and qsid.startswith("daily_event_"):
                            p = cond.get("p") or []
                            if len(p) >= 2 and str(p[0]).isdigit() and str(p[1]).isdigit():
                                daily.append(_hommoe_actions_to_daily(
                                    actions, int(p[0]), int(p[1]), repeat))


def convert_hommoe_to_unified(map_data):
    """
    Convert the JSON produced by parse_hommoe into the unified format.

    Args:
        map_data: Dictionary as returned by parse_hommoe.

    Returns:
        OrderedDict: The map in the unified format.
    """
    blocks = {}
    for block in map_data.get("blocks", []):
        if block.get("data") is not None:
            blocks[block.get("name")] = block["data"]
    scenario = blocks.get("scenario") or {}
    adventure = blocks.get("adventure") or {}

    unified = OrderedDict()
    unified["sourceGame"] = "hommoe"
    unified["sourceVersion"] = str(map_data.get("version", ""))
    unified["name"] = adventure.get("mapName") or scenario.get("title", "")
    unified["description"] = adventure.get("mapDesc") or scenario.get("desc", "")
    unified["creatorNotes"] = ""
    # Olden Era has no single map difficulty (only per-side start
    # settings, kept raw below); default to Normal like the other games.
    unified["difficulty"] = "Normal"

    width = scenario.get("sizeX") or adventure.get("sizeX_") or 0
    height = scenario.get("sizeZ") or adventure.get("sizeZ_") or width
    unified["mapSize"] = OrderedDict([("width", width), ("height", height)])
    unified["hasUnderground"] = False
    unified["mainLanguage"] = 0

    # Raw scenario fields with no unified equivalent, kept for reference.
    if scenario.get("title") or scenario.get("desc"):
        unified["sourceNameDescSids"] = OrderedDict([
            ("title", scenario.get("title", "")),
            ("desc", scenario.get("desc", "")),
        ])
    if scenario.get("startSettings"):
        unified["sourceStartSettings"] = scenario["startSettings"]
    if scenario.get("banInfoData"):
        unified["sourceBanInfoData"] = scenario["banInfoData"]
    # Raw scenario/adventure fields with no unified equivalent, kept as-is
    # so unified -> .map can re-emit them verbatim (5c/5d in
    # not_converted_yet.english.txt). hashSum is excluded: the writer
    # re-mints the per-map identity (see 5a).
    kept_scen = {"title", "desc", "spawns", "startSettings", "banInfoData",
                 "sizeX", "sizeZ", "endController"}
    scen_extra = OrderedDict((k, v) for k, v in scenario.items()
                             if k not in kept_scen and k != "hashSum")
    if scen_extra:
        unified["sourceScenarioExtra"] = scen_extra
    if scenario.get("spawns"):
        # Verbatim spawns block (isLocked/colorId/playerId/takenHeroes...).
        unified["sourceSpawnsRaw"] = scenario["spawns"]
    kept_adv = {"fileMapName", "mapName", "mapNameFromLoc", "mapDesc",
                "mapDescFromLoc", "sizeX_", "sizeZ_", "tilesMap", "levelsMap",
                "climbsMap", "roadsMap", "waterMap", "objects", "squads",
                "markers", "areas", "rivers", "objectsProperties"}
    adv_extra = OrderedDict((k, v) for k, v in adventure.items()
                            if k not in kept_adv)
    if adv_extra:
        unified["sourceAdventureExtra"] = adv_extra

    # Players: one spawn entry per side (owner is 1-based).
    spawns = (scenario.get("spawns") or {}).get("spawns", [])
    available = []
    human = []
    computer = []
    player_details = []
    for index, spawn in enumerate(spawns):
        color_id = spawn.get("colorId", -1)
        if not isinstance(color_id, int) or color_id < 0:
            color_id = index
        color = HOMMOE_PLAYER_COLORS[color_id % len(HOMMOE_PLAYER_COLORS)]
        spawn_type = spawn.get("spawnType", 2)
        if spawn_type in (0, 1):
            available.append(color)
        if spawn_type == 0:
            human.append(color)
        elif spawn_type == 1:
            computer.append(color)
        faction_sid = spawn.get("factionSid") or ""
        detail = OrderedDict()
        detail["color"] = color
        detail["available"] = spawn_type in (0, 1)
        detail["sourceRace"] = faction_sid if faction_sid else "Random"
        if faction_sid:
            detail["race"] = HOMMOE_FACTION_NAMES.get(faction_sid)
        else:
            detail["race"] = "Random"
        if spawn.get("isHeroDefined") and spawn.get("heroSid"):
            detail["sourceHeroSid"] = spawn["heroSid"]
        if spawn.get("spawnPointType") == 0:
            main_town = _hommoe_main_town(spawn, adventure, width)
            if main_town is not None:
                detail["mainTown"] = main_town
        player_details.append(detail)

    unified["players"] = OrderedDict([
        ("availableColors", available),
        ("humanColors", human),
        ("computerColors", computer),
    ])
    unified["playerDetails"] = player_details

    # No alliance data in the samples (maxAlliancesCount is 0).
    unified["teams"] = []

    # Victory: from adventure.settings.mapWinConditions (typeWinCondition
    # ints); when empty, from the scripting block (GameVictory action =
    # quest-scripted win, e.g. scenario maps). Loss: OE has no structured
    # loss list, so "loseEverything" unless the script forces a loss.
    win_entries = (adventure.get("settings") or {}).get("mapWinConditions") or []
    win_types = [entry.get("typeWinCondition") for entry in win_entries if isinstance(entry, dict)]
    script_actions = _hommoe_script_actions(blocks)
    has_script_victory = "GameVictory" in script_actions
    has_script_lose = bool(script_actions & {"GameLose", "SideLose"})

    victory = OrderedDict()
    if any(t == 0 for t in win_types):
        victory["type"] = "defeatEveryone"
        allow_normal = True
    elif win_types:
        victory["type"] = HOMMOE_WIN_CONDITIONS.get(win_types[0], "unknown")
        allow_normal = False
    elif has_script_victory:
        victory["type"] = "scriptedVictory"
        allow_normal = False
    else:
        victory["type"] = "defeatEveryone"
        allow_normal = True
    victory["allowNormalVictory"] = allow_normal
    victory["appliesToAI"] = True
    victory["metadata"] = list(win_types)
    victory["sourceEndController"] = scenario.get("endController", 0)
    if win_entries:
        victory["sourceWinConditions"] = win_entries
    if has_script_victory:
        victory["scriptHasVictoryAction"] = True
    unified["victoryCondition"] = victory

    loss = OrderedDict()
    loss["type"] = "loseEverything"
    loss["metadata"] = []
    if has_script_lose:
        loss["scriptHasLoseAction"] = True
    unified["lossCondition"] = loss

    unified["rumors"] = []
    unified["dailyEvents"] = []

    # Quest/dialog scripts: the Olden Era equivalent of H2/H3 map events,
    # but with full trigger support (conditions + actions + counters).
    # Blocks dialogQuestData and commentAiData are carried raw under
    # "scripts" so nothing is lost.
    scripts = OrderedDict()
    if blocks.get("dialogQuestData"):
        scripts["dialogQuestData"] = blocks["dialogQuestData"]
    if blocks.get("commentAiData"):
        scripts["commentAiData"] = blocks["commentAiData"]
    if scripts:
        unified["scripts"] = scripts
        # Structured (readable) view of the same native OE scripting:
        # counters, interruptions, quests with all condition/action types,
        # and the block-3 dialog lines/quests. Raw passthrough above keeps
        # .map -> .map lossless; this key is what .map -> H2/H3 can see.
        structured = _hommoe_scripting_to_structured(scripts)
        if structured:
            unified["oeScripting"] = structured

    # Terrain: tilesMap biome ids; a nonzero waterMap id means Water.
    grid = []
    tiles_map = adventure.get("tilesMap", [])
    water_map = adventure.get("waterMap", [])
    levels_map = adventure.get("levelsMap", [])
    climbs_map = adventure.get("climbsMap", [])
    roads_map = adventure.get("roadsMap", [])
    for index, tile_id in enumerate(tiles_map):
        x = index % width if width else 0
        y = index // width if width else 0
        water_id = water_map[index] if index < len(water_map) else 0
        if water_id:
            terrain = "Water"
            source_terrain = "water:{}".format(water_id)
        else:
            terrain = HOMMOE_TILE_TERRAINS.get(tile_id, "Unknown (0x{:02X})".format(tile_id))
            source_terrain = "tile:{}".format(tile_id)
        cell = OrderedDict([
            ("x", x),
            ("y", y),
            ("z", 0),
            ("terrain", terrain),
            ("sourceTerrain", source_terrain),
            ("sourceTileId", tile_id),
        ])
        if index < len(levels_map):
            cell["sourceLevel"] = levels_map[index]
        if index < len(climbs_map):
            cell["sourceClimb"] = climbs_map[index]
        if index < len(roads_map) and roads_map[index]:
            cell["sourceRoadIndex"] = roads_map[index]
        grid.append(cell)
    unified["terrain"] = OrderedDict([
        ("levels", [OrderedDict([("grid", grid)])]),
    ])

    unified["objects"] = _hommoe_objects_to_unified(adventure, width)
    _hommoe_owners_to_unified(unified)
    _hommoe_quests_to_events(unified)

    return unified


def convert_to_unified(map_data, source_game):
    """
    Convert a parsed map into the unified format.

    Args:
        map_data: Dictionary as returned by parse_h3m, parse_fh2m or
            parse_hommoe.
        source_game: "h3m", "fh2m" or "hommoe".

    Returns:
        OrderedDict: The map in the unified format.
    """
    if source_game == "fh2m":
        return convert_fh2m_to_unified(map_data)
    if source_game == "hommoe":
        return convert_hommoe_to_unified(map_data)
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
    "Desert": "Rough",
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
        # The fh2m maps encode to the SoD layout (0x1C): the object
        # encoder writes the AB/SoD object data (objectIDs, 2-byte
        # creature ids, the SoD hero/town fields), the header uses
        # the SoD sections (disposed heroes, allowed spells and
        # abilities bitfields, all-zero = everything allowed).
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

    # The fh2m color names must be aliased to the h3m ones (Yellow ->
    # Tan) before being compared against the h3m player slots; otherwise
    # the Tan slot is never marked playable while hero/town objects still
    # carry owner=Tan, and the game dereferences a non-playable player.
    def _h3m_color(name):
        return FH2M_TO_H3M_COLOR_ALIAS.get(name, name)

    players = unified.get("players", {})
    human_colors = {_h3m_color(c) for c in players.get("humanColors", [])}
    computer_colors = {_h3m_color(c) for c in players.get("computerColors", [])}
    details_by_color = {_h3m_color(d.get("color")): d for d in unified.get("playerDetails", [])}

    # Positions of the first owned town per color and the h3m town
    # types owned by each color: the official maps give every active
    # player a main town and set the owned town type bits; the
    # converted maps read them from the towns flying the player's
    # flag (decoded from the LANDSCAPE_FLAGS by the fh2m conversion).
    castle_meta = (unified.get("objects") or {}).get("castleMetadata") or {}
    town_tile_by_color = {}
    town_types_by_color = {}
    for tile_key, obj_list in ((unified.get("objects") or {}).get("tiles") or {}).items():
        for obj in obj_list:
            if obj.get("group") != "KINGDOM_TOWNS":
                continue
            meta = castle_meta.get(str(obj.get("id"))) or {}
            owner = _h3m_color(meta.get("ownerColor"))
            if not owner:
                continue
            if owner not in town_tile_by_color:
                town_tile_by_color[owner] = tile_key
            race_name = meta.get("raceName")
            for town_type, race in H3M_TOWN_TYPE_TO_FH2M_RACE.items():
                if race == race_name:
                    town_types_by_color.setdefault(owner, set()).add(H3M_TOWN_TYPES[town_type])
                    break

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
        is_active = (color in human_colors) or (color in computer_colors)
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
        # The converted maps: an active player owns the town types
        # placed on the map (decoded from the castle flags); a player
        # with no defined town can play any faction, like the official
        # maps (all town bits set - the editor shows Random).
        owned_types = town_types_by_color.get(color)
        if is_active and owned_types:
            for town in owned_types:
                owned_towns[town] = True
            player["Has Defined Towns"] = True
        elif is_active and not player["Has Defined Towns"]:
            for town in owned_towns:
                owned_towns[town] = True
            player["Has Defined Towns"] = True
        # A playable player needs a starting condition. The official
        # maps give every active player a main town or the random
        # town flag; a player with nothing would make the map invalid
        # for the official tools. The converted Heroes II maps carry
        # no starting town placement, so the active players without a
        # main town get the random town flag.
        owns_random_town = bool(detail.get("ownsRandomTown", False))
        # An active player with an owned town on the map gets it as
        # the main town (the official starting condition); a player
        # with nothing gets the random town flag.
        fallback_town_tile = town_tile_by_color.get(color) if is_active else None
        if is_active and not detail.get("mainTown") and not owns_random_town \
                and not any(owned_towns.values()) and not fallback_town_tile:
            owns_random_town = True
        player["Owns Random Town"] = owns_random_town
        player["Owned Towns"] = owned_towns

        main_town = detail.get("mainTown")
        if not main_town and fallback_town_tile:
            parts = fallback_town_tile.split("_")
            fallback_x, fallback_y = int(parts[0]), int(parts[1])
            if unified.get("sourceGame") != "h3m":
                # fh2m source: the unified town tile stores the h3m
                # instance position; Castle X/Y is the castle
                # entrance, instance + (-2, 0).
                fallback_x -= 2
            main_town = OrderedDict([
                ("generateHero", True),
                ("x", fallback_x),
                ("y", fallback_y),
                ("z", int(parts[2]) if len(parts) > 2 else 0),
            ])
        if main_town:
            player["Main Town"] = True
            player["Generate Hero At Main Town"] = bool(main_town.get("generateHero", True))
            # The game locates the starting town at its entrance cell,
            # which in every real map is the town instance coords shifted
            # by (-2, 0) (bottom-right corner of the 6x6 town minus 2 in
            # x). The fh2m town tile IS the entrance (the gate part of
            # the castle sprite sits on it), and the encoder places the
            # h3m town instance at entrance + (2, 0), so Castle X/Y is
            # the unified town tile as-is. h3m sources already carry
            # the entrance coords in their Castle X/Y.
            player["Castle X"] = int(main_town.get("x", 0))
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
    # like defeatEveryone. The Heroes II obtainArtifact with artifact
    # id 0 is the buried Ultimate Artifact: its Heroes III equivalent
    # is building the Grail.
    victory_metadata = victory.get("metadata") or []
    allow_normal = bool(victory.get("allowNormalVictory", True))
    applies_ai = bool(victory.get("appliesToAI", True))

    def _condition_detail(cond_type, metadata, is_victory):
        """h3m detail bytes (hex) for a victory/loss condition.

        h3m sources carry the raw detail bytes in the metadata (kept
        verbatim by convert_h3m_to_unified). fh2m sources carry the
        Heroes II metadata values: a tile index for the positional
        conditions (captureTown/killHero/defeatMonster/loseTown/
        loseHero), an artifact id for obtainArtifact, a resource id
        + amount for collectGold and a day count for outOfTime. The
        h3m positional details are the target object's actionable
        spot, which for a town is its entrance cell - exactly the
        tile the fh2m map stores the town on (the h3m town instance
        is placed at entrance + (2, 0)).
        """
        if unified.get("sourceGame") == "h3m":
            if metadata:
                return bytes(v & 0xFF for v in metadata).hex()
            return None
        if not metadata:
            return None
        if is_victory and cond_type in ("captureTown", "killHero", "defeatMonster") \
                or not is_victory and cond_type in ("loseTown", "loseHero"):
            tile_id = int(metadata[0])
            z = int(metadata[1]) if len(metadata) > 1 and metadata[1] in (0, 1) else 0
            level_cells = map_size * map_size
            if has_underground and tile_id >= level_cells:
                z = 1
                tile_id -= level_cells
            return bytes((tile_id % map_size, tile_id // map_size, z)).hex()
        if is_victory and cond_type == "obtainArtifact":
            from correspondence import FH2M_TO_H3M_ARTIFACTS, FH2M_ARTIFACT_CLASSES
            art = FH2M_TO_H3M_ARTIFACTS.get(int(metadata[0]))
            if art is None:
                # No h3m equivalent: fall back to the h3m random
                # artifact of the same Heroes II class (Treasure -> 66,
                # Minor -> 67, Major -> 68, Relic -> 69), the same
                # fallback as the artifact objects.
                fh2m_class = FH2M_ARTIFACT_CLASSES.get(int(metadata[0]))
                art = {1: 66, 2: 67, 3: 68, 4: 69}.get(fh2m_class, 0)
            return struct.pack("<H", art).hex()
        if is_victory and cond_type == "collectGold":
            resource = max(0, min(6, int(metadata[0])))
            amount = int(metadata[1]) if len(metadata) > 1 else 0
            return (struct.pack("<B", resource) + struct.pack("<I", amount)).hex()
        if not is_victory and cond_type == "outOfTime":
            return struct.pack("<H", int(metadata[0]) & 0xFFFF).hex()
        return None

    if victory_type in ("defeatEveryone", "defeatOtherSide"):
        data["Victory Condition"] = OrderedDict([("Type", "None")])
    elif victory_type == "obtainArtifact" and victory_metadata and victory_metadata[0] == 0:
        # buildGrail takes a town position; FF FF FF means any town. The
        # original game only accepts the Grail condition with the normal
        # victory and the AI allowed.
        data["Victory Condition"] = OrderedDict([
            ("Type", hex(victory_codes["buildGrail"])),
            ("Allow Normal Victory", True),
            ("Applies To AI", True),
            ("Detail", "ffffff"),
        ])
    else:
        vic_entry = OrderedDict([
            ("Type", hex(victory_codes.get(victory_type, 0x6))),
            ("Allow Normal Victory", allow_normal),
            ("Applies To AI", applies_ai),
        ])
        vic_detail = _condition_detail(victory_type, victory_metadata, True)
        if vic_detail:
            vic_entry["Detail"] = vic_detail
        data["Victory Condition"] = vic_entry

    loss = unified.get("lossCondition", {})
    loss_type = loss.get("type", "loseEverything")
    loss_codes = {name: code for code, name in H3M_LOSS_CONDITIONS.items()}
    loss_metadata = loss.get("metadata") or []
    if loss_type == "loseEverything":
        data["Loss Condition"] = OrderedDict([("Type", "None")])
    else:
        loss_entry = OrderedDict([
            ("Type", hex(loss_codes.get(loss_type, 0x0))),
        ])
        loss_detail = _condition_detail(loss_type, loss_metadata, False)
        if loss_detail:
            loss_entry["Detail"] = loss_detail
        data["Loss Condition"] = loss_entry

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

    # Available heroes bitfield: bit=1 means the hero can be hired.
    # A converted Heroes II map restricts no hero, so the default is
    # every hero available (all bits set), like the official maps. The
    # bitfield is 16 bytes in RoE and 20 bytes in AB/SoD, so pad with 0xFF
    # up to the target version's width.
    version_str = basic.get("Version", "")
    heroes_width = 20 if version_str != "RoE (Restoration of Erathia)" else 16
    bitfield = unified.get("availableHeroesBitfield") or "ff" * 16
    bitfield_bytes = bytes.fromhex(bitfield)
    bitfield_bytes = bitfield_bytes + b"\xff" * max(0, heroes_width - len(bitfield_bytes))
    bitfield = bitfield_bytes[:heroes_width].hex()
    data["Available Heroes"] = OrderedDict([
        ("Bitfield", bitfield),
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
    fh2m_road_index = {}
    fh2m_river_tiles = set()
    fh2m_river_index = {}
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
                    fh2m_road_index[(x, y, z)] = obj.get("index", 0)
                elif group == "STREAMS":
                    fh2m_river_tiles.add((x, y, z))
                    fh2m_river_index[(x, y, z)] = obj.get("index", 0)

        # H2 roads run diagonally (staircases of corner connections)
        # while H3 roads only connect tile to tile orthogonally: a
        # diagonal step converted as-is leaves a broken, disconnected
        # H3 road. The way the game editor draws it (see the corrected
        # Barbarian vs Wizard.h3m and Mymaptest.h3m references), a
        # diagonal step becomes an orthogonal bend through one of the
        # two inner-corner tiles - the south-most, as in the
        # Barbarian reference. A step whose corner already carries a
        # road tile (the H2 corner with both the diagonal shortcut and
        # the orthogonal path) needs no fill at all.
        _corner_steps = ((-1, -1, 0x01), (1, -1, 0x04),
                         (1, 1, 0x10), (-1, 1, 0x40))
        _added_roads = set()
        _filled_step_cands = set()
        for (rx, ry, rz) in list(fh2m_road_tiles):
            _bits = fh2m_road_index.get((rx, ry, rz), 0) & 0xFF
            for _dx, _dy, _bit in _corner_steps:
                if not _bits & _bit:
                    continue
                if (rx + _dx, ry + _dy, rz) not in fh2m_road_tiles:
                    continue
                # The two inner-corner tiles between the diagonal
                # pair; keep the south-most (the reference choice).
                _cand = [(rx + _dx, ry), (rx, ry + _dy)]
                _cand3 = [(cx, cy, rz) for cx, cy in _cand]
                if any(_c in fh2m_road_tiles or _c in _added_roads
                        for _c in _cand3):
                    # The corner already has its orthogonal path.
                    continue
                _cx, _cy = max(_cand, key=lambda t: t[1])
                if 0 <= _cx < map_size and 0 <= _cy < map_size:
                    _added_roads.add((_cx, _cy, rz))
                    _filled_step_cands.update(_cand3)

        # Road-end stubs (Mymaptest.h3m reference): the H2 road
        # visually extends one tile past a dead end, and past the end
        # of a straight run whose last tile also carries a diagonal
        # connection that already has its orthogonal path - the H3
        # road then starts its bend one tile further out, so the
        # straight run keeps the visual length it has in H2.
        _edge_dirs = {"N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0)}
        _edge_bits = {"N": 0x02, "E": 0x08, "S": 0x20, "W": 0x80}
        _stub_tiles = set()
        for (rx, ry, rz) in list(fh2m_road_tiles):
            _bits = fh2m_road_index.get((rx, ry, rz), 0) & 0xFF
            _edges = [d for d in _edge_bits if _bits & _edge_bits[d]]
            if len(_edges) != 1:
                continue
            _ex, _ey = _edge_dirs[_edges[0]]
            _sx, _sy = rx - _ex, ry - _ey
            _stub = (_sx, _sy, rz)
            if (_sx < 0 or _sx >= map_size or _sy < 0 or _sy >= map_size
                    or _stub in fh2m_road_tiles or _stub in _added_roads
                    or (_sx, _sy, rz) in _filled_step_cands):
                # Off the map, already a road, or the diagonal step of
                # this end already got its corner fill: no stub.
                continue
            _stub_tiles.add(_stub)

        # Corner stubs: a corner tile whose south neighbor and east or
        # west neighbor form a diagonal step (the H2 corner with its
        # diagonal shortcut on the south side) keeps the visual width
        # of the H2 corner - extend the horizontal one tile away from
        # the vertical (Mymaptest.h3m reference; the corners with the
        # shortcut on the north side get no stub).
        for (rx, ry, rz) in list(fh2m_road_tiles):
            if (rx, ry, rz) in _added_roads or (rx, ry, rz) in _stub_tiles:
                continue
            _bits = fh2m_road_index.get((rx, ry, rz), 0) & 0xFF
            _edges = [d for d in _edge_bits if _bits & _edge_bits[d]]
            if (len(_edges) != 2 or "S" not in _edges
                    or ("E" in _edges) == ("W" in _edges)):
                continue
            _horiz = "E" if "E" in _edges else "W"
            _s_nbr = (rx, ry + 1)
            _h_nbr = (rx + (1 if _horiz == "E" else -1), ry)
            if (_s_nbr[0], _s_nbr[1], rz) not in fh2m_road_tiles \
                    or (_h_nbr[0], _h_nbr[1], rz) not in fh2m_road_tiles:
                continue
            _s_bits = fh2m_road_index.get(
                (_s_nbr[0], _s_nbr[1], rz), 0) & 0xFF
            _brace_bit = 0x04 if _horiz == "E" else 0x01
            if not _s_bits & _brace_bit:
                continue
            _hx, _hy = _edge_dirs[_horiz]
            _sx, _sy = rx - _hx, ry - _hy
            _stub = (_sx, _sy, rz)
            if (0 <= _sx < map_size and 0 <= _sy < map_size
                    and _stub not in fh2m_road_tiles
                    and _stub not in _added_roads
                    and _stub not in _stub_tiles):
                _stub_tiles.add(_stub)
        fh2m_road_tiles |= _stub_tiles
        for _tile in _stub_tiles:
            _tx, _ty, _tz = _tile
            _mask = 0
            for _i in range(9):
                if _i == 4:
                    continue
                if (_tx + _i % 3 - 1, _ty + _i // 3 - 1, _tz) \
                        in fh2m_road_tiles:
                    _mask |= 1 << _i
            fh2m_road_index[_tile] = _mask
        fh2m_road_tiles |= _added_roads
        for _tile in _added_roads:
            # The added tile carries no H2 mask: derive the fallback
            # bitfield from the (augmented) road adjacency, the way
            # fheroes2 computes its road object index.
            _tx, _ty, _tz = _tile
            _mask = 0
            for _i in range(9):
                if _i == 4:
                    continue
                if (_tx + _i % 3 - 1, _ty + _i // 3 - 1, _tz) \
                        in fh2m_road_tiles:
                    _mask |= 1 << _i
            fh2m_road_index[_tile] = _mask

    # Per-terrain h3m main-tile ranges (VCMI editor terrainViewPatterns.json,
    # pattern n1): normal terrains 49-72, dirt 21-44, sand 0-23, water 20-32.
    # Transition/border sprites sit below those ranges and must be chosen
    # from the tile's neighbors, not copied from the fh2m image index.
    H3M_MAIN_RANGE = {
        "Water": (20, 32), "Dirt": (21, 44), "Sand": (0, 23),
        "Rock": (0, 7),
    }
    H3M_MAIN_RANGE_DEFAULT = (49, 72)

    # Neighbor direction order used for coastal masks (N,NE,E,SE,S,SW,W,NW).
    _COAST_DIRS = (("N", 0, -1), ("NE", 1, -1), ("E", 1, 0), ("SE", 1, 1),
                   ("S", 0, 1), ("SW", -1, 1), ("W", -1, 0), ("NW", -1, -1))

    # Coastal link table H2 -> H3, learned from the reference maps
    # (input/*.h3m): for each neighbor mask (directions of the other side of
    # the coast, '+'-joined), the h3m (picture, mirroring) actually used.
    # See coastal_tiles_h2_h3.md (Tableau 3) and coastal_h2/labels.csv.
    import json as _json
    import os as _os
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                            "coastal_link.json")) as _f:
        COAST_LINK = _json.load(_f)

    # Cardinal direction order used for road masks (N,E,S,W).
    _ROAD_DIRS = (("N", 0, -1), ("E", 1, 0), ("S", 0, 1), ("W", -1, 0))

    # Road link table H2 -> H3, learned from the reference maps
    # (input/*.h3m): for each cardinal road-neighbor mask, the h3m Road
    # Properties (sprite) and road mirror bits actually used.
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                            "road_link.json")) as _f:
        ROAD_LINK = _json.load(_f)

    # River link table H2 -> H3, learned from the reference maps
    # (input/*.h3m): for each cardinal river-neighbor mask, the h3m River
    # Properties (sprite) and river mirror bits (0x04/0x08) used.
    with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                            "river_link.json")) as _f:
        RIVER_LINK = _json.load(_f)

    def _fh2m_offset(cell):
        source_terrain = cell.get("sourceTerrain", "")
        if not source_terrain.startswith("terrain:"):
            return None
        try:
            image_index = int(source_terrain[len("terrain:"):])
        except ValueError:
            return None
        range_start = 0
        for start_index, name in FH2M_TERRAIN_INDEX_RANGES:
            if name == cell.get("terrain", "Grass"):
                break
            range_start = start_index
        return image_index - range_start

    # h3m water border sprite per set of land directions around the tile.
    # The picture encodes the border ORIENTATION, not the compass direction
    # (E/W and N/S share a range, the mirror flag picks the side), as
    # learned from the real maps and VCMI terrainViewPatterns.json (water
    # group): horizontal borders 4-7, vertical 8-11, corners 16-19, open
    # water 20-32. The odd offset of a pair is the mirrored variant.
    def _h3m_water_border_picture(has_n, has_e, has_s, has_w, has_diag=False,
                                  mirror=False):
        horiz = has_e or has_w
        vert = has_n or has_s
        if has_diag:
            return 18 + mirror
        if horiz and vert:
            return 16 + mirror
        if horiz:
            return 4 + mirror
        if vert:
            return 8 + mirror
        return 20

    # fh2m source terrain lookup: (x, y) -> (z, cell) per level, used to
    # derive border sprites from the neighboring terrain types.
    fh2m_level_grids = []
    if is_fh2m_source:
        for lvl in unified.get("terrain", {}).get("levels", []):
            g = {}
            for cell in lvl.get("grid", []):
                g[(cell.get("x", 0), cell.get("y", 0))] = (cell.get("z", 0), cell)
            fh2m_level_grids.append(g)

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
                # The fh2m terrain image index maps onto the h3m
                # Terrain Picture. In fh2m, each terrain range starts
                # with transition images (16 for Water and Dirt, 38
                # for the other land terrains, none for Beach) followed
                # by the main terrain images. In h3m the main tiles sit
                # in a per-terrain range (49-72 for normal land, 21-44
                # for Dirt, 0-23 for Sand, 20-32 for Water) and the
                # border sprites below them are picked from the
                # neighbors. A pure terrain tile gets a main sprite; a
                # tile touching another terrain (in fh2m a transition
                # image) gets the matching h3m border sprite derived
                # from the actual neighboring terrain types, so water
                # shores use the water border sprites (0-19).
                unified_name = cell.get("terrain", "Grass")
                offset = _fh2m_offset(cell)
                lo, hi = H3M_MAIN_RANGE.get(terrain_name, H3M_MAIN_RANGE_DEFAULT)
                if offset is None:
                    picture = lo
                elif unified_name == "Water":
                    picture = offset if offset < 16 else lo + (offset - 16) % (hi - lo + 1)
                elif unified_name == "Dirt":
                    # 16 transition images, then the main range 21-44.
                    picture = lo + (offset if offset < 16 else offset - 16) % (hi - lo + 1)
                elif unified_name == "Beach":
                    picture = offset % (hi + 1)
                elif offset < 38:
                    # H2 transition image: the border sprites are drawn
                    # from the neighboring terrain types below. A
                    # transition image without a land border (e.g. the
                    # H2 Desert/Wasteland pair, both Rough in H3) is a
                    # plain main variant.
                    picture = lo + offset % (hi - lo + 1)
                else:
                    picture = lo + (offset - 38) % (hi - lo + 1)
                level_grid = fh2m_level_grids[z] if z < len(fh2m_level_grids) else {}

                def neighbor_land(dx, dy):
                    entry = level_grid.get((x + dx, y + dy))
                    if entry is None:
                        return False
                    _, ncell = entry
                    return UNIFIED_TO_H3M_TERRAINS.get(ncell.get("terrain", "Grass"), "Dirt") not in ("Water", "Rock")

                def neighbor_water(dx, dy):
                    entry = level_grid.get((x + dx, y + dy))
                    if entry is None:
                        return False
                    _, ncell = entry
                    return UNIFIED_TO_H3M_TERRAINS.get(ncell.get("terrain", "Grass"), "Dirt") == "Water"

                def neighbor_h3_terrain(dx, dy):
                    entry = level_grid.get((x + dx, y + dy))
                    if entry is None:
                        return None
                    _, ncell = entry
                    return UNIFIED_TO_H3M_TERRAINS.get(ncell.get("terrain", "Grass"), "Dirt")

                # An H2 transition image drawn as a main variant or as
                # a border sprite carries no H2 mirroring: the H3
                # editor picks its own (the border logic below sets
                # the orientation bits it needs).
                if offset is not None and offset < 38 \
                        and unified_name not in ("Water", "Beach"):
                    mirror_bits = 0
                else:
                    mirror_bits = int(cell.get("flags", 0) or 0) & 0x03

                # Land <-> land borders: the H3 editor draws them from
                # the neighboring terrain types (the corrected
                # Mymaptest.h3m reference and VCMI's
                # terrainViewPatterns.json). A border tile of a normal
                # terrain uses the dirt-blend border sprites against
                # another land terrain and the sand-blend sprites
                # against Sand; Dirt has a single border set and Sand
                # has no borders at all (its main sprites depict the
                # transitions). Within a set the editor picks a random
                # variant, and the terrain mirroring bits 0x01/0x02
                # orient the border (E/W flip for the side, N/S flip
                # for the row).
                if terrain_name not in ("Water", "Rock", "Sand"):
                    _borders = {}
                    for _dname, _dx, _dy in (("NW", -1, -1), ("N", 0, -1),
                                            ("NE", 1, -1), ("W", -1, 0),
                                            ("E", 1, 0), ("SW", -1, 1),
                                            ("S", 0, 1), ("SE", 1, 1)):
                        _nt = neighbor_h3_terrain(_dx, _dy)
                        if (_nt is None or _nt in ("Water", "Rock")
                                or _nt == terrain_name):
                            continue
                        _borders[_dname] = (_nt == "Sand")
                    if _borders:
                        _vs_sand = (terrain_name != "Dirt") \
                            and any(_borders.values())
                        _edges = [d for d in ("N", "E", "S", "W")
                                  if d in _borders]
                        _pics = _mir = None
                        if len(_edges) == 1:
                            # A straight border on one side; the corner
                            # neighbors do not change the sprite.
                            _d = _edges[0]
                            if _d in ("E", "W"):
                                _pics = (24, 27) if _vs_sand else (4, 7)
                                _mir = 0x01 if _d == "E" else 0x00
                            else:
                                _pics = (28, 31) if _vs_sand else (8, 11)
                                _mir = 0x02 if _d == "S" else 0x00
                        elif len(_edges) == 2 and set(_edges) in \
                                ({"N", "E"}, {"E", "S"}, {"S", "W"}, {"W", "N"}):
                            # Two adjacent sides: an outer corner.
                            _corner = {frozenset(("N", "E")): "NE",
                                       frozenset(("E", "S")): "SE",
                                       frozenset(("S", "W")): "SW",
                                       frozenset(("W", "N")): "NW"}[frozenset(_edges)]
                            _pics = (20, 23) if _vs_sand else (0, 3)
                            _mir = {"NW": 0x00, "NE": 0x01,
                                    "SW": 0x02, "SE": 0x03}[_corner]
                        elif not _edges and len(_borders) == 1:
                            # A single diagonal neighbor: a corner tip.
                            _corner = next(iter(_borders))
                            _pics = (38, 39) if _vs_sand else (18, 19)
                            _mir = {"SE": 0x00, "SW": 0x01,
                                    "NE": 0x02, "NW": 0x03}[_corner]
                        else:
                            # A complex junction (opposite sides or a
                            # many-sided tile): draw the most prominent
                            # single side, south first.
                            for _d in ("S", "N", "E", "W"):
                                if _d in _borders:
                                    if _d in ("E", "W"):
                                        _pics = (24, 27) if _vs_sand else (4, 7)
                                        _mir = 0x01 if _d == "E" else 0x00
                                    else:
                                        _pics = (28, 31) if _vs_sand else (8, 11)
                                        _mir = 0x02 if _d == "S" else 0x00
                                    break
                        if _pics is not None:
                            picture = _random.randint(*_pics)
                            mirror_bits = (mirror_bits & ~0x03) | _mir

                # Sea borders: driven by the coastal link table learned
                # from the reference maps (coastal_link.json, see Tableau 3
                # in coastal_tiles_h2_h3.md). Each coastal tile is keyed by
                # the mask of its neighbors on the other side of the coast.
                if terrain_name == "Water":
                    lmask = frozenset(d for d, dx, dy in _COAST_DIRS
                                      if neighbor_land(dx, dy))
                    if lmask:
                        hit = COAST_LINK.get("water", {}).get("+".join(sorted(lmask)))
                        if hit:
                            picture = hit["picture"]
                            mirror_bits = int(hit["mirror"], 16) & 0x03
                        else:
                            has_n = neighbor_land(0, -1)
                            has_s = neighbor_land(0, 1)
                            has_w = neighbor_land(-1, 0)
                            has_e = neighbor_land(1, 0)
                            any_diag = any(neighbor_land(dx, dy) for dx, dy in
                                           ((-1, -1), (1, -1), (-1, 1), (1, 1)))
                            has_corner = any_diag and not (has_n or has_e or has_s or has_w)
                            picture = _h3m_water_border_picture(
                                has_n, has_e, has_s, has_w, has_corner,
                                mirror=bool(mirror_bits & 1))
                elif any(neighbor_water(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                         if (dx, dy) != (0, 0)):
                    # land tile touching water: coast bit (0x40) + border
                    # sprite from the link table (sand / normal terrains).
                    wmask = frozenset(d for d, dx, dy in _COAST_DIRS
                                      if neighbor_water(dx, dy))
                    wkey = "+".join(sorted(wmask))
                    if terrain_name == "Sand":
                        hit = COAST_LINK.get("sand", {}).get(wkey)
                    elif lo == H3M_MAIN_RANGE_DEFAULT[0]:
                        hit = COAST_LINK.get("landnorm", {}).get(wkey)
                    else:
                        hit = None
                    if hit:
                        picture = hit["picture"]
                        mirror_bits = int(hit["mirror"], 16) | 0x40
                    else:
                        mirror_bits |= 0x40
                        if lo == H3M_MAIN_RANGE_DEFAULT[0]:
                            w_horiz = neighbor_water(-1, 0) or neighbor_water(1, 0)
                            w_vert = neighbor_water(0, -1) or neighbor_water(0, 1)
                            w_diag = (not (w_horiz or w_vert)) and any(
                                neighbor_water(dx, dy) for dx, dy in
                                ((-1, -1), (1, -1), (-1, 1), (1, 1)))
                            if w_diag:
                                base = 38
                            elif w_horiz and w_vert:
                                base = 36
                            elif w_horiz:
                                base = 24
                            elif w_vert:
                                base = 28
                            else:
                                base = 24
                            picture = base + (mirror_bits & 1)
                # Roads (fh2m ROADS objects): the h3m Road Properties
                # sprite is chosen the way the game's own editor picks
                # the piece of a drawn road - the first matching 3x3
                # neighborhood pattern (see h3m_line_pattern_sprite:
                # the angle pieces 2-5 are the mixed corner+edge
                # pieces, the turn pieces 0-1 the cardinal corners,
                # 10-13 the straight variants, 16 the X-cross). A bend
                # no H3 piece draws (a corner joined to an edge, like
                # the H2 SW->N pieces) falls back to the fh2m
                # connection bitfield: the diagonal band piece toward
                # the corner.
                road = "None"
                road_props = 0
                if (x, y, z) in fh2m_road_tiles:
                    road = "Dirt"
                    from correspondence import h3m_line_pattern_sprite
                    _sprite, _mbits = h3m_line_pattern_sprite(
                        lambda nx, ny: (nx, ny, z) in fh2m_road_tiles,
                        x, y)
                    road_bits = fh2m_road_index.get((x, y, z), 0) & 0xFF
                    diagonals = {d for d, bit in (("NW", 1), ("NE", 4),
                                                 ("SE", 16), ("SW", 64))
                                 if road_bits & bit}
                    if _sprite is not None:
                        road_props = _sprite
                        mirror_bits |= _mbits
                    elif diagonals:
                        if len(diagonals) == 1 and not road_bits & 0xAA:
                            # A single diagonal connection: a road end
                            # through the corner (base SE).
                            road_props = 0
                            mirror_bits |= {"SE": 0x00, "SW": 0x10,
                                            "NE": 0x20,
                                            "NW": 0x30}[next(iter(diagonals))]
                        else:
                            # A diagonal band through the tile: SW<->NE
                            # (base) or SE<->NW (E<->W flip).
                            road_props = 2
                            if not diagonals & {"NE", "SW"}:
                                mirror_bits |= 0x10
                    else:
                        rkey = "".join(d for d, dx, dy in _ROAD_DIRS
                                       if (x + dx, y + dy, z) in fh2m_road_tiles)
                        hit = ROAD_LINK.get(rkey)
                        if hit is None:
                            hit = ROAD_LINK.get("-")
                        if hit:
                            road_props = hit["props"]
                            mirror_bits |= int(hit["mirror"], 16) & 0x30
                # Rivers (fh2m STREAMS objects): h3m River Type from the
                # tile terrain (Lava -> Lava, Snow -> Icy, Dirt -> Muddy,
                # else Clear), River Properties sprite from the cardinal
                # mask of neighboring river tiles via river_link.json, and
                # the river mirror bits 0x04/0x08 carry the corner
                # orientation.
                river = "None"
                river_props = 0
                if (x, y, z) in fh2m_river_tiles:
                    river = {"Lava": "Lava", "Snow": "Icy", "Dirt": "Muddy"}.get(
                        terrain_name, "Clear")
                    # Direct table first: the fh2m STREAMS index selects the
                    # segment (FH2M_TO_H3M_STREAMS); fall back to the
                    # neighbor-mask table for unknown indices.
                    from correspondence import FH2M_TO_H3M_STREAMS
                    direct = FH2M_TO_H3M_STREAMS.get(fh2m_river_index.get((x, y, z)))
                    if direct is not None:
                        river_props = direct[0]
                        mirror_bits |= direct[1] & 0x0C
                    else:
                        fkey = "".join(d for d, dx, dy in _ROAD_DIRS
                                       if (x + dx, y + dy, z) in fh2m_river_tiles)
                        hit = RIVER_LINK.get(fkey) or RIVER_LINK.get("-")
                        if hit:
                            river_props = hit["props"]
                            mirror_bits |= int(hit["mirror"], 16) & 0x0C
                        elif fkey == "NESW":
                            river_props = 4  # cross
                mirroring = "0x%02x" % mirror_bits
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

    if is_fh2m_source:
        road_index_side = OrderedDict()
        for level in unified.get("terrain", {}).get("levels", []):
            for cell in level.get("grid", []):
                if cell.get("sourceRoadIndex") is not None:
                    road_index_side["{}_{}_{}".format(
                        cell.get("x", 0), cell.get("y", 0), cell.get("z", 0))] = \
                        cell["sourceRoadIndex"]
        if road_index_side:
            # Side table for the in-memory h3m -> fh2m chain: the h3m
            # binary tile record (7 bytes) cannot store the fh2m road
            # bitfield, so it travels alongside the map dict instead
            # of inside the file (write_h3m ignores this key).
            data["fh2mRoadIndex"] = road_index_side

    # Timed events: rebuild the h3m global events table from the unified
    # daily events. The players mask is the union of the human and
    # computer color lists; the applies-to-human byte exists in SoD and
    # later only. The unified firstOccurrenceDay is 1-based, the h3m
    # field is 0-based.
    daily_events = unified.get("dailyEvents") or []
    if daily_events:
        h3m_events = []
        for index, daily in enumerate(daily_events):
            mask = 0
            for color in list(daily.get("humanColors") or []) + list(daily.get("computerColors") or []):
                if color in H3M_PLAYER_COLORS:
                    mask |= 1 << H3M_PLAYER_COLORS.index(color)
            event = OrderedDict([
                ("Name", daily.get("name") or "Event%d" % (index + 1)),
                ("Message", daily.get("message") or ""),
                ("Resources", OrderedDict(
                    (res, int((daily.get("resources") or {}).get(res, 0)))
                    for res in ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"))),
                ("Players Mask", mask),
            ])
            if version_sod:
                event["Applies to Human"] = bool(daily.get("humanColors"))
            event["Applies to Computer"] = bool(daily.get("computerColors"))
            event["First Occurrence Day"] = max(0, int(daily.get("firstOccurrenceDay", 1)) - 1)
            event["Repeat Period In Days"] = int(daily.get("repeatPeriodInDays", 0))
            h3m_events.append(event)
        data["Events"] = OrderedDict([
            ("Number of Events", len(h3m_events)),
            ("Events", h3m_events),
            ("Human Flag Present", version_sod),
            ("Raw Data", ""),
        ])

    return data


def _translate_h3m_tile_objects(obj_list, objects_section, translated_metadata,
                               dropped_ids, tile_terrain=None):
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
                # Random artifact (h3m classes 65-69): the fh2m random
                # artifacts are the last indices of the
                # ADVENTURE_ARTIFACTS group, one per class - the exact
                # inverse of the fh2m -> h3m mapping (91-95 -> 65-69).
                random_index = {65: 91, 66: 92, 67: 93, 68: 94, 69: 95}.get(
                    obj.get("class"), 74)
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_ARTIFACTS"),
                    ("index", random_index),
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
            # The fh2m ADVENTURE_ARTIFACTS group order (see
            # map_object_info.cpp, populateAdventureArtifacts): artifact
            # ids 9-81 at indices 0-72, Magic Book (id 82) at index 73,
            # the Price of Loyalty ids 87-103 at indices 74-90, then the
            # 5 random artifacts at 91-95.
            if fh2m_artifact <= 81:
                fh2m_index = fh2m_artifact - 9
            elif fh2m_artifact == 82:
                fh2m_index = 73
            else:
                fh2m_index = fh2m_artifact - 13
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
            if obj.get("class") == 77 or town_type == 255:
                # The h3m random town (its own class 77 in the real
                # maps): the H2 random town, with the castle built
                # when the h3m castle building is there (byte 0 bit 5
                # of the built bitfield, the H3 counterpart of the
                # fh2m BUILD_CASTLE flag; without custom buildings,
                # the fort byte carries it).
                built_hex = town_meta.get("builtBuildings")
                if built_hex:
                    has_castle = bool(bytes.fromhex(built_hex)[0] & 0x20)
                else:
                    has_castle = bool(town_meta.get("hasFort"))
                town_index = 12 if has_castle else 13
            elif race_name is None:
                # Unknown type: Knight castle.
                town_index = 0
            else:
                town_index = FH2M_TOWN_RACE_ORDER.index(race_name) * 2
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", "KINGDOM_TOWNS"),
                ("index", town_index),
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
            if group == "ADVENTURE_MINES" and obj.get("class") == 53:
                # The fh2m mine index encodes both the mine type (from
                # the h3m subclass) and the terrain appearance (from
                # the def name, or from the tile terrain when the def
                # has no terrain variant, e.g. the sulfur mine).
                from correspondence import h3m_mine_to_fh2m_index
                fh2m_index = h3m_mine_to_fh2m_index(obj.get("subclass"),
                                                    obj.get("sprite"),
                                                    tile_terrain)
            elif group == "ADVENTURE_DWELLINGS" and obj.get("class") == 17:
                # The h3m dwelling (class 17, subclass = dwelling id)
                # converts back to the fh2m dwelling index; dwellings
                # with no fh2m pairing fall back to index 0.
                from correspondence import H3M_TO_FH2M_DWELLINGS
                fh2m_index = H3M_TO_FH2M_DWELLINGS.get(obj.get("subclass"), 0)
            else:
                fh2m_index = 0
            translated.append(OrderedDict([
                ("id", obj_id),
                ("group", group),
                ("index", fh2m_index),
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
            sub = obj.get("subclass")
            if obj_class in (9, 10) and isinstance(sub, int) and 0 <= sub <= 7:
                # Border gate (9) / keymaster's tent (10): the subclass
                # is the color; they convert back to the fh2m Barrier /
                # Traveller's Tent color variants (MISC 51-58 / 59-66).
                from correspondence import H3M_TO_FH2M_COLOR_INDEX
                base = 51 if obj_class == 9 else 59
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", "ADVENTURE_MISCELLANEOUS"),
                    ("index", base + H3M_TO_FH2M_COLOR_INDEX[sub]),
                ]))
                continue
            interactive = H3M_TO_FH2M_INTERACTIVE.get(obj_class)
            if interactive is not None:
                translated.append(OrderedDict([
                    ("id", obj_id),
                    ("group", interactive[0]),
                    ("index", interactive[1]),
                ]))
                continue
            # The unmatchable defs (no single footprint-exact fh2m
            # object) fan out into several fh2m objects whose
            # footprints tile the def's blocked cells exactly.
            from correspondence import H3M_DEF_TO_FH2M_SUBSTITUTION
            substitution = H3M_DEF_TO_FH2M_SUBSTITUTION.get(
                (obj.get("sprite") or "").lower())
            if substitution is not None:
                for part, (sub_group, sub_index, sub_offset) in \
                        enumerate(substitution):
                    # Unique id per map: the parts beyond the first
                    # are offset above the h3m id range.
                    translated.append(OrderedDict([
                        ("id", obj_id if part == 0
                         else obj_id + part * 100000),
                        ("group", sub_group),
                        ("index", sub_index),
                        ("substOffset", [sub_offset[0], sub_offset[1]]),
                    ]))
                continue
            decorative = H3M_DECORATIVE_TO_FH2M.get(obj_class)
            if decorative is None:
                dropped_ids.append(obj_id)
                continue
            fh2m_group, fh2m_index = decorative
            if fh2m_group == "LANDSCAPE_TREES":
                # The tree def name carries the variant (forest, palm,
                # dead tree, log, stump...): use it for the fh2m index
                # when known, else keep the class-level index.
                from correspondence import h3m_tree_def_to_fh2m_index
                tree_index = h3m_tree_def_to_fh2m_index(obj_class,
                                                         obj.get("sprite"))
                if tree_index is not None:
                    fh2m_index = tree_index
                else:
                    from correspondence import \
                        H3M_TREE_DEF_TO_FH2M_MOUNTAIN_INDEX
                    mountain_tree = H3M_TREE_DEF_TO_FH2M_MOUNTAIN_INDEX.get(
                        (obj.get("sprite") or "").lower())
                    if mountain_tree is not None:
                        fh2m_group, fh2m_index = ("LANDSCAPE_MOUNTAINS",
                                                  mountain_tree)
            # The mountain def name carries the terrain and the size
            # (AVLmtgr3.def = grass medium mountain...): the fh2m
            # mountain index is the terrain block * 19 plus a variant
            # matching the size.
            from correspondence import (H3M_MOUNTAIN_CLASSES,
                                      h3m_mountain_def_to_fh2m_index)
            if obj_class in H3M_MOUNTAIN_CLASSES:
                mountain_index = h3m_mountain_def_to_fh2m_index(
                    obj_class, obj.get("sprite"))
                if mountain_index is not None:
                    fh2m_group, fh2m_index = ("LANDSCAPE_MOUNTAINS",
                                              mountain_index)
            translated_obj = OrderedDict([
                ("id", obj_id),
                ("group", fh2m_group),
                ("index", fh2m_index),
            ])
            if obj.get("sprite"):
                # The sprite carries the h3m footprint variant (the
                # blocked cells of the def): the fh2m restore uses it
                # to align the anchors exactly.
                translated_obj["sprite"] = obj.get("sprite")
            translated.append(translated_obj)
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
    restored_objects = []

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
    # h3m terrain name per tile, used by the mine translation to read
    # the appearance of the mine defs with no terrain variant.
    h3m_tile_terrains = {}
    if is_h3m_source:
        for level in unified.get("terrain", {}).get("levels", []):
            for cell in level.get("grid", []):
                h3m_tile_terrains[(cell.get("x", 0), cell.get("y", 0), cell.get("z", 0))] = \
                    cell.get("sourceTerrain") or cell.get("terrain")
    fh2m_tile_terrains = {}
    if not is_h3m_source:
        for level in unified.get("terrain", {}).get("levels", []):
            for cell in level.get("grid", []):
                fh2m_tile_terrains[(cell.get("x", 0), cell.get("y", 0), cell.get("z", 0))] = \
                    cell.get("terrain")
    for tile_key, obj_list in objects_section.get("tiles", {}).items():
        parts = tile_key.split("_")
        if len(parts) != 3:
            continue
        x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
        if z != 0:
            continue
        if not is_h3m_source:
            # fh2m source: the unified tiles hold the shifted (h3m
            # convention) anchors; restore the original fh2m
            # anchors with the stored anchorShift (the inverse of the
            # shift applied by the fh2m -> unified conversion, kept
            # per object so the same-format round-trip restores the
            # exact original tile). The objects of one original tile
            # may live on several unified tiles, so the original
            # order is restored globally through the sourceOrder.
            from correspondence import fh2m_to_h3m_anchor_shift
            for obj in obj_list:
                obj_group = obj.get("group", "")
                stored = obj.get("anchorShift")
                if stored:
                    shift = (int(stored[0]), int(stored[1]))
                elif obj_group == "KINGDOM_TOWNS":
                    shift = (2, 0)
                else:
                    shift = fh2m_to_h3m_anchor_shift(
                        obj_group, obj.get("index"),
                        fh2m_tile_terrains.get((x, y, z)))
                restored = OrderedDict((k, v) for k, v in obj.items()
                                       if k not in ("anchorShift",
                                                    "sourceOrder"))
                if shift:
                    target = (x - shift[0], y - shift[1])
                else:
                    target = (x, y)
                order = obj.get("sourceOrder")
                restored_objects.append(
                    (order if order is not None else 0, target, restored))
            continue
        translated = _translate_h3m_tile_objects(obj_list, objects_section,
                                                  translated_metadata,
                                                  dropped_ids,
                                                  h3m_tile_terrains.get((x, y, z)))
        if translated:
            # Per-object anchor shift, the opposite of the fh2m -> h3m
            # shift: the h3m anchor is the south-east corner of the
            # footprint, the fh2m anchor sits inside its deduced
            # footprint. Objects of one tile may shift to different
            # fh2m tiles, so they are redistributed per object.
            from correspondence import fh2m_to_h3m_anchor_shift
            tile_terrain = h3m_tile_terrains.get((x, y, z))
            for obj in translated:
                obj_group = obj.get("group", "")
                subst_offset = obj.get("substOffset")
                if subst_offset is not None:
                    # A substitution part: its offset from the h3m
                    # anchor already places the fh2m footprint.
                    obj.pop("substOffset", None)
                    target = (min(max(x + int(subst_offset[0]), 0), width - 1),
                              min(max(y + int(subst_offset[1]), 0), width - 1))
                    objects_by_tile.setdefault(target, []).append(obj)
                    continue
                if obj_group == "KINGDOM_TOWNS":
                    # The h3m town instance sits at the bottom-right
                    # corner of the castle footprint; the fh2m town
                    # tile is the entrance, 2 tiles to the left on
                    # the same row (instance + (-2, 0), the inverse
                    # of the fh2m -> h3m shift).
                    target = (max(x - 2, 0), y)
                else:
                    if (obj_group in ("LANDSCAPE_TREES", "LANDSCAPE_MOUNTAINS")
                            and obj.get("sprite")):
                        # The h3m def of the instance carries its real
                        # blocked cells: align on it, not on the def
                        # the fh2m -> h3m direction would pick.
                        from correspondence import h3m_def_anchor_shift
                        shift = h3m_def_anchor_shift(
                            obj_group, obj.get("index"), obj.get("sprite"))
                        if shift is None:
                            shift = fh2m_to_h3m_anchor_shift(
                                obj_group, obj.get("index"), tile_terrain)
                    else:
                        shift = fh2m_to_h3m_anchor_shift(obj_group,
                                                        obj.get("index"),
                                                        tile_terrain)
                    if shift:
                        target = (min(max(x - shift[0], 0), width - 1),
                                  min(max(y - shift[1], 0), width - 1))
                    else:
                        target = (x, y)
                objects_by_tile.setdefault(target, []).append(obj)
    if restored_objects:
        # fh2m source: flush the restored objects globally sorted by
        # their original tile-major order.
        for _, target, restored in sorted(restored_objects,
                                          key=lambda e: e[0]):
            objects_by_tile.setdefault(target, []).append(restored)
    if dropped_ids:
        objects_section = OrderedDict(objects_section)
        objects_section["dropped"] = dropped_ids

    default_terrain = (UNIFIED_TO_FH2M_TERRAIN_INDEX.get("Grass", 30), 0)

    # Roads and rivers (h3m and hommoe sources): the h3m format stores
    # the road/river type per tile and an Olden Era map stores the road
    # bitfield per tile (roadsMap) plus the river node lists; the
    # directions are derived from the neighboring tiles and encoded as
    # the fheroes2 bitfield (TOP_LEFT=1, TOP=2, TOP_RIGHT=4, RIGHT=8,
    # BOTTOM_RIGHT=16, BOTTOM=32, BOTTOM_LEFT=64, LEFT=128).
    road_tiles = {}
    road_props_tiles = {}
    road_index_tiles = {}
    river_tiles = {}
    is_hommoe_source = unified.get("sourceGame") == "hommoe"
    if is_h3m_source or is_hommoe_source:
        _h3m_direction_bits = [(-1, -1, 1), (0, -1, 2), (1, -1, 4),
                                (1, 0, 8), (1, 1, 16), (0, 1, 32),
                                (-1, 1, 64), (-1, 0, 128)]
        for level in unified.get("terrain", {}).get("levels", []):
            for cell in level.get("grid", []):
                if cell.get("z", 0) != 0:
                    continue
                pos = (cell.get("x", 0), cell.get("y", 0))
                if is_hommoe_source:
                    # An Olden Era map carries the original road bitfield
                    # per tile (roadsMap): restore it exactly.
                    if cell.get("sourceRoadIndex"):
                        road_tiles[pos] = "Dirt"
                        road_index_tiles[pos] = cell.get("sourceRoadIndex")
                else:
                    if cell.get("sourceRoad") and cell.get("sourceRoad") != "None":
                        road_tiles[pos] = cell.get("sourceRoad")
                        road_props_tiles[pos] = cell.get("sourceRoadProperties", 0)
                        if cell.get("sourceRoadIndex") is not None:
                            road_index_tiles[pos] = cell.get("sourceRoadIndex")
                    if cell.get("sourceRiver") and cell.get("sourceRiver") != "None":
                        river_tiles[pos] = cell.get("sourceRiver")
        if is_hommoe_source:
            # Olden Era rivers are node lists; mark the river tiles so the
            # STREAMS bitfield is derived from the neighbors below.
            for river in (objects_section.get("sourceRivers") or []):
                for node in river.get("nodes") or []:
                    n = node.get("n")
                    if n is not None and width:
                        river_tiles[(int(n) % width, int(n) // width)] = "Clear"

        def _direction_bitfield(present_set, x, y):
            bits = 0
            for dx, dy, bit in _h3m_direction_bits:
                if (x + dx, y + dy) in present_set:
                    bits |= bit
            return bits

        next_road_id = 100000
        for (x, y) in road_tiles:
            if road_index_tiles:
                # An h3m produced by this converter from an fh2m map
                # carries the original road indices: restore them
                # exactly and drop the corner fills/stubs the
                # fh2m -> h3m step added to the road graph.
                if (x, y) not in road_index_tiles:
                    continue
                bits = road_index_tiles[(x, y)]
            else:
                bits = _direction_bitfield(road_tiles, x, y)
                if road_props_tiles.get((x, y), 0) < 6:
                    # A diagonal road piece (ends 0x00-0x01, bands
                    # 0x02-0x05): the road continues through the tile
                    # corners, so the diagonal neighbors carry
                    # continuation bits too.
                    for dx, dy, bit in _h3m_direction_bits:
                        if bit in (1, 4, 16, 64) and (x + dx, y + dy) in road_tiles:
                            bits |= bit
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
    # fh2m map), it is kept as is. Missing ones are only generated for
    # h3m sources, so an fh2m source round-trips its own heroes - or
    # their absence - faithfully.
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
    for detail in (unified.get("playerDetails", [])
                   if is_h3m_source else []):
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


# unified terrain -> Olden Era tilesMap id (reverse of HOMMOE_TILE_TERRAINS).
# Water is emitted as tilesMap 2 (sand basin) + waterMap 7, the game's own
# convention for ocean/lake tiles (see the references' terrain-map.ts).
UNIFIED_TO_HOMMOE_TILE = {
    "Grass": 1, "Desert": 2, "Wasteland": 3, "Snow": 4,
    "Swamp": 5, "Lava": 6, "Dirt": 7, "Water": 2, "Rock": 7,
    "Subterranean": 7, "Beach": 2,
}
HOMMOE_WATER_TILE = 2
HOMMOE_WATER_ID = 7  # "Water (Grass)"

# unified object group -> Olden Era sid, for objects that carry no
# sourceSid (h2/h3 sources). Values observed on real maps; the fine-grained
# choice (which mine/artifact/dwelling sid) needs the game's Core.zip
# catalog and is out of scope here.
HOMMOE_GROUP_TO_SID = {
    "KINGDOM_TOWNS": "city-spawner",
    "KINGDOM_HEROES": "hero-spawner",
    "ADVENTURE_MINES": "mine_gold",
    "ADVENTURE_TREASURES": "chest",
    "ADVENTURE_DWELLINGS": "barracks_neutral_1",
    "MONSTERS": "random-squad",
    "ADVENTURE_MISCELLANEOUS": "windmill",
    "MAP_EXTRAS": "Zone 3x3",
}

# H2/H3 resource names -> Olden Era resource sids (BASIC_RESOURCE_IDS in
# the references' src/lib/resources.ts)
UNIFIED_TO_HOMMOE_RESOURCE = {
    "wood": "wood", "mercury": "mercury", "ore": "ore", "sulfur": "dust",
    "crystal": "crystals", "gems": "gemstones", "gold": "gold",
}
# reverse of UNIFIED_TO_HOMMOE_RESOURCE (OE resource sid -> unified name)
HOMMOE_TO_UNIFIED_RESOURCE = {v: k for k, v in UNIFIED_TO_HOMMOE_RESOURCE.items()}

# h3m classes dropped by decision when writing OE: OE has no message-bearer
# object for them. 91 Sign (user decision), 59 Ocean Bottle (dropped with
# the water-travel group, decision log in not_converted_yet.english.txt).
# Their signMetadata message stays in the unified JSON but no OE object or
# quest is emitted for them.
HOMMOE_DROPPED_MESSAGE_CLASSES = {59, 91}

# unified victory label -> typeWinCondition (reverse of HOMMOE_WIN_CONDITIONS)
UNIFIED_TO_HOMMOE_WIN = {
    "defeatEveryone": 0, "captureTown": 8, "killHero": 4,
}

# H3 random-artifact object classes -> OE ERarity bin (numeric rarity in
# propRandomItems rows). User mapping: Treasure <-> Common (0),
# Minor <-> Rare (1), Major <-> Epic (2), Relic <-> Legendary (3).
# Class 65 "any" gets no row: the game default (rarity 0) applies.
HOMMOE_RANDOM_ARTIFACT_RARITY = {66: 0, 67: 1, 68: 2, 69: 3}
# H3 artifact rarity class (H3M_ARTIFACT_CLASSES, 1-4) -> OE ERarity bin,
# used for specific artifacts with no exact OE match (random-item fallback).
HOMMOE_ARTIFACT_CLASS_RARITY = {1: 0, 2: 1, 3: 2, 4: 3}
# reverse: OE ERarity bin -> H3 random-artifact object class
HOMMOE_RARITY_TO_RANDOM_ARTIFACT_CLASS = {0: 66, 1: 67, 2: 68, 3: 69}

HOMMOE_DEFAULT_VERSION = "0.72.30"

# Default adventure.settings for H2/H3 -> .map outputs: the key set and
# values are copied from the reference's bundled template.map
# (src-tauri/resources/template.map); the writer fills in mapWinConditions
# from the unified victory condition and the difficulty arrays are all-true
# (FULL_DIFFICULTIES in map-write.ts: every real sample map has them
# populated, the template ships them empty).
HOMMOE_SETTINGS_DEFAULT = OrderedDict([
    ("heroCountMin", 5), ("heroCountMax", 10), ("heroCountIncrement", 1),
    ("enableHeroHireBan", False), ("enableCustomHeroMaxLevel", False),
    ("customHeroMaxLevel", -1), ("disableAutoBattleAgainstEnemyHeroes", False),
    ("disableWeekEffect", False), ("disableFactionLaws", False),
    ("disableMagicGuild", False), ("disableMagicCustomLearning", False),
    ("cantRewriteTurnMode", False),
    ("idSidesWithoutTimer", []), ("idSidesWithoutNotification", []),
    ("idSidesWithoutCameraFollowing", []), ("isTournamentRules", True),
    ("bonuses", []),
    ("gameMode", 0), ("endController", 0), ("isScenario", False),
    ("economicDifficulties", [True] * 6), ("aiDifficulties", [True] * 6),
    ("neutralDifficulties", [True] * 6), ("quickStartDifficulties", [True] * 6),
    ("enableCustomAI", False), ("customAISid", ""),
    ("factionLawsExpModifier", 1.0), ("astrologyExpModifier", 1.0),
])


# h3 eventMetadata primary-skill names -> OE GiveStatsHero stat names
# (shapes measured on real quests: p = [stat, heroSid, value]; blank hero
# sid = the currently selected / visiting hero).
_H3_TO_OE_STAT_NAME = {
    "attack": "offence", "defense": "defence",
    "spellPower": "spellPower", "knowledge": "intelligence",
}


def _hommoe_event_actions(event, obj_id):
    """Build OE script actions for an H2/H3 event object's metadata.

    Every reward type the unified eventMetadata carries becomes a real
    quest action (shapes measured on the game's own quest scripts):
    message -> Print, resources -> GiveRes, experience -> GiveExpHero,
    primary skills / morale / luck -> GiveStatsHero, mana ->
    ChangeManaHero, artifact -> GiveItemHero (exact sid, else random of
    the same rarity bin), monster -> GiveUnitHero, secondary skill ->
    AddSkillAll, spells -> AddSpellHero, removeAfterVisit ->
    DeleteEntity on the event entity. Only ids with no OE sid at all end
    up in `unconverted` (and then only in the trigger comment).
    """
    actions = []
    unconverted = []
    message = event.get("message") or ""
    if message:
        # Messages decoded from native OE Dialog actions carry a
        # "dialog:<sid>" marker; emit them back as DialogOne actions so the
        # Core.zip flow reference survives. Plain h2/h3 text stays Print -
        # the only self-contained text channel in a .map (Dialog sids are
        # resolved from the game's Core.zip, not from the map file).
        lines = [ln for ln in str(message).split("\n") if ln]
        if any(ln.startswith("dialog:") for ln in lines):
            for ln in lines:
                if ln.startswith("dialog:"):
                    actions.append(OrderedDict([
                        ("comment", ""), ("p", [ln[7:]]), ("a", "DialogOne"),
                    ]))
                else:
                    actions.append(OrderedDict([
                        ("comment", ""), ("p", [ln]), ("a", "Print"),
                    ]))
        else:
            actions.append(OrderedDict([("comment", ""), ("p", [message]), ("a", "Print")]))
    resources = event.get("resources") or {}
    for name, value in resources.items():
        oe_res = UNIFIED_TO_HOMMOE_RESOURCE.get(name)
        if oe_res and value:
            actions.append(OrderedDict([
                ("comment", ""), ("p", [oe_res, str(value)]), ("a", "GiveRes"),
            ]))
    if event.get("experience"):
        actions.append(OrderedDict([
            ("comment", ""), ("p", [str(event.get("experience")), ""]), ("a", "GiveExpHero"),
        ]))
    primaries = event.get("primarySkills") or {}
    for h3_name, oe_name in _H3_TO_OE_STAT_NAME.items():
        value = primaries.get(h3_name) or event.get(h3_name)
        if value:
            actions.append(OrderedDict([
                ("comment", ""), ("p", [oe_name, "", str(value)]), ("a", "GiveStatsHero"),
            ]))
    for field, oe_name in (("morale", "moral"), ("luck", "luck")):
        if event.get(field):
            actions.append(OrderedDict([
                ("comment", ""), ("p", [oe_name, "", str(event.get(field))]), ("a", "GiveStatsHero"),
            ]))
    if event.get("mana"):
        actions.append(OrderedDict([
            ("comment", ""), ("p", ["", str(event.get("mana"))]), ("a", "ChangeManaHero"),
        ]))
    if event.get("artifact") not in (None, 0, -1):
        # exact Core.zip name match, else a random OE artifact sid of the
        # same rarity bin (user decision: artifacts random is good)
        art_sid = _hommoe_artifact_sid(event.get("artifact"))
        if art_sid:
            # blank hero sid = the currently selected (visiting) hero
            actions.append(OrderedDict([
                ("comment", "h3 artifact {}".format(event.get("artifact"))),
                ("p", [art_sid, ""]), ("a", "GiveItemHero"),
            ]))
        else:
            unconverted.append("artifact={}".format(event.get("artifact")))
    if event.get("monsterType") not in (None, 0, -1):
        unit_sid = OE_CREATURE_EQUIVALENTS.get(str(event.get("monsterType")))
        if unit_sid:
            actions.append(OrderedDict([
                ("comment", "h3 creature {}".format(event.get("monsterType"))),
                ("p", [unit_sid, str(event.get("monsterCount", 0)), ""]), ("a", "GiveUnitHero"),
            ]))
        else:
            unconverted.append("monster={}x{}".format(event.get("monsterType"), event.get("monsterCount", 0)))
    if event.get("secondarySkill") not in (None, 0):
        # exact name match, else a random convertible OE skill sid (user
        # decision: unmapped skills convert randomly, skill_faction_* never)
        skill_sid = _oe_skill_sid(event.get("secondarySkill"))
        if skill_sid:
            actions.append(OrderedDict([
                ("comment", "level {}".format(event.get("secondarySkillLevel", 0))),
                ("p", [skill_sid]), ("a", "AddSkillAll"),
            ]))
        else:
            unconverted.append("skill={}/{}".format(event.get("secondarySkill"), event.get("secondarySkillLevel", 0)))
    for sp in event.get("spells") or []:
        # Spell reward: exact OE sid for the 11 name matches, else a random
        # OE spell of the same rank (user decision - spells are not 1:1).
        # The original h3 spell id rides in the action comment.
        if isinstance(sp, int) and 0 <= sp < len(H3M_SPELL_LEVELS):
            sp_sid = _hommoe_spell_sid(sp)
            if sp_sid:
                # blank hero sid = the currently selected (visiting) hero
                actions.append(OrderedDict([
                    ("comment", "h3 spell {}".format(sp)),
                    ("p", [sp_sid, ""]), ("a", "AddSpellHero"),
                ]))
            else:
                unconverted.append("spell={}".format(sp))
    if event.get("removeAfterVisit") and obj_id is not None:
        actions.append(OrderedDict([
            ("comment", ""), ("p", ["event_{}".format(obj_id)]), ("a", "DeleteEntity"),
        ]))
    return actions, unconverted


def _hommoe_generate_scripts(unified, width):
    """Generate the commentAiData scripting block for h2/h3-sourced maps.

    Converts the unified event patterns into Olden Era quest triggers:
    - H2 adventureMapEventMetadata / H3 eventMetadata objects -> a quest
      trigger with an ObjectInteractionAfter condition on the object's
      entity plus Print/GiveRes actions (repeat = isRecurringEvent)
    - H2 dailyEvents -> StartTurn condition (week/day from
      firstOccurrenceDay) + GiveRes actions
    """
    objects = unified.get("objects") or {}
    tiles = objects.get("tiles") or {}
    event_meta = {}
    for key in ("adventureMapEventMetadata", "eventMetadata"):
        for oid, entry in (objects.get(key) or {}).items():
            event_meta[int(oid)] = entry

    obj_by_id = {}
    for tile_key, obj_list in tiles.items():
        for obj in obj_list:
            if obj.get("id") is not None:
                obj_by_id[obj["id"]] = (tile_key, obj)

    quests = []
    prop_entities = []

    for oid, event in sorted(event_meta.items()):
        if oid not in obj_by_id:
            continue
        entity_sid = "event_{}".format(oid)
        prop_entities.append(OrderedDict([("type", 0), ("id", oid), ("sid", entity_sid)]))
        actions, unconverted = _hommoe_event_actions(event, oid)
        trigger = OrderedDict([
            ("comment", "converted event (unconverted without OE sids: {})".format(", ".join(unconverted)) if unconverted else ""),
            ("repeat", bool(event.get("isRecurringEvent", False))),
            ("conditions", [OrderedDict([
                ("comment", ""),
                ("p", [entity_sid, ""]),
                ("counter", 1),
                ("c", "ObjectInteractionAfter"),
            ])]),
            ("actions", actions),
            ("conditionsLogic", "And"),
        ])
        quests.append(OrderedDict([
            ("sid", "event_{}".format(oid)),
            ("activeOnStart", True),
            ("comment", "converted H2/H3 event object {}".format(oid)),
            ("main", False),
            ("hidden", True),
            ("name", ""),
            ("desc", ""),
            ("sharing", "Clone"),
            ("subQuests", [OrderedDict([
                ("sid", "1"), ("activeOnStart", True), ("hidden", False),
                ("name", ""), ("desc", ""), ("comment", ""),
                ("triggers", [trigger]),
            ])]),
        ]))

    for index, daily in enumerate(unified.get("dailyEvents") or []):
        day = int(daily.get("firstOccurrenceDay", 1))
        week = str((day - 1) // 7 + 1)
        day_of_week = str((day - 1) % 7 + 1)
        # same reward actions as ground events (daily events share the
        # eventMetadata shape for message/resources/primaries)
        actions, daily_unconverted = _hommoe_event_actions(daily, None)
        quests.append(OrderedDict([
            ("sid", "daily_event_{}".format(index)),
            ("activeOnStart", True),
            ("comment", "converted H2 daily event {}".format(index)),
            ("main", False),
            ("hidden", True),
            ("name", ""),
            ("desc", ""),
            ("sharing", "Clone"),
            ("subQuests", [OrderedDict([
                ("sid", "1"), ("activeOnStart", True), ("hidden", False),
                ("name", ""), ("desc", ""), ("comment", ""),
                ("triggers", [OrderedDict([
                    ("comment", ""),
                    ("repeat", int(daily.get("repeatPeriodInDays", 0)) > 0),
                    ("conditions", [OrderedDict([
                        ("comment", ""),
                        ("p", [week, day_of_week]),
                        ("counter", 1),
                        ("c", "StartTurn"),
                    ])]),
                    ("actions", actions),
                    ("conditionsLogic", "And"),
                ])]),
            ])]),
        ]))

    scripting = OrderedDict([
        ("comment", ""),
        ("aiRolesId", ""),
        ("counters", []),
        ("interruptions", []),
        ("quests", quests),
    ])
    return scripting, prop_entities


def _hommoe_town_race(obj, objects):
    """Race name of a unified KINGDOM_TOWNS object: fh2m keeps it in
    castleMetadata.raceName, h3m in townMetadata.type / class 98 subtype,
    fh2m objects via the town index (race * 2 [+ 1])."""
    from correspondence import FH2M_TOWN_RACE_ORDER, H3M_TOWN_TYPE_TO_FH2M_RACE
    oid = str(obj.get("id"))
    meta = (objects.get("castleMetadata") or {}).get(oid) or {}
    race = meta.get("raceName")
    if not race:
        tm = (objects.get("townMetadata") or {}).get(oid) or {}
        tt = tm.get("type")
        if tt is None and obj.get("class") == 98:
            tt = obj.get("subclass")
        if tt is not None:
            race = H3M_TOWN_TYPE_TO_FH2M_RACE.get(tt)
    if not race and obj.get("class") is None and obj.get("index") is not None:
        # fh2m town object: index = race * 2 (+1 village); 12/13 are the
        # random-town indices (h3m class 77), which carry no race
        idx = int(obj["index"]) // 2
        if 0 <= idx < len(FH2M_TOWN_RACE_ORDER):
            race = FH2M_TOWN_RACE_ORDER[idx]
    return race


def _hommoe_faction_sid(detail):
    """Unified playerDetails[] entry -> Olden Era spawn factionSid.

    A hommoe source keeps the raw sid in sourceRace; other sources go
    through the Races table mapping (sourceRace first, it preserves the
    h3-only Inferno/Fortress/Conflux values, then the normalized race).
    """
    source_race = detail.get("sourceRace")
    if source_race in HOMMOE_FACTION_NAMES:
        return source_race
    race = detail.get("race") or "Random"
    return UNIFIED_TO_HOMMOE_FACTION_SID.get(source_race or "",
                                              UNIFIED_TO_HOMMOE_FACTION_SID.get(race, ""))


def unified_to_hommoe(unified):
    """
    Convert a map in the unified format into the JSON structure expected by
    hommoedecoder.write_hommoe (parse_hommoe format).

    Args:
        unified: Dictionary in the unified format.

    Returns:
        OrderedDict: The map in the hommoe (Olden Era) detailed format.
    """
    width = int(unified.get("mapSize", {}).get("width", 0))
    height = int(unified.get("mapSize", {}).get("height", width))
    # OE maps must be sector-aligned: sizeX_/sizeZ_ are multiples of 16 and
    # views[0].secSizeX/Z = size // 16 (reference translator's
    # align_to_sector / validate_map.py: "map dimensions must be
    # sector-aligned (16)"). A non-aligned h2/h3 size (36/72/108...) makes
    # the game's Map.pmd -> byu.pxp(a, b, MapViewData[]) index out of range
    # at map load (IndexOutOfRangeException). Pad the atlas to the next
    # 16 boundary; padding cells become elevated dirt (tile 7, levelsMap 1,
    # climbs 0) so they are unpathable, like underground rock - the
    # reference's paint_envelope_padding_elevated_dirt policy. hommoe
    # sources pass through raw and are already aligned.
    src_width, src_height = width, height
    if unified.get("sourceGame") != "hommoe" and width and height:
        width = -(-width // 16) * 16
        height = -(-height // 16) * 16
    name = unified.get("name", "") or "converted map"
    description = unified.get("description", "")

    # The container header hash / block 1 hashSum is an opaque per-map
    # identity, NOT a content checksum: the reference brute-forced
    # md5/sha1/sha256/sha512 over block combinations with no match, and
    # resaving an unchanged map through GME mints a NEW hash - a fixed
    # cloned value makes maps collide and the game silently refuses to
    # recognize them (map-write.ts:2518-2545). So mint a fresh random
    # 32-hex per output map, exactly like the reference's generateMapHash()
    # (crypto.randomUUID without dashes); hashSum below is set equal to it.
    # .map -> .map stays byte-exact regardless via the raw passthrough.
    header_hash = _uuid.uuid4().hex

    # --- block 1: scenario ---
    player_details = unified.get("playerDetails") or []
    players = unified.get("players") or {}
    human_colors = players.get("humanColors") or []
    computer_colors = players.get("computerColors") or []
    available_colors = players.get("availableColors") or []
    spawns = []
    # --- player start resolution for h2/h3 sources ---
    # fh2m stores town ownership on the flag objects (castleMetadata
    # ownerColor); h3m stores the main town in playerDetails. Mirror the
    # h3m writer's fallback: an active player with an owned town gets it
    # as main town (OE spawnPointType 0 / city-spawner + propSpawns /
    # propCities rows, otherwise the game logs "Can not find objects of
    # type: City" at load); a player without a town gets a hero start
    # (spawnPointType 1 / hero-spawner + propSpawns / propHeroes). The
    # owned town's race also resolves a Random/Unknown player race to a
    # real factionSid (otherwise the game shows "random faction").
    _objs0 = unified.get("objects") or {}
    _castle_meta = _objs0.get("castleMetadata") or {}
    _town_obj_by_tile = {}
    for _tk, _ol in (_objs0.get("tiles") or {}).items():
        for _o in _ol:
            if _o.get("group") == "KINGDOM_TOWNS":
                _town_obj_by_tile[_tk] = _o
    town_owner_tile = {}   # h3m-aliased color -> tile_key of owned town
    color_race = {}        # h3m-aliased color -> race name of owned town
    for _oid, _meta in _castle_meta.items():
        _oc = _meta.get("ownerColor")
        if not _oc:
            continue
        for _tk, _o in _town_obj_by_tile.items():
            if str(_o.get("id")) == str(_oid):
                if _oc not in town_owner_tile:
                    town_owner_tile[_oc] = _tk
                _rn = _meta.get("raceName") or _hommoe_town_race(_o, _objs0)
                if _rn:
                    color_race.setdefault(_oc, _rn)
                break
    main_town_tile = {}    # tile_key -> (owner, spawnType, factionSid)
    for detail in player_details:
        mt = detail.get("mainTown")
        if not mt:
            continue
        _c = detail.get("color")
        _z = int(mt.get("z", 0) or 0)
        for _cand in ("%d_%d_%d" % (int(mt.get("x", 0)), int(mt.get("y", 0)), _z),
                      "%d_%d_%d" % (int(mt.get("x", 0)) + 2, int(mt.get("y", 0)), _z)):
            _o = _town_obj_by_tile.get(_cand)
            if _o is not None:
                main_town_tile[_cand] = None  # filled in the spawn loop below
                if _c not in color_race:
                    _rn = _hommoe_town_race(_o, _objs0)
                    if _rn:
                        color_race[_c] = _rn
                break
    hero_start_queue = []  # (owner, spawnType, detail) in spawn order

    color_owner = {}
    for detail in player_details:
        color = detail.get("color")
        # Only real players get a block 1 spawn entry: the game counts every
        # spawns[] entry as a player slot, so empty H2/H3 player slots must
        # not be written (real .map files only ever carry spawnType 0/1;
        # see the reference's h3-import/ownership.ts, which maps canHuman to
        # spawnType 0/1 for actual players only).
        if color not in human_colors and color not in computer_colors \
                and color not in available_colors and not detail.get("available"):
            continue
        human = color in human_colors
        available = color in available_colors
        # Real OE maps carry the player's colorId (index into
        # HOMMOE_PLAYER_COLORS); write it so the reverse conversion maps the
        # spawn back to the original H2/H3 color (fh2m "Yellow" aliases to
        # H3 "Tan", see FH2M_TO_H3M_COLOR_ALIAS). -1 when unknown.
        oe_color = FH2M_TO_H3M_COLOR_ALIAS.get(color, color)
        color_id = HOMMOE_PLAYER_COLORS.index(oe_color) \
            if oe_color in HOMMOE_PLAYER_COLORS else -1
        spawn_type = 0 if human else (1 if available else 2)
        # main town: explicit (h3m) or the first owned town (fh2m flags)
        owner = len(spawns) + 1
        mt_tile = town_owner_tile.get(color)
        if detail.get("mainTown"):
            _z = int(detail["mainTown"].get("z", 0) or 0)
            for _cand in ("%d_%d_%d" % (int(detail["mainTown"].get("x", 0)),
                                        int(detail["mainTown"].get("y", 0)), _z),
                          "%d_%d_%d" % (int(detail["mainTown"].get("x", 0)) + 2,
                                        int(detail["mainTown"].get("y", 0)), _z)):
                if _cand in main_town_tile or _cand in _town_obj_by_tile:
                    mt_tile = _cand
                    break
        has_town = mt_tile is not None
        faction_sid = _hommoe_faction_sid(detail)
        if not faction_sid and color in color_race:
            faction_sid = UNIFIED_TO_HOMMOE_FACTION_SID.get(color_race[color], "")
        if has_town:
            main_town_tile[mt_tile] = (owner, spawn_type, faction_sid)
        spawn = OrderedDict([
            ("owner", owner),
            ("spawnType", spawn_type),
            ("playerId", ""),
            ("spawnPointType", 0 if has_town else 1),
            ("isCityDefined", has_town),
            ("factionSid", faction_sid),
            ("isHeroDefined", bool(detail.get("sourceHeroSid"))),
            ("heroSid", detail.get("sourceHeroSid", "")),
            ("colorId", color_id),
            ("isAlive", True),
            ("isLocked", False),
        ])
        spawns.append(spawn)
        color_owner[color] = owner
        if not has_town:
            hero_start_queue.append((owner, spawn_type, detail))
    scenario = OrderedDict([
        ("title", name),
        ("template", ""),
        ("gameMode", 0),
        ("endController", (unified.get("victoryCondition") or {}).get("sourceEndController", 0)),
        ("desc", description),
        ("displayWinCondition", ""),
        ("hashSum", header_hash),
        ("nameFromLocalization", False),
        ("descFromLocalization", False),
        ("sizeX", width),
        ("sizeZ", height),
        ("spawns", OrderedDict([
            ("playersCount", len(spawns)),
            ("spawns", spawns),
            ("takenHeroes", []),
        ])),
        ("startSettings", unified.get("sourceStartSettings") or OrderedDict([
            ("RandomSeed", 0), ("MapSpeed", 0), ("BattleSpeed", 0),
            ("EconomicDifficulty", 0), ("NeutralsDifficulty", 0), ("AiDifficulty", 1),
            ("RestartPoints", 0), ("TurnMode", 2),
        ])),
        ("banInfoData", unified.get("sourceBanInfoData") or OrderedDict([
            ("bannedMagics", []), ("bannedItems", []), ("bannedSkills", []),
            ("bannedHeroes", []), ("bannedUnits", []),
        ])),
        ("daysInGame", 0),
        ("isAutoSave", False),
        ("currentTurnMode", 0),
        ("gameVersion", ""),
        ("isScenario", False),
    ])
    if unified.get("sourceGame") == "hommoe":
        # Lossless passthrough of the raw source fields (AGENTS.md): merge
        # the scenario keys with no unified equivalent and re-emit the
        # original spawns block verbatim (isLocked / colorId / playerId /
        # takenHeroes are kept exactly - 5c).
        for k, v in (unified.get("sourceScenarioExtra") or {}).items():
            scenario[k] = v  # override the base placeholders (gameMode, ...)
        raw_spawns = unified.get("sourceSpawnsRaw")
        if isinstance(raw_spawns, dict) and raw_spawns.get("spawns") is not None:
            scenario["spawns"] = raw_spawns
    else:
        # H2/H3 source: emit the reference template's key set (its
        # buildBlankMap spreads src-tauri/resources/template.map); the
        # difficulty arrays are all-true per FULL_DIFFICULTIES (every real
        # sample map has them populated, the template ships them empty).
        scenario["economicDifficulties"] = [True] * 6
        scenario["aiDifficulties"] = [True] * 6
        scenario["neutralDifficulties"] = [True] * 6
        scenario["quickStartDifficulties"] = [True] * 6
        scenario["campaignInfo"] = OrderedDict([
            ("missionNameSid", ""), ("missionDescSid", ""),
            ("campaignSid", ""), ("campaignDescSid", ""),
            ("hubIconSid", ""), ("missionIconSid", ""),
        ])
        scenario["dateTime"] = OrderedDict([("value", 134321555864529128)])

    # --- block 2: adventure ---
    levels = (unified.get("terrain") or {}).get("levels") or []
    grid = (levels[0] if levels else {}).get("grid") or []
    total = width * height
    tiles_map = [1] * total
    water_map = [0] * total
    levels_map = [0] * total
    climbs_map = [0] * total
    roads_map = [0] * total
    for cell in grid:
        x, y = int(cell.get("x", 0)), int(cell.get("y", 0))
        if 0 <= x < width and 0 <= y < height:
            index = y * width + x
            terrain = cell.get("terrain", "Grass")
            tiles_map[index] = UNIFIED_TO_HOMMOE_TILE.get(terrain, 1)
            if terrain == "Water":
                water_map[index] = HOMMOE_WATER_ID
                # OE renders water only in a lowered basin: every water
                # tile of the reference maps has levelsMap -1 (a water
                # tile at level 0 shows no water in game).
                levels_map[index] = -1
            if cell.get("sourceLevel") is not None and terrain != "Water":
                levels_map[index] = int(cell["sourceLevel"])
            if cell.get("sourceClimb") is not None:
                climbs_map[index] = int(cell["sourceClimb"])
            if unified.get("sourceGame") == "hommoe":
                # hommoe source: sourceRoadIndex is already the OE road
                # type id (0 none / 1 dirt / 2 stone) - keep it verbatim
                if cell.get("sourceRoadIndex"):
                    roads_map[index] = int(cell["sourceRoadIndex"])
            else:
                # h3m/fh2m source: roadsMap must hold the OE road TYPE id
                # (0/1/2), not the h3m/fh2m connection bitfield - the
                # game's minimap/thumbnail renderer (MapData.por) indexes
                # a road LUT with it and crashes on bitfield values
                road_name = cell.get("sourceRoad")
                if road_name and road_name != "None":
                    roads_map[index] = 2 if road_name == "Cobblestone" else 1
                elif cell.get("sourceRoadIndex"):
                    roads_map[index] = 1
    if width != src_width or height != src_height:
        # atlas padding (cells right/below the source rectangle): elevated
        # dirt with no water/road/climb - unpathable like underground rock
        padding_tile = UNIFIED_TO_HOMMOE_TILE.get("Dirt", 7)
        for y in range(height):
            for x in range(width):
                if x < src_width and y < src_height:
                    continue
                index = y * width + x
                tiles_map[index] = padding_tile
                levels_map[index] = 1
                climbs_map[index] = 0
                water_map[index] = 0
                roads_map[index] = 0
    terrain_by_pos = {}
    for cell in grid:
        terrain_by_pos[(int(cell.get("x", 0)), int(cell.get("y", 0)))] = \
            cell.get("terrain", "Grass")

    del HOMMOE_UNMAPPED_OBJECTS[:]
    del HOMMOE_BATTLEFIELD_PAINTED[:]
    del HOMMOE_RANDOM_DWELLINGS[:]
    objects = unified.get("objects") or {}
    groups = {}
    order = []
    squads_out = []
    markers_out = []
    prop_rows = {}
    next_free = 1
    for tile_key, obj_list in (objects.get("tiles") or {}).items():
        for obj in obj_list:
            oid = obj.get("id")
            if oid is None:
                oid = next_free
            next_free = max(next_free, int(oid) + 1)
            group = obj.get("group")
            sid = obj.get("sourceSid")
            ref = None
            if not sid:
                if group in ("ROADS", "STREAMS"):
                    # Roads and rivers are stored in the terrain layer
                    # (roadsMap / rivers node lists built above), not as
                    # Olden Era objects.
                    continue
                if group == "KINGDOM_TOWNS":
                    # OE towns are spawn-linked city-spawners: the game
                    # resolves a spawnPointType-0 start through
                    # propSpawns.owner -> the city-spawner object ->
                    # propCities, and logs "Can not find objects of type:
                    # City" when those rows are missing.
                    sid = "city-spawner"
                    mt = main_town_tile.get(tile_key)
                    race = _hommoe_town_race(obj, objects)
                    town_faction = UNIFIED_TO_HOMMOE_FACTION_SID.get(race, "") if race else ""
                    if mt is not None:
                        _owner, _spawn_type, _spawn_faction = mt
                        faction = _spawn_faction or town_faction
                        is_defined = bool(faction)
                        prop_rows.setdefault("propSpawns", []).append(OrderedDict([
                            ("type", 0), ("id", oid), ("owner", _owner),
                            ("spawnType", _spawn_type), ("spawnPointType", 0),
                            ("isLocked", False),
                        ]))
                        prop_rows.setdefault("propCities", []).append(OrderedDict([
                            ("type", 0), ("id", oid),
                            ("isDefined", is_defined), ("factionSid", faction),
                            # an isDefined city with spawnHero but no real
                            # propHeroes row crashes at load; an unconfigured
                            # city (isDefined false) with spawnHero and no row
                            # is the confirmed-safe GME default
                            ("spawnHero", not is_defined),
                            ("buildingsConstructionSid", "default_buildings_construction"),
                            ("buildingsBanSid", "default_buildings_ban"),
                            ("buildingsSettingsSid", "default_buildings_settings"),
                            ("customCityName", ""),
                        ]))
                        prop_rows.setdefault("propGrowthUnits", []).append(OrderedDict([
                            ("type", 0), ("id", oid),
                            ("isConstantGrowth", True), ("countGrowth", 1),
                        ]))
                        # every real city-spawner carries a guard squad row
                        prop_rows.setdefault("propRandomSquads", []).append(OrderedDict([
                            ("type", 0), ("id", oid), ("sids", []),
                            ("requestedValue", 0.0), ("fraction", ""),
                            ("tier", 0), ("isMainGuard", False),
                            ("reactionType", 2), ("customTopUnit", ""),
                            ("weeklyIncrementBonus", 0.0),
                            ("diplomacyUnitsCountBonus", 0.0),
                            ("isEscape", True), ("isAutobatle", True),
                            ("isFreeDiplomacy", False),
                            ("isCampaignFreeDiplomacy", False),
                            ("isCampaignDiplomacy", False),
                            ("isIgnoreMultiply", False), ("obstruction", ""),
                            ("customStacks", 0),
                        ]))
                    else:
                        # neutral / non-start town: unconfigured city-spawner
                        # plus ownership when the h2 flags gave an owner
                        prop_rows.setdefault("propCities", []).append(OrderedDict([
                            ("type", 0), ("id", oid), ("isDefined", False),
                            ("factionSid", ""), ("spawnHero", False),
                            ("customCityName", ""),
                        ]))
                        _own = (objects.get("castleMetadata") or {}).get(str(oid)) or {}
                        _oc = _own.get("ownerColor")
                        if _oc in color_owner:
                            prop_rows.setdefault("propOwners", []).append(OrderedDict([
                                ("type", 0), ("id", oid), ("owner", color_owner[_oc]),
                            ]))
                        else:
                            prop_rows.setdefault("propOwners", []).append(OrderedDict([
                                ("type", 0), ("id", oid),
                            ]))
                elif group == "KINGDOM_HEROES":
                    # hero-spawner for each player without a town start;
                    # extra placed heroes become random-hero spawners
                    if hero_start_queue:
                        _owner, _spawn_type, _hdetail = hero_start_queue.pop(0)
                        _hsid = _hdetail.get("sourceHeroSid") or "random"
                        sid = "hero-spawner"
                        prop_rows.setdefault("propSpawns", []).append(OrderedDict([
                            ("type", 0), ("id", oid), ("owner", _owner),
                            ("spawnType", _spawn_type), ("spawnPointType", 1),
                            ("isLocked", False),
                        ]))
                        prop_rows.setdefault("propHeroes", []).append(OrderedDict([
                            ("type", 0), ("id", oid),
                            ("isDefined", bool(_hdetail.get("sourceHeroSid"))),
                            ("heroSid", _hsid),
                        ]))
                    else:
                        sid = "random-hero"
                        prop_rows.setdefault("propHeroes", []).append(OrderedDict([
                            ("type", 0), ("id", oid),
                            ("isDefined", False), ("heroSid", "random"),
                        ]))
                else:
                    if obj.get("class") in HOMMOE_DROPPED_MESSAGE_CLASSES:
                        # Sign / ocean bottle: dropped by decision - OE has
                        # no message-bearer object for them (the message
                        # stays in the unified signMetadata only).
                        HOMMOE_UNMAPPED_OBJECTS.append(OrderedDict([
                            ("group", group),
                            ("index", obj.get("index")),
                            ("class", obj.get("class")),
                            ("subclass", obj.get("subclass")),
                            ("sprite", obj.get("sprite")),
                            ("tile", tile_key),
                        ]))
                        continue
                    parts = tile_key.split("_")
                    terrain_name = "Grass"
                    if len(parts) == 3:
                        terrain_name = terrain_by_pos.get(
                            (int(parts[0]), int(parts[1])), "Grass")
                    ref = _unified_obj_h3m_ref(obj, terrain_name)
                    if group == "ADVENTURE_ARTIFACTS":
                        # Prefer the exact h3m artifact id kept in the
                        # artifact metadata (hommoe sources) over the
                        # fh2m index, which many h3 artifacts lack.
                        art_meta = (objects.get("artifactMetadata") or {}).get(str(oid)) or {}
                        if art_meta.get("artifact") is not None:
                            ref = (5, int(art_meta["artifact"]), None)
                    if ref is not None:
                        sid = _resolve_hommoe_sid(ref[0], ref[2], ref[1],
                                                  terrain_name)
                    if sid is None and obj.get("class") in HOMMOE_RANDOM_DWELLING_CLASSES:
                        # Random dwelling (216/217/218): resolve to a fixed
                        # barracks_<faction>_<tier> (see 1d-note2b/2d); the
                        # owner rides along as a propOwners row below.
                        sid = _hommoe_random_dwelling_sid(obj, objects)
                    if sid is None:
                        sid = HOMMOE_GROUP_TO_SID.get(group)
                if sid in HOMMOE_REWARD_PARAMS_SIDS \
                        and not (obj.get("properties") or {}).get("propRewardParams"):
                    # altar_of_magic_* / beer_fountain / ...: the game editor always seeds a
                    # propRewardParams row for these sids
                    # (SIDS_WITH_REWARD_PARAMS_ONLY in the reference
                    # map-write.ts); real maps carry it with EMPTY
                    # parameters (Broken_Alliance) - the game draws from
                    # the bank's own school/rank variants. Hommoe-sourced
                    # objects keep their own row via the passthrough.
                    prop_rows.setdefault("propRewardParams", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("parameters", []),
                    ]))
                if group == "ADVENTURE_ARTIFACTS" and sid == "random-item":
                    # No exact OE artifact (or a random-artifact class):
                    # random-item + a propRandomItems row with the right
                    # rarity bin (Treasure/Common=0 .. Relic/Legendary=3).
                    from correspondence import H3M_ARTIFACT_CLASSES
                    h3_class = obj.get("class") if ref is None else ref[0]
                    rarity = HOMMOE_RANDOM_ARTIFACT_RARITY.get(h3_class)
                    if rarity is None and h3_class == 5:
                        art_meta = (objects.get("artifactMetadata") or {}).get(str(oid)) or {}
                        art = art_meta.get("artifact") or obj.get("subclass")
                        cls = H3M_ARTIFACT_CLASSES.get(art)
                        if cls is not None:
                            rarity = HOMMOE_ARTIFACT_CLASS_RARITY.get(cls)
                    if rarity is not None:
                        prop_rows.setdefault("propRandomItems", []).append(OrderedDict([
                            ("type", 0), ("id", oid), ("rarity", rarity),
                        ]))
                if sid == "pandora_box":
                    # Pandora's Box: emit the prop rows (variant, guards,
                    # reward slots, script actions) from the h3m pandora
                    # metadata kept in the unified objects section.
                    pandora_meta = (objects.get("pandoraMetadata") or {}).get(str(oid))
                    if pandora_meta is None:
                        # Scholar (h3 class 81, user mapping -> pandora_box):
                        # convert its reward through the same pandora rules.
                        sch_meta = (objects.get("scholarMetadata") or {}).get(str(oid))
                        if sch_meta is not None:
                            pandora_meta = _hommoe_scholar_to_pandora_meta(sch_meta)
                    if pandora_meta:
                        _hommoe_pandora_props(prop_rows, oid, pandora_meta)
                if sid in HOMMOE_BANK_SIDS:
                    # Bank / variant sid: seed the propVariants +
                    # propRewardParams rows the game editor always adds for
                    # these sids (selectedVar -1 = random logic variant,
                    # empty parameters = the variant's own reward; shapes of
                    # the real rows in Broken_Alliance / c_M1). SoD banks
                    # carry no per-instance guards, so no propSquads is
                    # synthesized here. Witch hut (wise_owl): a fixed h3
                    # skill rides in parameters as a bare OE skill sid.
                    reward_params = []
                    if sid == "wise_owl":
                        wh_meta = (objects.get("witchhutMetadata") or {}).get(str(oid)) or {}
                        skill = wh_meta.get("skill")
                        if skill is not None:
                            # exact name match, else a random convertible OE
                            # skill sid (user decision: unmapped skills
                            # convert randomly, skill_faction_* never)
                            sk_sid = _oe_skill_sid(skill)
                            if sk_sid:
                                reward_params = [sk_sid]
                    prop_rows.setdefault("propVariants", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("selectedVar", -1),
                        ("typeVariant", 0), ("fraction", 0), ("unitVersion", 0),
                    ]))
                    prop_rows.setdefault("propRewardParams", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("parameters", reward_params),
                    ]))
                if not sid:
                    bf_class = obj.get("class")
                    if bf_class in HOMMOE_BATTLEFIELD_CLASS_TO_BIOME:
                        # Battlefield terrain -> repaint the tile's tilesMap
                        # biome (OE battles use the tile biome; there is no
                        # OE object for magical terrain). The reverse
                        # direction yields the plain biome, not the object.
                        bf_biome = HOMMOE_BATTLEFIELD_CLASS_TO_BIOME[bf_class]
                        biome_id = UNIFIED_TO_HOMMOE_TILE.get(bf_biome, 1)
                        try:
                            _bx, _by, _bz = tile_key.split("_")
                            _bidx = int(_by) * width + int(_bx)
                            if 0 <= _bidx < total:
                                tiles_map[_bidx] = biome_id
                        except (ValueError, IndexError):
                            pass
                        HOMMOE_BATTLEFIELD_PAINTED.append(OrderedDict([
                            ("group", group),
                            ("class", bf_class),
                            ("subclass", obj.get("subclass")),
                            ("sprite", obj.get("sprite")),
                            ("tile", tile_key),
                            ("biome", bf_biome),
                            ("biomeId", biome_id),
                        ]))
                        continue
                    # No Olden Era equivalent for this object type.
                    HOMMOE_UNMAPPED_OBJECTS.append(OrderedDict([
                        ("group", group),
                        ("index", obj.get("index")),
                        ("class", obj.get("class")),
                        ("subclass", obj.get("subclass")),
                        ("sprite", obj.get("sprite")),
                        ("tile", tile_key),
                    ]))
                    continue
            # Player link for ownable objects (dwellings, mines, ...): the
            # h3m ownableMetadata owner byte maps to a propOwners row
            # (0-based player index; absent = neutral). Evidence:
            # not_converted_yet.english.txt 1d-note2c/2d. Hommoe-sourced
            # objects already carry their propOwners row in "properties"
            # (passthrough below), so no duplicate row is added.
            own_meta = (objects.get("ownableMetadata") or {}).get(str(oid)) or {}
            if own_meta.get("owner") is not None:
                stored_owner = _hommoe_owner_prop_value(own_meta.get("owner"),
                                                         color_owner)
                if stored_owner is not None \
                        and not (obj.get("properties") or {}).get("propOwners"):
                    prop_rows.setdefault("propOwners", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("owner", stored_owner),
                    ]))
            if obj.get("class") in HOMMOE_RANDOM_DWELLING_CLASSES:
                rd_meta = (objects.get("randomDwellingMetadata") or {}).get(str(oid)) or {}
                stored_owner = _hommoe_owner_prop_value(rd_meta.get("owner"),
                                                         color_owner)
                if stored_owner is not None:
                    prop_rows.setdefault("propOwners", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("owner", stored_owner),
                    ]))
            node = None
            try:
                x, y, _z = tile_key.split("_")
                node = int(y) * width + int(x)
            except (ValueError, IndexError):
                node = 0
            rotation = obj.get("rotation", 0)
            level = obj.get("level", 0)
            if obj.get("group") == "MAP_EXTRAS":
                markers_out.append(OrderedDict([
                    ("node", node), ("id", oid), ("sid", sid), ("v", ""),
                ]))
                continue
            if group == "MONSTERS":
                # Squad properties from the unified monster metadata:
                # fixed monsters -> propSquads with the OE unit sids,
                # random monsters -> propRandomSquads with the tier.
                from correspondence import FH2M_TO_H3M_MONSTERS
                monster_meta = (objects.get("monsterMetadata") or {}).get(str(oid)) or {}
                creature = monster_meta.get("creature")
                if creature is None and obj.get("class") is None:
                    creature = FH2M_TO_H3M_MONSTERS.get((obj.get("index") or 0) + 1)
                monster_class = monster_meta.get("monsterClass")
                if monster_class is None and obj.get("class") in (71, 72, 73, 74, 75):
                    monster_class = obj["class"]
                if monster_class is None and obj.get("class") is None \
                        and 66 <= (obj.get("index") or 0) <= 70:
                    # fh2m random monsters (indices 66-70 = ids 67-71)
                    monster_class = 71 + (obj.get("index") + 1 - 67)
                if monster_class is not None:
                    prop_rows.setdefault("propRandomSquads", []).append(OrderedDict([
                        ("type", 0), ("id", oid), ("sids", []),
                        ("requestedValue", 0.0), ("fraction", ""),
                        ("tier", monster_class - 70),
                        ("isMainGuard", False), ("reactionType", 2),
                        ("customTopUnit", ""), ("weeklyIncrementBonus", 0.0),
                        ("diplomacyUnitsCountBonus", 0.0), ("isEscape", True),
                        ("isAutobatle", True), ("isFreeDiplomacy", False),
                        ("isCampaignFreeDiplomacy", False),
                        ("isCampaignDiplomacy", False),
                        ("isIgnoreMultiply", False), ("obstruction", ""),
                        ("customStacks", 0),
                    ]))
                elif creature is not None:
                    unit_sid = OE_CREATURE_EQUIVALENTS.get(str(creature))
                    if unit_sid and unit_sid.endswith("_upg") \
                            and (unit_sid + "_alt") in OE_UNIT_SID_TO_H3_CREATURE:
                        # H3 has a single upgrade but OE has two
                        # (<base>_upg and <base>_upg_alt): pick one at random.
                        unit_sid = _random.choice((unit_sid, unit_sid + "_alt"))
                    if unit_sid:
                        prop_rows.setdefault("propSquads", []).append(OrderedDict([
                            ("type", 0), ("id", oid),
                            ("isMainGuard", False),
                            ("isStartBattleImmediately", False),
                            ("reactionType", 2),
                            ("weeklyIncrementBonus", 0.0),
                            ("unitProps", [OrderedDict([
                                ("sid", unit_sid),
                                ("count", int(monster_meta.get("count") or 0)),
                            ])]),
                        ]))
            if group == "MONSTERS" and sid.startswith("squad"):
                squads_out.append((sid, oid, node))
                continue
            if sid not in groups:
                groups[sid] = {"ids": [], "nodes": [], "rotations": [], "levels": []}
                order.append(sid)
            groups[sid]["ids"].append(oid)
            groups[sid]["nodes"].append(node)
            groups[sid]["rotations"].append(rotation)
            groups[sid]["levels"].append(level)
            if obj.get("properties"):
                for table, row in obj["properties"].items():
                    prop_rows.setdefault(table, []).append(row)

    objects_out = [OrderedDict([
        ("sid", sid),
        ("ids", groups[sid]["ids"]),
        ("nodes", groups[sid]["nodes"]),
        ("rotations", groups[sid]["rotations"]),
        ("levels", groups[sid]["levels"]),
    ]) for sid in order]
    squads_list = [OrderedDict([("sid", sid), ("ids", [oid]), ("nodes", [node])])
                   for sid, oid, node in squads_out]

    victory = unified.get("victoryCondition") or {}
    win_types = victory.get("metadata") or []
    if not win_types and victory.get("type") in UNIFIED_TO_HOMMOE_WIN:
        win_types = [UNIFIED_TO_HOMMOE_WIN[victory["type"]]]
    if not win_types:
        win_types = [0]
    win_entry_template = OrderedDict([
        ("valueDesertion", 0.0), ("dayAdditionWinCondition", 0), ("heroSids", []),
        ("indexSideCampaign", 0), ("indexOtherPlayers", []), ("sidBuildWinCondition", ""),
        ("isRegistrationStartWork", False), ("isRegistrationStartFight", True),
        ("daysDelayStart", 0), ("countDayGladiatorArena", 3), ("countDayLostStartCity", 0),
        ("countDayCityHold", 3), ("isResetColdownCityHold", True),
        ("daysAnounceTournament", []), ("daysDelayStartFightTournament", []),
        ("countPointsTournament", 0), ("isSaveArmyTournament", True), ("autoSelectRule", 0),
    ])
    map_win_conditions = []
    for t in win_types:
        entry = OrderedDict(win_entry_template)
        entry["typeWinCondition"] = t
        map_win_conditions.append(entry)

    # scripts: passthrough for hommoe sources, generated events otherwise
    scripts = unified.get("scripts") or {}
    extra_prop_entities = []
    has_scripts = False
    if unified.get("sourceGame") == "hommoe" and scripts.get("commentAiData"):
        scripting = scripts["commentAiData"]
        dialog_quest = scripts.get("dialogQuestData") or OrderedDict([
            ("dialogs", OrderedDict([("lines", [])])),
            ("quests", OrderedDict([("quests", [])])),
        ])
        has_scripts = True  # the source .map had a block 4: keep the shape
    else:
        scripting, extra_prop_entities = _hommoe_generate_scripts(unified, width)
        dialog_quest = OrderedDict([
            ("dialogs", OrderedDict([("lines", [])])),
            ("quests", OrderedDict([("quests", [])])),
        ])
        # real editors never emit an empty 4th chunk (map-write.ts), so only
        # set the 0x08 separator bit when quests were actually generated
        has_scripts = bool(scripting.get("quests"))
    if extra_prop_entities:
        prop_rows.setdefault("propEntities", []).extend(extra_prop_entities)

    objects_properties = OrderedDict()
    for table in sorted(prop_rows):
        objects_properties[table] = prop_rows[table]

    # Rivers (H2/H3 sources): OE stores rivers in the terrain layer as
    # node lists, each node {n, s, isWaterfall} where s is the 4-bit
    # cardinal connectivity bitmask over neighbouring river tiles
    # (E=1, W=2, N=4, S=8; N = z+1) - mined from real maps and documented
    # in map-editor-json-tool's river-shape.ts. H2/H3 STREAMS tiles and
    # h3m river cells become river nodes here (they are still not OE
    # objects, so the objects loop keeps skipping the STREAMS group).
    river_tiles = set()
    for cell in grid:
        if cell.get("sourceRiver") and cell.get("sourceRiver") != "None":
            river_tiles.add((int(cell.get("x", 0)), int(cell.get("y", 0))))
    for tile_key, obj_list in (objects.get("tiles") or {}).items():
        parts = str(tile_key).split("_")
        if len(parts) < 2:
            continue
        try:
            pos = (int(parts[0]), int(parts[1]))
        except ValueError:
            continue
        if any(o.get("group") == "STREAMS" for o in obj_list):
            river_tiles.add(pos)
    river_nodes = []
    for (x, y) in sorted(river_tiles):
        if not (0 <= x < width and 0 <= y < height):
            continue
        s = 0
        if (x + 1, y) in river_tiles:
            s |= 1  # E
        if (x - 1, y) in river_tiles:
            s |= 2  # W
        if (x, y + 1) in river_tiles:
            s |= 4  # N (z grows north)
        if (x, y - 1) in river_tiles:
            s |= 8  # S
        river_nodes.append(OrderedDict([
            ("n", y * width + x), ("s", s), ("isWaterfall", False),
        ]))
    if river_nodes:
        rivers_out = [OrderedDict([
            ("sid", "test"),
            ("randomSeed", _random.randint(0, 2 ** 31 - 1)),
            ("nodes", river_nodes),
        ])]
    else:
        rivers_out = [OrderedDict([
            ("sid", "test"), ("randomSeed", 0), ("nodes", []),
        ])]

    adventure = OrderedDict([
        ("fileMapName", name),
        ("mapName", name),
        ("mapNameFromLoc", False),
        ("mapDesc", description),
        ("mapDescFromLoc", False),
        ("sizeX_", width),
        ("sizeZ_", height),
        ("tilesMap", tiles_map),
        ("levelsMap", levels_map),
        ("climbsMap", climbs_map),
        ("roadsMap", roads_map),
        ("waterMap", water_map),
        ("cliffRandomSeed", 0),
        ("views", []),
        ("objects", objects_out),
        ("objectsFreeId", next_free),
        ("squads", squads_list),
        ("squadsFreeId", next_free),
        ("markers", markers_out),
        ("markersFreeId", next_free),
        ("areas", objects.get("sourceAreas") or []),
        ("areasVersion", 0),
        ("rivers", objects.get("sourceRivers") or rivers_out),
        ("objectsProperties", objects_properties),
        ("settings", OrderedDict([("mapWinConditions", map_win_conditions)])),
        ("banInfoData", scenario["banInfoData"]),
        ("takenHeroes", []),
        ("haveCustomAreas", False),
        ("customAreasPainting", []),
        ("generatorChecksum", 0),
    ])
    if unified.get("sourceGame") == "hommoe":
        # Lossless passthrough of the raw adventure fields (5d):
        # descBlocks, views, keyObjects, objectValuesOverrides, the full
        # settings, banInfoData, takenHeroes, haveCustomAreas,
        # customAreasPainting, generatorChecksum, cliffRandomSeed...
        adv_extra = unified.get("sourceAdventureExtra") or {}
        for k, v in adv_extra.items():
            adventure[k] = v  # override the base placeholders (views, ...)
        # full raw settings (incl. the original mapWinConditions)
        # orphan objectsProperties rows (id matches no object) re-emitted
        for table, rows in (objects.get("sourceOrphanProps") or {}).items():
            objects_properties.setdefault(table, []).extend(rows)
    else:
        # H2/H3 source: reference-template defaults. views[0] follows the
        # GME viewport rule confirmed across every real sample map:
        # secSizeX/secSizeZ = ceil(size/16) (map-write.ts buildBlankMap).
        adventure["views"] = [OrderedDict([
            ("name", ""), ("minSecX", 0), ("minSecZ", 0),
            ("secSizeX", max(1, -(-width // 16))),
            ("secSizeZ", max(1, -(-height // 16))),
            ("isUnderground", False), ("stack", -1),
        ])]
        adventure["keyObjects"] = []
        adventure["objectValuesOverrides"] = OrderedDict([("list", [])])
        adventure["takenHeroes"] = []
        adventure["haveCustomAreas"] = False
        adventure["customAreasPainting"] = []
        adventure["generatorChecksum"] = ""
        # A fresh GME map always carries one zone covering the whole map
        # (template.map areas[0]: id 0, keyObjectId -1, rootNode 0,
        # nodes 0..n-1, neighbors [], biome Grass, areasVersion 1). The
        # game's minimap/thumbnail renderer (MapData.por in the
        # BhMapPreview path) indexes per-node area data and throws
        # IndexOutOfRangeException when areas is empty.
        adventure["areas"] = [OrderedDict([
            ("id", 0), ("keyObjectId", -1), ("rootNode", 0),
            ("nodes", list(range(total))),
            ("neighbors", []), ("biome", "Grass"),
        ])]
        adventure["areasVersion"] = 1
        settings = OrderedDict(HOMMOE_SETTINGS_DEFAULT)
        settings["mapWinConditions"] = map_win_conditions
        settings["gameMode"] = scenario["gameMode"]
        settings["endController"] = scenario["endController"]
        settings["isScenario"] = scenario["isScenario"]
        adventure["settings"] = settings

    separator = [0x0D, 0x00] if has_scripts else [0x05, 0x00]

    blocks = [
        OrderedDict([("name", "scenario"), ("raw", None), ("data", scenario)]),
        OrderedDict([("name", "adventure"), ("raw", None), ("data", adventure)]),
        OrderedDict([("name", "dialogQuestData"), ("raw", None), ("data", dialog_quest)]),
    ]
    if has_scripts:
        blocks.append(OrderedDict([("name", "commentAiData"), ("raw", None), ("data", scripting)]))

    return OrderedDict([
        ("gzipHeader", OrderedDict([("flg", 0), ("mtime", 0), ("xfl", 0), ("os", 10), ("extra", "")])),
        ("headerHash", header_hash),
        ("version", HOMMOE_DEFAULT_VERSION),
        ("separator", separator),
        ("blocks", blocks),
        ("trailingData", ""),
    ])


def convert_from_unified(unified, source_game):
    """
    Convert a map in the unified format into the JSON structure of the
    given game, ready to be written by write_h3m or write_fh2m.

    Args:
        unified: Dictionary in the unified format.
        source_game: "h3m", "fh2m" or "hommoe".

    Returns:
        OrderedDict: The map in the game-specific format.
    """
    if source_game == "fh2m":
        return unified_to_fh2m(unified)
    if source_game == "hommoe":
        return unified_to_hommoe(unified)
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

    # Castle owners: the fh2m format encodes the owner of a castle
    # through the LANDSCAPE_FLAGS object placed on the tile to the
    # left of the castle entrance, carrying the castle's object id.
    # The flag index is color * 2 (left flag) or color * 2 + 1
    # (right flag), the colors being 0 Blue, 1 Green, 2 Red,
    # 3 Yellow, 4 Orange, 5 Purple, 6 neutral. The decoded owner is
    # stored on the castleMetadata so the h3m writer can assign the
    # towns to their players.
    town_positions = {}
    for tile_key, obj_list in tiles.items():
        for obj in obj_list:
            if obj.get("group") == "KINGDOM_TOWNS":
                town_positions[obj.get("id")] = tile_key
    flag_owners = {}
    for tile_key, obj_list in tiles.items():
        for obj in obj_list:
            if obj.get("group") != "LANDSCAPE_FLAGS":
                continue
            owner_id = obj.get("id")
            if owner_id not in town_positions:
                continue
            parts = town_positions[owner_id].split("_")
            town_x, town_y = int(parts[0]), int(parts[1])
            parts = tile_key.split("_")
            flag_x, flag_y = int(parts[0]), int(parts[1])
            # The left flag sits on the tile to the left of the castle.
            if flag_y == town_y and flag_x == town_x - 1:
                color_id = obj.get("index", 0) // 2
                if 0 <= color_id < len(FH2M_PLAYER_COLORS):
                    flag_owners[str(owner_id)] = FH2M_PLAYER_COLORS[color_id]
                else:
                    flag_owners[str(owner_id)] = None

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
            entries = OrderedDict(
                (obj_id, _fh2m_metadata_to_unified(key, metadata, _lookup(obj_id)))
                for obj_id, metadata in value_map.items()
            )
            if key == "castleMetadata":
                for obj_id, owner_color in flag_owners.items():
                    for entry_id in entries:
                        if str(entry_id) == obj_id and owner_color is not None:
                            entries[entry_id]["ownerColor"] = owner_color
            result[key] = entries

    # Anchor alignment: the unified objects follow the h3m anchor
    # convention (the south-east corner of the footprint), so the
    # fh2m -> unified conversion applies the anchor shifts here -
    # the h3m writer places the instances at the unified positions
    # as-is and the fh2m writer restores the original anchors with
    # the stored anchorShift (the inverse of the applied shift). The
    # castle flags keep their original tile: their position rule
    # (one tile left of the castle entrance) is fh2m-specific and
    # the owner decoding above runs on the unshifted positions.
    from correspondence import (fh2m_tree_h3m_cover,
                                fh2m_misc_h3m_cover,
                                fh2m_to_h3m_anchor_shift)
    terrain_names = {}
    for tile_index, tile in enumerate(map_data.get("tiles", [])):
        terrain_names[(tile_index % width, tile_index // width)] = \
            _fh2m_terrain_name(tile.get("terrainIndex", 0))
    shifted_tiles = OrderedDict()
    source_order = 0
    for tile_key, obj_list in tiles.items():
        parts = tile_key.split("_")
        x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
        for obj in obj_list:
            group, index = obj.get("group"), obj.get("index")
            # The source order (tile-major, then within-tile) lets the
            # fh2m writer restore the exact original object order.
            obj["sourceOrder"] = source_order
            source_order += 1
            if group == "KINGDOM_TOWNS":
                shift = (2, 0)
            elif (group == "LANDSCAPE_TREES"
                  and fh2m_tree_h3m_cover(
                      index, terrain_names.get((x, y))) is not None):
                # A forest or wide tree converts to several
                # same-terrain trees that position themselves from
                # the fh2m anchor.
                shift = (0, 0)
            elif (group == "LANDSCAPE_MISCELLANEOUS"
                  and fh2m_misc_h3m_cover(
                      index, terrain_names.get((x, y)), (x, y), width)
                  is not None):
                # A multi-cell miscellaneous object with no single
                # h3m def converts to several same-terrain defs that
                # position themselves from the fh2m anchor.
                shift = (0, 0)
            else:
                shift = fh2m_to_h3m_anchor_shift(
                    group, index, terrain_names.get((x, y)),
                    (x, y), width)
            if shift:
                obj["anchorShift"] = [shift[0], shift[1]]
                target = "{}_{}_{}".format(x + shift[0], y + shift[1], z)
            else:
                target = tile_key
            shifted_tiles.setdefault(target, []).append(obj)
    result["tiles"] = shifted_tiles

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
                                  FH2M_TO_H3M_RESOURCES,
                                  H3M_CREATURE_DEF_NAMES,
                                  H3M_DWELLING_DEFS,
                                  H3M_KEYMASTER_TENT_DEFS,
                                  H3M_BORDER_GATE_DEFS)

    objects_section = unified.get("objects") or {}
    tiles = objects_section.get("tiles") or {}
    monster_meta = objects_section.get("monsterMetadata") or {}
    ownable_meta = objects_section.get("ownableMetadata") or {}
    resource_meta = objects_section.get("resourceMetadata") or {}
    artifact_meta = objects_section.get("artifactMetadata") or {}
    map_width = (unified.get("mapSize") or {}).get("width", 72)

    # --- Collect the instances to encode, in tile order ---
    # The unified anchors already follow the h3m convention (the
    # fh2m -> unified conversion applied the anchor shifts), so the
    # instances are placed at the unified positions as-is; only
    # out-of-map anchors (a shifted object on the map edge) are
    # clamped to the map bounds.
    instances = []
    for tile_key, obj_list in tiles.items():
        parts = tile_key.split("_")
        if len(parts) != 3:
            continue
        raw_x, raw_y, z = int(parts[0]), int(parts[1]), int(parts[2])
        x = min(max(raw_x, 0), map_width - 1)
        y = min(max(raw_y, 0), map_width - 1)
        for obj in obj_list:
            group = obj.get("group")
            index = obj.get("index", 0)
            obj_id = obj.get("id", 0)
            meta = None
            # Terrain lookup position: the original fh2m tile (the
            # anchor shift may have moved the unified anchor to a
            # neighboring tile of another terrain).
            stored_shift = obj.get("anchorShift")
            if stored_shift:
                terrain_pos = (raw_x - int(stored_shift[0]),
                               raw_y - int(stored_shift[1]))
            else:
                terrain_pos = (raw_x, raw_y)
            entry = None
            if obj.get("class") == 113:
                # Witch hut (hommoe source, sid wise_owl): the taught skill
                # comes from witchhutMetadata (AB/SoD 4-byte skill bitmask).
                wh_meta = (objects_section.get("witchhutMetadata") or {}).get(str(obj_id)) or {}
                entry = ("witchHut", (x, y, z), (113, int(obj.get("subclass") or 0)), wh_meta)
            if entry is None and obj.get("class") == 83:
                # Seer hut (hommoe source, sid monty_hall): the quest and
                # reward come from seerMetadata when present (h3m sources
                # keep raw anyway), else an empty quest/reward is written.
                seer_meta = (objects_section.get("seerMetadata") or {}).get(str(obj_id)) or {}
                entry = ("seerHut", (x, y, z), (83, int(obj.get("subclass") or 0)), seer_meta)
            if entry is None and obj.get("class") in (16, 24, 25, 84, 85):
                # Creature bank (hommoe source): SoD banks carry no
                # per-instance data, so a plain generic instance with the
                # bank's (class, subtype) is enough. Def names come from
                # the catalog (AVXbnk10..70, AVXgyne0...).
                entry = ("generic", (x, y, z),
                         (int(obj["class"]), int(obj.get("subclass") or 0)), None)
            pandora_meta = (objects_section.get("pandoraMetadata") or {}).get(str(obj_id))
            event_meta = (objects_section.get("eventMetadata") or {}).get(str(obj_id))
            if entry is not None:
                pass  # a creature bank was already set above
            elif event_meta is not None and obj.get("class") == 26:
                # Ground event (h3m class 26) restored from an OE quest: the
                # payload is carried in the eventMetadata map.
                entry = ("event", (x, y, z), (26, 0), event_meta)
            elif pandora_meta is not None:
                # Pandora's Box (h3m class 6): the full box content is
                # carried in the pandoraMetadata map; the catalog entry
                # (6, 0) is AVA0128.def in the reference catalog.
                entry = ("pandora", (x, y, z), (6, 0), pandora_meta)
            elif group == "MONSTERS":
                creature = index + 1
                m = monster_meta.get(str(obj_id)) or {}
                count = m.get("count") or 0
                join = m.get("joinCondition") or 0
                # Random monsters (fh2m ids 67-71) map to the h3m
                # random monster classes 71-75.
                if creature in (67, 68, 69, 70, 71):
                    obj_class = 71 + (creature - 67)
                    # The real maps store random monsters with an empty
                    # quantity (0) and disposition 2.
                    entry = ("monster", (x, y, z), (obj_class, 0), (0, 2))
                else:
                    h3m_creature = FH2M_TO_H3M_MONSTERS.get(creature)
                    if h3m_creature is None:
                        continue
                    # Fixed monsters: quantity = fh2m count, disposition
                    # follows the fh2m join condition as in the real maps
                    # (0/skip -> 2, money/free -> 4).
                    disp = 4 if join in (1, 2) else 2
                    entry = ("monster", (x, y, z), (54, h3m_creature), (count, disp))
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
                    # Inverse of the h3m -> fh2m index computation above:
                    # ids 9-81 at indices 0-72, Magic Book (82) at 73,
                    # Price of Loyalty ids 87-103 at indices 74-90.
                    if index <= 72:
                        artifact = index + 9
                    elif index == 73:
                        artifact = 82
                    else:
                        artifact = index + 13
                    h3m_artifact = FH2M_TO_H3M_ARTIFACTS.get(artifact)
                    if h3m_artifact is None:
                        # No h3m equivalent: fall back to the h3m random
                        # artifact of the same Heroes II class (Treasure ->
                        # 66, Minor -> 67, Major -> 68, Relic -> 69), the
                        # inverse of the h3m -> fh2m fallback.
                        from correspondence import FH2M_ARTIFACT_CLASSES
                        fh2m_class = FH2M_ARTIFACT_CLASSES.get(artifact)
                        if fh2m_class is None:
                            continue
                        h3m_artifact = {1: 66, 2: 67, 3: 68, 4: 69}.get(fh2m_class)
                        if h3m_artifact is None:
                            continue
                        entry = ("artifact", (x, y, z), (h3m_artifact, 0), None)
                    else:
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
                    owner_color = FH2M_TO_H3M_COLOR_ALIAS.get(
                        FH2M_PLAYER_COLORS[owner_color_id],
                        FH2M_PLAYER_COLORS[owner_color_id])
                    if owner_color in H3M_PLAYER_COLORS:
                        hero_payload["owner"] = H3M_PLAYER_COLORS.index(owner_color)
                # The hero template carries the hero CLASS (the first
                # hero of each block of 8 heroes: 0-7 knight, 8-15
                # cleric, 16-23 ranger... 136-143 elementalist), not
                # the hero type; the sprite of a placed hero is the
                # class sprite (AH<class>_E.DEF, see the official
                # heroClasses table and the real maps' catalogs).
                hero_class = (hero_type or 0) // 8
                entry = ("hero", (x, y, z), (34, hero_class), hero_payload)
            elif group == "KINGDOM_TOWNS":
                # A town: the object index encodes the race (race * 2
                # for a castle); the indices 12/13 are the H2 random
                # town (12 with the castle built); the castleMetadata
                # carries the defenders.
                town_type = None
                random_key = None
                if index in (12, 13):
                    # The h3m random town: its own class 77 (subclass
                    # 0, the AVCranx0.def sprite of the real maps);
                    # the castle status converts through the building
                    # flags like for the regular towns.
                    random_key = (77, 0)
                else:
                    from correspondence import FH2M_TOWN_RACE_ORDER
                    race_id = index // 2
                    if 0 <= race_id < len(FH2M_TOWN_RACE_ORDER):
                        from correspondence import H3M_TOWN_TYPE_TO_FH2M_RACE
                        for tt, race in H3M_TOWN_TYPE_TO_FH2M_RACE.items():
                            if race == FH2M_TOWN_RACE_ORDER[race_id]:
                                town_type = tt
                                break
                if town_type is not None or random_key is not None:
                    castle_meta = (objects_section.get("castleMetadata") or {}).get(str(obj_id)) or {}
                    # The fh2m town tile is the castle entrance (the
                    # gate part of the sprite sits on it, the flags on
                    # the tiles x-1 and x+1). The unified conversion
                    # shifts it to the h3m instance position
                    # (entrance + (2, +1)), so the instance is placed
                    # at the unified position as-is.
                    entry = ("town", (x, y, z),
                             random_key or (98, town_type), castle_meta)
            elif group in ("ADVENTURE_MISCELLANEOUS", "ADVENTURE_WATER"):
                # The miscellaneous and water objects with a
                # confirmed h3m sprite map through the misc table.
                from correspondence import (FH2M_TO_H3M_MISC,
                                          FH2M_TO_H3M_COLOR_INDEX)
                if group == "ADVENTURE_MISCELLANEOUS" and 51 <= index <= 58:
                    # Barrier (PoL): the fh2m index is one of the 8
                    # color variants (fheroes2
                    # populateAdventureMiscellaneous); it maps to the
                    # h3m border gate (class 9) with the color as
                    # subclass (def AVXbor<c>0.def).
                    entry = ("generic", (x, y, z),
                             (9, FH2M_TO_H3M_COLOR_INDEX[index - 51]), None)
                elif group == "ADVENTURE_MISCELLANEOUS" and 59 <= index <= 66:
                    # Traveller's Tent (PoL): same color-variant scheme;
                    # it maps to the h3m keymaster's tent (class 10,
                    # subclass = color, def AVXkey<c>0.def).
                    entry = ("generic", (x, y, z),
                             (10, FH2M_TO_H3M_COLOR_INDEX[index - 59]), None)
                else:
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
                if obj.get("class") in (88, 89, 90):
                    # Shrine restored from an OE altar_of_magic (hommoe
                    # source): the class was chosen randomly on the way
                    # in (user decision), keep it.
                    shrine_meta = (objects_section.get("shrineMetadata") or {}).get(str(obj_id)) or {}
                    entry = ("shrine", (x, y, z), (int(obj["class"]), 0), shrine_meta)
                else:
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
                # (class 53, subclass per mine type). The h3m class 53
                # has one def per terrain variant, so the def follows
                # the mine's appearance: the catalog key carries the
                # def name as a third element.
                from correspondence import FH2M_TO_H3M_MINES, fh2m_mine_def_name
                h3m_mine = FH2M_TO_H3M_MINES.get(index)
                if h3m_mine is not None:
                    def_name = fh2m_mine_def_name(index)
                    entry = ("ownable", (x, y, z),
                             (h3m_mine[0], h3m_mine[1], def_name),
                             ownable_meta.get(str(obj_id)) or None)
            elif group == "ADVENTURE_DWELLINGS":
                # The fh2m dwelling index maps to the h3m ownable
                # dwelling (class 17, subclass = dwelling id).
                from correspondence import FH2M_TO_H3M_DWELLINGS
                h3m_dwelling = FH2M_TO_H3M_DWELLINGS.get(index)
                if h3m_dwelling is not None:
                    entry = ("ownable", (x, y, z), h3m_dwelling,
                             ownable_meta.get(str(obj_id)) or None)
            elif group in ("LANDSCAPE_TREES", "LANDSCAPE_MOUNTAINS",
                          "LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS",
                          "LANDSCAPE_WATER"):
                # Decorative trees, mountains, rocks, miscellaneous
                # and water objects: the def is the footprint-exact
                # conversion of the true fh2m footprint (the terrain
                # variant first), picked again with the original
                # fh2m anchor so an edge object gets the same on-map
                # def the fh2m -> unified shift selected. The
                # multi-cell trees (forests, wide trees) fan out into
                # same-terrain trees (one per blocked cell, the
                # anchor offset from the unshifted fh2m anchor).
                from correspondence import (FH2M_LANDSCAPE_TO_H3M,
                                            fh2m_tree_h3m_cover,
                                            fh2m_misc_h3m_cover,
                                            fh2m_landscape_def)
                tile_terrain = (tile_terrains or {}).get(terrain_pos, "Grass")
                forest_cover = None
                if group == "LANDSCAPE_TREES":
                    forest_cover = fh2m_tree_h3m_cover(
                        index, tile_terrain, terrain_pos, map_width)
                misc_cover = None
                if group == "LANDSCAPE_MISCELLANEOUS":
                    misc_cover = fh2m_misc_h3m_cover(
                        index, tile_terrain, terrain_pos, map_width)
                if forest_cover is not None:
                    for fc_class, fc_def, fc_offset in forest_cover:
                        fx = min(max(terrain_pos[0] + fc_offset[0], 0),
                                 map_width - 1)
                        fy = min(max(terrain_pos[1] + fc_offset[1], 0),
                                 map_width - 1)
                        instances.append(
                            ("decorative", (fx, fy, z),
                             (fc_class, 0, fc_def), None))
                if misc_cover is not None:
                    for mc_class, mc_def, mc_offset in misc_cover:
                        mx = min(max(terrain_pos[0] + mc_offset[0], 0),
                                 map_width - 1)
                        my = min(max(terrain_pos[1] + mc_offset[1], 0),
                                 map_width - 1)
                        instances.append(
                            ("decorative", (mx, my, z),
                             (mc_class, 0, mc_def), None))
                chosen = None if (forest_cover is not None
                                  or misc_cover is not None) else \
                    fh2m_landscape_def(group, index, tile_terrain,
                                       terrain_pos, map_width)
                if forest_cover is not None or misc_cover is not None:
                    pass  # the cover instances are already appended
                elif chosen is not None:
                    entry = ("decorative", (x, y, z),
                             (chosen[0], 0, chosen[1]), None)
                elif group in ("LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS",
                               "LANDSCAPE_WATER"):
                    # No footprint-exact H3 counterpart exists for this
                    # rock/misc/water object (see landscape_inventory.txt):
                    # drop it instead of falling back to a class-level
                    # def with the wrong footprint.
                    pass
                elif FH2M_LANDSCAPE_TO_H3M.get((group, index)) is not None:
                    entry = ("decorative", (x, y, z),
                             (FH2M_LANDSCAPE_TO_H3M[(group, index)], 0),
                             None)
            elif group.startswith("LANDSCAPE"):
                from correspondence import FH2M_LANDSCAPE_TO_H3M
                h3m_class = FH2M_LANDSCAPE_TO_H3M.get((group, index))
                if h3m_class is not None:
                    entry = ("decorative", (x, y, z), (h3m_class, 0), None)
            if entry:
                instances.append(entry)

    if not instances:
        return None

    # --- Build the sprite catalog: one def per used (class, subclass) ---
    # Every real map's catalog starts with two reserved, never-instanced
    # defs (the random monster template AVWmrnd0.def class 71 and the
    # holy ground AVLholg0.def class 124); the game expects them at
    # indexes 0 and 1, so object instances start at index 2.
    catalog_keys = [(71, 0), (124, 0)]
    catalog_entries = [FH2M_TO_H3M_CATALOG[(71, 0)],
                       FH2M_TO_H3M_CATALOG[(124, 0)]]
    kind_of = {(71, 0): 0, (124, 0): 1}
    for entry in instances:
        key = entry[2]
        obj_class, obj_subclass = key[0], key[1]
        if key not in kind_of:
            if len(key) == 3:
                # A variant def (mine terrain variant, tree or mountain
                # variant): the def name is the third key element and
                # its sprite body comes from H3M_MINE_DEFS /
                # H3M_TREE_DEFS / H3M_MOUNTAIN_DEFS.
                from correspondence import (H3M_MINE_DEFS, H3M_TREE_DEFS,
                                          H3M_MOUNTAIN_DEFS,
                                          H3M_LANDSCAPE_DEFS)
                ref = (H3M_MINE_DEFS.get((key[2] or "").lower())
                       or H3M_TREE_DEFS.get((key[2] or "").lower())
                       or H3M_MOUNTAIN_DEFS.get((key[2] or "").lower())
                       or H3M_LANDSCAPE_DEFS.get((key[2] or "").lower())
                       or FH2M_TO_H3M_CATALOG.get((key[0], key[1])))
            else:
                ref = FH2M_TO_H3M_CATALOG.get(key)
                if ref is None and obj_class == 17:
                    # Dwellings missing from the reference catalog get
                    # their def and passability body from the original
                    # game's Objects.txt (every dwelling id 0-79).
                    ref = H3M_DWELLING_DEFS.get(obj_subclass)
                if ref is None and obj_class == 10:
                    # Keymaster's tents missing from the reference
                    # catalog get their def from the original game's
                    # Objects.txt (AVXkey<c>0.def per color subclass).
                    ref = H3M_KEYMASTER_TENT_DEFS.get(obj_subclass)
                if ref is None and obj_class == 9:
                    # Border gates missing from the reference catalog
                    # get their def from the original game's Objects.txt
                    # (AVXbor<c>0.def per color subclass).
                    ref = H3M_BORDER_GATE_DEFS.get(obj_subclass)
            if ref is None and obj_class == 34:
                # The hero template subclass is the hero CLASS and
                # the sprite is the class sprite AH<class>_E.DEF (the
                # official heroClasses animation names). Both mask
                # cells must be (0,0) - the bottom-right cell, bit 47 of
                # the packed mask (0x80 in the last mask byte) - exactly
                # like the real game's hero template (Objects.txt,
                # ah00_e.def: passable ffffffffff7f, action ...80): the
                # passable last byte 0x7f blocks the hero's own cell,
                # while 0xbf would block the cell one to the left and
                # shift every placed hero one cell west.
                ref = ('ah%02d_e.def' % (obj_subclass or 0),
                       'ffffffffff7f000000000080ff010100',
                       '000000000000000000000000000000000000')
            if ref is None:
                continue
            kind_of[key] = len(catalog_keys)
            catalog_keys.append(key)
            catalog_entries.append(ref)

    # The game resolves random monsters against the map's own catalog
    # (NewfullMap::findObjectType in game::convertObject): a class-54 def
    # must exist for every creature id the game can roll (below
    # CREATURE_CATAPULT: 0..144 minus the unused slots), or the load
    # crashes. Add the missing creature defs with the standard monster
    # body (passable FF FF FF FF FF 7F, all lands, group 2) observed in
    # the real maps. Ids 145+ are war machines or unused slots: never
    # rolled, and several have no def in the game data (the real maps
    # only carry defs that exist), so they are skipped. This backfill
    # runs BEFORE the unknown-sprite filter below so that fixed monsters
    # (class 54) survive it: every rollable creature id gets a def.
    for creature_id, def_name in H3M_CREATURE_DEF_NAMES.items():
        if creature_id >= 145 or not def_name.lower().endswith(".def"):
            continue
        key = (54, creature_id)
        if key in kind_of:
            continue
        body = bytearray(42)
        body[0:6] = bytes.fromhex("ffffffffff7f")       # passable cells
        body[6:12] = bytes.fromhex("000000000080")      # actionable cells
        body[12:14] = bytes.fromhex("ff01")             # allowed landscapes
        body[14:16] = bytes.fromhex("0100")             # landscape group
        body[16:24] = struct.pack("<II", 54, creature_id)
        body[24] = 2                                    # editor group: monster
        body[25:42] = b"\x00" * 17                      # above + 16 unknown
        kind_of[key] = len(catalog_keys)
        catalog_keys.append(key)
        catalog_entries.append((def_name, body[:16].hex(), body[24:].hex()))

    # Fixed artifacts (class 5) used by the instances but absent from
    # the reference catalog get their def backfilled as well: they all
    # follow the AVA%04d.def naming with the standard artifact body
    # (passable FF FF FF FF FF 7F, all lands, editor group 4) observed
    # in the real maps' catalog.
    for entry in instances:
        key = entry[2]
        if key[0] == 5 and len(key) == 2 and key not in kind_of:
            body = bytearray(42)
            body[0:6] = bytes.fromhex("ffffffffff7f")       # passable cells
            body[6:12] = bytes.fromhex("000000000080")      # actionable cells
            body[12:14] = bytes.fromhex("ff01")             # allowed landscapes
            body[14:16] = bytes.fromhex("0100")             # landscape group
            body[16:24] = struct.pack("<II", 5, key[1])
            body[24] = 4                                    # editor group: artifacts
            body[25:42] = b"\x00" * 17                      # above + 16 unknown
            kind_of[key] = len(catalog_keys)
            catalog_keys.append(key)
            catalog_entries.append(("AVA%04d.def" % key[1],
                                    body[:16].hex(), body[24:].hex()))

    # Drop the instances whose sprite is unknown.
    instances = [e for e in instances if e[2] in kind_of]
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
        buffer.write(bytes.fromhex(trailing))

    # --- Instances ---
    buffer.write(struct.pack("<I", len(instances)))
    # In AB/SoD the creature slots and artifact ids are 16-bit and the
    # actionable objects carry a 4-byte objectID right after the header.
    creature_id_bytes = 2 if version_ab else 1
    artifact_id_bytes = 2 if version_ab else 1
    creature_fmt = "<HH" if version_ab else "<BH"
    creature_none = 0xFFFF if version_ab else 0xFF
    artifact_none = 0xFFFF if version_ab else 0xFF
    # SoD heroes carry 19 artifact slots (the extra misc5 slot).
    artifact_slots = 19 if version_sod else 18

    def write_creature_slot(creature, count):
        if creature is None:
            buffer.write(struct.pack(creature_fmt, creature_none, 0))
        else:
            buffer.write(struct.pack(creature_fmt, creature, count))

    def write_artifact_id(art):
        buffer.write(struct.pack("<H" if version_ab else "<B",
                                 artifact_none if art is None else art))

    for entry in instances:
        kind_name, (x, y, z), key, payload = entry
        obj_class, obj_subclass = key[0], key[1]
        buffer.write(struct.pack("<BBB", x, y, z))
        buffer.write(struct.pack("<I", kind_of[key]))
        # The 5 trailing header bytes are unknown and always 0 in the
        # real maps (h3mlib: unknown1[5]; //0x00).
        buffer.write(b"\x00" * 5)
        if kind_name in ("monster", "hero", "town"):
            if version_ab:
                buffer.write(struct.pack("<I", 0))  # objectID
        if kind_name == "monster":
            qty, disp = payload if isinstance(payload, tuple) else (payload & 0xFFFF, 0)
            buffer.write(struct.pack("<HB", qty & 0xFFFF, disp & 0xFF))
            buffer.write(struct.pack("<B", 0))  # no treasure
            # The editor ghost objects (random monster placeholders at
            # 0,0,0, the game writes them with no canFlee/canGrow tail
            # - see the parser's mirror rule) end at the treasure
            # byte; every other monster carries the 4 tail bytes.
            if not (x == 0 and y == 0 and z == 0
                    and obj_class in (71, 72, 73, 74, 75,
                                       162, 163, 164)):
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
            if version_ab and obj_class == 113:
                # Witch hut carries its 4 skill bits only in AB/SoD.
                buffer.write(struct.pack("<I", 0xFFFFFFFF))
            # other decorative objects: no per-instance data
        elif kind_name == "ownable":
            # Owner word (0xFF = neutral); recovered from the unified
            # ownableMetadata when the source carried one (h3m ownable
            # classes / OE propOwners rows).
            owner = payload.get("owner") if isinstance(payload, dict) else None
            if isinstance(owner, int) and 0 <= owner < 8:
                buffer.write(struct.pack("<I", owner))
            else:
                buffer.write(struct.pack("<I", 0xFF))  # neutral owner
        elif kind_name == "shrine":
            # RoE shrine layout is one spell byte + 3 padding bytes; the
            # real maps use 0xFF (random spell) there. A fixed spell from
            # the shrineMetadata is written as-is.
            spell = (payload or {}).get("spell") if isinstance(payload, dict) else None
            buffer.write(struct.pack("<B", 0xFF if spell is None else int(spell) & 0xFF))
            buffer.write(b"\x00" * 3)
        elif kind_name == "generic":
            # The generic objects: signs (classes 59/91) carry a
            # message; the ownable objects (class 42 Stone Liths)
            # carry an owner; the other misc objects (windmill,
            # lean-to, water wheel, witch hut, observation tower,
            # bottle, buoy) carry no per-instance data.
            if obj_class in (59, 91) and (payload or {}).get("message"):
                # Only sign/bottle objects (whose fh2m source is a sign
                # with a message) carry a message; the same h3m classes
                # reached from other fh2m groups (e.g. the Sea Chest,
                # class 82 via WATER_1) carry no per-instance data in
                # the real maps.
                msg_bytes = (payload["message"]).encode("cp1252", errors="replace")
                buffer.write(struct.pack("<i", len(msg_bytes)))
                buffer.write(msg_bytes)
                buffer.write(b"\x00" * 4)
            elif obj_class == 42:
                # The Stone Liths are ownable: an owner word.
                buffer.write(struct.pack("<I", 0xFF))  # neutral
            elif obj_class == 113 and version_ab:
                # The witch hut carries its 4 skill bits in AB/SoD
                # (the same rule as the decorative class 113) - the
                # parser reads them for every class 113 instance.
                buffer.write(struct.pack("<I", 0xFFFFFFFF))
        elif kind_name == "witchHut":
            # Witch hut: AB/SoD carry a 4-byte skill bitmask (0xFFFFFFFF =
            # random skill); RoE carries no skill bytes (random at start).
            if version_ab:
                skill = (payload or {}).get("skill")
                bits = 0xFFFFFFFF if skill is None else (1 << (int(skill) & 31))
                buffer.write(struct.pack("<I", bits & 0xFFFFFFFF))
        elif kind_name == "seerHut":
            # Seer hut layout, mirroring the h3decoder seerHut parser:
            # quest (RoE: one questArtifact byte), reward, 2 trailing bytes.
            meta = payload or {}
            quest = meta.get("quest")
            if not version_ab:
                qa = meta.get("questArtifact")
                buffer.write(struct.pack("<B", 0xFF if qa is None else qa & 0xFF))
            elif not quest or not quest.get("type"):
                buffer.write(struct.pack("<B", 0))  # empty quest
            else:
                qtype = int(quest.get("type")) & 0xFF
                buffer.write(struct.pack("<B", qtype))
                if qtype == 1:
                    buffer.write(struct.pack("<I", _to_int(quest.get("level")) & 0xFFFFFFFF))
                elif qtype == 2:
                    pr = quest.get("primarySkills") or {}
                    buffer.write(struct.pack("<4B", *[
                        _to_int(pr.get(n)) & 0xFF for n in
                        ("attack", "defense", "spellPower", "knowledge")]))
                elif qtype == 3 and version_ab:
                    buffer.write(struct.pack("<I", _to_int(quest.get("heroObjectID")) & 0xFFFFFFFF))
                elif qtype == 4 and version_ab:
                    buffer.write(struct.pack("<I", _to_int(quest.get("monsterObjectID")) & 0xFFFFFFFF))
                elif qtype == 5:
                    arts = [a for a in (quest.get("artifacts") or []) if isinstance(a, int)]
                    buffer.write(struct.pack("<B", min(len(arts), 255)))
                    for a in arts[:255]:
                        write_artifact_id(a)
                elif qtype == 6:
                    crs = [c for c in (quest.get("creatures") or []) if isinstance(c, dict)]
                    buffer.write(struct.pack("<B", min(len(crs), 255)))
                    for c in crs[:255]:
                        write_creature_slot(c.get("creature"), _to_int(c.get("count")))
                elif qtype == 7:
                    res = quest.get("resources") or {}
                    buffer.write(struct.pack("<7i", *[
                        _to_int(res.get(n)) for n in
                        ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold")]))
                elif qtype == 8:
                    buffer.write(struct.pack("<B", _to_int(quest.get("hero")) & 0xFF))
                elif qtype == 9:
                    buffer.write(struct.pack("<B", _to_int(quest.get("player")) & 0xFF))
                buffer.write(struct.pack("<I", _to_int(quest.get("deadline")) & 0xFFFFFFFF))
                for msg_name in ("firstVisitMessage", "nextVisitMessage", "completedMessage"):
                    mb = (quest.get(msg_name) or "").encode("cp1252", errors="replace")
                    buffer.write(struct.pack("<i", len(mb)))
                    buffer.write(mb)
            reward = meta.get("reward")
            if not reward or not reward.get("type") or int(reward.get("type")) in (0, 0xFF):
                buffer.write(struct.pack("<B", 0))  # no reward
            else:
                rtype = int(reward.get("type")) & 0xFF
                buffer.write(struct.pack("<B", rtype))
                if rtype == 1:
                    buffer.write(struct.pack("<I", _to_int(reward.get("experience")) & 0xFFFFFFFF))
                elif rtype == 2:
                    buffer.write(struct.pack("<I", _to_int(reward.get("spellPoints")) & 0xFFFFFFFF))
                elif rtype == 3:
                    buffer.write(struct.pack("<b", _to_int(reward.get("morale"))))
                elif rtype == 4:
                    buffer.write(struct.pack("<b", _to_int(reward.get("luck"))))
                elif rtype == 5:
                    buffer.write(struct.pack("<B", _to_int(reward.get("resourceType")) & 0xFF))
                    buffer.write(struct.pack("<I", _to_int(reward.get("amount")) & 0xFFFFFFFF))
                elif rtype == 6:
                    buffer.write(struct.pack("<B", _to_int(reward.get("primarySkill")) & 0xFF))
                    buffer.write(struct.pack("<B", _to_int(reward.get("value")) & 0xFF))
                elif rtype == 7:
                    buffer.write(struct.pack("<B", _to_int(reward.get("secondarySkill")) & 0xFF))
                    buffer.write(struct.pack("<B", _to_int(reward.get("level")) & 0xFF))
                elif rtype == 8:
                    write_artifact_id(reward.get("artifact"))
                elif rtype == 9:
                    buffer.write(struct.pack("<B", _to_int(reward.get("spell")) & 0xFF))
                elif rtype == 10:
                    write_creature_slot(reward.get("creature"), _to_int(reward.get("count")))
            buffer.write(b"\x00" * 2)
        elif kind_name == "event":
            # Ground event layout, mirroring the h3decoder 'event' parser:
            # optional guard (message + no creatures + 4 bytes), then
            # experience, mana, morale, luck, resources, primary skills,
            # secondary skills, artifacts, spells, creatures, 8 trailing
            # bytes, players, applyToComputer, removeAfterVisit, 4 bytes.
            meta = payload or {}
            msg = meta.get("message") or ""
            if msg:
                mb = msg.encode("cp1252", errors="replace")
                buffer.write(struct.pack("<B", 1))
                buffer.write(struct.pack("<i", len(mb)))
                buffer.write(mb)
                buffer.write(struct.pack("<B", 0))  # no guard creatures
                buffer.write(b"\x00" * 4)
            else:
                buffer.write(struct.pack("<B", 0))
            buffer.write(struct.pack("<I", _to_int(meta.get("experience")) & 0xFFFFFFFF))
            buffer.write(struct.pack("<H", _to_int(meta.get("mana")) & 0xFFFF))
            buffer.write(struct.pack("<b", _to_int(meta.get("morale"))))
            buffer.write(struct.pack("<b", _to_int(meta.get("luck"))))
            res = meta.get("resources") or {}
            buffer.write(struct.pack("<7h", *[
                _to_int(res.get(n)) for n in
                ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold")]))
            pr = meta.get("primarySkills") or {}
            buffer.write(struct.pack("<4B", *[
                _to_int(pr.get(n)) & 0xFF for n in
                ("attack", "defense", "spellPower", "knowledge")]))
            skills = [sk for sk in (meta.get("secondarySkills") or []) if isinstance(sk, dict)]
            buffer.write(struct.pack("<B", min(len(skills), 255)))
            for sk in skills[:255]:
                buffer.write(struct.pack("<BB", _to_int(sk.get("id")) & 0xFF,
                                         _to_int(sk.get("level")) & 0xFF))
            arts = [a for a in (meta.get("artifacts") or []) if isinstance(a, int)]
            buffer.write(struct.pack("<B", min(len(arts), 255)))
            for a in arts[:255]:
                write_artifact_id(a)
            spells = [sp for sp in (meta.get("spells") or []) if isinstance(sp, int)]
            buffer.write(struct.pack("<B", min(len(spells), 255)))
            for sp in spells[:255]:
                buffer.write(struct.pack("<B", sp & 0xFF))
            crs = [c for c in (meta.get("creatures") or []) if isinstance(c, dict)]
            buffer.write(struct.pack("<B", min(len(crs), 255)))
            for cr in crs[:255]:
                write_creature_slot(cr.get("creature"), _to_int(cr.get("count")))
            buffer.write(b"\x00" * 8)
            buffer.write(struct.pack("<B", _to_int(meta.get("players", 0xFF)) & 0xFF))
            buffer.write(struct.pack("<B", 1 if meta.get("applyToComputer", True) else 0))
            buffer.write(struct.pack("<B", 1 if meta.get("removeAfterVisit") else 0))
            buffer.write(b"\x00" * 4)
        elif kind_name == "pandora":
            # Pandora's Box layout, mirroring the pandoraBox parser:
            # optional guard (message + 7 creature slots + 4 bytes), then
            # experience, mana, morale, luck, resources, primary skills,
            # secondary skills, artifacts, spells, creatures, 8 trailing
            # bytes.
            meta = payload or {}
            guard = meta.get("guard")
            if guard:
                buffer.write(struct.pack("<B", 1))
                msg = (guard.get("message") or "").encode("cp1252", errors="replace")
                buffer.write(struct.pack("<i", len(msg)))
                buffer.write(msg)
                slots = list((guard.get("creatures") or [])[:7])
                while len(slots) < 7:
                    slots.append({"creature": None, "count": 0})
                has = any(s.get("creature") is not None
                          and (s.get("count") or 0) > 0 for s in slots)
                buffer.write(struct.pack("<B", 1 if has else 0))
                if has:
                    for s in slots:
                        write_creature_slot(s.get("creature"),
                                            _to_int(s.get("count")))
                buffer.write(b"\x00" * 4)
            else:
                buffer.write(struct.pack("<B", 0))
            buffer.write(struct.pack("<I", _to_int(meta.get("experience")) & 0xFFFFFFFF))
            buffer.write(struct.pack("<H", _to_int(meta.get("mana")) & 0xFFFF))
            buffer.write(struct.pack("<b", _to_int(meta.get("morale"))))
            buffer.write(struct.pack("<b", _to_int(meta.get("luck"))))
            res = meta.get("resources") or {}
            buffer.write(struct.pack("<7h", *[
                _to_int(res.get(n)) for n in
                ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold")]))
            pr = meta.get("primarySkills") or {}
            buffer.write(struct.pack("<4B", *[
                _to_int(pr.get(n)) & 0xFF for n in
                ("attack", "defense", "spellPower", "knowledge")]))
            skills = [s for s in (meta.get("secondarySkills") or [])
                      if isinstance(s, dict)]
            n = min(len(skills), 255)
            buffer.write(struct.pack("<B", n))
            for sk in skills[:n]:
                buffer.write(struct.pack("<BB",
                                         _to_int(sk.get("id")) & 0xFF,
                                         _to_int(sk.get("level")) & 0xFF))
            arts = [a for a in (meta.get("artifacts") or []) if isinstance(a, int)]
            n = min(len(arts), 255)
            buffer.write(struct.pack("<B", n))
            for a in arts[:n]:
                write_artifact_id(a)
            spells = [s for s in (meta.get("spells") or []) if isinstance(s, int)]
            n = min(len(spells), 255)
            buffer.write(struct.pack("<B", n))
            for s in spells[:n]:
                buffer.write(struct.pack("<B", s & 0xFF))
            crs = meta.get("creatures") or []
            n = min(len(crs), 255)
            buffer.write(struct.pack("<B", n))
            for cr in crs[:n]:
                write_creature_slot(cr.get("creature"), _to_int(cr.get("count")))
            buffer.write(b"\x00" * 8)
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
            if version_sod:
                # SoD wraps the experience in a flag byte; without it
                # the hero starts with the default experience.
                if experience and experience > 0:
                    buffer.write(struct.pack("<B", 1))
                    buffer.write(struct.pack("<I", experience))
                else:
                    buffer.write(struct.pack("<B", 0))
            else:
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
                        write_creature_slot(army[slot][0], army[slot][1])
                    else:
                        # An empty slot: creature 0xFF/0xFFFF means none.
                        write_creature_slot(None, 0)
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
                for slot in range(artifact_slots):
                    value = converted_artifacts[slot] if slot < len(converted_artifacts) else artifact_none
                    write_artifact_id(value)
                buffer.write(struct.pack("<H", 0))  # empty bag
            else:
                buffer.write(struct.pack("<B", 0))
            patrol = meta.get("isOnPatrol")
            radius = meta.get("patrolRadius") or 0
            buffer.write(struct.pack("<B", radius if patrol else 0xFF))
            buffer.write(b"\x00" * 16)
            if version_ab:
                # AB/SoD hero trailer: biography flag, gender, spells
                # and primary skills flags (all unset: the defaults).
                buffer.write(struct.pack("<B", 0))  # no custom biography
                buffer.write(struct.pack("<B", 0xFF))  # default gender
                spells_hex = meta.get("spells")
                if version_sod:
                    # SoD: flag byte + 9-byte spell bitfield when custom
                    # spells are set (OE hero standard startMagics for
                    # hommoe sources, see _h3_hero_spells_bitfield).
                    if isinstance(spells_hex, str) and spells_hex:
                        buffer.write(struct.pack("<B", 1))
                        buffer.write(bytes.fromhex(spells_hex).ljust(9, b"\x00")[:9])
                    else:
                        buffer.write(struct.pack("<B", 0))  # no custom spells
                else:
                    # AB: a single spells byte (bits 0-7) always present.
                    if isinstance(spells_hex, str) and spells_hex:
                        buffer.write(struct.pack("<B", bytes.fromhex(spells_hex)[0]))
                    elif isinstance(spells_hex, int):
                        buffer.write(struct.pack("<B", spells_hex & 0xFF))
                    else:
                        buffer.write(struct.pack("<B", 0))  # AB spells byte
                buffer.write(struct.pack("<B", 0))  # no custom primary skills
        elif kind_name == "town":
            # RoE town layout: owner, name, creatures (7 slots),
            # formation, buildings flags, spell bitfields and events.
            # The fh2m castleMetadata converts: the custom name, the
            # garrison defenders, the built buildings (the fh2m
            # flags map back through the building bit tables) and
            # the owner decoded from the castle flags.
            from correspondence import (H3M_DWELLING_BITS,
                                         H3M_TOWN_BUILDING_BITS,
                                         FH2M_TO_H3M_MONSTERS)
            meta = payload or {}
            owner = FH2M_TO_H3M_COLOR_ALIAS.get(meta.get("ownerColor"),
                                               meta.get("ownerColor"))
            if owner in H3M_PLAYER_COLORS:
                owner_byte = H3M_PLAYER_COLORS.index(owner)
            else:
                owner_byte = 0xFF
            buffer.write(struct.pack("<B", owner_byte))
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
                        write_creature_slot(defenders[slot][0], defenders[slot][1])
                    else:
                        write_creature_slot(None, 0)
            else:
                buffer.write(struct.pack("<B", 0))
            buffer.write(struct.pack("<B", 0))  # formation
            # Buildings: the real RoE maps always use the hasFort layout
            # (has_buildings=0 + one fort byte); the fh2m built flags do
            # not map onto the h3m building bitfield, and a custom
            # bitfield without the town hall crashes the game at load.
            buffer.write(struct.pack("<B", 0))  # no custom buildings
            # hasFort: always built, except the random town without
            # its castle (the fh2m BUILD_CASTLE flag 0x0800 missing
            # from the built buildings).
            if obj_class == 77:
                built_flags = meta.get("builtBuildings") or []
                has_fort = 1 if 0x0800 in built_flags else 0
            else:
                has_fort = 1
            buffer.write(struct.pack("<B", has_fort))
            if version_ab:
                # AB/SoD towns carry the existing-spells bitfield
                # before the impossible-spells one (all-zero: the
                # mage guild spells are generated by the game).
                buffer.write(b"\x00" * 9)
            buffer.write(b"\x00" * 9)  # impossible spells: all allowed
            buffer.write(struct.pack("<I", 0))  # no events
            if version_sod:
                # SoD towns carry an alignment byte after the events
                # (FF = same as owner / random).
                buffer.write(struct.pack("<B", 0xFF))
            buffer.write(b"\x00\x00\x00")  # trailing 3 bytes

    # --- Global events section ---
    # Every h3m file ends with a uint32 event count followed by the
    # events, right after the object details; the game reads this
    # section when loading the map and crashes when it is missing.
    # Convert the fh2m daily events (RoE/AB body layout; SoD adds the
    # applies-to-human byte).
    events = unified.get("dailyEvents") or []
    buffer.write(struct.pack("<I", len(events)))
    fh2m_to_h3m_color_bit = {"Red": 0, "Blue": 1, "Yellow": 2, "Green": 3,
                             "Orange": 4, "Purple": 5}
    for event in events:
        name_bytes = b""
        buffer.write(struct.pack("<I", len(name_bytes)))
        buffer.write(name_bytes)
        msg = (event.get("message") or "").encode("cp1252", errors="replace")
        buffer.write(struct.pack("<I", len(msg)))
        buffer.write(msg)
        res = event.get("resources") or {}
        values = [res.get(key, 0) or 0 for key in
                  ("wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold")]
        buffer.write(struct.pack("<7i", *values))
        players_mask = 0
        for color in (event.get("humanColors") or []) + (event.get("computerColors") or []):
            bit = fh2m_to_h3m_color_bit.get(color)
            if bit is not None:
                players_mask |= (1 << bit)
        buffer.write(struct.pack("<B", players_mask))
        if version_sod:
            buffer.write(struct.pack("<B", 1 if event.get("humanColors") else 0))
        buffer.write(struct.pack("<B", 1 if event.get("computerColors") else 0))
        first = (event.get("firstOccurrenceDay") or 1) - 1
        buffer.write(struct.pack("<H", max(0, min(671, first))))
        buffer.write(struct.pack("<B", min(28, event.get("repeatPeriodInDays") or 0)))
        buffer.write(b"\x00" * 17)

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
