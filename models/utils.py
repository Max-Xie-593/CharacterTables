from argparse import ArgumentParser, Namespace
from typing import Any, Optional
from itertools import product
from collections.abc import Sequence, Mapping
import json, os, asyncio

from .gi.constants import GI_CHARACTER_CURVE
from .general.constants import (
    CHARACTERS_JSON, 
    CHARACTERS_CLEANED, 
    GAME_CHOICES, 
    SUB_FOLDERS
)
from .general.enums import (
    GameInitials,
    DataFolders,
    ArgumentParserKwargs
)
from .client import get_client_api, API
from .builder import clean_up_character_info

__all__ = (
    "add_parser_info",
    "print_character_data",
    "convert_character_data",
)

def check_data_directory() -> None:
    """Check to see if the data directory exists, otherwise create it
    """
    for game, isclean in product(
        GAME_CHOICES,
        SUB_FOLDERS
    ):
        os.makedirs(
            os.path.join(
                DataFolders.DATA,
                game,
                isclean
            ),
            exist_ok=True
        )

def write_json_to_file(
        json_info: Any,
        game: GameInitials,
        output_file: str
    ) -> None:
    """output the json information into a file

    Args:
        json_info (Any): data from the game
        game (GameInitials): game the json information is for
        output_file (str): file name to output to
    """
    check_data_directory()
    with open(
        os.path.join(
            DataFolders.DATA,
            game,
            DataFolders.RAW,
            output_file
        ),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            json_info,
            file,
            indent=4,
            ensure_ascii=False
        )

def read_json_to_variable(
        game: GameInitials,
        input_file: str
    ) -> Optional[Any]:
    """read the file and store to a variable

    Args:
        game (GameInitials): game the json information is for
        input_file (str): file name to read from

    Returns:
        Optional[Any]: either a variable containing the file contents or nothing
    """
    check_data_directory()
    filePath = os.path.join(
        DataFolders.DATA,
        game,
        DataFolders.RAW,
        input_file
    )
    return json.load(
        open(
            filePath,
            "r",
            encoding="utf-8",
        )
    ) if os.path.isfile(filePath) else None

def add_parser_info(
    parser: ArgumentParser,
    arguments: Sequence[Mapping],
    defaults: Mapping
) -> None:
    """function to add arguments and defaults to the parser

    Args:
        parser (ArgumentParser): parser to add arugments and defaults to
        arguments (Sequence[Mapping]): dict containing arugment information
        defaults (Mapping): dict containing defaults in parser format
    """
    def add_arguments_to_parser(
            parser: ArgumentParser,
            arguments: Sequence[Mapping]
        ) -> None:
        """helper function to add arguments to the parser

        Args:
            parser (ArgumentParser): parser to add arugments and defaults to
            arguments (Sequence[Mapping]): dict containing arugment information
        """
        for parameter_info in arguments:
            parser.add_argument(
                parameter_info[
                    ArgumentParserKwargs.NAME
                ], 
                **parameter_info[
                    ArgumentParserKwargs.OTHER_PARAMS
                ]
            )

    def add_defaults_to_parser(
            parser: ArgumentParser,
            defaults: Mapping
        ) -> None:
        """helper function to add defaults to the parser

        Args:
            parser (ArgumentParser): parser to add arugments and defaults to
            defaults (Mapping): dict containing arugment information
        """
        parser.set_defaults(**defaults)

    add_arguments_to_parser(parser, arguments)
    add_defaults_to_parser(parser, defaults)

def convert_character_data(args: Namespace) -> None:
    """default function to run for the pandas function from the driver

    Args:
        args (Namespace): arguments parsed from the ArgumentParser
    """
    clean_json_to_csv(GameInitials(args.game))

def clean_json_to_csv(game: GameInitials) -> None:
    """convert the json information into a csv

    Args:
        game (GameInitials): game to read the files from
    """
    check_data_directory()
    clean_up_character_info(
        read_json_to_variable(
            game,
            f"{game}_{CHARACTERS_JSON}"
        ),
        read_json_to_variable(
            game,
            GI_CHARACTER_CURVE
        ),
        game,
    ).to_csv(
        os.path.join(
            DataFolders.DATA, 
            game, 
            DataFolders.CLEANED, 
            f"{game}_{CHARACTERS_CLEANED}"
        ), 
        encoding="utf-8",
        index=False
    )

def print_character_data(args: Namespace):
    """default function to run for the characters function from the driver

    Args:
        args (Namespace): arguments parsed from the ArgumentParser
    """
    game = GameInitials(args.game)
    extract_character_data(
        get_client_api(game),
        game
    )

def extract_character_data(
        client: API,
        game: GameInitials
    ) -> None:
    """retrieve json data from the websites using the API

    Args:
        client (ClientAPI): API Client used to retrieve data from
        game (GameInitials): game to retrieve data from
    """
    if game is GameInitials.GI and not os.path.exists(
        os.path.join(
            DataFolders.DATA,
            game,
            DataFolders.RAW,
            GI_CHARACTER_CURVE
        )
    ):
        asyncio.run(
            extract_gi_character_curve(
                client,
                game,
                GI_CHARACTER_CURVE
            )
        )
    asyncio.run(
        extract_character(
            client,
            game,
            f"{game}_{CHARACTERS_JSON}"
        )
    )

async def extract_gi_character_curve(
        client: API,
        game: GameInitials,
        output_file: str
    ) -> None:
    """function to extract the Genshin Impact character curve to calculate max stats

    Args:
        client (ClientAPI): API Client used to retrieve data from
        game (GameInitials): game to retrieve data from
        output_file (str): file name to output to
    """
    async with client as api:
        write_json_to_file(
            await api.fetch_avatar_curve(),
            game,
            output_file
        )

async def extract_character(
        client: API,
        game: GameInitials,
        output_file: str
    ) -> None:
    """function to extract character information from websites and output to a file

    Args:
        client (ClientAPI): API Client used to retrieve data from
        game (GameInitials): game to retrieve data from
        output_file (str): file name to output to
    """
    async with client as api:
        write_json_to_file(
            [
                json.loads(
                    (
                        await api.fetch_character_detail(
                            character.id, use_cache=False
                        )
                    ).model_dump_json(ensure_ascii=True)
                )
                for character in await api.fetch_characters(use_cache=False)
            ],
            game,
            output_file,
        )