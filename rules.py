from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule
from .regions import get_region_connection_name
from .utils import Constants
if TYPE_CHECKING:
    from worlds.armoredcore3 import AC3World


def set_all_rules(world: AC3World) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_entrance_rules(world: AC3World) -> None:
    menu = world.get_region(Constants.REGION_MENU)
    regions = []
    entrances = []
    for region in world.get_regions():
        if region != menu:
            regions.append(region)
            entrances.append(get_region_connection_name(menu.name, region.name))

    #ToDo add Items for Regions


def set_all_location_rules(world: AC3World) -> None:
    return

def set_completion_condition(world: AC3World) -> None:
    world.set_completion_rule(Has("Victory"))
