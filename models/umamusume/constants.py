from typing import Final
from collections.abc import Sequence, Mapping
from models.general.enums import CharacterTableColumnNames
from .enums import UmaMusuColumnNames

# ---------------------------------------------------------------------------
# In-flight field pruning: only the fields consumed by umamusume/pandas_utils.py
# are retained when model_dump_json(include=...) is called in extract_character.
#
# Virtually all UmaMusuColumnNames values are dot-paths (e.g. "item_data.id"),
# so the top-level keys "item_data" / "char_data" and their sub-keys must be
# plain string literals with cross-reference comments.
# ---------------------------------------------------------------------------
UMA_CHARACTER_INCLUDE_FIELDS: Final[Mapping] = {
    # item_data — keep only the sub-fields pandas_utils reads
    "item_data": {
        "id",               # UmaMusuColumnNames.UMAMUSU_ID           = "item_data.id"
        "name_en",          # UmaMusuColumnNames.UMAMUSU_NAME         = "item_data.name_en"
        "title",            # UmaMusuColumnNames.TITLE                = "item_data.title"
        "version",          # UmaMusuColumnNames.UMAMUSU_ALT          = "item_data.version"
        "rarity",           # UmaMusuColumnNames.UMAMUSU_RARITY       = "item_data.rarity"
        "stat_bonus",       # UmaMusuColumnNames.UMAMUSU_STAT_BONUSES = "item_data.stat_bonus"
        "base_stats",       # UmaMusuColumnNames.UMAMUSU_BASE_STATS   = "item_data.base_stats"
        "five_star_stats",  # UmaMusuColumnNames.UMAMUSU_FIVE_STAR_STATS = "item_data.five_star_stats"
        "aptitude",         # UmaMusuColumnNames.UMAMUSU_APTITUDE     = "item_data.aptitude"
    },

    # char_data — keep only the sub-fields pandas_utils reads
    "char_data": {
        "height",           # UmaMusuColumnNames.UMAMUSU_HEIGHT       = "char_data.height"
        "three_sizes",      # bust/waist/hips via "char_data.three_sizes.b/w/h"
        "birth_month",      # UmaMusuColumnNames.UMAMUSU_BIRTH_MONTH  = "char_data.birth_month"
        "birth_day",        # UmaMusuColumnNames.UMAMUSU_BIRTH_DAY    = "char_data.birth_day"
        "birth_year",       # UmaMusuColumnNames.UMAMUSU_BIRTH_YEAR   = "char_data.birth_year"
        "sex",              # UmaMusuColumnNames.UMAMUSU_GENDER        = "char_data.sex"
        "va_en",            # UmaMusuColumnNames.UMAMUSU_JP_VA        = "char_data.va_en"
    },

    # All other top-level keys (profile_data, event_data, evo_loc_data,
    # objective_data, profile_art_meta, n_ssg, is_char_card) are excluded.
}

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
