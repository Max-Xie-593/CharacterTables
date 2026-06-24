from typing import Final
from collections.abc import Sequence, Mapping, Set
from re import Match
from fgo_api_types.gameenums import NiceFuncTargetType
from models.general.enums import CharacterTableColumnNames
from .enums import FGOColumnNames

SELF_TEXT: Final[str] = "Self" 
SUPPORT_TEXT: Final[str] = "Support" 

FGO_REGEX_CARD_HITS_DISTRIBUTION: Match[str] = r'cardDetails\.(?:1|2|3|4)\.hitsDistribution'

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

FGO_NP_COLUMNS: Final[Mapping] = {
    FGOColumnNames.NPCARDTYPE: lambda x: x.str[FGOColumnNames.CARD],
    FGOColumnNames.NPRANKS: lambda x: x.str[FGOColumnNames.NPRANKS],
    FGOColumnNames.NPTYPES: lambda x: x.str[FGOColumnNames.NPTYPES],
    FGOColumnNames.NPTARGETEFFECT: lambda x: x.str[FGOColumnNames.EFFECTFLAGS].str[0],
}
