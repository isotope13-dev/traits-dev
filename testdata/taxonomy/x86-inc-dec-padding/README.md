# Canceling byte-register instruction padding

Run `python3 testdata/taxonomy/x86-inc-dec-padding/run.py` from the repository.
The 38 generated PE controls cover every legacy byte register in both INC/DEC
orders on x86 and x86-64, plus short, interrupted, different-register,
non-executable, section-crossing and ordinary-code negatives. All passed.
The fixtures contain synthetic instruction sequences and no malware payload.

## Sample review

All three reviewed files are **MALICIOUS StormAttack native loaders**:

| SHA-256 | Size |
| --- | ---: |
| `12cebb6250561085c25342dca2568b48d6eb0e5099925b75d5ef4cd497597caf` | 65558 |
| `e238b3787794a67fa13e3fb569db423d49e9792a9305b1bbeb93a7299e8866d0` | 65558 |
| `2c06f2c41c2a0ff1bf3f60b7121f45c9803691d59f01551f381ac97a7cf43c22` | 65536 |

Each received fresh atomscan, cleave facts, decoded-string extraction, PE
structure inspection and rizin disassembly. Verdicts derive from code effects;
ML probabilities and the supplied sandbox scores were not proof. The linked
Triage reports could not be retrieved. No sample was executed.

The loader identifies itself with StormAttack server/welcome banners and a
StormServer.dll payload name. The collection filename does not establish
Remcos, WannaCry or Elex identity. Samples 12ce and e238 have identical .text,
.data, .rsrc and .htext bytes. Their 28 differing bytes are in the .rdata GUID
area at file offsets 0x3079–0x309a. Sample 2c06 retains the same .data and
.rsrc, but changes padding, raw section extents and call detours.

### Execution paths and effects

All addresses below are image VAs, with base 0x400000.

* CRT entry 0x402674 calls 0x401cb0 at 0x4027a3. The mode field at
  0x404120 is 3, selecting 0x401f7a: call 0x401900 (Active Setup), then
  0x401390 (self-delete). These are code paths, not just import coincidences.
* 0x401900 obtains a GUID string from 0x401840, constructs a Windows-directory
  executable path and an HKLM Active Setup Installed Components subkey, and
  writes its StubPath via RegCreateKeyA / RegSetValueExA at 0x401a26/0x401a4b.
  The later CRT I/O reads the current image, patches fixed offsets, writes a
  copy, and launches it through CreateProcessA at 0x401b7e. Fixed-offset patching
  and GUID bytes overlapping the IAT mean successful reactivation is not proven.
* 0x401390 obtains its own module path, shortens it, reads COMSPEC, appends
  `/c del` and `> nul`, and calls CreateProcessA at 0x4014b8. It adjusts
  priorities and resumes the suspended cleanup thread. This follows the
  persistence-registration branch in the configured mode.
* Alternate mode 1 calls 0x402460 to extract resource DLL/101, writes it via
  0x4023c0, calls 0x401260 to delete and replace LanmanServer's ServiceDLL
  with the constructed System32 DLL path, then calls 0x401150 for injection.
* 0x401150 selects calc/notepad/Internet Explorer through 0x4010c0, starts
  the child, allocates memory with VirtualAllocEx, writes the DLL pathname
  with WriteProcessMemory, resolves kernel32!LoadLibraryA, and passes that
  resolved address plus the remote pathname to CreateRemoteThread at
  0x40123d. Injection success is conditional, not an observed runtime result.
* Mode 2 contains service-copy/create/start and service-dispatch branches;
  mode 4 extracts the resource and calls the same DLL-injection routine.

All three embed the identical 39936-byte damaged PE at file offset 0x5060.
Its .data contains only 1943 nonzero bytes; .rsrc and .reloc are zeroed. Its
entry RVA 0x741a resolves into zero bytes in non-executable .data, while import
and export directories no longer resolve to usable tables. Family strings,
HTTP templates and URLDownloadToFileA references survive. They do not prove a
working C2, downloader, DDoS loop or ransomware in these copies. Existing
hostile findings correctly describe loader code rather than payload success.

Decoded-string inspection recovered a supposed URL-encoding layer at 0x43b4.
Disassembly shows this is the snprintf GUID format at 0x4018ce, not a URL or
network operation. The engine-emitted percent-decoding observation supplies
no additional behavioral evidence; no YAML shadow or suppression was added.

### Missing obfuscation coverage

In 12ce/e238, 0x40190a jumps into .htext at 0x40f662, calls GUID generation,
runs arithmetic filler, and returns to 0x40190f. Another detour at 0x401c43
calls 0x401000 through 0x40f000 and returns to 0x401c48. A contiguous run at
file offset 0xf1df contains 218 DEC CL / INC CL pairs. In 2c06, the cleanup
call at 0x401f8f is detoured through 0x40f000; padding starting at file offset
0xf005 contains 138 DEC CH / INC CH pairs before returning to 0x401f94.
These restore register values while changing arithmetic flags. They supplement
the already detected self-MOV and self-XCHG filler.

The new suspicious trait requires 32 adjacent same-register byte INC/DEC pairs,
either order, wholly contained in an executable PE section. It requires neither
.htext, family strings, collector names nor an exact file size. Ordinary
arithmetic, a different-register pair and data-only bytes are near misses.
Ancestor consumers of instruction obfuscation were audited; broader consumers
are source-language rules outside the new PE/DLL scope. Fresh cleave report
diffs for every target add exactly this trait and remove nothing. Atomscan
rescans confirm it on all three, retaining four hostile loader findings.
