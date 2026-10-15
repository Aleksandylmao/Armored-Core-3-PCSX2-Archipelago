# Armored Core 3 (PCSX2) Archipelago

Armored Core 3 is a 2002 third-person shooter video game developed by FromSoftware for the PlayStation 2.
It is the sixth entry in the Armored Core series.

Available to download in the [releases](https://github.com/Aleksandylmao/Armored-Core-3-PCSX2-Archipelago/releases)  section!

## [Randomizer Info](docs/en_Armored%20Core%203.md)

[Setup Guide](docs/setup_en.md)
-----
### Prerequisites:
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases/latest)
- [The Armored Core 3 APWorld](https://github.com/Aleksandylmao/Armored-Core-3-PCSX2-Archipelago/releases) 
- [PCSX2 Emulator](https://pcsx2.net/downloads/)
- A legally-obtained Armored Core 3 ISO 
	- NTSC-U, SLUS-20435 

  
Acknowledgements
---
Thank you to these projects for helping me make this Archipelago Implementation possible:
- The Archipelago Core Team and Contributors
- evilwb's [pypine](https://github.com/evilwb/pypine)
- [thatbard's](https://retroachievements.org/user/thatbard) [Armored Core 3 RetroAchievements](https://retroachievements.org/game/3308) for providing some Memory Addresses
- [Armored Core APWorld](https://github.com/JustinMarshall98/Armored-Core-PSX-Archipelago/releases)  which got me to play the older games again and inspired me to make this APWorld 

AI Disclaimer
---
- Was AI used in any capacity?
- - Yes
- If so, what tools were used?
- - Claude and ChatGPT 
- What was the purpose of your use of these tools?
- - Mainly for code reviews, Ai looks at my code informs me of bugs that I missed, what would be a better design, etc. I always take its feedback with a grain of salt.    
- - Sometimes technical questions, since I'm still new to Python and APWorld development 
- - One minor bug fix. The bug was in Shopsanity where certain symbols (e.g. `<` and `>`) caused crashes, I identified it and AI wrote the function which looked good to me.
- - At the beginning I tried to use it to help me find memory addresses, but it didn't help at all. In the end it was faster to learn a bit of assembly myself.
- How extensively were the tools used? 
- - I let AI review my code occasionally. And besides that one bug not much. 
- How much human review was done?
- - All the code was reviewed and written by me. If somebody else wants to review my code feel free to do so. 

Support
---
Have suggestions, comments or issues?
Please get in touch in the Armored Core 3 thread of the future-games-design forum in the official Archipelago Discord Server.

---
Pls give the other Armored Core APWorlds also a try.
- [Armored Core](https://github.com/JustinMarshall98/Armored-Core-PSX-Archipelago/releases)
- [Armored Core 6](https://github.com/DeltaSilver/Armored-Core-6-Archipelago/releases)

