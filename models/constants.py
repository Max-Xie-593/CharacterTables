from typing import Final
from collections.abc import Sequence, Mapping, Set
from .enums import (
    GameInitials,
    DataFolders,
    CharacterTableColumnNames,
    GIColumnNames,
    ZZZColumnNames, 
    FGOColumnNames,
    UmaMusuColumnNames,
    ArgumentParserKwargs,
)
from fgo_api_types.gameenums import NiceFuncTargetType
from ambr.enums import Element, WeaponType, SpecialStat
from re import Match

__all__ = (
    "GI_CHARACTER_CURVE",
    "CHARACTERS_PARSER_INFO",
    "PANDAS_PARSER_INFO",
    "GAME_PARAM_INFO",
    "CHARACTERS_JSON",
    "CHARACTERS_CLEANED",
    "GI_COLUMNS",
    "ZZZ_COLUMNS",
    "FGO_COLUMNS",
    "UMAMUSUME_COLUMNS",
    "ZZZ_TEAM_PREFIXES",
    "ZZZ_ASSIST_TYPES",
    "ZZZ_INCOMPLETE_CHARACTER_IDS",
    "FGO_INCOMPLETE_CHARACTER_IDS",
    "FGO_ENEMY_TARGET_TYPE",
    "GI_BIRTHDAY_COLUMNS",
    "UMAMUSUME_BIRTHDAY_COLUMNS",
    "UMA_COLUMN_RENAMING",
    "UMA_STATS_COLUMNS",
)

# TEXT RELATED CONSTANTS
CHARACTERS_TEXT: Final[str] = "characters"

CHARACTER_TEXT: Final[str] = "character" 

NONE_TEXT: Final[str] = "None" 

SELF_TEXT: Final[str] = "Self" 

SUPPORT_TEXT: Final[str] = "Support" 

# SYSTEM RELATED CONSTANTS
SUB_FOLDERS: Final[Sequence[str]] = [DataFolders.RAW, DataFolders.CLEANED]

GAME_CHOICES : Final[Sequence[str]] = [game.value for game in GameInitials]

GI_CHARACTER_CURVE: Final[str] = "gi_character_curve.json"

CHARACTERS_JSON: Final[str] = f"{CHARACTERS_TEXT}.json"

CHARACTERS_CLEANED: Final[str] = f"{CHARACTERS_TEXT}.csv"

GAME_PARAM_INFO: Final[Mapping] =  {
    ArgumentParserKwargs.NAME: "game",
    ArgumentParserKwargs.OTHER_PARAMS: {
        ArgumentParserKwargs.TYPE: str,
        ArgumentParserKwargs.CHOICES: GAME_CHOICES,
        ArgumentParserKwargs.HELP: "required game to extract character data from",
    },
},

CHARACTERS_PARSER_INFO : Final[Mapping] = {
    ArgumentParserKwargs.NAME: "characters",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character data from a specified game",
    ArgumentParserKwargs.HELP: "extract all character information from a specified game into an json file.",
}

PANDAS_PARSER_INFO : Final[Mapping] = {
    ArgumentParserKwargs.NAME: "pandas",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character json data to a csv file",
    ArgumentParserKwargs.HELP: "convert all character json data into an csv file.",
}

# PANDAS RELATED CONSTANTS
# FGO_REGEX_CARD_HITS_DISTRIBUTION: Match[str] = r'cardDetails\.(?:arts|quick|buster|extra)\.hitsDistribution'
FGO_REGEX_CARD_HITS_DISTRIBUTION: Match[str] = r'cardDetails\.(?:1|2|3|4)\.hitsDistribution'

ZZZ_REGEX_TEAM_CONDITION: Match[str] = r'passive.levels\.\d{4}(?:055|507|514)\.descriptions'
ZZZ_REGEX_SIMPLE_TEAM_CONDITION: Match[str] = 'passive.levels.7.descriptions'
ZZZ_REGEX_TEAM_CONDITION_TYPES: Match[str] = r'(Attack|Stun|Support|Rupture|Defense|Anomaly|Defensive Assist|[Aa]ttribute|Faction)'
ZZZ_REGEX_OR: Match[str] = r',? or |,'

ZZZ_TEAM_PREFIXES: Final[Sequence[str]] = ["is an", "is a", "shares the same", "can activate"]
ZZZ_ASSIST_TYPES: Final[Sequence[str]] = tuple(["Defensive","Evasive"])

FGO_ENEMY_TARGET_TYPE: Final[Set[NiceFuncTargetType]] = set([
    NiceFuncTargetType.enemy,
    NiceFuncTargetType.enemyAll,
    NiceFuncTargetType.enemyAnother,
    NiceFuncTargetType.enemyFull,
    NiceFuncTargetType.enemyOther,
    NiceFuncTargetType.enemyOtherFull,
    NiceFuncTargetType.enemyRandom,
    NiceFuncTargetType.enemyRange,
    NiceFuncTargetType.enemyOneAnotherRandom,
    NiceFuncTargetType.enemyOneNoTargetNoAction,
])

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

FGO_COLUMNS: Final[Sequence[str]] = [
    CharacterTableColumnNames.ID, 
    FGOColumnNames.COLLECTION_NUM,
    CharacterTableColumnNames.NAME, 
    FGOColumnNames.CHARACTERVOICE,
    FGOColumnNames.ILLUSTRATOR,

    CharacterTableColumnNames.GENDER,
    FGOColumnNames.ATTRIBUTE,
    FGOColumnNames.SERVANTALIGNMENT1,
    FGOColumnNames.SERVANTALIGNMENT2,
    FGOColumnNames.SERVANTSTRENGTH, 
    FGOColumnNames.SERVANTENDURANCE, 
    FGOColumnNames.SERVANTAGILITY, 
    FGOColumnNames.SERVANTMAGIC,
    FGOColumnNames.SERVANTLUCK,
    FGOColumnNames.SERVANTNP,
    FGOColumnNames.SERVANTDIVINITY,
    FGOColumnNames.SERVANTTRAITS,

    CharacterTableColumnNames.RARITY, 
    CharacterTableColumnNames.COST, 
    FGOColumnNames.MAXLEVEL, 
    FGOColumnNames.SERVANTCLASS,
    FGOColumnNames.GROWTHCURVE,
    
    CharacterTableColumnNames.ATKMAX,
    CharacterTableColumnNames.HPMAX,
    FGOColumnNames.STARABSORPTION, 
    FGOColumnNames.STARGENERATION, 
    FGOColumnNames.DEATHCHANCE, 

    FGOColumnNames.CARDDECK, 
    FGOColumnNames.ARTS_HITCOUNT,
    FGOColumnNames.BUSTER_HITCOUNT, 
    FGOColumnNames.QUICK_HITCOUNT, 
    FGOColumnNames.EXTRA_HITCOUNT, 
    
    FGOColumnNames.NPCARDTYPE, 
    FGOColumnNames.NPRANKS, 
    FGOColumnNames.NPTYPES, 
    FGOColumnNames.NPTARGETEFFECT, 
      
    FGOColumnNames.SKILLTAGS,
    FGOColumnNames.NPTAGS,
]

UMAMUSUME_STAT_BONUSES: Final[Sequence[str]] = [
    UmaMusuColumnNames.SPD_STAT_BONUS,
    UmaMusuColumnNames.STA_STAT_BONUS,
    UmaMusuColumnNames.POW_STAT_BONUS,
    UmaMusuColumnNames.GUT_STAT_BONUS,
    UmaMusuColumnNames.WIT_STAT_BONUS,
]

UMAMUSUME_BASE_STATS: Final[Sequence[str]] = [
    UmaMusuColumnNames.SPD_BASE_STAT,
    UmaMusuColumnNames.STA_BASE_STAT,
    UmaMusuColumnNames.POW_BASE_STAT,
    UmaMusuColumnNames.GUT_BASE_STAT,
    UmaMusuColumnNames.WIT_BASE_STAT,
]

UMAMUSUME_MAX_BASE_STATS: Final[Sequence[str]] = [
    UmaMusuColumnNames.SPD_MAX_BASE_STAT,
    UmaMusuColumnNames.STA_MAX_BASE_STAT,
    UmaMusuColumnNames.POW_MAX_BASE_STAT,
    UmaMusuColumnNames.GUT_MAX_BASE_STAT,
    UmaMusuColumnNames.WIT_MAX_BASE_STAT,
]

UMAMUSUME_BASE_APTITUDES: Final[Sequence[str]] = [
    UmaMusuColumnNames.TURF_APTITUDE,
    UmaMusuColumnNames.DIRT_APTITUDE,
    UmaMusuColumnNames.SPRINT_APTITUDE,
    UmaMusuColumnNames.MILE_APTITUDE,
    UmaMusuColumnNames.MEDIUM_APTITUDE,
    UmaMusuColumnNames.LONG_APTITUDE,
    UmaMusuColumnNames.FRONT_APTITUDE,
    UmaMusuColumnNames.PACE_APTITUDE,
    UmaMusuColumnNames.LATE_APTITUDE,
    UmaMusuColumnNames.END_APTITUDE,
]

UMAMUSUME_COLUMNS: Final[Sequence[str]] = [
    CharacterTableColumnNames.ID,
    CharacterTableColumnNames.NAME,
    CharacterTableColumnNames.RARITY,
    UmaMusuColumnNames.UMAMUSU_ALT,
    UmaMusuColumnNames.TITLE,
    UmaMusuColumnNames.UMAMUSU_JP_VA,

    CharacterTableColumnNames.GENDER,
    CharacterTableColumnNames.BIRTHDAY,
    
    UmaMusuColumnNames.UMAMUSU_HEIGHT,
    UmaMusuColumnNames.UMAMUSU_BUST,
    UmaMusuColumnNames.UMAMUSU_WAIST,
    UmaMusuColumnNames.UMAMUSU_HIPS,

    *UMAMUSUME_BASE_STATS,
    *UMAMUSUME_MAX_BASE_STATS,
    *UMAMUSUME_STAT_BONUSES,
    *UMAMUSUME_BASE_APTITUDES,
]

UMAMUSUME_BIRTHDAY_COLUMNS: Final[Sequence[str]] = [
    UmaMusuColumnNames.UMAMUSU_BIRTH_MONTH,
    UmaMusuColumnNames.UMAMUSU_BIRTH_DAY,
    UmaMusuColumnNames.UMAMUSU_BIRTH_YEAR,
]

ZZZ_INCOMPLETE_CHARACTER_IDS: Final[Sequence[int]] = [
    1581, # Remielle
]

FGO_INCOMPLETE_CHARACTER_IDS: Final[Sequence[int]] = [
    9935530, # (152) Solomon (Caster) 
    1700100, # (83) Solomon ("Grand Caster") 
    9943610, # (333) Beast IV 
    9941730, # (240) Beast III/L 
    9939130, # (168) Beast III/R 
    9935500, # (151) Goetia 
    9935400, # (149) Tiamat 
    9945590, # (411) E-Flare Marie
    9945600, # (412) E-Aqua Marie
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

FGO_NP_COLUMNS: Final[Mapping] = {
    FGOColumnNames.NPCARDTYPE: lambda x: x.str[FGOColumnNames.CARD],
    FGOColumnNames.NPRANKS: lambda x: x.str[FGOColumnNames.NPRANKS],
    FGOColumnNames.NPTYPES: lambda x: x.str[FGOColumnNames.NPTYPES],
    FGOColumnNames.NPTARGETEFFECT: lambda x: x.str[FGOColumnNames.EFFECTFLAGS].str[0],
}

UMA_COLUMN_RENAMING: Final[Mapping] = {
    UmaMusuColumnNames.UMAMUSU_ID: CharacterTableColumnNames.ID,
    UmaMusuColumnNames.UMAMUSU_NAME: CharacterTableColumnNames.NAME,
    UmaMusuColumnNames.UMAMUSU_RARITY: CharacterTableColumnNames.RARITY,
}

UMA_STATS_COLUMNS: Final[Mapping] = {
    UmaMusuColumnNames.UMAMUSU_BASE_STATS: UMAMUSUME_BASE_STATS,
    UmaMusuColumnNames.UMAMUSU_FIVE_STAR_STATS: UMAMUSUME_MAX_BASE_STATS,
    UmaMusuColumnNames.UMAMUSU_STAT_BONUSES: UMAMUSUME_STAT_BONUSES,
    UmaMusuColumnNames.UMAMUSU_APTITUDE: UMAMUSUME_BASE_APTITUDES,
}
