# Native PE review

Judgments follow offline PE inspection, Capstone disassembly, Rizin function
analysis, atomscan reports, and cleave facts. No specimen was executed and no
specimen-supplied endpoint was contacted. These are local executables without
fetched package dependencies. The supplied Triage pages were inaccessible;
neither their scores nor antivirus labels establish the judgments below.

| SHA-256 | Identification | Judgment | Final unique hostile / suspicious traits |
| --- | --- | --- | --- |
| 49cadb3c78c6a0ff540db1f51ea9c857dfe62fdd046da2940055891771b9b039 | StormAttack installer with largely zeroed embedded DLL | MALICIOUS | 3 / 2 |
| 06504e57f3f59a43c5b773039f31eb3e20fa41817cb84a528547eafad709fe03 | Eupdate Helper 4.0.1.0, yztcsn | BENIGN | 0 / 1 |
| d710a7977e1c96d5fb991deb3534e64c812d5330dae3ae455c0b988a39ecffc1 | Same Eupdate Helper build with different trailing padding | BENIGN | 0 / 1 |

Counts deduplicate YAML IDs across each input and its embedded descendants.
They do not change the independent ML model classifications.

## StormAttack

The collector filename does not establish Elex, Remcos, or WannaCry. Embedded
StormAttack banners, the STORM command-format string, and installer code
support StormAttack identification.

- Entry 0x402674 reaches 0x401cb0. The configured mode at VA 0x404120 is 3:
  its branch at 0x401f75 calls 0x401900 and then the deletion helper 0x401390.
  0x401900 calls a GUID generator through the padded trampoline at 0x40f662,
  constructs an HKLM Active Setup Installed Components key and executable
  path, and writes that path as REG_EXPAND_SZ StubPath at 0x401a4b. It reads
  its own executable, changes fields in the copy, writes the new image at
  0x401b26, and launches the copy at 0x401b7e. The deletion helper launches
  COMSPEC with `/c del` targeting its own module path. These are concrete
  unwanted reactivation and cleanup mechanisms, not just imported APIs.
- Other supported configuration modes contain the service-DLL hijack and
  injection paths. 0x401260 constructs a StormServer.dll path, opens
  LanmanServer Parameters, deletes ServiceDLL at 0x401320 and writes the
  replacement REG_EXPAND_SZ value at 0x40133e. Resource extraction at
  0x402460 precedes that routine and 0x401150 in mode 1. The latter creates
  a child, allocates remote memory, writes the DLL path, resolves LoadLibraryA
  and passes it and the remote buffer to CreateRemoteThread at 0x40123d.
  These describe compiled capabilities, not successful execution in mode 3.
- Resource DLL/101 starts at file offset 0x5060 and is exactly 39936 bytes.
  About 94.5% is zero; its entry at RVA 0x741a is also zeroed. Family strings
  remain, but no working network dispatcher or DNS flood implementation can
  be recovered from these bytes. Retain the explicitly identity-only
  DNS-labeled module finding; add no flooding or live-C2 claim.
- Reachable .htext trampolines contain hundreds of self-moves, cancelling
  increment/decrement pairs, and redundant OR instructions. 0x40f000 calls
  the original helper, runs the filler, and jumps to 0x401c48; 0x40f662 calls
  the GUID generator and returns via 0x40190f. This is instruction padding,
  not an encrypted or compressed payload. Add a suspicious detection for
  at least 32 contiguous byte-register self-moves in an executable PE section.
  It requires no section spelling, endpoint, banner, or collector name.

The pre-existing Protected Storage finding at file offset 0x42de came from
`C:\Program Files\Internet Explorer`, used to choose an injection target.
There is no PStore factory or enumeration code. Replace the bare substring
matcher with a notable composite requiring both the canonical standalone
Internet Explorer label and a Protected Storage factory reference. Its
description explicitly reports co-occurrence, not enumeration. Existing
consumers keep the same ID; unrelated browser paths stop firing it.

## Eupdate Helper

Both files have byte-identical headers and mapped sections through offset
0x21bff. Their first difference is at 0x21c95, after the author release tag
and outside mapped sections. Behavior analysis therefore applies to both.

- 0x412964 fetches an info.txt manifest and parses version and downurl fields.
  The replacement acquisition path requires MessageBoxW at 0x412c6e to
  return IDYES (6), checked at 0x412c77. The other branch declines the update.
  The accepted path downloads a replacement, checks its MZ bytes, renames
  images and launches the replacement. Transport and authenticity checks
  are weak; there is no captured hostile replacement or concealed launch.
- The proxy listens on port 8000, obtains upstream account information,
  relays ESET update traffic, filters manifest routing sections at 0x417c40,
  and returns 404 for .signed requests at 0x4146c7. These do not show client
  verification patching, hostile update substitution, or local secret theft.
- The decoder at 0x416bb0 computes
  `out[i] = in[i] XOR key XOR ((31*i + 7) & 255)`. Four callers at
  0x415cc8, 0x415d14, 0x415de3 and 0x415e2f recover `encrypt`, `type`,
  `/id.html` and `id.1yz.me`; the URL construction appends port 4046.
  This serves account-list acquisition, rather than a remote-command channel.
- The Run write at 0x415af0 registers its current image; the elevation path
  uses normal ShellExecuteW runas consent. Bind failure at 0x413108 leads
  to TCP-table lookup, identification of the port owner, and termination at
  0x4132ab. There is no defender-process selection in that path.
- 0x4127e4 opens an executable and 0x4128ff seeks to EOF; 0x41292c appends
  4..11 pseudorandom bytes. 0x415800 copies and launches a standby instance
  with `-standby-mutate`, enabling mutation after the original exits and
  subsequent relaunch. This unusual hash rotation remains suspicious.

The existing traits already describe these capabilities without a hostile
conviction. No updater-specific exception or severity change is warranted.

## Verification

Run atomscan and cleave facts on every original path before edits. Re-run
atomscan with local traits, `--no-update --follow=none --format json` after
edits; assert the counts above and removal of the false PStore finding.

`check.py STORM_SAMPLE SCRATCH_DIRECTORY` generates fourteen static controls
outside the repository. They exercise the instruction-count boundary,
different self-move registers, ordinary moves, executable permissions,
overlay and section boundaries, renamed sections, IE path-only/label-only
and factory-only negatives, and narrow/wide PStore-label positives. All pass.
