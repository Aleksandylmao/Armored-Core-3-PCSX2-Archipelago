from typing import Dict, Tuple

from dataclasses import dataclass


class MissionRegion:
    name: str
    mission_list_addr: int
    list_length_addr: int
    def __init__(self, name: str, mission_list_addr: int,list_length_addr: int):
        self.name = name
        self.mission_list_addr = mission_list_addr
        self.list_length_addr = list_length_addr

@dataclass
class Constants:
    # Armored Core 3 constants
    GAME_NAME: str = "Armored Core 3"
    CLIENT_NAME: str = "Armored Core 3 Client"
    AC3_GAME_ID = "SLUS-20435"

    ITEM_PROGRESSIVE_MISSION_NAME ="Progressive Mission"
    UNLOCKS_PER_PROGRESSIVE_MISSION = 5
    ITEM_CREDIT_NAME: str = "Bonus Credits"
    ITEM_VICTORY:str = "Victory"

    REGION_MENU: str ="Menu"
    REGION_ARENA: str ="Arena Menu"
    REGION_MISSION_LIST: str ="Mission Menu"
    REGION_FIRST_DISTRICT2: str ="1st Layer: District 2"
    REGION_THIRD_INDUSTRIAL: str ="3rd Layer: Industrial Research"
    REGION_THIRD_DISTRICT1: str ="3rd Layer: District 1"
    REGION_FIRST_NATURE: str = "1st Layer: Nature Area"
    REGION_FIRST_SPECIAL: str = "1st Layer: Special Area"
    REGION_SECOND_WASTE: str = "2nd Layer: Waste Disposal"
    REGION_FOURTH_ENERGY: str = "4th Layer: Energy Production"
    REGION_LAYERED_HUB: str = "Layered Hub"
    all_regions: Tuple[str,...] = (
        REGION_MENU,
        REGION_ARENA,
        REGION_MISSION_LIST,
        REGION_FIRST_DISTRICT2,
        REGION_THIRD_INDUSTRIAL,
        REGION_THIRD_DISTRICT1,
        REGION_FIRST_NATURE,
        REGION_FIRST_SPECIAL,
        REGION_SECOND_WASTE,
        REGION_FOURTH_ENERGY,
        REGION_LAYERED_HUB,
    )
    ADDR_LOADING_ALL_MISSIONS: int = 0x5BE034
    ADDR_CURRENT_MENU: int = 0x5CB101
    ADDR_PREVIOUS_MENU:int = 0x5CB102
    ADDR_CREDITS: int = 0x5BE030
    ADDR_MAIL: int = 0x5BE0E0 #Bit 7 - Has been read
    ADDR_MISSION_COMPLETION : int = 0x5BE060
    ADDR_MISSION_RANK : int = 0x5BE0A0

    ADDR_INVENTORY: int = 0x5B2021 #value = how many times you own the part, useful for some back units
    ADDR_FUNC_DISABLE_SELL_ASSEMBLY_MENU: int = 0x002AE990 #Instruct those two function instantly return
    ADDR_FUNC_DISABLE_SELL_OPTIONAL_PART_MENU: int = 0x002B1E38 #Bytes: 03E00008 Instruction: jr ra
    INSTRUCTION_JR_RA: int = 0x03E00008
    #I was unable to figure out how to easily change the description of the shop items
    #The Strings get loaded from the disc and I don't know how to edit those on the disc
    #I can try to edit them before they get loaded into the ui but that would not be consistent
    #Therefore Shop Descriptions ain't implemented as of right now
    #ToDo: Shop Descriptions
    ADDR_SHOP: int = 0x5B2821   #same order as inventory; 0 = bought/not in shop; value > 0 times it can be bought
    ADDR_INSTR_DISABLE_ADDING_TO_INVENTORY: int = 0x002863AC #nop this
    #The shop item names have a max length of 18 characters
    OFFSET_SHOP_NAME: int = 0x18
    ADDR_SHOP_NAME_HEAD: int = 0x1344B34
    ADDR_SHOP_NAME_CORE: int = 0x1344E4C
    ADDR_SHOP_NAME_ARM: int = 0x1345164
    ADDR_SHOP_NAME_LEG: int = 0x134577C
    ADDR_SHOP_NAME_BOOSTER: int = 0x1345D94
    ADDR_SHOP_NAME_FCS: int = 0x13460AC
    ADDR_SHOP_NAME_GENERATOR: int = 0x13463C4
    ADDR_SHOP_NAME_RADIATOR: int = 0x13466DC
    ADDR_SHOP_NAME_INSIDE: int = 0x13469F4
    ADDR_SHOP_NAME_EXTENSION: int = 0x1346D0C
    ADDR_SHOP_NAME_BACK_UNIT: int = 0x1347024
    ADDR_SHOP_NAME_ARM_UNIT_R: int = 0x134763C
    ADDR_SHOP_NAME_ARM_UNIT_L: int = 0x1347C54
    ADDR_SHOP_NAME_OPTIONAL_PARTS: int = 0x1347F6C


    #You can probably do this way simpler. But I don't want to invest more time into finding better addresses or trying assembly, for now I will come back someday maybe idk
    #The Mission list and length addresses are rewritten to default values everytime you enter Mission from the Menu
    ADDR_MISSION_LIST_LAYERED_HUB: int = 0x19BC280
    ADDR_MISSION_LIST_FOURTH_ENERGY: int = 0x19BC380
    ADDR_MISSION_LIST_SECOND_WASTE: int = 0x19BC480
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

    MISSION_REGIONS: Tuple[MissionRegion, ...] =(
        MissionRegion(
            REGION_FIRST_DISTRICT2,
            ADDR_MISSION_LIST_FIRST_DISTRICT2,
            ADDR_LIST_LENGTH_FIRST_DISTRICT2,
        ),
        MissionRegion(
            REGION_THIRD_INDUSTRIAL,
            ADDR_MISSION_LIST_THIRD_INDUSTRIAL,
            ADDR_LIST_LENGTH_THIRD_INDUSTRIAL,
        ),
        MissionRegion(
            REGION_THIRD_DISTRICT1,
            ADDR_MISSION_LIST_THIRD_DISTRICT1,
            ADDR_LIST_LENGTH_THIRD_DISTRICT1,
        ),
        MissionRegion(
            REGION_FIRST_NATURE,
            ADDR_MISSION_LIST_FIRST_NATURE,
            ADDR_LIST_LENGTH_FIRST_NATURE,
        ),
        MissionRegion(
            REGION_FIRST_SPECIAL,
            ADDR_MISSION_LIST_FIRST_SPECIAL,
            ADDR_LIST_LENGTH_FIRST_SPECIAL,
        ),
        MissionRegion(
            REGION_SECOND_WASTE,
            ADDR_MISSION_LIST_SECOND_WASTE,
            ADDR_LIST_LENGTH_SECOND_WASTE,
        ),
        MissionRegion(
            REGION_FOURTH_ENERGY,
            ADDR_MISSION_LIST_FOURTH_ENERGY,
            ADDR_LIST_LENGTH_FOURTH_ENERGY,
        ),
        MissionRegion(
            REGION_LAYERED_HUB,
            ADDR_MISSION_LIST_LAYERED_HUB,
            ADDR_LIST_LENGTH_LAYERED_HUB,
        ),
    )

MISSION_REGIONS_BY_NAME: Dict[str, MissionRegion] = {mr.name: mr for mr in Constants.MISSION_REGIONS}
