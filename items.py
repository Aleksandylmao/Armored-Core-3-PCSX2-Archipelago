from __future__ import annotations
import typing
from BaseClasses import Item, ItemClassification
from typing import TYPE_CHECKING

from .mission import all_missions, name_to_mission, STARTING_MISSION
from .utils import Constants
from .parts import all_parts, base_starting_parts

if TYPE_CHECKING:
    from .world import AC3World

class AC3Item(Item):
    game: str = Constants.GAME_NAME

ITEM_NAME_TO_ID: typing.Dict[str, int] = {Constants.CREDIT_ITEM_NAME: Constants.ADDR_CREDITS}
item_id_to_item_name: typing.Dict[int, str] = {Constants.ADDR_CREDITS: Constants.CREDIT_ITEM_NAME}

"""for part in all_parts:
    item_id_to_item_name[part.id+ Constants.ADDR_INVENTORY] = part.name
    ITEM_NAME_TO_ID[part.name] = part.id+ Constants.ADDR_INVENTORY"""

for mission in all_missions:
    item_id_to_item_name[mission.id] = mission.name
    ITEM_NAME_TO_ID[mission.name] = mission.id



def create_item_with_correct_classification(world: AC3World, name: str) -> AC3Item:
    if name == Constants.CREDIT_ITEM_NAME:
        classification = ItemClassification.filler
    elif name in name_to_mission:
        classification = ItemClassification.progression
    else:
        classification = ItemClassification.useful

    return AC3Item(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: AC3World) -> None:
    itempool: list[Item] = []

    """starting_set = set(base_starting_parts)
    for part2 in all_parts:
        if not part2 in starting_set:
            itempool.append(world.create_item(part2.name))"""

    for mission2 in all_missions:
        if mission2 != STARTING_MISSION:
            itempool.append(world.create_item(mission2.name))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

    """for starting in base_starting_parts:
        world.push_precollected(world.create_item(starting.name))"""
    world.push_precollected(world.create_item(STARTING_MISSION.name))