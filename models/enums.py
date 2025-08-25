from enum import StrEnum, auto

class GameInitials(StrEnum): 
    """Enum of various games

    Args:
        StrEnum (class): class to enforce string enums
    """
    GI = auto()
    ZZZ = auto()
    FGO = auto()

class DataFolders(StrEnum):
    """Enum of folder names

    Args:
        StrEnum (class): class to enforce string enums
    """
    DATA = auto()
    RAW = auto()
    CLEANED = auto()

class ArgumentParserKwargs(StrEnum):
    """Enum of Keyword Arguments for ArgumentParser

    Args:
        StrEnum (_type_): class to enforce string enums
    """

    NAME = auto()
    DESCRIPTION = auto()
    HELP = auto()
    CHOICES = auto()
    TYPE = auto()
    RUN = auto()
    OTHER_PARAMS = auto()

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

class CharacterTableColumnNames(StrEnum):
    """Enum of Column names applicable to any game

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    ID = auto()
    RARITY = auto()
    NAME = auto()
    GENDER = auto()
    COST = auto()
    HPMAX = "hpMax"
    ATKMAX = "atkMax"
    DEFMAX = "defMax"


class GIColumnNames(StrEnum):
    """Enum of Column names applicable to Genshin Impact (GI)

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    REGION = auto() # ambr
    RELEASEDATE = "release" # ambr
    TALENTS = auto() # ambr
    BASE_STATS_PROP_TYPE = "prop_type" # ambr
    BASE_STATS_INIT_VALUE = "init_value" # ambr
    BASE_STATS_GROWTH_TYPE = "growth_type" # ambr
    PROMOTION_ADD_STATS = "add_stats" # ambr
    PROMOTION_UNLOCK_MAX_LEVEL = "unlock_max_level" # ambr
    PROMOTION_STAT_VALUE = "value" # ambr
    CURVEINFO = "curveInfos" # ambr (avatar curve)
    CHARACTER_BASE_HP = "FIGHT_PROP_BASE_HP" # ambr
    CHARACTER_BASE_ATK = "FIGHT_PROP_BASE_ATTACK" # ambr
    CHARACTER_BASE_DEFENSE = "FIGHT_PROP_BASE_DEFENSE" # ambr
    VOICE_ACTOR = "va" # ambr

    AFFILIATION = "info.native" # ambr_pandas_normalized
    CONSTELLATION = "info.constellation" # ambr_pandas_normalized
    TITLE = "info.title" # ambr_pandas_normalized
    CHARACTER_VOICE = "info.cv" # ambr_pandas_normalized
    BIRTHDATE_MONTH = "birthday.month" # ambr_pandas_normalized
    BIRTHDATE_DAY = "birthday.day" # ambr_pandas_normalized
    CHARACTER_BASESTATS = "upgrade.base_stats" # ambr_pandas_normalized
    CHARACTER_PROMOTION = "upgrade.promotes" # ambr_pandas_normalized
    
    ELEMENT = auto() # self_created
    WEAPONTYPE = "weapon_type" # self_created
    BIRTHDAY = auto() # self_created
    
    ULTIMATECOST = "ultimate_cost" # self_created
    ASCENSIONSTAT = "special_stat" # self_created
    JP_VA = auto() # self_created

class ZZZColumnNames(StrEnum):
    """Enum of Column names applicable to Zenless Zone Zero (ZZZ)

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    CODENAME = "code_name" # hakushin
    EXTRAASCENSION = "extra_ascension" # hakushin
    PROPS = auto() # hakushin
    ASCENSIONKEY = "ascension" # hakushin
    ASCENSIONATTACK = "attack" # hakushin
    ASCENSIONHP = "max_hp" # hakushin
    ASCENSIONDEFENSE = "defense" # hakushin
    
    ELEMENT = "element.name" # hakushin_pandas_normalized
    SPECIALTY = "specialty.name" # hakushin_pandas_normalized
    ATTACKTYPE = "attack_type.name" # hakushin_pandas_normalized
    FACTION = "faction.name" # hakushin_pandas_normalized
    BIRTHDAY = "info.birthday" # hakushin_pandas_normalized
    FULLNAME = "info.full_name" # hakushin_pandas_normalized
    ASSISTDESCRIPTION = "skills.Assist.descriptions" # hakushin_pandas_normalized
    ATTACK_STAT = "stats.Attack" # hakushin_pandas_normalized
    ATTACKGROWTH_STAT = "stats.AttackGrowth" # hakushin_pandas_normalized
    HP_STAT = "stats.HpMax" # hakushin_pandas_normalized
    HPGROWTH_STAT = "stats.HpGrowth" # hakushin_pandas_normalized
    DEFENSE_STAT = "stats.Defence" # hakushin_pandas_normalized
    DEFENSEGROWTH_STAT = "stats.DefenceGrowth" # hakushin_pandas_normalized

    ASCENSIONSTAT1 = "ascension_stat_1" # self_created
    ASCENSIONSTAT2 = "ascension_stat_2" # self_created
    ASSISTTYPE = "assist_type" # self_created
    TEAMCONDITION1 = "team_condition_1" # self_created
    TEAMCONDITION2 = "team_condition_2" # self_created
    TEAMCONDITION3 = "team_condition_3" # self_created

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
    EXTRA_HITCOUNT = "extraHitCount" # self_created
    SKILLTAGS = "skillTags" # self_created
    NPCARDTYPE = "npCards" # self_created
    NPTARGETEFFECT = "targetType" # self_created
    NPTAGS = "npTags" # self_created
    
