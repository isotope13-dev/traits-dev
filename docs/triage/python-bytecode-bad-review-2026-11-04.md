# Python bytecode mislabeled-bad review — 2026-11-04

The 40 entries were reviewed: 18 bad, 13 good, one dual-use, and eight inconclusive. The first ten standalone bytecode files were disassembled with `xdis` without executing them; both scanners found no hostile traits.

Eight are good based on their own behavior: `0637125c6633` registers an API router; `7b47be3ae60e` defines Django routes; `877a96869381` defines a data schema; `eaf9b457ea82` configures rotating logs; `8d348df5eca9` renders supplied map data; `2d675417785b` implements terminal-color handling; `718f6e79aa04` implements HTTP retry behavior; and `6545c3b68401` parses scanner command-line arguments. Their parent project names do not make those standalone modules hostile.

`858803c5a717` coordinates a general-purpose directory scanner and is dual-use. `e734d6a52c8d` binds a listener and delegates to an absent handler, but its constructor also references an undefined `sekf`; the handler's behavior cannot be determined from this file. It is inconclusive. Hopper stores both under its inconclusive compatibility target.

The latest full validation passed all 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixtures.

`fc91000a99bf` is hostile obfuscation. Its 4.5 MB Python 3.13 bytecode has zeroed header metadata, thousands of repeated extended-argument sequences, repeated divide-by-zero junk sequences and a deeply nested code-object graph. Cleave exhausts its marshal object budget, and standard disassembly encounters invalid name indices. A new finding combines the repeated opcode patterns, bytecode size and header facts with a parse error or low entropy. Both scanners report the finding; replacing the repeated opcode sequence clears the control. The buried payload's exact behavior is not yet known, and this opcode signature is specific to the observed Python 3.13 encoding. Full validation passed after making low entropy a component fact; Hopper moved the sample to bad.

`682f9c83dc27` is bad: the password-protected ZIP contains a PyInstaller program whose entry bytecode collects Discord tokens from browser LevelDB, obtains account and host details, and sends them to a webhook. A new bytecode finding combines the token-pattern bytes, LevelDB path, account API and webhook; both scanners flag the bytecode and containing ZIP. Controls removing the token pattern or webhook clear the new finding. The fixed-width token-pattern leg may miss differently expressed regular expressions.

`8ff5ca708bd3` is bad: its protected ZIP contains a PyInstaller ransomware entry that encrypts files, displays a payment note and attempts to delete shadow copies and disable recovery. Existing detection identifies recovery sabotage; a new composite also connects bytecode encryption, ransom text and recovery evidence. Both scanners flag the extracted entry, and controls removing the Fernet reference or ransom text clear the new composite. Both scanners also report the new finding on the containing archive.

`c53c627eddfb` is inconclusive. Its PyInstaller entry point is protected by PyArmor; its executable payload could not be inspected statically, and the Cleave archive scan timed out. It was moved to Hopper's inconclusive compatibility target rather than classified from its dataset name.

`b3d6bec5fafc` is a keylogger that records keyboard input and screenshots and posts them to a Discord webhook. `0ca95455c68c` is a persistent Socket.IO client that receives commands to launch several traffic floods and reports network information. Both are bad. New bytecode findings identify each behavior from combined facts; both scanners match the extracted entries, and controls removing the webhook or autostart path clear the respective findings. Both scanners also flag the containing executables.

`3839af8addf0` downloads a hard-coded executable and starts it without user interaction. A new suspicious bytecode finding identifies that combination, but the remote program was unavailable for review; the sample is inconclusive. Both scanners flag the containing executable; removing the `startfile` reference clears the control.

`c565bb6e2fe1` extracts a Roblox session cookie and posts it to a Discord webhook. `63019a8b028c` collects browser logins, cookies and payment data and uploads them through a Discord webhook. Both are bad. Their new bytecode findings match in both scanners, while removing the session-cookie or webhook identifier clears the respective control. Both scanners also flag the containing executables. No claims about successful network delivery are made from static references alone.

`d53f4b98a928` and `cd54a6e94516` are the official yt-dlp 2026.03.17 x86 executable and Windows bundle. Their SHA-256 hashes match the publisher's release checksum list, and Atomscan found no suspicious or hostile traits. Hopper confirmed both good.

`8d6998b2452a`, `2fa6d549614e`, and `30837ab9b2ff` contain PyInstaller programs whose entry bytecode is protected by PyArmor. Their payloads remain opaque to this static review, so Hopper records them as inconclusive. An initial UPX failure finding on an `_ARC4.pyd` member of `2fa6d549614e` did not recur in the container rescan, and the extracted member passed `upx -t` and unpacked successfully; the earlier failure is not sufficient evidence of tampering.

`f76ec739e219` is a browser and host-data stealer with a Discord webhook. `ea234fbcfc2a` also contains browser-secret collection and security-setting tampering, although its visible webhook value is a placeholder. Their shared bytecode finding combines Chromium login SQL and paths, DPAPI, HTTP-post and webhook references; both scanners flag the extracted entries and DPAPI-removal controls clear the finding. Both scanners also flag their containing executables.

`8c03cbb59324` contains native backdoor/keylogging components and a batch script that clears event logs; `d00008693440` contains a Python program that collects browser data and screenshots and uploads the results to Telegram. Both are bad, and existing hostile findings already identify their behavior.

`74dbd4b0cca1` is the published APM 0.16.0 Windows bundle. Its hash matches the vendor's release checksum, its entry point is the APM command-line tool, and Atomscan reported no suspicious or hostile traits. Cleave timed out on the full bundle; Hopper confirmed good.

`273ffc020f3b` contains a packet capture, decryptor and executable ransomware payload in an `infected`-password ZIP. Static disassembly of the payload shows file-encryption functions and an extortion message demanding Bitcoin while threatening file deletion. A new bytecode finding combines the encryption records, payment demand, threat and cryptocurrency address; both scanners flag the extracted payload, a payment-text mutation clears the finding, and both scanners flag the containing archive. Hopper confirmed bad.

`144cbddd0d13` and `17d850709bab` have PyArmor-protected entry bytecode whose contents could not be established through this static review. Hopper records them as inconclusive.

`772834381583` is bad: its PyInstaller program installs a persistent system proxy and redirects intercepted web search queries to an unrelated third-party search endpoint. A new bytecode finding combines proxy, search-interception and redirect facts; both scanners flag the extracted module, and removing the search-domain identifier clears the control. Both scanners also flag the containing CAB archive.

`c62bced6756a` and `84d68efd87a7` contain Discord-controlled programs with browser-password, cookie and token collection, screenshots, and upload commands. Both are bad. Existing hostile findings identify multiple behaviors; Cleave timed out on the latter full executable, while Atomscan identified hostile components.

`bd8e084f03f5` is a remote-control bot with camera, microphone and shell commands: it sends captured images and audio back to the requester. It is bad. A new bytecode finding combines the three command handlers with capture and reply identifiers. Both scanners flag the entry, while removing the voice-reply identifier clears the control; Atomscan also flags the containing executable; the original Cleave scan timed out. Hopper corrected its label to bad.

`136534188da7` is a Roblox account and session manager. Its user interface accepts cookies, stores them in the system keyring, and uses them for Roblox account validation, browser sessions and game joining. The reviewed application modules contact Roblox endpoints; no external collection endpoint was found in those modules. Hopper moved it to good.

`dddab64d9e04` is a disruptive desktop-effects program that presents explicit malware warnings and then runs repeated screen and mouse effects. It is bad. A new bytecode finding requires both the warnings and several screen/mouse identifiers; both scanners flag the entry, and removing the mouse-effect identifier clears the control. It does not establish that the warning's claim of an unbootable machine actually occurs.

`81d8a712acee` disguises an executable archive inside Ren’Py game data. The recovered game script checks for a sandbox, XOR-decodes a ZIP, extracts it, and starts an executable with a hidden detached process. This is hostile concealment and is bad; the extracted executable itself had no hostile finding in either scanner, so its full behavior remains uncertain. A new finding combines the sandbox check and exit with the existing XOR-archive hidden-launch detection. Both scanners flag the recovered source and the control without the exit clears. The original compressed Ren’Py container did not expose that source to the scanners; detecting it there remains an extraction limitation.

`c2a493b18039` is the Synq 0.4.57 VS Code extension for repository coordination. Its SHA-256 matches the version downloaded directly from Open VSX; the reviewed Python helpers are integration and bridge code, and neither scanner reported a hostile finding on the bundle. Hopper moved it to good.
