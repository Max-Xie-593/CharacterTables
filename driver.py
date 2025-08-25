from argparse import ArgumentParser, RawTextHelpFormatter, RawDescriptionHelpFormatter, Namespace
from typing import Generator, Dict, Callable, Tuple
from models import *

def construct_main_parser() -> ArgumentParser:
    """Creates the Argument Parser used for parsing command line inputs

    Returns:
        ArgumentParser: Object for parsing command line strings into Python objects
    """

    def retrieve_subparser_information() -> Generator[
        Tuple[
            Dict,
            Callable[
                [
                    Namespace
                ],
                None
            ]
        ],
        None,
        None
        ]:
        """Generator to output tuples of information for creating subparsers

        Yields:
            Generator[Tuple[Dict,Callable[[Namespace],None]],None,None]: Tuple containing a dict information regarding parser data and functions for the parser to run
        """
        yield (CHARACTERS_PARSER_INFO, print_character_data)
        yield (PANDAS_PARSER_INFO, convert_character_data)

    parser: ArgumentParser = ArgumentParser(
        prog="chardata",
        description="A Character Roster Parser of various games",
        formatter_class=RawDescriptionHelpFormatter,
    )

    subparser = parser.add_subparsers()
    subparser.required = True

    for newParser, default in retrieve_subparser_information():
        moduleParser = subparser.add_parser(
            newParser[
                ArgumentParserKwargs.NAME
            ],
            description=newParser[
                ArgumentParserKwargs.DESCRIPTION
            ],
            help=newParser[
                ArgumentParserKwargs.HELP
            ],
            formatter_class=RawTextHelpFormatter,
        )
        add_parser_info(
            moduleParser,
            GAME_PARAM_INFO,
            { 
                ArgumentParserKwargs.RUN: default 
            }
        )

    return parser

def main() -> None:
    """Driver to parse and execute the functions
    """
    args = construct_main_parser().parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
