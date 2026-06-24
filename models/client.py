import hakushin, ambr, atlasacademy, umamusume
from .enums import GameInitials
from functools import cache

type API = ambr.AmbrAPI | hakushin.HakushinAPI | atlasacademy.AtlasAcademyAPI | umamusume.UmaMusumeAPI

@cache
def get_client_api(game: GameInitials) -> API | None:
    """Factory function that caches the API client so it is only initialized once per game.

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
            case _: # Highly unlikely default case
                return None