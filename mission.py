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
    mission_order: int
    story_progression: int
    def __init__(self, _id: int, name: str, region: str, mission_order:int, story_progression: int):
        self.id = _id
        self.name = name
        self.region = region
        self.mission_order = mission_order
        self.story_progression = story_progression

    def __str__(self) -> str:
        return (
            f"{self.name} "
        )

#mission_order source https://www.scribd.com/document/86339948/Armored-Core-3-Prima-Official-eGuide-Copia#page=3
#Story_progression, from the memory

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

all_missions: typing.Tuple[Mission, ...] = (
    Mission(0x1, "Raven Test",Constants.REGION_FIRST_DISTRICT2, 0,0x00),
    Mission(0x2, "Defend Testing Grounds",Constants.REGION_FIRST_DISTRICT2, 8,0x06),
    Mission(0x3, "Secure Trene City",Constants.REGION_FIRST_DISTRICT2, 37,0x1D),
    Mission(0x4, "Defend the Arena",Constants.REGION_FIRST_DISTRICT2,1,0x01),
    Mission(0x5, "Secure the Mine", Constants.REGION_THIRD_INDUSTRIAL, 3,0x02),
    Mission(0x6, "Defend Personnel Convoy",Constants.REGION_THIRD_INDUSTRIAL,17,0x0D),
    Mission(0x7, "Destroy Kisaragi Forces",Constants.REGION_THIRD_INDUSTRIAL,36,0x1D),
    Mission(0x8, "Defend Naire Bridge",Constants.REGION_THIRD_INDUSTRIAL,4,0x04),
    Mission(0x9, "Destroy Naire Bridge",Constants.REGION_THIRD_INDUSTRIAL,12,0x09),
    Mission(0xA, "Destroy Escaping MT",Constants.REGION_FIRST_DISTRICT2,7,0x08),
    Mission(0xB, "Escort Transport", Constants.REGION_FIRST_DISTRICT2,5,0x04),
    Mission(0xC, "Rescue the Survey Team",Constants.REGION_THIRD_INDUSTRIAL,9,0x07),
    Mission(0xD, "Investigate Water Swells",Constants.REGION_THIRD_INDUSTRIAL,23,0x12),
    Mission(0xE, "Defend Water Processors",Constants.REGION_FIRST_NATURE, 34,0x19),
    Mission(0xF, "Prevent Capsule Theft",Constants.REGION_FIRST_NATURE,15,0x0D),
    Mission(0x10, "Defend Ruglen Laboratory", Constants.REGION_FIRST_SPECIAL, 21,0x10),
    Mission(0x11, "Eradicate Life Forms",Constants.REGION_FIRST_SPECIAL,22,0x12),
    Mission(0x12, "Eliminate the Bombers", Constants.REGION_FIRST_NATURE,35,0x19), #It's a bonus mission to Defend Water Processors
    Mission(0x13, "Attack Mirage Forces",Constants.REGION_FIRST_NATURE,20,0x0E),
    Mission(0x14,"Destroy Massive MT",Constants.REGION_FIRST_NATURE, 47,0x27),
    Mission(0x15, "Eliminate Infiltrators",Constants.REGION_THIRD_DISTRICT1,10,0x08),
    Mission(0x16, "Destroy Massive Weapon",Constants.REGION_FIRST_NATURE, 43,0x23),
    Mission(0x17, "Defend Energy Reactor", Constants.REGION_FOURTH_ENERGY, 46,0x26),
    Mission(0x18, "Eliminate Intruders",Constants.REGION_THIRD_DISTRICT1,14,0x0C),
    Mission(0x19, "Safeguard Alloy Sample",Constants.REGION_THIRD_DISTRICT1, 25,0x13),
    Mission(0x1A, "Destroy the AC", Constants.REGION_THIRD_DISTRICT1,18,0x0D), #Bonus Mission, Defend Personnel Convoy
    Mission(0x1B, "Defend the Monorail",Constants.REGION_THIRD_DISTRICT1, 11,0x06),
    Mission(0x1C, "Destroy Computer",Constants.REGION_THIRD_INDUSTRIAL,30,0x17),
    #Mission(0x1D, "",?,?,?), #The game crashes after trying to commence this "mission"
    Mission(0x1E, "Protect Crest Convoy",Constants.REGION_FIRST_SPECIAL, 40,0x20),
    Mission(0x1F, "Disable Radar Equipment",Constants.REGION_FIRST_SPECIAL,41,0x20),
    Mission(0x20, "End Employee Standoff",Constants.REGION_FIRST_DISTRICT2,2,0x01),
    Mission(0x21, "End Employee Rebellion",Constants.REGION_FIRST_DISTRICT2,6,0x05),
    Mission(0x22, "Recover Ship Cargo",Constants.REGION_FIRST_NATURE, 24,0x13),
    Mission(0x23, "Defend Helicopter Crew",Constants.REGION_FIRST_NATURE,16,0x0D),#Bonus Mission, Prevent Capsule Theft
    Mission(0x24, "Destroy Gun Emplacements",Constants.REGION_FIRST_SPECIAL, 32,0x19),
    Mission(0x25, "Recover Data Capsules",Constants.REGION_FIRST_SPECIAL,31,0x17),
    Mission(0x26, "Steal the Access Program",Constants.REGION_FOURTH_ENERGY,38,0x1F),
    Mission(0x27, "Infiltrate Rehito Lab",Constants.REGION_FOURTH_ENERGY, 45,0x25),
    Mission(0x28, "Bomb Disarmament", Constants.REGION_SECOND_WASTE,28,0x16),
    Mission(0x29, "Disable Pulse Generators", Constants.REGION_SECOND_WASTE ,39,0x1F),
    Mission(0x2A, "Defend Crest HQ", Constants.REGION_SECOND_WASTE, 42,0x22),
    Mission(0x2B, "Distract Union Defenses",Constants.REGION_FIRST_SPECIAL,33,0x19), #Bonus Mission, Destroy Gun Emplacements
    Mission(0x2C, "Safeguard Water Supply",Constants.REGION_THIRD_INDUSTRIAL,13,0x09),
    Mission(0x2D, "Disable Security System", Constants.REGION_SECOND_WASTE, 26,0x15),
    Mission(0x2E, "Assault Crest Facility", Constants.REGION_SECOND_WASTE,27,0x15),
    Mission(0x2F, "Destroy Germ Canisters",Constants.REGION_FIRST_SPECIAL,29,0x17),
    Mission(0x30, "MT Training Exercise",Constants.REGION_THIRD_INDUSTRIAL, 19,0x0E),
    Mission(0x31, "Investigate Magna Ruins",Constants.REGION_FOURTH_ENERGY,44,0x24),
    Mission(0x32, "Infiltrate Layered Hub", Constants.REGION_LAYERED_HUB,48,0x28),
)
progressive_mission = Mission(0x33, Constants.ITEM_PROGRESSIVE_MISSION_NAME, Constants.REGION_MISSION_LIST,0,0)

all_missions_by_order: typing.Tuple[Mission, ...] = tuple(sorted(all_missions, key=lambda mission: mission.mission_order))

STARTING_MISSION = all_missions[0]
FINAL_MISSION = all_missions[-1]

id_to_mission = {mission.id: mission for mission in all_missions}
name_to_mission = {mission.name: mission for mission in all_missions}
all_mission_ids = {mission.id for mission in all_missions}
