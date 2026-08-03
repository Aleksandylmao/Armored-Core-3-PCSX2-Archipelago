import asyncio, multiprocessing, traceback
from collections.abc import Sequence
from argparse import Namespace

from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, handle_url_arg, server_loop, logger
from .mission import all_missions
from .parts import all_parts, all_part_ids
from .pcsx2_interface import AC3Interface
from NetUtils import ClientStatus

from .utils import Constants

class AC3CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)

class AC3Context(CommonContext):
    command_processor = AC3CommandProcessor
    game = Constants.GAME_NAME
    items_handling = 0b111
    interface_sync_task : asyncio.Task = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.written_item_indexes: set[int] = set()
        self.interface = AC3Interface(self)
        self.most_recent_instruction = None

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.connection_state = "request"
            self.previously_checked_locations = set(args["checked_locations"])
            self.processed_items = 0
            self.previously_processed_items = -1
        elif cmd == "Retrieved":
            if self.connection_state == "requested":
                retrieved = args["keys"].get(f"ac3_processed_{self.team}_{self.slot}")
                self.previously_processed_items = retrieved if retrieved is not None else -1
                checked = args["keys"].get(f"ac3_checked_{self.team}_{self.slot}") or []
                self.previously_checked_locations.update(checked)
                self.connection_state = "ready"

    def player_instruction(self, instruction) -> None:
        if self.most_recent_instruction != instruction:
            logger.info(instruction)
            self.most_recent_instruction = instruction

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"Archipelago {Constants.GAME_NAME}"
        ui.logging_pairs = [("Client", "Archipelago")]
        return ui


async def interface_sync_task(ctx):
    ctx.player_instruction("Beginning communication with PCSX2...")
    logger.info("Beginning communication with PCSX2...")
    print("about to connect")

    while not ctx.exit_event.is_set():
        if not ctx.interface.connected:
            print("about to connect")
            ctx.interface.connect_game()
            print("connect returned")
        await asyncio.sleep(0.1) # Poll rate
        try:
            if ctx.interface.connected:
                await check_game(ctx)
            else:
                await reconnect_game(ctx)
                logger.info("Game reconnected")
        except ConnectionError:
            ctx.interface.disconnected()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue

async def check_game(ctx) -> None:
    if not ctx.server:
        ctx.player_instruction("You are not currently connected to an Archipelago server. Connect now!")
        ctx.connection_state = "none"
        return

    if not (ctx.slot and ctx.connection_state == "ready"):
        if ctx.connection_state == "request":
            ctx.connection_state = "requested"
            await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [
                    f"ac3_processed_{ctx.team}_{ctx.slot}",
                    f"ac3_checked_{ctx.team}_{ctx.slot}",
                ],
            }])
        await asyncio.sleep(1)
        return

    ctx.player_instruction("Connected and ready to play.")
    # Detect and send new location checks
    new_locations = ctx.interface.completed_missions.difference(ctx.previously_checked_locations)

    if new_locations:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(new_locations)}])
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"ac3_checked_{ctx.team}_{ctx.slot}",
            "default": {},
            "want_reply": False,
            "operations": [{"operation": "replace", "value": list(ctx.interface.completed_missions)}],
        }])
        ctx.previously_checked_locations.update(new_locations)

    #Receive and apply items
    for i in range(len(ctx.items_received)):
        if i < ctx.processed_items:
            continue  #already handled this session

        server_item = ctx.items_received[i]
        item_id = server_item.item

        #Idempotent unlocks: safe to re-apply every reconnect
        if item_id == Constants.ADDR_MISSION_COMPLETION+all_missions[-1].id: #Victory location for now
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        elif item_id - Constants.ADDR_INVENTORY in all_part_ids:
            ctx.interface.unlock_part(item_id)

        #Non-idempotent / consumable items: only apply items beyond
        #what Data Storage says we already processed last session
        if ctx.previously_processed_items != -1 and ctx.previously_processed_items < i:
            if item_id == Constants.ADDR_CREDITS:
                ctx.interface.queued_credits += 10000

            ctx.previously_processed_items = i
            if ctx.interface.queued_credits > 0:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"ac3_processed_{ctx.team}_{ctx.slot}",
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": ctx.previously_processed_items}],
                }])

        ctx.processed_items += 1
    ctx.interface.enforce_game_state()

async def reconnect_game(ctx : AC3Context):
    logger.info("Communication with PCSX2 failed. Please ensure that PCSX2 is open and Ape Escape 2 is loaded.")
    ctx.interface.connect_game()
    await asyncio.sleep(3)

async def main(args: Namespace) -> None:
    ctx = AC3Context(args.connect, args.password)
    ctx.auth = args.name
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    ctx.run_gui()
    ctx.run_cli()

    ctx.interface_sync_task = asyncio.create_task(interface_sync_task(ctx), name="PCSX2 Sync")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    if ctx.interface_sync_task:
        await asyncio.sleep(3)
        await ctx.interface_sync_task
    

def launch_ac3_client(*args: Sequence[str]) -> None:
    import colorama
    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url",  default=None, nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))
    colorama.init()
    asyncio.run(main(launch_args))
    colorama.deinit()

