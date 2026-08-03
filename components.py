from worlds.LauncherComponents import Component, Type, components, launch
from worlds.armoredcore3.utils import Constants


def run_client(*args: str) -> None:
	from .client import launch_ac3_client
	launch(launch_ac3_client, name=Constants.CLIENT_NAME, args=args)

components.append(
    Component(
        Constants.CLIENT_NAME,
        func=run_client,
        game_name=Constants.GAME_NAME,
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)