import pandas as pd
import time
from datetime import datetime
from collections import defaultdict
from collections.abc import Mapping
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TranslationNotFound, RequestError
from tqdm import tqdm
from loguru import logger

from typing import Any, Optional
from ambr.enums import SpecialStat

from models.general.enums import CharacterTableColumnNames
from models.general.pandas_utils import extract_birthday, normalize_json
from .enums import GIColumnNames
from .constants import (
    GI_SPECIAL_ENUMS_COLUMNS,
    GI_COLUMNS,
    GI_STATS_COLUMNS,
    GI_BIRTHDAY_COLUMNS,
)

def convert_special_enums(dataFrame: pd.DataFrame) -> None:
    """function to extract special stats of GI characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
    for col_name, special_enum in GI_SPECIAL_ENUMS_COLUMNS.items():
        dataFrame[col_name] = dataFrame[col_name].apply(lambda x: special_enum(x).name)

def convert_release_time(dataFrame: pd.DataFrame) -> None:
    """function to convert the release date of GI characters to a ISO-formatted date. 

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
    dataFrame[
        GIColumnNames.RELEASEDATE
    ] = dataFrame[
        GIColumnNames.RELEASEDATE
    ].apply(
        lambda x: datetime.fromisoformat(x).date()
    )

def convert_jp_va(dataFrame: pd.DataFrame) -> None:
    """function to convert the japanese voice actor of GI characters to english names using Google Translate. 
    Translations may not be accurate. Uses tqdm to show progress of translations.

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
    translator = GoogleTranslator(source="ja")

    # 1. Extract raw Japanese names first to avoid nested lambda issues
    jp_names = dataFrame[GIColumnNames.CHARACTER_VOICE].str[2].apply(
        lambda x: x[GIColumnNames.VOICE_ACTOR] if isinstance(x, dict) else None
    )
    
    translated_names = []

    logger.remove()
    logger.add(
        lambda msg: tqdm.write(msg, end=""),
        colorize=True,
        level="ERROR"
    )
    
    # 2. Process names sequentially with error handling
    for name in tqdm(jp_names, desc="Translating VA Names", unit="name"):
        if pd.isna(name) or not str(name).strip():
            translated_names.append(name)
            continue
            
        translated_text = name
        max_retries = 3
        backoff_delay = 2  # Seconds
        
        for attempt in range(max_retries):
            try:
                # Add a mandatory baseline delay between every request
                time.sleep(1.0) 
                
                translated_text = translator.translate(name)
                break  # Success, exit the retry loop
                
            except (RequestError, TranslationNotFound, Exception) as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to translate '{name}' after {max_retries} attempts. Error: {e}")
                    # Keeps the original Japanese name as a fallback instead of crashing
                    break  
                
                # Wait longer before retrying (2s, then 4s, etc.)
                time.sleep(backoff_delay)
                backoff_delay *= 2 
                
        translated_names.append(translated_text)
        
    # 3. Assign the stable results back to the DataFrame
    dataFrame[GIColumnNames.JP_VA] = translated_names

def extract_max_hp_atk_def(dataFrame: pd.DataFrame, curve_data: Mapping) -> None:
    """function to extract the max stats of GI characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
        curve_data (Mapping): growth curve data of GI characters
    """
    def calculate_upgrade_stat_values(
        base_stats: pd.Series,
        promotion_stats: pd.Series,
        curve_data: Mapping[str, Mapping[str, Mapping[str, float]]],
        level: int,
        ascended: bool,
    ) -> Mapping[str, float]:
        """helper function to calculate the max stats of GI characters. Copied from ambr-py due to incompatible typing.

        Args:
            base_stats (pd.Series): column data of GI character's stats at level 1
            promotion_stats (pd.Series): column data of GI character's stat gains on ascension
            curve_data (Mapping[str, Mapping[str, Mapping[str, float]]]): growth curve data of GI characters
            level (int): level to ascend to
            ascended (bool): is the character ascended

        Returns:
            Mapping[str, float]: dictionary of calculated character stats for GI
        """
        result: defaultdict[str, float] = defaultdict(float)

        for stat in base_stats:
            if stat[GIColumnNames.BASE_STATS_PROP_TYPE] is None:
                continue
            result[stat[GIColumnNames.BASE_STATS_PROP_TYPE]] = (
                stat[
                    GIColumnNames.BASE_STATS_INIT_VALUE
                    ] * curve_data[
                        str(level)
                    ][
                        GIColumnNames.CURVEINFO
                    ][
                        stat[GIColumnNames.BASE_STATS_GROWTH_TYPE]
                    ]
            )

        for promote in reversed(promotion_stats):
            if promote[GIColumnNames.PROMOTION_ADD_STATS] is None:
                continue
            if (
                level == promote[GIColumnNames.PROMOTION_UNLOCK_MAX_LEVEL] and 
                ascended
            ) or level > promote[GIColumnNames.PROMOTION_UNLOCK_MAX_LEVEL]:
                for stat in promote[GIColumnNames.PROMOTION_ADD_STATS]:
                    if stat[GIColumnNames.PROMOTION_STAT_VALUE] != 0:
                        result[
                            stat[CharacterTableColumnNames.ID]
                        ] += stat[GIColumnNames.PROMOTION_STAT_VALUE]
                        if stat[CharacterTableColumnNames.ID] in {
                            SpecialStat.CRITI_DMG, 
                            SpecialStat.CRIT_RATE
                        }:
                            result[stat[CharacterTableColumnNames.ID]] += 0.5
                break

        return result
    
    def extract_max_stats(dataFrame: pd.DataFrame, curve_data: Mapping) -> pd.DataFrame:
        """helper function to extract max stats of GI characters

        Args:
            dataFrame (pd.DataFrame): DataFrame Object containing GI characters information
            curve_data (Mapping): growth curve data of GI characters

        Returns:
            pd.DataFrame: characters stats converted into a DataFrame Object
        """
        return normalize_json(
            dataFrame.apply(
                lambda x: calculate_upgrade_stat_values(
                    *x, 
                    curve_data, 
                    90, 
                    True
                ),
                axis=1
            )
        ) 

    dataFrame[
        GI_STATS_COLUMNS["new_cols"]
    ] = extract_max_stats(
        dataFrame[
            GI_STATS_COLUMNS["upgrade_cols"]
        ], 
        curve_data
    )[
        GI_STATS_COLUMNS["stat_cols"]
    ].round(4)

def extract_energy_costs(dataFrame: pd.DataFrame) -> None:
    """function to extract the energy cost of GI character's ultimates

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
    dataFrame[GIColumnNames.ULTIMATECOST] = dataFrame[GIColumnNames.TALENTS].apply(
        lambda x: [
            y["cost"] 
            for y in x 
            if y["cost"] is not None
        ] 
    ).str[-1]

def process_gi_data(dataFrame: pd.DataFrame, curve_data: Optional[Any]) -> pd.DataFrame:
    """helper function that contains GI relevant functions to create the table

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing ZZZ game data
        curve_data (Optional[Any]): GI character growth curve data

    Returns:
        pd.DataFrame: cleaned up DataFrame Object containing GI game data
    """
    extract_birthday(dataFrame, GI_BIRTHDAY_COLUMNS)
    convert_special_enums(dataFrame)
    convert_release_time(dataFrame)
    convert_jp_va(dataFrame)
    extract_max_hp_atk_def(dataFrame, curve_data)
    extract_energy_costs(dataFrame)
    return pd.DataFrame(dataFrame[GI_COLUMNS])
