import pandas as pd
from typing import Any, Optional

from .general.enums import GameInitials
from .general.pandas_utils import normalize_json
from .gi.pandas_utils import process_gi_data
from .zzz.pandas_utils import process_zzz_data
from .fgo.pandas_utils import process_fgo_data
from .umamusume.pandas_utils import process_umamusume_data

def clean_up_character_info(character_data: Any, curve_data: Optional[Any], game: GameInitials) -> pd.DataFrame:
    """function to convert character information into a DataFrame Object. Attempt at a Facade/Factory Design Pattern.

    Args:
        character_data (Any): information of game characters from a game
        curve_data (Optional[Any]): growth curve data of GI characters
        game (GameInitials): game the character data is from

    Returns:
        pd.DataFrame: DataFrame Object containing character game data
    """
    pdData = normalize_json(character_data)

    match game:
        case GameInitials.GI:
            return process_gi_data(pdData, curve_data)
        case GameInitials.ZZZ:
            return process_zzz_data(pdData)
        case GameInitials.FGO:
            return process_fgo_data(pdData)
        case GameInitials.UMAMUSU:
            return process_umamusume_data(pdData)
        case _: # highly unlikely default case 
            return None
