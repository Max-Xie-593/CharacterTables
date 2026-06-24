from enum import StrEnum, auto

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
