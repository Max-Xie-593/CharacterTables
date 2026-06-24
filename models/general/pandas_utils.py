import pandas as pd
from pandas.io.json._normalize import json_normalize
import traceback, logging, calendar
from typing import Any, Sequence, Mapping
from multipledispatch import dispatch
from .constants import NONE_TEXT
from .enums import CharacterTableColumnNames

def debug_pandas_output(x: pd.DataFrame) -> None:
    """Function to fully output pandas tables. For debugging purposes.

    Args:
        x (pd.DataFrame): DataFrame Table
    """
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 2000)
    pd.set_option("display.float_format", "{:20,.2f}".format)
    pd.set_option("display.max_colwidth", None)
    print(x)
    pd.reset_option("display.max_rows")
    pd.reset_option("display.max_columns")
    pd.reset_option("display.width")
    pd.reset_option("display.float_format")
    pd.reset_option("display.max_colwidth")

def normalize_json(json_info: Any) -> pd.DataFrame:
    """attempts to normalize json information into table format

    Args:
        json_info (Any): json information

    Returns:
        pd.DataFrame: Dataframe table from Json information
    """
    try:
        return json_normalize(json_info)
    except Exception:
        logging.error(traceback.format_exc())

def remove_incomplete_data(dataFrame: pd.DataFrame, incomplete_ids: Sequence[int]) -> None:
    """removes any incomplete information from the table

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing character information
        incomplete_ids (Sequence[int]): an list of character IDs with incomplete data
    """
    dataFrame.drop(
        dataFrame[
            dataFrame[
                CharacterTableColumnNames.ID
            ].isin(
                incomplete_ids
            )
        ].index,
        inplace=True
    )
    dataFrame.reset_index(inplace=True)

def rename_dataframe_columns(dataFrame: pd.DataFrame, columns: Mapping) -> None:
    """function to rename columns in the Dataframe Object.

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing character information
    """
    dataFrame.rename(columns=columns, inplace=True)

@dispatch(pd.Series, pd.Series)
def create_birthday(month: pd.Series, day: pd.Series) -> pd.Series:
    """helper function to extract the birthday of characters

    Args:
        month (pd.Series): birth month of characters
        day (pd.Series): birth day of characters 

    Returns:
        pd.Series: birthday column of characters
    """
    return (
        month.apply(
            lambda x: calendar.month_abbr[x] 
            if x > 0 
            else NONE_TEXT
        ) + 
        " " + 
        day.astype(str)
    )

@dispatch(pd.Series, pd.Series, pd.Series)
def create_birthday(month: pd.Series, day: pd.Series, year: pd.Series) -> pd.Series:
    """helper function to extract the birthday of characters

    Args:
        month (pd.Series): birth month of characters
        day (pd.Series): birth day of characters
        year (pd.Series): birth year of characters 

    Returns:
        pd.Series: birthday column of characters
    """
    return create_birthday(month,day) + " " + year.astype(str)


def extract_birthday(dataFrame: pd.DataFrame, columns: Sequence[str]) -> None:
    """function to extract the birthdays of characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing character information
        columns (Sequence[str]): Column names containing birthday relevant column names
    """

    dataFrame[CharacterTableColumnNames.BIRTHDAY] = create_birthday(
        *map(
            dataFrame.get, 
            columns
        )
    )
