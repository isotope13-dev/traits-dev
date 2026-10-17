# StormAttack loader review

All three inputs are **MALICIOUS**, based on traced unwanted persistence,
DLL injection and self-deletion code. The collection names do not establish
Elex, Remcos or WannaCry. These are local PE inputs, with no fetched dependency.
Analysis used atomscan, cleave facts (including decoded strings), Rizin
disassembly and direct PE byte/field inspection. No specimen was executed.
The supplied Triage pages could not be retrieved; their scores were not
used as behavioral evidence.

| SHA-256 | Identification | Hostile / suspicious IDs after changes |
| --- | --- | --- |
| 66b8f9965964de89e46244f7e2a2a5e24b9b2de21098d3007b799e1fbde12974 | StormAttack loader, console-subsystem variant | 4 / 1 |
| 7eae699b161614590373d3369ca3ca0bd8806d5a972cdb33d8cb2a61538830e9 | Same loader with padded call trampolines | 4 / 3 |
| 7d1f4afe218da341f24f5053a91a25b048aace20e2b3e5976ca958f87714a391 | Same loader with erased resources and modified headers | 4 / 1 |

Counts deduplicate IDs across each input and embedded children. Verdicts are
independent of the model ensemble, and compiled branches need not succeed to
establish the retained capability findings.

## Execution and effects

The three files have the same original code at VAs 0x401000..0x40289a,
apart from three call-site redirections in 7eae. Entry 0x402674 reaches
dispatcher 0x401cb0. Its configuration at 0x404120 is 3 in every input.

- Mode 3, at 0x401f75, calls 0x401900 and then 0x401390. The first routine
  generates a GUID (0x401840), constructs an HKLM Active Setup Installed
  Components subkey, and writes a GUID-named executable path as REG_EXPAND_SZ
  StubPath at 0x401a4b. It obtains its current module path, reads its image
  through fopen/fread, edits the buffer, writes a copy with fwrite at
  0x401b26 and launches it with CreateProcessA at 0x401b7e. The hardcoded
  patch offsets 0x6a0 and 0x3058 no longer correspond to the configuration
  fields in these memory-layout files: do not claim the copied image changes
  mode successfully. The original mode remains at file offset 0x4120.
- 0x401390 obtains the current module path and its short path, reads COMSPEC,
  constructs `/c del <module> > nul`, launches the command processor with
  creation flags 0x0c and resumes the child thread. This is a self-deletion
  attempt associated with the unwanted loader, rather than an unrelated
  file-deletion API reference.
- Mode 1 obtains DLL resource 101, writes it beneath the system directory
  using helpers 0x402460 and 0x4023c0, then calls 0x401260. That routine opens
  LanmanServer Parameters, deletes ServiceDLL at 0x401320 and writes a
  replacement REG_EXPAND_SZ path at 0x40133e. It then passes the dropped DLL
  path to 0x401150: a host is selected from iexplore/notepad/calc, created,
  and given a VirtualAllocEx buffer populated by WriteProcessMemory.
  GetProcAddress resolves LoadLibraryA, and CreateRemoteThread at 0x40123d
  receives that function and the remote DLL-path buffer. This is a traced
  service hijack/injection capability; it is not the initial mode-3 path.
- Mode 2 installs/dispatches a separate named service using 0x401fd0 and
  0x401510. Mode 4 calls 0x401b90, which extracts the resource and invokes
  the same DLL injector. The retained hostile traits cover the specific
  service-DLL hijack, Active Setup branch and loader cleanup; four hostile
  IDs already provide the requested coverage, without adding a speculative
  C2, theft or ransomware claim.

## Damage and obfuscation

66b8 and 7eae contain identical DLL/101 resources at file offset 0x5060,
length 39936. The embedded PE has no imports or executable sections and its
entry RVA 0x741a points into zero bytes. Most of its image is erased. The
remaining StormAttack banners and `STORM:%d|%s|%s|%s|%s` configuration format
corroborate identity, but no working traffic-flood or network-command path
can be recovered from this DLL. 7d1f has an entirely zero-filled .rsrc and
therefore no embedded DLL to recover at all. Resource API findings describe
the remaining loader code, not successful extraction from those resources.

7eae adds an executable, writable .htext section and changes three calls
to jumps. Each target calls the original routine, executes register filler,
then jumps back to the original continuation:

| Patched call site | Trampoline | Original callee | Continuation |
| --- | --- | --- | --- |
| 0x40115e | 0x40f696 | 0x4010c0 | 0x401163 |
| 0x401eb0 | 0x40f000 | 0x401150 | 0x401eb5 |
| 0x401f03 | 0x40fbdb | 0x402320 | 0x401f08 |

The filler includes 252 `xchg ebx,ebx` instructions from 0x40f005,
256 `xchg dl,dl` instructions from 0x40f1fd, 220 `mov bx,bx` instructions
from 0x40f3fd, and long balanced push/pop, redundant OR and cancelling
increment/decrement runs. These are instruction padding around real calls,
not encrypted payloads. The GUID printf format at file offset 0x43b4 also
produces a URL-decoded fact in cleave; it is ordinary formatting syntax and
does not establish intentional encoding or runtime decoding.

## Trait changes and controls

- Extend the existing self-move rule with 16-bit MOV encodings, preserving
  the byte-register matcher. Require at least 32 contiguous instructions
  wholly within an executable PE section. The 16-bit form preserves upper
  register bits in long mode as well.
- Add a suspicious self-exchange padding rule, requiring at least 32
  adjacent same-register byte/dword exchanges in executable PE section
  bytes. Restrict its scope to x86; 32-bit writes can clear upper register
  halves on x86-64. It requires no name, fixed address, banner or endpoint.
- Make the `.htext` RWX label observation notable. A chosen label and
  permission bits establish layout; the new instruction matchers carry the
  supported concealment inference. Existing layout and family consumers
  retain the same matching membership.

`check.py SCRATCH_DIRECTORY PADDED_SAMPLE` generates 22 inert PE controls:
both self-move forms, alternate opcode directions/registers, 31-instruction
near misses, moves/exchanges between different registers, x86-64 scope,
non-executable data, overlays, section-boundary crossings, ordinary NOP
alignment, both behaviors together and a renamed real sample section.
All pass. See `control-results.json` and `sample-results.json` for recorded
outcomes. Each original was scanned before and after edits and received
exactly one `.MALICIOUS` marker beside its full supplied path.
