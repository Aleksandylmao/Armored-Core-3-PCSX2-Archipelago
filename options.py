from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, Range, Toggle


# If anyone is reading this check out Armored Core 1 APWorld and Armored Core 6 APWorld
class Goal(Choice):
	"""
	Choose what you want your goal to be.
	In missionsanity all missions are individually added to the pool of checks,
	you set the number of missions that you must complete in order to complete your goal.

	In progressive missions you receive 'progressive mission' items that unlock groups of
	5 missions at a time. Your goal is completing Infiltrate Layered Hub after collecting
	all 'progressive mission' items.
	"""
	display_name = "Goal"
	option_missionsanity = 0
	option_progressive_missions = 1
	default = 1


class MissionsanityGoalRequirement(Range):
	"""
	When goal is missionsanity.
	How many missions must be completed to win.
	"""
	display_name = "Missionsanity Goal Requirement"
	range_start = 1
	range_end = 49
	default = 49


class IncludeMissionRanks(Toggle):
	"""
	Each Rank you can achieve in a Mission will be its own Location.
	"""
	display_name = "Include Mission Ranks"


class ExcludeMissionRanks(Choice):
	"""
	Choose what achievable rank locations should be excluded.
	If you choose Rank A, Rank A and Rank S will be excluded.
	"""
	display_name = "Exclude Mission Ranks"
	option_rank_e = 0
	option_rank_d = 1
	option_rank_c = 2
	option_rank_b = 3
	option_rank_a = 4
	option_rank_s = 5
	option_exclude_nothing = 6
	default = 6


class Shopsanity(Toggle):
	"""
	Shopsanity turns all parts listings in the shop into locations,
	and all parts that you don't start with are shuffled into the multiworld.
	"""
	display_name = "Shopsanity"


class ShopsanityListingsPerMission(Range):
	"""
	Define how many shop listings open up per mission completion.
	Higher numbers may require more grinding. Includes Raven Test.
	"""
	display_name = "Shopsanity Listings Per Mission"
	range_start = 5
	range_end = 231
	default = 5


# Todo, adjust the link to where ever the extra rules are written down.
class ExtraRules(Toggle):
	"""
	When Shopsanity is turned on.
	This setting adds more rules to some Missions so that players will have an easier time.
	E.g. "Destroy Massive Weapon" will require a Leg-Hover part.
	For more infos see https://github.com/Aleksandylmao/Armored-Core-3-PCSX2-Archipelago/tree/master/docs
	"""


class CreditCheckAmount(Range):
	"""
	Define how much you earn from Credit Filler checks you receieve.
	"""
	display_name = "Credit Check Amount"
	range_start = 1000
	range_end = 100000
	default = 10000


@dataclass
class AC3Options(PerGameCommonOptions):
	goal: Goal
	missionsanity_goal_requirement: MissionsanityGoalRequirement
	credit_check_amount: CreditCheckAmount
	mission_rank: IncludeMissionRanks
	exclude_mission_ranks: ExcludeMissionRanks
	shopsanity: Shopsanity
	shopsanity_listings_per_mission: ShopsanityListingsPerMission
	extraRules: ExtraRules
