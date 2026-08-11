from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, DefaultOnToggle, Toggle as DefaultOffToggle
#If anyone is reading this check out Armored Core 1 APWorld it's sick
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
    default = 0

class MissionsanityGoalRequirement(Range):
    """
    When Goal is Missionsanity.
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

@dataclass
class AC3Options(PerGameCommonOptions):
    goal: Goal
    missionsanity_goal_requirement: MissionsanityGoalRequirement
    credit_check_amount: CreditCheckAmount