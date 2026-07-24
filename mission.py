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
    Mission(0x0, "Raven Test"),
    Mission(0x1, "Defend Testing Grounds"),
    Mission(0x2, "Secure Trene City"),
    Mission(0x3, "Defend the Arena"),
    Mission(0x4, "Secure the Mine"),
    Mission(0x5, "Defend Personnel Convoy"),
    Mission(0x6, "Destroy Kisaragi Forces"),
    Mission(0x7, "Defend Naire Bridge"),
    Mission(0x8, "Destroy Naire Bridge"),
    Mission(0x9, "Destroy Escaping MT"),
    Mission(0xA, "Escort Transport"),
    Mission(0xB, "Rescue the Survey Team"),
    Mission(0xC, "Investigate Water Swells"),
    Mission(0xD, "Defend Water Processors"),
    Mission(0xE, "Prevent Capsule Theft"),
    Mission(0xF, "Defend Ruglem Laboratory"),
    Mission(0x10, "Eradicate Life Forms"),
    Mission(0x11, "Eliminate the Bombers"),
    Mission(0x12, "Attack Mirage Forces"),
    Mission(0x13,"Destroy Massive MT"),
    Mission(0x14, "Eliminate Infiltrators"),
    Mission(0x15, "Destroy Massive Weapon"),
    Mission(0x16, "Defend Energy Reactor"),
    Mission(0x17, "Eliminate Intruders"),
    Mission(0x18, "Safeguard Alloy Sample"),
    Mission(0x19, "Destroy the AC"),
    Mission(0x1A, "Defend the Monorail"),
    Mission(0x1B, "Destroy Computer"),
    #Mission(0x1C, ""), #idk what here could be
    Mission(0x1D, "Protect Crest Convoy"),
    Mission(0x1E, "Disable Radar Equipment"),
    Mission(0x1F, "End Employee Standoff"),
    Mission(0x20, "End Employee Rebellion"),
    Mission(0x21, "Recover Ship Cargo"),
    Mission(0x22, "Defend Helicopter Crew"),
    Mission(0x23, "Destroy Gun Emplacements"),
    Mission(0x24, "Recover Data Capsules"),
    Mission(0x25, "Steal the Access Program"),
    Mission(0x26, "Infiltrate Rehito Lab"),
    Mission(0x27, "Bomb Disarmament" ),
    Mission(0x28, "Disable Pulse Generators" ),
    Mission(0x29, "Defend Crest HQ" ),
    Mission(0x2A, "Distract Union Defenses"),
    Mission(0x2B, "Safeguard Water Supply"),
    Mission(0x2C, "Disable Security System" ),
    Mission(0x2D, "Assault Crest Facility" ),
    Mission(0x2E, "Destroy Germ Canisters"),
    Mission(0x2F, "MT Training Exercise"),
    Mission(0x30, "Investigate Magna Ruins"),
    Mission(0x31, "Infiltrate Layered Hub"),
)

STARTING_MISSION = all_missions[0]
id_to_mission = {mission.id: mission for mission in all_missions}
name_to_mission = {mission.name: mission for mission in all_missions}