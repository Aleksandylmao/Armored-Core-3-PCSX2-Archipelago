"""
Reusable rule builders. Everything that says "can the player do mission X / N missions"
lives here, so mission locations, shop locations and mail locations share ONE definition.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from rule_builder.rules import And, False_, Has, HasFromList, Rule, True_

from .mail import (Always, AllOf, MissionCount, HasMission, Requirement, Unsupported, WithPart)
from .mission import Mission, all_missions, all_missions_by_order, mission_names, name_to_mission, \
	progressive_mission, DESTROY_KISARAGI_FORCES, DESTROY_MASSIVE_MT, DESTROY_MASSIVE_WEAPON, PROTECT_CREST_CONVOY, \
	INVESTIGATE_MAGNA_RUINS, INFILTRATE_REHITO_LAB
from .options import Goal
from .utils import Constants

if TYPE_CHECKING:
	from .world import AC3World


HARD_MISSIONS: tuple[Mission, ...] = (
	DESTROY_KISARAGI_FORCES,
	DESTROY_MASSIVE_MT,
	DESTROY_MASSIVE_WEAPON,
	PROTECT_CREST_CONVOY,
	INVESTIGATE_MAGNA_RUINS,
	INFILTRATE_REHITO_LAB,
)

HARD_MISSION_UNLOCK_REQUIREMENT = 10

_ORDER_INDEX = {m.name: i for i, m in enumerate(all_missions_by_order)}


def _chunks(order_index: int) -> int:
	"""Number of 'Progressive Mission' items needed to unlock the mission at this order index."""
	return order_index // Constants.UNLOCKS_PER_PROGRESSIVE_MISSION + 1


def _is_missionsanity(world: AC3World) -> bool:
	return world.options.goal == Goal.option_missionsanity


def hard_unlock_rule(world: AC3World) -> Rule:
	if _is_missionsanity(world):
		return HasFromList(*mission_names, count=HARD_MISSION_UNLOCK_REQUIREMENT)
	return True_()  # progressive order already handles it


def mission_rule(world: AC3World, mission: Mission) -> Rule:
	"""Can the player play (and therefore complete / fail) this mission?"""
	if _is_missionsanity(world):
		rule: Rule = Has(mission.name)
		if mission in HARD_MISSIONS:
			rule = rule & hard_unlock_rule(world)
		return rule
	return Has(progressive_mission.name, _chunks(_ORDER_INDEX[mission.name]))


def count_rule(world: AC3World, missions: Iterable[Mission], n: int) -> Rule:
	"""Can the player have completed `n` different missions out of `missions`?"""
	missions = list(missions)
	if n <= 0:
		return True_()
	if n > len(missions):
		return False_()
	if _is_missionsanity(world):
		return HasFromList(*(m.name for m in missions), count=n)
	# progressive: missions open in a fixed order, so the n-th earliest one decides
	indices = sorted(_ORDER_INDEX[m.name] for m in missions)
	return Has(progressive_mission.name, _chunks(indices[n - 1]))


def requirement_rule(world: AC3World, req: Requirement) -> Rule:
	"""Compile a declarative mail requirement into a Rule."""
	if isinstance(req, Always):
		return True_()
	if isinstance(req, HasMission):
		return mission_rule(world, req.mission)
	if isinstance(req, MissionCount):
		subset = all_missions if req.missions is None else req.missions
		return count_rule(world, subset, req.n)
	if isinstance(req, WithPart):
		rule = mission_rule(world, req.mission)
		if world.options.shopsanity:  # without shopsanity no part items exist, see notes
			rule = rule & Has(req.part)
		return rule
	if isinstance(req, AllOf):
		return And(*(requirement_rule(world, r) for r in req.requirements))
	if isinstance(req, Unsupported):
		return False_()
	raise TypeError(f"Unknown requirement {req!r}")
