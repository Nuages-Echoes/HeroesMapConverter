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
H3M_TOWN_RACES = {
    "Castle": "Knight",
    "Rampart": "Sorceress",
    "Tower": "Wizard",
    "Inferno": "Warlock",
    "Necropolis": "Necromancer",
    "Dungeon": "Warlock",
    "Stronghold": "Barbarian",
    "Fortress": "Sorceress",
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
            ]))
        levels.append(OrderedDict([("grid", grid)]))
    unified["terrain"] = OrderedDict([("levels", levels)])

    return unified


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
    for color in unified["players"]["availableColors"]:
        if color not in FH2M_PLAYER_COLORS:
            continue
        index = FH2M_PLAYER_COLORS.index(color)
        if index >= len(races):
            continue
        source_race = races[index]
        detail = OrderedDict()
        detail["color"] = color
        detail["race"] = FH2M_RACES.get(source_race)
        detail["sourceRace"] = source_race
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
        ]))
    unified["terrain"] = OrderedDict([
        ("levels", [OrderedDict([("grid", grid)])]),
    ])

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
