# Armored Core 3 Setup Guide

## Required Software

- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases) (0.5.0+)
- PCSX2 2.0 or newer, with PINE support
- A legally-obtained Armored Core 3 (NTSC-U, SLUS-20406) ISO
- The Armored Core 3 client's Python dependency: `pip install pine`

## Installing the World

1. Download `armored_core_3.apworld` from the releases page.
2. Double-click it, or drag it onto `ArchipelagoLauncher.exe`, to install it.
3. Run `ArchipelagoLauncher.exe` -> **Generate Template Options** to get
   `Armored Core 3.yaml` in your `Players/Templates` folder. Edit it to
   taste and drop it in `Players/`.

## Configuring PCSX2

1. In PCSX2: **Tools -> Show Advanced Settings**.
2. **System -> Settings -> Advanced -> PINE Settings**: check **Enable**,
   Slot **28011**.
3. Boot Armored Core 3 and get to the garage/menu before connecting.

## Connecting

1. Open the **Armored Core 3 Client** from the Archipelago launcher.
2. It will try to auto-detect PCSX2 over PINE.
3. Enter `archipelago.gg:<port>` (or your local host:port) and your slot
   name to connect, same as any other Archipelago client.
