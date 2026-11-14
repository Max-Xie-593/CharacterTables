from typing import Final
from collections.abc import Sequence, Mapping, Set
from re import Match
from fgo_api_types.gameenums import NiceFuncTargetType
from models.general.enums import CharacterTableColumnNames
from .enums import FGOColumnNames

# ---------------------------------------------------------------------------
# In-flight field pruning: only the fields consumed by fgo/pandas_utils.py
# are retained when model_dump_json(include=...) is called in extract_character.
#
# Layer 1 enums (no dots in value) are used as keys where applicable.
# "noblePhantasms.__all__" must be a dict (not a set) because it mixes
# plain field names with a nested "functions" include spec.
# ---------------------------------------------------------------------------
FGO_SERVANT_INCLUDE_FIELDS: Final[Mapping] = {
    # Scalar top-level fields
    CharacterTableColumnNames.ID:       True,   # "id"
    CharacterTableColumnNames.NAME:     True,   # "name"
    CharacterTableColumnNames.GENDER:   True,   # "gender"
    CharacterTableColumnNames.RARITY:   True,   # "rarity"
    CharacterTableColumnNames.COST:     True,   # "cost"
    CharacterTableColumnNames.HPMAX:    True,   # "hpMax"  — matches FGO API field
    CharacterTableColumnNames.ATKMAX:   True,   # "atkMax" — matches FGO API field
    FGOColumnNames.COLLECTION_NUM:      True,   # "collectionNo"
    FGOColumnNames.MAXLEVEL:            True,   # "lvMax"
    FGOColumnNames.SERVANTCLASS:        True,   # "className"
    FGOColumnNames.ATTRIBUTE:           True,   # "attribute"
    FGOColumnNames.GROWTHCURVE:         True,   # "growthCurve"
    FGOColumnNames.STARABSORPTION:      True,   # "starAbsorb"
    FGOColumnNames.STARGENERATION:      True,   # "starGen"
    FGOColumnNames.DEATHCHANCE:         True,   # "instantDeathChance"
    FGOColumnNames.CARDS:               True,   # "cards"

    # traits — keep only "name" per trait entry
    FGOColumnNames.SERVANTTRAITS: {"__all__": {CharacterTableColumnNames.NAME}},

    # cardDetails — keep only hitsDistribution per card slot (no enum for these sub-keys)
    "cardDetails": {"__all__": {"hitsDistribution"}},

    # skills — keep only the 3 function filter fields used by aggregate_functions
    FGOColumnNames.SKILLS: {
        "__all__": {
            FGOColumnNames.FUNCTIONS: {
                "__all__": {
                    FGOColumnNames.FUNCTARGETTYPE,   # "funcTargetType"
                    FGOColumnNames.FUNCTARGETTEAM,   # "funcTargetTeam"
                    FGOColumnNames.FUNCPOPUPTEXT,    # "funcPopupText"
                }
            }
        }
    },

    # noblePhantasms — card/rank/type/effectFlags + same 3 function fields.
    # Must be a dict (not a set) so the "functions" nested spec can be included.
    FGOColumnNames.NOBLEPHANTASMS: {
        "__all__": {
            FGOColumnNames.CARD:        True,   # "card"
            FGOColumnNames.EFFECTFLAGS: True,   # "effectFlags"
            # NPRANKS/"rank" and NPTYPES/"type" values happen to match raw API field names
            FGOColumnNames.NPRANKS:     True,   # "rank"
            FGOColumnNames.NPTYPES:     True,   # "type"
            FGOColumnNames.FUNCTIONS: {
                "__all__": {
                    FGOColumnNames.FUNCTARGETTYPE,
                    FGOColumnNames.FUNCTARGETTEAM,
                    FGOColumnNames.FUNCPOPUPTEXT,
                }
            }
        }
    },

    # profile — keep cv, illustrator, stats only (drops voices, comments, costume)
    # Sub-keys only exist as dot-path enums (e.g. "profile.cv"); bare names have no enum.
    "profile": {
        "cv",           # FGOColumnNames.CHARACTERVOICE = "profile.cv" (dot-path only)
        "illustrator",  # FGOColumnNames.ILLUSTRATOR     = "profile.illustrator"
        "stats",        # keeps all stats sub-fields (strength/endurance/etc.)
    },
}

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
