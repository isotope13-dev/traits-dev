# First reasoned review of three native IoT bots

All three samples are **MALICIOUS**, based on static execution-path analysis.
No sample was executed and no embedded endpoint was contacted. Atomscan and
`cleave facts` were run separately for each file, before rule changes; atomscan
was then rerun on each target. External sample pages were unavailable, so the
queue's family labels and scores were not used as proof.

## x86-64 pair

- `7a625966f12f55e3ab44851cff76ee72be6aaf4d21a5398de3d400af3a0ca680`
- `5ec5f9e689a96716385bffc8933bfaacbd4e806922ff13bd2edb3d3d6aa86234`

Both are unstripped, dynamically linked Linux PIEs with substantially shared
Mirai-derived code. The second was tagged Wraith in the queue; no independent
subfamily attribution is asserted here. Rizin disassembly confirms:

- Main calls `killer_init` and `scanner_init` at `0x2a4a` and `0x2a51`.
  The received command buffer reaches `attack_parse` at `0x30d2`.
  The parser extracts duration, vector, target addresses/prefixes and options,
  then calls `attack_start`, which forks and invokes the registered handler.
- `attack_init` installs TCP, UDP, GRE and amplification handlers. In
  `attack_udp_generic`, `socket(AF_INET, SOCK_RAW, IPPROTO_UDP)` at `0x7559`
  is followed by IP_HDRINCL configuration, packet/header/checksum construction,
  repeated `sendto` at `0x77e0`, and backwards control flow. This is working
  flood code, not just handler names.
- `add_auth_entry` uses `deobf`, whose paired byte loop at `0x90c0` XORs
  credentials with `0x22`. Decoding recovers device-specific defaults including
  `xmhdipc`, `juantech` and `smcadmin`. `scanner_init` constructs probes,
  connects to responsive targets, negotiates Telnet, sends usernames/passwords,
  retries other combinations and reports successful address/port/credential
  tuples through its loader callback (`connect` at `0xa72b`, sends through
  `0xa7d1`). This supports credential guessing and reporting capability.
- `killer_init` removes permissions from downloader/transfer utilities using
  `chmod(path, 0)` at `0x85d0`. It repeatedly enumerates procfs, reads process
  names, compares against a blacklist containing rival bots, miners, services
  and interpreters, and issues `kill(pid, SIGKILL)` at `0x8861`. The matching
  diagnostic at `0xdae8` identifies this as name-selected termination.
- `toggle_obf` applies twenty four-byte XOR keys, each to every table byte.
  Their combined byte key is `0x3a`; decoded entries include procfs fragments,
  router shell commands and a BusyBox probe. Table declarations alone were
  not taken as proof that every configured endpoint works. In particular,
  the plaintext-looking controller entry still passes through this transform;
  successful remote tasking was not established dynamically.

The first binary additionally embeds an HTTP POST logging implementation;
the second's logging implementation differs. Source-file symbols naming
`persist.c`, `hide.c` or `fileless.c` do not establish those behaviors.

## ARM sample

`f1146624e0dddb086a1e1ddaf134a663241988c9c756a8f79b65606670665980`
is a stripped, statically linked ARM EABI Mirai-derived router worm.

- The scanner at `0x1402c` handles Telnet negotiation and authentication, sends
  router CLI shell-entry commands and `ping ;sh`, and transmits BusyBox shell
  commands through the send wrapper at `0x19774` (underlying syscall stub
  `0x19730`). At `0x14890`–`0x148a0` it sends the chmod-and-execute command;
  the paths around `0x158f8` send downloader pipelines with wget, tftp, ftpget
  and curl alternatives. These are remote propagation commands.
- Packet-construction loops repeatedly call the sendto wrapper at `0x197f0`
  while iterating supplied targets. The matched send-loop window starts at
  file offset `0x11a8` (virtual `0x91a8`). Propagation supplies the bot context
  for the flood objective; the send loop alone stays notable.
- The resolver path calls `0x11138` at `0x136fc` to transform a four-byte
  address. That routine initializes an RC4 permutation, schedules the key
  `GET/dlr.`, and XORs keystream bytes into the address buffer. This token is
  not itself an HTTP request.
- Hex-escaped script fragments reconstruct a `/proc/*` walk that tests whether
  `/proc/$pid/exe` ends in `(deleted)` and issues `kill -9 "$pid"`. The loader
  stages these fragments with BusyBox `echo -ne` and shell execution. This is
  additional process-disruption behavior in the propagation implementation.

## Trait changes and controls

The raw-socket-only hostile rule was removed: its two neutral constituent
traits remain, while the replacement under `dos/flood` also requires TCP/UDP
attack handlers and packet sending. The protocol-neutral attack-status matcher
moved from `dos/udp` to `communications/flood`, preserving its matcher, scope
and exact consumers; no ancestor directory consumers select either location.

`MIRAI` in this pair is a blacklist entry, not a loader status banner.
The loader-status matcher now requires its actual `Loadinggg` diagnostic.
The name-only family reference is also suppressed when the new rival-killer
profile establishes that the name is a target; process-name observations remain.
New rules cover paired XOR code, credential retry scanning, and rival/deleted
image termination. No campaign hostname, sample filename or exact file size
is required by these detections.

The newly surfaced generic `kill` symbol matcher moved unchanged from
`process/terminate/signal::kill` to `process/control/signal::posix-kill-symbol`.
Its seven exact consumers were updated. The generic symbol retains its original
baseline severity: stock native runtimes include it. Specific SIGKILL code stays
notable. Unsupported defense-evasion mappings and context-based downgrades were
removed. Ancestor selectors under `process/terminate` intentionally lose this
single API observation: the timing/logic-bomb and SQL backdoor consumers must
not treat unspecified signal delivery as termination. No existing selector
targets the new control/signal directory. Other source-file rules (`killpg`,
`sigprocmask`, two architecture syscall wrappers and the procfs miner
composite) remain unchanged and are outside these samples' firing findings.

Run `python3 testdata/triage/mirai-first-review/check.py` for inert positive and
near-miss controls. They distinguish ordinary raw sockets, a family-name mention,
credential retries without credentials/network/decoder, kill text without code,
signal zero, and isolated cleanup scripts. The existing
`testdata/taxonomy/mirai-native-review/check.py` checks the retained ARM RC4 and
escaped-script observations. Final sample scans have four hostile traits per
x86-64 file and five for ARM, spanning impact, lateral movement and family
identity; the ARM count includes two pre-existing overlapping family profiles.
