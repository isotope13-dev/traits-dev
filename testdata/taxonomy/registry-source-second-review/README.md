# Registry-source second review

No specimen or decoded stage was executed. The controls exercise rule meaning,
not runtime exploit success. `check.py` copies controls outside test-path
suppressors before scanning them. Run it from the repository root:

```sh
python3 testdata/taxonomy/registry-source-second-review/check.py
```

## Identifications and judgments

- **invoice.pdf.lnk — MALICIOUS.** The Shell Link targets Windows PowerShell,
  requests `Unrestricted` policy, minimizes without activation, and presents a
  PDF-style name and Edge icon. `MkZib` reverses its input. `fYPTozHjY` reverses
  the input and then reverses successive two-character chunks, including its
  one-character tail. Applied to the configured string, this reconstructs
  `https://transfer.sh/get/MYsFUC/rb.hta`. The script derives the last URL
  segment, joins it to AppData, requests TLS 1.2, downloads with `wget`, writes
  the response using `WriteAllText`, invokes the resulting path with `&`,
  sleeps three seconds, and removes it. This is a concealed document-lure
  downloader, not an overlay extractor. Invocation success and the HTA's
  further behavior are unknown. Forager exhausted retries fetching the URL.
- **ShieldCrash.cpp — BENIGN research source.** SHA-256 matches the source
  retrieved from the author's public repository exactly:
  <https://github.com/MSNightmare/ShieldCrash>. Its documented purpose is an
  arbitrary file-read proof of concept, and the traced source implements that
  purpose. `wmain` converts the caller's requested path to an NT path; creates
  permissive hidden working objects; builds shadow object directories and
  symbolic links; writes a ZIP resource; and copies `ntdll.dll` into an NTFS
  stream. A worker loads `MpClient.dll`, starts a targeted Defender scan, and
  requests cleanup. Directory notifications time alias removal/recreation,
  CLFS-file deletion and file renaming. A mount-point reparse and object-manager
  stream link redirect privileged file access to the caller's path. The code
  maps the resulting file and copies its contents beside the executable before
  cleanup. The ZIP resource and supporting headers are absent from this source
  artifact. No hidden implant, exfiltration, persistence, or remote control was
  found. Deployment authorization is unknown; the exploit remains dangerous.
  All supported hostile exploit findings are retained. The source does not
  demonstrate disabling Defender, so the four findings retain T1068 without
  the unsupported T1562.001 mapping.
- **demo-pkg 1.0.0 wheel — MALICIOUS startup downloader, declared fixture.**
  The ordinary package initializer is only a docstring. Wheel installation
  places `demo-startup.pth` directly into site-packages through `.data/purelib`.
  Python processes its import-prefixed line at interpreter startup, even when
  the package is never imported. The line checks a hidden `/tmp` sentinel,
  Base64-decodes a literal, XORs each decoded character with `0x5A`, joins it,
  and executes the reconstructed source. The source writes the sentinel first,
  then calls `subprocess.Popen` with a shell command that downloads an agent
  into a hidden temporary file and runs `python3 ... --daemon` after successful
  download. Both standard output streams go to `DEVNULL`, and
  `start_new_session=True` detaches the child. The sentinel prevents retries
  even when the first download fails. The configured address is in TEST-NET-1,
  and the metadata, generator and initializer explicitly describe a threat
  fixture. These are mitigating provenance clues, but no trusted fixture origin
  or confined deployment was established: this is an installable, active hook
  with no lab-only guard. Forager's required all-wheels request for
  `pkg:pypi/demo-pkg@1.0.0` returned no release metadata; its browser fallback
  failed to initialize. The fixture claim alone does not justify a benign
  label. No credential theft or exfiltration is inferred.

## Rule corrections and retained coverage

- Generic HTTP command/API references, policy relaxation, `Substring`, and
  file-write/call-operator observations retain notable capability findings.
  They do not independently establish a downloader objective or overlay access.
  Two equivalent policy matchers are consolidated into the broader canonical
  observation, and exact consumers are updated.
- The former `download-and-execute-comp` required only independent downloader
  and execution references. It did not bind a response to execution or require
  an abuse context. Its observation remains as a notable co-occurrence finding.
- Both prefix and postfix reverse-index joins are supported as neutral string
  operations. Reversal plus downloading is suspicious and explicitly describes
  co-occurrence; the matcher does not bind a reversed value to a URL. The
  stronger concealed downloader, invocation and removal chain adds a hostile
  cleanup finding. Reverse-plus-evaluator attack coverage is retained.
- A nearby `:stream` literal does not make a `FileRenameInfo` operation an ADS
  rename: ShieldCrash renames the primary file to an ordinary temporary path.
  The rule now names the supported co-occurrence, preserving the matcher and
  its self-deletion consumer. Thread API names in commented-out code remain
  references, without claims of active context mutation or suspension.
- SID construction is not a privilege check; hidden-file creation is not
  necessarily temporary-file creation. Those observations and thread
  configuration/lifecycle references are placed with their actual subjects.
- Existing priority and DACL observations gain native source coverage, and an
  actual native file-deletion call gains a notable observation. Defender
  exploitation composites require scan/cleanup and object-manager mechanisms
  rather than attacker-selected `WD_*` names. A renamed source control checks
  retained exploit coverage.
- Python startup hooks reactivate independently of login. The firing startup
  composites move to system Python startup. Base64-shaped content remains
  visible through the canonical encoding observation and a neutral `.pth`
  content composite. The old unanchored fragment matcher could describe part
  of a larger non-Base64 literal as a whole encoded literal; it is replaced by
  the existing complete-literal matcher.
- `shipped-pth-executes-encoded-payload` formerly accepted a subprocess import
  as its execution leg. The `base64-data.pth` control demonstrates that false
  hostile match. The corrected rule requires an executable startup import and
  actual `exec` evidence; encoded-execution positives remain covered.

## Limits

The LNK receives two hostile findings: document masquerade and concealed
invocation/removal. A third hostile finding is not manufactured from ordinary
HTTP and execution references. The static analysis confirms the actual
source-to-file-to-invocation chain manually, but LNK facts do not expose
PowerShell variable provenance. Regex co-occurrence cannot prove arbitrary
variable equality. Neutral findings cover the individual operations and their
co-occurrence. The unavailable HTA prevents claims about its later objectives.

For the wheel, file facts recover the first Base64 layer but not the following
character-XOR transform. The manually decoded stage proves HTTP downloading,
shell creation, stream suppression, session detachment and a sentinel write.
Those operations are matchable when scanning the recovered source; the
original wheel currently exposes only the outer loader/startup observations.
A general decoder improvement is needed to propagate these stage findings;
key- or endpoint-specific signatures were deliberately avoided.

## Scan comparison and validation

Counts are hostile/suspicious, including promoted archive findings.

| Artifact | Judgment | Before | After | Classifier probability before → after |
|---|---|---:|---:|---:|
| invoice.pdf.lnk | MALICIOUS | 2/6 | 2/1 | 0.9977048 → 0.9986867 |
| ShieldCrash.cpp | BENIGN | 4/0 | 4/0 | 0.9934440 → 0.9914421 |
| demo-pkg wheel | MALICIOUS | 3/0 | 3/0 | 0.9990872 → 0.9990872 |
| wheel startup .pth | MALICIOUS behavior | 3/0 | 3/0 | See scan-comparison.json |
| wheel initializer | BENIGN content | 0/0 | 0/0 | See scan-comparison.json |
| wheel METADATA | Declared fixture metadata | 0/0 | 0/0 | See scan-comparison.json |

The classifier continues to flag the three outer artifacts. ShieldCrash is the
remaining verdict disagreement: its real exploit primitives are retained while
the artifact is judged a public research source. The engine reports limited
source flow recovery, which the manual execution-path review addresses here.
The installed model also reports feature-schema v18 versus current v21; new
features require a model update, independently of rule correctness.

The old LNK download/execution hostile rule loses its unsupported intent claim;
its capability evidence remains. The new hostile cleanup rule covers the
specimen. The two wheel startup hostile IDs move without losing the specimen's
coverage. All hostile findings on two existing malicious LNKs, two native
process-ghosting/hollowing fixtures, and the existing XOR-exec fixture are
retained. A separately renamed ShieldCrash source retains all four exploit
findings. Fourteen focused controls pass, including a Base64-data-only .pth
that lost its false hostile match and an encoded-execution .pth that retained
its attack finding. Existing ordinary shortcut behavior remains free of hostile
findings. `scan-comparison.json` records the counts and external controls.

Ancestor selectors of HTTP client and process creation were inspected. Their
other required roles and effective file/type scopes remain necessary; none
uses the newly migrated LNK reference grouping as two independent roles.
The one inspected ancestor consumer with `needs: 2`,
`github-contents-polled-mailbox-c2`, excludes standalone LNK inputs and also
requires Rust reqwest, a GitHub write flow, authorization, and an unbounded
loop. Its file scope does not pool unrelated archive members. Its selector
therefore cannot consume two of the new standalone LNK observations here.
