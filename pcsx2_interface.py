
from enum import Enum

from worlds.armoredcore3.mission import all_missions
from worlds.armoredcore3.pine import Pine
from worlds.armoredcore3.utils import Constants


class ConnectionStatus(Enum):
    WRONG_GAME = -1
    DISCONNECTED = 0
    CONNECTED = 1
    IN_GAME = 2


class AC3Interface:

    def __init__(self, logger, slot: int = 28011):
        self.logger = logger
        self.pine = Pine(slot)
        self.connected = False
        self.completed_missions = set()
        self.queued_credits: int =0

    def connect_game(self) -> None:
        try:
            self.pine.connect()
            game_id = self.pine.get_game_id()
            self.connected = (game_id == "SLUS-20435")
            if self.connected:
                print(f"Detected Game ID: {game_id}")
        except Exception as e:
            print(f"PCSX2 connection failed with error: {e}")
            self.connected = False

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.connected = False

    def check_completed_missions(self) -> None:
        for mission in all_missions:
            completed = self.pine.read_int8(mission.id + Constants.ADDR_MISSION_COMPLETION)
            if completed in (2, 6):
                self.completed_missions.add(mission.id+Constants.ADDR_MISSION_COMPLETION)

        # whatever your world calls it
    def unlock_part(self, part_id:int) -> None:
        self.pine.write_int8(part_id,0x01)

    def enforce_game_state(self) -> None:
        self.check_completed_missions()

def main():
    interface = AC3Interface
    interface.connect_game()
