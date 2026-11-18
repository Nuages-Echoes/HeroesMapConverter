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


# Adventure-map def name of every creature (object class 54), from the
# game's DEF database (id;name;combat def;adventure def). The game
# resolves random monsters against the map's own object catalog
# (NewfullMap::findObjectType in game::convertObject), and under SoD it
# can roll any creature up to CREATURE_CATAPULT-1, so generated maps
# must carry a class-54 def for every creature id.
H3M_CREATURE_DEF_NAMES = {
    0: 'avwpike.def',
    1: 'avwpikx0.def',
    2: 'avwlcrs.def',
    3: 'avwhcrs.def',
    4: 'avwgrif.def',
    5: 'avwgrix0.def',
    6: 'avwswrd0.def',
    7: 'avwswrx0.def',
    8: 'avwmonk.def',
    9: 'avwmonx0.def',
    10: 'avwcvlr0.def',
    11: 'avwcvlx0.def',
    12: 'avwangl.def',
    13: 'avwarch.def',
    14: 'avwcent0.def',
    15: 'avwcenx0.def',
    16: 'avwdwrf0.def',
    17: 'avwdwrx0.def',
    18: 'avwelfw0.def',
    19: 'avwelfx0.def',
    20: 'avwpega0.def',
    21: 'avwpegx0.def',
    22: 'avwtree0.def',
    23: 'avwtrex0.def',
    24: 'avwunic0.def',
    25: 'avwunix0.def',
    26: 'avwdrag0.def',
    27: 'avwdrax0.def',
    28: 'avwgrem0.def',
    29: 'avwgrex0.def',
    30: 'avwgarg0.def',
    31: 'avwgarx0.def',
    32: 'avwgolm0.def',
    33: 'avwgolx0.def',
    34: 'avwmage0.def',
    35: 'avwmagx0.def',
    36: 'avwgeni0.def',
    37: 'avwgenx0.def',
    38: 'avwnaga0.def',
    39: 'avwnagx0.def',
    40: 'avwtitn0.def',
    41: 'avwtitx0.def',
    42: 'avwimp0.def',
    43: 'avwimpx0.def',
    44: 'avwgog0.def',
    45: 'avwgogx0.def',
    46: 'avwhoun0.def',
    47: 'avwhoux0.def',
    48: 'avwdemn0.def',
    49: 'avwdemx0.def',
    50: 'avwpitf0.def',
    51: 'avwpitx0.def',
    52: 'avwefre0.def',
    53: 'avwefrx0.def',
    54: 'avwdevl0.def',
    55: 'avwdevx0.def',
    56: 'avwskel0.def',
    57: 'avwskex0.def',
    58: 'avwzomb0.def',
    59: 'avwzomx0.def',
    60: 'avwwigh.def',
    61: 'avwwigx0.def',
    62: 'avwvamp0.def',
    63: 'avwvamx0.def',
    64: 'avwlich0.def',
    65: 'avwlicx0.def',
    66: 'avwbkni0.def',
    67: 'avwbknx0.def',
    68: 'avwbone0.def',
    69: 'avwbonx0.def',
    70: 'avwtrog0.def',
    71: 'avwinfr.def',
    72: 'avwharp0.def',
    73: 'avwharx0.def',
    74: 'avwbehl0.def',
    75: 'avwbehx0.def',
    76: 'avwmeds.def',
    77: 'avwmedx0.def',
    78: 'avwmino.def',
    79: 'avwminx0.def',
    80: 'avwmant0.def',
    81: 'avwmanx0.def',
    82: 'avwrdrg.def',
    83: 'avwddrx0.def',
    84: 'avwgobl0.def',
    85: 'avwgobx0.def',
    86: 'avwwolf0.def',
    87: 'avwwolx0.def',
    88: 'avworc0.def',
    89: 'avworcx0.def',
    90: 'avwogre0.def',
    91: 'avwogrx0.def',
    92: 'avwroc0.def',
    93: 'avwrocx0.def',
    94: 'avwcycl0.def',
    95: 'avwcycx0.def',
    96: 'avwbhmt0.def',
    97: 'avwbhmx0.def',
    98: 'avwgnll0.def',
    99: 'avwgnlx0.def',
    100: 'avwlizr.def',
    101: 'avwlizx0.def',
    102: 'avwgorg.def',
    103: 'avwgorx0.def',
    104: 'avwdfly.def',
    105: 'avwdfir.def',
    106: 'avwbasl.def',
    107: 'avwgbas.def',
    108: 'avwwyvr.def',
    109: 'avwwyvx0.def',
    110: 'avwhydr.def',
    111: 'avwhydx0.def',
    112: 'avwelma0.def',
    113: 'avwelme0.def',
    114: 'avwelmf0.def',
    115: 'avwelmw0.def',
    116: 'avwglmg0.def',
    117: 'avwglmd0.def',
    118: 'avwpixie.def',
    119: 'avwsprit.def',
    120: 'avwpsye.def',
    121: 'avwmagel.def',
    122: 'notused',
    123: 'avwicee.def',
    124: 'notused',
    125: 'avwstone.def',
    126: 'notused',
    127: 'avwstorm.def',
    128: 'notused',
    129: 'avwnrg.def',
    130: 'avwfbird.def',
    131: 'avwphx.def',
    132: 'avwazure.def',
    133: 'avwcdrg.def',
    134: 'avwfdrg.def',
    135: 'avwrust.def',
    136: 'avwench.def',
    137: 'avwsharp.def',
    138: 'avwhalf.def',
    139: 'avwpeas.def',
    140: 'avwboar.def',
    141: 'avwmumy.def',
    142: 'avwnomd.def',
    143: 'avwrog.def',
    144: 'avwtrll.def',
    145: 'ava0003.def',
    146: 'ava0004.def',
    147: 'ava0006.def',
    148: 'ava0005.def',
    149: 'notused',
    150: 'zmm150z.def',
    151: 'zmm151z.def',
    152: 'zmm152z.def',
    153: 'zmm153z.def',
    154: 'zmm154z.def',
    155: 'zmm155z.def',
    156: 'zmm156z.def',
    157: 'zmm157z.def',
    158: 'zmm158z.def',
    159: 'z358o8.def',
    160: 'zmm160g.def',
    161: 'zmm161g.def',
    162: 'zmm162g.def',
    163: 'zmm163g.def',
    164: 'zmm164d.def',
    165: 'zmm165d.def',
    166: 'zmm166d.def',
    167: 'zmm167d.def',
    168: 'zmm168g.def',
    169: 'zmm169z.def',
    170: 'zmm170s.def',
    171: 'zmm171s.def',
    172: 'zmm172n.def',
    173: 'zmm173m.def',
    174: 'zmm174n.def',
    175: 'zmm175n.def',
    176: 'zmm176n.def',
    177: 'zmm177n.def',
    178: 'zmm178n.def',
    179: 'zmm179n.def',
    180: 'zmm180n.def',
    181: 'zmm181n.def',
    182: 'zmm182n.def',
    183: 'zmm174n.def',
    184: 'zmm175n.def',
    185: 'zmm176n.def',
    186: 'zmm177n.def',
    187: 'zmm178n.def',
    188: 'zmm179n.def',
    189: 'zmm180n.def',
    190: 'zmm181n.def',
    191: 'zmm182n.def',
    192: 'zmm192z.def',
    193: 'zmm193z.def',
    194: 'zmm194z.def',
    195: 'zmm195z.def',
    196: 'zmm196z.def',
}


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
    116: 42,  # Gold Golem -> Steel Golem (per user decision)
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
# fh2m mine object index -> h3m (class, subclass), derived from the H2
# object descriptions (fheroes2 populateAdventureMines order), not from
# index arithmetic:
#   0-39  resource mines: appearance = index//5 (0 Generic, 1 Grass,
#         2 Snow, 3 Swamp, 4 Lava, 5 Desert, 6 Dirt, 7 Wasteland),
#         resource = index%5 (0 Ore, 1 Sulfur, 2 Crystal, 3 Gems, 4 Gold)
#   40-47 abandoned mines (same 8 appearances)
#   48-53 sawmills (Grass/Swamp, Snow, Lava, Desert, Dirt, Wasteland)
#   54-55 alchemist lab (generic, snow)
# h3m class 53 subclasses (from the real maps' catalogs):
#   0 sawmill, 1 alchemist, 2 ore, 3 sulfur, 4 crystal, 5 gems, 6 gold,
#   7 abandoned.
FH2M_TO_H3M_MINES = {}
_mine_resources = [2, 3, 4, 5, 6]  # ore, sulfur, crystal, gems, gold
for _appearance in range(8):
    for _res_index, _subclass in enumerate(_mine_resources):
        FH2M_TO_H3M_MINES[_appearance * 5 + _res_index] = (53, _subclass)
for _i in range(8):
    FH2M_TO_H3M_MINES[40 + _i] = (53, 7)  # abandoned mines
for _i in range(6):
    FH2M_TO_H3M_MINES[48 + _i] = (53, 0)  # sawmills
FH2M_TO_H3M_MINES[54] = (53, 1)  # alchemist lab
FH2M_TO_H3M_MINES[55] = (53, 1)  # alchemist lab snow

# fh2m mine appearance names, in appearance order: for the resource
# mines (index 0-39) the appearance is index//5, for the abandoned
# mines (40-47) it is index-40.
FH2M_MINE_APPEARANCES = ["Generic", "Grass", "Snow", "Swamp", "Lava",
                         "Desert", "Dirt", "Wasteland"]

# Appearance of the sawmill (48-53) and alchemist lab (54-55) indices:
# the sawmills have no generic variant and no swamp variant of their
# own (the grass sawmill is used on swamp terrain too).
_FH2M_SAWMILL_APPEARANCES = [1, 2, 4, 5, 6, 7]  # Grass/Swamp, Snow, Lava, Desert, Dirt, Wasteland


def fh2m_mine_appearance(index):
    """Terrain appearance (0-7, see FH2M_MINE_APPEARANCES) of a fh2m
    mine object index."""
    if 0 <= index < 40:
        return index // 5
    if 40 <= index < 48:
        return index - 40
    if 48 <= index < 54:
        return _FH2M_SAWMILL_APPEARANCES[index - 48]
    if index == 54:
        return 0  # alchemist lab, generic
    if index == 55:
        return 2  # alchemist lab, snow
    return 0


# The h3m class 53 carries one def per mine type AND per terrain, all
# with the same subclass: AVMorsn0.def is the ore mine on snow,
# AVMswds0.def the sawmill on sand, ... Each def name below was matched
# with the terrain of the tile its instances stand on in the reference
# maps (input/*.h3m). Appearances with no def in the reference data
# (e.g. the desert crystal) fall back to the type's generic def.
H3M_MINE_GENERIC_DEF = {
    0: "AVMsawg0.def", 1: "AVMalch0.def", 2: "AVMore0.def",
    3: "AVMsulf0.def", 4: "AVMcrys0.def", 5: "AVMgems0.def",
    6: "AVMgold0.def", 7: "AVXabnd0.def",
}
FH2M_MINE_DEF_BY_APPEARANCE = {
    0: {0: "AVMsawg0.def", 1: "AVMsawg0.def", 2: "AVMswsn0.def",
        3: "AVMsawg0.def", 4: "AVMsawl0.def", 5: "AVMswds0.def",
        6: "AVMsawd0.def", 7: "AVMsawr0.def"},
    1: {0: "AVMalch0.def", 2: "AVMalcs0.def"},
    2: {0: "AVMore0.def", 1: "AVMore0.def", 2: "AVMorsn0.def",
        3: "AVMorsw0.def", 4: "AVMorlv0.def", 5: "AVMords0.def",
        6: "AVMordr0.def", 7: "AVMorro0.def"},
    3: {},  # sulfur mine: a single def for every terrain
    4: {0: "AVMcrys0.def", 1: "AVMcrgr0.def", 2: "AVMcrsn0.def",
        3: "AVMcrsw0.def", 4: "AVMcrvo0.def", 6: "AVMcrdr0.def",
        7: "AVMcrrf0.def"},
    5: {2: "AVMgesn0.def", 6: "AVMgedr0.def", 7: "AVMgerf0.def"},
    6: {1: "AVMgogr0.def", 4: "AVMgovo0.def", 5: "AVMgods0.def"},
    7: {},  # abandoned mine: AVXabnd0.def only
}


def fh2m_mine_def_name(index):
    """h3m class 53 def for a fh2m mine object index, following the
    mine's terrain appearance (None when the index is not a mine)."""
    h3m_mine = FH2M_TO_H3M_MINES.get(index)
    if h3m_mine is None:
        return None
    subclass = h3m_mine[1]
    appearance = fh2m_mine_appearance(index)
    return (FH2M_MINE_DEF_BY_APPEARANCE.get(subclass, {}).get(appearance)
            or H3M_MINE_GENERIC_DEF.get(subclass))


# h3m terrain name -> fh2m mine appearance, used in the h3m -> fh2m
# direction when the mine def carries no terrain variant (sulfur,
# abandoned, ...): the appearance is then read from the terrain of the
# tile the mine stands on.
H3M_TERRAIN_TO_FH2M_MINE_APPEARANCE = {
    "Grass": 1, "Snow": 2, "Swamp": 3, "Lava": 4,
    "Sand": 5, "Dirt": 6, "Rough": 7,
}


def h3m_mine_to_fh2m_index(subclass, def_name, tile_terrain=None):
    """fh2m mine index for an h3m class 53 object: the subclass gives
    the mine type, the def name (or the tile terrain when the def has
    no terrain variant) gives the appearance."""
    name = (def_name or "").lower()
    appearances = [app for app, d in FH2M_MINE_DEF_BY_APPEARANCE.get(subclass, {}).items()
                   if d.lower() == name]
    terrain_appearance = H3M_TERRAIN_TO_FH2M_MINE_APPEARANCE.get(tile_terrain)
    if terrain_appearance in appearances:
        appearance = terrain_appearance
    elif appearances:
        appearance = appearances[0]
    elif terrain_appearance is not None:
        appearance = terrain_appearance
    else:
        appearance = 0
    if subclass in (2, 3, 4, 5, 6):
        return appearance * 5 + (subclass - 2)  # resource mines
    if subclass == 7:
        return 40 + appearance  # abandoned mines
    if subclass == 0:
        if appearance in _FH2M_SAWMILL_APPEARANCES:
            return 48 + _FH2M_SAWMILL_APPEARANCES.index(appearance)
        return 48  # grass/swamp sawmill
    if subclass == 1:
        return 55 if appearance == 2 else 54  # alchemist lab
    return 0


# Sprite catalog of the h3m class 53 mine defs (sprite name, passability
# and landscape masks, trailing bytes), extracted from the catalogs of
# the reference maps (input/*.h3m), one entry per terrain variant def.
H3M_MINE_DEFS = {
    "avmalch0.def": ("AVMalch0.def", "ffffffffff1f000000000040ff010700", "000000000000000000000000000000000000"),
    "avmalcs0.def": ("AVMalcs0.def", "ffffffffff1f000000000040ff000800", "000000000000000000000000000000000000"),
    "avmcrdr0.def": ("AVMcrdr0.def", "ffffffffff1f000000000040ff010100", "000000000000000000000000000000000000"),
    "avmcrgr0.def": ("AVMcrgr0.def", "ffffffffff1f000000000040ff000400", "000000000000000000000000000000000000"),
    "avmcrrf0.def": ("AVMcrrf0.def", "ffffffffff1f000000000040ff002000", "000000000000000000000000000000000000"),
    "avmcrsn0.def": ("AVMcrsn0.def", "ffffffffff1f000000000040ff000800", "000000000000000000000000000000000000"),
    "avmcrsu0.def": ("AVMcrsu0.def", "ffffffffff1f000000000040ff014000", "000000000000000000000000000000000000"),
    "avmcrsw0.def": ("AVMcrsw0.def", "ffffffff1f1f000000000040ff001000", "000000000000000000000000000000000000"),
    "avmcrvo0.def": ("AVMcrvo0.def", "ffffffffff1f000000000040ff008000", "000000000000000000000000000000000000"),
    "avmcrys0.def": ("AVMcrys0.def", "ffffffffff1f000000000040ff010400", "000000000000000000000000000000000000"),
    "avmgedr0.def": ("AVMgedr0.def", "ffffffff1f1f000000000040ff010100", "000100000000000000000000000000000000"),
    "avmgems0.def": ("AVMgems0.def", "ffffffff1f1f000000000040ff011400", "000100000000000000000000000000000000"),
    "avmgerf0.def": ("AVMgerf0.def", "ffffffff1f1f000000000040ff016200", "000100000000000000000000000000000000"),
    "avmgesn0.def": ("AVMgesn0.def", "ffffffff1f1f000000000040ff000800", "000100000000000000000000000000000000"),
    "avmgods0.def": ("AVMgods0.def", "ffffffff1f1f000000000040ff010200", "000000000000000000000000000000000000"),
    "avmgogr0.def": ("AVMgogr0.def", "ffffffffff1f000000000040ff000400", "000000000000000000000000000000000000"),
    "avmgold0.def": ("AVMgold0.def", "ffffffffff1f000000000040ff000400", "000000000000000000000000000000000000"),
    "avmgosb0.def": ("AVMgosb0.def", "ffffffffff1f000000000040ff014000", "000000000000000000000000000000000000"),
    "avmgovo0.def": ("AVMgovo0.def", "ffffffffff1f000000000040ff018000", "000000000000000000000000000000000000"),
    "avmordr0.def": ("AVMordr0.def", "ffffffff1f1f00000000004001000100", "000100000000000000000000000000000000"),
    "avmords0.def": ("AVMords0.def", "ffffffff1f1f000000000040ff010200", "000100000000000000000000000000000000"),
    "avmore0.def": ("AVMore0.def", "ffffffff1f1f000000000040ff010400", "000100000000000000000000000000000000"),
    "avmorlv0.def": ("AVMorlv0.def", "ffffffff1f1f000000000040ff018000", "000100000000000000000000000000000000"),
    "avmorro0.def": ("AVMorro0.def", "ffffffff1f1f00000000004020002000", "000100000000000000000000000000000000"),
    "avmorsb0.def": ("AVMorsb0.def", "ffffffff1f1f000000000040ff014000", "000100000000000000000000000000000000"),
    "avmorsn0.def": ("AVMorsn0.def", "ffffffff1f1f000000000040ff010800", "000100000000000000000000000000000000"),
    "avmorsw0.def": ("AVMorsw0.def", "ffffffff1f1f00000000004010001000", "000100000000000000000000000000000000"),
    "avmsawd0.def": ("AVMsawd0.def", "ffffffff3f0f000000000040ff010100", "000000000000000000000000000000000000"),
    "avmsawg0.def": ("AVMsawg0.def", "ffffffff3f0f000000000040ff011400", "000000000000000000000000000000000000"),
    "avmsawl0.def": ("AVMsawl0.def", "ffffffff3f0f000000000040ff01c000", "000000000000000000000000000000000000"),
    "avmsawr0.def": ("AVMsawr0.def", "ffffffff3f0f000000000040ff002000", "000000000000000000000000000000000000"),
    "avmsulf0.def": ("AVMsulf0.def", "ffffffffff1f000000000040ff010700", "000000000000000000000000000000000000"),
    "avmswds0.def": ("AVMswds0.def", "ffffffff3f0f000000000040ff010200", "000000000000000000000000000000000000"),
    "avmswsn0.def": ("AVMswsn0.def", "ffffffff3f0f000000000040ff000800", "000000000000000000000000000000000000"),
    "avxabnd0.def": ("AVXabnd0.def", "ffffffffff1f000000000040ff010100", "000000000000000000000000000000000000"),
}

# fh2m STREAMS object index (0-12, frame of the H2 STREAM animation) ->
# h3m per-tile (River Properties, river mirror bits 0x04/0x08 of the
# Mirroring byte). The H2 frame order differs from the H3 river def
# frame order, so this is a real translation table, not a copy.
# Derived from the reference H3M maps (input/*.h3m) by matching each
# index to the cardinal mask of its neighboring STREAMS tiles.
# Indices 6, 9, 10, 11 are not present in the sample maps; they are
# assigned by elimination (remaining T junctions and the cross).
FH2M_TO_H3M_STREAMS = {
    0: (1, 0x04),    # corner S+W
    1: (0, 0x00),    # corner E+S
    2: (11, 0x00),   # horizontal line E-W
    3: (9, 0x00),    # vertical line N-S
    4: (1, 0x08),    # corner N+E
    5: (11, 0x00),   # horizontal line E-W, variant
    6: (5, 0x00),    # T junction E+S+W (by elimination)
    7: (3, 0x0C),    # corner N+W
    8: (5, 0x08),    # T junction N+E+W
    9: (8, 0x00),    # T junction N+E+S (by elimination)
    10: (7, 0x04),   # T junction N+S+W (by elimination)
    11: (4, 0x00),   # cross N+E+S+W (by elimination)
    12: (10, 0x00),  # vertical line N-S, variant
}

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
    # Indices 21-24 are the elemental summoning altars (fheroes2
    # populateAdventureDwellings): Earth/Air/Fire/Water Summoning
    # Altar -> the matching H3 elemental altar dwelling (h3m class 17
    # with the elemental creature id: 113 Earth, 112 Air, 114 Fire,
    # 115 Water).
    21: (17, 113),  # Earth Summoning Altar -> Earth Elemental
    22: (17, 112),  # Air Summoning Altar -> Air Elemental
    23: (17, 114),  # Fire Summoning Altar -> Fire Elemental
    24: (17, 115),  # Water Summoning Altar -> Water Elemental
}


# fh2m landscape object index -> h3m decorative class. The Heroes
# II landscape groups carry one entry per sprite variant; each maps
# to the closest h3m decorative family class (the h3m encoder writes
# the representative sprite of the class).
FH2M_LANDSCAPE_TO_H3M = {
    # TREES (fheroes2 populateLandscapeTrees): 6 forest types x 6
    # objects (big, big, medium, medium, small, small), then 33
    # singles (three trees, stumps, dead trees, logs...). The tree
    # and mountain writers refine the class and the def per index;
    # these entries are the class-level fallback.
    **{("LANDSCAPE_TREES", i): 155 for i in range(69)},
    # MOUNTAINS (fheroes2 populateLandscapeMountains): 8 terrain
    # blocks of 6-8 objects, then 11 singles (mounds, volcanoes,
    # dunes).
    **{("LANDSCAPE_MOUNTAINS", i): 134 for i in range(63)},
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



# True fh2m footprints of the non-tree landscape objects (rocks,
# miscellaneous, water), extracted from the fheroes2 catalog
# (map_object_info.cpp): the blocked cells as (dx, dy) offsets
# from the fh2m anchor. The passable overlays (cracks, flowers,
# dug holes...) have no blocked cell.
FH2M_LANDSCAPE_SHAPES = {
    # LANDSCAPE_MISCELLANEOUS
    ("LANDSCAPE_MISCELLANEOUS", 0): [],
    ("LANDSCAPE_MISCELLANEOUS", 1): [],
    ("LANDSCAPE_MISCELLANEOUS", 2): [],
    ("LANDSCAPE_MISCELLANEOUS", 3): [],
    ("LANDSCAPE_MISCELLANEOUS", 5): [(-2, -1), (-2, 0), (-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 6): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 7): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 8): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 9): [(0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 10): [(0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 11): [(0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 12): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 13): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 14): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 15): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 16): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 17): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 18): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 19): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 20): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 21): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 22): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 23): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 24): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 29): [],
    ("LANDSCAPE_MISCELLANEOUS", 34): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 35): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 36): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 38): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 39): [(0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 40): [],
    ("LANDSCAPE_MISCELLANEOUS", 41): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 44): [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1)],
    ("LANDSCAPE_MISCELLANEOUS", 45): [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1)],
    ("LANDSCAPE_MISCELLANEOUS", 46): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 47): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 48): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 49): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 50): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 52): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 53): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 54): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 55): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 57): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 58): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 59): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 60): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 61): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 62): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 63): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 64): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 65): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 66): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 67): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 68): [],
    ("LANDSCAPE_MISCELLANEOUS", 74): [(-3, -1), (-3, 0), (-2, -1), (-2, 0), (-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0), (2, -1), (2, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 75): [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 76): [(-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 77): [(-1, -1), (-1, 0), (0, -1), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 79): [(-1, -1), (-1, 0), (0, -1), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 82): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 83): [],
    ("LANDSCAPE_MISCELLANEOUS", 84): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 85): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 86): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 87): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 88): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 89): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 90): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 91): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 92): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 93): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 94): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 95): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 96): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 98): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 99): [],
    ("LANDSCAPE_MISCELLANEOUS", 100): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 101): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 102): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 104): [(-2, -1), (-2, 0), (-1, -1), (-1, 0), (0, -1), (0, 0), (1, -1), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 105): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 106): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 107): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 108): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 109): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 110): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 111): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 112): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 113): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 114): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 115): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 116): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 117): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 118): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 119): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 120): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 121): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 122): [(-1, 0), (0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 129): [],
    ("LANDSCAPE_MISCELLANEOUS", 130): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 131): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 132): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 133): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 136): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 137): [(0, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 141): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 142): [(-1, 0), (0, 0), (1, 0)],
    ("LANDSCAPE_MISCELLANEOUS", 143): [],
    ("LANDSCAPE_MISCELLANEOUS", 144): [],
    ("LANDSCAPE_MISCELLANEOUS", 145): [],
    ("LANDSCAPE_MISCELLANEOUS", 146): [],
    # LANDSCAPE_ROCKS
    ("LANDSCAPE_ROCKS", 0): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 1): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 2): [(0, 0)],
    ("LANDSCAPE_ROCKS", 3): [(0, 0)],
    ("LANDSCAPE_ROCKS", 4): [(0, 0)],
    ("LANDSCAPE_ROCKS", 5): [(0, 0)],
    ("LANDSCAPE_ROCKS", 6): [(0, 0)],
    ("LANDSCAPE_ROCKS", 7): [(0, 0)],
    ("LANDSCAPE_ROCKS", 8): [(0, 0)],
    ("LANDSCAPE_ROCKS", 9): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 10): [(0, 0)],
    ("LANDSCAPE_ROCKS", 11): [(0, 0)],
    ("LANDSCAPE_ROCKS", 12): [(0, 0)],
    ("LANDSCAPE_ROCKS", 13): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 14): [(0, 0)],
    ("LANDSCAPE_ROCKS", 15): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 16): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 17): [(0, 0)],
    ("LANDSCAPE_ROCKS", 18): [(0, 0)],
    ("LANDSCAPE_ROCKS", 19): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 20): [(0, 0)],
    ("LANDSCAPE_ROCKS", 21): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 22): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 23): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 24): [(0, 0)],
    ("LANDSCAPE_ROCKS", 25): [(0, 0)],
    ("LANDSCAPE_ROCKS", 26): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 27): [(0, 0)],
    ("LANDSCAPE_ROCKS", 28): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 29): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 30): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 31): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 32): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 33): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 34): [(0, 0), (1, 0)],
    ("LANDSCAPE_ROCKS", 35): [(-1, 0), (0, 0)],
    ("LANDSCAPE_ROCKS", 36): [(0, 0)],
    ("LANDSCAPE_ROCKS", 37): [(0, 0)],
    ("LANDSCAPE_ROCKS", 38): [(0, 0)],
    ("LANDSCAPE_ROCKS", 39): [(0, 0)],
    # LANDSCAPE_WATER
    ("LANDSCAPE_WATER", 0): [(0, 0), (1, 0)],
    ("LANDSCAPE_WATER", 1): [(0, 0)],
    ("LANDSCAPE_WATER", 2): [(0, 0), (1, 0)],
    ("LANDSCAPE_WATER", 3): [(0, 0)],
    ("LANDSCAPE_WATER", 4): [],
    ("LANDSCAPE_WATER", 5): [],
    ("LANDSCAPE_WATER", 6): [(0, 0), (0, 1), (1, -1), (1, 0), (1, 1), (2, -1), (2, 0)],
    ("LANDSCAPE_WATER", 7): [(0, -1), (0, 0), (1, -1), (1, 0), (1, 1), (2, 0), (2, 1)],
    ("LANDSCAPE_WATER", 8): [(0, 0), (0, 1), (1, 0), (1, 1)],
    ("LANDSCAPE_WATER", 9): [(-1, 1), (0, 0), (0, 1)],
    ("LANDSCAPE_WATER", 10): [(0, 0), (1, 0)],
    ("LANDSCAPE_WATER", 11): [(0, 0), (0, 1)],
}

# Footprint-exact, terrain-faithful H3 conversion of the non-tree
# landscape objects: (fh2m group, index) -> (h3m class, [def
# names]). All the defs of one entry block the same cells (a
# random pick among them never changes the footprint); the
# same-terrain defs come first, the entries without a
# same-terrain model fall back to the closest footprint-exact
# def of the family. The objects without an entry have no
# same-footprint H3 model and keep the class-level fallback
# (see FH2M_LANDSCAPE_UNCONVERTED below).
FH2M_LANDSCAPE_GROUP_DEF = {
    # LANDSCAPE_MISCELLANEOUS
    ("LANDSCAPE_MISCELLANEOUS", 0): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 1): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 2): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 3): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 5): (126, "AVLlk2g0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 6): (126, "AVLlk3g0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 7): (150, ["AVLsh1g0.def", "AVLsh2g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 8): (150, ["AVLsh1g0.def", "AVLsh2g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 9): (150, ["AVLsh3g0.def", "AVLsh4g0.def", "AVLsh5g0.def", "AVLsh6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 10): (150, ["AVLsh3g0.def", "AVLsh4g0.def", "AVLsh5g0.def", "AVLsh6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 11): (150, ["AVLsh3g0.def", "AVLsh4g0.def", "AVLsh5g0.def", "AVLsh6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 12): (150, ["AVLs05s0.def", "AVLs07s0.def", "AVLs08s0.def", "AVLs10s0.def", "AVLs11s0.def", "AVLs1sn0.def", "AVLs2sn0.def", "AVLsh1r0.def", "AVLsh2r0.def", "AVLsh3r0.def", "AVLsh5d0.def", "AVLsh8d0.def", "avlsh4r0.def", "avlsh5r0.def", "avlsh7r0.def", "avlsh8r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 13): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 14): (120, ["AVLf02g0.def", "AVLf03g0.def", "AVLf04g0.def", "AVLf05g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 15): (120, ["AVLf02g0.def", "AVLf03g0.def", "AVLf04g0.def", "AVLf05g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 16): (120, ["AVLf02g0.def", "AVLf03g0.def", "AVLf04g0.def", "AVLf05g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 17): (120, ["AVLf02g0.def", "AVLf03g0.def", "AVLf04g0.def", "AVLf05g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 18): (120, ["AVLf06g0.def", "AVLf07g0.def", "AVLf08g0.def", "AVLf10g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 19): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 20): (120, ["AVLf06g0.def", "AVLf07g0.def", "AVLf08g0.def", "AVLf10g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 21): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 22): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 23): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 24): (120, ["AVLf01g0.def", "AVLf09g0.def", "AVLf11g0.def", "AVLf12g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 29): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 34): (150, ["AVLs1sn0.def", "AVLs2sn0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 35): (150, ["AVLs1sn0.def", "AVLs2sn0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 36): (150, ["AVLs1sn0.def", "AVLs2sn0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 38): (121, "AVLflk20.def"),
    ("LANDSCAPE_MISCELLANEOUS", 39): (121, "AVLflk30.def"),
    ("LANDSCAPE_MISCELLANEOUS", 40): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 41): (150, ["AVLs01s0.def", "AVLs06s0.def", "AVLs09s0.def", "AVLswp40.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 44): (126, "AVLlk2s0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 45): (126, "AVLlk3s0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 46): (131, ["AVLman10.def", "AVLman30.def", "AVLman50.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 47): (131, "AVLman20.def"),
    ("LANDSCAPE_MISCELLANEOUS", 48): (131, ["AVLman10.def", "AVLman30.def", "AVLman50.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 49): (131, "AVLman40.def"),
    ("LANDSCAPE_MISCELLANEOUS", 50): (131, ["AVLman10.def", "AVLman30.def", "AVLman50.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 52): (126, "AVLlk3g0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 53): (126, "AVLlk3g0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 54): (126, "AVLlk3g0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 55): (126, "AVLswp50.def"),
    ("LANDSCAPE_MISCELLANEOUS", 57): (131, "AVLman40.def"),
    ("LANDSCAPE_MISCELLANEOUS", 58): (131, ["AVLman10.def", "AVLman30.def", "AVLman50.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 59): (150, ["AVLs01s0.def", "AVLs06s0.def", "AVLs09s0.def", "AVLswp40.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 60): (150, ["AVLs01s0.def", "AVLs06s0.def", "AVLs09s0.def", "AVLswp40.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 61): (150, ["AVLs05s0.def", "AVLs07s0.def", "AVLs08s0.def", "AVLs10s0.def", "AVLs11s0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 62): (150, ["AVLs01s0.def", "AVLs06s0.def", "AVLs09s0.def", "AVLswp40.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 63): (150, ["AVLs05s0.def", "AVLs07s0.def", "AVLs08s0.def", "AVLs10s0.def", "AVLs11s0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 64): (150, ["AVLs05s0.def", "AVLs07s0.def", "AVLs08s0.def", "AVLs10s0.def", "AVLs11s0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 65): (150, ["AVLs01s0.def", "AVLs06s0.def", "AVLs09s0.def", "AVLswp40.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 66): (150, ["AVLs05s0.def", "AVLs07s0.def", "AVLs08s0.def", "AVLs10s0.def", "AVLs11s0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 67): (129, ["AVLms010.def", "AVLms060.def", "AVLms070.def", "AVLms120.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 68): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 74): (127, "AVLlav30.def"),
    ("LANDSCAPE_MISCELLANEOUS", 75): (127, ["AVLlav40.def", "AVLlav50.def", "AVLlav90.def", "AVLlv100.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 76): (127, ["AVLlav40.def", "AVLlav50.def", "AVLlav90.def", "AVLlv100.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 77): (127, ["AVLlav60.def", "AVLlav70.def", "AVLlav80.def", "AVLlv110.def", "AVLlv180.def", "AVLlv190.def", "AVLlv200.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 79): (127, ["AVLlav60.def", "AVLlav70.def", "AVLlav80.def", "AVLlv110.def", "AVLlv180.def", "AVLlv190.def", "AVLlv200.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 82): (127, ["AVLlv120.def", "AVLlv130.def", "AVLlv140.def", "AVLlv240.def", "AVLlv260.def", "AVLlv3u0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 83): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 84): (116, ["AVLca010.def", "AVLca020.def", "AVLca030.def", "AVLca040.def", "AVLca050.def", "AVLca060.def", "AVLca070.def", "AVLca080.def", "AVLca090.def", "AVLca100.def", "AVLca110.def", "AVLca120.def", "AVLca130.def", "AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 85): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 86): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 87): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 88): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 89): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 90): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 91): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 92): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 93): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 94): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 95): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 96): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 98): (149, "AVLspit0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 99): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 100): (118, ["AVLct1d0.def", "AVLct2d0.def", "AVLct3d0.def", "AVLct4d0.def", "AVLctrd0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 101): (118, ["AVLct1d0.def", "AVLct2d0.def", "AVLct3d0.def", "AVLct4d0.def", "AVLctrd0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 102): (118, ["AVLct1d0.def", "AVLct2d0.def", "AVLct3d0.def", "AVLct4d0.def", "AVLctrd0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 104): (126, "AVLlk2d0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 105): (126, "AVLlk3d0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 106): (150, ["AVLsh1d0.def", "AVLsh2d0.def", "AVLsh3d0.def", "AVLsh4d0.def", "AVLsh7d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 107): (150, ["AVLsh1d0.def", "AVLsh2d0.def", "AVLsh3d0.def", "AVLsh4d0.def", "AVLsh7d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 108): (150, ["AVLsh1d0.def", "AVLsh2d0.def", "AVLsh3d0.def", "AVLsh4d0.def", "AVLsh7d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 109): (150, ["AVLsh5d0.def", "AVLsh8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 110): (150, ["AVLsh5d0.def", "AVLsh8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 111): (120, ["AVLfl1d0.def", "AVLfl2d0.def", "AVLfl3d0.def", "AVLfl4d0.def", "AVLfl7d0.def", "AVLfl8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 112): (120, ["AVLfl1d0.def", "AVLfl2d0.def", "AVLfl3d0.def", "AVLfl4d0.def", "AVLfl7d0.def", "AVLfl8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 113): (120, ["AVLfl1d0.def", "AVLfl2d0.def", "AVLfl3d0.def", "AVLfl4d0.def", "AVLfl7d0.def", "AVLfl8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 114): (120, ["AVLfl1d0.def", "AVLfl2d0.def", "AVLfl3d0.def", "AVLfl4d0.def", "AVLfl7d0.def", "AVLfl8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 115): (120, ["AVLfl6d0.def", "AVLfl9d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 116): (120, ["AVLfl6d0.def", "AVLfl9d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 117): (120, ["AVLfl6d0.def", "AVLfl9d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 118): (120, ["AVLfl6d0.def", "AVLfl9d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 119): (120, ["AVLfl6d0.def", "AVLfl9d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 120): (150, ["AVLsh5d0.def", "AVLsh8d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 121): (150, ["AVLsh1d0.def", "AVLsh2d0.def", "AVLsh3d0.def", "AVLsh4d0.def", "AVLsh7d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 122): (150, ["AVLsh1d0.def", "AVLsh2d0.def", "AVLsh3d0.def", "AVLsh4d0.def", "AVLsh7d0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 129): (118, ["AVLct4g0.def", "AVLct6g0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 130): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 131): (116, ["AVLca1r0.def", "AVLca2r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 132): (151, "AVLskul0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 133): (150, ["AVLsh1r0.def", "AVLsh2r0.def", "AVLsh3r0.def", "avlsh4r0.def", "avlsh5r0.def", "avlsh7r0.def", "avlsh8r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 136): (150, ["AVLsh1r0.def", "AVLsh2r0.def", "AVLsh3r0.def", "avlsh4r0.def", "avlsh5r0.def", "avlsh7r0.def", "avlsh8r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 137): (150, ["AVLsh1r0.def", "AVLsh2r0.def", "AVLsh3r0.def", "avlsh4r0.def", "avlsh5r0.def", "avlsh7r0.def", "avlsh8r0.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 141): (118, "AVLct3r0.def"),
    ("LANDSCAPE_MISCELLANEOUS", 142): (150, ["AVLs02s0.def", "AVLs04s0.def", "AVLsh1g0.def", "AVLsh2g0.def", "AVLsh6d0.def", "AVLswp20.def", "AVLswp30.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 143): (143, ["clrdelt1.def", "clrdelt2.def", "clrdelt3.def", "clrdelt4.def", "icedelt1.def", "icedelt2.def", "icedelt3.def", "icedelt4.def", "lavdelt1.def", "lavdelt2.def", "lavdelt3.def", "lavdelt4.def", "muddelt1.def", "muddelt2.def", "muddelt3.def", "muddelt4.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 144): (143, ["clrdelt1.def", "clrdelt2.def", "clrdelt3.def", "clrdelt4.def", "icedelt1.def", "icedelt2.def", "icedelt3.def", "icedelt4.def", "lavdelt1.def", "lavdelt2.def", "lavdelt3.def", "lavdelt4.def", "muddelt1.def", "muddelt2.def", "muddelt3.def", "muddelt4.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 145): (143, ["clrdelt1.def", "clrdelt2.def", "clrdelt3.def", "clrdelt4.def", "icedelt1.def", "icedelt2.def", "icedelt3.def", "icedelt4.def", "lavdelt1.def", "lavdelt2.def", "lavdelt3.def", "lavdelt4.def", "muddelt1.def", "muddelt2.def", "muddelt3.def", "muddelt4.def"]),
    ("LANDSCAPE_MISCELLANEOUS", 146): (143, ["clrdelt1.def", "clrdelt2.def", "clrdelt3.def", "clrdelt4.def", "icedelt1.def", "icedelt2.def", "icedelt3.def", "icedelt4.def", "lavdelt1.def", "lavdelt2.def", "lavdelt3.def", "lavdelt4.def", "muddelt1.def", "muddelt2.def", "muddelt3.def", "muddelt4.def"]),
    # LANDSCAPE_ROCKS
    ("LANDSCAPE_ROCKS", 0): (147, ["AvLRG01.def", "AvLRG02.def"]),
    ("LANDSCAPE_ROCKS", 1): (147, ["AvLRG01.def", "AvLRG02.def"]),
    ("LANDSCAPE_ROCKS", 2): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 3): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 4): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 5): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 6): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 7): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 8): (147, ["AVLr1sn0.def", "AVLr3sn0.def", "AVLr4sn0.def", "AVLr5sn0.def", "AVLr7sn0.def", "AVLr8sn0.def"]),
    ("LANDSCAPE_ROCKS", 9): (147, ["AVLr2sn0.def", "AVLr6sn0.def"]),
    ("LANDSCAPE_ROCKS", 10): (147, ["AVLr1sn0.def", "AVLr3sn0.def", "AVLr4sn0.def", "AVLr5sn0.def", "AVLr7sn0.def", "AVLr8sn0.def"]),
    ("LANDSCAPE_ROCKS", 11): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 12): (147, ["AvLRG03.def", "AvLRG04.def", "AvLRG05.def", "AvLRG06.def", "AvLRG07.def", "AvLRG08.def", "AvLRG09.def", "AvLRG10.def", "AvLRG11.def"]),
    ("LANDSCAPE_ROCKS", 13): (147, ["AVLr2sn0.def", "AVLr6sn0.def"]),
    ("LANDSCAPE_ROCKS", 14): (147, ["AVLr1sn0.def", "AVLr3sn0.def", "AVLr4sn0.def", "AVLr5sn0.def", "AVLr7sn0.def", "AVLr8sn0.def"]),
    ("LANDSCAPE_ROCKS", 15): (147, ["AVLr2sn0.def", "AVLr6sn0.def"]),
    ("LANDSCAPE_ROCKS", 16): (147, "AVLrk3s0.def"),
    ("LANDSCAPE_ROCKS", 17): (147, ["AVLrk1s0.def", "AVLrk2s0.def", "AVLrk4s0.def"]),
    ("LANDSCAPE_ROCKS", 18): (147, ["AVLrk1s0.def", "AVLrk2s0.def", "AVLrk4s0.def"]),
    ("LANDSCAPE_ROCKS", 19): (147, "AVLrk3s0.def"),
    ("LANDSCAPE_ROCKS", 20): (147, ["AVLrk1s0.def", "AVLrk2s0.def", "AVLrk4s0.def"]),
    ("LANDSCAPE_ROCKS", 21): (147, ["AVLrk3d0.def", "AvLRD01.def", "AvLRD02.def"]),
    ("LANDSCAPE_ROCKS", 22): (147, ["AVLrk3d0.def", "AvLRD01.def", "AvLRD02.def"]),
    ("LANDSCAPE_ROCKS", 23): (147, ["AVLrk3d0.def", "AvLRD01.def", "AvLRD02.def"]),
    ("LANDSCAPE_ROCKS", 24): (147, ["AVLrk5d0.def", "AvLRD04.def"]),
    ("LANDSCAPE_ROCKS", 25): (147, ["AVLrk5d0.def", "AvLRD04.def"]),
    ("LANDSCAPE_ROCKS", 26): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 27): (147, ["AVLr10r0.def", "AVLr11r0.def", "AVLr12r0.def", "AVLr13r0.def", "AVLr14r0.def", "AVLr15r0.def", "AvLRR01.def"]),
    ("LANDSCAPE_ROCKS", 28): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 29): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 30): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 31): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 32): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 33): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 34): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 35): (147, ["AVLr02r0.def", "AVLr03r0.def", "AVLr04r0.def", "AVLr06r0.def", "AVLr07r0.def", "AVLr08r0.def", "AVLr09r0.def", "AvLRR05.def", "avlbuzr0.def"]),
    ("LANDSCAPE_ROCKS", 36): (147, ["AVLr10r0.def", "AVLr11r0.def", "AVLr12r0.def", "AVLr13r0.def", "AVLr14r0.def", "AVLr15r0.def", "AvLRR01.def"]),
    ("LANDSCAPE_ROCKS", 37): (147, ["AVLr10r0.def", "AVLr11r0.def", "AVLr12r0.def", "AVLr13r0.def", "AVLr14r0.def", "AVLr15r0.def", "AvLRR01.def"]),
    ("LANDSCAPE_ROCKS", 38): (147, ["AVLr10r0.def", "AVLr11r0.def", "AVLr12r0.def", "AVLr13r0.def", "AVLr14r0.def", "AVLr15r0.def", "AvLRR01.def"]),
    ("LANDSCAPE_ROCKS", 39): (147, ["AVLr10r0.def", "AVLr11r0.def", "AVLr12r0.def", "AVLr13r0.def", "AVLr14r0.def", "AVLr15r0.def", "AvLRR01.def"]),
    # LANDSCAPE_WATER
    ("LANDSCAPE_WATER", 0): (147, "AVLrk1w0.def"),
    ("LANDSCAPE_WATER", 1): (147, ["AVLrk2w0.def", "AVLrk3w0.def", "AVLrk4w0.def"]),
    ("LANDSCAPE_WATER", 2): (147, "AVLrk1w0.def"),
    ("LANDSCAPE_WATER", 3): (147, ["AVLrk2w0.def", "AVLrk3w0.def", "AVLrk4w0.def"]),
    ("LANDSCAPE_WATER", 4): (125, ["AVLklp10.def", "AVLklp20.def"]),
    ("LANDSCAPE_WATER", 5): (125, ["AVLklp10.def", "AVLklp20.def"]),
    ("LANDSCAPE_WATER", 6): (161, "AVLref10.def"),
    ("LANDSCAPE_WATER", 7): (161, "AVLref20.def"),
    ("LANDSCAPE_WATER", 8): (161, "AVLref30.def"),
    ("LANDSCAPE_WATER", 9): (161, "AVLref40.def"),
    ("LANDSCAPE_WATER", 10): (161, "AVLref50.def"),
    ("LANDSCAPE_WATER", 11): (161, "AVLref60.def"),
}

# Sprite catalog of the H3 defs used by the landscape conversion
# (from the game's own Objects.txt: pass/action bitmaps, allowed
# landscapes, editor group; the trailing bytes carry the editor
# group).
H3M_LANDSCAPE_DEFS = {
    "avlbuzr0.def": ("avlbuzr0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlc10l0.def": ("AVLc10l0.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlca010.def": ("AVLca010.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca020.def": ("AVLca020.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca030.def": ("AVLca030.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca040.def": ("AVLca040.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca050.def": ("AVLca050.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca060.def": ("AVLca060.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca070.def": ("AVLca070.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca080.def": ("AVLca080.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca090.def": ("AVLca090.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca100.def": ("AVLca100.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca110.def": ("AVLca110.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca120.def": ("AVLca120.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca130.def": ("AVLca130.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlca1r0.def": ("AVLca1r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlca2r0.def": ("AVLca2r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlct1d0.def": ("AVLct1d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlct1u0.def": ("AVLct1u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlct2d0.def": ("AVLct2d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlct3d0.def": ("AVLct3d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlct3r0.def": ("AVLct3r0.def", "ffffffffff1f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlct4d0.def": ("AVLct4d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlct4g0.def": ("AVLct4g0.def", "ffffffffffff000000000000ff010400", "000000000000000000000000000000000000"),
    "avlct4r0.def": ("AVLct4r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlct5g0.def": ("AVLct5g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlct5r0.def": ("AVLct5r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlct6g0.def": ("AVLct6g0.def", "ffffffffffff000000000000ff010400", "000000000000000000000000000000000000"),
    "avlct8r0.def": ("AVLct8r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlct9l0.def": ("AVLct9l0.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlctds0.def": ("AVLctds0.def", "ffffffffff3f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlctrd0.def": ("AVLctrd0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlctrg0.def": ("AVLctrg0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlctrl0.def": ("AVLctrl0.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlctrr0.def": ("AVLctrr0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlctrs0.def": ("AVLctrs0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlctsn0.def": ("AVLctsn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlf01g0.def": ("AVLf01g0.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf02g0.def": ("AVLf02g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf03g0.def": ("AVLf03g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf04g0.def": ("AVLf04g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf05g0.def": ("AVLf05g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf06g0.def": ("AVLf06g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf07g0.def": ("AVLf07g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf08g0.def": ("AVLf08g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf09g0.def": ("AVLf09g0.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf10g0.def": ("AVLf10g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf11g0.def": ("AVLf11g0.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlf12g0.def": ("AVLf12g0.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlfl1d0.def": ("AVLfl1d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl2d0.def": ("AVLfl2d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl3d0.def": ("AVLfl3d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl4d0.def": ("AVLfl4d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl5d0.def": ("AVLfl5d0.def", "ffffffffff1f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl6d0.def": ("AVLfl6d0.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl7d0.def": ("AVLfl7d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl8d0.def": ("AVLfl8d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlfl9d0.def": ("AVLfl9d0.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlflk20.def": ("AVLflk20.def", "ffffffffff1f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlflk30.def": ("AVLflk30.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlklp10.def": ("AVLklp10.def", "ffffffffffff000000000000ff010001", "000000000000000000000000000000000000"),
    "avlklp20.def": ("AVLklp20.def", "ffffffffffff000000000000ff010001", "000000000000000000000000000000000000"),
    "avllav30.def": ("AVLlav30.def", "ffffffff0303000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav40.def": ("AVLlav40.def", "ffffffff1f1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav50.def": ("AVLlav50.def", "ffffffff1f1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav60.def": ("AVLlav60.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav70.def": ("AVLlav70.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav80.def": ("AVLlav80.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllav90.def": ("AVLlav90.def", "ffffffff1f1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllk2d0.def": ("AVLlk2d0.def", "ffffffff0f0f000000000000ff010100", "000000000000000000000000000000000000"),
    "avllk2g0.def": ("AVLlk2g0.def", "ffffffff0f0f000000000000ff010400", "000000000000000000000000000000000000"),
    "avllk2s0.def": ("AVLlk2s0.def", "ffffffff1f9f000000000000ff011000", "000000000000000000000000000000000000"),
    "avllk2u0.def": ("AVLlk2u0.def", "ffffffff0f0f000000000000ff014000", "000000000000000000000000000000000000"),
    "avllk3d0.def": ("AVLlk3d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avllk3g0.def": ("AVLlk3g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avllk3s0.def": ("AVLlk3s0.def", "ffffff9f9f9f000000000000ff011000", "000000000000000000000000000000000000"),
    "avllk3u0.def": ("AVLlk3u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avllv100.def": ("AVLlv100.def", "ffffffff1f1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv110.def": ("AVLlv110.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv120.def": ("AVLlv120.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv130.def": ("AVLlv130.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv140.def": ("AVLlv140.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv180.def": ("AVLlv180.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv190.def": ("AVLlv190.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv1u0.def": ("AVLlv1u0.def", "ffffffff3f3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avllv200.def": ("AVLlv200.def", "ffffffff3f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv240.def": ("AVLlv240.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv260.def": ("AVLlv260.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avllv3u0.def": ("AVLlv3u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlman10.def": ("AVLman10.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlman20.def": ("AVLman20.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlman30.def": ("AVLman30.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlman40.def": ("AVLman40.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlman50.def": ("AVLman50.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlms010.def": ("AVLms010.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlms060.def": ("AVLms060.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlms070.def": ("AVLms070.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlms120.def": ("AVLms120.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr01u0.def": ("AVLr01u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr02r0.def": ("AVLr02r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr02u0.def": ("AVLr02u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr03r0.def": ("AVLr03r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr03u0.def": ("AVLr03u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr04r0.def": ("AVLr04r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr04u0.def": ("AVLr04u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr05u0.def": ("AVLr05u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr06r0.def": ("AVLr06r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr06u0.def": ("AVLr06u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr07r0.def": ("AVLr07r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr07u0.def": ("AVLr07u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr08r0.def": ("AVLr08r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr08u0.def": ("AVLr08u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr09r0.def": ("AVLr09r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr09u0.def": ("AVLr09u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr10r0.def": ("AVLr10r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr10u0.def": ("AVLr10u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr11r0.def": ("AVLr11r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr11u0.def": ("AVLr11u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr12r0.def": ("AVLr12r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr12u0.def": ("AVLr12u0.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr13r0.def": ("AVLr13r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr13u0.def": ("AVLr13u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr14r0.def": ("AVLr14r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr14u0.def": ("AVLr14u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr15r0.def": ("AVLr15r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlr15u0.def": ("AVLr15u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr16u0.def": ("AVLr16u0.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlr1sn0.def": ("AVLr1sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr2sn0.def": ("AVLr2sn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr3sn0.def": ("AVLr3sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr4sn0.def": ("AVLr4sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr5sn0.def": ("AVLr5sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr6sn0.def": ("AVLr6sn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr7sn0.def": ("AVLr7sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr8sn0.def": ("AVLr8sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlrd01.def": ("AvLRD01.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlrd02.def": ("AvLRD02.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlrd04.def": ("AvLRD04.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlref10.def": ("AVLref10.def", "ffffff3f1f9f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlref20.def": ("AVLref20.def", "ffffff9f1f3f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlref30.def": ("AVLref30.def", "ffffffff3f3f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlref40.def": ("AVLref40.def", "ffffffff7f3f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlref50.def": ("AVLref50.def", "ffffffffff3f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlref60.def": ("AVLref60.def", "ffffffff7f7f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlrg01.def": ("AvLRG01.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg02.def": ("AvLRG02.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg03.def": ("AvLRG03.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg04.def": ("AvLRG04.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg05.def": ("AvLRG05.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg06.def": ("AvLRG06.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg07.def": ("AvLRG07.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg08.def": ("AvLRG08.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg09.def": ("AvLRG09.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg10.def": ("AvLRG10.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrg11.def": ("AvLRG11.def", "ffffffffff7f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlrk1s0.def": ("AVLrk1s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlrk1w0.def": ("AVLrk1w0.def", "ffffffffff3f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlrk2s0.def": ("AVLrk2s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlrk2w0.def": ("AVLrk2w0.def", "ffffffffff7f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlrk3d0.def": ("AVLrk3d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlrk3s0.def": ("AVLrk3s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlrk3w0.def": ("AVLrk3w0.def", "ffffffffff7f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlrk4s0.def": ("AVLrk4s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlrk4w0.def": ("AVLrk4w0.def", "ffffffffff7f000000000000ff010001", "000000000000000000000000000000000000"),
    "avlrk5d0.def": ("AVLrk5d0.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlrr01.def": ("AvLRR01.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlrr05.def": ("AvLRR05.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avls01s0.def": ("AVLs01s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls02s0.def": ("AVLs02s0.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls04s0.def": ("AVLs04s0.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls05s0.def": ("AVLs05s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls06s0.def": ("AVLs06s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls07s0.def": ("AVLs07s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls08s0.def": ("AVLs08s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls09s0.def": ("AVLs09s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls10s0.def": ("AVLs10s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls11s0.def": ("AVLs11s0.def", "ffffffffff7f000000000000ff011000", "000000000000000000000000000000000000"),
    "avls1sn0.def": ("AVLs1sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avls2sn0.def": ("AVLs2sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avls3sn0.def": ("AVLs3sn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsh1d0.def": ("AVLsh1d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh1g0.def": ("AVLsh1g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh1r0.def": ("AVLsh1r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh2d0.def": ("AVLsh2d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh2g0.def": ("AVLsh2g0.def", "ffffffffff1f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh2r0.def": ("AVLsh2r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh3d0.def": ("AVLsh3d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh3g0.def": ("AVLsh3g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh3r0.def": ("AVLsh3r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh4d0.def": ("AVLsh4d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh4g0.def": ("AVLsh4g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh4r0.def": ("avlsh4r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh5d0.def": ("AVLsh5d0.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh5g0.def": ("AVLsh5g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh5r0.def": ("avlsh5r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh6d0.def": ("AVLsh6d0.def", "ffffffffff1f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh6g0.def": ("AVLsh6g0.def", "ffffffffff3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlsh6r0.def": ("avlsh6r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh7d0.def": ("AVLsh7d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh7r0.def": ("avlsh7r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh8d0.def": ("AVLsh8d0.def", "ffffffffff7f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlsh8r0.def": ("avlsh8r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlsh9r0.def": ("avlsh9r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlskul0.def": ("AVLskul0.def", "ffffffffff7f000000000000ff012200", "000000000000000000000000000000000000"),
    "avlspit0.def": ("AVLspit0.def", "ffffffffff1f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlstg10.def": ("AVLstg10.def", "ffffffffff3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlstg20.def": ("AVLstg20.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlstg30.def": ("AVLstg30.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlstg40.def": ("AVLstg40.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlstg50.def": ("AVLstg50.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlstg60.def": ("AVLstg60.def", "ffffffffff7f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlswp20.def": ("AVLswp20.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlswp30.def": ("AVLswp30.def", "ffffffffff1f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlswp40.def": ("AVLswp40.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlswp50.def": ("AVLswp50.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "clrdelt1.def": ("clrdelt1.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "clrdelt2.def": ("clrdelt2.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "clrdelt3.def": ("clrdelt3.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "clrdelt4.def": ("clrdelt4.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "icedelt1.def": ("icedelt1.def", "ffffffffffff000000000000ff010800", "000000000000000000000000000000000000"),
    "icedelt2.def": ("icedelt2.def", "ffffffffffff000000000000ff010800", "000000000000000000000000000000000000"),
    "icedelt3.def": ("icedelt3.def", "ffffffffffff000000000000ff010800", "000000000000000000000000000000000000"),
    "icedelt4.def": ("icedelt4.def", "ffffffffffff000000000000ff010800", "000000000000000000000000000000000000"),
    "lavdelt1.def": ("lavdelt1.def", "ffffffffffff000000000000ff018000", "000000000000000000000000000000000000"),
    "lavdelt2.def": ("lavdelt2.def", "ffffffffffff000000000000ff018000", "000000000000000000000000000000000000"),
    "lavdelt3.def": ("lavdelt3.def", "ffffffffffff000000000000ff018000", "000000000000000000000000000000000000"),
    "lavdelt4.def": ("lavdelt4.def", "ffffffffffff000000000000ff018000", "000000000000000000000000000000000000"),
    "muddelt1.def": ("muddelt1.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "muddelt2.def": ("muddelt2.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "muddelt3.def": ("muddelt3.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
    "muddelt4.def": ("muddelt4.def", "ffffffffffff000000000000ff01c000", "000000000000000000000000000000000000"),
}


# The h3m tree classes (101 conifers, 119 dead trees, 125 palms,
# 130 log, 147 rough/subterra/snow trees, 153 stumps, 155 deciduous
# trees; the class 57 is the obelisk, not a tree) carry their sprite
# variants as DIFFERENT DEF NAMES under the same subclass 0
# (AVLtr1d0.def = deciduous tree, AVLdead6.def = big dead tree,
# AVLswmp3.def = swamp tree, ...), and the variants have different
# footprints (the 6-byte passability mask ranges from 1 to 7 blocked
# cells) - so the def name, not the subclass, carries the sprite
# size.
H3M_TREE_CLASSES = {101, 119, 125, 130, 135, 137, 147, 153, 155}


# True game object class of the tree defs, from the game's own
# Objects.txt: an emitted tree instance carries the class of its
# DEF, not the class key of the conversion tables (AVLr04r0 is a
# class 147 tree even when the pair table stores it under the
# deciduous class key, AVLtr1d0 a class 155 one, ...). Unknown defs
# keep the class the table gave.
H3M_DEF_OBJECT_CLASS = {
    "avld3sn0.def": 119,
    "avldead0.def": 119, "avldead1.def": 119, "avldead2.def": 119,
    "avldead3.def": 119, "avldead4.def": 119, "avldead5.def": 119,
    "avldead6.def": 119, "avldead7.def": 119,
    "avldlog.def": 130,
    "avldt1s0.def": 119, "avldt2s0.def": 119, "avldt3s0.def": 119,
    "avlklp10.def": 125, "avlklp20.def": 125,
    "avlp1sn0.def": 153, "avlp2sn0.def": 153,
    "avlplm30.def": 155, "avlplm50.def": 155,
    "avlr04r0.def": 147,
    "avlroug0.def": 155, "avlroug1.def": 155, "avlroug2.def": 155,
    "avlautr0.def": 135, "avlautr1.def": 135,
    "avlautr2.def": 135, "avlautr3.def": 135,
    "avlautr4.def": 135, "avlautr5.def": 135,
    "avlpntr0.def": 137, "avlpntr1.def": 137,
    "avlpntr2.def": 137, "avlpntr3.def": 137,
    "avlpntr4.def": 137, "avlpntr5.def": 137,
    "avlsntr0.def": 137, "avlsntr1.def": 137,
    "avlsntr2.def": 137, "avlsntr3.def": 137,
    "avlsntr4.def": 137, "avlsntr5.def": 137,
    "avlr2sn0.def": 147, "avlr6sn0.def": 147,
    "avlstm1.def": 153, "avlstm2.def": 153, "avlstm3.def": 153,
    "avlswmp0.def": 155, "avlswmp1.def": 155, "avlswmp2.def": 155,
    "avlswmp3.def": 155, "avlswmp4.def": 155, "avlswmp5.def": 155,
    "avlswp60.def": 119, "avlswp70.def": 119,
    "avltr1d0.def": 155, "avltr2d0.def": 155, "avltr3d0.def": 155,
    "avlwlw10.def": 155, "avlwlw20.def": 155, "avlwlw30.def": 155,
    "avlyuc10.def": 155, "avlyuc20.def": 155, "avlyuc30.def": 155,
    "avtchst0.def": 101,
}


def h3m_def_object_class(def_name, default_class):
    """True game object class of a tree def (see
    H3M_DEF_OBJECT_CLASS), or the table class when unknown."""
    return H3M_DEF_OBJECT_CLASS.get((def_name or "").lower(),
                                    default_class)


# A tree conversion entry may list several equivalent H3 defs (same
# footprint, same land): one of them is chosen at random when the
# H3 map is written, so repeated conversions vary the tree models.
import random as _random


def _h3m_tree_def_pick(value):
    """One def name out of a conversion table entry: a plain string
    passes through; a list of alternatives picks one at random - an
    alternative whose BLOCKED CELLS differ from the first def is
    dropped, so the random choice never changes the footprint (the
    anchor shift is computed once per object, and a different cell
    layout would misalign the instance)."""
    if not isinstance(value, (list, tuple)):
        return value
    names = [n for n in value if isinstance(n, str)]
    if not names:
        return None
    if len(names) == 1:
        return names[0]
    base = _fh2m_forest_tree_cells(names[0])
    same = [n for n in names
            if _fh2m_forest_tree_cells(n) == base]
    return _random.choice(same or [names[0]])


# The H3 line (road / river) sprite patterns of the game's own editor
# (VCMI CDrawRoadsOperation.cpp, the rules the H3 map editor uses to
# pick the piece of a drawn road). Per pattern: the 3x3 neighborhood
# grid in map order (NW, N, NE / W, center, E / SW, S, SE; '+' = the
# neighbor carries the line, '-' = it does not, '?' = anything), the
# sprite range the editor picks from at random, and the allowed
# flips. The FIRST matching pattern wins; the flip becomes the
# mirror bits 0x10 (E<->W) / 0x20 (N<->S).
#
# The piece inventory this encodes: the angle pieces 2-5 are the
# "mixed" pieces - a diagonal band from the SW corner to the NE
# corner that also joins the E and S edges; the turn pieces 0-1 are
# the cardinal corners; 6-9 the T-junctions; 10-13 the straights
# (two visual variants each); 14-15 the end caps; 16 the X-cross.
# Road/river sprite patterns of the SoD editor, inferred from a
# user-corrected map (Barbarian vs Wizard.h3m) plus real H3 maps.
# Each entry is (row1, row2, row3, (lo, hi), mirror bits): a 3x3
# neighborhood written row-major ('+' = line, '-' = no line,
# '?' = anything, the center is always the line tile itself), the
# random sprite range the editor picks within, and the mirroring
# bits (road 0x10/0x20, river 0x04/0x08) of that orientation.
# The grid is written in its final orientation: the mirroring bits
# are what the game applies on top of the base sprite.
#
# The angle pieces (sprites 2-5) are the "mixed pieces" the game
# draws when a corner also touches a diagonal neighbor: the SoD
# editor prefers them over the plain turn pieces whenever one of
# the two diagonals adjacent to the corner carries a line, and
# uses them for pure diagonal connections as well.
H3M_LINE_PATTERNS = [
    # X cross
    ("?+?", "+++", "?+?", (16, 16), 0x00),
    # T horizontal (N+E+S), mirrored (N+W+S)
    ("?+?", "-++", "?+?", (6, 7), 0x00),
    ("?+?", "++-", "?+?", (6, 7), 0x10),
    # T vertical (E+S+W), flipped (E+N+W)
    ("?-?", "+++", "?+?", (8, 9), 0x00),
    ("?+?", "+++", "?-?", (8, 9), 0x20),
    # straight horizontal / vertical
    ("?-?", "+++", "?-?", (12, 13), 0x00),
    ("?+?", "-+-", "?+?", (10, 11), 0x00),
    # angle, E+S corner with a line on the NE or SW corner (the
    # diagonal the mixed piece cuts through)
    ("??+", "?++", "?+?", (2, 5), 0x00),
    ("???", "?++", "+??", (2, 5), 0x00),
    # angle, W+S corner with a line on the NW or SE corner
    ("+??", "++?", "?+?", (2, 5), 0x10),
    ("???", "++?", "??+", (2, 5), 0x10),
    # angle, N+E corner with a line on the NW or SE corner
    ("++?", "?++", "???", (2, 5), 0x20),
    ("?+?", "?++", "??+", (2, 5), 0x20),
    # angle, N+W corner with a line on the NE or SW corner
    ("?++", "++?", "???", (2, 5), 0x30),
    ("?+?", "++?", "+??", (2, 5), 0x30),
    # angle, a pure NE<->SW / NW<->SE diagonal band (no edge)
    ("--+", "-+-", "+--", (2, 5), 0x00),
    ("+-+", "-+-", "--+", (2, 5), 0x10),
    # turn: a cardinal corner (two edges, no diagonal)
    ("?-?", "-++", "?+?", (0, 1), 0x00),
    ("?-?", "++-", "?+?", (0, 1), 0x10),
    ("?+?", "-++", "?-?", (0, 1), 0x20),
    ("?+?", "++-", "?-?", (0, 1), 0x30),
    # dead end horizontal / vertical
    ("?-?", "-++", "?-?", (15, 15), 0x00),
    ("?-?", "++-", "?-?", (15, 15), 0x10),
    ("?-?", "-+-", "?+?", (14, 14), 0x00),
    ("?+?", "-+-", "?-?", (14, 14), 0x20),
    # single tile (fallback)
    ("?-?", "-+-", "?-?", (14, 14), 0x00),
]


def h3m_line_pattern_sprite(has_line, x, y):
    """(sprite, mirror bits) the game's editor picks for a road tile at
    (x, y): the first matching neighborhood pattern of
    H3M_LINE_PATTERNS, the sprite chosen at random within the
    pattern's range. has_line(nx, ny) tells whether the neighbor tile
    carries the line. (None, None) when no pattern matches - a bend
    (corner + edge) no H3 piece draws."""
    for r1, r2, r3, (lo, hi), mbits in H3M_LINE_PATTERNS:
        grid = r1 + r2 + r3
        ok = True
        for i in range(9):
            if i == 4:
                continue
            rule = grid[i]
            if rule == "?":
                continue
            has = has_line(x + (i % 3) - 1, y + (i // 3) - 1)
            if (rule == "+") != has:
                ok = False
                break
        if ok:
            return _random.randint(lo, hi), mbits
    return None, None


# The terrain-variant tables of the landscape objects are keyed by
# h3m terrain names, while the fh2m -> unified step works with the
# unified (Heroes II) names: normalize at the entry points below
# (Desert/Wasteland -> Rough, Beach -> Sand).
FH2M_UNIFIED_TO_H3M_TERRAIN = {
    "Water": "Water", "Grass": "Grass", "Snow": "Snow",
    "Swamp": "Swamp", "Lava": "Lava", "Desert": "Rough",
    "Dirt": "Dirt", "Wasteland": "Rough", "Beach": "Sand",
    "Subterranean": "Subterranean", "Rock": "Rock",
}


def _h3_tile_terrain(tile_terrain):
    """h3m terrain name for a unified (fh2m) or h3m terrain name."""
    if tile_terrain is None:
        return None
    return FH2M_UNIFIED_TO_H3M_TERRAIN.get(tile_terrain, tile_terrain)


def h3m_passability_cells(mask_hex):
    """Blocked cells (dx, dy) of a 6-byte h3m passability mask, as
    map offsets from the object anchor (tile = anchor + (dx, dy), y
    grows southward): a clear bit blocks; bit 47 (byte 5, MSB) is
    the anchor cell, the columns run west from it (MSB-first) and
    the rows north."""
    b = bytes.fromhex(mask_hex)
    return [(-c, r - 5) for r in range(6) for c in range(8)
            if not (b[r] >> (7 - c)) & 1]


def _normalized_cells(cells):
    """Shape of footprint cells, invariant by translation: the cells
    re-based on their north-west corner, sorted."""
    cells = list(cells)
    if not cells:
        return ()
    mx = min(x for x, _ in cells)
    my = min(y for _, y in cells)
    return tuple(sorted((x - mx, y - my) for x, y in cells))

# True footprints of the fh2m LANDSCAPE_TREES objects, from the
# fheroes2 object catalog (src/fheroes2/maps/map_object_info.cpp,
# populateLandscapeTrees): the groundLevelParts offsets on the
# OBJECT_LAYER/BACKGROUND_LAYER layers, as map offsets from the
# object anchor tile.
FH2M_TREE_SHAPES = {
    "forest_a": [(-1, 0), (0, 0), (0, 1), (1, 1)],
    "forest_b": [(-1, 1), (0, 0), (0, 1), (1, 0)],
    "forest_c": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "forest_d": [(-1, 0), (0, -1), (0, 0), (1, -1)],
    "wide": [(-1, 0), (0, 0), (1, 0)],
    "pair": [(0, 0), (1, 0)],
    "west_pair": [(-1, 0), (0, 0)],
    "single": [(0, 0)],
}


def fh2m_tree_shape(index):
    """True fh2m LANDSCAPE_TREES footprint (map offsets from the
    anchor), or None for an unknown index."""
    if 0 <= index < 36:
        pos = index % 6
        if pos < 4:
            return FH2M_TREE_SHAPES["forest_" + "abcd"[pos]]
        return FH2M_TREE_SHAPES["single"]
    singles = {36: "wide", 37: "pair", 41: "pair", 42: "wide",
               50: "west_pair", 51: "pair", 52: "pair"}
    key = singles.get(index, "single")
    return FH2M_TREE_SHAPES[key] if 36 <= index <= 68 else None


def fh2m_tree_h3m_class(index, tile_terrain=None):
    """h3m class for a fh2m LANDSCAPE_TREES object, chosen so a def
    with the same footprint exists: the 4-cell forests map to the
    4-cell swamp-tree defs (class 155, the lush counterpart of the
    equally 4-cell dead trees), the stumps to 153, the dead trees to
    119 and the other singles to 155."""
    if not 0 <= index <= 68:
        return None
    if index < 36:
        return 155
    if index in (39, 40, 66, 67, 68):
        return 153
    if index in (36, 37, 38, 42) or 53 <= index <= 63:
        return 155
    return 119


# h3m tree def per (class, tile terrain), matched against the terrain
# of the tile each def instance stands on in the reference maps
# (input/*.h3m). Terrains with no observed def fall back to the
# class's generic def below.
FH2M_TREE_DEF_BY_TERRAIN = {
    101: {},  # conifers: a single def for every terrain
    # the H2 dead trees (1-cell class 119 singles) keep the dead
    # species on every land: the dead tree models (AVLdead0/1) where
    # H3 has no land-specific dead tree, the snow dead tree on Snow
    # (the H2 wasteland dead trees have no rough dead model).
    119: {"Grass": ["AVLdead0.def", "AVLdead1.def"],
          "Dirt": ["AVLdead0.def", "AVLdead1.def"],
          "Swamp": ["AVLdead0.def", "AVLdead1.def"],
          "Rough": ["AVLdead0.def", "AVLdead1.def"],
          "Sand": ["AVLdead0.def", "AVLdead1.def"],
          "Water": "AVLswp60.def", "Snow": "AVLd3sn0.def",
          "Lava": ["AVLdead0.def", "AVLdead1.def"]},
    # palms: the land palms block their tile (AVLplm30.def); the
    # passable kelp (AVLklp10.def) is the water variant only.
    125: {"Water": "AVLklp10.def"},
    130: {},  # log: AvLdlog.def
    # stumps (153): the stump defs are used on every terrain,
    # including Snow (no terrain variant).
    153: {},
    # deciduous singles: the same-terrain 1-cell tree everywhere -
    # the dead tree on Dirt and on Lava (no lava-native tree family:
    # the burnt dead trees), the pine on Snow.
    155: {"Grass": ["AVLtr1d0.def", "AVLtr2d0.def", "AVLtr3d0.def"],
          "Dirt": ["AVLdead0.def", "AVLdead1.def"],
          "Swamp": ["AVLswmp0.def", "AVLswmp1.def"],
          "Rough": ["AVLroug0.def", "AVLroug1.def", "AVLroug2.def"],
          "Sand": ["AVLyuc10.def", "AVLyuc20.def", "AVLyuc30.def"],
          "Snow": ["AVLp1sn0.def", "AVLp2sn0.def"],
          "Lava": ["AVLdead0.def", "AVLdead1.def"]},
}

# Same-terrain 2-cell pair defs of the fh2m pair trees: the lush
# pair (idx 37) and the dead pairs (idx 41, 50, 51, 52) use the
# terrain's pair tree on Grass/Dirt/Swamp/Rough (the dead pairs
# also on Snow: the 2-cell snow trees AVLr2sn0/AVLr6sn0); Sand has
# no pair def and falls back to same-terrain single trees (see
# fh2m_tree_h3m_cover).
FH2M_PAIR_TREE_TERRAIN_DEF = {
    37: {"Grass": "AVLwlw20.def", "Dirt": ["AVLdt1s0.def", "AVLdt2s0.def"],
         "Swamp": "AVLswp60.def", "Rough": "AVLr04r0.def",
         "Lava": ["AVLdt1s0.def", "AVLdt2s0.def"]},
    41: {"Grass": "AVLwlw20.def", "Dirt": ["AVLdt1s0.def", "AVLdt2s0.def"],
         "Swamp": "AVLswp60.def", "Rough": "AVLr04r0.def",
         "Snow": ["AVLr2sn0.def", "AVLr6sn0.def"],
         "Lava": ["AVLdt1s0.def", "AVLdt2s0.def"]},
    50: {"Grass": "AVLwlw20.def", "Dirt": ["AVLdt1s0.def", "AVLdt2s0.def"],
         "Swamp": "AVLswp60.def", "Rough": "AVLr04r0.def",
         "Snow": ["AVLr2sn0.def", "AVLr6sn0.def"],
         "Lava": ["AVLdt1s0.def", "AVLdt2s0.def"]},
    51: {"Grass": "AVLwlw20.def", "Dirt": ["AVLdt1s0.def", "AVLdt2s0.def"],
         "Swamp": "AVLswp60.def", "Rough": "AVLr04r0.def",
         "Snow": ["AVLr2sn0.def", "AVLr6sn0.def"],
         "Lava": ["AVLdt1s0.def", "AVLdt2s0.def"]},
    52: {"Grass": "AVLwlw20.def", "Dirt": ["AVLdt1s0.def", "AVLdt2s0.def"],
         "Swamp": "AVLswp60.def", "Rough": "AVLr04r0.def",
         "Snow": ["AVLr2sn0.def", "AVLr6sn0.def"],
         "Lava": ["AVLdt1s0.def", "AVLdt2s0.def"]},
}

# Default (generic) def of each tree class, matching the
# FH2M_TO_H3M_CATALOG entries: used when the terrain has no observed
# variant def.
H3M_TREE_GENERIC_DEF = {
    101: "AVTchst0.def", 119: "AVLswp70.def",
    125: "AVLplm30.def", 130: "AvLdlog.def", 153: "AvLStm2.def",
    155: "AVLroug0.def",
}


# Footprint-exact h3m defs of the fh2m tree objects whose shape has
# no terrain-variant def: the 4-cell forests -> the 4-cell swamp
# trees (the lush counterpart of the equally 4-cell dead trees), the
# 3-cell singles -> the winter willow, the 2-cell dead trees -> the
# small dead trees. The 1-cell objects use the terrain variant
# tables above.
FH2M_TREE_EXACT_DEF = {}
for _i in range(0, 36):
    if _i % 6 < 4:
        FH2M_TREE_EXACT_DEF[_i] = ("AVLswmp2.def" if _i % 6 in (0, 2)
                                   else "AVLswmp3.def")
FH2M_TREE_EXACT_DEF.update({
    36: "AVLwlw10.def", 37: "AVLwlw20.def",
    41: "AVLdt1s0.def", 42: "AVLwlw10.def",
    50: "AVLdt2s0.def", 51: "AVLdt1s0.def", 52: "AVLdt2s0.def",
})

# Species-faithful per-index conversions: the H2 autumn trees (12-17,
# the Grass family with the autumn look) become the H3 autumn trees
# (class 135) on Grass, the H2 fir trees (18-23, the Grass family
# with the fir look) the H3 pines (class 137), and the H2 snow fir
# trees (30-35, the Snow family) the H3 snow pines (class 137) -
# the 4-cell forests use the footprint-exact 4-cell trees
# (AVLAUTR4/5, AVLPNTR4/5, AVLSNTR4/5 match the a/c forest shapes,
# AVLAUTR2/3, AVLPNTR2/3, AVLSNTR2/3 the b/d ones), the singles the
# 1-cell trees. A list holds equivalent models, one picked at
# random. Other terrains keep the same-terrain cover.
FH2M_TREE_INDEX_TERRAIN_DEF = {
    (12, "Grass"): (135, ["AVLAUTR4.def", "AVLAUTR5.def"]),
    (13, "Grass"): (135, ["AVLAUTR2.def", "AVLAUTR3.def"]),
    (14, "Grass"): (135, ["AVLAUTR4.def", "AVLAUTR5.def"]),
    (15, "Grass"): (135, ["AVLAUTR2.def", "AVLAUTR3.def"]),
    (16, "Grass"): (135, ["avlautr0.def", "avlautr1.def"]),
    (17, "Grass"): (135, ["avlautr0.def", "avlautr1.def"]),
    # The H2 fir trees (18-23, the Grass family with the fir look)
    # become the H3 pines (class 137) on Grass: AVLPNTR4/5 (a/c
    # shapes), AVLPNTR2/3 (b/d), the 1-cell AVLPNTR0/1.
    (18, "Grass"): (137, ["AVLPNTR4.def", "AVLPNTR5.def"]),
    (19, "Grass"): (137, ["AVLPNTR2.def", "AVLPNTR3.def"]),
    (20, "Grass"): (137, ["AVLPNTR4.def", "AVLPNTR5.def"]),
    (21, "Grass"): (137, ["AVLPNTR2.def", "AVLPNTR3.def"]),
    (22, "Grass"): (137, ["AVLPNTR0.def", "AVLPNTR1.def"]),
    (23, "Grass"): (137, ["AVLPNTR0.def", "AVLPNTR1.def"]),
    # The H2 snow fir trees (30-35, the Snow family) become the H3
    # snow pines (class 137) on Snow: AVLSNTR4/5 (a/c shapes),
    # AVLSNTR2/3 (b/d), the 1-cell AVLSNTR0/1.
    (30, "Snow"): (137, ["AVLSNTR4.def", "AVLSNTR5.def"]),
    (31, "Snow"): (137, ["AVLSNTR2.def", "AVLSNTR3.def"]),
    (32, "Snow"): (137, ["AVLSNTR4.def", "AVLSNTR5.def"]),
    (33, "Snow"): (137, ["AVLSNTR2.def", "AVLSNTR3.def"]),
    (34, "Snow"): (137, ["AVLSNTR0.def", "AVLSNTR1.def"]),
    (35, "Snow"): (137, ["AVLSNTR0.def", "AVLSNTR1.def"]),
}


# Same-terrain tree defs used to convert the 4-cell H2 forests: a
# forest converts to same-terrain trees whose blocked cells tile the
# forest footprint exactly. The terrains with a 4-cell tree whose
# blocked cells match the forest shape (the dead trees on Dirt, the
# swamp trees on Swamp) use one exact instance per forest; the other
# terrains overlap their 2-cell pair trees - two per forest, one per
# horizontal cell pair - and the terrains without one (Sand, Snow)
# fall back to one single-cell tree per footprint cell. Terrains
# without an entry keep the single footprint-exact swamp-tree model.
FH2M_FOREST_TERRAIN_TREE = {
    # terrain: (2-cell pair def or None, 1-cell def); a list holds
    # equivalent same-footprint alternatives, one picked at random.
    "Grass": ((155, "AVLwlw20.def"),
               (155, ["AVLtr1d0.def", "AVLtr2d0.def", "AVLtr3d0.def"])),
    "Dirt": ((119, ["AVLdt1s0.def", "AVLdt2s0.def"]),
              (119, ["AVLdead0.def", "AVLdead1.def"])),
    "Swamp": ((119, "AVLswp60.def"),
              (155, ["AVLswmp0.def", "AVLswmp1.def"])),
    "Rough": ((147, "AVLr04r0.def"),
               (155, ["AVLroug0.def", "AVLroug1.def", "AVLroug2.def"])),
    "Sand": (None, (155, ["AVLyuc10.def", "AVLyuc20.def", "AVLyuc30.def"])),
    "Snow": (None, (153, ["AVLp1sn0.def", "AVLp2sn0.def"])),
    # Lava has no native tree family: the dead trees (see the exact
    # table below for the one-instance forest cover).
    "Lava": ((119, ["AVLdt1s0.def", "AVLdt2s0.def"]),
              (119, ["AVLdead0.def", "AVLdead1.def"])),
}

# 4-cell h3m trees whose blocked cells tile a 4-cell fh2m forest
# footprint exactly (one instance covers the whole forest): the
# first candidate whose shape aligns with the forest footprint wins
# (AVLdead2/AVLswmp2 match the forest_a/forest_c shapes,
# AVLdead3/AVLswmp3 the forest_b/forest_d ones). Dirt uses the dead
# trees.
FH2M_FOREST_TERRAIN_TREE_EXACT = {
    "Dirt": [(119, "AVLdead2.def"), (119, "AVLdead4.def"),
             (119, "AVLdead3.def"), (119, "AVLdead5.def")],
    "Swamp": [(155, "AVLswmp2.def"), (155, "AVLswmp4.def"),
              (155, "AVLswmp3.def"), (155, "AVLswmp5.def")],
    "Lava": [(119, "AVLdead2.def"), (119, "AVLdead4.def"),
             (119, "AVLdead3.def"), (119, "AVLdead5.def")],
}

# Fallback tree of the terrains whose 1-cell forest tree blocks the
# cell west of its anchor (AVLtr1d0): a same-class tree blocking its
# own anchor cell, so a footprint cell on the eastern map edge still
# gets its tree.
FH2M_FOREST_TERRAIN_TREE_ALT = {
    "Grass": (155, "AVLwlw30.def"),
}


def _fh2m_forest_tree_cells(def_name):
    """Blocked cells of an h3m tree def, or None when the def is
    unknown."""
    body = _h3m_def_body(None, 0, def_name)
    if not body:
        return None
    return h3m_passability_cells(body[1][:12])


def _fh2m_forest_shape_offset(cells, shape):
    """Translation aligning the def blocked cells onto the forest
    footprint cells, or None when the shapes differ."""
    if not cells:
        return None
    ox = min(x for x, _ in shape) - min(x for x, _ in cells)
    oy = min(y for _, y in shape) - min(y for _, y in cells)
    if sorted((x + ox, y + oy) for x, y in cells) == sorted(shape):
        return (ox, oy)
    return None


# Same-terrain 2-cell pair trees used to convert the 3-cell fh2m
# wide trees (idx 36 and 42) on the terrains without a 3-cell def:
# two overlapping pairs, the west pair anchoring on the fh2m anchor
# and the east pair one tile further east (they share the middle
# cell). Grass keeps its exact 3-cell willow; Sand and Snow have no
# pair tree and fall back to same-terrain single trees (see
# fh2m_tree_h3m_cover).
FH2M_WIDE_TREE_TERRAIN_PAIR = {
    "Dirt": (119, ["AVLdt1s0.def", "AVLdt2s0.def"]),
    "Swamp": (119, "AVLswp60.def"),
    "Rough": (147, "AVLr04r0.def"),
    "Lava": (119, ["AVLdt1s0.def", "AVLdt2s0.def"]),
}


def _fh2m_wide_tree_h3m_cover(tile_terrain, anchor, map_width):
    """Instances covering the 3-cell wide fh2m tree with two
    overlapping same-terrain pair trees, or None when the terrain
    has no pair tree (the caller keeps the single footprint-exact
    def)."""
    pair = FH2M_WIDE_TREE_TERRAIN_PAIR.get(tile_terrain)
    if pair is None:
        return None
    pair = (pair[0], _h3m_tree_def_pick(pair[1]))
    cells = _fh2m_forest_tree_cells(pair[1])
    if not cells or sorted(cells) != [(-1, 0), (0, 0)]:
        return None
    cover = [(pair[0], pair[1], (0, 0))]
    if (anchor is None or map_width is None
            or 0 <= anchor[0] + 1 < map_width):
        cover.append((pair[0], pair[1], (1, 0)))
    return cover


def _fh2m_class_single_tree(index, tile_terrain):
    """Same-terrain 1-cell tree (h3m class, def name) of a fh2m tree
    object's class, on a terrain with a single-tree model - or None
    when the terrain has none (Lava, Water...) or the class has no
    1-cell def."""
    if tile_terrain not in FH2M_FOREST_TERRAIN_TREE:
        return None
    h3m_class = fh2m_tree_h3m_class(index)
    if h3m_class is None:
        return None
    name = _h3m_tree_def_pick(
        (FH2M_TREE_DEF_BY_TERRAIN.get(h3m_class, {})
         .get(tile_terrain)) or H3M_TREE_GENERIC_DEF.get(h3m_class))
    cells = _fh2m_forest_tree_cells(name) if name else None
    if not cells or len(cells) != 1:
        return None
    return (h3m_def_object_class(name, h3m_class), name)


def _fh2m_singles_cover(shape, single_tree, tile_terrain, anchor,
                        map_width):
    """Instances of one same-terrain single-cell tree per footprint
    cell of a multi-cell fh2m tree: each single anchors so that its
    blocked cell is the footprint cell; when that anchor would leave
    the map, the terrain fallback tree blocks its own anchor cell.
    None when no instance could be placed."""
    def on_map(dx, dy):
        if anchor is None or map_width is None:
            return True
        return (0 <= anchor[0] + dx < map_width
                and 0 <= anchor[1] + dy < map_width)

    cells = _fh2m_forest_tree_cells(single_tree[1])
    if not cells or len(cells) != 1:
        return None
    bx, by = cells[0]
    cover = []
    for dx, dy in shape:
        ax, ay = dx - bx, dy - by
        if on_map(ax, ay):
            cover.append((single_tree[0], single_tree[1], (ax, ay)))
        elif (bx, by) != (0, 0):
            alt = FH2M_FOREST_TERRAIN_TREE_ALT.get(tile_terrain)
            if alt is not None and on_map(dx, dy):
                cover.append((alt[0], alt[1], (dx, dy)))
    return cover or None


def fh2m_tree_h3m_cover(index, tile_terrain, anchor=None,
                         map_width=None):
    """h3m instances covering a multi-cell fh2m tree with
    same-terrain trees: a list of (class, def name, anchor offset
    from the fh2m anchor) whose blocked cells tile the tree
    footprint exactly. The 3-cell wide trees (idx 36, 42) use two
    overlapping same-terrain pairs on the terrains that have one
    (Grass keeps its exact willow, Sand/Snow fall back to single
    trees). The 2-cell pair trees (idx 37, 41, 50, 51, 52) keep the
    terrain pair def when there is one, else fall back to single
    trees on Sand/Snow. A 4-cell forest with a same-terrain 4-cell
    tree of the forest shape uses one exact instance; the other
    forests overlap their 2-cell pair trees (one per horizontal
    cell pair), the single-cell trees covering only the cells the
    pairs cannot (no pair def for the terrain, or a pair cell
    outside the map). A single-cell tree anchors so that its blocked
    cell is the footprint cell; when that anchor would leave the
    map, the terrain fallback tree blocks its own anchor cell
    instead. None for any other tree or a terrain without a tree
    model (the caller keeps the single footprint-exact def)."""
    tile_terrain = _h3_tile_terrain(tile_terrain)
    if index in (36, 42):
        cover = _fh2m_wide_tree_h3m_cover(tile_terrain, anchor,
                                          map_width)
        if cover is not None:
            return cover
        if tile_terrain != "Grass":
            single = _fh2m_class_single_tree(index, tile_terrain)
            if single is not None:
                return _fh2m_singles_cover(fh2m_tree_shape(index),
                                            single, tile_terrain,
                                            anchor, map_width)
        return None
    if index in (37, 41, 50, 51, 52):
        if FH2M_PAIR_TREE_TERRAIN_DEF.get(index, {}).get(tile_terrain):
            return None
        single = _fh2m_class_single_tree(index, tile_terrain)
        if single is not None:
            return _fh2m_singles_cover(fh2m_tree_shape(index), single,
                                        tile_terrain, anchor, map_width)
        return None
    if not (0 <= index < 36 and index % 6 < 4):
        return None
    tree = FH2M_FOREST_TERRAIN_TREE.get(tile_terrain)
    if tree is None:
        return None
    # One random pick per cover, so the instances of one forest
    # share the same model; the classes follow the picked defs.
    pair_tree, single_tree = tree
    if pair_tree is not None:
        pair_tree = (pair_tree[0], _h3m_tree_def_pick(pair_tree[1]))
    if single_tree is not None:
        single_tree = (single_tree[0],
                       _h3m_tree_def_pick(single_tree[1]))
    shape = fh2m_tree_shape(index)

    def on_map(dx, dy):
        if anchor is None or map_width is None:
            return True
        return (0 <= anchor[0] + dx < map_width
                and 0 <= anchor[1] + dy < map_width)

    def single_cover(dx, dy):
        """Instances blocking the on-map footprint cell (dx, dy)."""
        cells = _fh2m_forest_tree_cells(single_tree[1])
        if not cells or len(cells) != 1:
            return []
        bx, by = cells[0]
        ax, ay = dx - bx, dy - by
        if on_map(ax, ay):
            return [(single_tree[0], single_tree[1], (ax, ay))]
        if (bx, by) != (0, 0):
            alt = FH2M_FOREST_TERRAIN_TREE_ALT.get(tile_terrain)
            if alt is not None and on_map(dx, dy):
                return [(alt[0], alt[1], (dx, dy))]
        return []

    # One exact 4-cell tree covers the whole footprint: among the
    # candidates of the forest shape (equivalent models), one is
    # chosen at random. The per-index species-faithful trees (the
    # H2 autumn forests) come first.
    exact_matches = []
    index_def = FH2M_TREE_INDEX_TERRAIN_DEF.get(
        (index, tile_terrain))
    if index_def is not None:
        alts = index_def[1] if isinstance(index_def[1], (list, tuple)) \
            else [index_def[1]]
        for d in alts:
            cells = _fh2m_forest_tree_cells(d)
            offset = _fh2m_forest_shape_offset(cells, shape) \
                if cells else None
            if offset is not None:
                exact_matches.append((index_def[0], d, offset))
    for exact in FH2M_FOREST_TERRAIN_TREE_EXACT.get(tile_terrain, []):
        cells = _fh2m_forest_tree_cells(exact[1])
        offset = _fh2m_forest_shape_offset(cells, shape) \
            if cells else None
        if offset is not None:
            exact_matches.append((exact[0], exact[1], offset))
    exact_matches = [e for e in exact_matches if on_map(*e[2])]
    if exact_matches:
        exact = _random.choice(exact_matches)
        return [(h3m_def_object_class(exact[1], exact[0]),
                 exact[1], exact[2])]

    cover = []
    paired_all = False
    if pair_tree is not None:
        cells = _fh2m_forest_tree_cells(pair_tree[1])
        if cells and len(cells) == 2 and cells[0] == (0, 0) \
                and cells[1] == (-1, 0):
            # Group the footprint cells into horizontal (west, east)
            # pairs; the pair tree anchors on the east cell.
            rows = {}
            for dx, dy in shape:
                rows.setdefault(dy, []).append(dx)
            paired = []
            for dy, xs in rows.items():
                xs = sorted(xs)
                if len(xs) == 2 and xs[1] == xs[0] + 1:
                    paired.append((dy, xs[0], xs[1]))
            if len(paired) == len(rows):
                for dy, wx, ex in paired:
                    if on_map(ex, dy):
                        cover.append((pair_tree[0], pair_tree[1],
                                       (ex, dy)))
                    elif on_map(wx, dy):
                        # Only the west cell is on the map: a single
                        # tree covers it.
                        cover.extend(single_cover(wx, dy))
                # The pairs cover every footprint cell.
                paired_all = True
    if not paired_all:
        # No pair def (or the shape is not pairable): one
        # single-cell tree per footprint cell.
        for dx, dy in shape:
            if on_map(dx, dy):
                cover.extend(single_cover(dx, dy))
    if not cover:
        return None
    return [(h3m_def_object_class(d, c), d, o)
            for c, d, o in cover]


def fh2m_tree_def_name(h3m_class, tile_terrain, index=None):
    """h3m tree def (sprite name) for a tree class on a given h3m tile
    terrain, so the converted tree keeps a terrain variant of the same
    footprint. The multi-cell shapes have a footprint-exact def; the
    1-cell objects use the terrain variant of their class."""
    shape = fh2m_tree_shape(index) if index is not None else None
    if shape is not None and len(shape) > 1:
        exact = _h3m_tree_def_pick(FH2M_TREE_EXACT_DEF.get(index))
        if exact is not None:
            return exact
    name = _h3m_tree_def_pick(
        FH2M_TREE_DEF_BY_TERRAIN.get(h3m_class, {}).get(tile_terrain)
        or H3M_TREE_GENERIC_DEF.get(h3m_class))
    if shape is not None and name is not None:
        body = H3M_TREE_DEFS.get(name.lower())
        if body is None or _normalized_cells(
                h3m_passability_cells(body[1][:12])) != _normalized_cells(shape):
            name = H3M_TREE_GENERIC_DEF.get(h3m_class)
    return name


# Reverse: h3m tree def name -> fh2m LANDSCAPE_TREES index with the
# same footprint (the shape anchors: 4-cell forests -> 0-3, grass
# medium mountains aside, dead trees -> 43, stumps -> 66, single
# trees -> 53). The kelp defs (passable, no blocked cell) and the
# 2x2 dead tree have no fh2m counterpart: they fall back to the
# class-level index of H3M_DECORATIVE_TO_FH2M.
H3M_TREE_DEF_TO_FH2M_INDEX = {
    # 4-cell forests (diagonal shapes)
    "avldead2.def": 0, "avldead4.def": 0,
    "avlswmp2.def": 0, "avlswmp4.def": 0,
    "avlautr4.def": 0, "avlautr5.def": 0,
    "avldead3.def": 1, "avldead5.def": 1,
    "avlswmp3.def": 1, "avlswmp5.def": 1,
    "avlautr2.def": 1, "avlautr3.def": 1,
    "avlpntr2.def": 1, "avlpntr3.def": 1,
    "avlsntr2.def": 1, "avlsntr3.def": 1,
    "avlpntr4.def": 0, "avlpntr5.def": 0,
    "avlsntr4.def": 0, "avlsntr5.def": 0,
    # 1-cell dead trees / swamp trees
    "avldead0.def": 43, "avldead1.def": 43,
    "avld3sn0.def": 43, "avlswp70.def": 43,
    # 2-cell dead trees
    "avldt1s0.def": 41, "avldt2s0.def": 50, "avlswp60.def": 41,
    # wide (3-cell) and pair (2-cell) trees
    "avlwlw10.def": 36, "avlwlw20.def": 37, "avlr04r0.def": 37,
    # single trees / conifers (1 cell)
    "avlswmp0.def": 53, "avlswmp1.def": 53, "avlwlw30.def": 53,
    "avltr1d0.def": 53, "avltr2d0.def": 53, "avltr3d0.def": 53,
    "avlroug0.def": 53, "avlroug1.def": 53, "avlroug2.def": 53,
    "avlyuc10.def": 53, "avlyuc20.def": 53, "avlyuc30.def": 53,
    "avtchst0.def": 53,
    # autumn trees (1 cell)
    "avlautr0.def": 53, "avlautr1.def": 53,
    # pines and snow pines (1 cell)
    "avlpntr0.def": 53, "avlpntr1.def": 53,
    "avlsntr0.def": 53, "avlsntr1.def": 53,
    # stumps (1 cell)
    "avlstm1.def": 66, "avlstm2.def": 66, "avlstm3.def": 66,
    "avlp1sn0.def": 66, "avlp2sn0.def": 66,
    # log and palms (1 cell): closest single-cell objects
    "avldlog.def": 39, "avlplm30.def": 38, "avlplm50.def": 38,
    # class 147 trees (rough / subterranean / snow variants, from
    # the game's Objects.txt footprints): 2-cell pairs -> the lush
    # pair, 1-cell singles -> the single tree.
    "avlr01u0.def": 37, "avlr02r0.def": 37, "avlr02u0.def": 37,
    "avlr03r0.def": 37, "avlr03u0.def": 37, "avlr04r0.def": 37,
    "avlr04u0.def": 37, "avlr05u0.def": 37, "avlr06r0.def": 37,
    "avlr07r0.def": 37, "avlr08r0.def": 37, "avlr09r0.def": 37,
    "avlr10u0.def": 37, "avlr12u0.def": 37, "avlr2sn0.def": 37,
    "avlr6sn0.def": 37, "avlrd01.def": 37, "avlrd02.def": 37,
    "avlrg01.def": 37, "avlrg02.def": 37, "avlrr05.def": 37,
    "avlr06u0.def": 53, "avlr07u0.def": 53, "avlr08u0.def": 53,
    "avlr09u0.def": 53, "avlr10r0.def": 53, "avlr11r0.def": 53,
    "avlr11u0.def": 53, "avlr12r0.def": 53, "avlr13r0.def": 53,
    "avlr13u0.def": 53, "avlr14r0.def": 53, "avlr14u0.def": 53,
    "avlr15r0.def": 53, "avlr15u0.def": 53, "avlr16u0.def": 53,
    "avlr1sn0.def": 53, "avlr3sn0.def": 53, "avlr4sn0.def": 53,
    "avlr5sn0.def": 53, "avlr7sn0.def": 53, "avlr8sn0.def": 53,
    "avlrd04.def": 53, "avlrg03.def": 53, "avlrg04.def": 53,
    "avlrg05.def": 53, "avlrg06.def": 53, "avlrg07.def": 53,
    "avlrg08.def": 53, "avlrg09.def": 53, "avlrg10.def": 53,
    "avlrg11.def": 53, "avlrr01.def": 53,
}


# The 7-cell big dead trees (AVLdead6/7) are the footprint-exact
# h3m counterparts of the fh2m grass medium mountains: they map back
# to the LANDSCAPE_MOUNTAINS group, not to a tree index.
H3M_TREE_DEF_TO_FH2M_MOUNTAIN_INDEX = {"avldead6.def": 8, "avldead7.def": 9}


def h3m_tree_def_to_fh2m_index(obj_class, def_name):
    """fh2m LANDSCAPE_TREES index for an h3m tree object, from its def
    name when known (else None: the caller falls back to the
    class-level H3M_DECORATIVE_TO_FH2M index)."""
    if obj_class not in H3M_TREE_CLASSES:
        return None
    return H3M_TREE_DEF_TO_FH2M_INDEX.get((def_name or "").lower())


# Sprite catalog of the h3m tree defs (sprite name, passability and
# landscape masks, trailing bytes), extracted from the catalogs of the
# reference maps (input/*.h3m), one entry per variant def.
H3M_TREE_DEFS = {
    "avld3sn0.def": ("AVLd3sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avldead0.def": ("AVLdead0.def", "ffffffffff7f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead1.def": ("AVLdead1.def", "ffffffffff7f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead2.def": ("AVLdead2.def", "ffffffff9f3f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead3.def": ("AVLdead3.def", "ffffffff3f9f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead4.def": ("AVLdead4.def", "ffffffff9f3f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead5.def": ("AVLdead5.def", "ffffffff3f9f000000000000ff01d000", "000000000000000000000000000000000000"),
    "avldead6.def": ("AVLdead6.def", "ffffff9f1f3f000000000000ff00d000", "000000000000000000000000000000000000"),
    "avldead7.def": ("AVLdead7.def", "ffffff3f1f9f000000000000ff00d000", "000000000000000000000000000000000000"),
    "avldlog.def": ("AvLdlog.def", "ffffffffff7f000000000000ff012500", "000000000000000000000000000000000000"),
    "avldt1s0.def": ("AVLdt1s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avldt2s0.def": ("AVLdt2s0.def", "ffffffffff3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avldt3s0.def": ("AVLdt3s0.def", "ffffffff3f3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlklp10.def": ("AVLklp10.def", "ffffffffffff000000000000ff010001", "000100000000000000000000000000000000"),
    "avlklp20.def": ("AVLklp20.def", "ffffffffffff000000000000ff010001", "000100000000000000000000000000000000"),
    "avlp1sn0.def": ("AVLp1sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlp2sn0.def": ("AVLp2sn0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlplm30.def": ("AVLplm30.def", "ffffffffff7f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlplm50.def": ("AVLplm50.def", "ffffffffffbf000000000000ff010200", "000000000000000000000000000000000000"),
    "avlr04r0.def": ("AVLr04r0.def", "ffffffffff3f000000000000ff002000", "000000000000000000000000000000000000"),
    # autumn trees (class 135), from the game's Objects.txt: the
    # 1-cell avlautr0/1, the 4-cell AVLAUTR2/3 (shapes b/d) and
    # AVLAUTR4/5 (shapes a/c).
    "avlautr0.def": ("avlautr0.def", "ffffffffff7f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlautr1.def": ("avlautr1.def", "ffffffffff7f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlautr2.def": ("AVLAUTR2.def", "ffffffff3f9f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlautr3.def": ("AVLAUTR3.def", "ffffffff3f9f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlautr4.def": ("AVLAUTR4.def", "ffffffff9f3f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlautr5.def": ("AVLAUTR5.def", "ffffffff9f3f000000000000ff010500", "000000000000000000000000000000000000"),
    # pine trees (class 137), from the game's Objects.txt: the 1-cell
    # AVLPNTR0/1, the 4-cell AVLPNTR2/3 (shapes b/d) and AVLPNTR4/5
    # (shapes a/c); the snow variants AVLSNTR0-5 with the same shapes.
    "avlpntr0.def": ("AVLPNTR0.def", "ffffffffff7f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlpntr1.def": ("AVLPNTR1.def", "ffffffffff7f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlpntr2.def": ("AVLPNTR2.def", "ffffffff3f9f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlpntr3.def": ("AVLPNTR3.def", "ffffffff3f9f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlpntr4.def": ("AVLPNTR4.def", "ffffffff9f3f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlpntr5.def": ("AVLPNTR5.def", "ffffffff9f3f000000000000ff010500", "000000000000000000000000000000000000"),
    "avlsntr0.def": ("AVLSNTR0.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsntr1.def": ("AVLSNTR1.def", "ffffffffff7f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsntr2.def": ("AVLSNTR2.def", "ffffffff3f9f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsntr3.def": ("AVLSNTR3.def", "ffffffff3f9f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsntr4.def": ("AVLSNTR4.def", "ffffffff9f3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlsntr5.def": ("AVLSNTR5.def", "ffffffff9f3f000000000000ff010800", "000000000000000000000000000000000000"),
    # 2-cell snow trees (class 147), from the game's Objects.txt:
    # the same-terrain counterpart of the H2 snow dead pairs.
    "avlr2sn0.def": ("AVLr2sn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlr6sn0.def": ("AVLr6sn0.def", "ffffffffff3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlroug0.def": ("AVLroug0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlroug1.def": ("AVLroug1.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlroug2.def": ("AVLroug2.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlstm1.def": ("AvLStm1.def", "ffffffffff7f000000000000ff002500", "000000000000000000000000000000000000"),
    "avlstm2.def": ("AvLStm2.def", "ffffffffff7f000000000000ff012500", "000000000000000000000000000000000000"),
    "avlstm3.def": ("AvLStm3.def", "ffffffffff7f000000000000ff002500", "000000000000000000000000000000000000"),
    "avlswmp0.def": ("AVLswmp0.def", "ffffffffff7f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlswmp1.def": ("AVLswmp1.def", "ffffffffff7f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlswmp2.def": ("AVLswmp2.def", "ffffffff9f3f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlswmp3.def": ("AVLswmp3.def", "ffffffff3f9f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlswmp4.def": ("AVLswmp4.def", "ffffffff9f3f000000000000ff011400", "000000000000000000000000000000000000"),
    "avlswmp5.def": ("AVLswmp5.def", "ffffffff3f9f000000000000ff011400", "000000000000000000000000000000000000"),
    "avlswp60.def": ("AVLswp60.def", "ffffffffff3f000000000000ff011000", "000100000000000000000000000000000000"),
    "avlswp70.def": ("AVLswp70.def", "ffffffffff7f000000000000ff011000", "000100000000000000000000000000000000"),
    "avltr1d0.def": ("AVLtr1d0.def", "ffffffffffbf000000000000ff011500", "000000000000000000000000000000000000"),
    "avltr2d0.def": ("AVLtr2d0.def", "ffffffffffbf000000000000ff011500", "000000000000000000000000000000000000"),
    "avltr3d0.def": ("AVLtr3d0.def", "ffffffffff7f000000000000ff011500", "000000000000000000000000000000000000"),
    "avlwlw10.def": ("AVLwlw10.def", "ffffffffff1f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlwlw20.def": ("AVLwlw20.def", "ffffffffff3f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlwlw30.def": ("AVLwlw30.def", "ffffffffff7f000000000000ff001400", "000000000000000000000000000000000000"),
    "avlyuc10.def": ("AVLyuc10.def", "ffffffffff7f000000000000ff012200", "000000000000000000000000000000000000"),
    "avlyuc20.def": ("AVLyuc20.def", "ffffffffff7f000000000000ff012200", "000000000000000000000000000000000000"),
    "avlyuc30.def": ("AVLyuc30.def", "ffffffffff7f000000000000ff012200", "000000000000000000000000000000000000"),
    "avtchst0.def": ("AVTchst0.def", "ffffffffff7f000000000080ff01ff00", "050000000000000000000000000000000000"),
}

# The h3m mountain classes (133 mound, 134 mountain, 148 dune, 158
# volcano) carry their variants as DIFFERENT DEF NAMES under subclass 0:
# the name encodes the terrain (AVLmt + gr/sn/sw/rf/vo/ds/dr/sb prefix)
# and the size (variant 1-2 big = 12 blocked cells, 3-4 medium = 5,
# 5-6 small = 4; volcanoes AVLvol10..50, dunes AVLdun10..30, mounds
# AVLmd1/2/3) - like the tree classes, the def name carries the sprite
# size.
H3M_MOUNTAIN_CLASSES = {133, 134, 148, 158}

# Default (generic) def of each mountain class, used when no
# footprint-exact def exists in the reference data.
H3M_MOUNTAIN_GENERIC_DEF = {
    133: "AVLmd1g0.def", 134: "AVLmtgr3.def", 148: "AVLdun10.def",
    158: "AVLvol40.def",
}

# fh2m LANDSCAPE_MOUNTAINS layout (fheroes2 populateLandscapeMountains):
# 8 terrain blocks in the order Generic, Grass, Snow, Swamp, Lava,
# Desert, Dirt, Wasteland - 6 objects each (big, big, medium, medium,
# small, small), the Dirt and Wasteland blocks carry 2 extra 6-cell
# mountains between the bigs and the mediums - then 11 singles
# (mounds, volcanoes, dunes).
FH2M_MOUNTAIN_TERRAIN_BLOCKS = [
    ("gn", 0, 6),    # generic
    ("gr", 6, 6),    # grass
    ("sn", 12, 6),   # snow
    ("sw", 18, 6),   # swamp
    ("vo", 24, 6),   # lava
    ("ds", 30, 6),   # desert
    ("dr", 36, 8),   # dirt
    ("rf", 44, 8),   # wasteland
]

# True footprints of the fh2m LANDSCAPE_MOUNTAINS objects, from the
# fheroes2 object catalog (src/fheroes2/maps/map_object_info.cpp):
# the groundLevelParts offsets on the OBJECT_LAYER/BACKGROUND_LAYER
# layers, as map offsets from the object anchor tile.
FH2M_MOUNTAIN_SHAPES = {
    "big_a": [(-2, -1), (-2, 0), (-1, -1), (-1, 0), (0, -1), (0, 0),
              (0, 1), (1, -1), (1, 0), (1, 1), (2, 0), (2, 1)],
    "big_b": [(-2, 0), (-2, 1), (-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 0), (0, 1), (1, -1), (1, 0), (2, -1), (2, 0)],
    "medium_a": [(-1, 0), (0, 0), (0, 1), (1, 0), (1, 1)],
    "medium_b": [(-1, 0), (-1, 1), (0, 0), (0, 1), (1, 0)],
    "grass_medium_a": [(-1, -1), (-1, 0), (0, -1), (0, 0), (0, 1),
                        (1, 0), (1, 1)],
    "grass_medium_b": [(-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1),
                        (1, -1), (1, 0)],
    "extra_a": [(-2, 0), (-1, 0), (0, 0), (0, 1), (1, 1), (2, 1)],
    "extra_b": [(-2, 1), (-1, 1), (0, 0), (0, 1), (1, 0), (2, 0)],
    "small_a": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "small_b": [(-1, 0), (0, -1), (0, 0), (1, -1)],
    "crack_medium_b": [(-1, 1), (0, 0), (0, 1), (1, 0)],
    "wide": [(-1, 0), (0, 0), (1, 0)],
    "pair": [(0, 0), (1, 0)],
}


def fh2m_mountain_shape(index):
    """True fh2m LANDSCAPE_MOUNTAINS footprint (map offsets from the
    anchor), or None for an unknown index."""
    if 0 <= index <= 51:
        for prefix, start, count in FH2M_MOUNTAIN_TERRAIN_BLOCKS:
            if start <= index < start + count:
                pos = index - start
                if prefix == "gr" and count == 6 and pos in (2, 3):
                    return FH2M_MOUNTAIN_SHAPES[
                        "grass_medium_a" if pos == 2 else "grass_medium_b"]
                if count == 8:
                    keys = ("big_a", "big_b", "extra_a", "extra_b",
                            "medium_a",
                            "medium_b" if prefix == "dr" else "crack_medium_b",
                            "small_a", "small_b")
                else:
                    keys = ("big_a", "big_b", "medium_a", "medium_b",
                            "small_a", "small_b")
                return FH2M_MOUNTAIN_SHAPES[keys[pos]]
    singles = {52: "pair", 53: "pair", 54: "wide", 55: "wide",
               56: "wide", 57: "pair", 58: "pair", 59: "pair",
               60: "wide", 61: "pair", 62: "pair"}
    key = singles.get(index)
    return FH2M_MOUNTAIN_SHAPES[key] if key else None


def _fh2m_mountain_block_prefix(index):
    """h3m class 134 def prefix of the fh2m terrain block an index
    belongs to (None for the singles)."""
    for prefix, start, count in FH2M_MOUNTAIN_TERRAIN_BLOCKS:
        if start <= index < start + count:
            return prefix
    return None


def fh2m_mountain_h3m_class(index, tile_terrain=None):
    """h3m mountain class for a fh2m LANDSCAPE_MOUNTAINS object:
    the grass mediums (7 blocked cells) only match the big dead
    trees (119); the singles keep their identity - volcanoes 158,
    dunes 148, mounds 133; the grouped mountains are 134."""
    if index in (8, 9):
        return 119
    if index in (54, 55, 56, 57):
        return 158
    if index in (58, 59, 60):
        return 148
    if 52 <= index <= 62:
        return 133
    if 0 <= index <= 51:
        return 134
    return None


def fh2m_mountain_def_name(index, h3m_class, tile_terrain=None):
    """h3m mountain def for a fh2m LANDSCAPE_MOUNTAINS object, chosen
    so its blocked cells reproduce the true fh2m footprint: the
    terrain prefix of the object's block first, then the other
    prefixes; the singles use their own def families."""
    shape = fh2m_mountain_shape(index)
    if h3m_class == 119:  # grass mediums: the 7-cell dead trees
        return "AVLdead6.def" if index == 8 else "AVLdead7.def"
    if shape is None:
        return H3M_MOUNTAIN_GENERIC_DEF.get(h3m_class)
    if h3m_class == 158:  # volcanoes
        return "AVLvol30.def" if len(shape) == 3 else "AVLvol10.def"
    if h3m_class == 148:  # dunes
        return "AVLdun30.def" if len(shape) == 3 else "AVLdun10.def"
    if h3m_class == 133:  # mounds
        suffix = {"Dirt": "d", "Grass": "g"}.get(tile_terrain, "r")
        return "AVLmd1%s0.def" % suffix
    # grouped mountains (class 134): footprint-exact terrain def
    target = _normalized_cells(shape)
    own = _fh2m_mountain_block_prefix(index)
    candidates = []
    for name, body in H3M_MOUNTAIN_DEFS.items():
        if not name.startswith("avlmt"):
            continue
        if _normalized_cells(h3m_passability_cells(body[1][:12])) == target:
            candidates.append(name)
    if candidates:
        candidates.sort(key=lambda n: (not n.startswith("avlmt%s" % own), n))
        return H3M_MOUNTAIN_DEFS[candidates[0]][0]
    return H3M_MOUNTAIN_GENERIC_DEF.get(h3m_class)


# Reverse: h3m mountain def name -> fh2m LANDSCAPE_MOUNTAINS index,
# built after the def catalog below by footprint equality (the
# terrain block of the def prefix first, then the generic block).
H3M_MOUNTAIN_DEF_TO_FH2M_INDEX = {}


# Multi-object substitutions of the h3m defs with no single
# footprint-exact fh2m counterpart (the unmatchable elements of the
# landscape inventory): def name -> list of (fh2m group, index,
# offset from the h3m anchor). The union of the fh2m footprints
# placed at the offsets reproduces the def's blocked cells exactly.
# AVLmtvo2 (11 cells) = 2 lava medium A + 1 lava medium B + 1 lava
# small A; AVLvol50 (2x3) = 2 volcano wides; AVLvol40 (a 3-row plus
# an isolated cell) = 1 volcano wide + 1 small tree (no mountain
# footprint fits a single cell); AVLdt3s0 (2x2) = 2 dead-tree pairs;
# AVLmd2r0 (1 cell) = 1 stump (no mountain blocks a single cell);
# the passable kelp = 1 passable fh2m aquatic plant (0 blocked
# cells).
H3M_DEF_TO_FH2M_SUBSTITUTION = {
    "avlmtvo2.def": [
        ("LANDSCAPE_MOUNTAINS", 26, (-3, -1)),
        ("LANDSCAPE_MOUNTAINS", 26, (-2, -2)),
        ("LANDSCAPE_MOUNTAINS", 27, (-3, -1)),
        ("LANDSCAPE_MOUNTAINS", 28, (-1, -1)),
    ],
    "avlvol50.def": [
        ("LANDSCAPE_MOUNTAINS", 54, (-2, -1)),
        ("LANDSCAPE_MOUNTAINS", 54, (-2, 0)),
    ],
    "avlvol40.def": [
        ("LANDSCAPE_MOUNTAINS", 54, (-1, 0)),
        ("LANDSCAPE_TREES", 4, (-1, -1)),
    ],
    "avldt3s0.def": [
        ("LANDSCAPE_TREES", 41, (-1, -1)),
        ("LANDSCAPE_TREES", 41, (-1, 0)),
    ],
    "avlmd2r0.def": [
        ("LANDSCAPE_TREES", 39, (0, 0)),
    ],
    "avlklp10.def": [
        ("LANDSCAPE_WATER", 4, (0, 0)),
    ],
    "avlklp20.def": [
        ("LANDSCAPE_WATER", 4, (0, 0)),
    ],
}


def h3m_mountain_def_to_fh2m_index(obj_class, def_name):
    """fh2m LANDSCAPE_MOUNTAINS index for an h3m mountain object, from
    its def name when known (else None: the caller falls back to the
    class-level H3M_DECORATIVE_TO_FH2M entry)."""
    if obj_class not in H3M_MOUNTAIN_CLASSES:
        return None
    return H3M_MOUNTAIN_DEF_TO_FH2M_INDEX.get((def_name or "").lower())


# Sprite catalog of the h3m mountain defs (sprite name, passability and
# landscape masks, trailing bytes), extracted from the catalogs of the
# reference maps (input/*.h3m), one entry per variant def.
H3M_MOUNTAIN_DEFS = {
    "avldun10.def": ("AVLdun10.def", "ffffffffff3f000000000000ff010200", "000000000000000000000000000000000000"),
    "avldun20.def": ("AVLdun20.def", "ffffffffff3f000000000000ff010200", "000000000000000000000000000000000000"),
    "avldun30.def": ("AVLdun30.def", "ffffffffff1f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlmd1d0.def": ("AVLmd1d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmd1g0.def": ("AVLmd1g0.def", "ffffffffff3f00000000000004000400", "000000000000000000000000000000000000"),
    "avlmd1r0.def": ("AVLmd1r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmd2d0.def": ("AVLmd2d0.def", "ffffffffff3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmd2g0.def": ("AVLmd2g0.def", "ffffffffff3f00000000000004000400", "000000000000000000000000000000000000"),
    "avlmd2r0.def": ("AVLmd2r0.def", "ffffffffff7f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmd3r0.def": ("AVLmd3r0.def", "ffffffffff3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtdr1.def": ("avlmtdr1.def", "ffffff87071f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr2.def": ("avlmtdr2.def", "ffffff0f07c7000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr3.def": ("avlmtdr3.def", "ffffffff1f3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr4.def": ("avlmtdr4.def", "ffffffff1f9f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr5.def": ("avlmtdr5.def", "ffffffff9f3f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr6.def": ("avlmtdr6.def", "ffffffff3f9f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr7.def": ("avlmtdr7.def", "ffffffffc71f000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtdr8.def": ("avlmtdr8.def", "ffffffff1fc7000000000000ff010100", "000000000000000000000000000000000000"),
    "avlmtds1.def": ("AVLmtds1.def", "ffffff87071f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlmtds2.def": ("AVLmtds2.def", "ffffff0f07c7000000000000ff010200", "000000000000000000000000000000000000"),
    "avlmtds4.def": ("AVLmtds4.def", "ffffffff1f9f000000000000ff010200", "000000000000000000000000000000000000"),
    "avlmtgn0.def": ("AVLmtgn0.def", "ffffff0f07c7000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgn1.def": ("AVLmtgn1.def", "ffffff87071f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgn2.def": ("AVLmtgn2.def", "ffffffff1f9f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgn3.def": ("AVLmtgn3.def", "ffffffff1f3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgn4.def": ("AVLmtgn4.def", "ffffffff3f9f000000000000ff000400", "000000000000000000000000000000000000"),
    "avlmtgn5.def": ("AVLmtgn5.def", "ffffffff9f3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgr1.def": ("AVLmtgr1.def", "ffffff87071f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgr2.def": ("AVLmtgr2.def", "ffffff0f07c7000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgr3.def": ("AVLmtgr3.def", "ffffffff1f3f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgr4.def": ("AVLmtgr4.def", "ffffffff1f9f000000000000ff010400", "000000000000000000000000000000000000"),
    "avlmtgr5.def": ("AVLmtgr5.def", "ffffffff9f3f000000000000ff000400", "000000000000000000000000000000000000"),
    "avlmtgr6.def": ("AVLmtgr6.def", "ffffffff3f9f000000000000ff000400", "000000000000000000000000000000000000"),
    "avlmtrf1.def": ("avlmtrf1.def", "ffffff87071f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtrf2.def": ("avlmtrf2.def", "ffffff0f07c7000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtrf3.def": ("avlmtrf3.def", "ffffffff1f3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtrf4.def": ("avlmtrf4.def", "ffffffff1f9f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtrf5.def": ("avlmtrf5.def", "ffffffff9f3f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtrf6.def": ("avlmtrf6.def", "ffffffff3f9f000000000000ff012000", "000000000000000000000000000000000000"),
    "avlmtsb0.def": ("AVLmtsb0.def", "ffffff0f07c7000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsb1.def": ("AVLmtsb1.def", "ffffff87071f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsb2.def": ("AVLmtsb2.def", "ffffffff1f9f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsb3.def": ("AVLmtsb3.def", "ffffffff1f3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsb4.def": ("AVLmtsb4.def", "ffffffff3f9f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsb5.def": ("AVLmtsb5.def", "ffffffff9f3f000000000000ff014000", "000000000000000000000000000000000000"),
    "avlmtsn1.def": ("AVLmtsn1.def", "ffffff87071f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlmtsn2.def": ("AVLmtsn2.def", "ffffff0f07c7000000000000ff010800", "000000000000000000000000000000000000"),
    "avlmtsn3.def": ("AVLmtsn3.def", "ffffffff1f3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlmtsn4.def": ("AVLmtsn4.def", "ffffffff1f9f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlmtsn5.def": ("AVLmtsn5.def", "ffffffff9f3f000000000000ff010800", "000000000000000000000000000000000000"),
    "avlmtsn6.def": ("AVLmtsn6.def", "ffffffff3f9f000000000000ff000800", "000000000000000000000000000000000000"),
    "avlmtsw1.def": ("AVLmtsw1.def", "ffffff87071f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlmtsw2.def": ("AVLmtsw2.def", "ffffff0f07c7000000000000ff011000", "000000000000000000000000000000000000"),
    "avlmtsw3.def": ("AVLmtsw3.def", "ffffffff1f3f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlmtsw4.def": ("AVLmtsw4.def", "ffffffff1f9f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlmtsw5.def": ("AVLmtsw5.def", "ffffffff9f3f000000000000ff001000", "000000000000000000000000000000000000"),
    "avlmtsw6.def": ("AVLmtsw6.def", "ffffffff3f9f000000000000ff011000", "000000000000000000000000000000000000"),
    "avlmtvo1.def": ("AVLmtvo1.def", "ffffff87071f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlmtvo2.def": ("AVLmtvo2.def", "ffffff8f07c7000000000000ff018000", "000000000000000000000000000000000000"),
    "avlmtvo3.def": ("AVLmtvo3.def", "ffffffff1f3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlmtvo4.def": ("AVLmtvo4.def", "ffffffff1f9f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlmtvo5.def": ("AVLmtvo5.def", "ffffffff9f3f000000000000ff008000", "000000000000000000000000000000000000"),
    "avlmtvo6.def": ("AVLmtvo6.def", "ffffffff3f9f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlvol10.def": ("AVLvol10.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlvol20.def": ("AVLvol20.def", "ffffffffff3f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlvol30.def": ("AVLvol30.def", "ffffffffff1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlvol40.def": ("AVLvol40.def", "ffffffffbf1f000000000000ff018000", "000000000000000000000000000000000000"),
    "avlvol50.def": ("AVLvol50.def", "ffffffff8f8f000000000000ff018000", "000000000000000000000000000000000000"),
}


def _fh2m_mountain_category(index):
    """Landscape family of a mountain index: the grouped blocks, the
    volcanoes, the dunes or the mounds."""
    if index <= 51:
        return "grouped"
    if 54 <= index <= 57:
        return "volcano"
    if 58 <= index <= 60:
        return "dune"
    return "mound"


for _name, _body in H3M_MOUNTAIN_DEFS.items():
    _target = _normalized_cells(h3m_passability_cells(_body[1][:12]))
    _own = _name[5:7] if _name.startswith("avlmt") else None
    _family = ("volcano" if _name.startswith("avlvol")
               else "dune" if _name.startswith("avldun")
               else "mound" if _name.startswith("avlmd") else None)
    _matches = [(_idx, fh2m_mountain_shape(_idx))
                for _idx in range(63)
                if fh2m_mountain_shape(_idx)
                and _normalized_cells(fh2m_mountain_shape(_idx)) == _target]
    if _family:
        _matches = [(i, s) for i, s in _matches
                    if _fh2m_mountain_category(i) == _family]
    elif _own:
        _matches.sort(key=lambda i_s: (
            _fh2m_mountain_block_prefix(i_s[0]) != _own,
            _fh2m_mountain_category(i_s[0]) != "grouped",
            i_s[0]))
    if _matches:
        H3M_MOUNTAIN_DEF_TO_FH2M_INDEX[_name] = _matches[0][0]


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
    # The random town (town type FF): the H2 random town object,
    # with or without its castle built. The def entry is not verified
    # against a reference map (none contains one): the sprite name
    # comes from the H3 data and the mask is the one shared by every
    # town def of the catalog.
    # The h3m random town: its own class 77 (subclass 0) with the
    # AVCranx0.def sprite - the real reference maps (all for one.h3m)
    # carry this exact entry, with the town mask of the race towns
    # and the same per-instance data layout as the class 98 towns.
    (77, 0): ("AVCranx0.def", "ffffff8f0707000000000020ff00ff00", "010000000000000000000000000000000000"),
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
    (54, 0): ("AvWPike.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Pikeman
    (54, 5): ("AVWgrix0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Royal Griffin
    (54, 3): ("AvWHCrs.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Marksman
    (54, 84): ("AVWgobl0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Goblin
    (54, 86): ("AVWwolf0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Goblin Wolf Rider
    (54, 88): ("AVWorc0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Orc
    (54, 93): ("AVWrocx0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Thunderbird (Roc upgrade)
    (54, 28): ("AVWgrem0.def", "ffffffffff7f000000000080ff010100", "000000000000000000000000000000000000"),  # Gremlin
    (56, 0): ("AVXosis0.def", "ffffffffff7f000000000080ff01ff00", "000000000000000000000000000000000000"),  # Oasis
}


# --- H2/H3 anchor alignment ---------------------------------------------
# The h3m object anchor is the south-east corner of the object's
# footprint (bit 47 of the passability mask, the bottom-right cell:
# see the hero template note in unified.py), so the blocked cells of
# an h3m def extend west (dx < 0) and north (dy < 0, the map y grows
# southward) of the anchor. The fh2m anchor semantics differ per
# family; the footprints below were deduced from the input maps by
# road-frequency analysis (map makers never paint roads on footprint
# tiles; the town calibration reproduces the documented
# castle-entrance road one tile south of the town):
#   - resource mines (0-47): dx -1..+1, dy -2..0 - the body extends
#     north of the anchor (the gate tile), roads pass at dy +1/+2;
#   - sawmills and alchemist labs (48-55): dx -2..+2, dy -3..+1;
#   - mountains: big variants 0-1 dx -1..+1 dy -2..+1, medium
#     variants 2-5 dx -1..+1 dy 0, small variants 6+ dx -1..+1
#     dy -1..+1 (the anchor sits at the center/south of the
#     footprint);
#   - trees: the anchor cell only.
# The towns keep their dedicated (+-2, 0) shift in unified.py: it
# follows the Castle X/Y relation observed in every real map
# (entrance = instance + (-2, 0)), stronger evidence than the
# statistical deduction.

def _footprint_rect(dx0, dx1, dy0, dy1):
    return [(dx, dy) for dx in range(dx0, dx1 + 1)
            for dy in range(dy0, dy1 + 1)]


# Deduced footprints of the fh2m adventure objects (the landscape
# objects use the true fheroes2 catalog shapes above).
FH2M_FOOTPRINTS = {
    "mine": _footprint_rect(-1, 1, -2, 0),
    "sawmill": _footprint_rect(-2, 2, -3, 1),
}


# The fh2m LANDSCAPE_WATER aquatic plants (fheroes2
# populateLandscapeWater): the indices 4-5 (OBJ_NONE plants) block no
# cell - the passable counterparts of the h3m kelp.
FH2M_WATER_PASSABLE_INDICES = {4, 5}


def fh2m_water_shape(index):
    """True fh2m LANDSCAPE_WATER footprint: empty (passable) for the
    aquatic plants, None for the other water objects (rocks and
    reefs, no shift model)."""
    return [] if index in FH2M_WATER_PASSABLE_INDICES else None


def fh2m_footprint(group, index):
    """fh2m footprint cells (map offsets from the anchor) of an
    object family - the true fheroes2 catalog footprints for the
    landscape objects, the deduced ones for the mines - or None
    when unknown (no shift applied)."""
    if group == "ADVENTURE_MINES":
        return FH2M_FOOTPRINTS["sawmill" if index >= 48 else "mine"]
    if group == "LANDSCAPE_MOUNTAINS":
        return fh2m_mountain_shape(index)
    if group == "LANDSCAPE_TREES":
        return fh2m_tree_shape(index)
    if group == "LANDSCAPE_WATER":
        return FH2M_LANDSCAPE_SHAPES.get((group, index),
                                         fh2m_water_shape(index))
    if group in ("LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS"):
        return FH2M_LANDSCAPE_SHAPES.get((group, index))
    return None


def fh2m_h3m_anchor_shift(h2_cells, h3_cells):
    """(dx, dy) to add to an fh2m anchor so that the h3m footprint
    (the blocked cells of its def) covers the fh2m footprint:
    minimizes the symmetric difference between the h3m cells
    translated by the shift and the fh2m cells, preferring the
    smallest shift on ties, then the western/southern one."""
    best_key, best_shift = None, None
    h2_set = set(h2_cells)
    for dx in range(-7, 8):
        for dy in range(-5, 6):
            shifted = {(x + dx, y + dy) for x, y in h3_cells}
            key = (len(shifted ^ h2_set), abs(dx) + abs(dy), -dx, -dy)
            if best_key is None or key < best_key:
                best_key, best_shift = key, (dx, dy)
    return best_shift


def _h3m_def_body(h3m_class, h3m_subclass, def_name):
    """Catalog body (sprite, 16 passability/actionability bytes hex,
    trailing bytes hex) of an h3m def: the variant def tables first,
    then the class catalog."""
    return (H3M_MINE_DEFS.get((def_name or "").lower())
            or H3M_TREE_DEFS.get((def_name or "").lower())
            or H3M_MOUNTAIN_DEFS.get((def_name or "").lower())
            or H3M_LANDSCAPE_DEFS.get((def_name or "").lower())
            or FH2M_TO_H3M_CATALOG.get((h3m_class, h3m_subclass)))


# In-game validated corrections to the computed anchor shifts,
# checked before the footprint alignment: the alchemist lab def
# (AVMalch0/AVMalcs0) is drawn one tile further west than its deduced
# footprint alignment, so the h3m instance goes one tile further east
# than the symmetric-difference minimum; the mercenary camp def
# (AVXmercn0.def) is drawn one tile further west than the fh2m
# Mercenary Camp anchor.
FH2M_TO_H3M_SHIFT_OVERRIDE = {
    ("ADVENTURE_MINES", 54): (1, 0),  # alchemist lab, generic
    ("ADVENTURE_MINES", 55): (1, 0),  # alchemist lab, snow
    ("ADVENTURE_POWER_UPS", 13): (1, 0),  # mercenary camp
    ("ADVENTURE_POWER_UPS", 5): (1, 0),   # oasis
    ("ADVENTURE_MISCELLANEOUS", 4): (1, 0),   # windmill, grass
    ("ADVENTURE_MISCELLANEOUS", 5): (1, 0),   # windmill, snow
    ("ADVENTURE_MISCELLANEOUS", 6): (1, 0),   # windmill, dirt
    ("ADVENTURE_MISCELLANEOUS", 26): (1, 0),  # witch's hut
}


def _fh2m_landscape_def_candidates(group, index, tile_terrain):
    """Footprint-exact h3m defs of a landscape object, best first:
    the terrain variant, then the class generic def (trees), or the
    terrain-block prefix then the other prefixes (mountains), or the
    footprint-exact terrain-faithful table (rocks, miscellaneous,
    water)."""
    if group in ("LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS",
                 "LANDSCAPE_WATER"):
        entry = FH2M_LANDSCAPE_GROUP_DEF.get((group, index))
        if entry is None:
            return []
        picked = _h3m_tree_def_pick(entry[1])
        return [picked] if picked else []
    if group == "LANDSCAPE_TREES":
        h3m_class = fh2m_tree_h3m_class(index)
        if h3m_class is None:
            return []
        names = []
        index_def = FH2M_TREE_INDEX_TERRAIN_DEF.get(
            (index, tile_terrain or "Grass"))
        if index_def is not None:
            picked = _h3m_tree_def_pick(index_def[1])
            if picked:
                names.append(picked)
        terrain_def = _h3m_tree_def_pick(
            FH2M_TREE_DEF_BY_TERRAIN.get(h3m_class, {})
            .get(tile_terrain or "Grass"))
        for name in (terrain_def, H3M_TREE_GENERIC_DEF.get(h3m_class)):
            if name and name not in names:
                names.append(name)
        exact = _h3m_tree_def_pick(FH2M_TREE_EXACT_DEF.get(index))
        if exact:
            names = [exact] + [n for n in names if n != exact]
        pair_def = _h3m_tree_def_pick(
            FH2M_PAIR_TREE_TERRAIN_DEF.get(index, {})
            .get(tile_terrain or "Grass"))
        if pair_def:
            names = [pair_def] + [n for n in names if n != pair_def]
        shape = fh2m_tree_shape(index)
        return [n for n in names
                if shape is not None and n.lower() in H3M_TREE_DEFS
                and _normalized_cells(h3m_passability_cells(
                    H3M_TREE_DEFS[n.lower()][1][:12]))
                == _normalized_cells(shape)]
    if group == "LANDSCAPE_MOUNTAINS":
        h3m_class = fh2m_mountain_h3m_class(index)
        if h3m_class is None:
            return []
        if h3m_class != 134:
            name = fh2m_mountain_def_name(index, h3m_class,
                                          tile_terrain or "Grass")
            return [name] if name else []
        shape = fh2m_mountain_shape(index)
        if shape is None:
            return []
        target = _normalized_cells(shape)
        own = _fh2m_mountain_block_prefix(index)
        candidates = [name for name, body in H3M_MOUNTAIN_DEFS.items()
                      if name.startswith("avlmt")
                      and _normalized_cells(h3m_passability_cells(
                          body[1][:12])) == target]
        candidates.sort(key=lambda n: (not n.startswith("avlmt%s" % own), n))
        return [H3M_MOUNTAIN_DEFS[n][0] for n in candidates]
    return []


def fh2m_landscape_def(group, index, tile_terrain, anchor=None,
                      map_width=None):
    """(h3m class, def name, anchor shift) of the footprint-exact
    h3m conversion of a landscape object: the def whose blocked
    cells reproduce the true fh2m footprint, the terrain variant
    first. With the anchor and the map width, an edge object whose
    shifted anchor would leave the map picks the first def whose
    alignment keeps the anchor on the map. None when no def of the
    object's classes matches."""
    tile_terrain = _h3_tile_terrain(tile_terrain)
    if group == "LANDSCAPE_TREES":
        h3m_class = fh2m_tree_h3m_class(index)
    elif group == "LANDSCAPE_MOUNTAINS":
        h3m_class = fh2m_mountain_h3m_class(index)
    elif group in ("LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS",
                   "LANDSCAPE_WATER"):
        entry = FH2M_LANDSCAPE_GROUP_DEF.get((group, index))
        h3m_class = entry[0] if entry else None
    else:
        return None
    if h3m_class is None:
        return None
    h2_cells = fh2m_footprint(group, index)
    if h2_cells is None:
        return None
    best = None
    for def_name in _fh2m_landscape_def_candidates(group, index,
                                                  tile_terrain):
        body = _h3m_def_body(None, 0, def_name)
        if body is None:
            continue
        h3_cells = h3m_passability_cells(body[1][:12])
        if not h2_cells:
            # A passable fh2m overlay converts to a passable def at
            # the same anchor.
            if h3_cells:
                continue
            return (h3m_def_object_class(def_name, h3m_class),
                    def_name, (0, 0))
        if not h3_cells:
            continue
        shift = fh2m_h3m_anchor_shift(h2_cells, h3_cells)
        if best is None:
            best = (h3m_def_object_class(def_name, h3m_class),
                    def_name, shift)
        if anchor is None or map_width is None:
            break
        ax, ay = anchor[0] + shift[0], anchor[1] + shift[1]
        if 0 <= ax < map_width and 0 <= ay < map_width:
            best = (h3m_def_object_class(def_name, h3m_class),
                    def_name, shift)
            break
        # The alignment leaves the map: keep the first def as the
        # fallback and try the next one.
    return best


def h3m_def_anchor_shift(group, index, def_name):
    """Anchor shift of the h3m -> fh2m direction, computed from the
    actual h3m def of the instance (its blocked cells), so the
    restored fh2m anchor realigns the footprints exactly. None when
    the def or the fh2m footprint is unknown."""
    h2_cells = fh2m_footprint(group, index)
    body = _h3m_def_body(None, 0, def_name)
    if not h2_cells or body is None:
        return None
    h3_cells = h3m_passability_cells(body[1][:12])
    if not h3_cells:
        return None
    return fh2m_h3m_anchor_shift(h2_cells, h3_cells)


def fh2m_to_h3m_anchor_shift(group, index, tile_terrain=None,
                             anchor=None, map_width=None):
    """Anchor shift (dx, dy) applied when writing an fh2m object to
    h3m: the h3m instance goes at fh2m anchor + shift so that its
    footprint covers the deduced fh2m footprint. The h3m -> fh2m
    direction applies the opposite shift, so a cross-format
    round-trip restores the original anchor. None when the family
    has no known footprint (the anchor is copied as is)."""
    h2_cells = fh2m_footprint(group, index)
    if not h2_cells:
        # Families without a deduced footprint still honour the
        # in-game validated overrides.
        return FH2M_TO_H3M_SHIFT_OVERRIDE.get((group, index))
    if group == "ADVENTURE_MINES":
        h3m_mine = FH2M_TO_H3M_MINES.get(index)
        if h3m_mine is None:
            return None
        h3m_class, h3m_subclass = h3m_mine
        def_name = fh2m_mine_def_name(index)
        body = _h3m_def_body(h3m_class, h3m_subclass, def_name)
        if body is None:
            return None
        h3_cells = h3m_passability_cells(body[1][:12])
        if not h3_cells:
            return None
        return FH2M_TO_H3M_SHIFT_OVERRIDE.get(
            (group, index), fh2m_h3m_anchor_shift(h2_cells, h3_cells))
    if group in ("LANDSCAPE_TREES", "LANDSCAPE_MOUNTAINS",
                 "LANDSCAPE_ROCKS", "LANDSCAPE_MISCELLANEOUS",
                 "LANDSCAPE_WATER"):
        chosen = fh2m_landscape_def(group, index, tile_terrain,
                                    anchor, map_width)
        if chosen is None:
            return FH2M_TO_H3M_SHIFT_OVERRIDE.get((group, index))
        return FH2M_TO_H3M_SHIFT_OVERRIDE.get((group, index), chosen[2])
    return None

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
    # monolith (45), daemon caves -> subterranean gate? no: dropped,
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
    # The Stone Liths are the Heroes II teleportation portals (two-way
    # only in H2): they convert to the h3m two-way monolith (45), the
    # H3 land teleporter. All variants map to the same color
    # (subclass 0, green) so the whole family stays one monolith
    # family, as in H2 where all liths are interlinked.
    "MISC_35": (45, 0),   # Stone Liths, generic -> two-way monolith (green)
    "MISC_36": (45, 0),   # Stone Liths, generic 2 -> two-way monolith (green)
    "MISC_37": (45, 0),   # Stone Liths, Resurrection variant -> two-way monolith (green)
    # The Observation Tower converts to the h3m Redwood Observatory
    # (class 58, AvXRedW.def) - the inverse of the h3m -> fh2m
    # pairing; the class 99 is the Trading Post, not a lookout tower.
    # The fh2m indices of the 4 tower variants differ between the
    # fheroes2 catalog versions: the open-source catalog puts them
    # at 41-44, the Olden Era editor at 42-45 (one extra object
    # before the family), so the whole 41-45 range converts.
    "MISC_41": (58, 0),   # Observation Tower, grass (open-source catalog)
    "MISC_42": (58, 0),   # Observation Tower, generic (open) / grass (Olden Era)
    "MISC_43": (58, 0),   # Observation Tower, desert (open) / generic (Olden Era)
    "MISC_44": (58, 0),   # Observation Tower, snow (open) / desert (Olden Era)
    "MISC_45": (58, 0),   # Observation Tower, snow (Olden Era catalog)
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
    # sea chest (82), flotsam -> flotsam (29), boat -> boat (8),
    # shipwreck survivor -> shipwreck survivor (86).
    "WATER_0": (59, 0),  # Bottle
    "WATER_1": (82, 0),  # Sea Chest
    "WATER_2": (29, 0),  # Flotsam
    "WATER_3": (11, 0),  # Buoy
    "WATER_4": (8, 1),   # Boat
    "WATER_5": (86, 0),  # Shipwreck Survivor
    "WATER_7": (111, 0),  # Whirlpool -> whirlpool (the H3 water teleporter)
    "WATER_10": (52, 0),  # Mermaid
    "WATER_11": (92, 0),  # Sirens
}


# h3m interactive classes with a Heroes II object equivalent,
# mapped in the h3m -> fh2m direction (the inverse pairs of the
# FH2M_TO_H3M_MISC table): the teleportation portals stay portals -
# two-way monolith and both one-way monoliths -> Stone Liths
# (H2 has a single two-way lith family), whirlpool -> Whirlpool;
# magic well -> Magic Well, mystical garden -> Magic Garden, redwood
# observatory -> Observation Tower, learning stone -> Gazebo,
# water wheel -> Water Wheel, windmill -> Windmill.
H3M_TO_FH2M_INTERACTIVE = {
    45: ("ADVENTURE_MISCELLANEOUS", 35),   # two-way monolith -> Stone Liths
    49: ("ADVENTURE_POWER_UPS", 7),        # magic well -> Magic Well
    55: ("ADVENTURE_MISCELLANEOUS", 40),   # mystical garden -> Magic Garden
    58: ("ADVENTURE_MISCELLANEOUS", 43),   # redwood observatory -> Observation Tower (generic variant)
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
    60: ("ADVENTURE_MISCELLANEOUS", 43),     # pillar of fire -> Observation Tower (generic variant)
    4: ("ADVENTURE_POWER_UPS", 22),           # arena -> Arena
    94: ("ADVENTURE_MISCELLANEOUS", 46),     # stables -> Stables
    106: ("ADVENTURE_MISCELLANEOUS", 39),    # war machine factory -> Freeman's Foundry
    64: ("ADVENTURE_POWER_UPS", 1),           # rally flag -> Watering Hole
    37: ("ADVENTURE_MISCELLANEOUS", 48),     # hut of the magi -> Hut of the Magi
    14: ("ADVENTURE_POWER_UPS", 17),          # swan pond -> Idol
    52: ("ADVENTURE_WATER", 10),              # mermaid -> Mermaid
    107: ("ADVENTURE_POWER_UPS", 22),         # school of war -> Arena
    13: ("ADVENTURE_MISCELLANEOUS", 43),      # cartographer -> Observation Tower (generic variant)
    95: ("ADVENTURE_MISCELLANEOUS", 7),       # tavern -> Oracle
    35: ("ADVENTURE_MISCELLANEOUS", 2),       # hill fort -> Hill Fort
    48: ("ADVENTURE_POWER_UPS", 0),           # magic spring -> Artesian Spring
    43: ("ADVENTURE_MISCELLANEOUS", 35),      # monolith one-way entrance -> Stone Liths
    44: ("ADVENTURE_MISCELLANEOUS", 35),      # monolith one-way exit -> Stone Liths
    51: ("ADVENTURE_POWER_UPS", 13),           # mercenary camp -> Mercenary Camp
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
    134: ("LANDSCAPE_MOUNTAINS", 2),        # mountains -> medium mountain, generic
    137: ("LANDSCAPE_MISCELLANEOUS", 11),  # plants -> pink flowers, grass
    119: ("LANDSCAPE_TREES", 43),           # dead trees -> dead tree, generic
    147: ("LANDSCAPE_ROCKS", 2),            # class 147 rocks/stalagmites
                                           # (the AVLr**/AvLR* trees are
                                           # reverse-mapped by def name)
    120: ("LANDSCAPE_MISCELLANEOUS", 18),  # flowers -> small flowers, grass
    116: ("LANDSCAPE_MISCELLANEOUS", 73),  # cacti -> small cactus, desert
    131: ("LANDSCAPE_MISCELLANEOUS", 7),   # mandrakes -> wide shrub, grass
    155: ("LANDSCAPE_TREES", 53),           # deciduous trees -> single tree, grass
    129: ("LANDSCAPE_MISCELLANEOUS", 30),  # mosses -> shrub, swamp
    118: ("LANDSCAPE_MISCELLANEOUS", 0),   # cracks -> crack, grass
    127: ("LANDSCAPE_MISCELLANEOUS", 56),  # lava lakes -> small lava pool
    161: ("LANDSCAPE_MISCELLANEOUS", 19),  # debris -> dug hole, grass
    135: ("LANDSCAPE_MOUNTAINS", 2),      # mountains (snow) -> medium mountain
    136: ("LANDSCAPE_MOUNTAINS", 2),      # mountains (dirt) -> medium mountain
    101: ("LANDSCAPE_TREES", 53),          # conifers -> single tree, grass
    126: ("LANDSCAPE_MISCELLANEOUS", 11), # flowers (tall) -> pink flowers
    128: ("LANDSCAPE_MISCELLANEOUS", 12), # flowers (wide) -> wide flowers
    125: ("LANDSCAPE_TREES", 38),          # palms -> single tree, grass
    133: ("LANDSCAPE_MOUNTAINS", 52),     # mounds -> mound, grass
    22:  ("LANDSCAPE_MISCELLANEOUS", 20), # small cliffs -> small cliff, grass
    29:  ("LANDSCAPE_WATER", 4),            # water plants -> aquatic plants
    148: ("LANDSCAPE_MOUNTAINS", 58),     # dunes -> dune
    57:  ("LANDSCAPE_TREES", 5),           # forest -> three trees, grass
    12:  ("LANDSCAPE_MISCELLANEOUS", 69), # cactus -> tiny cactus
    124: ("LANDSCAPE_MISCELLANEOUS", 19), # hole -> dug hole, grass
    130: ("LANDSCAPE_TREES", 39),          # log -> stump, generic
    132: ("LANDSCAPE_ROCKS", 13),          # moss -> medium mossy rock
    143: ("LANDSCAPE_MISCELLANEOUS", 112), # river delta -> river delta
    151: ("LANDSCAPE_MISCELLANEOUS", 102), # skull -> cow skull
    153: ("LANDSCAPE_TREES", 66),          # stump -> stump, generic
    158: ("LANDSCAPE_MOUNTAINS", 54),     # volcano -> volcano
    121: ("LANDSCAPE_MISCELLANEOUS", 26), # frozen lake -> frozen water lake, snow
    149: ("LANDSCAPE_MISCELLANEOUS", 79), # sand pit -> dug hole, desert
    117: ("LANDSCAPE_MISCELLANEOUS", 104), # canyon -> big crack, wasteland
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

# h3m artifact id -> Heroes III artifact class: 1 Treasure, 2 Minor,
# 3 Major, 4 Relic (the official RoE/AB/SoD classification). The
# artifacts with no Heroes II equivalent convert to the fh2m random
# artifact of the matching class (Relic -> Random Major per user
# decision: Heroes II has no random relic). Sources: the Heroes III
# artifact lists (weapon/shield/torso/helmet/feet/cape/necklace/
# ring/misc slots).
H3M_ARTIFACT_CLASSES = {
    7: 1, 8: 2, 9: 2, 10: 3, 11: 3, 12: 4,           # weapons
    13: 1, 14: 2, 15: 2, 16: 3, 17: 3, 18: 4,       # shields
    25: 1, 26: 2, 27: 2, 28: 3, 29: 3, 30: 4,       # torso
    19: 1, 20: 1, 21: 2, 22: 2, 23: 3, 24: 4,       # helmets
    41: 1, 98: 2, 56: 3, 59: 4, 32: 4, 90: 4,       # feet
    78: 1, 42: 2, 55: 2, 58: 3, 68: 3, 109: 3,      # capes
    83: 3, 99: 3, 72: 4,                            # capes (SoD)
    37: 1, 45: 1, 33: 4, 34: 4, 36: 4, 44: 4,       # necklaces (dragons)
    100: 1, 105: 1, 103: 1, 104: 1, 102: 1, 107: 1,  # pendant immunities
    101: 3, 106: 3, 76: 1, 54: 1, 57: 3, 66: 3,     # necklaces
    97: 1, 108: 3, 43: 3, 71: 3, 119: 2, 120: 2, 121: 3, 122: 3,  # necklaces/rings
    46: 1, 47: 1, 48: 1, 49: 1, 50: 1, 51: 1,       # luck/morale misc
    84: 1, 52: 1, 53: 1, 85: 1, 62: 3, 91: 3,       # eagle eye/archery misc
    60: 1, 61: 2,                                   # archery misc
    73: 1, 74: 1, 75: 1,                            # mana misc
    80: 3, 79: 3, 82: 3, 81: 3,                     # orbs
    86: 4, 87: 4, 88: 4, 89: 4,                     # tomes
    92: 3, 126: 4, 93: 4,                          # sphere/orb of inhibition
    63: 1, 64: 1, 65: 2,                            # eagle eye misc
    94: 1, 95: 1, 96: 3,                            # rings of life
    115: 4, 116: 3, 117: 3,                         # endless gold
    114: 2, 112: 2, 111: 3, 113: 2,                 # resource carts
    118: 1, 110: 3, 125: 3, 127: 4,                  # legion/shackles
    128: 4, 129: 4, 130: 4, 131: 4, 132: 4, 133: 4,  # combos
    134: 4, 135: 4, 136: 4, 137: 4, 138: 4, 139: 4, 140: 4,
    123: 4, 124: 4,                                 # Sea Captain's/Spellbinder's
    39: 3, 40: 4,                                   # dragon scale shield/armor
    31: 2,                                          # Armor of Wonder
    # spell book/scroll/grail and the war machines are relic-class (the
    # war machines are never rolled randomly; the class only serves the
    # no-equivalent fallback); campaign uniques are relics too.
    0: 4, 1: 4, 2: 4, 3: 4, 6: 4, 35: 4, 38: 4, 67: 4,
    69: 2, 70: 1, 77: 2,                             # rings / gloves
}

# fh2m artifact id -> Heroes II artifact class: 1 Treasure, 2 Minor,
# 3 Major, 4 Relic (the Price of Loyalty and "no random" uniques are
# bucketed as relics, the class H3 uses for its unique artifacts).
# Source: fheroes2 Artifact::Level() (src/fheroes2/resource/artifact.cpp).
FH2M_ARTIFACT_CLASSES = {
    # treasure
    **{i: 1 for i in (13, 14, 15, 16, 18, 19, 20, 21, 36, 37, 38, 39, 43,
                      46, 47, 48, 52, 56, 57, 58, 59, 60, 61, 62, 64, 65, 66)},
    # minor
    **{i: 2 for i in (10, 11, 23, 25, 27, 33, 41, 42, 44, 45, 49, 50, 51,
                      53, 54, 55, 68, 69, 75, 76, 78, 80)},
    # major
    **{i: 3 for i in (9, 12, 22, 24, 26, 28, 29, 30, 31, 32, 34, 35, 40,
                      63, 67, 72, 73, 74, 77, 79, 81)},
    # relic: "no random" uniques and the Price of Loyalty artifacts (88-103)
    **{i: 4 for i in (17, 70, 71, 82, 87)},
    **{i: 4 for i in range(88, 104)},
}

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
