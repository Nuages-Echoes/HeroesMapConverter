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
    "Random Monster", "Random Monster Level 1", "Random Monster Level 2",
    "Random Monster Level 3", "Random Monster Level 4",
]

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
