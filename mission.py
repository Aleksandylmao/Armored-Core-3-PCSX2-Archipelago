import typing

class Mission:
    id: int
    name: str

    def __init__(self, _id: int, name: str):
        self.id = _id
        self.name = name

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

all_ranks = {
    Mission(0x0, "E"),
    Mission(0x1, "D"),
    Mission(0x2, "C"),
    Mission(0x3, "B"),
    Mission(0x4, "A"),
    Mission(0x5, "S"),
}

all_missions: typing.Tuple[Mission, ...] = (
    Mission(0x1, "Raven Test"),
    Mission(0x2, "Defend Testing Grounds"),
    Mission(0x3, "Secure Trene City"),
    Mission(0x4, "Defend the Arena"),
    Mission(0x5, "Secure the Mine"),
    Mission(0x6, "Defend Personnel Convoy"),
    Mission(0x7, "Destroy Kisaragi Forces"),
    Mission(0x8, "Defend Naire Bridge"),
    Mission(0x9, "Destroy Naire Bridge"),
    Mission(0xA, "Destroy Escaping MT"),
    Mission(0xB, "Escort Transport"),
    Mission(0xC, "Rescue the Survey Team"),
    Mission(0xD, "Investigate Water Swells"),
    Mission(0xE, "Defend Water Processors"),
    Mission(0xF, "Prevent Capsule Theft"),
    Mission(0x10, "Defend Ruglem Laboratory"),
    Mission(0x11, "Eradicate Life Forms"),
    Mission(0x12, "Eliminate the Bombers"),
    Mission(0x13, "Attack Mirage Forces"),
    Mission(0x14,"Destroy Massive MT"),
    Mission(0x15, "Eliminate Infiltrators"),
    Mission(0x16, "Destroy Massive Weapon"),
    Mission(0x17, "Defend Energy Reactor"),
    Mission(0x18, "Eliminate Intruders"),
    Mission(0x19, "Safeguard Alloy Sample"),
    Mission(0x1A, "Destroy the AC"),
    Mission(0x1B, "Defend the Monorail"),
    Mission(0x1C, "Destroy Computer"),
    #Mission(0x1D, ""), #The game crashes after commencing this mission
    Mission(0x1E, "Protect Crest Convoy"),
    Mission(0x1F, "Disable Radar Equipment"),
    Mission(0x20, "End Employee Standoff"),
    Mission(0x21, "End Employee Rebellion"),
    Mission(0x22, "Recover Ship Cargo"),
    Mission(0x23, "Defend Helicopter Crew"),
    Mission(0x24, "Destroy Gun Emplacements"),
    Mission(0x25, "Recover Data Capsules"),
    Mission(0x26, "Steal the Access Program"),
    Mission(0x27, "Infiltrate Rehito Lab"),
    Mission(0x28, "Bomb Disarmament" ),
    Mission(0x29, "Disable Pulse Generators" ),
    Mission(0x2A, "Defend Crest HQ" ),
    Mission(0x2B, "Distract Union Defenses"),
    Mission(0x2C, "Safeguard Water Supply"),
    Mission(0x2D, "Disable Security System" ),
    Mission(0x2E, "Assault Crest Facility" ),
    Mission(0x2F, "Destroy Germ Canisters"),
    Mission(0x30, "MT Training Exercise"),
    Mission(0x31, "Investigate Magna Ruins"),
    Mission(0x32, "Infiltrate Layered Hub"),
)

STARTING_MISSION = all_missions[0]
id_to_mission = {mission.id: mission for mission in all_missions}
name_to_mission = {mission.name: mission for mission in all_missions}