from enum import StrEnum, auto

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
