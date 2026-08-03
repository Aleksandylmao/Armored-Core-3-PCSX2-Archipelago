import typing

from dataclasses import dataclass

@dataclass
class Constants:
    # Armored Core 3 constants
    GAME_NAME: str = "Armored Core 3"
    CLIENT_NAME: str = "Armored Core 3 Client"
    AC3_GAME_ID = "SLUS-20435"

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

    ADDR_CURRENT_MENU: int = 0x5CB101
    ADDR_CREDITS: int = 0x5BE030
    ADDR_MISSION_COMPLETION : int = 0x5BE060
    ADDR_MISSION_RANK : int = 0x5BE0A0
    ADDR_INVENTORY: int = 0x5B2021 #value = how many times you own the part, useful for some back units
    ADDR_SHOP: int = 0x5B2821   #parts are in the same order as in inventory
                                #0 = bought/not in shop; value = times it can be bought; if you buy an Item it reduces the value by 1

    #You can probably do this way simpler. But I don't want to invest more time into finding better addresses or trying assembly, for now I will come back someday maybe idk
    #The Mission list and length addresses are rewritten to default values everytime you enter Mission from the Menu
    ADDR_MISSION_LIST_LAYERED_HUB: int = 0x19BC280
    ADDR_MISSION_LIST_FOURTH_ENERGY: int = 0x19BC380
    ADDR_MISSION_LIST_SECOND_WASTE: int = 0x19BC280
    ADDR_MISSION_LIST_FIRST_DISTRICT2: int = 0x19BC580
    ADDR_MISSION_LIST_THIRD_INDUSTRIAL: int = 0x19BC680
    ADDR_MISSION_LIST_FIRST_SPECIAL: int = 0x19BC780
    ADDR_MISSION_LIST_THIRD_DISTRICT1: int = 0x19BC880
    ADDR_MISSION_LIST_FIRST_NATURE: int = 0x19BC980

    ADDR_LIST_LENGTH_LAYERED_HUB: int = 0x19BC2AA
    ADDR_LIST_LENGTH_FOURTH_ENERGY: int = 0x19BC3AA
    ADDR_LIST_LENGTH_SECOND_WASTE: int = 0x19BC4AA
    ADDR_LIST_LENGTH_FIRST_DISTRICT2: int = 0x19BC5AA
    ADDR_LIST_LENGTH_THIRD_INDUSTRIAL: int = 0x19BC6AA
    ADDR_LIST_LENGTH_FIRST_SPECIAL: int = 0x19BC7AA
    ADDR_LIST_LENGTH_THIRD_DISTRICT1: int = 0x19BC8AA
    ADDR_LIST_LENGTH_FIRST_NATURE: int = 0x19BC9AA
