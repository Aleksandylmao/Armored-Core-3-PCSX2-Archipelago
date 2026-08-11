from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.options import OptionFilter
from .items import item_id_to_item_name
from .locations import get_location_name_for_mission_completed
from .regions import get_region_connection_name
from .utils import Constants
from .options import Goal
from .mission import all_missions, STARTING_MISSION
from ..generic.Rules import set_rule
from rule_builder.rules import AtLeast, Has, HasAll, Rule
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
    for mission in all_missions:
        if mission == STARTING_MISSION:
            continue  # always accessible, no item required
        location = world.get_location(get_location_name_for_mission_completed(mission))
        world.set_rule(location, Has(mission.name))

def set_completion_condition(world: AC3World) -> None:
    player = world.player

    if world.options.goal == Goal.option_missionsanity:
        non_starting = [
            mission.name
            for mission in all_missions
            if mission != STARTING_MISSION
        ]
        amount = world.options.missionsanity_goal_requirement.value

        world.multiworld.completion_condition[player] = AtLeast(
            amount,*(Has(mission) for mission in non_starting),).resolve(world)
    else: #Progressive mission
        final_mission = all_missions[-1]
        world.multiworld.completion_condition[player] = Has(final_mission.name).resolve(world)