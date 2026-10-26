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

# h3m random monster object classes (RANDOM_MONSTER and
# RANDOM_MONSTER_L1 to L4) -> fh2m random monster ids (fheroes2
# MonsterType: RANDOM_MONSTER and RANDOM_MONSTER_LEVEL_1 to 4). Used
# when the h3m monsterMetadata carries no creature id (creature is
# None): the object class gives the random level.
H3M_RANDOM_MONSTER_CLASSES = {
    71: 67,  # RANDOM_MONSTER
    72: 68,  # RANDOM_MONSTER_L1
    73: 69,  # RANDOM_MONSTER_L2
    74: 70,  # RANDOM_MONSTER_L3
    75: 71,  # RANDOM_MONSTER_L4
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
    0: 4,   # Pikeman -> Pikeman
    1: 5,   # Halberdier -> Veteran Pikeman
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
    82: 36,   # Red Dragon -> Green Dragon
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
    138: 39,   # Halfling -> Halfling
    139: 1,   # Peasant -> Peasant
    140: 40,   # Boar -> Boar
    141: 51,   # Mummy -> Mummy
    142: 59,   # Nomad -> Nomad
    143: 58,   # Rogue -> Rogue
    144: 18,   # Troll -> Troll
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
    123: 25,   # Ice Elemental -> Grand Elf
    125: 27,   # Magma Elemental -> Greater Druid
    127: 23,   # Storm Elemental -> Battle Dwarf
    129: 26,   # Energy Elemental -> Druid
    130: 29,   # Firebird -> Phoenix
}



def fh2m_building_name(building_id):
    """Name of a fh2m building bit flag, or None when unknown."""
    return FH2M_BUILDING_NAMES.get(building_id)


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
