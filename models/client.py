import hakushin, ambr, atlasacademy, umamusume
from .general.enums import GameInitials

type API = ambr.AmbrAPI | hakushin.HakushinAPI | atlasacademy.AtlasAcademyAPI | umamusume.UmaMusumeAPI

def get_client_api(game: GameInitials) -> API | None:
    """Factory function to initialize the API client for a given game.

    Args:
        game (GameInitials): Enum containing various games

    Returns:
        API | None: API to retrieve data from
    """
    match game:
            case GameInitials.GI:
                return ambr.AmbrAPI()
            case GameInitials.ZZZ:
                return hakushin.HakushinAPI(GameInitials.ZZZ,use_live=True)
            case GameInitials.FGO:
                return atlasacademy.AtlasAcademyAPI()
            case GameInitials.UMAMUSU:
                return umamusume.UmaMusumeAPI()
            case _: # highly unlikely default case
                return None