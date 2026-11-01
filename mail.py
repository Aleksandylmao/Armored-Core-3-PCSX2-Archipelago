from __future__ import annotations
from dataclasses import dataclass

class Requirement:
	"""Marker base class."""

@dataclass(frozen=True)
class Always(Requirement):
	pass

@dataclass(frozen=True)
class MissionDone(Requirement):
	"""Mission completed OR failed. Both only require that the mission is playable."""
	mission: str

@dataclass(frozen=True)
class MissionCount(Requirement):
	"""At least `n` different missions completed (optionally only out of `missions`).
	Also used for 'story progression >= n', see Story()."""
	n: int
	missions: tuple[str, ...] | None = None

@dataclass(frozen=True)
class WithPart(Requirement):
	"""Mission done while a part is equipped (part is an item with shopsanity)."""
	mission: str
	part: str

@dataclass(frozen=True)
class AllOf(Requirement):
	requirements: tuple[Requirement, ...]

@dataclass(frozen=True)
class Unsupported(Requirement):
	"""Cannot be modelled yet (arena, ambiguous rank rules, ...). Mail is left out."""
	reason: str

def done(mission: str) -> Requirement:
	return MissionDone(mission)

def story(n: int) -> Requirement:
	# Client writes story progression (0x5BE040) = number of different completed missions,
	# so "story >= n" is exactly "n different missions completed".
    # This is only needed for Organizing, It may be possible to add a Story Progression mode
    # where you play exactly like normal with choices instead of having something like Progressive Mission.
	return MissionCount(n)


# TODO: fill in which missions belong to which client (needed for the part-lineup mails).
# Until a client has enough missions listed, its mails are automatically treated as unsupported.
CLIENT_MISSIONS: dict[str, tuple[str, ...]] = {
	"Mirage": (),
	"Crest": (),
	"Kisaragi": (),
}

def client_count(client: str, n: int) -> Requirement:
	return MissionCount(n, CLIENT_MISSIONS[client])

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
	Mail(0x03, "Crest - Our Thanks", done("End Employee Standoff")),
	Mail(0x04, "Laine Meyers - Layered", done("End Employee Standoff")),
	Mail(0x05, "Mirage - Raven", done("Secure the Mine")),
	Mail(0x09, "Mirage - Announcement", done("Defend the Monorail")),
	Mail(0x0B, "Crest - Closure of Sector 302", story(0x09)),
	Mail(0x0E, "Crest - Thanks For Your Help", done("Eliminate Intruders")),
	Mail(0x0F, "Laine Meyers - Reason for Closure", done("Eliminate Intruders")),
	Mail(0x10, "Union - Raven", story(0x0F)),
	Mail(0x11, "Laine Meyers - Unknown AC", done("Destroy Escaping MT")),
	Mail(0x12, "Union - Hypothesis", done("Destroy Escaping MT")),
	Mail(0x13, "Union - The Truth", story(0x15)),
	Mail(0x14, "Union - To Our Comrades", done("Disable Security System")),
	Mail(0x15, "Union - To Our Comrades (2)", done("Assault Crest Facility")),
	Mail(0x16, "Union - Operation Failed", done("Disable Security System")),  # needs a *failed* attempt
	Mail(0x17, "Union - Operation Failed (2)", done("Assault Crest Facility")),
	Mail(0x18, "Laine Meyers - Suspicions About Union", story(0x17)),
	Mail(0x19, "Laine Meyers - Emergency", story(0x1C)),
	Mail(0x1A, "Laine Meyers - Status Report", story(0x1E)),
	Mail(0x1B, "Mirage - Access Failed", story(0x22)),
	Mail(0x1D, "Laine Meyers - Crest Defenses Defeated", story(0x23)),
	Mail(0x1E, "Crest - Great Work", story(0x23)),
	Mail(0x1F, "Mirage - Request for Help", done("Destroy Massive Weapon")),
	Mail(0x20, "Mirage - The Controller", done("Investigate Magna Ruins")),
	Mail(0x21, "Laine Meyers - Necessity", done("Destroy Massive MT")),
	Mail(0x22, "Union - Will", done("Infiltrate Rehito Lab")),
	Mail(0x28, "Kisaragi - Additional Reward", done("Destroy Germ Canisters"), challenge=True),
	Mail(0x29, "Kisaragi - Additional Reward (2)", done("MT Training Exercise"), challenge=True),
	Mail(0x2A, "Kisaragi - Additional Reward (3)", AllOf((done("Defend Water Processors"), done("Eliminate the Bombers"))), challenge=True),
	Mail(0x2B, "Crest - Thanks", done("Safeguard Alloy Sample"), challenge=True),
	Mail(0x2C, "Crest - Thanks (2)", done("Eradicate Life Forms"), challenge=True),
	Mail(0x2D, "Crest - Thanks (3)", AllOf((done("Destroy Gun Emplacements"), done("Distract Union Defenses"))), challenge=True),
	Mail(0x2E, "Global Cortex - Congratulations"),  # AC test in the garage, always in logic
	Mail(0x2F, "Mirage - Special Reward", done("Defend Personnel Convoy"), challenge=True),
	Mail(0x30, "Union - Part Supply", done("Destroy Massive MT"), challenge=True),
	Mail(0x31, "Union - New Part", done("Defend Ruglen Laboratory"), challenge=True),
	Mail(0x32, "Union - New Part (2)", done("Destroy Massive MT"), challenge=True),  # real trigger unknown
	Mail(0x33, "Union - New Part (3)", done("Infiltrate Layered Hub")),
	Mail(0x34, "??? - Request", done("Infiltrate Layered Hub")),
	Mail(0x35, "Kisaragi - Additional Reward (4)", done("Destroy Naire Bridge"), challenge=True),
	Mail(0x36, "Mirage - Updated Part Lineup", client_count("Mirage", 6)),
	Mail(0x37, "Mirage - Updated Part Lineup (2)", client_count("Mirage", 9)),
	Mail(0x38, "Mirage - Updated Part Lineup (3)", client_count("Mirage", 12)),
	Mail(0x39, "Crest - New Product Addition", client_count("Crest", 8)),
	Mail(0x3A, "Crest - New Product Addition (2)", client_count("Crest", 13)),
	Mail(0x3B, "Crest - New Product Addition (3)", client_count("Crest", 17)),
	Mail(0x3C, "Kisaragi - New Part Release", client_count("Kisaragi", 10)),
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
	Mail(0x55, "Regina - Thanks", done("Defend Testing Grounds")),
	Mail(0x57, "Gaidoz - We'll Meet Again", done("Defend the Arena")),
	Mail(0x5A, "OP-INTENSIFY - New Function Added - Radar", ARENA),
	Mail(0x5B, "OP-INTENSIFY - New Function Added - Various Sensors", WithPart("Eliminate Intruders", OP), True),
	Mail(0x5C, "OP-INTENSIFY - New Function Added - Blade Wave", WithPart("Destroy Massive Weapon", OP), True),
	Mail(0x5D, "OP-INTENSIFY - New Function Added - Enhanced Cooling", WithPart("Destroy Massive MT", OP), True),
	Mail(0x5E, "OP-INTENSIFY - New Function Added - Cannon Operation", WithPart("Destroy Massive MT", OP), True),
	Mail(0x5F, "OP-INTENSIFY - New Function Added - Booster", ARENA),
	Mail(0x60, "OP-INTENSIFY - New Function Added - Turning", WithPart("Bomb Disarmament", OP), True),
	Mail(0x61, "OP-INTENSIFY - New Function Added - Missile Interception", WithPart("Defend Water Processors", OP), True),
	Mail(0x62, "OP-INTENSIFY - New Function Added - Improved Targeting", WithPart("Defend Ruglen Laboratory", OP), True),
	Mail(0x63, "OP-INTENSIFY - New Function Added - Blade Range", ARENA),
)

id_to_mail = {m.id: m for m in all_mails}
assert len(id_to_mail) == len(all_mails), "duplicate mail id"
assert len({m.name for m in all_mails}) == len(all_mails), "duplicate mail name (location names must be unique)"


def included_mails(include_challenges: bool) -> list[Mail]:
	"""Mails that become locations (and that the client watches)."""
	return [m for m in all_mails
            if is_supported(m.requirement) and (include_challenges or not m.challenge)]