import hakushin, ambr, atlasacademy
from .enums import GameInitials

type API = ambr.AmbrAPI | hakushin.HakushinAPI | atlasacademy.AtlasAcademyAPI

class ClientAPI:
    """Class to represent a Client API to request data from websites
    """
    def __new__(cls, game: GameInitials) -> API:
        """Attempt at a Singleton design pattern. Create using a different API based on what game

        Args:
            game (GameInitials): Enum containing various games

        Returns:
            API: API to retrieve data from
        """
        match game:
            case GameInitials.GI:
                return ambr.AmbrAPI()
            case GameInitials.ZZZ:
                return hakushin.HakushinAPI(GameInitials.ZZZ)
            case GameInitials.FGO:
                return atlasacademy.AtlasAcademyAPI()
            case _: # Highly unlikely default case
                return None