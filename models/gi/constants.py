from typing import Final
from collections.abc import Sequence, Mapping
from ambr.enums import Element, WeaponType, SpecialStat
from models.general.enums import CharacterTableColumnNames
from .enums import GIColumnNames

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
