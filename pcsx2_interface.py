from enum import Enum

from .mission import all_missions, id_to_mission, STARTING_MISSION
from .parts import all_parts
from .pine import Pine
from .utils import Constants, MISSION_REGIONS_BY_NAME
from ..factorio.Technologies import unlock


class ConnectionStatus(Enum):
    DISCONNECTED = 0
    AC3_NOT_DETECTED = 1
    IN_GAME = 2


class AC3Interface:

    def __init__(self, slot: int = 28011):
        self.pine = Pine(slot)
        self.connected = False
        self.status = ConnectionStatus.DISCONNECTED
        self.completed_missions = set()
        self.received_missions: set[int] = set()
        self.received_parts: list[int] = []
        self.queued_credits: int = 0
        self.parts_shuffle: bool = False
        self.shop_sanity: bool = False

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
                self.disconnected()
                return self.status
        except Exception as e:
            self.status = ConnectionStatus.DISCONNECTED
            self.disconnected()
            return self.status

        return self.check_ac3_loaded()

    def check_ac3_loaded(self) -> ConnectionStatus:
        try:
            game_id = self.pine.get_game_id()

            if game_id == Constants.AC3_GAME_ID:
                self.status = ConnectionStatus.IN_GAME
            else:
                self.status = ConnectionStatus.AC3_NOT_DETECTED
                self.disconnected()
            return self.status
        except Exception as e:
            self.disconnected()
            self.status = ConnectionStatus.AC3_NOT_DETECTED
            return self.status

    def disconnect_game(self) -> None:
        self.pine.disconnect()
        self.status = ConnectionStatus.DISCONNECTED
        self.disconnected()

    def check_completed_missions(self) -> None:
        for mission in all_missions:
            completed = self.pine.read_int8_unsigned(mission.id + Constants.ADDR_MISSION_COMPLETION)
            if completed in (2, 6):
                self.completed_missions.add(mission.id+Constants.ADDR_MISSION_COMPLETION)

    def unlock_mission(self, mission_ids: list[int]) -> None:
        if not mission_ids and not self.received_missions:
            return

        counts = {name: 0 for name in MISSION_REGIONS_BY_NAME}
        self.received_missions.update(mission_ids)
        self.pine.write_int8_unsigned(Constants.ADDR_LOADING_ALL_MISSIONS,1)
        for mission_id in self.received_missions:
            mission = id_to_mission[mission_id]
            region = MISSION_REGIONS_BY_NAME.get(mission.region)
            if region is None:
                continue
            counts[mission.region] += 1
            slot = counts[mission.region]

            self.pine.write_int8_unsigned(region.mission_list_addr + slot - 1, mission_id)
            self.pine.write_int8_unsigned(region.list_length_addr, slot)

        for name, region in MISSION_REGIONS_BY_NAME.items():
            if counts[name] == 0:
                self.pine.write_int8_unsigned(region.list_length_addr, 0x00)

    def apply_credits(self) -> None:
        if self.queued_credits == 0:
            return
        if (self.pine.read_int8_signed(Constants.ADDR_CURRENT_MENU) != 0 #Garage/Default Menu ID
                and self.pine.read_int8_signed(Constants.ADDR_MISSION_COMPLETION+ STARTING_MISSION.id) == 0): #Ravens test must be completed otherwise you are not ingame
            return

        credit = self.queued_credits
        self.queued_credits = 0
        credit += self.pine.read_int32_signed(Constants.ADDR_CREDITS)
        self.pine.write_int32_signed(Constants.ADDR_CREDITS, credit)

    def unlock_parts(self) -> None:
        if self.parts_shuffle or self.shop_sanity:
            for part in all_parts:
                part_addr = part.id + Constants.ADDR_INVENTORY
                amount: int = 0
                if part_addr in self.received_parts:
                    amount = self.received_parts.count(part_addr)

                self.pine.write_int8_unsigned(part_addr, amount)

    def disable_selling_parts(self) -> None:
        if  self.parts_shuffle or self.shop_sanity:
            self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_OPTIONAL_PART_MENU, Constants.INSTRUCTION_JR_RA)
            self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU, Constants.INSTRUCTION_JR_RA)

    def disable_adding_parts_from_shop(self) -> None:
        if self.shop_sanity:
            self.pine.write_int32_unsigned(Constants.ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY,0x00000000)

    def enforce_game_state(self) -> None:
        self.check_completed_missions()
        self.apply_credits()
        self.disable_selling_parts()
        self.disable_adding_parts_from_shop()

    def is_connected(self) -> bool:
        return self.status == ConnectionStatus.IN_GAME

    def disconnected(self) -> None:
        self.connected = False
        self.status = ConnectionStatus.DISCONNECTED
        self.completed_missions = set()
        self.received_missions: set[int] = set()
        self.received_parts: list[int] = []
        self.queued_credits: int = 0
        self.parts_shuffle: bool = False