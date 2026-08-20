from enum import StrEnum, auto

class GameInitials(StrEnum): 
    """Enum of various games

    Args:
        StrEnum (class): class to enforce string enums
    """
    GI = auto()
    ZZZ = auto()
    FGO = auto()
    UMAMUSU = auto()

class DataFolders(StrEnum):
    """Enum of folder names

    Args:
        StrEnum (class): class to enforce string enums
    """
    DATA = auto()
    RAW = auto()
    CLEANED = auto()

class ArgumentParserKwargs(StrEnum):
    """Enum of Keyword Arguments for ArgumentParser

    Args:
        StrEnum (_type_): class to enforce string enums
    """

    NAME = auto()
    DESCRIPTION = auto()
    HELP = auto()
    CHOICES = auto()
    TYPE = auto()
    RUN = auto()
    OTHER_PARAMS = auto()
    ACTION = auto() # Added for flags like store_true

class CharacterTableColumnNames(StrEnum):
    """Enum of Column names applicable to any game

    Args:
        StrEnum (_type_): class to enforce string enums
    """
    ID = auto()
    RARITY = auto()
    NAME = auto()
    GENDER = auto()
    COST = auto()
    BIRTHDAY = auto()
    HPMAX = "hpMax"
    ATKMAX = "atkMax"
    DEFMAX = "defMax"
