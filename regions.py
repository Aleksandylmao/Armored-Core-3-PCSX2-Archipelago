from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region
from .utils import Constants

if TYPE_CHECKING:
    from .world import AC3World


def create_and_connect_regions(world: AC3World) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: AC3World) -> None:
    menu = Region(Constants.REGION_MENU, world.player, world.multiworld)
    arena = Region(Constants.REGION_ARENA, world.player, world.multiworld)
    mission_list = Region(Constants.REGION_MISSION_LIST, world.player, world.multiworld)
    first_layer_district2 = Region(Constants.REGION_FIRST_DISTRICT2, world.player, world.multiworld)
    third_layer_industrial_research  = Region(Constants.REGION_THIRD_INDUSTRIAL, world.player, world.multiworld)
    third_layer_district1 = Region(Constants.REGION_THIRD_DISTRICT1, world.player, world.multiworld)
    first_layer_nature_area = Region(Constants.REGION_FIRST_NATURE, world.player, world.multiworld)
    first_layer_special_research= Region(Constants.REGION_FIRST_SPECIAL, world.player, world.multiworld)
    second_layer_waste_disposal = Region(Constants.REGION_SECOND_WASTE, world.player, world.multiworld)
    fourth_layer_energy_production = Region(Constants.REGION_FOURTH_ENERGY, world.player, world.multiworld)
    layered_hub = Region(Constants.REGION_LAYERED_HUB, world.player, world.multiworld)

    regions = [menu,arena,mission_list,first_layer_district2,third_layer_industrial_research,third_layer_district1,
               first_layer_nature_area,first_layer_special_research,second_layer_waste_disposal,
               fourth_layer_energy_production,layered_hub]
    world.multiworld.regions += regions

def connect_regions(world: AC3World) -> None:
    menu = world.get_region(Constants.REGION_MENU)

    for region in world.get_regions():
        if region != menu:
            menu.connect(region, get_region_connection_name(menu.name, region.name))

def get_region_connection_name(region1: str, region2: str) -> str:
    return f"{region1} to {region2}"