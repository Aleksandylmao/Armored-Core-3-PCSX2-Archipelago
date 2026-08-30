from enum import Enum

from .mission import all_missions, id_to_mission, STARTING_MISSION
from .parts import all_parts, all_heads, Part, all_part_list
from .pine import Pine
from .utils import Constants, MISSION_REGIONS_BY_NAME, Menu

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
        self.shop_part_bought: set[int] = set()
        self.shop_part_added: list[int] = []
        self.shop_listing_per_mission: int = 5
        self.shop_scouted: dict[int, tuple[str, str]] ={}
        self.current_menu_value: int = 0

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
        if self.in_menu(Menu.MISSION):
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
        if (self.in_menu(Menu.GARAGE_DEFAULT)
                and self.pine.read_int8_signed(Constants.ADDR_MISSION_COMPLETION+ STARTING_MISSION.id) == 0): #Ravens test must be completed otherwise you are not ingame
            return

        credit = self.queued_credits
        self.queued_credits = 0
        credit += self.pine.read_int32_signed(Constants.ADDR_CREDITS)
        self.pine.write_int32_signed(Constants.ADDR_CREDITS, credit)

    def unlock_parts(self) -> None:
        if not self.in_menu(Menu.GARAGE_ASSEMBLY):
            return

        for part in all_parts:
            part_addr = part.id + Constants.ADDR_INVENTORY
            amount: int = 0
            if part_addr in self.received_parts:
                amount = self.received_parts.count(part_addr)

            self.pine.write_int8_unsigned(part_addr, amount)

    def disable_selling_parts(self) -> None:
        self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_OPTIONAL_PART_MENU, Constants.INSTRUCTION_JR_RA)
        self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU, Constants.INSTRUCTION_JR_RA)

    def disable_adding_parts_from_shop(self) -> None:
        self.pine.write_int32_unsigned(Constants.ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY,0x00000000)

    def check_bought_parts(self) -> None:
        count = len(self.completed_missions)
        start_index = 0
        end_index = min(count * self.shop_listing_per_mission, len(all_parts))
        for part in all_parts[start_index:end_index]:
            if part.id in self.shop_part_added and not part.id + Constants.ADDR_SHOP in self.shop_part_bought:
                if self.pine.read_int8_signed(Constants.ADDR_SHOP+part.id) == 0x00:
                    self.shop_part_bought.add(part.id + Constants.ADDR_SHOP)
                    print(part.id, part.name)
                    
    def unlock_shop_parts(self) -> None:
        count = len(self.completed_missions)
        start_index = 0
        end_index = min(count* self.shop_listing_per_mission, len(all_parts))
        for part in all_parts[start_index:end_index]:
            if not part.id in self.shop_part_added and not part.id + Constants.ADDR_SHOP in self.shop_part_bought:
                self.pine.write_int8_unsigned(Constants.ADDR_SHOP+part.id,0x01)
                self.shop_part_added.append(part.id)
                print("part has been added to shop")
                print(part.id, part.name)
            elif part.id + Constants.ADDR_SHOP in self.shop_part_bought:
                self.pine.write_int8_unsigned(Constants.ADDR_SHOP+part.id,0x0)

        for part in all_parts[end_index:len(all_parts)]:
            self.pine.write_int8_unsigned(Constants.ADDR_SHOP+part.id,0x0)

    def change_shop_part_name(self) ->None:
        if not self.in_menu(Menu.GARAGE_SHOP):
            return
        for part_list_index in range(len(all_part_list)):
            for part_index in range(len(all_part_list[part_list_index])):
                scouted = self.shop_scouted.get(all_part_list[part_list_index][part_index].id+Constants.ADDR_SHOP)
                if scouted is None:
                    continue
                item_name, classification = scouted
                text = f"[{item_name}]"[:18]
                address = Constants.LIST_SHOP_PART_NAMES[part_list_index] + (part_index* Constants.OFFSET_SHOP_NAME)
                self.pine.write_string(address,text)

    def change_shop_part_description(self) ->None:
        if not self.in_menu(Menu.GARAGE_SHOP):
            return
        #Check to see if a Shop {part} menu was truly entered
        sum_of_parts_in_the_shop: int = self.pine.read_int8_unsigned(Constants.ADDR_SUM_OF_DISPLAYED_PARTS)
        if sum_of_parts_in_the_shop == 0:
            return
        location_id: int = self.resolve_currently_viewed_part() + Constants.ADDR_SHOP
        scouted = self.shop_scouted.get(location_id)
        if scouted is None:
            return
        print(location_id)
        item_name, classification = scouted
        text = f"[{classification}]: {item_name}"
        self.pine.write_string(Constants.ADDR_PART_DESCRIPTION, text)

    def resolve_currently_viewed_part(self) -> int:
        shop_index: int = self.pine.read_int8_unsigned(Constants.ADDR_INDEX_CURRENT_SHOP_PART_MENU)
        current_menu_part_list = all_part_list[shop_index]
        part_in_shop: list[int] = []
        for shop_part in self.shop_part_added:
            for part in current_menu_part_list:
                if shop_part == part.id and not part.id + Constants.ADDR_SHOP in self.shop_part_bought:
                    part_in_shop.append(shop_part)

        if not part_in_shop:
            return 0
        selected_part_index: int = self.pine.read_int8_unsigned(Constants.ADDR_INDEX_SHOP_SELECTED_PART)
        selected_part_id = part_in_shop[selected_part_index]
        return selected_part_id

    def read_current_menu_value(self):
        self.current_menu_value = self.pine.read_int8_unsigned(Constants.ADDR_CURRENT_MENU)

    def in_menu(self, menu: Menu) -> bool:
        return self.current_menu_value == menu.value

    def enforce_game_state(self) -> None:
        self.read_current_menu_value()

        self.check_completed_missions()
        self.apply_credits()

        #Shop sanity
        if self.shop_sanity:
            self.disable_selling_parts()
            self.disable_adding_parts_from_shop()
            self.unlock_shop_parts()
            self.check_bought_parts()
            self.change_shop_part_description()
            self.change_shop_part_name()

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

    def set_shop_scout_data(self, scouted: dict[int, tuple[str, str]]) -> None:
        self.shop_scouted = scouted