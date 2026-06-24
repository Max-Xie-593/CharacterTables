from enum import StrEnum, auto

class GameInitials(StrEnum): 
    """Enum of various games

    Args:
        StrEnum (class): class to enforce string enums
    """
    GI = auto()
    ZZZ = auto()
    FGO = auto()
    UMAMUSU = auto()

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
    BIRTHDAY = auto()
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
    ASSISTDESCRIPTION = "skills.assist.descriptions" # hakushin_pandas_normalized
    ATTACK_STAT = "stats.attack" # hakushin_pandas_normalized
    ATTACKGROWTH_STAT = "stats.attack_growth" # hakushin_pandas_normalized
    HP_STAT = "stats.hp_max" # hakushin_pandas_normalized
    HPGROWTH_STAT = "stats.hp_growth" # hakushin_pandas_normalized
    DEFENSE_STAT = "stats.defence" # hakushin_pandas_normalized
    DEFENSEGROWTH_STAT = "stats.defence_growth" # hakushin_pandas_normalized

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
    EXTRA_HITCOUNT = "addattackHitCount" # self_created
    SKILLTAGS = "skillTags" # self_created
    NPCARDTYPE = "npCards" # self_created
    NPTARGETEFFECT = "targetType" # self_created
    NPTAGS = "npTags" # self_created

class UmaMusuColumnNames(StrEnum):
    """Enum of Column names applicable to Uma Musume Pretty Derby (UmaMusu)

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    UMAMUSU_ID = "item_data.id" # umamusume_api_pandas_normalized
    UMAMUSU_NAME = "item_data.name_en" # umamusume_api_pandas_normalized
    TITLE = "item_data.title" # umamusume_api_pandas_normalized
    UMAMUSU_ALT = "item_data.version" # umamusume_api_pandas_normalized
    UMAMUSU_RARITY = "item_data.rarity" # umamusume_api_pandas_normalized
    UMAMUSU_HEIGHT = "char_data.height" # umamusume_api_pandas_normalized
    UMAMUSU_BUST = "char_data.three_sizes.b" # umamusume_api_pandas_normalized
    UMAMUSU_WAIST = "char_data.three_sizes.w" # umamusume_api_pandas_normalized
    UMAMUSU_HIPS = "char_data.three_sizes.h" # umamusume_api_pandas_normalized

    UMAMUSU_BIRTH_MONTH = "char_data.birth_month" # umamusume_api_pandas_normalized
    UMAMUSU_BIRTH_DAY = "char_data.birth_day" # umamusume_api_pandas_normalized
    UMAMUSU_BIRTH_YEAR = "char_data.birth_year" # umamusume_api_pandas_normalized 

    UMAMUSU_GENDER = "char_data.sex" # umamusume_api_pandas_normalized
    UMAMUSU_JP_VA = "char_data.va_en" # umamusume_api_pandas_normalized

    UMAMUSU_STAT_BONUSES = "item_data.stat_bonus" # umamusume_api_pandas_normalized
    SPD_STAT_BONUS = "speed_bonus" # self_created
    STA_STAT_BONUS = "stamina_bonus" # self_created
    POW_STAT_BONUS = "power_bonus" # self_created
    GUT_STAT_BONUS = "guts_bonus" # self_created
    WIT_STAT_BONUS = "wit_bonus" # self_created

    UMAMUSU_BASE_STATS = "item_data.base_stats" # umamusume_api_pandas_normalized
    SPD_BASE_STAT = "base_speed" # self_created
    STA_BASE_STAT = "base_stamina" # self_created
    POW_BASE_STAT = "base_power" # self_created
    GUT_BASE_STAT = "base_guts" # self_created
    WIT_BASE_STAT = "base_wit" # self_created

    UMAMUSU_FIVE_STAR_STATS = "item_data.five_star_stats" # umamusume_api_pandas_normalized
    SPD_MAX_BASE_STAT = "max_base_speed" # self_created
    STA_MAX_BASE_STAT = "max_base_stamina" # self_created
    POW_MAX_BASE_STAT = "max_base_power" # self_created
    GUT_MAX_BASE_STAT = "max_base_guts" # self_created
    WIT_MAX_BASE_STAT = "max_base_wit" # self_created

    UMAMUSU_APTITUDE = "item_data.aptitude" # umamusume_api_pandas_normalized
    TURF_APTITUDE = auto() # self_created
    DIRT_APTITUDE = auto() # self_created
    SPRINT_APTITUDE = auto() # self_created
    MILE_APTITUDE = auto() # self_created
    MEDIUM_APTITUDE = auto() # self_created
    LONG_APTITUDE = auto() # self_created
    FRONT_APTITUDE = auto() # self_created
    PACE_APTITUDE = auto() # self_created
    LATE_APTITUDE = auto() # self_created
    END_APTITUDE = auto() # self_created


    
