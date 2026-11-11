from __future__ import annotations
from dataclasses import dataclass
from .mission import RequesterClient, mirage, crest, kisaragi, CLIENT_MISSIONS, Mission, \
	DEFEND_RUGLEN_LABORATORY, DEFEND_WATER_PROCESSORS, BOMB_DISARMAMENT, DESTROY_MASSIVE_MT, DESTROY_MASSIVE_WEAPON, \
	ELIMINATE_INTRUDERS, DEFEND_THE_ARENA, DEFEND_TESTING_GROUNDS, DESTROY_NAIRE_BRIDGE, INFILTRATE_LAYERED_HUB, \
	DEFEND_PERSONNEL_CONVOY, DESTROY_GUN_EMPLACEMENTS, DISTRACT_UNION_DEFENSES, ERADICATE_LIFE_FORMS, \
	SAFEGUARD_ALLOY_SAMPLE, DESTROY_GERM_CANISTERS, MT_TRAINING_EXERCISE, ELIMINATE_THE_BOMBERS, INFILTRATE_REHITO_LAB, \
	INVESTIGATE_MAGNA_RUINS, ASSAULT_CREST_FACILITY, DISABLE_SECURITY_SYSTEM, DESTROY_ESCAPING_MT, SECURE_THE_MINE, \
	DEFEND_THE_MONORAIL, EMPLOYEE_STANDOFF


class Requirement:
    """Marker base class."""


@dataclass(frozen=True)
class Always(Requirement):
    """Requirement is always satisfied."""
    pass


@dataclass(frozen=True)
class HasMission(Requirement):
    """
    Mission has been completed OR failed at least once.
    """
    mission: Mission


@dataclass(frozen=True)
class MissionCount(Requirement):
    """
    At least `n` different missions successfully completed.
    If `missions` is None, count all missions.
    Otherwise, count only missions in the supplied tuple.
    Also used for story progression.
    """
    n: int
    missions: tuple[Mission, ...] | None = None


@dataclass(frozen=True)
class WithPart(Requirement):
    """Mission attempted while a specific part is equipped."""
    mission: Mission
    part: str


@dataclass(frozen=True)
class AllOf(Requirement):
    """All supplied requirements must be satisfied."""
    requirements: tuple[Requirement, ...]


@dataclass(frozen=True)
class Unsupported(Requirement):
    """Cannot currently be modelled (arena, ambiguous rank rules, etc.)."""
    reason: str

def has_mission(mission: Mission) -> Requirement:
    """Mission completed OR failed."""
    return HasMission(mission)


def story(n: int) -> Requirement:
    """
    Story progression is the number of different successfully
    completed missions.
    """
    return MissionCount(n)


def client_count(client: RequesterClient, n: int) -> Requirement:
    """Number of successfully completed missions for a specific client."""
    return MissionCount(n, CLIENT_MISSIONS[client])


def with_part(mission: Mission, part: str) -> Requirement:
    return WithPart(mission, part)


def all_of(*requirements: Requirement) -> Requirement:
    return AllOf(tuple(requirements))


def is_supported(req: Requirement) -> bool:
    if isinstance(req, Unsupported):
        return False

    if isinstance(req, AllOf):
        return all(is_supported(r) for r in req.requirements)

    if isinstance(req, MissionCount) and req.missions is not None:
        return len(req.missions) >= req.n

    return True

#------------------------------------------------------------------------
@dataclass(frozen=True)
class Mail:
	id: int
	name: str
	requirement: Requirement = Always()
	challenge: bool = False  # needs a special condition in the mission, only with mailsanity = include_challenges


OP = "OP-INTENSIFY"
ARENA = Unsupported("arena not implemented")
ARENA_RANK = Unsupported("rank not implemented")

all_mails: tuple[Mail, ...] = (
	Mail(0x01, "The Controller - No. 0824-FK3203"),  # Raven Test is precollected -> always
	Mail(0x02, "Laine Meyers - Welcome Raven"),
	Mail(0x03, "Crest - Our Thanks", has_mission(EMPLOYEE_STANDOFF)),
	Mail(0x04, "Laine Meyers - Layered", has_mission(EMPLOYEE_STANDOFF)),
	Mail(0x05, "Mirage - Raven", has_mission(SECURE_THE_MINE)),
	Mail(0x09, "Mirage - Announcement", has_mission(DEFEND_THE_MONORAIL)),
	Mail(0x0B, "Crest - Closure of Sector 302", story(0x09)),
	Mail(0x0E, "Crest - Thanks For Your Help", has_mission(ELIMINATE_INTRUDERS)),
	Mail(0x0F, "Laine Meyers - Reason for Closure", has_mission(ELIMINATE_INTRUDERS)),
	Mail(0x10, "Union - Raven", story(0x0F)),
	Mail(0x11, "Laine Meyers - Unknown AC", has_mission(DESTROY_ESCAPING_MT)),
	Mail(0x12, "Union - Hypothesis", has_mission(DESTROY_ESCAPING_MT)),
	Mail(0x13, "Union - The Truth", story(0x15)),
	Mail(0x14, "Union - To Our Comrades", has_mission(DISABLE_SECURITY_SYSTEM)),
	Mail(0x15, "Union - To Our Comrades (2)", has_mission(ASSAULT_CREST_FACILITY)),
	Mail(0x16, "Union - Operation Failed", has_mission(DISABLE_SECURITY_SYSTEM)),  # needs a *failed* attempt
	Mail(0x17, "Union - Operation Failed (2)", has_mission(ASSAULT_CREST_FACILITY)),
	Mail(0x18, "Laine Meyers - Suspicions About Union", story(0x17)),
	Mail(0x19, "Laine Meyers - Emergency", story(0x1C)),
	Mail(0x1A, "Laine Meyers - Status Report", story(0x1E)),
	Mail(0x1B, "Mirage - Access Failed", story(0x22)),
	Mail(0x1D, "Laine Meyers - Crest Defenses Defeated", story(0x23)),
	Mail(0x1E, "Crest - Great Work", story(0x23)),
	Mail(0x1F, "Mirage - Request for Help", has_mission(DESTROY_MASSIVE_WEAPON)),
	Mail(0x20, "Mirage - The Controller", has_mission(INVESTIGATE_MAGNA_RUINS)),
	Mail(0x21, "Laine Meyers - Necessity", has_mission(DESTROY_MASSIVE_MT)),
	Mail(0x22, "Union - Will", has_mission(INFILTRATE_REHITO_LAB)),
	Mail(0x28, "Kisaragi - Additional Reward", has_mission(DESTROY_GERM_CANISTERS), challenge=True),
	Mail(0x29, "Kisaragi - Additional Reward (2)", has_mission(MT_TRAINING_EXERCISE), challenge=True),
	Mail(0x2A, "Kisaragi - Additional Reward (3)", AllOf((has_mission(DEFEND_WATER_PROCESSORS), has_mission(ELIMINATE_THE_BOMBERS))), challenge=True),
	Mail(0x2B, "Crest - Thanks", has_mission(SAFEGUARD_ALLOY_SAMPLE), challenge=True),
	Mail(0x2C, "Crest - Thanks (2)", has_mission(ERADICATE_LIFE_FORMS), challenge=True),
	Mail(0x2D, "Crest - Thanks (3)", AllOf((has_mission(DESTROY_GUN_EMPLACEMENTS), has_mission(DISTRACT_UNION_DEFENSES))), challenge=True),
	Mail(0x2E, "Global Cortex - Congratulations"),  # AC test in the garage, always in logic
	Mail(0x2F, "Mirage - Special Reward", has_mission(DEFEND_PERSONNEL_CONVOY), challenge=True),
	Mail(0x30, "Union - Part Supply", has_mission(DESTROY_MASSIVE_MT), challenge=True),
	Mail(0x31, "Union - New Part", has_mission(DEFEND_RUGLEN_LABORATORY), challenge=True),
	Mail(0x32, "Union - New Part (2)", has_mission(DESTROY_MASSIVE_MT), challenge=True),  # real trigger unknown
	Mail(0x33, "Union - New Part (3)", has_mission(INFILTRATE_LAYERED_HUB)),
	Mail(0x34, "??? - Request", has_mission(INFILTRATE_LAYERED_HUB)),
	Mail(0x35, "Kisaragi - Additional Reward (4)", has_mission(DESTROY_NAIRE_BRIDGE), challenge=True),
	Mail(0x36, "Mirage - Updated Part Lineup", client_count(mirage, 6)),
	Mail(0x37, "Mirage - Updated Part Lineup (2)", client_count(mirage, 9)),
	Mail(0x38, "Mirage - Updated Part Lineup (3)", client_count(mirage, 12)),
	Mail(0x39, "Crest - New Product Addition", client_count(crest, 8)),
	Mail(0x3A, "Crest - New Product Addition (2)", client_count(crest, 13)),
	Mail(0x3B, "Crest - New Product Addition (3)", client_count(crest, 17)),
	Mail(0x3C, "Kisaragi - New Part Release", client_count(kisaragi, 10)),
	Mail(0x3D, "Global Cortex - Top-Ranked Pilot", ARENA),
	Mail(0x3E, "Global Cortex - Advancement Reward", ARENA_RANK),  # any A rank
	Mail(0x3F, "Global Cortex - Advancement Reward (2)", ARENA_RANK),
	Mail(0x40, "Global Cortex - Advancement Reward (3)", ARENA_RANK),
	Mail(0x41, "Global Cortex - Advancement Reward (4)", ARENA_RANK),
	Mail(0x42, "Global Cortex - Reward", ARENA),
	Mail(0x43, "Crest - Good Luck", ARENA_RANK),
	Mail(0x44, "Crest - Crest Product Sponsor", ARENA_RANK),
	Mail(0x45, "Ace - (No Title)", ARENA),
	Mail(0x46, "Royal Mist - (No Title)", ARENA),
	Mail(0x47, "Valkyrie - (No Title)", ARENA),
	Mail(0x49, "Fixer - (No Subject)", ARENA),
	Mail(0x4A, "Royal Mist - (No Subject)",ARENA_RANK),  # any A rank
	Mail(0x50, "Spartan - Advancement", story(0x17)),
	Mail(0x51, "Cold Heart - Report", story(0x12)),
	Mail(0x52, "Huntress - Hi", story(0x14)),
	Mail(0x53, "Scylla - Unit Upgrade", story(0x15)),
	Mail(0x55, "Regina - Thanks", has_mission(DEFEND_TESTING_GROUNDS)),
	Mail(0x57, "Gaidoz - We'll Meet Again", has_mission(DEFEND_THE_ARENA)),
	Mail(0x5A, "OP-INTENSIFY - New Function Added - Radar", ARENA),
	Mail(0x5B, "OP-INTENSIFY - New Function Added - Various Sensors", WithPart(ELIMINATE_INTRUDERS, OP), True),
	Mail(0x5C, "OP-INTENSIFY - New Function Added - Blade Wave", WithPart(DESTROY_MASSIVE_WEAPON, OP), True),
	Mail(0x5D, "OP-INTENSIFY - New Function Added - Enhanced Cooling", WithPart(DESTROY_MASSIVE_MT, OP), True),
	Mail(0x5E, "OP-INTENSIFY - New Function Added - Cannon Operation", WithPart(DESTROY_MASSIVE_MT, OP), True),
	Mail(0x5F, "OP-INTENSIFY - New Function Added - Booster", ARENA),
	Mail(0x60, "OP-INTENSIFY - New Function Added - Turning", WithPart(BOMB_DISARMAMENT, OP), True),
	Mail(0x61, "OP-INTENSIFY - New Function Added - Missile Interception", WithPart(DEFEND_WATER_PROCESSORS, OP), True),
	Mail(0x62, "OP-INTENSIFY - New Function Added - Improved Targeting", with_part(DEFEND_RUGLEN_LABORATORY, OP), True),
	Mail(0x63, "OP-INTENSIFY - New Function Added - Blade Range", ARENA),
)

id_to_mail = {m.id: m for m in all_mails}
assert len(id_to_mail) == len(all_mails), "duplicate mail id"
assert len({m.name for m in all_mails}) == len(all_mails), "duplicate mail name (location names must be unique)"


def included_mails(include_challenges: bool) -> list[Mail]:
	"""Mails that become locations (and that the client watches)."""
	return [m for m in all_mails
            if is_supported(m.requirement) and (include_challenges or not m.challenge)]