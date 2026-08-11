from __future__ import annotations
from typing import TYPE_CHECKING
from BaseClasses import Location
from . import items, options
from .utils import Constants
from .mission import Mission, all_missions, all_ranks, id_to_mission

if TYPE_CHECKING:
    from .world import AC3World

class AC3Location(Location):
    game = Constants.GAME_NAME


def get_location_name_for_mission_completed(m: Mission) -> str:
    return f"{m.name} Completed"

def get_location_id_for_mission_completed_id(mission_id: int) -> int:
    return Constants.ADDR_MISSION_COMPLETION + mission_id

def get_location_name_for_mission_rank(m: Mission, rank: str) -> str:
    return f"{m.name} Rank-{rank} Completed"

mission_location_name_to_id: dict[str, int] = {}
for mission in all_missions:
    mission_location_name_to_id[get_location_name_for_mission_completed(mission)] = get_location_id_for_mission_completed_id(mission.id)

#ToDo: Testing for ranks 
#mission_rank_location_name_to_id: dict[str, int] = {}
#i = all_missions[-1].id +2
#for mission in all_missions:
 #   for rank in all_ranks:
  #      mission_rank_location_name_to_id[get_location_name_for_mission_rank(mission,rank.name)] = i
   #     i=i+1

LOCATION_NAME_TO_ID: dict[str, int]
LOCATION_NAME_TO_ID = mission_location_name_to_id
#LOCATION_NAME_TO_ID.update(mission_rank_location_name_to_id.copy())

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def create_all_locations(world: AC3World) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: AC3World) -> None:
    mission_list = world.get_region(Constants.REGION_MISSION_LIST)
    first_district2 = world.get_region(Constants.REGION_FIRST_DISTRICT2)
    third_industrial_research = world.get_region(Constants.REGION_THIRD_INDUSTRIAL)
    third_district1 = world.get_region(Constants.REGION_THIRD_DISTRICT1)
    first_nature_area = world.get_region(Constants.REGION_FIRST_NATURE)
    first_special_research = world.get_region(Constants.REGION_FIRST_SPECIAL)
    second_waste_disposal = world.get_region(Constants.REGION_SECOND_WASTE)
    fourth_energy_production = world.get_region(Constants.REGION_FOURTH_ENERGY)
    layered_hub = world.get_region(Constants.REGION_LAYERED_HUB)

    # ToDo add region for missions so that I can do Region Shuffle
    location_to_add: dict[str, int] ={}

    for name, id in mission_location_name_to_id.items():
        if not world.options.goal == options.Goal.option_missionsanity and name == get_location_name_for_mission_completed(all_missions[-1]):
            continue

        location_to_add[name] = id

    mission_list.add_locations(location_to_add, AC3Location)

def create_events(world: AC3World) -> None:
    mission_list = world.get_region(Constants.REGION_MISSION_LIST)
    if world.options.goal == options.Goal.option_progressive_missions:
        mission_list.add_event(get_location_name_for_mission_completed(all_missions[-1]),"Victory", location_type=AC3Location,item_type=items.AC3Item)

