from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld
from .utils import Constants

class AC3Web(WebWorld):
    game = Constants.GAME_NAME
    theme = "dirt"
    setup_en = Tutorial(
            "Multiworld Setup Guide",
            f"A guide to setting up {Constants.GAME_NAME} for Archipelago multiworld games.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Aleksandy"],
        )
    tutorials = [setup_en]
