import pandas as pd
import re
from typing import Any, Optional
from models.general.pandas_utils import normalize_json, remove_incomplete_data
from models.general.enums import CharacterTableColumnNames
from hakushin.enums import ZZZSpecialty

from .enums import ZZZColumnNames
from .constants import (
    CHARACTER_TEXT,
    ZZZ_INCOMPLETE_CHARACTER_IDS,
    ZZZ_TEAM_PREFIXES,
    ZZZ_ASSIST_TYPES,
    ZZZ_REGEX_SIMPLE_TEAM_CONDITION,
    ZZZ_REGEX_TEAM_CONDITION_TYPES,
    ZZZ_STATS_COLUMNS,
    ZZZ_COLUMNS,
)

def extract_team_condition(dataFrame: pd.DataFrame) -> None:
    """extracts team conditions for agents in ZZZ

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing ZZZ character information
    """
    def interpret_team_condition(condition: str) -> str:
        """helper function to parse the team condition text

        Args:
            condition (str): text containing the team conditions for ZZZ characters

        Returns:
            str: formatted text of the character's team condition
        """
        def format_team_condition(condition_text: str) -> str:
            """helper function to format the team condition text

            Args:
                condition_text (str): formatted team condition text

            Returns:
                str: formatted text of the character's team condition
            """
            character_types = set(ZZZSpecialty.__members__)
            condition_list = condition_text.split()
            if condition_list[-1].upper() in character_types:
                condition_list.append(CHARACTER_TEXT)
            return " ".join(
                x.capitalize() 
                for x in condition_list
            )

        if not condition:
            return ""
        for prefix in ZZZ_TEAM_PREFIXES:
            if condition.startswith(prefix):
                return format_team_condition(
                    condition.removeprefix(prefix)
                )
        return format_team_condition(condition)

    subset_data = dataFrame.filter(regex=ZZZ_REGEX_SIMPLE_TEAM_CONDITION)

    subset_data = (
        subset_data.iloc[:,-1]
        .str[1]
        .apply(
            lambda x: x.split(":")[0]
        )
    )
    subset_data = pd.DataFrame(
        subset_data.apply(
            lambda conditions: re.findall(
                ZZZ_REGEX_TEAM_CONDITION_TYPES,
                conditions
            )
        ).to_list()
    ).fillna("")
    for idx, col in enumerate(subset_data):
        dataFrame[
            f"team_condition_{idx+1}"
        ] = subset_data[col].apply(
            lambda y: interpret_team_condition(y)
        )

def extract_assist(dataFrame: pd.DataFrame) -> None:
    """function to extract the assist type 

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing ZZZ character information
    """
    dataFrame[ZZZColumnNames.ASSISTTYPE] = dataFrame[ZZZColumnNames.ASSISTDESCRIPTION].apply(
        lambda x: list(
            filter(
                None,
                [
                    y 
                    if y[CharacterTableColumnNames.NAME].startswith(ZZZ_ASSIST_TYPES) 
                    else None 
                    for y in x
                ]
            )
        )
    ).str[0].map(
        lambda x: x[CharacterTableColumnNames.NAME].split(":")[0]
    )

def extract_ascension_stats(dataFrame: pd.DataFrame) -> None:
    """function to extract the ascension stats for ZZZ characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing ZZZ character information
    """
    subset_data = normalize_json(dataFrame[ZZZColumnNames.EXTRAASCENSION].str[5])

    dataFrame[ZZZColumnNames.ASCENSIONSTAT1], dataFrame[ZZZColumnNames.ASCENSIONSTAT2] = (
        subset_data[ZZZColumnNames.PROPS]
        .str[n]
        .apply(
            lambda x: x[CharacterTableColumnNames.NAME]
        ) 
        for n in range(2)
    )

def extract_max_hp_atk_def(dataFrame: pd.DataFrame) -> None:
    """function to calculate the max stats of ZZZ characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing ZZZ character information
    """
    def calculate_max_stat(
        base_stat: pd.Series,
        growth_stat: pd.Series,
        ascension_stat: pd.Series,
        ascension_key: str,
    ) -> pd.Series:
        """helper function to calculate the max stats of ZZZ characters

        Args:
            base_stat (pd.Series): stats of ZZZ characters at level 1
            growth_stat (pd.Series): stat gains of ZZZ characters upon leveling up
            ascension_stat (pd.Series): stat gains of ZZZ characters upon ascending
            ascension_key (str): stat type of ZZZ characters ascension stat

        Returns:
            pd.Series: column data of ZZZ character stats at max level (60)
        """
        return (
            base_stat
            + (59 * (growth_stat / pow(10, 4)))
            + ascension_stat.str[5].apply(lambda x: x[ascension_key])
        )

    for new_col_name, (stat_string, *column_names) in ZZZ_STATS_COLUMNS.items():
        dataFrame[new_col_name] = calculate_max_stat(
            *map(
                dataFrame.get,
                column_names
            ),
            stat_string
        ).round(4)

def process_zzz_data(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """helper function that contains ZZZ relevant functions to create the table

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing ZZZ game data

    Returns:
        pd.DataFrame: cleaned up DataFrame Object containing ZZZ game data
    """
    remove_incomplete_data(dataFrame, ZZZ_INCOMPLETE_CHARACTER_IDS)
    extract_max_hp_atk_def(dataFrame)
    extract_ascension_stats(dataFrame)
    extract_assist(dataFrame)
    extract_team_condition(dataFrame)
    return pd.DataFrame(dataFrame[ZZZ_COLUMNS])
