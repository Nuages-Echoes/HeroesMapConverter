"""
Identifier tables for the fh2m object metadata.

The fh2m file format stores raw numeric identifiers (monsters, artifacts,
spells, secondary skills). These tables give them readable names used as
the normalized values of the unified format; the raw source identifiers
are preserved in the unified objects so that the fh2m round-trip remains
byte-perfect.

The fh2m identifier spaces follow the fheroes2 engine enumerations
(src/fheroes2/monster/monster.h, spell/spell.h, resource/artifact.h and
heroes/skill.h).
"""

# fh2m resource order: the ADVENTURE_TREASURES group lists the seven
# resources in this order (map_object_info.cpp, populateAdventure
# Treasures), so the object index of a resource is its position here.
FH2M_RESOURCE_ORDER = ["wood", "mercury", "ore", "sulfur", "crystal", "gems", "gold"]

# fheroes2 MonsterType enumeration; index 0 (UNKNOWN) is not a real
# monster. Values above 66 are the random monster placeholders.
FH2M_MONSTER_NAMES = [
    "Unknown",
    "Peasant", "Archer", "Ranger", "Pikeman", "Veteran Pikeman",
    "Swordsman", "Master Swordsman", "Cavalry", "Champion", "Paladin",
    "Crusader", "Goblin", "Orc", "Orc Chief", "Wolf", "Ogre",
    "Ogre Lord", "Troll", "War Troll", "Cyclops", "Sprite", "Dwarf",
    "Battle Dwarf", "Elf", "Grand Elf", "Druid", "Greater Druid",
    "Unicorn", "Phoenix", "Centaur", "Gargoyle", "Griffin", "Minotaur",
    "Minotaur King", "Hydra", "Green Dragon", "Red Dragon", "Black Dragon",
    "Halfling", "Boar", "Iron Golem", "Steel Golem", "Roc", "Mage",
    "Archmage", "Giant", "Titan", "Skeleton", "Zombie", "Mutant Zombie",
    "Mummy", "Royal Mummy", "Vampire", "Vampire Lord", "Lich",
    "Power Lich", "Bone Dragon",
    "Rogue", "Nomad", "Ghost", "Genie", "Medusa", "Earth Element",
    "Air Element", "Fire Element", "Water Element",
    "Random Monster", "Random Monster 1", "Random Monster 2",
    "Random Monster 3", "Random Monster 4",
]

# h3m random monster object classes (RANDOM_MONSTER, RANDOM_MONSTER_L1
# to L4 and the Shadow of Death RANDOM_MONSTER_L5 to L7) -> fh2m random
# monster ids (fheroes2 MonsterType: RANDOM_MONSTER and
# RANDOM_MONSTER_LEVEL_1 to 4). Used when the h3m monsterMetadata
# carries no creature id (creature is None): the object class gives
# the random level. Heroes II random monsters stop at level 4, so the
# h3m levels 5 to 7 are converted to the highest Heroes II level
# (T7 H3 -> T6+ H2 -> Random Monster 4).
H3M_RANDOM_MONSTER_CLASSES = {
    71: 67,  # RANDOM_MONSTER
    72: 68,  # RANDOM_MONSTER_L1
    73: 69,  # RANDOM_MONSTER_L2
    74: 70,  # RANDOM_MONSTER_L3
    75: 71,  # RANDOM_MONSTER_L4
    162: 71,  # RANDOM_MONSTER_L5
    163: 71,  # RANDOM_MONSTER_L6
    164: 71,  # RANDOM_MONSTER_L7
}


# fheroes2 Spell enumeration; index 0 (NONE) is not a real spell.
FH2M_SPELL_NAMES = [
    "None",
    "Fireball", "Fireblast", "Lightning Bolt", "Chain Lightning",
    "Teleport", "Cure", "Mass Cure", "Resurrect", "True Resurrect",
    "Haste", "Mass Haste", "Slow", "Mass Slow", "Blind", "Bless",
    "Mass Bless", "Stoneskin", "Steelskin", "Curse", "Mass Curse",
    "Holy Word", "Holy Shout", "Anti Magic", "Dispel", "Mass Dispel",
    "Magic Arrow", "Berserker", "Armageddon", "Elemental Storm",
    "Meteor Shower", "Paralyze", "Hypnotize", "Cold Ray", "Cold Ring",
    "Disrupting Ray", "Death Ripple", "Death Wave", "Dragonslayer",
    "Bloodlust", "Animate Dead", "Mirror Image", "Shield",
    "Mass Shield", "Summon Earth Element", "Summon Air Element",
    "Summon Fire Element", "Summon Water Element", "Earthquake",
    "View Mines", "View Resources", "View Artifacts", "View Towns",
    "View Heroes", "View All", "Identify Hero", "Summon Boat",
    "Dimension Door", "Town Gate", "Town Portal", "Visions", "Haunt",
    "Set Earth Guardian", "Set Air Guardian", "Set Fire Guardian",
    "Set Water Guardian",
    "Random Spell", "Random Spell 1", "Random Spell 2",
    "Random Spell 3", "Random Spell 4", "Random Spell 5", "Petrify",
]

# fheroes2 Skill::Secondary enumeration; index 0 (UNKNOWN) is not a
# real skill.
FH2M_SECONDARY_SKILL_NAMES = [
    "Unknown",
    "Pathfinding", "Archery", "Logistics", "Scouting", "Diplomacy",
    "Navigation", "Leadership", "Wisdom", "Mysticism", "Luck",
    "Ballistics", "Eagle Eye", "Necromancy", "Estates",
]

# fheroes2 Skill::Level enumeration for secondary skill levels.
FH2M_SKILL_LEVEL_NAMES = ["None", "Basic", "Advanced", "Expert"]

# fheroes2 Monster::JoinCondition enumeration.
FH2M_JOIN_CONDITIONS = {
    -1: "unset",
    0: "skip",
    1: "money",
    2: "free",
}

# fheroes2 Artifact enumeration; index 0 (UNKNOWN) is not a real
# artifact. The Spell Scroll artifact (88) carries a spell id in its
# metadata; the Ultimate and Random editor artifacts (82 to 87) are
# editor placeholders.
FH2M_ARTIFACT_NAMES = [
    "Unknown",
    "Ultimate Book", "Ultimate Sword", "Ultimate Cloak", "Ultimate Wand",
    "Ultimate Shield", "Ultimate Staff", "Ultimate Crown", "Golden Goose",
    "Arcane Necklace", "Caster's Bracelet", "Mage's Ring",
    "Witch's Broach", "Medal of Valor", "Medal of Courage",
    "Medal of Honor", "Medal of Distinction", "Fizbin of Misfortune",
    "Thunder Mace", "Armored Gauntlets", "Defender Helm", "Giant Flail",
    "Ballista", "Stealth Shield", "Dragon Sword", "Power Axe",
    "Divine Breastplate", "Minor Scroll", "Major Scroll",
    "Superior Scroll", "Foremost Scroll", "Endless Sack of Gold",
    "Endless Bag of Gold", "Endless Purse of Gold", "Nomad Boots",
    "Traveler's Boots", "Rabbit's Foot", "Golden Horseshoe",
    "Gambler's Lucky Coin", "Four-Leaf Clover", "True Compass",
    "Sailor's Astrolabe", "Evil Eye", "Enchanted Hourglass",
    "Gold Watch", "Skullcap", "Ice Cloak", "Fire Cloak", "Lightning Helm",
    "Evercold Icicle", "Everhot Lava Rock", "Lightning Rod", "Snake Ring",
    "Ankh", "Book of Elements", "Elemental Ring", "Holy Pendant",
    "Pendant of Free Will", "Pendant of Life", "Serenity Pendant",
    "Seeing-Eye Pendant", "Kinetic Pendant", "Pendant of Death",
    "Wand of Negation", "Golden Bow", "Telescope", "Statesman's Quill",
    "Wizard's Hat", "Power Ring", "Ammo Cart", "Tax Lien",
    "Hideous Mask", "Endless Pouch of Sulfur", "Endless Vial of Mercury",
    "Endless Pouch of Gems", "Endless Cord of Wood",
    "Endless Cart of Ore", "Endless Pouch of Crystal", "Spiked Helm",
    "Spiked Shield", "White Pearl", "Black Pearl",
    "Magic Book",
    "Editor Any Ultimate Artifact",
    "Unused 84", "Unused 85", "Unused 86",
    "Spell Scroll", "Arm of the Martyr", "Breastplate of Anduran",
    "Broach of Shielding", "Battle Garb", "Crystal Ball",
    "Heart of Fire", "Heart of Ice", "Helmet of Anduran",
    "Holy Hammer", "Legendary Scepter", "Masthead",
    "Sphere of Negation", "Staff of Wizardry", "Sword Breaker",
    "Sword of Anduran", "Spade of Necromancy",
]


# fheroes2 BuildingType bit flags (src/fheroes2/castle/castle.h).
FH2M_BUILDING_NAMES = {
    0x00000000: "Nothing",
    0x00000001: "Thieves Guild",
    0x00000002: "Tavern",
    0x00000004: "Shipyard",
    0x00000008: "Well",
    0x00000010: "Statue",
    0x00000020: "Left Turret",
    0x00000040: "Right Turret",
    0x00000080: "Marketplace",
    0x00000100: "Well2",
    0x00000200: "Moat",
    0x00000400: "Spec",
    0x00000800: "Castle",
    0x00001000: "Captain",
    0x00002000: "Shrine",
    0x00004000: "Mage Guild 1",
    0x00008000: "Mage Guild 2",
    0x00010000: "Mage Guild 3",
    0x00020000: "Mage Guild 4",
    0x00040000: "Mage Guild 5",
    0x00080000: "Tent",
    0x00100000: "Dwelling 1",
    0x00200000: "Dwelling 2",
    0x00400000: "Dwelling 3",
    0x00800000: "Dwelling 4",
    0x01000000: "Dwelling 5",
    0x02000000: "Dwelling 6",
    0x04000000: "Upgrade 2",
    0x08000000: "Upgrade 3",
    0x10000000: "Upgrade 4",
    0x20000000: "Upgrade 5",
    0x40000000: "Upgrade 6",
    0x80000000: "Upgrade 7",
}


# Heroes III creature identifiers, in the CRTRAITS.TXT order used by
# the h3m files (Angel... no: the list starts with the Castle faction,
# pikeman first). Indices 122, 124, 126 and 128 do not exist (unused
# slots in the AB creature set); 145-149 are war machines.
H3M_CREATURE_NAMES = [
    "Pikeman", "Halberdier", "Archer", "Marksman", "Griffin",
    "Royal Griffin", "Swordsman", "Crusader", "Monk", "Zealot",
    "Cavalier", "Champion", "Angel", "Archangel",
    "Centaur", "Centaur Captain", "Dwarf", "Battle Dwarf", "Wood Elf",
    "Grand Elf", "Pegasus", "Silver Pegasus", "Dendroid Guard",
    "Dendroid Soldier", "Unicorn", "War Unicorn", "Green Dragon",
    "Gold Dragon",
    "Gremlin", "Master Gremlin", "Stone Gargoyle", "Obsidian Gargoyle",
    "Iron Golem", "Stone Golem", "Mage", "Archmage", "Genie",
    "Master Genie", "Naga", "Naga Queen", "Giant", "Titan",
    "Imp", "Familiar", "Gog", "Magog", "Hell Hound", "Cerberus",
    "Demon", "Horned Demon", "Pit Fiend", "Pit Lord", "Efreet",
    "Efreet Sultan", "Devil", "Arch Devil",
    "Skeleton", "Skeleton Warrior", "Walking Dead", "Zombie Lord",
    "Wight", "Wraith", "Vampire", "Vampire Lord", "Lich", "Power Lich",
    "Black Knight", "Dread Knight", "Bone Dragon", "Ghost Dragon",
    "Troglodyte", "Infernal Troglodyte", "Harpy", "Harpy Hag",
    "Beholder", "Evil Eye", "Medusa", "Medusa Queen", "Minotaur",
    "Minotaur King", "Manticore", "Scorpicore", "Red Dragon",
    "Black Dragon",
    "Goblin", "Hobgoblin", "Goblin Wolf Rider", "Hobgoblin Wolf Rider",
    "Orc", "Orc Chieftain", "Ogre", "Ogre Mage", "Roc", "Thunderbird",
    "Cyclops", "Cyclops King", "Behemoth", "Ancient Behemoth",
    "Gnoll", "Gnoll Marauder", "Lizardman", "Lizard Warrior", "Gorgon",
    "Mighty Gorgon", "Serpent Fly", "Fire Dragon Fly", "Basilisk",
    "Greater Basilisk", "Wyvern", "Wyvern Monarch", "Hydra",
    "Chaos Hydra",
    "Air Elemental", "Earth Elemental",
    "Fire Elemental", "Water Elemental", "Gold Golem", "Diamond Golem",
    "Pixie", "Sprite", "Psychic Elemental", "Magic Elemental",
    None,  # 122: unused
    "Ice Elemental",
    None,  # 124: unused
    "Magma Elemental",
    None,  # 126: unused
    "Storm Elemental",
    None,  # 128: unused
    "Energy Elemental", "Firebird", "Phoenix", "Azure Dragon",
    "Crystal Dragon", "Fairie Dragon", "Rust Dragon", "Enchanter",
    "Sharpshooter", "Halfling", "Peasant", "Boar", "Mummy", "Nomad",
    "Rogue", "Troll",
]

# h3m creature id -> fh2m monster id (fheroes2 MonsterType); -1
# when the creature has no Heroes II equivalent. Within each
# faction the creatures are matched by tier: h3m tier N maps
# to the fh2m tier N creature (see the faction tables in
# heroes_field_correspondence.english.txt).
H3M_TO_FH2M_MONSTERS = {
    0: 1,   # Pikeman -> Peasant (tier 1)
    1: 1,   # Halberdier -> Peasant (tier 1)
    2: 2,   # Archer -> Archer
    3: 3,   # Marksman -> Ranger
    4: 4,   # Griffin -> Pikeman
    5: 5,   # Royal Griffin -> Veteran Pikeman
    6: 6,   # Swordsman -> Swordsman
    7: 7,   # Crusader -> Master Swordsman
    8: 8,   # Monk -> Cavalry
    9: 9,   # Zealot -> Champion
    10: 8,   # Cavalier -> Cavalry
    11: 9,   # Champion -> Champion
    12: 10,   # Angel -> Paladin
    13: 11,   # Archangel -> Crusader
    14: 21,   # Centaur -> Sprite
    15: 21,   # Centaur Captain -> Sprite
    16: 22,   # Dwarf -> Dwarf
    17: 23,   # Battle Dwarf -> Battle Dwarf
    18: 24,   # Wood Elf -> Elf
    19: 25,   # Grand Elf -> Grand Elf
    20: 26,   # Pegasus -> Druid
    21: 27,   # Silver Pegasus -> Greater Druid
    22: 26,   # Dendroid Guard -> Druid
    23: 27,   # Dendroid Soldier -> Greater Druid
    24: 28,   # Unicorn -> Unicorn
    25: 28,   # War Unicorn -> Unicorn
    26: 29,   # Green Dragon -> Phoenix
    27: 29,   # Gold Dragon -> Phoenix
    28: 39,   # Gremlin -> Halfling
    29: 39,   # Master Gremlin -> Halfling
    30: 40,   # Stone Gargoyle -> Boar
    31: 40,   # Obsidian Gargoyle -> Boar
    32: 41,   # Iron Golem -> Iron Golem
    33: 42,   # Stone Golem -> Steel Golem
    34: 43,   # Mage -> Roc
    35: 43,   # Archmage -> Roc
    36: 44,   # Genie -> Mage
    37: 45,   # Master Genie -> Archmage
    38: 46,   # Naga -> Giant
    39: 46,   # Naga Queen -> Giant
    40: 46,   # Giant -> Giant
    41: 47,   # Titan -> Titan
    56: 48,   # Skeleton -> Skeleton
    57: 48,   # Skeleton Warrior -> Skeleton
    58: 49,   # Walking Dead -> Zombie
    59: 50,   # Zombie Lord -> Mutant Zombie
    60: 51,   # Wight -> Mummy
    61: 52,   # Wraith -> Royal Mummy
    62: 53,   # Vampire -> Vampire
    63: 54,   # Vampire Lord -> Vampire Lord
    64: 55,   # Lich -> Lich
    65: 56,   # Power Lich -> Power Lich
    66: 55,   # Black Knight -> Lich
    67: 56,   # Dread Knight -> Power Lich
    68: 57,   # Bone Dragon -> Bone Dragon
    69: 57,   # Ghost Dragon -> Bone Dragon
    70: 30,   # Troglodyte -> Centaur
    71: 30,   # Infernal Troglodyte -> Centaur
    72: 31,   # Harpy -> Gargoyle
    73: 31,   # Harpy Hag -> Gargoyle
    74: 32,   # Beholder -> Griffin
    75: 32,   # Evil Eye -> Griffin
    76: 33,   # Medusa -> Minotaur
    77: 34,   # Medusa Queen -> Minotaur King
    78: 33,   # Minotaur -> Minotaur
    79: 34,   # Minotaur King -> Minotaur King
    80: 35,   # Manticore -> Hydra
    81: 35,   # Scorpicore -> Hydra
    82: 37,   # Red Dragon -> Red Dragon
    83: 38,   # Black Dragon -> Black Dragon
    84: 12,   # Goblin -> Goblin
    85: 12,   # Hobgoblin -> Goblin
    86: 13,   # Goblin Wolf Rider -> Orc
    87: 14,   # Hobgoblin Wolf Rider -> Orc Chief
    88: 15,   # Orc -> Wolf
    89: 15,   # Orc Chieftain -> Wolf
    90: 16,   # Ogre -> Ogre
    91: 17,   # Ogre Mage -> Ogre Lord
    92: 18,   # Roc -> Troll
    93: 19,   # Thunderbird -> War Troll
    94: 20,   # Cyclops -> Cyclops
    95: 20,   # Cyclops King -> Cyclops
    96: 20,   # Behemoth -> Cyclops
    97: 20,   # Ancient Behemoth -> Cyclops
    119: 21,   # Sprite -> Sprite
    118: 21,   # Pixie -> Sprite
    112: 64,   # Air Elemental -> Air Element
    113: 63,   # Earth Elemental -> Earth Element
    114: 65,   # Fire Elemental -> Fire Element
    115: 66,   # Water Elemental -> Water Element
    131: 29,   # Phoenix -> Phoenix
    138: 58,   # Halfling -> Rogue (neutral tier 1)
    139: 58,   # Peasant -> Rogue (neutral tier 1)
    140: 59,   # Boar -> Nomad (neutral tier 2)
    141: 59,   # Mummy -> Nomad (neutral tier 2)
    142: 59,   # Nomad -> Nomad
    143: 58,   # Rogue -> Rogue
    144: 62,   # Troll -> Medusa (neutral tier 3)
    42: 30,   # Imp -> Centaur
    43: 30,   # Familiar -> Centaur
    44: 31,   # Gog -> Gargoyle
    45: 31,   # Magog -> Gargoyle
    46: 32,   # Hell Hound -> Griffin
    47: 32,   # Cerberus -> Griffin
    48: 33,   # Demon -> Minotaur
    49: 34,   # Horned Demon -> Minotaur King
    50: 33,   # Pit Fiend -> Minotaur
    51: 34,   # Pit Lord -> Minotaur King
    52: 35,   # Efreet -> Hydra
    53: 35,   # Efreet Sultan -> Hydra
    54: 36,   # Devil -> Green Dragon
    55: 37,   # Arch Devil -> Red Dragon
    98: 12,   # Gnoll -> Goblin
    99: 12,   # Gnoll Marauder -> Goblin
    100: 13,   # Lizardman -> Orc
    101: 14,   # Lizard Warrior -> Orc Chief
    102: 18,   # Gorgon -> Troll
    103: 19,   # Mighty Gorgon -> War Troll
    104: 15,   # Serpent Fly -> Wolf
    105: 15,   # Fire Dragon Fly -> Wolf
    106: 16,   # Basilisk -> Ogre
    107: 17,   # Greater Basilisk -> Ogre Lord
    108: 20,   # Wyvern -> Cyclops
    109: 20,   # Wyvern Monarch -> Cyclops
    110: 20,   # Hydra -> Cyclops
    111: 20,   # Chaos Hydra -> Cyclops
    118: 21,   # Pixie -> Sprite
    120: 28,   # Psychic Elemental -> Unicorn
    121: 28,   # Magic Elemental -> Unicorn
    123: 66,   # Ice Elemental -> Water Element
    125: 63,   # Magma Elemental -> Earth Element
    127: 64,   # Storm Elemental -> Air Element
    129: 65,   # Energy Elemental -> Fire Element
    130: 29,   # Firebird -> Phoenix
}



def fh2m_building_name(building_id):
    """Name of a fh2m building bit flag, or None when unknown."""
    return FH2M_BUILDING_NAMES.get(building_id)


# fheroes2 Race bit flags (src/fheroes2/kingdom/race.h), used by the
# fh2m heroMetadata race field.
FH2M_RACE_FLAGS = {
    0x00: "None",
    0x01: "Knight",
    0x02: "Barbarian",
    0x04: "Sorceress",
    0x08: "Warlock",
    0x10: "Wizard",
    0x20: "Necromancer",
    0x40: "Multiple",
    0x80: "Random",
}


# fheroes2 id of the Spell Scroll artifact: only this artifact carries
# a spell in its metadata.
FH2M_SPELL_SCROLL_ID = 88


# fh2m KINGDOM_TOWNS object index -> race id (fheroes2 Race bit
# flags): the group lists castle/town pairs per race (index = race
# position * 2, castle first, then town; see map_object_info.cpp,
# populateKingdomTowns).
FH2M_TOWN_INDEX_TO_RACE = {
    0: 0x01, 1: 0x01,
    2: 0x02, 3: 0x02,
    4: 0x04, 5: 0x04,
    6: 0x08, 7: 0x08,
    8: 0x10, 9: 0x10,
    10: 0x20, 11: 0x20,
}

# fh2m town race bit flag -> monster id recruitable in each of the
# six castle dwellings, tier 1 to tier 6 (fheroes2 Monster::FromDwelling).
FH2M_RACE_DWELLING_MONSTERS = {
    0x01: [1, 2, 4, 6, 8, 10],      # Knight: Peasant, Archer, Pikeman, Swordsman, Cavalry, Paladin
    0x02: [12, 13, 15, 16, 18, 20],  # Barbarian: Goblin, Orc, Wolf, Ogre, Troll, Cyclops
    0x04: [21, 22, 24, 26, 28, 29],  # Sorceress: Sprite, Dwarf, Elf, Druid, Unicorn, Phoenix
    0x08: [30, 31, 32, 33, 35, 36],  # Warlock: Centaur, Gargoyle, Griffin, Minotaur, Hydra, Green Dragon
    0x10: [39, 40, 41, 43, 44, 46],   # Wizard: Halfling, Boar, Iron Golem, Roc, Mage, Giant
    0x20: [48, 49, 51, 53, 55, 57],   # Necromancer: Skeleton, Zombie, Mummy, Vampire, Lich, Bone Dragon
}


def fh2m_town_race(town_index):
    """Race bit flag of a fh2m KINGDOM_TOWNS object index, or None."""
    return FH2M_TOWN_INDEX_TO_RACE.get(town_index)


# fheroes2 HeroBase portrait identifiers: a zero or negative custom
# portrait means no customization (the default hero portrait is used).
def fh2m_portrait_name(portrait_id):
    """Describe an fh2m hero portrait customization value."""
    if portrait_id is None or portrait_id <= 0:
        return None
    return "portrait:{}".format(portrait_id)


def fh2m_race_name(race_id):
    """Name of an fh2m race bit flag value, or None when unknown."""
    return FH2M_RACE_FLAGS.get(race_id)


def fh2m_monster_name(monster_id):
    """Name of a fh2m monster id, or None when out of range."""
    if 0 <= monster_id < len(FH2M_MONSTER_NAMES):
        return FH2M_MONSTER_NAMES[monster_id]
    return None


def fh2m_spell_name(spell_id):
    """Name of a fh2m spell id, or None when out of range."""
    if 0 <= spell_id < len(FH2M_SPELL_NAMES):
        return FH2M_SPELL_NAMES[spell_id]
    return None


def fh2m_secondary_skill_name(skill_id):
    """Name of a fh2m secondary skill id, or None when out of range."""
    if 0 <= skill_id < len(FH2M_SECONDARY_SKILL_NAMES):
        return FH2M_SECONDARY_SKILL_NAMES[skill_id]
    return None


def fh2m_skill_level_name(level_id):
    """Name of a fh2m secondary skill level id, or None when out of range."""
    if 0 <= level_id < len(FH2M_SKILL_LEVEL_NAMES):
        return FH2M_SKILL_LEVEL_NAMES[level_id]
    return None


def fh2m_join_condition_name(condition_id):
    """Name of a fh2m monster join condition id."""
    return FH2M_JOIN_CONDITIONS.get(condition_id)


def fh2m_artifact_name(artifact_id):
    """Name of a fh2m artifact id, or None when out of range."""
    if 0 <= artifact_id < len(FH2M_ARTIFACT_NAMES):
        return FH2M_ARTIFACT_NAMES[artifact_id]
    return None

# fh2m monster id -> h3m creature id, the inverse of
# H3M_TO_FH2M_MONSTERS: when several h3m creatures map to the
# same fh2m monster, the preimage is chosen by tier of the
# Heroes II primary faction (see the faction tables in
# heroes_field_correspondence.english.txt), with the validated
# arbitrages: Cavalry/Champion <- Cavalier/Champion,
# Minotaur/Minotaur King <- Minotaur/Minotaur King,
# Lich/Power Lich <- Lich/Power Lich, Mage/Archmage <-
# Mage/Archmage, Giant/Titan <- Giant/Titan, and the dragon
# chain Green <- Red, Red <- Black, Black <- Black.
# fh2m monster id -> h3m creature id: the inverse of the validated
# H3M_TO_FH2M_MONSTERS table (the first h3m creature of each pair).
FH2M_TO_H3M_MONSTERS = {
    1: 0,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 12,
    11: 13,
    12: 84,
    13: 86,
    14: 87,
    15: 88,
    16: 90,
    17: 91,
    18: 92,
    19: 93,
    20: 94,
    21: 14,
    22: 16,
    23: 17,
    24: 18,
    25: 19,
    26: 20,
    27: 21,
    28: 24,
    29: 26,
    30: 70,
    31: 72,
    32: 74,
    33: 76,
    34: 77,
    35: 80,
    36: 54,
    37: 82,
    38: 83,
    39: 28,
    40: 30,
    41: 32,
    42: 33,
    43: 34,
    44: 36,
    45: 37,
    46: 38,
    47: 41,
    48: 56,
    49: 58,
    50: 59,
    51: 60,
    52: 61,
    53: 62,
    54: 63,
    55: 64,
    56: 65,
    57: 68,
    58: 138,
    59: 140,
    62: 144,
    63: 113,
    64: 112,
    65: 114,
    66: 115,
}


# fh2m monsters with no h3m creature equivalent: converted to
# an h3m random monster of level 4 (object class 75).
FH2M_MONSTERS_TO_H3M_RANDOM_CLASS = {
    43: 75,  # Roc (its preimages Mage/Archmage map to Mage/Archmage)
    60: 75,  # Ghost (no ghost creature in Heroes III)
    61: 75,  # Genie
    62: 75,  # Medusa
}

# h3m secondary skill id -> fh2m secondary skill id (the SECSKILL
# order maps to the fheroes2 Skill::Secondary order, offset by one
# because the fh2m ids start at 1). Navigation (h3m id 5) has no
# Heroes II equivalent; the h3m skills 14 to 27 (magic schools,
# Scholar, Tactics, Artillery, Learning, Offence, Armorer,
# Intelligence, Sorcery, Resistance, First Aid) have no Heroes II
# equivalent either.
H3M_TO_FH2M_SECONDARY_SKILLS = {
    0: 1,   # Pathfinding
    1: 2,   # Archery
    2: 3,   # Logistics
    3: 4,   # Scouting
    4: 5,   # Diplomacy
    6: 7,   # Leadership
    7: 8,   # Wisdom
    8: 9,   # Mysticism
    9: 10,  # Luck
    10: 11, # Ballistics
    11: 12, # Eagle Eye
    12: 13, # Necromancy
    13: 14, # Estates
}


# fh2m random monster ids -> h3m random monster object classes
# (inverse of H3M_RANDOM_MONSTER_CLASSES).
FH2M_RANDOM_TO_H3M_CLASS = {
    67: 71,  # Random Monster <- any level
    68: 72,  # Random Monster 1 <- level 1
    69: 73,  # Random Monster 2 <- level 2
    70: 74,  # Random Monster 3 <- level 3
    71: 75,  # Random Monster 4 <- level 4
}

# fh2m artifact id -> h3m artifact id (inverse of
# H3M_TO_FH2M_ARTIFACTS; the forward table is injective).
FH2M_TO_H3M_ARTIFACTS = {
    82: 0,   # Magic Book <- Spell Book
    87: 1,   # Spell Scroll <- Spell Scroll
    22: 4,   # Ballista <- Ballista
    69: 5,   # Ammo Cart <- Ammo Cart
    64: 91,   # Golden Bow <- Golden Bow
    35: 97,   # Traveler's Boots <- Necklace of Swiftness
    40: 98,   # True Compass <- Boots of Speed
    57: 105,   # Pendant of Free Will <- Pendant of Free Will
    77: 109,   # Endless Pouch of Crystal <- Everflowing Crystal Cloak
    74: 110,   # Endless Pouch of Gems <- Ring of Infinite Gems
    73: 111,   # Endless Vial of Mercury <- Everpouring Vial of Mercury
    76: 112,   # Endless Cart of Ore <- Inexhaustible Cart of Ore
    72: 113,   # Endless Pouch of Sulfur <- Eversmoking Ring of Sulfur
    75: 114,   # Endless Cord of Wood <- Inexhaustible Cart of Lumber
    31: 115,   # Endless Sack of Gold <- Endless Sack of Gold
    32: 116,   # Endless Bag of Gold <- Endless Bag of Gold
    33: 117,   # Endless Purse of Gold <- Endless Purse of Gold
}

# fh2m spell id -> h3m spell id (inverse of
# H3M_TO_FH2M_SPELLS; the forward table is injective).
FH2M_TO_H3M_SPELLS = {
    56: 0,   # Summon Boat <- Summon Boat
    60: 2,   # Visions <- Visions
    49: 3,   # View Mines <- View Earth
    53: 5,   # View Heroes <- View Air
    57: 8,   # Dimension Door <- Dimension Door
    59: 9,   # Town Portal <- Town Portal
    48: 14,   # Earthquake <- Earthquake
    26: 15,   # Magic Arrow <- Magic Arrow
    3: 17,   # Lightning Bolt <- Lightning Bolt
    4: 19,   # Chain Lightning <- Chain Lightning
    1: 21,   # Fireball <- Fireball
    30: 23,   # Meteor Shower <- Meteor Shower
    36: 24,   # Death Ripple <- Death Ripple
    28: 26,   # Armageddon <- Armageddon
    42: 27,   # Shield <- Shield
    23: 34,   # Anti Magic <- Anti Magic
    24: 35,   # Dispel <- Dispel
    6: 37,   # Cure <- Cure
    40: 39,   # Animate Dead <- Animate Dead
    15: 41,   # Bless <- Bless
    19: 42,   # Curse <- Curse
    39: 43,   # Bloodlust <- Bloodlust
    17: 46,   # Stoneskin <- Stone Skin
    35: 47,   # Disrupting Ray <- Disrupting Ray
    10: 53,   # Haste <- Haste
    12: 54,   # Slow <- Slow
    32: 60,   # Hypnotize <- Hypnotize
    14: 62,   # Blind <- Blind
    5: 63,   # Teleport <- Teleport
}

# fh2m mine object index -> h3m (class, subclass). The Heroes II
# mines: index 0-39 are the 5 resources (ore, sulfur, crystal,
# gems, gold in the order) x 8 appearances (generic, grass, snow,
# swamp, lava, desert, dirt, wasteland), 40-44 the abandoned mines,
# 45-46 the sawmills, 47-48 the alchemist labs. The h3m class 53
# subclass identifies the mine type: 0 sawmill, 1 alchemist lab,
# 2 ore, 3 sulfur, 4 crystal, 5 gems, 6 gold, 7 abandoned.
FH2M_TO_H3M_MINES = {}
_mine_resources = [2, 3, 4, 5, 6]  # ore, sulfur, crystal, gems, gold
for _appearance in range(8):
    for _res_index, _subclass in enumerate(_mine_resources):
        FH2M_TO_H3M_MINES[_appearance * 5 + _res_index] = (53, _subclass)
for _i in range(5):
    FH2M_TO_H3M_MINES[40 + _i] = (53, 7)  # abandoned mines
FH2M_TO_H3M_MINES[45] = (53, 0)  # sawmill grass/swamp
FH2M_TO_H3M_MINES[46] = (53, 0)  # sawmill other
FH2M_TO_H3M_MINES[47] = (53, 1)  # alchemist lab
FH2M_TO_H3M_MINES[48] = (53, 1)  # alchemist lab snow

# fh2m dwelling object index -> h3m (class, subclass). The Heroes
# II dwellings house a Heroes II creature; the h3m dwelling class
# 17 carries the paired h3m creature id as its subclass (see the
# FH2M_TO_H3M_MONSTERS creature table). The dwellings whose
# creature has no h3m pairing map to subclass 0.
FH2M_TO_H3M_DWELLINGS = {
    0: (17, 0),  # Peasant -> Pikeman
    1: (17, 144),  # Medusa -> Troll
    2: (17, 14),  # Sprite -> Centaur
    3: (17, 86),  # Orc -> Goblin Wolf Rider
    4: (17, 86),  # Orc -> Goblin Wolf Rider
    5: (17, 28),  # Halfling -> Gremlin
    6: (17, 28),  # Halfling -> Gremlin
    7: (17, 14),  # Sprite -> Centaur
    8: (17, 14),  # Sprite -> Centaur
    9: (17, 140),  # Nomad -> Boar
    10: (17, 64),  # Lich -> Lich
    11: (17, 56),  # Skeleton -> Skeleton
    12: (17, 92),  # Troll -> Roc
    13: (17, 2),  # Archer -> Archer
    14: (17, 84),  # Goblin -> Goblin
    15: (17, 16),  # Dwarf -> Dwarf
    16: (17, 91),  # Ogre Lord -> Ogre Mage
    17: (17, 138),  # Rogue -> Halfling
    18: (17, 70),  # Centaur -> Troglodyte
    19: (17, 70),  # Centaur -> Troglodyte
    20: (17, 0),  # Ghost -> ?
    21: (17, 94),  # Cyclops -> Cyclops
    22: (17, 14),  # Sprite -> Centaur
    23: (17, 16),  # Dwarf -> Dwarf
    24: (17, 17),  # Battle Dwarf -> Battle Dwarf
}


# fh2m landscape object index -> h3m decorative class. The Heroes
# II landscape groups carry one entry per sprite variant; each maps
# to the closest h3m decorative family class (the h3m encoder writes
# the representative sprite of the class).
FH2M_LANDSCAPE_TO_H3M = {
    # TREES: forests and grass/dirt trees -> deciduous trees (155),
    # snow/swamp stumps and dead trees -> dead trees (119), palms ->
    # palm trees (125).
    **{("LANDSCAPE_TREES", i): 155 for i in (0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23)},
    **{("LANDSCAPE_TREES", i): 119 for i in (8, 9, 10, 11, 12, 13, 14, 15, 16, 24, 25, 26, 27, 28)},
    **{("LANDSCAPE_TREES", i): 125 for i in (17, 18, 19, 20)},
    # The additional tree variants (the loop-generated entries
    # 29-62: more dead trees, palms, dirt trees and stumps) -> the
    # h3m tree classes; the encoder refines by tile terrain.
    **{("LANDSCAPE_TREES", i): 155 for i in range(29, 63)},
    # MOUNTAINS: 8 terrains x 19 variants (index = terrain * 19 +
    # variant); all map to the h3m mountains (134) - the exact
    # variant index formula is not documented, so a generic
    # mountain is the safe visual choice.
    **{("LANDSCAPE_MOUNTAINS", i): 134 for i in range(152)},
    # ROCKS: all the 40 entries (33 + the loop variants) -> rocks
    # (147).
    **{("LANDSCAPE_ROCKS", i): 147 for i in range(40)},

    # WATER: rocks -> rocks (147), aquatic plants and reefs ->
    # water plants (29).
    **{("LANDSCAPE_WATER", i): 147 for i in (0, 1, 2, 3)},
    **{("LANDSCAPE_WATER", i): 29 for i in (4, 5, 6, 7, 8, 9, 10, 11)},
    # MISCELLANEOUS: cracks, dug holes, cliffs and craters -> cracks
    # (118), shrubs -> shrubs (150), flowers -> flowers (120), water
    # and swampy lakes -> water plants (29), mandrakes and reeds ->
    # mandrakes (131), lava pools and volcano craters -> lava lakes
    # (127), cacti -> cacti (116), meadows and grass -> shrubs (150),
    # tar pits and cow skulls -> debris (161), river deltas -> water
    # plants (29).
    **{("LANDSCAPE_MISCELLANEOUS", i): 118 for i in
       (0, 1, 2, 3, 19, 20, 21, 22, 23, 24, 29, 31, 53, 54, 55, 58,
        68, 79, 81, 82, 97, 98, 99, 104, 105, 108, 109, 110)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 150 for i in
       (7, 8, 9, 10, 25, 30, 48, 49, 50, 51, 86, 87, 103, 106, 111)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 120 for i in
       (11, 12, 13, 14, 15, 16, 17, 18, 88, 89, 90, 91, 92)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 29 for i in
       (4, 5, 6, 26, 27, 28, 32, 33, 34, 40, 41, 42, 83, 84, 85,
        112, 113, 114, 115)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 131 for i in
       (35, 36, 37, 38, 39, 43, 44, 45, 46, 47, 52)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 127 for i in
       (56, 57, 59, 60, 61, 62, 63, 64, 65, 66, 67)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 116 for i in
       (69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 100, 101)},
    **{("LANDSCAPE_MISCELLANEOUS", i): 161 for i in (80, 93, 94, 95, 96, 102, 107)},
    # The loop-generated variants (116-146: more cracks, shrubs,
    # flowers, lakes...) map to the same families by modulo of
    # their base variant; the unmapped ones default to cracks
    # (118).
    **{("LANDSCAPE_MISCELLANEOUS", i): 118 for i in range(116, 147)},
}


# fh2m resource object index (ADVENTURE_TREASURES 0-6: wood,
# mercury, ore, sulfur, crystal, gems, gold) -> h3m resource
# subclass (the h3m class 79 subclass values, the same order).
FH2M_TO_H3M_RESOURCES = {i: i for i in range(7)}


# Reference h3m object sprites extracted from real maps: (class,
# subclass) -> (sprite name, 16 passability/actionability bytes hex,
# 18 trailing unknown bytes hex). Used by the h3m object encoder.
FH2M_TO_H3M_CATALOG = {
    (2, 0): ("AvXAltar.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (4, 0): ("AVSarna0.def", "ffffffff1f1f000000000040ff010500", "000000000000000000000000000000000000"),
    (5, 7): ("AVA0007.def", "ffffffffff7f000000000080ff000100", "040000000000000000000000000000000000"),
    (5, 13): ("AVA0013.def", "ffffffffff7f000000000080ff000100", "040000000000000000000000000000000000"),
    (5, 33): ("AVA0033.def", "ffffffffff7f000000000080ff000100", "040000000000000000000000000000000000"),
    (5, 51): ("AVA0051.def", "ffffffffff7f000000000080ff000100", "040000000000000000000000000000000000"),
    (5, 55): ("AVA0055.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (5, 65): ("AVA0065.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (5, 123): ("AVA0123.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (5, 125): ("AVA0125.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (6, 0): ("AVA0128.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (7, 0): ("AVXmktb0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (8, 1): ("AVXboat1.def", "ffffffffffbf00000000004000010001", "000000000000000000000000000000000000"),
    (8, 2): ("AVXboat2.def", "ffffffffffbf00000000004000010001", "000000000000000000000000000000000000"),
    (9, 0): ("AVXbor00.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (9, 2): ("AVXbor20.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (10, 0): ("AVXkey00.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (10, 2): ("AVXkey20.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (11, 0): ("AVSbuoy0.def", "ffffffffff7f00000000008000010001", "000000000000000000000000000000000000"),
    (12, 0): ("adcfra.def", "ffffffffff7f000000000080ff013500", "000000000000000000000000000000000000"),
    (13, 0): ("AVXmapw0.def", "ffffffffff3f000000000040ff010001", "000000000000000000000000000000000000"),
    (13, 1): ("AVXmaps0.def", "ffffffffff3f000000000040ff01bf00", "000000000000000000000000000000000000"),
    (13, 2): ("AVXmapu0.def", "ffffffffff3f000000000040ff014000", "000000000000000000000000000000000000"),
    (14, 0): ("AVSclvg0.def", "ffffffffff3f000000000040ff010400", "000000000000000000000000000000000000"),
    (15, 0): ("AVXcovr0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (16, 0): ("AVXbnk10.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (16, 1): ("AVXbnk20.def", "ffffffffff1f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (16, 2): ("AVXbnk30.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (16, 3): ("AVXbnk40.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (16, 4): ("AVXbnk50.def", "ffffffffff3f000000000040ff01bf00", "000000000000000000000000000000000000"),
    (16, 5): ("AVXbnk60.def", "ffffffffff3f000000000040ff00ff00", "000000000000000000000000000000000000"),
    (16, 6): ("AVXbnk70.def", "ffffffffffbf000000000040ff00ff00", "000000000000000000000000000000000000"),
    (17, 1): ("AVGbhmt0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 3): ("AVGbkni0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 4): ("AVGbone0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 5): ("AVGcavl0.def", "ffffffffff3f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 6): ("AVGcent0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 8): ("AVGangl0.def", "ffffffffff9f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 10): ("AVGdevl0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 11): ("AVGdfly0.def", "ffffffffff3f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 12): ("AVGdwrf0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 15): ("AVGelf0.def", "ffffffffff3f000000000040ff00ff00", "000000000000000000000000000000000000"),
    (17, 17): ("AVGgarg0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 19): ("AVGwolf0.def", "ffffffffbf3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 20): ("AVGgnll0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 21): ("AVGgobl0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 22): ("AVGgogs0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 24): ("AVGgdrg0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 25): ("AVGgrff0.def", "ffffffffff3f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 26): ("AVGharp0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 28): ("AVGhydr0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 29): ("AVGimp0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 30): ("AVGlzrd0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 35): ("AVGmonk0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 37): ("AVGdemn0.def", "ffffffffff3f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 39): ("AVGorcg0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 41): ("AVGrdrg0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (17, 43): ("AVGgrem0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 44): ("AVGtitn0.def", "ffffffffbf3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 46): ("AVGtrog0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 49): ("AVGwyvn0.def", "ffffffffff3f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (17, 54): ("AVGskel0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 55): ("AVGzomb0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 56): ("AVGpike0.def", "ffffffffbf3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (17, 57): ("AVGcros0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (21, 0): ("AVXcrsd0.def", "ffffffffffff000000000000ff00ff00", "000100000000000000000000000000000000"),
    (22, 0): ("AVXskds0.def", "ffffffffff7f000000000080ff012200", "000000000000000000000000000000000000"),
    (23, 0): ("AvSMarl.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (24, 0): ("AVAdlic0.def", "ffffffffff3f00000000004000010001", "000000000000000000000000000000000000"),
    (26, 0): ("AVZevnt0.def", "ffffffffff7f000000000080ff01ff01", "000000000000000000000000000000000000"),
    (27, 0): ("AVXeyem0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (28, 0): ("AVSring0.def", "ffffffffff3f000000000040ff011500", "000000000000000000000000000000000000"),
    (29, 0): ("AVAflot0.def", "ffffffffff7f00000000008000010001", "000000000000000000000000000000000000"),
    (30, 0): ("AVSfntn0.def", "ffffffffff7f000000000080ff011500", "000000000000000000000000000000000000"),
    (31, 0): ("AVXfyth0.def", "ffffffff3f3f000000000080ff011500", "000000000000000000000000000000000000"),
    (32, 0): ("AVSgrdn0.def", "ffffffffff7f000000000080ff015500", "000000000000000000000000000000000000"),
    (33, 0): ("AVCgar10.def", "ffffffffff1f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (35, 0): ("AVXhild0.def", "ffffffffff1f000000000080ff000100", "000000000000000000000000000000000000"),
    (37, 0): ("AVXhutm0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (38, 0): ("AVSidol0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (39, 0): ("AVMlean0.def", "ffffffffff3f000000000080ff010800", "000000000000000000000000000000000000"),
    (41, 0): ("AVSlibr0.def", "ffffffff3f0f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (42, 0): ("AVXlths0.def", "ffffffffff7f000000000080ff01bf00", "000000000000000000000000000000000000"),
    (43, 0): ("AVXmn1b0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (43, 1): ("AVXmn1r0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (44, 0): ("AVXmx1b0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (44, 1): ("AVXmx1r0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (45, 0): ("AVXmn2g0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (45, 1): ("AVXmn2o0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (45, 2): ("AVXmn2p0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (46, 0): ("AVXplns0.def", "ffffffffffff000000000000ff00ff00", "000100000000000000000000000000000000"),
    (47, 0): ("AVSschm0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (48, 0): ("AVXmags0.def", "ffffffffff3f0000000000c0ff012000", "000000000000000000000000000000000000"),
    (49, 0): ("AVXwelg0.def", "ffffffffff7f000000000080ff011500", "000000000000000000000000000000000000"),
    (51, 0): ("AVSmerc0.def", "ffffffffff1f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (52, 0): ("AVXmerm0.def", "ffffffffff1f00000000004000010001", "000000000000000000000000000000000000"),
    (53, 0): ("AVMsawg0.def", "ffffffff3f0f000000000040ff011400", "000000000000000000000000000000000000"),
    (53, 1): ("AVMalch0.def", "ffffffffff1f000000000040ff010700", "000000000000000000000000000000000000"),
    (53, 2): ("AVMore0.def", "ffffffff1f1f000000000040ff010400", "000100000000000000000000000000000000"),
    (53, 3): ("AVMsulf0.def", "ffffffffff1f000000000040ff010700", "000000000000000000000000000000000000"),
    (53, 4): ("AVMcrdr0.def", "ffffffffff1f000000000040ff010100", "000000000000000000000000000000000000"),
    (53, 5): ("AVMgems0.def", "ffffffff1f1f000000000040ff011400", "000100000000000000000000000000000000"),
    (53, 6): ("AVMgovo0.def", "ffffffffff1f000000000040ff018000", "000000000000000000000000000000000000"),
    (53, 7): ("AVXabnd0.def", "ffffffffff1f000000000040ff010100", "000000000000000000000000000000000000"),
    (54, 2): ("AvWLCrs.def", "ffffffffff7f000000000080ff000400", "020000000000000000000000000000000000"),
    (54, 4): ("AvWGrif.def", "ffffffffff7f000000000080ff000400", "020000000000000000000000000000000000"),
    (54, 6): ("AVWswrd0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 7): ("AVWswrx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 9): ("AVWmonx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 11): ("AVWcvlx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 12): ("AvWAngl.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 14): ("AVWcent0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 15): ("AVWcenx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 16): ("AVWdwrf0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 17): ("AVWdwrx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 18): ("AVWelfw0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 19): ("AVWelfx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 22): ("AVWtree0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 23): ("AVWtrex0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 24): ("AVWunic0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 25): ("AVWunix0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 26): ("AVWdrag0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 29): ("AVWgrex0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 30): ("AVWgarg0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 31): ("AVWgarx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 33): ("AVWgolx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 34): ("AVWmage0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 35): ("AVWmagx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 38): ("AVWnaga0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 42): ("AVWimp0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 45): ("AVWgogx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 46): ("AVWhoun0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 47): ("AVWhoux0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 48): ("AVWdemn0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 49): ("AVWdemx0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 51): ("AVWpitx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 57): ("AVWskex0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 58): ("AVWzomb0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 59): ("AVWzomx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 61): ("AVWwigx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 67): ("AVWbknx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 70): ("AVWtrog0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 71): ("AvWInfr.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 72): ("AVWharp0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 74): ("AVWbehl0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 75): ("AVWbehx0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 76): ("AvWMeds.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 78): ("AvWMino.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 79): ("AVWminx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 83): ("AVWddrx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 90): ("AVWogre0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 91): ("AVWogrx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 94): ("AVWcycl0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 95): ("AVWcycx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 99): ("AVWgnlx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 101): ("AVWlizx0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 103): ("AVWgorx0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (54, 104): ("AvWDFly.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 105): ("AvWDFir.def", "ffffffffff7f000000000080ff010400", "020000000000000000000000000000000000"),
    (54, 108): ("AvWWyvr.def", "ffffffffff7f000000000080ff000400", "020000000000000000000000000000000000"),
    (54, 112): ("AVWelma0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 114): ("AVWelmf0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 115): ("AVWelmw0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 116): ("AVWglmg0.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (55, 0): ("AVTmyst0.def", "ffffffffff1f000000000040ff011500", "000000000000000000000000000000000000"),
    (57, 0): ("AvXOblW.def", "ffffffffff7f000000000080ff010400", "000000000000000000000000000000000000"),
    (58, 0): ("AvXRedW.def", "ffffffffff7f000000000080ff01bf00", "000000000000000000000000000000000000"),
    (59, 0): ("AVXbttl0.def", "ffffffffff7f00000000008000010001", "000000000000000000000000000000000000"),
    (60, 0): ("AVXpllr0.def", "ffffffffff7f00000000008040004000", "000000000000000000000000000000000000"),
    (61, 0): ("AVSaxis0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (62, 0): ("AVXprsn0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (63, 0): ("AVXprmd0.def", "ffffffffff3f000000000080ff010200", "000000000000000000000000000000000000"),
    (64, 0): ("AVXrlly0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (65, 0): ("AVArand.def", "ffffffffff7f000000000080ff000100", "040000000000000000000000000000000000"),
    (66, 0): ("AVArnd1.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (67, 0): ("AVArnd2.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (68, 0): ("AVArnd3.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (69, 0): ("AVArnd4.def", "ffffffffff7f000000000080ff010100", "040000000000000000000000000000000000"),
    (71, 0): ("AVWmrnd0.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (72, 0): ("AVWmon1.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (73, 0): ("AVWmon2.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (74, 0): ("AVWmon3.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (75, 0): ("AVWmon4.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (76, 0): ("AVTrndm0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (77, 0): ("AVCranx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (78, 0): ("AVGrefg0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (79, 0): ("AVTwood0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (79, 1): ("AVTmerc0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (79, 2): ("AVTore0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (79, 3): ("AVTsulf0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (79, 4): ("AVTcrys0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (79, 5): ("AVTgems0.def", "ffffffffff7f000000000080ff01ff00", "050000000000000000000000000000000000"),
    (79, 6): ("AVTgold0.def", "ffffffffff7f000000000080ff010100", "050000000000000000000000000000000000"),
    (80, 0): ("AVXsanc0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (81, 0): ("AVXschl0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (82, 0): ("AVXccht0.def", "ffffffffff7f00000000008000010001", "000000000000000000000000000000000000"),
    (83, 0): ("AVXseer0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (83, 1): ("AVXseey0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (83, 2): ("AVXseeb0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (84, 0): ("AVXgyne0.def", "ffffffffff1f000000000040ff011500", "000000000000000000000000000000000000"),
    (85, 0): ("AVAwre20.def", "ffffffffff3f00000000008000010001", "000000000000000000000000000000000000"),
    (86, 0): ("AVAsurv0.def", "ffffffffff7f00000000008000010001", "000000000000000000000000000000000000"),
    (87, 0): ("AVXshyd0.def", "ffffffffff1f000000000040ff00ff00", "000000000000000000000000000000000000"),
    (88, 0): ("AVXl1sh0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (89, 0): ("AVXl2sh0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (90, 0): ("AVXl3sh0.def", "ffffffffff7f000000000080ff00ff00", "000000000000000000000000000000000000"),
    (91, 0): ("AVXsndg0.def", "ffffffffff7f000000000080ff004500", "000000000000000000000000000000000000"),
    (92, 0): ("AVXsirn0.def", "ffffffffff1f00000000004000010001", "000000000000000000000000000000000000"),
    (94, 0): ("AVXstbl0.def", "ffffffffff3f000000000080ff012500", "000000000000000000000000000000000000"),
    (95, 0): ("AVXtvrn0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (96, 0): ("AVStmpl0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (97, 0): ("AVXdend0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (98, 0): ("AVCcasx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 1): ("AVCramx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 2): ("AVCtowx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 3): ("AVCinfx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 4): ("AVCnecx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 5): ("AVCdunx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 6): ("AVCstrx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (98, 7): ("AVCftrx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
    (99, 0): ("AVXpost0.def", "ffffffffff3f000000000080ff010500", "000000000000000000000000000000000000"),
    (100, 0): ("AVSgzbo0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (101, 0): ("AVTchst0.def", "ffffffffff7f000000000080ff01ff00", "050000000000000000000000000000000000"),
    (102, 0): ("AVXtrek0.def", "ffffffffffbf000000000040ff010500", "000000000000000000000000000000000000"),
    (103, 0): ("AvTCave.def", "ffffffffbf1f000000000040ff00ff00", "000000000000000000000000000000000000"),
    (104, 0): ("AVSuniv0.def", "ffffff8f0f0f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (105, 0): ("AVTwagn0.def", "ffffffffff7f000000000080ff012000", "000000000000000000000000000000000000"),
    (106, 0): ("AVGsieg0.def", "ffffffffff3f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (107, 0): ("AVSwar20.def", "ffffff9f0f9f000000000040ff01ff00", "000000000000000000000000000000000000"),
    (108, 0): ("AVXtomb0.def", "ffffffffff3f000000000080ff01ff00", "000000000000000000000000000000000000"),
    (109, 0): ("AVMwwhl0.def", "ffffffff1f1f000000000080ff011500", "000000000000000000000000000000000000"),
    (110, 0): ("AVXwtrh0.def", "ffffffffff0f0000000000f0ff012000", "000000000000000000000000000000000000"),
    (111, 0): ("AVXwhrl0.def", "ffffffff1f1f00000000e0e000010001", "000100000000000000000000000000000000"),
    (112, 0): ("AVMwndd0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (113, 0): ("AVSwtch0.def", "ffffffffffbf000000000040ff01ff00", "000000000000000000000000000000000000"),
    (116, 0): ("AVLca010.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    (117, 0): ("AVLglly0.def", "ffffffcf0f3f000000000000ff002000", "000100000000000000000000000000000000"),
    (118, 0): ("AVLct4l0.def", "ffffffff3fbf000000000000ff018000", "000100000000000000000000000000000000"),
    (119, 0): ("AVLswp70.def", "ffffffffff7f000000000000ff011000", "000100000000000000000000000000000000"),
    (120, 0): ("AVLf01g0.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    (121, 0): ("AVLflk10.def", "ffffffff0707000000000000ff010800", "000100000000000000000000000000000000"),
    (124, 0): ("AVLholg0.def", "ffffffffffff00000000000004000400", "000100000000000000000000000000000000"),
    (125, 0): ("AVLklp10.def", "ffffffffffff000000000000ff010001", "000100000000000000000000000000000000"),
    (126, 0): ("AVLlk1g0.def", "ffffff07078f000000000000ff010400", "000100000000000000000000000000000000"),
    (127, 0): ("AVLlv110.def", "ffffffff3f3f000000000000ff018000", "000100000000000000000000000000000000"),
    (128, 0): ("AVLlav10.def", "ffffffff3f3f000000000000ff018000", "000100000000000000000000000000000000"),
    (129, 0): ("AVLms100.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    (130, 0): ("AvLdlog.def", "ffffffffff7f000000000000ff012500", "000000000000000000000000000000000000"),
    (131, 0): ("AVLman40.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    (132, 0): ("AVLmoss0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    (133, 0): ("AVLmd1g0.def", "ffffffffff3f00000000000004000400", "000000000000000000000000000000000000"),
    (134, 0): ("AVLmtsn2.def", "ffffff0f07c7000000000000ff010800", "000000000000000000000000000000000000"),
    (135, 0): ("AVLautr7.def", "ffffff3f1f9f000000000000ff010500", "000000000000000000000000000000000000"),
    (136, 0): ("AVLoc2d0.def", "ffffffffff3f000000000000ff010100", "000100000000000000000000000000000000"),
    (137, 0): ("AVLPNTR3.def", "ffffffff3f9f000000000000ff010500", "000000000000000000000000000000000000"),
    (143, 0): ("clrdelt4.def", "ffffffffffff000000000000ff013800", "000100000000000000000000000000000000"),
    (147, 0): ("AVLrk4w0.def", "ffffffffff7f000000000000ff010001", "000000000000000000000000000000000000"),
    (148, 0): ("AVLdun10.def", "ffffffffff3f000000000000ff010200", "000000000000000000000000000000000000"),
    (149, 0): ("AVLspit0.def", "ffffffffff1f000000000000ff010200", "000100000000000000000000000000000000"),
    (150, 0): ("AVLsh4g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    (151, 0): ("AVLskul0.def", "ffffffffff7f000000000000ff012200", "000000000000000000000000000000000000"),
    (153, 0): ("AvLStm2.def", "ffffffffff7f000000000000ff012500", "000000000000000000000000000000000000"),
    (155, 0): ("AVLroug0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    (158, 0): ("AVLvol40.def", "ffffffffbf1f000000000000ff018000", "000000000000000000000000000000000000"),
    (161, 0): ("AVLref30.def", "ffffffff3f3f000000000000ff010001", "000100000000000000000000000000000000"),
    (162, 0): ("AVWmon5.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (163, 0): ("AVWmon6.def", "ffffffffff7f000000000080ff000100", "020000000000000000000000000000000000"),
    (164, 0): ("AVWmon7.def", "ffffffffff7f000000000080ff010100", "020000000000000000000000000000000000"),
    (54, 0): ("avwpike.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Pikeman
    (54, 5): ("avwgrix0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Royal Griffin
    (54, 3): ("avwhcrs.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Marksman
    (54, 84): ("avwgobl0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Goblin
    (54, 86): ("avwwolf0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Goblin Wolf Rider
    (54, 88): ("avworc0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Orc
    (54, 93): ("avwrocx0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Thunderbird (Roc upgrade)
    (54, 28): ("avwgrem0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Gremlin
    (56, 0): ("AVXosis0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),  # Oasis
}

# fh2m hero race id (the KINGDOM_HEROES object index modulo 7:
# 0 Knight, 1 Barbarian, 2 Sorceress, 3 Warlock, 4 Wizard,
# 5 Necromancer, 6 random) -> the first h3m hero id of the paired
# faction (the 144 h3m heroes are ordered by 16 per faction:
# Castle 0, Rampart 16, Tower 32, Inferno 48, Necropolis 64,
# Dungeon 80, Stronghold 96, Fortress 112).
FH2M_TO_H3M_HERO_RACE = {
    0: 0,    # Knight -> Castle (Orrin)
    1: 96,   # Barbarian -> Stronghold (Yog)
    2: 16,   # Sorceress -> Rampart (Mephala? no: Jenova)
    3: 80,   # Warlock -> Dungeon (Lorelei)
    4: 32,   # Wizard -> Tower (Piquedram)
    5: 64,   # Necromancer -> Necropolis (Straker)
}


# fh2m shrine circle index (ADVENTURE_POWER_UPS 14 First Circle,
# 15 Second Circle, 16 Third Circle) -> the h3m shrine class (88
# Incantation, 89 Gesture, 90 Thought). The Heroes II Shrine of
# Magic Mystery converts to the Third Circle as well.
FH2M_TO_H3M_SHRINES = {
    14: 88,  # Shrine of the First Circle -> Magic Incantation
    15: 89,  # Shrine of the Second Circle -> Magic Gesture
    16: 90,  # Shrine of the Third Circle -> Magic Thought
}


# fh2m miscellaneous/water object index -> h3m (class, subclass).
# Only the objects with a confirmed h3m sprite in the reference
# catalog are mapped; the others (obelisk, oracle, pyramid, PoL
# objects...) stay dropped until their h3m classes are confirmed.
FH2M_TO_H3M_MISC = {
    # MISC: windmills -> windmill (112), lean-tos -> lean-to (39),
    # signs -> sign (91), water wheels -> water wheel (109),
    # witch's hut -> witch hut (113), stone liths -> two-way
    # monolith (42), daemon caves -> subterranean gate? no: dropped,
    # sphinx -> seer hut (83) [the sphinx riddle], magic garden ->
    # ... dropped, trading post -> market of trading? (7) dropped.
    "MISC_4": (112, 0),   # Windmill, grass
    "MISC_5": (112, 0),   # Windmill, snow
    "MISC_6": (112, 0),   # Windmill, dirt
    "MISC_16": (39, 0),   # Lean-to, snow
    "MISC_17": (39, 0),   # Lean-to, grass
    "MISC_18": (91, 0),   # Sign, snow
    "MISC_19": (91, 0),   # Sign, swamp
    "MISC_20": (91, 0),   # Sign, lava
    "MISC_21": (91, 0),   # Sign, desert
    "MISC_22": (91, 0),   # Sign, generic
    "MISC_23": (109, 0),  # Water wheel, snow
    "MISC_24": (109, 0),  # Water wheel, generic
    "MISC_26": (113, 0),  # Witch's Hut, swamp
    "MISC_35": (42, 0),   # Stone Liths, generic
    "MISC_36": (42, 0),   # Stone Liths, generic 2
    "MISC_37": (42, 0),   # Stone Liths, Resurrection variant
    "MISC_41": (99, 0),   # Observation Tower, grass -> lookout tower (99)
    "MISC_42": (99, 0),   # Observation Tower, generic
    "MISC_43": (99, 0),   # Observation Tower, desert
    "MISC_44": (99, 0),   # Observation Tower, snow
    # POWER_UPS: the Gazebo (index 11) maps to the h3m learning
    # stone (100 - the inverse pairing: the h3m learning stone
    # converts to the Heroes II Gazebo); the other power-ups stay
    # dropped or map through the shrines.
    "POWER_11": (100, 0),  # Gazebo -> learning stone
    # Power-up pairings (per user decision): the Heroes II
    # power-ups map to their h3m counterparts.
    "POWER_0": (48, 0),    # Artesian Spring -> Magic Spring
    "POWER_1": (110, 0),   # Watering Hole -> Watering Hole
    "POWER_2": (28, 0),    # Faerie Ring -> Faerie Ring
    "POWER_3": (28, 0),    # Faerie Ring variant -> Faerie Ring
    "POWER_4": (28, 0),    # Faerie Ring variant -> Faerie Ring
    "POWER_5": (56, 0),    # Oasis -> Oasis
    "POWER_6": (30, 0),    # Fountain -> Fountain of Fortune
    "POWER_10": (23, 0),   # Fort -> Marletto Tower
    "POWER_12": (32, 0),   # Witch Doctor's Hut -> Garden of Revelation
    "POWER_13": (51, 0),   # Mercenary Camp -> Mercenary Camp
    "POWER_18": (61, 0),   # Standing Stones -> Star Axis
    "POWER_19": (96, 0),   # Temple -> Temple
    "POWER_21": (41, 0),   # Xanadu -> Library of Enlightenment
    "POWER_22": (4, 0),     # Arena -> Arena
    # TREASURES: Genie's Lamp -> Refugee Camp (the h3m creature
    # vendor); Random Resource -> random resource (76); Treasure
    # Chest -> treasure chest (101); campfires -> campfire (12).
    "TREASURE_7": (78, 0),   # Genie's Lamp -> Refugee Camp
    "TREASURE_8": (76, 0),   # Random Resource -> random resource
    "TREASURE_9": (101, 0),  # Treasure Chest -> treasure chest
    "TREASURE_10": (12, 0),   # Campfire -> campfire
    "TREASURE_11": (12, 0),   # Campfire on show -> campfire
    "TREASURE_12": (12, 0),   # Campfire in desert -> campfire
    # Obelisks (the ADVENTURE_MISCELLANEOUS terrain variants,
    # keyed MISC_x to avoid colliding with the ADVENTURE_TREASURES
    # indexes) -> obelisk (57 - the same puzzle-map mechanic in
    # both games).
    "MISC_9": (57, 0),    # Obelisk, grass
    "MISC_10": (57, 0),   # Obelisk, snow
    "MISC_11": (57, 0),   # Obelisk, swamp
    "MISC_12": (57, 0),   # Obelisk, lava
    "MISC_13": (57, 0),   # Obelisk, desert
    "MISC_14": (57, 0),   # Obelisk, wasteland
    "MISC_15": (57, 0),   # Obelisk, dirt
    # WATER: bottle -> bottle (59), buoy -> buoy (11), sea chest ->
    # sea chest (82), flotsam -> flotsam (29), shipwreck survivor
    # -> shipwreck survivor (86).
    "WATER_0": (59, 0),  # Bottle
    "WATER_1": (82, 0),  # Sea Chest
    "WATER_2": (29, 0),  # Flotsam
    "WATER_3": (11, 0),  # Buoy
    "WATER_5": (86, 0),  # Shipwreck Survivor
    "WATER_10": (52, 0),  # Mermaid
    "WATER_11": (92, 0),  # Sirens
}


# h3m interactive classes with a Heroes II object equivalent,
# mapped in the h3m -> fh2m direction (the inverse pairs of the
# FH2M_TO_H3M_MISC table): two-way monolith -> Stone Liths, magic
# well -> Magic Well, mystical garden -> Magic Garden, redwood
# observatory -> Observation Tower, learning stone -> Gazebo,
# water wheel -> Water Wheel, windmill -> Windmill.
H3M_TO_FH2M_INTERACTIVE = {
    45: ("ADVENTURE_MISCELLANEOUS", 35),   # two-way monolith -> Stone Liths
    49: ("ADVENTURE_POWER_UPS", 7),        # magic well -> Magic Well
    55: ("ADVENTURE_MISCELLANEOUS", 40),   # mystical garden -> Magic Garden
    58: ("ADVENTURE_MISCELLANEOUS", 41),   # redwood observatory -> Observation Tower
    100: ("ADVENTURE_POWER_UPS", 11),      # learning stone -> Gazebo
    109: ("ADVENTURE_MISCELLANEOUS", 24),  # water wheel -> Water Wheel
    112: ("ADVENTURE_MISCELLANEOUS", 4),   # windmill -> Windmill
    # Manual pairings (per user decision): the h3m interactive
    # classes map to the closest Heroes II gameplay objects.
    2: ("ADVENTURE_MISCELLANEOUS", 27),    # altar of sacrifice -> Daemon Cave
    23: ("ADVENTURE_POWER_UPS", 13),       # marletto tower -> Mercenary Camp
    30: ("ADVENTURE_POWER_UPS", 2),        # fountain of fortune -> Faerie Ring
    32: ("ADVENTURE_POWER_UPS", 12),       # garden of revelation -> Witch Doctor's Hut
    38: ("ADVENTURE_POWER_UPS", 17),       # idol of fortune -> Idol
    61: ("ADVENTURE_POWER_UPS", 18),       # star axis -> Standing Stones
    82: ("ADVENTURE_WATER", 1),            # sea chest -> Sea Chest
    96: ("ADVENTURE_POWER_UPS", 19),       # temple -> Temple
    97: ("ADVENTURE_MISCELLANEOUS", 32),   # den of thieves -> Trading Post
    102: ("ADVENTURE_POWER_UPS", 20),      # tree of knowledge -> Tree of Knowledge
    108: ("ADVENTURE_MISCELLANEOUS", 0),   # warrior's tomb -> Graveyard
    # Additional pairings (per user decision): the h3m editor-only
    # and PoL classes map to their Heroes II counterparts.
    8: ("ADVENTURE_WATER", 4),             # boat -> Boat
    27: ("ADVENTURE_MISCELLANEOUS", 49),    # eye of the magi -> Eye of the Magi
    78: ("ADVENTURE_DWELLINGS", 17),        # refugee camp -> Wagon Camp
    105: ("ADVENTURE_MISCELLANEOUS", 25),   # wagon -> Wagon
    39: ("ADVENTURE_MISCELLANEOUS", 16),    # lean-to -> Lean-to, snow terrain
    110: ("ADVENTURE_POWER_UPS", 1),         # watering hole variant -> Watering Hole
    # Per-user-decision pairings for the remaining h3m interactive
    # and editor classes.
    80: ("ADVENTURE_POWER_UPS", 19),         # sanctuary -> Temple
    99: ("ADVENTURE_MISCELLANEOUS", 32),     # trading post -> Trading Post
    41: ("ADVENTURE_POWER_UPS", 21),         # library of enlightenment -> Xanadu
    104: ("ADVENTURE_POWER_UPS", 21),        # university -> Xanadu
    7: ("ADVENTURE_MISCELLANEOUS", 32),      # black market -> Trading Post
    60: ("ADVENTURE_MISCELLANEOUS", 41),     # pillar of fire -> Observation Tower
    4: ("ADVENTURE_POWER_UPS", 22),           # arena -> Arena
    94: ("ADVENTURE_MISCELLANEOUS", 46),     # stables -> Stables
    106: ("ADVENTURE_MISCELLANEOUS", 39),    # war machine factory -> Freeman's Foundry
    64: ("ADVENTURE_POWER_UPS", 1),           # rally flag -> Watering Hole
    37: ("ADVENTURE_MISCELLANEOUS", 48),     # hut of the magi -> Hut of the Magi
    14: ("ADVENTURE_POWER_UPS", 17),          # swan pond -> Idol
    52: ("ADVENTURE_WATER", 10),              # mermaid -> Mermaid
    107: ("ADVENTURE_POWER_UPS", 22),         # school of war -> Arena
    13: ("ADVENTURE_MISCELLANEOUS", 41),      # cartographer -> Observation Tower
    95: ("ADVENTURE_MISCELLANEOUS", 7),       # tavern -> Oracle
    35: ("ADVENTURE_MISCELLANEOUS", 2),       # hill fort -> Hill Fort
    48: ("ADVENTURE_POWER_UPS", 0),           # magic spring -> Artesian Spring
    43: ("ADVENTURE_MISCELLANEOUS", 35),      # monolith one-way entrance -> Stone Liths
    44: ("ADVENTURE_MISCELLANEOUS", 35),      # monolith one-way exit -> Stone Liths
    111: ("ADVENTURE_WATER", 7),           # whirlpool -> Whirlpool
    # Additional pairings (the h3m interactive objects with a
    # Heroes II counterpart).
    12: ("ADVENTURE_TREASURES", 10),       # campfire -> Campfire
    29: ("ADVENTURE_WATER", 2),            # flotsam -> Flotsam
    11: ("ADVENTURE_WATER", 3),            # buoy -> Buoy
    22: ("ADVENTURE_MISCELLANEOUS", 30),   # corpse -> Skeleton
    63: ("ADVENTURE_MISCELLANEOUS", 29),   # pyramid -> Pyramid
    86: ("ADVENTURE_WATER", 5),            # shipwreck survivor -> Shipwreck Survivor
    92: ("ADVENTURE_WATER", 11),           # sirens -> Sirens
    47: ("ADVENTURE_MISCELLANEOUS", 26),   # scholar -> Witch's Hut
    28: ("ADVENTURE_POWER_UPS", 2),        # swan pond -> Faerie Ring
    31: ("ADVENTURE_POWER_UPS", 1),        # fountain of youth -> Watering Hole
    57: ("ADVENTURE_MISCELLANEOUS", 15),   # obelisk -> Obelisk
    # Dropped (no Heroes II gameplay equivalent): cursed ground (21),
    # magic plains (46), subterranean gate (103), arena (4),
    # black market (7), border gate (9), keymaster tent (10),
    # cartographer (13), cover of darkness (15), hill fort (35),
    # hut of the magi (37), magic spring (48), resource merchant
    # (52), rally point (64), stables (94), trading post (99 - the
    # den of thieves already maps to it), war memorial (107),
    # gallows (117), frozen lake (121), sand pit (149).
}


# h3m decorative object classes -> (fh2m landscape group, index).
# The h3m classes cover the families of decorative objects (the sprite
# names identify them: AVLsh = shrubs, AVLmt = mountains, AVLf =
# flowers...); each family converts to a representative Heroes II
# landscape object (see fheroes2 map_object_info.cpp). The classes
# not listed here stay dropped.
H3M_DECORATIVE_TO_FH2M = {
    150: ("LANDSCAPE_MISCELLANEOUS", 10),  # shrubs -> small shrub, grass
    134: ("LANDSCAPE_MOUNTAINS", 4),        # mountains -> medium mountain
    137: ("LANDSCAPE_MISCELLANEOUS", 11),  # plants -> pink flowers, grass
    119: ("LANDSCAPE_TREES", 24),           # dead trees -> dead tree, generic
    147: ("LANDSCAPE_ROCKS", 2),            # rocks -> single medium rock, grass
    120: ("LANDSCAPE_MISCELLANEOUS", 18),  # flowers -> small flowers, grass
    116: ("LANDSCAPE_MISCELLANEOUS", 73),  # cacti -> small cactus, desert
    131: ("LANDSCAPE_MISCELLANEOUS", 7),   # mandrakes -> wide shrub, grass
    155: ("LANDSCAPE_TREES", 7),            # deciduous trees -> single tree, grass
    129: ("LANDSCAPE_MISCELLANEOUS", 30),  # mosses -> shrub, swamp
    118: ("LANDSCAPE_MISCELLANEOUS", 0),   # cracks -> crack, grass
    127: ("LANDSCAPE_MISCELLANEOUS", 56),  # lava lakes -> small lava pool
    161: ("LANDSCAPE_MISCELLANEOUS", 19),  # debris -> dug hole, grass
    135: ("LANDSCAPE_MOUNTAINS", 4),      # mountains (snow) -> medium mountain
    136: ("LANDSCAPE_MOUNTAINS", 4),      # mountains (dirt) -> medium mountain
    101: ("LANDSCAPE_TREES", 7),           # conifers -> single tree, grass
    126: ("LANDSCAPE_MISCELLANEOUS", 11), # flowers (tall) -> pink flowers
    128: ("LANDSCAPE_MISCELLANEOUS", 12), # flowers (wide) -> wide flowers
    125: ("LANDSCAPE_TREES", 17),          # palms -> two tall palms, desert
    133: ("LANDSCAPE_ROCKS", 2),            # rocks (dirt) -> medium rock
    22:  ("LANDSCAPE_MISCELLANEOUS", 20), # small cliffs -> small cliff, grass
    29:  ("LANDSCAPE_WATER", 4),            # water plants -> aquatic plants
    148: ("LANDSCAPE_MISCELLANEOUS", 25), # shrubs (snow) -> small shrub, snow
    57:  ("LANDSCAPE_TREES", 5),           # forest -> three trees, grass
    12:  ("LANDSCAPE_MISCELLANEOUS", 69), # cactus -> tiny cactus
    124: ("LANDSCAPE_MISCELLANEOUS", 19), # hole -> dug hole, grass
    130: ("LANDSCAPE_TREES", 25),          # log -> log, generic
    132: ("LANDSCAPE_ROCKS", 13),          # moss -> medium mossy rock
    143: ("LANDSCAPE_MISCELLANEOUS", 112), # river delta -> river delta
    151: ("LANDSCAPE_MISCELLANEOUS", 102), # skull -> cow skull
    153: ("LANDSCAPE_TREES", 26),          # stump -> three stumps, generic
    158: ("LANDSCAPE_MISCELLANEOUS", 67), # volcano -> smoking volcano crater
}


# Shrine mapping: the Heroes III shrines (class 88 Incantation,
# 89 Gesture, 90 Thought) map to the Heroes II shrine circles (the
# ADVENTURE_POWER_UPS group: index 14 First Circle, 15 Second Circle,
# 16 Third Circle). The Heroes II Shrine of Magic Mystery has no
# Heroes III equivalent: it converts to the Third Circle (per
# decision).
H3M_TO_FH2M_SHRINES = {
    88: 14,  # Shrine of Magic Incantation -> Shrine of the First Circle
    89: 15,  # Shrine of Magic Gesture -> Shrine of the Second Circle
    90: 16,  # Shrine of Magic Thought -> Shrine of the Third Circle
}

# fh2m shrine index -> h3m shrine class (inverse; the fh2m Mystery
# shrine, whatever its index, maps to the Third Circle per decision).
FH2M_TO_H3M_SHRINES = {
    14: 88,  # Shrine of the First Circle -> Shrine of Magic Incantation
    15: 89,  # Shrine of the Second Circle -> Shrine of Magic Gesture
    16: 90,  # Shrine of the Third Circle -> Shrine of Magic Thought
}


# h3m town buildings (bit position in the 6-byte bitfield) -> fh2m
# building bit flags. Bytes 1 and 2 carry the common buildings
# (fixed position); bytes 3 to 6 carry faction buildings where only
# the generic dwellings (hordeN, dwellingN, dwellingNU) map to the
# fh2m dwellings. The fh2m flags come from the fheroes2 BuildingType
# enumeration (castle.h); a None value means no Heroes II equivalent.
H3M_TOWN_BUILDING_BITS = {
    # Byte 1 (bits 0-7)
    (0, 0): None,   # townHall
    (0, 1): None,   # cityHall
    (0, 2): None,   # capitol
    (0, 3): None,   # fort
    (0, 4): None,   # citadel
    (0, 5): 0x0800,  # castle -> BUILD_CASTLE
    (0, 6): 0x0002,  # tavern -> BUILD_TAVERN
    (0, 7): None,   # blacksmith
    # Byte 2 (bits 8-15)
    (1, 0): 0x0080,  # marketplace -> BUILD_MARKETPLACE
    (1, 1): None,   # resourceSilo
    (1, 2): None,   # artifactMerchants
    (1, 3): 0x4000,  # mageGuild1 -> BUILD_MAGEGUILD1
    (1, 4): 0x8000,  # mageGuild2 -> BUILD_MAGEGUILD2
    (1, 5): 0x10000, # mageGuild3 -> BUILD_MAGEGUILD3
    (1, 6): 0x20000, # mageGuild4 -> BUILD_MAGEGUILD4
    (1, 7): 0x40000, # mageGuild5 -> BUILD_MAGEGUILD5
    # Byte 3 (bits 16-23): shipyard (16), grail (17) and the
    # faction buildings (18-23) have no generic Heroes II mapping.
    (2, 0): 0x0004,  # shipyard -> BUILD_SHIPYARD
    # Byte 4-6: the horde and dwelling bits depend on the faction
    # layout; the generic dwellings map through
    # H3M_TOWN_FACTION_BUILDING_BITS below.
}

# Generic dwelling bits per byte: bit positions of hordeN, dwellingN
# and dwellingNU in bytes 4-6, the same for every faction (the lists
# in the corpus show dwN at fixed positions per byte).
# Byte 3: dwelling1 at bit 5, dwelling1U at bit 6.
# Byte 4: horde1 bit 0, dwelling2 bit 1, dwelling2U bit 2, horde2
# bit 3, dwelling3 bit 4, dwelling3U bit 5, horde3 bit 6, dwelling4
# bit 7. Byte 5: dwelling4U bit 0, horde4 bit 1, dwelling5 bit 2,
# dwelling5U bit 3, horde5 bit 4, dwelling6 bit 5, dwelling6U bit 6,
# dwelling7 bit 7. Byte 6: dwelling7U bit 0.
H3M_DWELLING_BITS = {
    (2, 5): 0x100000,  # dwelling1 -> DWELLING_MONSTER1
    (2, 6): 0x04000000, # dwelling1U -> DWELLING_UPGRADE2
    (3, 1): 0x200000,  # dwelling2 -> DWELLING_MONSTER2
    (3, 2): 0x8000000, # dwelling2U -> DWELLING_UPGRADE3
    (3, 4): 0x400000,  # dwelling3 -> DWELLING_MONSTER3
    (3, 5): 0x10000000, # dwelling3U -> DWELLING_UPGRADE4
    (3, 7): 0x800000,  # dwelling4 -> DWELLING_MONSTER4
    (4, 0): 0x20000000, # dwelling4U -> DWELLING_UPGRADE5
    (4, 2): 0x1000000, # dwelling5 -> DWELLING_MONSTER5
    (4, 3): 0x40000000, # dwelling5U -> DWELLING_UPGRADE6
    (4, 5): 0x2000000,  # dwelling6 -> DWELLING_MONSTER6
    (4, 6): 0x80000000, # dwelling6U -> DWELLING_UPGRADE7
    (4, 7): None,   # dwelling7 (Heroes II has only 6 dwellings)
    (5, 0): None,   # dwelling7U
}


# h3m town type (subclass of the town object, 0-8; -1 for a random
# town) -> fh2m town race, following the validated faction pairings:
# Castle->Knight, Rampart/Conflux->Sorceress, Tower->Wizard,
# Inferno/Dungeon->Warlock, Necropolis->Necromancer,
# Stronghold/Fortress->Barbarian. The fh2m KINGDOM_TOWNS object index
# is race * 2 (castle) or race * 2 + 1 (town), the fheroes2 race
# order being Knight, Barbarian, Sorceress, Warlock, Wizard,
# Necromancer (see map_object_info.cpp, populateKingdomTowns).
H3M_TOWN_TYPE_TO_FH2M_RACE = {
    0: "Knight",       # Castle
    1: "Sorceress",    # Rampart
    2: "Wizard",       # Tower
    3: "Warlock",      # Inferno
    4: "Necromancer",  # Necropolis
    5: "Warlock",      # Dungeon
    6: "Barbarian",    # Stronghold
    7: "Barbarian",    # Fortress
    8: "Sorceress",    # Conflux
}

FH2M_TOWN_RACE_ORDER = ["Knight", "Barbarian", "Sorceress", "Warlock",
                        "Wizard", "Necromancer"]


# Heroes III player colors, in the file order (owner byte of the
# town, garrison and hero objects; 255 means neutral).
H3M_PLAYER_COLOR_NAMES = {
    0: "Red", 1: "Blue", 2: "Tan", 3: "Green",
    4: "Orange", 5: "Purple", 6: "Teal", 7: "Pink",
    255: None,
}

# Heroes III secondary skills, in the SECSKILL.TXT order (h3m ids).
H3M_SECONDARY_SKILL_NAMES = [
    "Pathfinding", "Archery", "Logistics", "Scouting", "Diplomacy",
    "Navigation", "Leadership", "Wisdom", "Mysticism", "Luck",
    "Ballistics", "Eagle Eye", "Necromancy", "Estates", "Fire Magic",
    "Air Magic", "Water Magic", "Earth Magic", "Scholar", "Tactics",
    "Artillery", "Learning", "Offence", "Armorer", "Intelligence",
    "Sorcery", "Resistance", "First Aid",
]


# Heroes III hero identifiers, in the game order used by the h3m
# files (Hero Settings section: 156 entries, one per hero).
H3M_HERO_NAMES = [
    'Orrin',
    'Valeska',
    'Edric',
    'Sylvia',
    'Lord Haart',
    'Sorsha',
    'Christian',
    'Tyris',
    'Rion',
    'Adela',
    'Cuthbert',
    'Adelaide',
    'Ingham',
    'Sanya',
    'Loynis',
    'Caitlin',
    'Mephala',
    'Ufretin',
    'Jenova',
    'Ryland',
    'Thorgrim',
    'Ivor',
    'Clancy',
    'Kyrre',
    'Coronius',
    'Uland',
    'Elleshar',
    'Gem',
    'Malcom',
    'Melodia',
    'Alagar',
    'Aeris',
    'Piquedram',
    'Thane',
    'Josephine',
    'Neela',
    'Torosar',
    'Fafner',
    'Rissa',
    'Iona',
    'Astral',
    'Halon',
    'Serena',
    'Daremyth',
    'Theodorus',
    'Solmyr',
    'Cyra',
    'Aine',
    'Fiona',
    'Rashka',
    'Marius',
    'Ignatius',
    'Octavia',
    'Calh',
    'Pyre',
    'Nymus',
    'Ayden',
    'Xyron',
    'Axsis',
    'Olema',
    'Calid',
    'Ash',
    'Zydar',
    'Xarfax',
    'Straker',
    'Vokial',
    'Moandor',
    'Charna',
    'Tamika',
    'Isra',
    'Clavius',
    'Galthran',
    'Septienna',
    'Aislinn',
    'Sandro',
    'Nimbus',
    'Thant',
    'Xsi',
    'Vidomina',
    'Nagash',
    'Lorelei',
    'Arlach',
    'Dace',
    'Ajit',
    'Damacon',
    'Gunnar',
    'Synca',
    'Shakti',
    'Alamar',
    'Jaegar',
    'Malekith',
    'Jeddite',
    'Geon',
    'Deemer',
    'Sephinroth',
    'Darkstorn',
    'Yog',
    'Gurnisson',
    'Jabarkas',
    'Shiva',
    'Gretchin',
    'Krellion',
    'Crag Hack',
    'Tyraxor',
    'Gird',
    'Vey',
    'Dessa',
    'Terek',
    'Zubin',
    'Gundula',
    'Oris',
    'Saurug',
    'Bron',
    'Drakon',
    'Wystan',
    'Tazar',
    'Alkin',
    'Korbac',
    'Gerwulf',
    'Broghild',
    'Mirlanda',
    'Rosic',
    'Voy',
    'Verdish',
    'Merist',
    'Styg',
    'Andra',
    'Tiva',
    'Pasis',
    'Thunar',
    'Ignissa',
    'Lacus',
    'Monere',
    'Erdamon',
    'Fiur',
    'Kalt',
    'Luna',
    'Brissa',
    'Ciele',
    'Labetha',
    'Inteus',
    'Aenain',
    'Gelare',
    'Grindan',
    'Sir Mullich',
    'Adrienne',
    'Catherine',
    'Dracon',
    'Gelu',
    'Kilgor',
    'Undead Haart',
    'Mutare',
    'Roland',
    'Mutare Drake',
    'Boragus',
    'Xeron',
]

# Heroes II hero identifiers, in the fheroes2 Heroes enumeration
# order (index 0 is the uninitialized hero).
FH2M_HERO_NAMES = [
    'Unknown',
    'Lord Kilburn',
    'Sir Gallant',
    'Ector',
    'Gwenneth',
    'Tyro',
    'Ambrose',
    'Ruby',
    'Maximus',
    'Dimitry',
    'Thundax',
    'Fineous',
    'Jojosh',
    'Crag Hack',
    'Jezebel',
    'Jaclyn',
    'Ergon',
    'Tsabu',
    'Atlas',
    'Astra',
    'Natasha',
    'Troyan',
    'Vatawna',
    'Rebecca',
    'Gem',
    'Ariel',
    'Carlawn',
    'Luna',
    'Arie',
    'Alamar',
    'Vesper',
    'Crodo',
    'Barok',
    'Kastore',
    'Agar',
    'Falagar',
    'Wrathmont',
    'Myra',
    'Flint',
    'Dawn',
    'Halon',
    'Myrini',
    'Wilfrey',
    'Sarakin',
    'Kalindra',
    'Mandigal',
    'Zom',
    'Darlana',
    'Zam',
    'Ranloo',
    'Charity',
    'Rialdo',
    'Roxana',
    'Sandro',
    'Celia',
    'Roland',
    'Lord Corlagon',
    'Sister Eliza',
    'Archibald',
    'Lord Halton',
    'Brother Brax',
    'Solmyr',
    'Dainwin',
    'Mog',
    'Uncle Ivan',
    'Joseph',
    'Gallavant',
    'Elderian',
    'Ceallach',
    'Drakonia',
    'Martine',
    'Jarkonas',
    'Debug Hero',
]

# h3m hero id -> fh2m hero id: the heroes sharing their name match
# by name (Gem, Halon, Solmyr, Sandro, Alamar, Crag Hack, Luna,
# Roland); the others are paired within their faction
# (Castle->Knight, Stronghold/Fortress->Barbarian,
# Rampart/Conflux->Sorceress, Tower->Wizard,
# Dungeon/Inferno->Warlock, Necropolis->Necromancer),
# round-robin in the game order. Campaign heroes and the
# Debug Hero have no equivalent.
H3M_TO_FH2M_HEROES = {
    0: 1,  # Orrin -> Lord Kilburn (faction pairing)
    1: 2,  # Valeska -> Sir Gallant (faction pairing)
    2: 3,  # Edric -> Ector (faction pairing)
    3: 4,  # Sylvia -> Gwenneth (faction pairing)
    4: 5,  # Lord Haart -> Tyro (faction pairing)
    5: 6,  # Sorsha -> Ambrose (faction pairing)
    6: 7,  # Christian -> Ruby (faction pairing)
    7: 8,  # Tyris -> Maximus (faction pairing)
    8: 9,  # Rion -> Dimitry (faction pairing)
    9: 1,  # Adela -> Lord Kilburn (faction pairing)
    10: 2,  # Cuthbert -> Sir Gallant (faction pairing)
    11: 3,  # Adelaide -> Ector (faction pairing)
    12: 4,  # Ingham -> Gwenneth (faction pairing)
    13: 5,  # Sanya -> Tyro (faction pairing)
    14: 6,  # Loynis -> Ambrose (faction pairing)
    15: 7,  # Caitlin -> Ruby (faction pairing)
    16: 19,  # Mephala -> Astra (faction pairing)
    17: 20,  # Ufretin -> Natasha (faction pairing)
    18: 21,  # Jenova -> Troyan (faction pairing)
    19: 22,  # Ryland -> Vatawna (faction pairing)
    20: 23,  # Thorgrim -> Rebecca (faction pairing)
    21: 25,  # Ivor -> Ariel (faction pairing)
    22: 26,  # Clancy -> Carlawn (faction pairing)
    23: 19,  # Kyrre -> Astra (faction pairing)
    24: 20,  # Coronius -> Natasha (faction pairing)
    25: 21,  # Uland -> Troyan (faction pairing)
    26: 22,  # Elleshar -> Vatawna (faction pairing)
    27: 24,  # Gem -> Gem (name match)
    28: 23,  # Malcom -> Rebecca (faction pairing)
    29: 25,  # Melodia -> Ariel (faction pairing)
    30: 26,  # Alagar -> Carlawn (faction pairing)
    31: 19,  # Aeris -> Astra (faction pairing)
    32: 37,  # Piquedram -> Myra (faction pairing)
    33: 38,  # Thane -> Flint (faction pairing)
    34: 39,  # Josephine -> Dawn (faction pairing)
    35: 41,  # Neela -> Myrini (faction pairing)
    36: 42,  # Torosar -> Wilfrey (faction pairing)
    37: 43,  # Fafner -> Sarakin (faction pairing)
    38: 44,  # Rissa -> Kalindra (faction pairing)
    39: 45,  # Iona -> Mandigal (faction pairing)
    40: 37,  # Astral -> Myra (faction pairing)
    41: 40,  # Halon -> Halon (name match)
    42: 38,  # Serena -> Flint (faction pairing)
    43: 39,  # Daremyth -> Dawn (faction pairing)
    44: 41,  # Theodorus -> Myrini (faction pairing)
    45: 61,  # Solmyr -> Solmyr (name match)
    46: 42,  # Cyra -> Wilfrey (faction pairing)
    47: 43,  # Aine -> Sarakin (faction pairing)
    48: 28,  # Fiona -> Arie (faction pairing)
    49: 30,  # Rashka -> Vesper (faction pairing)
    50: 31,  # Marius -> Crodo (faction pairing)
    51: 32,  # Ignatius -> Barok (faction pairing)
    52: 33,  # Octavia -> Kastore (faction pairing)
    53: 34,  # Calh -> Agar (faction pairing)
    54: 35,  # Pyre -> Falagar (faction pairing)
    55: 36,  # Nymus -> Wrathmont (faction pairing)
    56: 28,  # Ayden -> Arie (faction pairing)
    57: 30,  # Xyron -> Vesper (faction pairing)
    58: 31,  # Axsis -> Crodo (faction pairing)
    59: 32,  # Olema -> Barok (faction pairing)
    60: 33,  # Calid -> Kastore (faction pairing)
    61: 34,  # Ash -> Agar (faction pairing)
    62: 35,  # Zydar -> Falagar (faction pairing)
    63: 36,  # Xarfax -> Wrathmont (faction pairing)
    64: 46,  # Straker -> Zom (faction pairing)
    65: 47,  # Vokial -> Darlana (faction pairing)
    66: 48,  # Moandor -> Zam (faction pairing)
    67: 49,  # Charna -> Ranloo (faction pairing)
    68: 50,  # Tamika -> Charity (faction pairing)
    69: 51,  # Isra -> Rialdo (faction pairing)
    70: 52,  # Clavius -> Roxana (faction pairing)
    71: 54,  # Galthran -> Celia (faction pairing)
    72: 46,  # Septienna -> Zom (faction pairing)
    73: 47,  # Aislinn -> Darlana (faction pairing)
    74: 53,  # Sandro -> Sandro (name match)
    75: 48,  # Nimbus -> Zam (faction pairing)
    76: 49,  # Thant -> Ranloo (faction pairing)
    77: 50,  # Xsi -> Charity (faction pairing)
    78: 51,  # Vidomina -> Rialdo (faction pairing)
    79: 52,  # Nagash -> Roxana (faction pairing)
    80: 28,  # Lorelei -> Arie (faction pairing)
    81: 30,  # Arlach -> Vesper (faction pairing)
    82: 31,  # Dace -> Crodo (faction pairing)
    83: 32,  # Ajit -> Barok (faction pairing)
    84: 33,  # Damacon -> Kastore (faction pairing)
    85: 34,  # Gunnar -> Agar (faction pairing)
    86: 35,  # Synca -> Falagar (faction pairing)
    87: 36,  # Shakti -> Wrathmont (faction pairing)
    88: 29,  # Alamar -> Alamar (name match)
    89: 28,  # Jaegar -> Arie (faction pairing)
    90: 30,  # Malekith -> Vesper (faction pairing)
    91: 31,  # Jeddite -> Crodo (faction pairing)
    92: 32,  # Geon -> Barok (faction pairing)
    93: 33,  # Deemer -> Kastore (faction pairing)
    94: 34,  # Sephinroth -> Agar (faction pairing)
    95: 35,  # Darkstorn -> Falagar (faction pairing)
    96: 10,  # Yog -> Thundax (faction pairing)
    97: 11,  # Gurnisson -> Fineous (faction pairing)
    98: 12,  # Jabarkas -> Jojosh (faction pairing)
    99: 14,  # Shiva -> Jezebel (faction pairing)
    100: 15,  # Gretchin -> Jaclyn (faction pairing)
    101: 16,  # Krellion -> Ergon (faction pairing)
    102: 13,  # Crag Hack -> Crag Hack (name match)
    103: 17,  # Tyraxor -> Tsabu (faction pairing)
    104: 18,  # Gird -> Atlas (faction pairing)
    105: 10,  # Vey -> Thundax (faction pairing)
    106: 11,  # Dessa -> Fineous (faction pairing)
    107: 12,  # Terek -> Jojosh (faction pairing)
    108: 14,  # Zubin -> Jezebel (faction pairing)
    109: 15,  # Gundula -> Jaclyn (faction pairing)
    110: 16,  # Oris -> Ergon (faction pairing)
    111: 17,  # Saurug -> Tsabu (faction pairing)
    112: 18,  # Bron -> Atlas (faction pairing)
    113: 10,  # Drakon -> Thundax (faction pairing)
    114: 11,  # Wystan -> Fineous (faction pairing)
    115: 12,  # Tazar -> Jojosh (faction pairing)
    116: 14,  # Alkin -> Jezebel (faction pairing)
    117: 15,  # Korbac -> Jaclyn (faction pairing)
    118: 16,  # Gerwulf -> Ergon (faction pairing)
    119: 17,  # Broghild -> Tsabu (faction pairing)
    120: 18,  # Mirlanda -> Atlas (faction pairing)
    121: 10,  # Rosic -> Thundax (faction pairing)
    122: 11,  # Voy -> Fineous (faction pairing)
    123: 12,  # Verdish -> Jojosh (faction pairing)
    124: 14,  # Merist -> Jezebel (faction pairing)
    125: 15,  # Styg -> Jaclyn (faction pairing)
    126: 16,  # Andra -> Ergon (faction pairing)
    127: 17,  # Tiva -> Tsabu (faction pairing)
    128: 20,  # Pasis -> Natasha (faction pairing)
    129: 21,  # Thunar -> Troyan (faction pairing)
    130: 22,  # Ignissa -> Vatawna (faction pairing)
    131: 23,  # Lacus -> Rebecca (faction pairing)
    132: 25,  # Monere -> Ariel (faction pairing)
    133: 26,  # Erdamon -> Carlawn (faction pairing)
    134: 19,  # Fiur -> Astra (faction pairing)
    135: 20,  # Kalt -> Natasha (faction pairing)
    136: 27,  # Luna -> Luna (name match)
    137: 21,  # Brissa -> Troyan (faction pairing)
    138: 22,  # Ciele -> Vatawna (faction pairing)
    139: 23,  # Labetha -> Rebecca (faction pairing)
    140: 25,  # Inteus -> Ariel (faction pairing)
    141: 26,  # Aenain -> Carlawn (faction pairing)
    142: 19,  # Gelare -> Astra (faction pairing)
    143: 20,  # Grindan -> Natasha (faction pairing)
    152: 55,  # Roland -> Roland (name match)
}

# fh2m hero id -> h3m hero id (inverse for the paired heroes:
# the preimage is the first Heroes III hero in the game order
# pointing to the Heroes II hero). Campaign heroes and the
# Debug Hero have no equivalent.
FH2M_TO_H3M_HEROES = {
    1: 0,  # Lord Kilburn <- Orrin
    2: 1,  # Sir Gallant <- Valeska
    3: 2,  # Ector <- Edric
    4: 3,  # Gwenneth <- Sylvia
    5: 4,  # Tyro <- Lord Haart
    6: 5,  # Ambrose <- Sorsha
    7: 6,  # Ruby <- Christian
    8: 7,  # Maximus <- Tyris
    9: 8,  # Dimitry <- Rion
    10: 96,  # Thundax <- Yog
    11: 97,  # Fineous <- Gurnisson
    12: 98,  # Jojosh <- Jabarkas
    13: 102,  # Crag Hack <- Crag Hack
    14: 99,  # Jezebel <- Shiva
    15: 100,  # Jaclyn <- Gretchin
    16: 101,  # Ergon <- Krellion
    17: 103,  # Tsabu <- Tyraxor
    18: 104,  # Atlas <- Gird
    19: 16,  # Astra <- Mephala
    20: 17,  # Natasha <- Ufretin
    21: 18,  # Troyan <- Jenova
    22: 19,  # Vatawna <- Ryland
    23: 20,  # Rebecca <- Thorgrim
    24: 27,  # Gem <- Gem
    25: 21,  # Ariel <- Ivor
    26: 22,  # Carlawn <- Clancy
    27: 136,  # Luna <- Luna
    28: 48,  # Arie <- Fiona
    29: 88,  # Alamar <- Alamar
    30: 49,  # Vesper <- Rashka
    31: 50,  # Crodo <- Marius
    32: 51,  # Barok <- Ignatius
    33: 52,  # Kastore <- Octavia
    34: 53,  # Agar <- Calh
    35: 54,  # Falagar <- Pyre
    36: 55,  # Wrathmont <- Nymus
    37: 32,  # Myra <- Piquedram
    38: 33,  # Flint <- Thane
    39: 34,  # Dawn <- Josephine
    40: 41,  # Halon <- Halon
    41: 35,  # Myrini <- Neela
    42: 36,  # Wilfrey <- Torosar
    43: 37,  # Sarakin <- Fafner
    44: 38,  # Kalindra <- Rissa
    45: 39,  # Mandigal <- Iona
    46: 64,  # Zom <- Straker
    47: 65,  # Darlana <- Vokial
    48: 66,  # Zam <- Moandor
    49: 67,  # Ranloo <- Charna
    50: 68,  # Charity <- Tamika
    51: 69,  # Rialdo <- Isra
    52: 70,  # Roxana <- Clavius
    53: 74,  # Sandro <- Sandro
    54: 71,  # Celia <- Galthran
    55: 152,  # Roland <- Roland
    61: 45,  # Solmyr <- Solmyr
}

# Heroes III artifact identifiers, in the ARTIFACT.TXT order used by the
# h3m files.
H3M_ARTIFACT_NAMES = [
    "Spell Book", "Spell Scroll", "Grail", "Catapult", "Ballista",
    "Ammo Cart", "First Aid Tent", "Centaur Axe",
    "Blackshard of the Dead Knight", "Greater Gnoll's Flail",
    "Ogre's Club of Havoc", "Sword of Hellfire", "Titan's Gladius",
    "Shield of the Dwarven Lords", "Shield of the Yawning Dead",
    "Buckler of the Gnoll King", "Targ of the Rampaging Ogre",
    "Shield of the Damned", "Sentinel's Shield",
    "Helm of the Alabaster Unicorn", "Skull Helmet", "Helm of Chaos",
    "Crown of the Supreme Magi", "Hellstorm Helmet", "Thunder Helmet",
    "Breastplate of Petrified Wood", "Rib Cage",
    "Scales of the Greater Basilisk", "Tunic of the Cyclops King",
    "Breastplate of Brimstone", "Titan's Cuirass", "Armor of Wonder",
    "Sandals of the Saint", "Celestial Necklace of Bliss",
    "Lion's Shield of Courage", "Sword of Judgement",
    "Helm of Heavenly Enlightenment", "Quiet Eye of the Dragon",
    "Red Dragon Flame Tongue", "Dragon Scale Shield", "Dragon Scale Armor",
    "Dragonbone Greaves", "Dragon Wing Tabard", "Necklace of Dragonteeth",
    "Crown of Dragontooth", "Still Eye of the Dragon",
    "Clover of Fortune", "Cards of Prophecy", "Ladybird of Luck",
    "Badge of Courage", "Crest of Valor", "Glyph of Gallantry",
    "Speculum", "Spyglass", "Amulet of the Undertaker", "Vampire's Cowl",
    "Dead Man's Boots", "Garniture of Interference",
    "Surcoat of Counterpoise", "Boots of Polarity",
    "Bow of Elven Cherrywood", "Bowstring of the Unicorn's Mane",
    "Angel Feather Arrows", "Bird of Perception", "Stoic Watchman",
    "Emblem of Cognizance", "Statesman's Medal", "Diplomat's Ring",
    "Ambassador's Sash", "Ring of the Wayfarer", "Equestrian's Gloves",
    "Necklace of Ocean Guidance", "Angel Wings", "Charm of Mana",
    "Talisman of Mana", "Mystic Orb of Mana", "Collar of Conjuring",
    "Ring of Conjuring", "Cape of Conjuring", "Orb of the Firmament",
    "Orb of Silt", "Orb of Tempestuous Fire", "Orb of Driving Rain",
    "Recanter's Cloak", "Spirit of Oppression",
    "Hourglass of the Evil Hour", "Tome of Fire Magic",
    "Tome of Air Magic", "Tome of Water Magic", "Tome of Earth Magic",
    "Boots of Levitation", "Golden Bow", "Sphere of Permanence",
    "Orb of Vulnerability", "Ring of Vitality", "Ring of Life",
    "Vial of Lifeblood", "Necklace of Swiftness", "Boots of Speed",
    "Cape of Velocity", "Pendant of Dispassion",
    "Pendant of Second Sight", "Pendant of Holiness", "Pendant of Life",
    "Pendant of Death", "Pendant of Free Will", "Pendant of Negativity",
    "Pendant of Total Recall", "Pendant of Courage",
    "Everflowing Crystal Cloak", "Ring of Infinite Gems",
    "Everpouring Vial of Mercury", "Inexhaustible Cart of Ore",
    "Eversmoking Ring of Sulfur", "Inexhaustible Cart of Lumber",
    "Endless Sack of Gold", "Endless Bag of Gold", "Endless Purse of Gold",
    "Legs of Legion", "Loins of Legion", "Torso of Legion",
    "Arms of Legion", "Head of Legion", "Sea Captain's Hat",
    "Spellbinder's Hat", "Shackles of War", "Orb of Inhibition",
    "Vial of Dragon Blood", "Armageddon's Blade", "Angelic Alliance",
    "Cloak of the Undead King", "Elixir of Life", "Armor of the Damned",
    "Statue of Legion", "Power of the Dragon Father", "Titan's Thunder",
    "Admiral's Hat", "Bow of the Sharpshooter", "Wizard's Well",
    "Ring of the Magi", "Cornucopia",
    "Unused 1", "Unused 2", "Unused 3",
]

# h3m artifact id -> fh2m artifact id (fheroes2 Artifact enum); -1
# when the artifact has no Heroes II equivalent. Only artifacts with a
# clear Heroes II counterpart (same role and name) are mapped.
# h3m artifact id -> fh2m artifact id (fheroes2 Artifact enum); -1
# when the artifact has no Heroes II equivalent. Only artifacts with a
# clear Heroes II counterpart (same role and name) are mapped.
H3M_TO_FH2M_ARTIFACTS = {
    0: 82,   # Spell Book
    1: 87,   # Spell Scroll
    4: 22,   # Ballista
    5: 69,   # Ammo Cart
    91: 64,   # Golden Bow
    97: 35,   # Necklace of Swiftness
    98: 40,   # Boots of Speed
    105: 57,   # Pendant of Free Will
    109: 77,   # Everflowing Crystal Cloak
    110: 74,   # Ring of Infinite Gems
    111: 73,   # Everpouring Vial of Mercury
    112: 76,   # Inexhaustible Cart of Ore
    113: 72,   # Eversmoking Ring of Sulfur
    114: 75,   # Inexhaustible Cart of Lumber
    115: 31,   # Endless Sack of Gold
    116: 32,   # Endless Bag of Gold
    117: 33,   # Endless Purse of Gold
}

# Heroes III spell identifiers, in the SPELLS.TXT order used by the
# h3m files.
H3M_SPELL_NAMES = [
    "Summon Boat", "Scuttle Boat", "Visions", "View Earth", "Disguise",
    "View Air", "Fly", "Water Walk", "Dimension Door", "Town Portal",
    "Quicksand", "Land Mine", "Force Field", "Fire Wall", "Earthquake",
    "Magic Arrow", "Ice Bolt", "Lightning Bolt", "Implosion",
    "Chain Lightning", "Frost Ring", "Fireball", "Inferno",
    "Meteor Shower", "Death Ripple", "Destroy Undead", "Armageddon",
    "Shield", "Air Shield", "Fire Shield", "Protect Air", "Protect Fire",
    "Protect Water", "Protect Earth", "Anti Magic", "Dispel",
    "Magic Mirror", "Cure", "Resurrection", "Animate Dead", "Sacrifice",
    "Bless", "Curse", "Bloodlust", "Precision", "Weakness",
    "Stone Skin", "Disrupting Ray", "Prayer", "Mirth", "Sorrow",
    "Fortune", "Misfortune", "Haste", "Slow", "Slayer", "Frenzy",
    "Titan Bolt", "Counterstrike", "Berserk", "Hypnotize",
    "Forgetfulness", "Blind", "Teleport", "Remove Obstacle", "Clone",
    "Fire Elemental", "Earth Elemental", "Water Elemental",
    "Air Elemental",
]

# h3m spell id -> fh2m spell id (fheroes2 Spell enum); -1 when the
# spell has no Heroes II equivalent. Only spells keeping the same
# effect in both games are mapped.
# h3m spell id -> fh2m spell id (fheroes2 Spell enum); -1 when the
# spell has no Heroes II equivalent. Only spells keeping the same
# effect in both games are mapped.
H3M_TO_FH2M_SPELLS = {
    0: 56,   # Summon Boat
    2: 60,   # Visions
    3: 49,   # View Earth
    5: 53,   # View Air
    8: 57,   # Dimension Door
    9: 59,   # Town Portal
    14: 48,   # Earthquake
    15: 26,   # Magic Arrow
    17: 3,   # Lightning Bolt
    19: 4,   # Chain Lightning
    21: 1,   # Fireball
    23: 30,   # Meteor Shower
    24: 36,   # Death Ripple
    26: 28,   # Armageddon
    27: 42,   # Shield
    34: 23,   # Anti Magic
    35: 24,   # Dispel
    37: 6,   # Cure
    39: 40,   # Animate Dead
    41: 15,   # Bless
    42: 19,   # Curse
    43: 39,   # Bloodlust
    46: 17,   # Stone Skin
    47: 35,   # Disrupting Ray
    53: 10,   # Haste
    54: 12,   # Slow
    60: 32,   # Hypnotize
    62: 14,   # Blind
    63: 5,   # Teleport
}


def h3m_creature_name(creature_id):
    """Name of an h3m creature id, or None when out of range."""
    if 0 <= creature_id < len(H3M_CREATURE_NAMES):
        return H3M_CREATURE_NAMES[creature_id]
    return None


def h3m_artifact_name(artifact_id):
    """Name of an h3m artifact id, or None when out of range."""
    if 0 <= artifact_id < len(H3M_ARTIFACT_NAMES):
        return H3M_ARTIFACT_NAMES[artifact_id]
    return None


def h3m_spell_name(spell_id):
    """Name of an h3m spell id, or None when out of range."""
    if 0 <= spell_id < len(H3M_SPELL_NAMES):
        return H3M_SPELL_NAMES[spell_id]
    return None
