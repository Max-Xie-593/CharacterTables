from typing import Final
from collections.abc import Sequence, Mapping
from ambr.enums import Element, WeaponType, SpecialStat
from models.general.enums import CharacterTableColumnNames
from .enums import GIColumnNames

# ---------------------------------------------------------------------------
# In-flight field pruning: only the fields consumed by gi/pandas_utils.py
# are retained when model_dump_json(include=...) is called in extract_character.
#
# Layer 1 enums (no dots in value) are used as keys where applicable.
# Sub-keys inside "info" and "upgrade" only exist as dot-path enums
# (e.g. GIColumnNames.CHARACTER_BASESTATS = "upgrade.base_stats"), so
# bare string literals are used there with cross-reference comments.
# ---------------------------------------------------------------------------
GI_CHARACTER_INCLUDE_FIELDS: Final[Mapping] = {
    # Scalar top-level fields
    CharacterTableColumnNames.ID:       True,   # "id"
    CharacterTableColumnNames.NAME:     True,   # "name"
    CharacterTableColumnNames.RARITY:   True,   # "rarity"
    CharacterTableColumnNames.BIRTHDAY: True,   # "birthday" — keep whole {month, day} object
    GIColumnNames.ELEMENT:              True,   # "element"
    GIColumnNames.WEAPONTYPE:           True,   # "weapon_type"
    GIColumnNames.RELEASEDATE:          True,   # "release"
    GIColumnNames.REGION:               True,   # "region"
    GIColumnNames.ASCENSIONSTAT:        True,   # "special_stat" — used by convert_special_enums

    # talents — only "cost" per entry used by extract_energy_costs
    GIColumnNames.TALENTS: {"__all__": {"cost"}},

    # upgrade — base_stats and promotes used by extract_max_hp_atk_def
    # GIColumnNames.CHARACTER_BASESTATS = "upgrade.base_stats" (dot-path, not usable as key)
    "upgrade": {
        "base_stats",   # GIColumnNames.CHARACTER_BASESTATS = "upgrade.base_stats"
        "promotes",     # GIColumnNames.CHARACTER_PROMOTION = "upgrade.promotes"
    },

    # info — cv/title/constellation/native used for voice actor, lore fields
    # All GIColumnNames entries here are dot-paths (e.g. "info.cv"), so bare strings are used.
    "info": {
        "cv",           # GIColumnNames.CHARACTER_VOICE  = "info.cv"
        "title",        # GIColumnNames.TITLE            = "info.title"
        "constellation",# GIColumnNames.CONSTELLATION    = "info.constellation"
        "native",       # GIColumnNames.AFFILIATION      = "info.native"
    },
}

GI_CHARACTER_CURVE: Final[str] = "gi_character_curve.json"

GI_COLUMNS: Final[Sequence[str]] = [
    CharacterTableColumnNames.ID, 
    CharacterTableColumnNames.NAME,
    GIColumnNames.JP_VA,
    GIColumnNames.TITLE,
    GIColumnNames.REGION,
    GIColumnNames.AFFILIATION,
    GIColumnNames.CONSTELLATION,
    CharacterTableColumnNames.BIRTHDAY,
    GIColumnNames.RELEASEDATE,

    CharacterTableColumnNames.RARITY, 
    GIColumnNames.WEAPONTYPE, 
    GIColumnNames.ELEMENT,

    CharacterTableColumnNames.HPMAX, 
    CharacterTableColumnNames.ATKMAX, 
    CharacterTableColumnNames.DEFMAX,
    GIColumnNames.ASCENSIONSTAT, 
    GIColumnNames.ULTIMATECOST,
]

GI_BIRTHDAY_COLUMNS: Final[Sequence[str]] = [
    GIColumnNames.BIRTHDATE_MONTH,
    GIColumnNames.BIRTHDATE_DAY,
]

GI_STATS_COLUMNS: Final[Mapping] = {
    "new_cols": [
        CharacterTableColumnNames.HPMAX,
        CharacterTableColumnNames.ATKMAX,
        CharacterTableColumnNames.DEFMAX
    ],
    "upgrade_cols": [
        GIColumnNames.CHARACTER_BASESTATS,
        GIColumnNames.CHARACTER_PROMOTION
    ],
    "stat_cols" : [
        GIColumnNames.CHARACTER_BASE_HP,
        GIColumnNames.CHARACTER_BASE_ATK,
        GIColumnNames.CHARACTER_BASE_DEFENSE
    ],
}

GI_SPECIAL_ENUMS_COLUMNS: Final[Mapping] = {
    GIColumnNames.ELEMENT: Element,
    GIColumnNames.WEAPONTYPE: WeaponType,
    GIColumnNames.ASCENSIONSTAT: SpecialStat
}

GI_CHARACTER_INCLUDE_FIELDS: Final[Mapping] = {
    # General enums
    CharacterTableColumnNames.ID:       True,   # "id"
    CharacterTableColumnNames.NAME:     True,   # "name"
    CharacterTableColumnNames.RARITY:   True,   # "rarity"
    CharacterTableColumnNames.BIRTHDAY: True,   # "birthday" — keep whole {month, day} object
    # GI Layer 1 enums
    GIColumnNames.ELEMENT:              True,   # "element"
    GIColumnNames.WEAPONTYPE:           True,   # "weapon_type"
    GIColumnNames.RELEASEDATE:          True,   # "release"
    GIColumnNames.REGION:               True,   # "region"
    GIColumnNames.ASCENSIONSTAT:        True,   # "special_stat" — used by convert_special_enums  ← top-level key (see open question below)
    # talents — only "cost" per entry; no enum for bare "cost" here
    GIColumnNames.TALENTS: {"__all__": {"cost"}},
    # upgrade — sub-keys are dot-path enums; use string literals for the bare sub-keys
    # GIColumnNames.CHARACTER_BASESTATS = "upgrade.base_stats" (dot-path, not usable)
    "upgrade": {
        "base_stats",   # no bare enum
        "promotes",     # no bare enum
    },
    # info — sub-keys are dot-path enums; use string literals
    # GIColumnNames.CHARACTER_VOICE = "info.cv", TITLE = "info.title", etc.
    "info": {
        "cv",           # no bare enum
        "title",        # no bare enum
        "constellation",# no bare enum
        "native",       # no bare enum
    },
}