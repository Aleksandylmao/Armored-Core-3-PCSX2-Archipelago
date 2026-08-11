import typing

from worlds.armoredcore3.utils import Constants

class Rank:
    id: int
    name: str

    def __init__(self, _id: int, name: str):
        self.id = _id
        self.name = name

    def __str__(self) -> str:
        return (
            f"{self.name} "
        )


class Mission:
    id: int
    name: str
    region: str

    def __init__(self, _id: int, name: str, region: str):
        self.id = _id
        self.name = name
        self.region = region

    def __str__(self) -> str:
        return (
            f"{self.name} "
        )

#Mission Completion 1 byte
#   Bit 1 - Ever successfully completed
#   Bit 2 - Ever failed
#Mission rank [8-Bit]
#   0x00 - Incomplete / Rank E
#   0x01 - Rank D
#   0x02 - Rank C
#   0x03 - Rank B
#   0x04 - Rank A
#   0x05 - Rank S

all_ranks:typing.Tuple[Rank,...] = (
    Rank(0x0, "E"),
    Rank(0x1, "D"),
    Rank(0x2, "C"),
    Rank(0x3, "B"),
    Rank(0x4, "A"),
    Rank(0x5, "S"),
)
#I decided against null iteration because those are the IDs that are used in game4
all_missions: typing.Tuple[Mission, ...] = (
    Mission(0x1, "Raven Test",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x2, "Defend Testing Grounds",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x3, "Secure Trene City",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x4, "Defend the Arena",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x5, "Secure the Mine", Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x6, "Defend Personnel Convoy",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x7, "Destroy Kisaragi Forces",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x8, "Defend Naire Bridge",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x9, "Destroy Naire Bridge",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0xA, "Destroy Escaping MT",Constants.REGION_FIRST_DISTRICT2),
    Mission(0xB, "Escort Transport", Constants.REGION_FIRST_DISTRICT2),
    Mission(0xC, "Rescue the Survey Team",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0xD, "Investigate Water Swells",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0xE, "Defend Water Processors",Constants.REGION_FIRST_NATURE),
    Mission(0xF, "Prevent Capsule Theft",Constants.REGION_FIRST_NATURE),
    Mission(0x10, "Defend Ruglem Laboratory", Constants.REGION_FIRST_SPECIAL),
    Mission(0x11, "Eradicate Life Forms",Constants.REGION_FIRST_SPECIAL),
    Mission(0x12, "Eliminate the Bombers", Constants.REGION_FIRST_NATURE),
    Mission(0x13, "Attack Mirage Forces",Constants.REGION_FIRST_NATURE),
    Mission(0x14,"Destroy Massive MT",Constants.REGION_FIRST_NATURE),
    Mission(0x15, "Eliminate Infiltrators",Constants.REGION_THIRD_DISTRICT1),
    Mission(0x16, "Destroy Massive Weapon",Constants.REGION_FIRST_NATURE),
    Mission(0x17, "Defend Energy Reactor", Constants.REGION_FOURTH_ENERGY),
    Mission(0x18, "Eliminate Intruders",Constants.REGION_THIRD_DISTRICT1),
    Mission(0x19, "Safeguard Alloy Sample",Constants.REGION_THIRD_DISTRICT1),
    Mission(0x1A, "Destroy the AC", Constants.REGION_THIRD_DISTRICT1),
    Mission(0x1B, "Defend the Monorail",Constants.REGION_THIRD_DISTRICT1),
    Mission(0x1C, "Destroy Computer",Constants.REGION_THIRD_INDUSTRIAL),
    #Mission(0x1D, ""), #The game crashes after commencing this mission
    Mission(0x1E, "Protect Crest Convoy",Constants.REGION_FIRST_SPECIAL),
    Mission(0x1F, "Disable Radar Equipment",Constants.REGION_FIRST_SPECIAL),
    Mission(0x20, "End Employee Standoff",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x21, "End Employee Rebellion",Constants.REGION_FIRST_DISTRICT2),
    Mission(0x22, "Recover Ship Cargo",Constants.REGION_FIRST_NATURE),
    Mission(0x23, "Defend Helicopter Crew",Constants.REGION_FIRST_NATURE),
    Mission(0x24, "Destroy Gun Emplacements",Constants.REGION_FIRST_SPECIAL),
    Mission(0x25, "Recover Data Capsules",Constants.REGION_FIRST_SPECIAL),
    Mission(0x26, "Steal the Access Program",Constants.REGION_FOURTH_ENERGY),
    Mission(0x27, "Infiltrate Rehito Lab",Constants.REGION_FOURTH_ENERGY),
    Mission(0x28, "Bomb Disarmament", Constants.REGION_SECOND_WASTE),
    Mission(0x29, "Disable Pulse Generators", Constants.REGION_SECOND_WASTE ),
    Mission(0x2A, "Defend Crest HQ", Constants.REGION_SECOND_WASTE),
    Mission(0x2B, "Distract Union Defenses",Constants.REGION_FIRST_SPECIAL),
    Mission(0x2C, "Safeguard Water Supply",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x2D, "Disable Security System", Constants.REGION_SECOND_WASTE),
    Mission(0x2E, "Assault Crest Facility", Constants.REGION_SECOND_WASTE),
    Mission(0x2F, "Destroy Germ Canisters",Constants.REGION_FIRST_SPECIAL),
    Mission(0x30, "MT Training Exercise",Constants.REGION_THIRD_INDUSTRIAL),
    Mission(0x31, "Investigate Magna Ruins",Constants.REGION_FOURTH_ENERGY),
    Mission(0x32, "Infiltrate Layered Hub", Constants.REGION_LAYERED_HUB),
)

STARTING_MISSION = all_missions[0]
id_to_mission = {mission.id: mission for mission in all_missions}
name_to_mission = {mission.name: mission for mission in all_missions}
all_mission_ids = {mission.id for mission in all_missions}
