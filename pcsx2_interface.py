import asyncio
import time
from enum import Enum

from .locations import shop_location_name_to_id, get_location_id_for_mission_rank
from .mail import Mail
from .mission import all_missions, id_to_mission, STARTING_MISSION, all_ranks, all_mission_ids
from .parts import all_parts, all_part_list, all_part_ids
from .pine import Pine
from .utils import Constants, MISSION_REGIONS_BY_NAME, Menu, SHOP_TEXT_SAFE_CHARS


PURCHASE_GRACE_SECONDS = 3.0  # how long after leaving the shop a purchase is still accepted
OUTSIDE_MENU_GRACE_SECONDS = 2.0  # outside the shop the listings are only re-checked this often
PART_ID_SPAN = max(all_part_ids) + 1   # 0x350: the tables are indexed by part id


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
		self.last_in_shop: float = float("-inf")
		self.last_shop_sync: float = float("-inf")
		self.last_in_mail_menu: float = float("-inf")
		self.last_listed_count: int = -1
		self.shop_location_scouted: set[int] = set()
		self.watched_mails: set[Mail] = set()
		self.mail_locations_read: set[int] = set()

	async def connect_game_async(self) -> ConnectionStatus:
		return await asyncio.to_thread(self.connect_game)

	def connect_game(self) -> ConnectionStatus:
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

	def check_mails(self):

		now = time.monotonic()
		if self.in_menu(Menu.MAIL):
			self.last_in_mail_menu = now
		mail_read_possible = now - self.last_in_shop <= PURCHASE_GRACE_SECONDS

		if not self.sync_due(now, mail_read_possible):
			return

		pending_mails = [m for m in self.watched_mails
				   if Constants.ADDR_MAIL + m.id not in self.mail_locations_read]
		if not pending_mails:
			return

		flags = self.pine.read_bytes(Constants.ADDR_MAIL, max(m.id for m in pending_mails) + 1)
		for mail in pending_mails:
			if flags[mail.id] & Constants.MASK_MAIL_READ:
				self.mail_locations_read.add(Constants.ADDR_MAIL + mail.id)

	def write_story_progress(self):
		self.pine.write_int8_unsigned(Constants.ADDR_STORY_PROGRESSION, min(len(self.completed_missions), 0x28))

	def check_completed_missions(self) -> None:
		flags = self.pine.read_bytes(Constants.ADDR_MISSION_COMPLETION, max(all_mission_ids) + 1)
		for mission in all_missions:
			if flags[mission.id] in (2, 6):
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

		self.received_missions.update(mission_ids)
		wanted_region_mission_id = self.wanted_mission_lists()
		if self.mission_lists_intact(wanted_region_mission_id):
			return

		self.write_mission_lists(wanted_region_mission_id)

	def wanted_mission_lists(self) -> dict[str, list[int]]:
		lists: dict[str, list[int]] = {name: [] for name in MISSION_REGIONS_BY_NAME}
		for mission_id in sorted(self.received_missions):
			region_name = id_to_mission[mission_id].region
			if region_name in lists:
				lists[region_name].append(mission_id)
		return lists

	def mission_lists_intact(self, wanted: dict[str, list[int]]) -> bool:
		"""Cheap check, about 20 reads every tick.
		The game resets the lists to its defaults when the mission menu is entered"""
		# I could try to find the method that does this that would make this obselete and improves the performance
		if self.pine.read_int8_unsigned(Constants.ADDR_LOADING_ALL_MISSIONS) != 1:
			return False
		for name, ids in wanted.items():
			region = MISSION_REGIONS_BY_NAME[name]
			if self.pine.read_int8_unsigned(region.list_length_addr) != len(ids):
				return False
			if ids and self.pine.read_bytes(region.mission_list_addr, len(ids)) != bytes(ids):
				return False
		return True

	def write_mission_lists(self, wanted_region_mission_id: dict[str, list[int]]) -> None:
		self.pine.write_int8_unsigned(Constants.ADDR_LOADING_ALL_MISSIONS, 1)
		for name, ids in wanted_region_mission_id.items():
			region = MISSION_REGIONS_BY_NAME[name]
			if ids:
				self.pine.write_bytes(region.mission_list_addr, bytes(ids))
			self.pine.write_int8_unsigned(region.list_length_addr, len(ids))  # 0 for an empty region

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

		actual = self.read_part_table(Constants.ADDR_INVENTORY)
		for part in all_parts:
			part_addr = part.id + Constants.ADDR_INVENTORY
			wanted = 0x02 if part_addr in self.received_parts else 0
			if actual[part.id] != wanted:
				self.pine.write_int8_unsigned(part_addr, wanted)

	def disable_selling_parts(self) -> None:
		self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_OPTIONAL_PART_MENU, Constants.INSTRUCTION_JR_RA)
		self.pine.write_int32_unsigned(Constants.ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU, Constants.INSTRUCTION_JR_RA)
		self.pine.write_string(Constants.ADDR_TEXT_SELL, "NO")

	def disable_adding_parts_from_shop(self) -> None:
		self.pine.write_int32_unsigned(Constants.ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY, 0x0)

	def check_bought_parts(self) -> None:
		now = time.monotonic()
		if self.in_menu(Menu.GARAGE_SHOP):
			self.last_in_shop = now
		#A small time window is better than "one extra tick", I'M IMPROVING yay
		purchases_possible = now - self.last_in_shop <= PURCHASE_GRACE_SECONDS

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

	def sync_shop_listings(self) -> None:
		now = time.monotonic()
		if self.in_menu(Menu.GARAGE_SHOP):
			self.last_in_shop = now
		purchases_possible = now - self.last_in_shop <= PURCHASE_GRACE_SECONDS

		listed_count = len(self.completed_missions)
		if not self.shop_sync_due(now, purchases_possible, listed_count):
			return
		self.last_shop_sync = now
		self.last_listed_count = listed_count

		actual = self.read_part_table(Constants.ADDR_SHOP)
		end_index = min(listed_count * self.shop_listing_per_mission, len(all_parts))

		for index, part in enumerate(all_parts):
			location = Constants.ADDR_SHOP + part.id
			value = actual[part.id]

			if index >= end_index:
				wanted = 0  # not unlocked yet
			elif location in self.shop_locations_bought:
				wanted = 0  # already bought -> stays hidden
			elif location not in self.shop_location_added:
				wanted = 1  # unlocked
				self.shop_location_added.add(location)
			elif value == 0:
				# It was visible and is empty now, so the game removed it.
				if purchases_possible:
					self.shop_locations_bought.add(location)
					wanted = 0
				else:
					wanted = 1
			else:
				wanted = value  # visible and untouched, leave it alone

			if value != wanted:  # only touch the game when something is different
				self.pine.write_int8_unsigned(location, wanted)

	def shop_sync_due(self, now, in_shop_window, listed_count):
		return (self.sync_due(now,in_shop_window)
				or listed_count != self.last_listed_count) # a mission was completed


	def sync_due(self, now, in_shop_window):
		return in_shop_window or now - self.last_shop_sync >= OUTSIDE_MENU_GRACE_SECONDS

	def change_shop_part_name(self) -> None:
		if not self.in_menu(Menu.GARAGE_SHOP):
			return

		# 1. Where does each scouted name go and which bytes is it?
		names: dict[int, bytes] = {}  # address -> bytes
		addresses_by_category: dict[int, list[int]] = {}
		for part_list_index, part_list in enumerate(all_part_list):
			for part_index, part in enumerate(part_list):
				scouted = self.shop_scouted.get(part.id + Constants.ADDR_SHOP)
				if scouted is None:
					continue
				item_name, classification = scouted
				name_index = self.get_shop_name_index(part_list_index, part_index)
				address = Constants.LIST_SHOP_PART_NAMES[part_list_index] + (
							name_index * Constants.OFFSET_SHOP_NAME)
				names[address] = item_name[:Constants.MAX_PART_NAME_LENGTH].encode("ascii") + b"\x00"
				addresses_by_category.setdefault(part_list_index, []).append(address)

		# 2. Did the game overwrite our names? Check the first and last name of every category.
		# If one is different, forget the whole category so it gets written again below.
		for addresses in addresses_by_category.values():
			for address in (addresses[0], addresses[-1]):
				cached = self.shop_name_cache.get(address)
				if cached is not None and self.pine.read_bytes(address, len(cached)) != cached:
					for stale in addresses:
						self.shop_name_cache.pop(stale, None)
					break

		# 3. Write only the names that are new / were forgotten
		for address, data in names.items():
			if self.shop_name_cache.get(address) != data:
				self.pine.write_bytes(address, data)
				self.shop_name_cache[address] = data

	def get_shop_name_index(self, shop_index: int, part_index: int) -> int:
		if shop_index != 8: #What in the Magic Number did I do.. Anyway this is some part shop idk which one but it is...
			return part_index #If I remember right it could be the Arm or back unit weapons shop since there could be some filler
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

	def read_part_table(self, base: int) -> bytes:
		return self.pine.read_bytes(base, PART_ID_SPAN)  # result[part.id] = byte for that part

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
		self.write_story_progress()
		self.check_mails()
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
		self.mail_locations_read: set[int] = set()
		self.last_shop_sync = float("-inf")
		self.last_in_mail_menu = float("-inf")
		self.last_listed_count = -1

	def set_shop_scout_data(self, scouted: dict[int, tuple[str, str]]) -> None:
		self.shop_scouted.update(scouted)

	def set_previously_bought_shop_locations(self, checked_locations: set[int]) -> None:
		shop_location_ids = set(shop_location_name_to_id.values())
		self.shop_locations_bought = (checked_locations & shop_location_ids)

	@staticmethod
	def sanitize_for_ps2_display(text: str) -> str:
		cleaned = "".join(c if c in SHOP_TEXT_SAFE_CHARS else "?" for c in text)
		return cleaned