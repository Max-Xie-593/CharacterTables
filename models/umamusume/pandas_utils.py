import pandas as pd
from typing import Any

from models.general.enums import CharacterTableColumnNames
from models.general.pandas_utils import extract_birthday, rename_dataframe_columns

from .enums import UmaMusuColumnNames
from .constants import (
    UMA_COLUMN_RENAMING,
    UMAMUSUME_BIRTHDAY_COLUMNS,
    UMA_STATS_COLUMNS,
    UMAMUSUME_COLUMNS,
)

def extract_umamusume_gender(dataFrame: pd.DataFrame) -> None:
    """function to determine the gender of the real life Uma Musume

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing Umamusume character information
    """
    dataFrame[CharacterTableColumnNames.GENDER] = dataFrame[
        UmaMusuColumnNames.UMAMUSU_GENDER
        ].apply(
            lambda x: "M" 
            if x == 1 
            else "F"
        )

def extract_umamusume_stats(dataFrame: pd.DataFrame) -> None:
    """function to unpack Umamusume's stats

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing Umamusume character information
    """
    for original_col, unpacked_cols in UMA_STATS_COLUMNS.items():
        dataFrame[unpacked_cols] = dataFrame[original_col].to_list()

def process_umamusume_data(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """helper function that contains UmaMusume relevant functions to create the table

    Args:
        data (pd.DataFrame): DataFrame Object containing UmaMusume game data

    Returns:
        pd.DataFrame: cleaned up DataFrame Object containing UmaMusume game data
    """
    rename_dataframe_columns(dataFrame, UMA_COLUMN_RENAMING)
    extract_birthday(dataFrame, UMAMUSUME_BIRTHDAY_COLUMNS)
    extract_umamusume_stats(dataFrame)
    extract_umamusume_gender(dataFrame)
    return pd.DataFrame(dataFrame[UMAMUSUME_COLUMNS])
