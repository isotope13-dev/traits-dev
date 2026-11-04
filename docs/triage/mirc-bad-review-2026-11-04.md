# mIRC mislabeled-bad review — 2026-11-04

Reviewed all 40 entries with Cleave and Atom and inspected their content without execution. Nineteen are bad, 13 good, one dual-use and seven inconclusive.

The bad entries are `0c567fb8f524`, `7504c62291eb`, `08aa978efcd1`, `a64f65ca23b8`, `9ec27322880b`, `aa9a6345838c`, `6ebb40272fb9`, `b95a8c48dda0`, `5877fe00d216`, `71508d02764b`, `e60aa899a01e`, `7b67d327c209`, `ddff9e33c37f`, `3aa4e41c61d9`, `dd5bddc0d4c8`, `e1df66bfeddc`, `8f3d3396c904`, `9d9cb62ad2fe` and `17fde06a0092`.

`ddff9e33c37f` scans router Telnet ports, attempts enable authentication and sends discovered router IP addresses and passwords to an IRC channel. A new hostile composite records the host-findings report. `7b67d327c209` parses discovered host credentials and stages network-access commands; its `talk` reporting helper is not included, so the destination of those status messages is not established. `3aa4e41c61d9` scans SMB hosts, reports discoveries to a channel and attempts to invoke an infection helper. The helper is absent, so successful infection was not assumed. `b95a8c48dda0` attempts to use SubSeven commands to enable FTP and launch VBScript; its secondary script is also absent.

New hostile findings cover a UDP listener that evaluates received commands, a Cobalt Strike browser-password task loader, an IRC-triggered run command, packet-flood clients and controllers, an operator menu for flooding and hidden execution, and scripts that reconstruct or send their own IRC code. `e60aa899a01e` constructs a forced drive-deletion batch and schedules it when the script loads. The detection combines the variable assignment, generated command, execution and load trigger. Each new finding was checked in Cleave and Atom against its applicable sample and a control removing a defining behavior.

`07d79c58538a` is a general IRC socket bridge and is dual-use. The existing hostile PING/PONG finding was reduced to a neutral fact, and a file-backdoor composite now requires actual file-operation evidence rather than accepting ordinary token parsing. Both scanners clear the bridge's hostile findings, while the file-reading and deleting listener `71508d02764b` remains hostile. The separate flood behavior in `17fde06a0092` now has its own hostile finding.

The inconclusive entries are `2de3fc53f124`, `d81c9489356a`, `c0f473b70b9c`, `0e12d455bf6b`, `45e59d777c14`, `327ffd43bc91` and `0877989b9678`. These depend on absent executables, remotely fetched scripts, message content or external aliases, or perform targeted file deletion whose purpose is unresolved. They and the dual-use bridge are stored in Hopper's purgatory.

The good entries are `64e8041e81da`, `7cf5b3f84272`, `d639f65c458d`, `830f5baf1c75`, `6cc6df41144e`, `02219d79c1b4`, `ae815f518c06`, `e75f45486fc3`, `154967591468`, `f4628245eb71`, `7e497bf1af5b`, `2867bb1463ea` and `42e5efb3fb57`. They are configuration, interface definitions, general IRC utilities or an installer that delegates to absent sibling scripts. The last contains an inert IIS command string and retains one suspicious finding; it does not itself execute that string.

Full validation passed after the rule changes. No scanner feature was added.
