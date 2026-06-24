import pandas as pd
import re
import itertools
from typing import Any, Sequence, Mapping, Set, Optional, Callable

from fgo_api_types.enums import FuncApplyTarget
from fgo_api_types.gameenums import NiceFuncTargetType, CardType, NiceCardType

from models.general.pandas_utils import remove_incomplete_data
from models.general.enums import CharacterTableColumnNames
from models.general.constants import NONE_TEXT

from .enums import FGOColumnNames, FGOGrowthCurve
from .constants import (
    FGO_INCOMPLETE_CHARACTER_IDS,
    FGO_REGEX_CARD_HITS_DISTRIBUTION,
    FGO_ENEMY_TARGET_TYPE,
    SELF_TEXT,
    SUPPORT_TEXT,
    FGO_NP_COLUMNS,
    FGO_COLUMNS,
)

def extract_servant_traits(dataFrame: pd.DataFrame) -> None:
    """function to extract servant traits of FGO characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO character information
    """
    dataFrame[FGOColumnNames.SERVANTTRAITS] = dataFrame[FGOColumnNames.SERVANTTRAITS].apply(
        lambda x: ", ".join(
            trait[CharacterTableColumnNames.NAME] 
            for trait in x
        )
    )

def extract_servant_card_deck_details(dataFrame: pd.DataFrame) -> None:
    """function to extract card deck details of FGO characters 

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO character information
    """
    dataFrame[FGOColumnNames.CARDDECK] = dataFrame[FGOColumnNames.CARDS].apply(
        lambda x: "".join(
            CardType(int(card)).name[0]
            for card in x
        )
    )
    subset_data = dataFrame.filter(regex=FGO_REGEX_CARD_HITS_DISTRIBUTION)
    for columnName in subset_data.columns:
        dataFrame[
            f"{NiceCardType(columnName.split('.')[1]).name}HitCount"
        ] = subset_data[columnName].apply(lambda x: len(x))

def extract_servant_growth_curve(dataFrame: pd.DataFrame) -> None:
    """function to extract the growth curve of FGO characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO character information
    """
    def determine_growth_curve(growthCurve: int) -> FGOGrowthCurve:
        """helper function to determine the FGO character's growth curve

        Args:
            growthCurve (int): number indicating the character's growth curve

        Returns:
            FGOGrowthCurve: Growth Curve of FGO character
        """
        match growthCurve:
            case growthCurve if 0 < growthCurve <= 5:
                return FGOGrowthCurve.LINEAR
            case growthCurve if 5 < growthCurve <= 10:
                return FGOGrowthCurve.REVERSE_S
            case growthCurve if 10 < growthCurve <= 15:
                return FGOGrowthCurve.S
            case growthCurve if 20 < growthCurve <= 25:
                return FGOGrowthCurve.SEMI_REVERSE_S
            case growthCurve if 25 < growthCurve <= 30:
                return FGOGrowthCurve.SEMI_S
            case _:
                return FGOGrowthCurve.UNKNOWN
    
    dataFrame[FGOColumnNames.GROWTHCURVE] = dataFrame[
        FGOColumnNames.GROWTHCURVE
    ].apply(
        lambda x: determine_growth_curve(x)
    )

def clean_up_servant_buff(buffText: str) -> str:
    """function to clean up text of special characters

    Args:
        buffText (str): text of the buff

    Returns:
        str: cleaned up buff text
    """
    return re.sub(r'\n'," ",buffText)

def determine_servant_buff_exists(buffText: str) -> bool:
    """function to check the text is not "None"

    Args:
        buffText (str): text of the buff

    Returns:
        bool: text is not "None"
    """
    return clean_up_servant_buff(buffText) != NONE_TEXT

def determine_player_skill_buffs(**kwargs) -> bool:
    """function to determine if the buff is the player

    Returns:
        bool: is the buff a player buff
    """
    def determine_applyTarget_player(targetTeam: str) -> bool:
        """helper function to check if the buff involves the player

        Args:
            targetTeam (str): Target team of buff

        Returns:
            bool: buff of target involves the player
        """
        return targetTeam in set(
            [
                FuncApplyTarget.player,
                FuncApplyTarget.playerAndEnemy
            ]
        )

    return determine_applyTarget_player(
        kwargs[FGOColumnNames.FUNCTARGETTEAM]
    ) and clean_up_servant_buff(
        kwargs[FGOColumnNames.FUNCPOPUPTEXT]
    )

def determine_player_np_buffs(**kwargs) -> bool:
    """function to determine if the np buff involves the player

    Returns:
        bool: is the np buff a player buff
    """
    def determine_enemy_servant(targetType: str, targetTeam: str) -> bool:
        """helper function to check if the np buff involves the player

        Args:
            targetType (str): Target type of buff
            targetTeam (str): Target team of buff

        Returns:
            bool: np buff of target involves the player
        """
        return (
            (
                targetType in FGO_ENEMY_TARGET_TYPE or 
                targetTeam == FuncApplyTarget.enemy
            ) and not (
                targetType in FGO_ENEMY_TARGET_TYPE and 
                targetTeam == FuncApplyTarget.enemy
            )
        )
    
    def determine_NP_applyTarget_player(targetTeam: str) -> bool:
        """helper function to check if the np buff involves the player

        Args:
            targetTeam (str): Target team of buff

        Returns:
            bool: np buff of target involves the player
        """
        return targetTeam == FuncApplyTarget.playerAndEnemy

    return (
        (
            not determine_enemy_servant(
                kwargs[FGOColumnNames.FUNCTARGETTYPE],
                kwargs[FGOColumnNames.FUNCTARGETTEAM]
            ) or determine_NP_applyTarget_player(kwargs[FGOColumnNames.FUNCTARGETTEAM])
        ) and 
        clean_up_servant_buff(kwargs[FGOColumnNames.FUNCPOPUPTEXT]) and 
        determine_servant_buff_exists(kwargs[FGOColumnNames.FUNCPOPUPTEXT])
    )

def aggregate_functions(data: Sequence[Mapping], bool_function: Callable[...,bool]) -> Set[Optional[Sequence[str]]]:
    """function to combine all buff functions of a skill or NP into one list 

    Args:
        data (Sequence[Mapping]): Sequence of functions
        bool_function (Callable[...,bool]): boolean function to check

    Returns:
        Set[Optional[Sequence[str]]]: all buff function of a skill or NP into one list
    """
    def determine_targetType_self_or_support(targetType: str) -> str:
        """helper function to determine if the buff applys to self or others

        Args:
            targetType (str): Target type of buff

        Returns:
            str: "Self" if target type is self else "Support"
        """
        return (
            SELF_TEXT 
            if targetType == NiceFuncTargetType.self_ 
            else SUPPORT_TEXT
        )

    return (
        set() 
        if not data 
        else set(
            filter(
                None,
                [
                    " ".join(
                        [
                            determine_targetType_self_or_support(
                                buffInfo[FGOColumnNames.FUNCTARGETTYPE]
                            ),
                            clean_up_servant_buff(
                                buffInfo[FGOColumnNames.FUNCPOPUPTEXT]
                            ) 
                        ]
                    ) if bool_function(
                        funcTargetType=buffInfo[FGOColumnNames.FUNCTARGETTYPE],
                        funcTargetTeam=buffInfo[FGOColumnNames.FUNCTARGETTEAM],
                        funcPopupText=buffInfo[FGOColumnNames.FUNCPOPUPTEXT]
                    ) else "" 
                    for buffInfo in data
                ] 
            ) 
        )
    )

def join_all_items(seriesData: pd.Series) -> pd.Series:
    """function to join all list of buffs to one list

    Args:
        seriesData (pd.Series): Row data containing list of buffs

    Returns:
        pd.Series: set of buffs
    """
    return ", ".join(
        set(
            itertools.chain(
                (
                    data 
                    for data in seriesData 
                    if data
                )
            )
        )
    )

def join_all_set_items(seriesData: pd.Series) -> pd.Series:
    """function to join all sets of buffs to one list

    Args:
        seriesData (pd.Series): Row data containing list of buffs

    Returns:
        pd.Series: set of buffs
    """
    return ", ".join(
        set(
            itertools.chain(
                *(
                    data 
                    for data in seriesData 
                    if data
                )
            )
        )
    )

def extract_servant_skill_tags(dataFrame: pd.DataFrame) -> None:
    """function to extract all skill tags of a FGO character

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO character information
    """
    def aggregate_skill_functions(rowdata: pd.Series) -> pd.Series:
        """helper function to extract skill tags of a FGO characters

        Args:
            rowdata (pd.Series): Series Object containing FGO character skills

        Returns:
            pd.Series: data containing all skill tags of a FGO character
        """
        return rowdata.apply(
            lambda x: aggregate_functions(
                x,
                determine_player_skill_buffs
            )
        )

    dataFrame[FGOColumnNames.SKILLTAGS] = pd.DataFrame(
        dataFrame[FGOColumnNames.SKILLS].apply(
            lambda x: [
                y[FGOColumnNames.FUNCTIONS]
                for y in x
            ]
        ).to_list()
    ).apply(
        lambda x: aggregate_skill_functions(x),
        axis=1
    ).agg(
        lambda x: join_all_set_items(x),
        axis=1
    )


def extract_noble_phantasms_details(dataFrame: pd.DataFrame) -> None:
    """function to extract all NP tags of a FGO character

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO character information
    """
    def extract_noble_phantasm_functions(rowdata: pd.Series) -> pd.Series:
        """helper function to extract NP tags of a FGO characters

        Args:
            rowdata (pd.Series): Series Object containing FGO character skills

        Returns:
            pd.Series: data containing all NP tags of a FGO character
        """
        return rowdata.apply(
            lambda x: aggregate_functions(
                x,
                determine_player_np_buffs
            )
        )

    subset_data = pd.DataFrame(
        dataFrame[
            FGOColumnNames.NOBLEPHANTASMS
        ].to_list()
    )

    for new_col_name, lambdaFunc in FGO_NP_COLUMNS.items():
        dataFrame[
            new_col_name
        ] = subset_data.apply(
            lambdaFunc
        ).agg(
            lambda x: join_all_items(x),
            axis=1
        )
    
    # Map NP Card Number to Card type Name 
    dataFrame[FGOColumnNames.NPCARDTYPE] = dataFrame[
        FGOColumnNames.NPCARDTYPE
        ].apply(
            lambda x: ", ".join(
                CardType(int(card)).name 
                for card in x.split(",")
            ) 
    )

    dataFrame[FGOColumnNames.NPTAGS] = subset_data.apply(
        lambda x: x.str[FGOColumnNames.FUNCTIONS]
    ).apply(
        lambda x: extract_noble_phantasm_functions(x)
    ).agg(
        lambda x: join_all_set_items(x),axis=1
    )

def process_fgo_data(dataFrame: pd.DataFrame) -> pd.DataFrame:
    """helper function that contains FGO relevant functions to create the table

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing FGO game data

    Returns:
        pd.DataFrame: cleaned up DataFrame Object containing FGO game data
    """
    remove_incomplete_data(dataFrame, FGO_INCOMPLETE_CHARACTER_IDS)
    extract_servant_traits(dataFrame)
    extract_servant_card_deck_details(dataFrame)
    extract_servant_growth_curve(dataFrame)
    extract_servant_skill_tags(dataFrame)
    extract_noble_phantasms_details(dataFrame)
    return pd.DataFrame(dataFrame[FGO_COLUMNS])
