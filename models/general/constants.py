from typing import Final
from collections.abc import Sequence, Mapping

from .enums import (
    GameInitials,
    DataFolders,
    ArgumentParserKwargs,
)

# TEXT RELATED CONSTANTS
CHARACTERS_TEXT: Final[str] = "characters"
NONE_TEXT: Final[str] = "None" 

# SYSTEM RELATED CONSTANTS
SUB_FOLDERS: Final[Sequence[str]] = [DataFolders.RAW, DataFolders.CLEANED]

GAME_CHOICES : Final[Sequence[str]] = [game.value for game in GameInitials]

CHARACTERS_JSON: Final[str] = f"{CHARACTERS_TEXT}.json"

CHARACTERS_CLEANED: Final[str] = f"{CHARACTERS_TEXT}.csv"

GAME_PARAM_INFO: Final[Sequence[Mapping]] =  [
    {
        ArgumentParserKwargs.NAME: "game",
        ArgumentParserKwargs.OTHER_PARAMS: {
            ArgumentParserKwargs.TYPE: str,
            ArgumentParserKwargs.CHOICES: GAME_CHOICES,
            ArgumentParserKwargs.HELP: "required game to extract character data from",
        },
    },
    {
        ArgumentParserKwargs.NAME: ("-d","--debug"),
        ArgumentParserKwargs.OTHER_PARAMS: {
            ArgumentParserKwargs.ACTION: "store_true",
            ArgumentParserKwargs.HELP: "enable debug mode",
        },
    },
]

CHARACTERS_PARSER_INFO : Final[Mapping] = {
    ArgumentParserKwargs.NAME: "characters",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character data from a specified game",
    ArgumentParserKwargs.HELP: "extract all character information from a specified game into an json file.",
}

PANDAS_PARSER_INFO : Final[Mapping] = {
    ArgumentParserKwargs.NAME: "pandas",
    ArgumentParserKwargs.DESCRIPTION: "subparser for extracting character json data to a csv file",
    ArgumentParserKwargs.HELP: "convert all character json data into an csv file.",
}

SYNC_PARSER_INFO: Final[Mapping] = {
    ArgumentParserKwargs.NAME: "sync",
    ArgumentParserKwargs.DESCRIPTION: "Fetch and convert character data for one or all games in a single step",
    ArgumentParserKwargs.HELP: "fetch and convert character data in one step (combines 'characters' + 'pandas').",
}

SYNC_GAME_PARAM_INFO: Final[Sequence[Mapping]] = [
    {
        ArgumentParserKwargs.NAME: "game",
        ArgumentParserKwargs.OTHER_PARAMS: {
            ArgumentParserKwargs.TYPE: str,
            ArgumentParserKwargs.CHOICES: GAME_CHOICES,
            ArgumentParserKwargs.HELP: "game to sync character data for",
            "nargs": "?",
            "default": None,
        },
    },
    {
        ArgumentParserKwargs.NAME: ("--all",),
        ArgumentParserKwargs.OTHER_PARAMS: {
            ArgumentParserKwargs.ACTION: "store_true",
            ArgumentParserKwargs.HELP: "sync all games in sequence",
        },
    },
    {
        ArgumentParserKwargs.NAME: ("-d", "--debug"),
        ArgumentParserKwargs.OTHER_PARAMS: {
            ArgumentParserKwargs.ACTION: "store_true",
            ArgumentParserKwargs.HELP: "enable debug mode",
        },
    },
]
