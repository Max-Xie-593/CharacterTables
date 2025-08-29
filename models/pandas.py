import pandas as pd
from pandas.io.json._normalize import json_normalize

import traceback, logging, os, re, calendar, itertools

from deep_translator import GoogleTranslator

from typing import Any, Optional
from collections import defaultdict
from collections.abc import Callable, Sequence, Mapping, Set
from datetime import datetime

from ambr.enums import SpecialStat
from fgo_api_types.enums import FuncApplyTarget
from fgo_api_types.gameenums import NiceFuncTargetType
from .enums import (
    GameInitials, 
    FGOGrowthCurve, 
    CharacterTableColumnNames, 
    GIColumnNames, 
    ZZZColumnNames, 
    FGOColumnNames
)
from .constants import (
    GI_COLUMNS, 
    ZZZ_COLUMNS, 
    FGO_COLUMNS, 
    ZZZ_TEAM_PREFIXES, 
    ZZZ_INCOMPLETE_CHARACTER_IDS, 
    FGO_INCOMPLETE_CHARACTER_IDS, 
    FGO_ENEMY_TARGET_TYPE, 
    CHARACTER_TEXT, 
    NONE_TEXT, 
    SELF_TEXT, 
    SUPPORT_TEXT,
    FGO_REGEX_CARD_HITS_DISTRIBUTION,
    ZZZ_REGEX_TEAM_CONDITION,
    ZZZ_REGEX_SIMPLE_TEAM_CONDITION,
    ZZZ_REGEX_OR,
    GI_STATS_COLUMNS,
    ZZZ_STATS_COLUMNS,
    FGO_NP_COLUMNS,
    GI_SPECIAL_ENUMS_COLUMNS,
    ZZZ_REGEX_TEAM_CONDITION_TYPES
)
from hakushin.enums import ZZZSpecialty
from multipledispatch import dispatch

# PANDAS GENERAL FUNCTIONS
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

def remove_incomplete_data(dataFrame: pd.DataFrame, game: GameInitials) -> None:
    """removes any incomplete information from the table

    Args:
        dataFrame (pd.DataFrame): Dataframe Object containing character information
    """
    def retrieve_incomplete_ids(game: GameInitials) -> Sequence[int]:
        """function to remove character information with incomplete data

        Args:
            game (GameInitials): game the character data is from

        Returns:
            Sequence[int]: an list of character IDs with incomplete data
        """
        match game:
            case GameInitials.ZZZ:
                return ZZZ_INCOMPLETE_CHARACTER_IDS
            case GameInitials.FGO:
                return FGO_INCOMPLETE_CHARACTER_IDS
            case _: # Highly unlikely default case
                return []
            
    dataFrame.drop(
        dataFrame[
            dataFrame[
                CharacterTableColumnNames.ID
            ].isin(
                retrieve_incomplete_ids(game)
            )
        ].index,
        inplace=True
    )
    dataFrame.reset_index(inplace=True)

# PANDAS ZZZ FUNCTIONS
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

    def find_common_prefix(path_lists: Sequence[str]) -> str:
        """helper function to find common prefix from the team condition text

        Args:
            path_lists (Sequence[str]): Sequence of team condition text from ZZZ characters

        Returns:
            str: common prefix from the team condition text
        """
        return os.path.commonprefix(path_lists)

    subset_data = dataFrame.filter(regex=ZZZ_REGEX_SIMPLE_TEAM_CONDITION)
    # subset_data = dataFrame.filter(regex=ZZZ_REGEX_TEAM_CONDITION)

    # subset_data = subset_data.ffill(axis=1)
    subset_data = (
        subset_data.iloc[:,-1]
        .str[1]
        .apply(
            lambda x: x.split(":")[0]
        )
    )
    # NEW WAY TO PARSE CONDITION TEXT
    subset_data = pd.DataFrame(
        subset_data.apply(
            lambda conditions: re.findall(
                ZZZ_REGEX_TEAM_CONDITION_TYPES,
                conditions
            )
        ).to_list()
    )
    # OLD WAY TO PARSE CONDITION TEXT
    # subset_data = pd.DataFrame(
    #     subset_data.apply(
    #         lambda x: re.split(
    #             ZZZ_REGEX_OR,
    #             x.removeprefix(
    #                 find_common_prefix(
    #                     subset_data.to_list()
    #                 )
    #             )
    #         )
    #     ).to_list()
    # )
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
    subset_data = normalize_json(dataFrame[ZZZColumnNames.ASSISTDESCRIPTION])
    subset_data = subset_data.ffill(axis=1)
    subset_data = subset_data.map(
        lambda x: x[CharacterTableColumnNames.NAME].split(":")[0]
    ).apply(
        lambda x: sorted(list(set(x))), axis=1
    )
    dataFrame[ZZZColumnNames.ASSISTTYPE] = subset_data.apply(lambda x: x[1])

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

@dispatch(pd.DataFrame)
def extract_max_hp_atk_def(dataFrame: pd.DataFrame) -> None:
    """helper function to calculate the max stats of ZZZ characters

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

# PANDAS GI FUNCTIONS
def extract_birthday(dataFrame: pd.DataFrame) -> None:
    """function to extract the birthdays of Genshin Impact characters

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
        
    def create_birthday(month: pd.Series, day: pd.Series) -> pd.Series:
        """helper function to extract the birthday of GI characters

        Args:
            month (pd.Series): birth month of GI characters
            day (pd.Series): birth day of GI characters 

        Returns:
            pd.Series: birthday column of GI characters
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

    dataFrame[GIColumnNames.BIRTHDAY] = create_birthday(
        *map(
            dataFrame.get, 
            [
                GIColumnNames.BIRTHDATE_MONTH,
                GIColumnNames.BIRTHDATE_DAY
            ]
        )
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
    Translations may not be accurate. 

    Args:
        dataFrame (pd.DataFrame): DataFrame Object containing GI character information
    """
    translator = GoogleTranslator(source="ja")
    dataFrame[GIColumnNames.JP_VA] = json_normalize(
        dataFrame[GIColumnNames.CHARACTER_VOICE]
    ).apply(
        lambda x: x.str[GIColumnNames.VOICE_ACTOR]
    )[2].map(
        lambda x: translator.translate(x)
    )

@dispatch(pd.DataFrame,Mapping)
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
        return json_normalize(
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
    dataFrame[GIColumnNames.ULTIMATECOST] = normalize_json(
        dataFrame[GIColumnNames.TALENTS]
    ).apply(
        lambda x: x.str["cost"]
    ).infer_objects().ffill(axis=1).iloc[:,-1]

# PANDAS FGO FUNCTIONS
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
            card[0].upper() 
            for card in x
        )
    )
    subset_data = dataFrame.filter(regex=FGO_REGEX_CARD_HITS_DISTRIBUTION)
    for columnName in subset_data.columns:
        dataFrame[
            f"{columnName.split(".")[1]}HitCount"
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

    dataFrame[FGOColumnNames.SKILLTAGS] = normalize_json(
        dataFrame[FGOColumnNames.SKILLS]
    ).apply(
        lambda x: x.str[FGOColumnNames.FUNCTIONS]
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

    subset_data = normalize_json(dataFrame[FGOColumnNames.NOBLEPHANTASMS])

    for new_col_name, lambdaFunc in FGO_NP_COLUMNS.items():
        dataFrame[
            new_col_name
        ] = subset_data.apply(
            lambdaFunc
        ).agg(
            lambda x: join_all_items(x),
            axis=1
        )

    dataFrame[FGOColumnNames.NPTAGS] = subset_data.apply(
        lambda x: x.str[FGOColumnNames.FUNCTIONS]
    ).apply(
        lambda x: extract_noble_phantasm_functions(x)
    ).agg(
        lambda x: join_all_set_items(x),axis=1
    )

# PANDAS BUILDER
def clean_up_character_info(character_data: Any, curve_data: Optional[Any], game: GameInitials) -> pd.DataFrame:
    """function to convert character information into a DataFrame Object. Attempt at a Builder Design Pattern.

    Args:
        character_data (Any): information of game characters from a game
        curve_data (Optional[Any]): growth curve data of GI characters
        game (GameInitials): game the character data is from

    Returns:
        pd.DataFrame: DataFrame Object containing character game data
    """

    def clean_up_zzz_character_info(dataFrame: pd.DataFrame) -> pd.DataFrame:
        """helper function that contains ZZZ relevant functions to create the table

        Args:
            dataFrame (pd.DataFrame): DataFrame Object containing ZZZ game data

        Returns:
            pd.DataFrame: cleaned up DataFrame Object containing ZZZ game data
        """
        remove_incomplete_data(dataFrame, GameInitials.ZZZ)
        extract_max_hp_atk_def(dataFrame)
        extract_ascension_stats(dataFrame)
        extract_assist(dataFrame)
        extract_team_condition(dataFrame)
        return pd.DataFrame(dataFrame[ZZZ_COLUMNS])
    
    def clean_up_gi_character_info(dataFrame: pd.DataFrame, curve_data: Optional[Any]) -> pd.DataFrame:
        """helper function that contains GI relevant functions to create the table

        Args:
            dataFrame (pd.DataFrame): DataFrame Object containing ZZZ game data
            curve_data (Optional[Any]): GI character growth curve data

        Returns:
            pd.DataFrame: cleaned up DataFrame Object containing GI game data
        """
        extract_birthday(dataFrame)
        convert_special_enums(dataFrame)
        convert_release_time(dataFrame)
        convert_jp_va(dataFrame)
        extract_max_hp_atk_def(dataFrame, curve_data)
        extract_energy_costs(dataFrame)
        return pd.DataFrame(dataFrame[GI_COLUMNS])
    
        
    def clean_up_fgo_character_info(dataFrame: pd.DataFrame) -> pd.DataFrame:
        """helper function that contains FGO relevant functions to create the table

        Args:
            dataFrame (pd.DataFrame): DataFrame Object containing FGO game data

        Returns:
            pd.DataFrame: cleaned up DataFrame Object containing FGO game data
        """
        remove_incomplete_data(dataFrame, GameInitials.FGO)
        extract_servant_traits(dataFrame)
        extract_servant_card_deck_details(dataFrame)
        extract_servant_growth_curve(dataFrame)
        extract_servant_skill_tags(dataFrame)
        extract_noble_phantasms_details(dataFrame)
        return pd.DataFrame(dataFrame[FGO_COLUMNS])

    pdData = normalize_json(character_data)

    match game:
        case GameInitials.GI:
            return clean_up_gi_character_info(pdData,curve_data)
        case GameInitials.ZZZ:
            return clean_up_zzz_character_info(pdData)
        case GameInitials.FGO:
            return clean_up_fgo_character_info(pdData)
        case _: # Highly unlikely default case
            return None
     