# Native sample review, 2026-10-17

The verdicts below follow static execution-path analysis, not ML scores.
Original samples were hashed, scanned with atomscan, and inspected with
`cleave facts`. Analysis artifacts and disassembly are in the task scratch
folder `review-5569-8aec-1ee6`; specimens were never launched.

| SHA-256 prefix | Identification | Verdict | Execution evidence |
| --- | --- | --- | --- |
| 5569fb9242d2 | Mirai-style Linux HTTP flood bot | MALICIOUS | POST flood, concealed startup installation, kernel privilege exploit |
| 8aec734e419d | StormAttack service-DLL injector | MALICIOUS | LanmanServer ServiceDLL hijack, Active Setup registration, remote DLL thread |
| 1ee660bd8a6f | UPX-packed Gh0st RAT with Hidden drivers | MALICIOUS | Credential command handler, directory-result filtering, physical boot-sector clearing |

## Linux bot

The ELF is statically linked i386 code. Its startup calls the configuration
initializer at 0x0804b02b. Table entries are allocated at 0x0804afcc and
transformed by 0x0804abcb, which derives key material and calls the byte
transform at 0x08054409 with the `KATARU` context. Emulating only these
memory-transform routines, with allocation stubbed and interrupts rejected,
recovers configuration entries including two IPv4 endpoints, port 443,
`/proc/net/tcp`, watchdog paths and process-name lists. Heuristic XOR strings
from facts were not treated as reliable plaintext.

The poll-driven network routine formats the oversized POST template at
0x0804d876 and passes it to the send routine at 0x0804d90f; subsequent states
continue writing rather than completing an ordinary HTTP transaction.
Persistence construction formats the cron template at 0x08059044 and uses
shared filesystem writers for startup paths. TracerPid parsing at
0x0805bad5 calls its termination path for a nonzero debugger PID.
The RxKAD exploit includes the write/corruption stage and post-write
verification of the su image around 0x080676d9–0x080677fe.

An ELF64 header resides inside mapped read-only data. The matcher does not
establish an appended overlay or conflicting file interpretation; its new
home is binary-layout metadata. Persistence templates alone also occur in
installers, so the hostile persistence composite now requires flood-bot
context. A standalone MIRAI-CNC user-agent token is a neutral HTTP token.

## StormAttack injector

The outer entry reaches routines that extract a PE resource at 0x00402460,
write its contents through 0x004023c0, set the LanmanServer ServiceDLL value,
and create Active Setup registration. The injection routine at 0x00401150
creates a process, allocates remote memory, writes the DLL path, resolves the
loader export, and passes that address and remote buffer to
CreateRemoteThread at 0x0040123d. Its existing persistence, injection and
cleanup findings are supported.

The resource at file offset 0x5060 carries Storm banners and command-format
identity strings, but much of its code/import region is zeroed. It supports
the existing DNS-*labeled* module identity, not proof of an executing DNS
reflection flood. The collection filename supplies no evidence for Elex,
Remcos or WannaCry.

## Gh0st and embedded drivers

UPX decompression produces a 1,310,720-byte DLL. Two embedded PEs at offsets
0x102920 and 0x111f68 implement the Hidden filesystem driver in x86/x64 form.
In the x86 driver, the directory-cleaning routine at 0x00403010 checks hidden
object lists, changes NextEntryOffset links, compacts results with memmove,
and can return STATUS_NO_MORE_FILES. This verifies concealment independently
of the QAssist diagnostics.

The AV image-name table beginning at 0x10124ff8 feeds 0x100143b0: each process
lookup returns a PID; matches cause the corresponding vendor label to be
appended to a report. The report builder consumes it at 0x100151d1. It does
not pass those PIDs into TerminateProcess. Other command handlers use
termination and service-control APIs independently. The generic conjunctions
therefore belong in neutral capability directories, not hostile EDR-killing
objectives. Multiple vendor names do not supply the missing data flow.

DeviceIoControl calls around 0x10064614 service the Hidden object interface;
the calls around 0x1000c215/0x1000c244 lock/unlock disk storage. Neither
establishes exploitation of a vulnerable driver. BYOVD detection now requires
known driver/termination-IOCTL evidence as well as security targets.

The command handler at 0x1000c290 dispatches to 0x1000c180. That routine
initializes a 512-byte sector buffer, stamps 55 AA, opens PHYSICALDRIVE0 for
writing, locks it, writes the sector through the same handle, unlocks it,
and calls ExitWindowsEx with flags 6 (forced reboot). This erases boot and
partition information; the new detection requires that clearing/lock/write/
unlock instruction sequence plus physical-drive and write/reboot API facts.
It has no dependency on a specimen name, hash, C2 address or exact file size.
The GetMP handler stages received executable bytes and writes the
`sekurlsa::logonpasswords` command to the child channel at 0x1001ce20–0x1001ce50.

Upstream RAT rules also matched trailing parent strings in an extracted
minifilter view. Prefer the native RAT/rootkit findings in that context;
the standalone minifilter is not itself a RAT. Generic software inventory
signatures add neither malicious intent nor a useful family identity.

## Placement and controls

The firing EDR/AV process-name union and its named-process atoms move into
`micro-behaviors/os/security/product`, retaining their matchers and scopes.
Their severities become notable because a complete process-name reference is
independently useful. The aggregate no longer accepts a Defender-suppression
behavior as an alternative proof of a process-name reference; that behavior
retains its own objective. Exact consumers are updated. No ancestor-directory
selectors of the moved leaves or security-product directory were found.


Postgres and inetd tokens use neutral process-name references; the duplicate
inetd atom is consolidated. Their database-name union uses service-name
references. The existing Wireshark executable-name matcher moves to debugging
tool references, without changing its matcher or scope. This also frees space
in the process-name leaf without adding a count-based taxonomy split.
The wide CSRSS suffix atom does not prove masquerade; its worm consumer uses
the existing neutral CSRSS name reference instead. That intentionally admits
ASCII spellings while retaining the VB6 copy and drive-type requirements.

The inventory regression fixture now checks both single- and multi-vendor
inventories for *zero* hostile findings. Both pass. The boot-sector sequence
and hostile composite match the unpacked RAT. Removing the sector-clear
operation makes the new composite decline despite retained disk/write/reboot
APIs; this byte-mutated near miss is not labeled a benign program. The
ordinary browser-handler PE control also declines the wipe and BYOVD rules.
Original samples are rescanned after changes. Each retains at least two
independent native hostile traits.
