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


class MissionRanks(Choice):
	"""
	Choose what achievable Mission-Rank locations should be included.
	If you choose Rank A, Rank A and all Ranks below it will be included, E-Rank - A-Rank.
	Currently, the logic is if you can play the Mission you can achieve all included Ranks.
	I sincerely don't recommend S-Rank, especially with Shopsanity.
	"""
	display_name = "Include Mission Ranks"
	option_none = 0
	option_rank_e = 1
	option_rank_d = 2
	option_rank_c = 3
	option_rank_b = 4
	option_rank_a = 5
	option_rank_s = 6
	default = 0


class Shopsanity(Toggle):
	"""
	Shopsanity turns all parts listings in the shop into locations,
	and all parts that you don't start with are shuffled into the multiworld.
	Currently, the Missions will have no additional rules, Destroy Massive Weapon will not expect you to have a Hover.Part.
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
	# mission_rank: MissionRanks
	shopsanity: Shopsanity
	shopsanity_listings_per_mission: ShopsanityListingsPerMission
