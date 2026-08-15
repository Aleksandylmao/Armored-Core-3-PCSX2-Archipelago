from __future__ import annotations
import typing
from BaseClasses import Item, ItemClassification
from typing import TYPE_CHECKING

from . import options
from .mission import all_missions, name_to_mission, STARTING_MISSION, progressive_mission
from .utils import Constants

if TYPE_CHECKING:
    from .world import AC3World

class AC3Item(Item):
    game: str = Constants.GAME_NAME

#Credits
ITEM_NAME_TO_ID: typing.Dict[str, int] = {Constants.ITEM_CREDIT_NAME: Constants.ADDR_CREDITS}
item_id_to_item_name: typing.Dict[int, str] = {Constants.ADDR_CREDITS: Constants.ITEM_CREDIT_NAME}

#Missions
for mission in all_missions:
    item_id_to_item_name[mission.id + Constants.ADDR_MISSION_COMPLETION] = mission.name
    ITEM_NAME_TO_ID[mission.name] = mission.id + Constants.ADDR_MISSION_COMPLETION

ITEM_NAME_TO_ID[progressive_mission.name] = progressive_mission.id
item_id_to_item_name[progressive_mission.id] = progressive_mission.name


def create_item_with_correct_classification(world: AC3World, name: str) -> AC3Item:
    if name == Constants.ITEM_CREDIT_NAME:
        classification = ItemClassification.filler
    elif name in name_to_mission or name is progressive_mission.name:
        classification = ItemClassification.progression
    else:
        classification = ItemClassification.useful

    return AC3Item(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: AC3World) -> None:
    create_missions(world)
    create_filler(world)

def create_filler(world: AC3World) -> None:
    itempool: list[Item] = []

    number_of_items = len(world.multiworld.itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool

def create_missions(world: AC3World) -> None:
    itempool: list[Item] = []
    if world.options.goal == options.Goal.option_missionsanity:
        world.push_precollected(world.create_item(STARTING_MISSION.name))
        for mission2 in all_missions:
            if mission2 != STARTING_MISSION:
                itempool.append(world.create_item(mission2.name))
    else:
        world.push_precollected(world.create_item(progressive_mission.name))
        mission_count:int = int(len(all_missions)/Constants.UNLOCKS_PER_PROGRESSIVE_MISSION)
        for x in range(mission_count):
            itempool.append(world.create_item(progressive_mission.name))

    world.multiworld.itempool += itempool
