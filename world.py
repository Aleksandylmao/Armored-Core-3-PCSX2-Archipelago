from collections.abc import Mapping
from typing import Any
from worlds.AutoWorld import World
from . import items, locations, regions, rules, web_world
from .options import AC3Options
from .utils import Constants

class AC3World(World):
	"""
	Armored Core 3 is a 2002 third-person shooter video game developed by FromSoftware for the PlayStation 2.
	It is the sixth entry in the Armored Core series.
	"""

	game = Constants.GAME_NAME
	web = web_world.AC3Web()
	options_dataclass = AC3Options
	location_name_to_id = locations.LOCATION_NAME_TO_ID
	item_name_to_id = items.ITEM_NAME_TO_ID

	origin_region_name = Constants.REGION_MENU

	def create_regions(self) -> None:
		regions.create_and_connect_regions(self)
		locations.create_all_locations(self)

	def set_rules(self) -> None:
		rules.set_all_rules(self)

	def create_items(self) -> None:
		items.create_all_items(self)

	def create_item(self, name: str) -> items.AC3Item:
		return items.create_item_with_correct_classification(self, name)

	def get_filler_item_name(self) -> str:
		return Constants.CREDIT_ITEM_NAME

	def fill_slot_data(self) -> Mapping[str, Any]:
		return self.options.as_dict(
			"include_op_intensify"
		)