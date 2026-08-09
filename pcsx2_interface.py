
from enum import Enum

from worlds.armoredcore3.mission import all_missions
from worlds.armoredcore3.pine import Pine
from worlds.armoredcore3.utils import Constants


class ConnectionStatus(Enum):
    DISCONNECTED = 0
    AC3_NOT_DETECTED = 1
    IN_GAME = 2


class AC3Interface:

    def __init__(self, logger, slot: int = 28011):
        self.logger = logger
        self.pine = Pine(slot)
        self.connected = False
        self.status = ConnectionStatus.DISCONNECTED
        self.completed_missions = set()
        self.queued_credits: int = 0

    def connect_game(self) -> ConnectionStatus:
        #Todo the pine.connect() method freezes the main window, if PCSX2 is not open.
        # It runs into a timeout set for the socket in pine. Idk how to fix it right now, will look into it at some point
        # simply because it annoys me, but hey its not breaking anything it's just annoying
        # workaround: open PCSX2
        try:
            self.pine.connect()
            if self.pine.is_connected():
                self.status = ConnectionStatus.AC3_NOT_DETECTED
            else:
                self.status = ConnectionStatus.DISCONNECTED
                return self.status
        except Exception as e:
            self.status = ConnectionStatus.DISCONNECTED
            return self.status

        return self.check_ac3_loaded()

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.status = ConnectionStatus.DISCONNECTED

    def check_completed_missions(self) -> None:
        for mission in all_missions:
            completed = self.pine.read_int8(mission.id + Constants.ADDR_MISSION_COMPLETION)
            if completed in (2, 6):
                self.completed_missions.add(mission.id+Constants.ADDR_MISSION_COMPLETION)


    def unlock_part(self, part_id:int) -> None:
        self.pine.write_int8(part_id,0x01)

    def enforce_game_state(self) -> None:
        self.check_completed_missions()

    def is_connected(self) -> bool:
        return self.status == ConnectionStatus.IN_GAME

    def check_ac3_loaded(self) -> ConnectionStatus:
        try:
            game_id = self.pine.get_game_id()

            if game_id == Constants.AC3_GAME_ID:
                self.status = ConnectionStatus.IN_GAME
            else:
                self.status = ConnectionStatus.AC3_NOT_DETECTED
            return self.status
        except Exception as e:
            self.status = ConnectionStatus.AC3_NOT_DETECTED
            return self.status
def main():
    interface = AC3Interface
    interface.connect_game()
