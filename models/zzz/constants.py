from typing import Final
from collections.abc import Sequence, Mapping
from re import Match
from models.general.enums import CharacterTableColumnNames
from .enums import ZZZColumnNames

# ---------------------------------------------------------------------------
# In-flight field pruning: only the fields consumed by zzz/pandas_utils.py
# are retained when model_dump_json(include=...) is called in extract_character.
#
# Most ZZZColumnNames values are dot-paths (e.g. "element.name", "stats.attack"),
# so the top-level object keys ("element", "stats", "info", etc.) and their
# sub-keys must be plain string literals. Only ZZZColumnNames.CODENAME and
# ZZZColumnNames.EXTRAASCENSION are usable Layer 1 enum keys.
#
# "passive" is kept (not unused) because extract_team_condition applies a
# DataFrame column regex that targets "passive.levels.<n>.descriptions" after
# normalize_json flattens the structure.
# ---------------------------------------------------------------------------
ZZZ_AGENT_INCLUDE_FIELDS: Final[Mapping] = {
    # Scalar top-level fields
    CharacterTableColumnNames.ID:       True,   # "id"
    CharacterTableColumnNames.NAME:     True,   # "name"
    CharacterTableColumnNames.GENDER:   True,   # "gender"
    CharacterTableColumnNames.RARITY:   True,   # "rarity"
    ZZZColumnNames.CODENAME:            True,   # "code_name"
    ZZZColumnNames.EXTRAASCENSION:      True,   # "extra_ascension" — index [5] used for ascension props
    ZZZColumnNames.ASCENSIONKEY:        True,   # "ascension" — index [5] used for max HP/ATK/DEF stat calculation

    # Top-level object keys whose enum values are dot-paths — use string literals
    "element":      True,   # ZZZColumnNames.ELEMENT    = "element.name"    (dot-path)
    "specialty":    True,   # ZZZColumnNames.SPECIALTY  = "specialty.name"  (dot-path)
    "attack_type":  True,   # ZZZColumnNames.ATTACKTYPE = "attack_type.name" (dot-path)
    "faction":      True,   # ZZZColumnNames.FACTION    = "faction.name"    (dot-path)

    # info — birthday and full_name used; enum values are dot-paths
    "info": {
        "birthday",     # ZZZColumnNames.BIRTHDAY  = "info.birthday"
        "full_name",    # ZZZColumnNames.FULLNAME   = "info.full_name"
    },

    # stats — 6 stat fields used; enum values are dot-paths
    "stats": {
        "attack",           # ZZZColumnNames.ATTACK_STAT       = "stats.attack"
        "attack_growth",    # ZZZColumnNames.ATTACKGROWTH_STAT = "stats.attack_growth"
        "hp_max",           # ZZZColumnNames.HP_STAT           = "stats.hp_max"
        "hp_growth",        # ZZZColumnNames.HPGROWTH_STAT     = "stats.hp_growth"
        "defence",          # ZZZColumnNames.DEFENSE_STAT      = "stats.defence"
        "defence_growth",   # ZZZColumnNames.DEFENSEGROWTH_STAT= "stats.defence_growth"
    },

    # skills — only assist.descriptions used by extract_assist
    # ZZZColumnNames.ASSISTDESCRIPTION = "skills.assist.descriptions" (dot-path)
    "skills": {
        "assist": {"descriptions"},
    },

    # passive — levels.<n>.descriptions matched by team condition DataFrame column regex
    "passive": {
        "levels": {
            "__all__": {"descriptions"}
        }
    },
}

CHARACTER_TEXT: Final[str] = "character" 

ZZZ_REGEX_TEAM_CONDITION: Match[str] = r'passive.levels\.\d{4}(?:055|507|514)\.descriptions'
ZZZ_REGEX_SIMPLE_TEAM_CONDITION: Match[str] = 'passive.levels.7.descriptions'
ZZZ_REGEX_TEAM_CONDITION_TYPES: Match[str] = r'(Attack|Stun|Support|Rupture|Defense|Anomaly|Armorer|Defensive Assist|[Aa]ttribute|[Ff]action)'
ZZZ_REGEX_OR: Match[str] = r',? or |,'

ZZZ_TEAM_PREFIXES: Final[Sequence[str]] = ["is an", "is a", "shares the same", "can activate"]
ZZZ_ASSIST_TYPES: Final[Sequence[str]] = tuple(["Defensive","Evasive"])

ZZZ_COLUMNS: Final[Sequence[str]] = [
    CharacterTableColumnNames.ID, 
    CharacterTableColumnNames.NAME, 
    ZZZColumnNames.CODENAME, 
    ZZZColumnNames.FULLNAME,
    ZZZColumnNames.FACTION,
    ZZZColumnNames.BIRTHDAY,
    CharacterTableColumnNames.GENDER,

    CharacterTableColumnNames.RARITY, 
    ZZZColumnNames.ATTACKTYPE, 
    ZZZColumnNames.SPECIALTY, 
    ZZZColumnNames.ELEMENT,

    CharacterTableColumnNames.ATKMAX, 
    CharacterTableColumnNames.HPMAX, 
    CharacterTableColumnNames.DEFMAX, 
    ZZZColumnNames.ASCENSIONSTAT1, 
    ZZZColumnNames.ASCENSIONSTAT2, 
    ZZZColumnNames.ASSISTTYPE, 
    ZZZColumnNames.TEAMCONDITION1, 
    ZZZColumnNames.TEAMCONDITION2, 
    ZZZColumnNames.TEAMCONDITION3, 
]

ZZZ_INCOMPLETE_CHARACTER_IDS: Final[Sequence[int]] = [
    # 1581, # Remielle
]

ZZZ_STATS_COLUMNS: Final[Mapping] = {
    CharacterTableColumnNames.ATKMAX: [
        ZZZColumnNames.ASCENSIONATTACK,
        ZZZColumnNames.ATTACK_STAT,
        ZZZColumnNames.ATTACKGROWTH_STAT,
        ZZZColumnNames.ASCENSIONKEY
    ],
    CharacterTableColumnNames.HPMAX: [
        ZZZColumnNames.ASCENSIONHP,
        ZZZColumnNames.HP_STAT,
        ZZZColumnNames.HPGROWTH_STAT,
        ZZZColumnNames.ASCENSIONKEY
    ],
    CharacterTableColumnNames.DEFMAX: [
        ZZZColumnNames.ASCENSIONDEFENSE,
        ZZZColumnNames.DEFENSE_STAT,
        ZZZColumnNames.DEFENSEGROWTH_STAT,
        ZZZColumnNames.ASCENSIONKEY
    ],
}
