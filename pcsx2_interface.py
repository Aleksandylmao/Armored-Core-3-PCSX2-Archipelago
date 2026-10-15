import asyncio
from enum import Enum

from .locations import shop_location_name_to_id, get_location_id_for_mission_rank
from .mission import all_missions, id_to_mission, STARTING_MISSION, all_ranks
from .parts import all_parts, all_part_list
from .pine import Pine
from .utils import Constants, MISSION_REGIONS_BY_NAME, Menu, SHOP_TEXT_SAFE_CHARS


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
		self.completed_mission_ranks: set[int] = set()
		self.received_parts: set[int] =  set()
		self.queued_credits: int = 0
		self.shop_sanity: bool = False
		self.shop_locations_bought: set[int] = set()
		self.shop_location_added: set[int] = set()
		self.shop_listing_per_mission: int = 5 #default value
		self.shop_scouted: dict[int, tuple[str, str]] = {}
		self.current_menu_value: int = 0
		self.was_in_shop: bool = False
		self.shop_location_scouted: set[int] = set()

	async def connect_game_async(self) -> ConnectionStatus:
		return await asyncio.to_thread(self.connect_game)

	def connect_game(self) -> ConnectionStatus:
		# Todo the pine.connect() method freezes the main window, if PCSX2 is not open.
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

	def disconnect_game(self) -> None:
		self.pine.disconnect()
		self.status = ConnectionStatus.DISCONNECTED

	def check_completed_missions(self) -> None:
		for mission in all_missions:
			completed = self.pine.read_int8_unsigned(mission.id + Constants.ADDR_MISSION_COMPLETION)
			if completed in (2, 6):
				self.completed_missions.add(mission.id + Constants.ADDR_MISSION_COMPLETION)

	def check_mission_ranks(self) -> None:
		# Missions must be completed otherwise all rank E location would be sent out.
		for mission in all_missions:
			achieved = self.pine.read_int8_unsigned(mission.id + Constants.ADDR_MISSION_RANK)
			if not mission.id + Constants.ADDR_MISSION_COMPLETION in self.completed_missions:
				continue
			for rank in all_ranks:
				if rank.id <= achieved:
					self.completed_mission_ranks.add(get_location_id_for_mission_rank(mission, rank))

	def unlock_mission(self, mission_ids: list[int]) -> None:
		if not mission_ids and not self.received_missions:
			return

		counts = {name: 0 for name in MISSION_REGIONS_BY_NAME}
		self.received_missions.update(mission_ids)
		self.pine.write_int8_unsigned(Constants.ADDR_LOADING_ALL_MISSIONS, 1)
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

		credit = self.queued_credits
		credit += self.pine.read_int32_signed(Constants.ADDR_CREDITS)
		self.pine.write_int32_signed(Constants.ADDR_CREDITS, credit)
		self.queued_credits = 0

	def unlock_parts(self) -> None:
		if not self.in_menu(Menu.GARAGE_ASSEMBLY):
			return

		for part in all_parts:
			part_addr = part.id + Constants.ADDR_INVENTORY
			amount: int = 0x02  # 0 if I want to implement a setting to receive parts individual
			if part_addr in self.received_parts:
				self.pine.write_int8_unsigned(part_addr, amount)
			#	amount = self.received_parts.count(part_addr)
			else:
				self.pine.write_int8_unsigned(part_addr, 0)

	def disable_selling_parts(self) -> None:
		self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_OPTIONAL_PART_MENU, Constants.INSTRUCTION_JR_RA)
		self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU, Constants.INSTRUCTION_JR_RA)
		self.pine.write_string(Constants.ADDR_TEXT_SELL, "NO")

	def disable_adding_parts_from_shop(self) -> None:
		self.pine.write_int32_unsigned(Constants.ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY, 0x0)

	def check_bought_parts(self) -> None:
		in_shop = self.in_menu(Menu.GARAGE_SHOP)
		purchases_possible = in_shop or self.was_in_shop #one extra tick just to be safe
		self.was_in_shop = in_shop

		count = len(self.completed_missions)
		start_index = 0
		end_index = min(count * self.shop_listing_per_mission, len(all_parts))
		for part in all_parts[start_index:end_index]:
			if part.name == "DUMMY":
				continue
			location = part.id + Constants.ADDR_SHOP
			if location in self.shop_location_added and not location in self.shop_locations_bought:
				if self.pine.read_int8_signed(location) == 0x0:
					if purchases_possible:
						self.shop_locations_bought.add(location)
					else:
						self.pine.write_int8_unsigned(location, 0x1)

	def unlock_shop_parts(self) -> None:
		count = len(self.completed_missions)
		start_index = 0
		end_index = min(count * self.shop_listing_per_mission, len(all_parts))
		for part in all_parts[start_index:end_index]:
			if not Constants.ADDR_SHOP + part.id in self.shop_location_added and not part.id + Constants.ADDR_SHOP in self.shop_locations_bought:
				self.pine.write_int8_unsigned(Constants.ADDR_SHOP + part.id, 0x01)
				self.shop_location_added.add(part.id + Constants.ADDR_SHOP)
			elif part.id + Constants.ADDR_SHOP in self.shop_locations_bought:
				self.pine.write_int8_unsigned(Constants.ADDR_SHOP + part.id, 0x0)

		for part in all_parts[end_index:len(all_parts)]:
			self.pine.write_int8_unsigned(Constants.ADDR_SHOP + part.id, 0x0)

	def change_shop_part_name(self) -> None:
		if not self.in_menu(Menu.GARAGE_SHOP):
			return
		for part_list_index in range(len(all_part_list)):
			for part_index in range(len(all_part_list[part_list_index])):
				scouted = self.shop_scouted.get(all_part_list[part_list_index][part_index].id + Constants.ADDR_SHOP)
				if scouted is None:
					continue
				name_index = self.get_shop_name_index(part_list_index, part_index)
				item_name, classification = scouted
				address = Constants.LIST_SHOP_PART_NAMES[part_list_index] + (name_index * Constants.OFFSET_SHOP_NAME)
				self.pine.write_string(address, item_name[:Constants.MAX_PART_NAME_LENGTH])

	def get_shop_name_index(self, shop_index: int, part_index: int) -> int:
		if shop_index != 8: #What in the Magic Number did I do.. Anyway this is some part shop idk which one but it is...
			return part_index
		return part_index + 2 if part_index >= 6 else part_index

	def change_shop_part_description(self) -> None:
		if not self.in_menu(Menu.GARAGE_SHOP):
			return
		# Check to see if a Shop {part} menu was truly entered
		sum_of_parts_in_the_shop: int = self.pine.read_int8_unsigned(Constants.ADDR_SUM_OF_DISPLAYED_PARTS)
		if sum_of_parts_in_the_shop == 0:
			return

		part_id  = self.resolve_currently_viewed_part()
		if part_id is None:
			return
		location_id = part_id + Constants.ADDR_SHOP
		scouted = self.shop_scouted.get(location_id)
		if scouted is None:
			return
		item_name, classification = scouted
		text = f"[{classification}]: {item_name}"
		self.pine.write_string(Constants.ADDR_PART_DESCRIPTION, text[:Constants.MAX_DESCRIPTION_TEXT_LENGTH])

	def resolve_currently_viewed_part(self) -> int | None:
		shop_index: int = self.pine.read_int8_unsigned(Constants.ADDR_INDEX_CURRENT_SHOP_PART_MENU)
		if shop_index >= len(all_part_list):
			return None

		current_menu_part_list = all_part_list[shop_index]

		part_in_shop: list[int] = []
		for part in current_menu_part_list:
			if part.id + Constants.ADDR_SHOP in self.shop_location_added:
				if not part.id + Constants.ADDR_SHOP in self.shop_locations_bought:
					part_in_shop.append(part.id)

		if not part_in_shop:
			return None
		selected_part_index: int = self.pine.read_int8_unsigned(Constants.ADDR_INDEX_SHOP_SELECTED_PART)

		if selected_part_index >= len(part_in_shop):
			return None

		return part_in_shop[selected_part_index]

	def read_current_menu_value(self):
		self.current_menu_value = self.pine.read_int8_unsigned(Constants.ADDR_CURRENT_MENU)

	def in_menu(self, menu: Menu) -> bool:
		return self.current_menu_value == menu.value

	def raven_test_not_completed(self) -> bool:
		return self.in_menu(Menu.GARAGE_DEFAULT) and self.pine.read_int8_signed(Constants.ADDR_MISSION_COMPLETION + STARTING_MISSION.id) == 0  # Ravens test must be completed otherwise you are not ingame

	def enforce_game_state(self) -> None:
		self.read_current_menu_value()

		if self.raven_test_not_completed(): # this means ingame need to find a better check...
			return

		self.check_completed_missions()
		#self.check_mission_ranks()
		self.apply_credits()
		# Shop sanity
		if self.shop_sanity:
			self.unlock_parts()
			self.check_bought_parts()
			self.unlock_shop_parts()
			self.change_shop_part_description()
			self.change_shop_part_name()
			if not self.patches_applied():
				self.disable_selling_parts()
				self.disable_adding_parts_from_shop()

	def patches_applied(self) -> bool:
		return (self.pine.read_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU) == Constants.INSTRUCTION_JR_RA
            and self.pine.read_int32_unsigned(Constants.ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY) == 0x0)

	def is_connected(self) -> bool:
		return self.status == ConnectionStatus.IN_GAME

	def default_variables_values(self) -> None:
		self.connected = False
		self.completed_missions = set()
		self.completed_mission_ranks = set()
		self.received_missions: set[int] = set()
		self.received_parts: set[int] = set()
		self.queued_credits: int = 0
		self.shop_sanity: bool = False
		self.shop_locations_bought: set[int] = set()
		self.shop_location_added: set[int] = set()
		self.shop_scouted: dict[int, tuple[str, str]] = {}
		self.shop_listing_per_mission: int = 5
		self.shop_location_scouted: set[int] = set()

	def set_shop_scout_data(self, scouted: dict[int, tuple[str, str]]) -> None:
		self.shop_scouted.update(scouted)

	def set_previously_bought_shop_locations(self, checked_locations: set[int]) -> None:
		shop_location_ids = set(shop_location_name_to_id.values())
		self.shop_locations_bought = (checked_locations & shop_location_ids)

	@staticmethod
	def sanitize_for_ps2_display(text: str) -> str:
		cleaned = "".join(c if c in SHOP_TEXT_SAFE_CHARS else "?" for c in text)
		return cleaned