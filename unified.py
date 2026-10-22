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
    "Inferno": "Inferno",
    "Necropolis": "Necromancer",
    "Dungeon": "Warlock",
    "Stronghold": "Barbarian",
    "Fortress": "Fortress",
    "Conflux": "Conflux",
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

# h3m terrain -> unified terrain
H3M_TERRAINS = {
    "Dirt": "Dirt",
    "Sand": "Sand",
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


def _h3m_objects_to_unified(map_data):
    """
    Convert the decoded h3m object instances into the unified objects
    section: objects stored per tile with metadata maps keyed by object
    id, as the fh2m format does.

    Objects whose group could not be mapped to a unified group are
    dropped (UNDEFINED_* groups); their ids are listed under "dropped".
    """
    objects_section = map_data.get("Objects", {})
    tiles_data = objects_section.get("Tiles")
    if not tiles_data:
        return None

    tiles = OrderedDict()
    dropped = []
    for tile_key, obj_list in tiles_data.get("tiles", {}).items():
        x, y, z = tile_key.split("_")
        unified_objs = []
        for obj in obj_list:
            group = obj.get("group", "")
            if group.startswith("UNDEFINED"):
                dropped.append(obj.get("id"))
                continue
            unified_objs.append(OrderedDict([
                ("id", obj.get("id")),
                ("group", group),
                ("index", obj.get("index")),
            ]))
        if unified_objs:
            tiles[tile_key] = unified_objs

    # Metadata maps are already keyed by object id and use unified-friendly
    # field names; pass them through, dropping ids of dropped objects.
    dropped_set = set(dropped)
    metadata = OrderedDict()
    for key, value_map in tiles_data.items():
        if key == "tiles":
            continue
        cleaned = OrderedDict()
        for obj_id, value in value_map.items():
            if int(obj_id) not in dropped_set:
                cleaned[obj_id] = value
        if cleaned:
            metadata[key] = cleaned

    result = OrderedDict([("tiles", tiles)])
    result.update(metadata)
    if dropped:
        result["dropped"] = dropped
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
    "Sand": 415,
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
            "la carte {} ne peut pas être convertie".format(unified.get("name", ""))
        )

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
        data["translations"] = OrderedDict()

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
    for tile_key, obj_list in objects_section.get("tiles", {}).items():
        parts = tile_key.split("_")
        if len(parts) != 3:
            continue
        x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
        if z != 0:
            continue
        objects_by_tile[(x, y)] = [OrderedDict(obj) for obj in obj_list]

    default_terrain = (UNIFIED_TO_FH2M_TERRAIN_INDEX.get("Grass", 30), 0)
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
        data["translationInfo"] = OrderedDict()

    # Metadata maps keyed by object id, from the unified objects section,
    # overriding the empty defaults above.
    for key in ("castleMetadata", "heroMetadata", "sphinxMetadata",
                "signMetadata", "adventureMapEventMetadata",
                "selectionObjectMetadata", "capturableObjectsMetadata",
                "monsterMetadata", "artifactMetadata", "resourceMetadata"):
        value_map = objects_section.get(key)
        if value_map:
            data[key] = OrderedDict(value_map)
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


def _fh2m_objects_to_unified(map_data):
    """
    Convert the fh2m object instances into the unified objects section.
    The fh2m storage is already the unified one: objects per tile with
    metadata maps keyed by object id; the metadata maps are passed
    through with their original keys.
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

    # Metadata maps keyed by object id
    for key in ("castleMetadata", "heroMetadata", "sphinxMetadata",
                "signMetadata", "adventureMapEventMetadata",
                "selectionObjectMetadata", "capturableObjectsMetadata",
                "monsterMetadata", "artifactMetadata", "resourceMetadata",
                "standardObjectMetadata"):
        value_map = map_data.get(key)
        if value_map:
            result[key] = value_map

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
