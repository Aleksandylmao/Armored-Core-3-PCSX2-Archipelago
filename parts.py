import typing

class Part:
	id: int
	name: str

	def __init__(self, _id: int, name: str):
		self.id = _id
		self.name = name


class Head(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)
all_heads: typing.Tuple[Head, ...] = (
	Head(0x000, "CDH-01-ATE"),
	Head(0x001, "MHD-MM/003"),
	Head(0x002, "CHD-04-YIV"),
	Head(0x003, "MHD-RE/005"),
	Head(0x004, "MHD-RE/008"),
	Head(0x005, "CHD-06-0VE"),
	Head(0x006, "CHD-02-TIE"),
	Head(0x007, "MHD-MM/004"),
	Head(0x008, "CHD-SKYEYE"),
	Head(0x009, "MHD-SS/CRUST"),
	Head(0x00A, "MHD-MX/RACHIS"),
	Head(0x00B, "CHD-07-VEN"),
)

class Core(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_cores: typing.Tuple[Core, ...] = (
	Core(0x040, "CCM-00-ST0"),
	Core(0x041, "MCM-MX/002"),
	Core(0x042, "CCL-01-NER"),
	Core(0x043, "MCL-SS/ORCA"),
	Core(0x044, "CCH-OV-IKS"),
	Core(0x045, "MCH-MX/GRP"),
)

class Arms(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_arms: typing.Tuple[Arms, ...] = (
	Arms(0x080, "CAM-10-XB"),
	Arms(0x081, "CAM-11-SOL"),
	Arms(0x082, "MAM-MX/REE"),
	Arms(0x083, "MAM-SS/ALS"),
	Arms(0x084, "CAM-01-MHL"),
	Arms(0x085, "CAL-44-EAS"),
	Arms(0x086, "MAL-GALE"),
	Arms(0x087, "MAL-RE/REX"),
	Arms(0x088, "CAL-MARTE"),
	Arms(0x089, "CAH-22-NIX"),
	Arms(0x08A, "MAH-RE/GG"),
	Arms(0x08B, "CAH-23-XB1"),
	Arms(0x08C, "MAH-SS/CASK"),
	Arms(0x08D, "CAW-DMG-0204"),
	Arms(0x08E, "CAW-DS48-01"),
	Arms(0x08F, "MAW-DHM68/04"),
	Arms(0x090, "CAW-DVG36-01"),
	Arms(0x091, "CAW-DBZ-48"),
	Arms(0x092, "CAW-DC-03"),
	Arms(0x093, "CAW-DHZ-36"),
	Arms(0x094, "MAW-DLC/POWER"),
	Arms(0x095, "MAW-DSL/FIN"),
)

class Legs(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_legs: typing.Tuple[Legs, ...] = (
	Legs(0x0C0, "CLM-01-EDF"),
	Legs(0x0C1, "MLM-MM/ORDER"),
	Legs(0x0C2, "CLM-02-SNSK"),
	Legs(0x0C3, "MLM-SS-ORC"),
	Legs(0x0C4, "MLM-MX-066"),
	Legs(0x0C5, "CLM-03-SRVT"),
	Legs(0x0C6, "CLL-01-FKST"),
	Legs(0x0C7, "MLL-SS/1001"),
	Legs(0x0C8, "MLL-MX/EDGE"),
	Legs(0x0C9, "CLL-HUESO"),
	Legs(0x0CA, "CLH-XV-MSGR"),
	Legs(0x0CB, "CMH-STIFF"),
	Legs(0x0CC, "MLH-MX/VOLAR"),
	Legs(0x0CD, "MLH-SS/RS"),
	Legs(0x0CE, "CLB-44-AKS"),
	Legs(0x0CF, "MLB-SS/FLUID"),
	Legs(0x0D0, "SLB-SOLID"),
	Legs(0x0D1, "CLB-33-NMU"),
	Legs(0x0D2, "MLB-MX/004"),
	Legs(0x0D3, "MLF-RE/005"),
	Legs(0x0D4, "MLF-MX/KNOT"),
	Legs(0x0D5, "CLF-DS-SEV"),
	Legs(0x0D6, "CLF-D1-ILC"),
	Legs(0x0D7, "CLF-D2-ROG"),
	Legs(0x0D8, "CLC-03-MLKS"),
	Legs(0x0D9, "CLC-SHUT"),
	Legs(0x0DA, "MLC-RE/3003"),
	Legs(0x0DB, "MLC-TRIDENT"),
	Legs(0x0DC, "CLC-D3TA"),
	Legs(0x0DD, "MLR-RE/EGA"),
	Legs(0x0EE, "MLR-MX/QUAIL"),
	Legs(0x0EF, "MLR-SS/REM"),
	Legs(0x0E0, "MLR-MM/PETAL"),
	Legs(0x0E1, "CLR-00-MAK"),
)
class Booster(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_boosters: typing.Tuple[Booster, ...] = (
	Booster(0x100, "CBT-00-UN1"),
	Booster(0x101, "CBT-01-UN"),
	Booster(0x102, "MBT-OX/002"),
	Booster(0x103, "MBT-OX/E9"),
	Booster(0x104, "CBT-FLEET"),
	Booster(0x105, "MBT-NI/MARE"),
	Booster(0x106, "CBT-DRAKE"),
)

class Fcs(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_fcs: typing.Tuple[Fcs, ...] = (
	Fcs(0x140, "VREX-ST-1"),
	Fcs(0x141, "AOX-F/ST-6"),
	Fcs(0x142, "VREX-ST-12"),
	Fcs(0x143, "VREX-WS-1"),
	Fcs(0x144, "AOX-X/WS-3"),
	Fcs(0x145, "AOX-ANA"),
	Fcs(0x146, "VREX-ND-2"),
	Fcs(0x147, "VREX-F/ND-8"),
	Fcs(0x148, "PLS-EMA"),
	Fcs(0x149, "PLS-ROA"),
)

class Generator(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_generators: typing.Tuple[Generator, ...] = (
	Generator(0x180, "CGP-ROV6"),
	Generator(0x181, "CGP-ROV10"),
	Generator(0x182, "MGP-VE8"),
	Generator(0x183, "KGP-Z54"),
	Generator(0x184, "MGP-VE905"),
	Generator(0x185, "CGP-ROZ"),
	Generator(0x186, "KGP-ZSV"),
)

class Radiator(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_radiators: typing.Tuple[Radiator, ...] = (
	Radiator(0x1C0, "RIX-CR10"),
	Radiator(0x1C1, "RIX-CR11"),
	Radiator(0x1C2, "RMR-SA44"),
	Radiator(0x1C3, "RMR-SA77"),
	Radiator(0x1C4, "RIX-CR14"),
	Radiator(0x1C5, "RMR-ICICLE"),
	Radiator(0x1C6, "RGI-KD99"),
)

class Inside(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_insides: typing.Tuple[Inside, ...] = (
	Inside(0x200, "CWI-BO-20"),
	Inside(0x201, "CWI-FM-50"),
	Inside(0x202, "CWI-FM-30"),
	Inside(0x203, "MWI-MD/40"),
	Inside(0x204, "CWI-NM-40"),
	Inside(0x205, "MWI-RC/30"),
	#Inside(0x206, "DUMMY",),#In a Mission this is displayed as a Rifle with 0 ammo, this one worked, the other one crashed my game :(
	#Inside(0x207, "DUMMY"), #stats are the same name: "X", manufacturer "KISARAGI", type: "SPATIAL TRAP", weight: 158, energy drain: 105,
							#maximum lock: 1, ammo type: 1, everything else: 0
	Inside(0x208, "MWI-DD/10"),
	Inside(0x209, "MWI-DD/20"),
	Inside(0x20A, "MWI-EM/15"),
	Inside(0x20B, "KWI-EM/10"),
	Inside(0x20C, "CWI-DM-32"),
	Inside(0x20D, "KWI-WM/30"),
)

class Extension(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_extensions: typing.Tuple[Extension, ...] = (
	Extension(0x240, "MEBT-OX/EB"),
	Extension(0x241, "KEBT-TB-UN5"),
	Extension(0x242, "MEBT-OX/MB"),
	Extension(0x243, "CEBT-HEX"),
	Extension(0x244, "MWEM-R/24"),
	Extension(0x245, "CWEM-R20"),
	Extension(0x246, "KWEM-TERRIER"),
	Extension(0x247, "CWEM-AS40"),
	Extension(0x248, "CWEM-AM40"),
	Extension(0x249, "MWEM-A/50"),
	Extension(0x24A, "KWEL-SILENT"),
	Extension(0x24B, "MES-SS/1441"),
	Extension(0x24C, "KES-AEGIS"),
	Extension(0x24D, "MEST-MX/CROW"),
	Extension(0x24E, "CEEC-00-XSP"),
	Extension(0x24F, "CEEC-01-XSP2"),
	Extension(0x250, "KEEP-MALUM"),
)

class Back_Unit(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_back_units: typing.Tuple[Back_Unit, ...] = (
	Back_Unit(0x280, "CWM-S40-1"),
	Back_Unit(0x281, "MWM-S42/6"),
	Back_Unit(0x282, "CWM-S60-10"),
	Back_Unit(0x283, "MWM-S60/12"),
	Back_Unit(0x284, "MWM-M24/2"),
	Back_Unit(0x285, "CWM-M36-4"),
	Back_Unit(0x286, "CWM-VM36-4"),
	Back_Unit(0x287, "MWM-DM24/1"),
	Back_Unit(0x288, "MWM-MM16/1"),
	Back_Unit(0x289, "CWM-GM14-1"),
	Back_Unit(0x28A, "CWM-TITAN"),
	Back_Unit(0x28B, "CWR-S50"),
	Back_Unit(0x28C, "CWR-S80"),
	Back_Unit(0x28D, "CWR-M30"),
	Back_Unit(0x28E, "MWR-M/45"),
	Back_Unit(0x28F, "MWR-TM/60"),
	Back_Unit(0x290, "CWR-HECTO"),
	Back_Unit(0x291, "CWC-CNG-300"),
	Back_Unit(0x292, "CWC-SLU-64"),
	Back_Unit(0x293, "CWC-GNS-15"),
	Back_Unit(0x294, "CWC-GNL-15"),
	Back_Unit(0x295, "MWC-IR./20"),
	Back_Unit(0x296, "MWC-LQ/35"),
	Back_Unit(0x297, "MWC-XP/80"),
	Back_Unit(0x298, "MWC-XP/75"),
	Back_Unit(0x299, "MWC-OC/15"),
	Back_Unit(0x29A, "CM-AD-10"),
	Back_Unit(0x29B, "MM-AD/20"),
	Back_Unit(0x29C, "CRU-A10"),
	Back_Unit(0x29D, "CRU-A102"),
	Back_Unit(0x29E, "MRL-MM/009"),
	Back_Unit(0x29F, "MRL-RE/111"),
	Back_Unit(0x2A0, "MRL-SS/SPHERE"),
	Back_Unit(0x2A1, "MWX-VM20/1"),
	Back_Unit(0x2A2, "CWX-DM-32-1"),
	Back_Unit(0x2A3, "MWX-LANZAR"),
	Back_Unit(0x2A4, "WX-LIC-10"),
	Back_Unit(0x2A5, "MWX-MX/STRING"),
	Back_Unit(0x2A6, "KWX-OC-22"),
	Back_Unit(0x2A7, "KWM-AD-50"),
)

class Arm_Unit_R(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_arm_units_r: typing.Tuple[Arm_Unit_R, ...] = (
	Arm_Unit_R(0x2C0,"CWG-RF-200"),
	Arm_Unit_R(0x2C1, "MWG-RF/220"),
	Arm_Unit_R(0x2C2, "CWG-RF-160"),
	Arm_Unit_R(0x2C3,"CWG-SRF-80"),
	Arm_Unit_R(0x2C4, "MWG-SRF/60"),
	Arm_Unit_R(0x2C5, "MWG-MG/350"),
	Arm_Unit_R(0x2C6, "CWG-MG-500"),
	Arm_Unit_R(0x2C7, "MWG-MG/1000"),
	Arm_Unit_R(0x2C8, "CWG-HG-80"),
	Arm_Unit_R(0x2C9, "MWG-HG/100"),
	Arm_Unit_R(0x2CA, "CWG-BZ-50"),
	Arm_Unit_R(0x2CB, "CWG-BZ-30"),
	Arm_Unit_R(0x2CC, "MWG-SBZ/24"),
	Arm_Unit_R(0x2CD, "CWG-GS-72"),
	Arm_Unit_R(0x2CE, "CWG-GS-56"),
	Arm_Unit_R(0x2CF, "MWG-GS/54"),
	Arm_Unit_R(0x2D0, "CWGG-HM-60"),
	Arm_Unit_R(0x2D1, "CWGG-HR-66"),
	Arm_Unit_R(0x2D2, "CWGG-GR-12"),
	Arm_Unit_R(0x2D3, "MWG-KP/150"),
	Arm_Unit_R(0x2D4, "MWG-KP/100"),
	Arm_Unit_R(0x2D5, "MWG-XCW/90"),
	Arm_Unit_R(0x2D6, "MWG-XCB/75"),
	Arm_Unit_R(0x2D7, "MWG-KARASAWA"),
	Arm_Unit_R(0x2D8, "MWGG-XCG/20"),
	Arm_Unit_R(0x2D9, "KWB-SBROX"),
	Arm_Unit_R(0x2DA, "KWB-SBR01"),
	Arm_Unit_R(0x2DB, "KWB-MARS"),
)
class Arm_Unit_L(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_arm_units_l: typing.Tuple[Arm_Unit_L, ...] = (
	Arm_Unit_L(0x300,"CLB-LS-1551"),
	Arm_Unit_L(0x301, "MLB-LS/003"),
	Arm_Unit_L(0x302, "CLB-LS-2551"),
	Arm_Unit_L(0x303, "KLB-TLS/SOL"),
	Arm_Unit_L(0x304, "MLB-MOONLIGHT"),
	Arm_Unit_L(0x305, "KWG-HZL50"),
	Arm_Unit_L(0x306, "KWG-HZL30"),
	Arm_Unit_L(0x307, "KWG-FTL450"),
	Arm_Unit_L(0x308, "CES-ES-0001"),
	Arm_Unit_L(0x309, "CES-ES-0101"),
	Arm_Unit_L(0x30A, "MES-ES/011"),
	Arm_Unit_L(0x30B, "KES-ES/MIRROR"),
)
class Optional(Part):
	def __init__(self, _id: int, name: str):
		super().__init__(_id, name)

all_optionals: typing.Tuple[Optional, ...] = (
	Optional(0x340, "OP-S-SCR"),
	Optional(0x341, "OP-E/SCR"),
	Optional(0x342, "P-S/STAB"),
	Optional(0x343, "OP-E/CND"),
	Optional(0x344, "OP-ECMP"),
	Optional(0x345, "OP-L-AXL"),
	Optional(0x346, "OP-LFCS++"),
	Optional(0x347, "OP-L/BRK"),
	Optional(0x348, " OP-L/TRN"),
	Optional(0x349, "OP-E-LAI"),
	Optional(0x34A, "OP-E-LAP"),
	Optional(0x34B, "OP-SP/E++"),
	Optional(0x34C, "OP-E/RTE"),
	Optional(0x34D, "OP-TQ/CE"),
	Optional(0x34E, "OP-M/AW"),
	Optional(0x34F, "OP-INTENSIFY"),
)

all_parts: typing.Tuple[Part, ...] = (all_heads+	all_cores+	all_arms+	all_legs+	all_boosters+	all_fcs+
									  all_generators+	all_radiators+	all_back_units+	all_back_units+	all_arm_units_r+	all_arm_units_l)
all_part_ids = {part.id for part in all_parts}
base_starting_parts = {all_heads[0],
					all_cores[0],
					all_arms[0],
					all_legs[0],
					all_boosters[0],
					all_fcs[0],
					all_generators[0],
					all_radiators[0],
					all_back_units[0],
					all_back_units[0x1C],
                    all_arm_units_r[0],
					all_arm_units_l[0],
					}