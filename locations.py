from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location
from . import items, options
from .mission import Mission, all_missions, FINAL_MISSION, all_ranks, Rank
from .parts import Part, all_parts
from .utils import Constants

if TYPE_CHECKING:
	from .world import AC3World


class AC3Location(Location):
	game = Constants.GAME_NAME


def get_location_name_for_mission_completed(m: Mission) -> str:
	return f"{m.name} Completed"


def get_location_id_for_mission_completed_id(mission_id: int) -> int:
	return Constants.ADDR_MISSION_COMPLETION + mission_id


def get_location_name_for_mission_rank(m: Mission, rank: Rank) -> str:
	return f"{m.name} Rank-{rank} Completed"


def get_location_id_for_mission_rank(mission: Mission, rank: Rank) -> int:
	return Constants.RANK_LOCATION_ID_BASE + (mission.id * len(all_ranks)) + rank.id


mission_location_name_to_id: dict[str, int] = {}
mission_rank_location_name_to_id: dict[str, int] = {}
for mission in all_missions:
	mission_location_name_to_id[
		get_location_name_for_mission_completed(mission)] = get_location_id_for_mission_completed_id(mission.id)
	for rank in all_ranks:
		mission_rank_location_name_to_id[
			get_location_name_for_mission_rank(mission, rank)] = get_location_id_for_mission_rank(mission, rank)


def get_location_name_for_shop(p: Part) -> str:
	return f"Shop {p.name}"


def get_location_id_for_shop_id(part_id: int) -> int:
	return Constants.ADDR_SHOP + part_id


shop_location_name_to_id: dict[str, int] = {}
for part in all_parts:
	shop_location_name_to_id[get_location_name_for_shop(part)] = get_location_id_for_shop_id(part.id)

LOCATION_NAME_TO_ID: dict[str, int]
LOCATION_NAME_TO_ID = {**mission_location_name_to_id, **shop_location_name_to_id, **mission_rank_location_name_to_id}


def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
	return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: AC3World) -> None:
	create_mission_locations(world)
	create_mission_rank_locations(world)
	create_shop_locations(world)
	create_events(world)


def create_shop_locations(world: AC3World) -> None:
	if not world.options.shopsanity:
		return

	shop = world.get_region(Constants.REGION_SHOP)
	shop.add_locations(shop_location_name_to_id, AC3Location)


def create_mission_locations(world: AC3World) -> None:
	mission_list = world.get_region(Constants.REGION_MISSION_LIST)
	location_to_add: dict[str, int] = {}

	for name, id in mission_location_name_to_id.items():
		# If the Mission mode is Progressiv skip the Final mission here, because it gets created as an event
		if not world.options.goal == options.Goal.option_missionsanity and name == get_location_name_for_mission_completed(
				FINAL_MISSION):
			continue
		location_to_add[name] = id
	mission_list.add_locations(location_to_add, AC3Location)


def create_mission_rank_locations(world: AC3World) -> None:
	if not world.options.mission_rank:
		return
	exclude_from: int = world.options.exclude_mission_ranks.value
	print(exclude_from)
	included_ranks = all_ranks[:exclude_from]

	mission_list = world.get_region(Constants.REGION_MISSION_LIST)
	location_to_add: dict[str, int] = {}

	for mission in all_missions:
		for rank in included_ranks:
			location_to_add[get_location_name_for_mission_rank(mission, rank)] = get_location_id_for_mission_rank(
				mission, rank)
	mission_list.add_locations(location_to_add, AC3Location)


def create_events(world: AC3World) -> None:
	if world.options.goal == options.Goal.option_progressive_missions:
		mission_list = world.get_region(Constants.REGION_MISSION_LIST)
		mission_list.add_event(get_location_name_for_mission_completed(FINAL_MISSION), Constants.ITEM_VICTORY,
		                       location_type=AC3Location, item_type=items.AC3Item)
