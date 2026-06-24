from typing import Final
from collections.abc import Sequence, Mapping
from models.general.enums import CharacterTableColumnNames
from .enums import UmaMusuColumnNames

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
