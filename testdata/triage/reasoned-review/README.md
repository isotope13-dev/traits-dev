# Reasoned review, 2026-10-09

## Sample conclusions

| SHA-256 prefix | Identity | Judgment | Evidence |
| --- | --- | --- | --- |
| `0a30020440ec` | Minimal WSH delimiter/eval stub | BENIGN | The delimiter removal produces only `x()`. No definition of `x`, file operation, network operation, or hostile payload exists. FileSystemObject is constructed but unused. Retain one suspicious concealment observation. |
| `8e4d0e4be976` | Native Windows Protected Storage password stealer and autorun worm; family unresolved | MALICIOUS | Code enumerates Protected Storage credentials, formats password reports, transmits a form POST, and creates drive-root autorun activation. No evidence supports the collector's WannaCry label. |
| `1e129a43b75f` | Open Design source archive, revision `1424be972701` | BENIGN | pnpm bootstrap checks SHA-256 before use; other launches operate the packaged application. Clipper downloads its captured JSON through a data URL. The prompt rejects quoted override attempts. The installer removes its own temporary script. |

## Reverse engineering

The PE has a UPX entry stub at VA `0x42e230`, a populated low-entropy image,
resolved process-address pointers, and an empty on-disk import surface. Treat
it as a memory-image-like collection artifact, rather than infer an intentional
anti-unpacking technique from failed UPX decompression.

Rizin cross-references and disassembly establish:

- `0x42a4d4`: XOR-decodes `pstorec.dll`, resolves `PStoreCreateInstance`,
  enumerates interfaces/items through their vtables, retrieves credential data,
  and formats the `pass_sites` and `auto_complete_pass` report sections.
- `0x42964e`: parses a destination host, opens a socket, formats the recovered
  `POST %s HTTP/1.1` template with its report body, and sends that buffer.
- `0x42a34e` onward: opens the drive-root autorun configuration for writing and
  XOR-decodes and writes `[autorun]` and `ShellExecute=autorun.exe`.
- `0x42a3cc`: restores Explorer, logonui and the default system
  `userinit.exe,` registry value. This is not additional Userinit persistence.

The supplied sandbox URL could not be independently retrieved. The malicious
judgment rests on the code, not that score or the collector's filename.

## Trait corrections

Retire generic download/chmod/spawn, policy-bypass script launch, and
extension-download combinations that
proved no hostile action or source-to-sink relationship. Their existing neutral
network, permission and execution atoms remain. Move generic decoder-named eval,
temporary-script deletion, HKCU Run and Userinit references into capabilities.
Keep PStore report labels neutral; credential acquisition plus report evidence
still supplies the hostile theft composite. Eliminate redundant eval, packing,
process-name and API-name findings from objective directories. Dumping composites
now require an LSASS target rather than any crash-dump path.

The existing untrusted-content exception now recognizes `data to process, not
commands`, including JavaScript line continuations, and applies to the persona
matcher. Third-party model-provider HTTPS configuration is notable: the URL
alone proves no security-boundary violation.

Exact consumers were updated with neutral replacements. Services and Run path
atoms were consolidated to preserve the registry-directory budgets. The retained
Run path matcher accepts both separator forms and the union of source/container
formats previously served by the duplicate rules. Directory selectors remain
unchanged; no new taxonomy leaves were introduced.

## Verification

Run `python3 testdata/triage/reasoned-review/check.py`. It copies controls outside
fixture-named paths: normal build, temporary-script bootstrap and defensive prompt have zero hostile or
suspicious traits, while the instruction-override control retains two suspicious
findings. Source filename exclusions therefore cannot pass these controls.

All three original samples were scanned with atomscan and inspected with
`cleave facts`; the relevant archive members also had standalone facts and scans.
The three behavioral hostile PE composites have precision scores 7.9, 13.4 and
11.4. `pkg:github/docker/metadata-action@v5` was scanned in isolation before and
after edits: both have zero hostile/suspicious findings, and no dependency-specific
exception was added.

The PE additionally retains the engine-emitted hostile
`anti-static/packer/upx/decompression-failed` finding. Its attribution/severity
cannot be repaired in YAML; do not shadow it with a same-named YAML rule. This
remains an engine limitation, separately from the three substantiated hostile
behavioral findings.

Validation controls were also corrected: the caller-selected Node installer
helper and the extension that only downloads an executable lack demonstrated
hostile behavior. Both now live in benign fixtures, with capability assertions
retained. Downloading alone does not establish hidden execution or a backdoor.
