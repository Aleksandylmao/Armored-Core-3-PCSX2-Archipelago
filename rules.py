from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has
from .locations import get_location_name_for_mission_completed, get_location_name_for_shop, \
	get_location_name_for_mission_rank
from .mission import all_missions, progressive_mission, all_missions_by_order, all_ranks, name_to_mission
from .options import Goal
from .parts import all_parts, all_part_list, base_starting_parts
from .regions import get_region_connection_name
from .utils import Constants
from ..generic.Rules import add_rule

if TYPE_CHECKING:
	from .world import AC3World

HARD_MISSIONS: tuple[str, ...] = (
	"Destroy Kisaragi Forces",
	"Destroy Massive MT",
	"Destroy Massive Weapon",
	"Protect Crest Convoy",
	"Investigate Magna Ruins",
	"Infiltrate Rehito Lab",
)
HARD_MISSION_UNLOCK_REQUIREMENT = 10


def set_all_rules(world: AC3World) -> None:
	set_all_entrance_rules(world)
	set_mission_location_rules(world)
	set_completion_condition(world)
	set_shop_location_rules(world)
	# set_mission_rank_location_rules(world)
	set_hard_mission_rules(world)


def set_all_entrance_rules(world: AC3World) -> None:
	menu = world.get_region(Constants.REGION_MENU)
	regions = []
	entrances = []
	for region in world.get_regions():
		if region != menu:
			regions.append(region)
			entrances.append(get_region_connection_name(menu.name, region.name))


def set_mission_location_rules(world: AC3World) -> None:
	if world.options.goal == Goal.option_progressive_missions:
		count = 0
		for x in range(len(all_missions_by_order)):
			if x % Constants.UNLOCKS_PER_PROGRESSIVE_MISSION == 0:
				count += 1
			location = world.get_location(get_location_name_for_mission_completed(all_missions_by_order[x]))
			world.set_rule(location, Has(progressive_mission.name, count))

	elif world.options.goal == Goal.option_missionsanity:
		for mission in all_missions:
			location = world.get_location(get_location_name_for_mission_completed(mission))
			world.set_rule(location, Has(mission.name))


def set_completion_condition(world: AC3World) -> None:
	player = world.player

	if world.options.goal == Goal.option_missionsanity:
		amount = world.options.missionsanity_goal_requirement.value
		world.multiworld.completion_condition[player] = lambda state: (
				sum(state.has(mission.name, player) for mission in all_missions) >= amount)
	else:  # Progressive mission
		world.multiworld.completion_condition[player] = Has(Constants.ITEM_VICTORY).resolve(world)


def set_shop_location_rules(world: AC3World) -> None:
	if not world.options.shopsanity:
		return
	shop_listings = world.options.shopsanity_listings_per_mission.value

	if world.options.goal == Goal.option_missionsanity:
		for count, mission in enumerate(all_missions):
			start_index = count * shop_listings
			end_index = min(start_index + shop_listings, len(all_parts))

			for part in all_parts[start_index:end_index]:
				location = world.get_location(get_location_name_for_shop(part))
				world.set_rule(location, Has(mission.name))

	elif world.options.goal == Goal.option_progressive_missions:
		for count, _ in enumerate(all_missions_by_order):
			progressive_count = (count // Constants.UNLOCKS_PER_PROGRESSIVE_MISSION) + 1
			start_index = count * shop_listings
			end_index = min(start_index + shop_listings, len(all_parts))

			for part in all_parts[start_index:end_index]:
				location = world.get_location(get_location_name_for_shop(part))
				world.set_rule(location, Has(progressive_mission.name, progressive_count))


def set_mission_rank_location_rules(world: AC3World) -> None:
	included_ranks = all_ranks[:world.options.mission_rank.value]
	if world.options.goal == Goal.option_progressive_missions:
		count = 0
		for x in range(len(all_missions_by_order)):
			if x % Constants.UNLOCKS_PER_PROGRESSIVE_MISSION == 0:
				count += 1
			for rank in included_ranks:
				location = world.get_location(get_location_name_for_mission_rank(all_missions_by_order[x], rank))
				world.set_rule(location, Has(progressive_mission.name, count))

	elif world.options.goal == Goal.option_missionsanity:
		for mission in all_missions:
			for rank in included_ranks:
				location = world.get_location(get_location_name_for_mission_rank(mission, rank))
				world.set_rule(location, Has(mission.name))


def missions_unlocked_rule(world: AC3World):
	player = world.player
	if world.options.goal == Goal.option_missionsanity:
		def rule(state):
			return sum(state.has(m.name, player) for m in all_missions) >= HARD_MISSION_UNLOCK_REQUIREMENT

		return rule
	chunks_needed = -(-HARD_MISSION_UNLOCK_REQUIREMENT // Constants.UNLOCKS_PER_PROGRESSIVE_MISSION)
	return Has(progressive_mission.name, chunks_needed).resolve(world)


def shopsanity_part_diversity_rule(world: AC3World):
	player = world.player
	category_requirements = []  # (category, required_count) pairs, computed once
	for category in all_part_list:
		starting_in_category = sum(1 for p in category if p in base_starting_parts)
		required = starting_in_category + 1
		category_requirements.append((category, required))

	def rule(state):
		for category, required in category_requirements:
			owned = sum(1 for p in category if state.has(p.name, player))
			if owned < required:
				return False
		return True

	return rule


def set_hard_mission_rules(world: AC3World) -> None:
	if world.options.goal == Goal.option_progressive_missions:
		return
	unlock_rule = missions_unlocked_rule(world)
	# part_rule = shopsanity_part_diversity_rule(world) if world.options.shopsanity else None

	for mission_name in HARD_MISSIONS:
		mission = name_to_mission[mission_name]
		location = world.get_location(get_location_name_for_mission_completed(mission))
		add_rule(location, unlock_rule)
#	if part_rule is not None:
#		add_rule(location, part_rule)
