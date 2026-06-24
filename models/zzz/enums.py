from enum import StrEnum, auto

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
