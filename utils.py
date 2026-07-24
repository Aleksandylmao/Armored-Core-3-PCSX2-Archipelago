import typing

from dataclasses import dataclass

@dataclass
class Constants:
    # Armored Core 3 constants
    GAME_NAME: str = "Armored Core 3"

    CREDIT_ITEM_NAME: str = "Bonus Credits"
    #ToDo just do a region list or something like that
    REGION_MENU: str ="Menu"
    REGION_ARENA: str ="Arena"
    REGION_MISSION_LIST: str ="Mission List"
    REGION_FIRST_DISTRICT2: str ="1st Layer: District 2"
    REGION_THIRD_INDUSTRIAL: str ="3rd Layer: Industrial Research"
    REGION_THIRD_DISTRICT1: str ="3rd Layer: District 1"
    REGION_FIRST_NATURE: str = "1st Layer: Nature Area"
    REGION_FIRST_SPECIAL: str = "1st Layer: Special Area"
    REGION_SECOND_WASTE: str = "2nd Layer: Waste Disposal"
    REGION_FOURTH_ENERGY: str = "4th Layer: Energy Production"
    REGION_LAYERED_HUB: str = "Layered Hub"

    ADDR_CREDITS: int = 0x5BE030
    ADDR_MISSION_COMPLETION : int = 0x5BE061
    ADDR_MISSION_RANK : int = 0x5BE0A1
    ADDR_INVENTORY: int = 0x5b2021 #value = how many times you own the part, useful for some back units
    ADDR_SHOP: int = 0x5b2821   #parts are in the same order as in inventory ToDo further testing
                                #0 = bought/not in shop; value = times it can be bought; if you buy an Item it reduces the value by 1





#Not needed anymore, will get deleted after I tested most stuff
#    ADDR_INVENTORY_HEAD :int = 0x5b2021
#    ADDR_INVENTORY_CORE :int = 0x5b2061
#    ADDR_INVENTORY_ARMS:int = 0x5b20a1
#    ADDR_INVENTORY_LEGS :int = 0x5b20e1
#    ADDR_INVENTORY_BOOSTER: int = 0x5b2121
#    ADDR_INVENTORY_FCS: int = 0x5b2161
#    ADDR_INVENTORY_GENERATOR: int = 0x5b21a1
#    ADDR_INVENTORY_RADIATOR: int = 0x5b21e1
#    ADDR_INVENTORY_INSIDE: int = 0x5b2221
#    ADDR_INVENTORY_EXTENSIONS: int = 0x5b2261
#    ADDR_INVENTORY_BACK: int = 0x5b22a1
#    ADDR_INVENTORY_ARM_R: int = 0x5b22e1
#    ADDR_INVENTORY_ARM_L: int = 0x5b2321
#    ADDR_INVENTORY_OPTIONALS: int = 0x5b2361
