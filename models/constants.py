from typing import Final, Text, Dict, List, Set
from .enums import (
    GameInitials,
    DataFolders,
    CharacterTableColumnNames,
    GIColumnNames,
    ZZZColumnNames, 
    FGOColumnNames,
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
    "ZZZ_TEAM_PREFIXES",
    "ZZZ_INCOMPLETE_CHARACTER_IDS",
    "FGO_INCOMPLETE_CHARACTER_IDS",
    "FGO_ENEMY_TARGET_TYPE",
)

# TEXT RELATED CONSTANTS
CHARACTERS_TEXT: Final[Text] = "characters"

CHARACTER_TEXT: Final[Text] = "character" 

NONE_TEXT: Final[Text] = "None" 

SELF_TEXT: Final[Text] = "Self" 

SUPPORT_TEXT: Final[Text] = "Support" 

# SYSTEM RELATED CONSTANTS
SUB_FOLDERS: Final[List[Text]] = [DataFolders.RAW, DataFolders.CLEANED]

GAME_CHOICES : Final[List[Text]] = [game.value for game in GameInitials]

GI_CHARACTER_CURVE: Final[Text] = "gi_character_curve.json"

CHARACTERS_JSON: Final[Text] = f"{CHARACTERS_TEXT}.json"

CHARACTERS_CLEANED: Final[Text] = f"{CHARACTERS_TEXT}.csv"

GAME_PARAM_INFO: Final[Dict] =  {
    ArgumentParserKwargs.NAME: "game",
    ArgumentParserKwargs.OTHER_PARAMS: {
        ArgumentParserKwargs.TYPE: str,
        ArgumentParserKwargs.CHOICES: GAME_CHOICES,
        ArgumentParserKwargs.HELP: "required game to extract character data from",
    },
},

CHARACTERS_PARSER_INFO : Final[Dict] = {
    ArgumentParserKwargs.NAME: "characters",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character data from a specified game",
    ArgumentParserKwargs.HELP: "extract all character information from a specified game into an json file.",
}

PANDAS_PARSER_INFO : Final[Dict] = {
    ArgumentParserKwargs.NAME: "pandas",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character json data to a csv file",
    ArgumentParserKwargs.HELP: "convert all character json data into an csv file.",
}

# PANDAS RELATED CONSTANTS
FGO_REGEX_CARD_HITS_DISTRIBUTION: Match[Text] = r'cardDetails\.(?:arts|quick|buster|extra)\.hitsDistribution'

ZZZ_REGEX_TEAM_CONDITION: Match[Text] = r'passive.levels\.\d{4}(?:055|507|514)\.descriptions'
ZZZ_REGEX_SIMPLE_TEAM_CONDITION: Match[Text] = 'passive.levels.7.descriptions'

ZZZ_REGEX_OR: Match[Text] = r',? or |,'

ZZZ_TEAM_PREFIXES: Final[List[Text]] = ["is an", "is a", "shares the same", "can activate"]

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

ZZZ_COLUMNS: Final[List[Text]] = [
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

GI_COLUMNS: Final[List[Text]] = [
    CharacterTableColumnNames.ID, 
    CharacterTableColumnNames.NAME,
    GIColumnNames.JP_VA,
    GIColumnNames.TITLE,
    GIColumnNames.REGION,
    GIColumnNames.AFFILIATION,
    GIColumnNames.CONSTELLATION,
    GIColumnNames.BIRTHDAY,
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

FGO_COLUMNS: Final[List[Text]] = [
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

ZZZ_INCOMPLETE_CHARACTER_IDS: Final[List[int]] = [
    1301, # Orphie & Magus
    1441, # Komano Manato
    1461, # Seed
    1051, # Yidhari
    1451, # Lucia
]

FGO_INCOMPLETE_CHARACTER_IDS: Final[List[int]] = [
    9935530, # (152) Solomon (Caster) 
    1700100, # (83) Solomon ("Grand Caster") 
    9943610, # (333) Beast IV 
    9941730, # (240) Beast III/L 
    9939130, # (168) Beast III/R 
    9935500, # (151) Goetia 
    9935400, # (149) Tiamat 
]

GI_STATS_COLUMNS: Final[Dict] = {
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

GI_SPECIAL_ENUMS_COLUMNS: Final[Dict] = {
    GIColumnNames.ELEMENT: Element,
    GIColumnNames.WEAPONTYPE: WeaponType,
    GIColumnNames.ASCENSIONSTAT: SpecialStat
}

ZZZ_STATS_COLUMNS: Final[Dict] = {
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

FGO_NP_COLUMNS: Final[Dict] ={
    FGOColumnNames.NPCARDTYPE: lambda x: x.str[FGOColumnNames.CARD],
    FGOColumnNames.NPRANKS: lambda x: x.str[FGOColumnNames.NPRANKS],
    FGOColumnNames.NPTYPES: lambda x: x.str[FGOColumnNames.NPTYPES],
    FGOColumnNames.NPTARGETEFFECT: lambda x: x.str[FGOColumnNames.EFFECTFLAGS].str[0],
}


