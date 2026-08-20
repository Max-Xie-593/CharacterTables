from typing import Final
from collections.abc import Sequence, Mapping
from re import Match
from models.general.enums import CharacterTableColumnNames
from .enums import ZZZColumnNames

CHARACTER_TEXT: Final[str] = "character" 

ZZZ_REGEX_TEAM_CONDITION: Match[str] = r'passive.levels\.\d{4}(?:055|507|514)\.descriptions'
ZZZ_REGEX_SIMPLE_TEAM_CONDITION: Match[str] = 'passive.levels.7.descriptions'
ZZZ_REGEX_TEAM_CONDITION_TYPES: Match[str] = r'(Attack|Stun|Support|Rupture|Defense|Anomaly|Defensive Assist|[Aa]ttribute|[Ff]action)'
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
