from dataclasses import dataclass
from Options import Choice, PerGameCommonOptions, Range, Toggle
#If anyone is reading this check out Armored Core 1 APWorld and Armored Core 6 APWorld
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

class CreditCheckAmount(Range):
    """
    Define how much you earn from Credit Filler checks you receieve.
    """
    display_name = "Credit Check Amount"
    range_start = 1000
    range_end = 100000
    default = 10000

class IncludeMissionRanks(Toggle):
    """
    Each Rank you can achieve in a Mission will be its own Location.
    """
    display_name = "Include Mission Ranks"

class ExcludeMissionRanks(Choice):
    """
    Choose what achievable ranks should be excluded.
    If you choose Rank A, Rank A and Rank S will be excluded.
    """
    display_name = "Exclude Mission Ranks"
    none = 0
    rank_s = 1
    rank_a = 2
    rank_b = 3
    rank_c = 4
    rank_d = 5
    rank_e = 6
    default = 1

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
    range_start = 4
    range_end = 146
    default = 4

class ShuffleParts(Toggle):
    """
    If you choose against Shopsanity.
    All parts that you don't start with are shuffled into the multiworld.
    And the shop will be disabled.
    """
    display_name = "Shuffle Parts"

@dataclass
class AC3Options(PerGameCommonOptions):
    goal: Goal
    missionsanity_goal_requirement: MissionsanityGoalRequirement
    credit_check_amount: CreditCheckAmount