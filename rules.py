from __future__ import annotations

from typing import TYPE_CHECKING
from rule_builder.rules import AtLeast, Has

from .locations import get_location_name_for_mission_completed
from .regions import get_region_connection_name
from .utils import Constants
from .options import Goal
from .mission import all_missions, STARTING_MISSION, progressive_mission, all_missions_by_order
if TYPE_CHECKING:
    from .world import AC3World


def set_all_rules(world: AC3World) -> None:
    set_all_entrance_rules(world)
    set_mission_location_rules(world)
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


def set_mission_location_rules(world: AC3World) -> None:
    if world.options.goal == Goal.option_progressive_missions:
        count =0
        for x in range(len(all_missions_by_order)):
            if x%Constants.UNLOCKS_PER_PROGRESSIVE_MISSION == 0:
                count += 1
            location = world.get_location(get_location_name_for_mission_completed(all_missions_by_order[x]))
            world.set_rule(location, Has(progressive_mission.name,count))

    elif world.options.goal == Goal.option_missionsanity:
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
        world.multiworld.completion_condition[player] = Has(Constants.ITEM_VICTORY).resolve(world)