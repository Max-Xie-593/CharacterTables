from enum import StrEnum, auto

class FGOGrowthCurve(StrEnum):
    """Enum of FGO Growth Curves

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    LINEAR = "Linear"
    REVERSE_S = "Reverse S"
    S = "S"
    SEMI_REVERSE_S = "Semi Reverse S"
    SEMI_S = "Semi S"
    UNKNOWN = "Unknown"

class FGOColumnNames(StrEnum):
    """Enum of Column names applicable to Fate Grand Order (FGO)

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    COLLECTION_NUM = "collectionNo" # fgo_api_types
    MAXLEVEL = "lvMax" # fgo_api_types
    SERVANTCLASS = "className" # fgo_api_types
    ATTRIBUTE = auto() # fgo_api_types
    SERVANTTRAITS = "traits" # fgo_api_types
    STARABSORPTION = "starAbsorb" # fgo_api_types
    STARGENERATION = "starGen" # fgo_api_types
    DEATHCHANCE = "instantDeathChance" # fgo_api_types
    GROWTHCURVE = "growthCurve" # fgo_api_types
    CARD = auto() # fgo_api_types
    CARDS = auto() # fgo_api_types
    EFFECTFLAGS = "effectFlags" # fgo_api_types
    SKILLS = auto() # fgo_api_types
    NOBLEPHANTASMS = "noblePhantasms" # fgo_api_types
    FUNCTIONS = auto() # fgo_api_types
    FUNCTARGETTYPE = "funcTargetType" # fgo_api_types
    FUNCTARGETTEAM = "funcTargetTeam" # fgo_api_types
    FUNCPOPUPTEXT = "funcPopupText" # fgo_api_types

    CHARACTERVOICE = "profile.cv" # fgo_api_types_pandas_normalized
    ILLUSTRATOR = "profile.illustrator" # fgo_api_types_pandas_normalized
    SERVANTSTRENGTH = "profile.stats.strength" # fgo_api_types_pandas_normalized
    SERVANTENDURANCE = "profile.stats.endurance" # fgo_api_types_pandas_normalized
    SERVANTAGILITY = "profile.stats.agility" # fgo_api_types_pandas_normalized
    SERVANTMAGIC = "profile.stats.magic" # fgo_api_types_pandas_normalized
    SERVANTLUCK = "profile.stats.luck" # fgo_api_types_pandas_normalized
    SERVANTNP = "profile.stats.np" # fgo_api_types_pandas_normalized
    SERVANTALIGNMENT1 = "profile.stats.policy" # fgo_api_types_pandas_normalized
    SERVANTALIGNMENT2 = "profile.stats.personality" # fgo_api_types_pandas_normalized
    SERVANTDIVINITY = "profile.stats.deity" # fgo_api_types_pandas_normalized
    NPRANKS = "rank" # fgo_api_types_pandas_normalized
    NPTYPES = "type" # fgo_api_types_pandas_normalized

    CARDDECK = "cardDeck" # self_created
    ARTS_HITCOUNT = "artsHitCount" # self_created
    BUSTER_HITCOUNT = "busterHitCount" # self_created
    QUICK_HITCOUNT = "quickHitCount" # self_created
    EXTRA_HITCOUNT = "addattackHitCount" # self_created
    SKILLTAGS = "skillTags" # self_created
    NPCARDTYPE = "npCards" # self_created
    NPTARGETEFFECT = "targetType" # self_created
    NPTAGS = "npTags" # self_created
