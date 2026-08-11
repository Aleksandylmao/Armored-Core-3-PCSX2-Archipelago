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
#Those below are just Ideas that I had I don't know if those Ideas are great or not, I'm not sure
#Ai should take a look at what I write, my god...
"""class Goal(Choice):
    
    Choose which one will be your Goal.
    
    display_name = Goal
    option_mission = 0
    option_arena = 1
    option_both = 2
    default = option_both
"""
"""class MissionGoal(Choice):
    
    You need to include either an Arena or Mission goal or both.
    In missionsanity all missions are individually added to the pool of checks,
    you set the number of missions that you must complete in order to complete your goal.
    In progressive missions you receive 'progressive mission' items that unlock groups of
    5 missions at a time. Your goal is completing Destroy Floating Mines after collecting
    all 'progressive mission' items.
    In exclude mission, missions don't send checks .
    
    display_name = Mission Goal
    option_missionsanity = 0
    option_progressive_missions = 1
    option_exclude_missions = 2
    default = option_progressive_missions"""

"""class ArenaGoal(Choice):
    
    You need to include either an Arena or Mission goal or both.
    In arenasanity all arena challenges are individually added to the pool of checks,
    you set the number of challenges that you must complete in order to complete your goal.
    In progressive arena you receive 'progressive arena' items that unlock groups of
    5 challenges at a time. Your goal is to achieve Rank 1 after collecting
    all 'progressive mission' items.
    In exclude arena, arena challenges don't send checks.
    
    display_name = Arena Goal
    option_arenasanity = 0
    option_progressive_arena = 1
    option_exclude_arena = 2
    default = option_progressive_arena"""

"""class MissionsanityGoalRequirement(Range):
    
    This option only matters if your Goal is Missionsanity.
    Select how many missions it takes to complete your goal.
    Does not include the tutorial mission.
    
    display_name = Missionsanity Goal Requirement
    range_start = 1
    range_end = 48
    default = 48"""

"""class ArenasanityGoalRequirement(Range):
    
    This option only matters if your Goal is Arenasanity.
    Select how many missions it takes to complete your goal.
    Does not include the tutorial mission.
   
    display_name = Arenasanity Goal Requirement
    range_start = 1
    range_end = 71
    default = 71"""


"""class RanomizeStartingParts(DefaultOffToggle):
    
    Your starting AC Parts will be randomized but still
    adhere to weight and energy limits.
    
    display_name = Randomize Starting AC Parts"""

"""class ShuffleRegions(DefaultOffToggle):

    This includes the Arena and the Regions in the Mission select screen.
    Ravens test completion will be in logic, but not the ranks.
   
    display_name = Shuffle Regions"""



"""class Shopsanity(DefaultOffToggle):
    
    Shopsanity turns all parts listings in the shop into locations,
    and all parts that you don't start with are shuffled into the multiworld.
    
    display_name = "Shopsanity"""

"""class ShopsanityListingsPerMission(Range):
    
    Define how many shop listings open up per mission completion.
    Higher numbers may require more grinding. Includes Raven Test.
   
    display_name = Shopsanity Listings Per Mission
    range_start = 4
    range_end = 146
    default = 4"""

#This one might be its own Goal option honestly, since you need to complete little side missions with OP-INTENSIFY equipped
"""class IncludeOpIntensify(DefaultOffToggle):

    If this option is on, OP-INTENSIFY will be added to the item pool.

    display_name = "Include OP-INTENSIFY"""

