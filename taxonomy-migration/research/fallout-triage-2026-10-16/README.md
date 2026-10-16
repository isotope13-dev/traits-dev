# Fallout sample review, 2026-10-16

Judgments are based on static reverse engineering, not the ensemble score.
No sample code was executed. Atomscan and `cleave facts` were run on all
three supplied inputs. Rizin analysis and PyInstaller extraction were used
to distinguish native program behavior from bundled runtimes.

## 2556ed5385c26698e68183812c65b3e2c97437f7984512457bc2eeacfe3887df

**MALICIOUS: native Delphi IRC bot and NetBIOS share worm.** No narrower
family attribution is established. The collector's list of malware names is
not evidence for any of those families.

The PE entry at VA 0x40a270 creates a single-instance mutex, copies itself
into the system directory, and writes a replacement `system.ini` boot shell
containing Explorer and its own executable (0x40a380-0x40a399). The network
share routine at 0x4045f0 loops over usernames/passwords with
WNetAddConnection2A, copies its own module to remote `Setup.exe` paths at
0x404756, and invokes a remote job helper at 0x403d7c. That helper computes a
remote job time and calls the dynamically resolved NetScheduleJobAdd.
The IRC handler at 0x408964 processes operator commands, downloads files,
launches them with ShellExecuteA (0x409316), and sends status to IRC.
The infection report at 0x4047d1 is thus executable worm logic.

The appended PyInstaller archive contains a separate Python 3.7
`downloader_req` program. Its marshaled code was parsed with xdis, not run:
it takes a URL and destination from argv, calls requests.get(timeout=10),
and writes the response in binary mode. This utility and its CPython/OpenSSL
libraries do not establish malware by themselves. The native wrapper does.
The native IRC status ` :Files Infected : ` at 0x409ff4 is not a fake AV
verdict; its former scareware finding was wrong.

The two behavioral hostile rules have measured precision 5.8 (share worm)
and 6.9 (IRC infection reporting), exceeding the 3.5 authoring floor.
Atomscan also emits `anti-static/packer/upx/decompression-failed` from its
engine, outside the YAML rule catalog. This is an unpacker diagnostic, not
independent hostile behavior. No YAML shadow was introduced to suppress an
engine-generated finding; its severity requires an engine correction.

## f23b974860bd810b22290f70b1ab198b3b92d0d470e19255559d4df6b81eefd5

**MALICIOUS: QQpass / myRunner launcher replacement trojan.**

The native code at 0x4063c0 reads executable and text-file open-command
associations, locates Tencent QQ via its installation registry key, constructs
TIMPlatform.exe and the visually similar TIMP1atform.exe, and replaces the
launcher while retaining a path to launch the original. The routine at
0x407210 installs RunServices entries using browser/input-process names;
RegSetValueExA is called at 0x407cac. The image contains mailbox/control and
update configuration consistent with the existing myRunner signatures.
These executable changes, rather than the blank sections or old timestamp,
justify the judgment.

QQpass is corroborated as the recognized family by a different sample with
the same update/configuration endpoints in this
[Triage report](https://tria.ge/260920-rac5lsaj8x/static1). That report is
family corroboration, not a claim that its hash equals the reviewed input.
The existing identity catalog was moved from the build name `myrunner` to
`qqpass`, preserving matchers and file scope. A generic Tencent registry-key
atom moved to the registry-key capability catalog with its original unnamed
section and size bounds. The existing Elex consumer was updated.
The three retained hostile composites scored 6.8, 7.6, and 11.8 in test-rules.

## c8946ceef78e2d9b273066d9f42fc8464f669308153ec3c8e17c6c8a95cd6b24

**BENIGN: UiPath Community.Activities source archive at 97f06b962af8.**

Direct byte comparisons against raw.githubusercontent.com at the pinned
commit matched all three inspected upstream files:

| Member | SHA-256 |
| --- | --- |
| Script/AutoHotkey.Interop/x86/AutoHotkey.dll | f993218904db92fd8333541ce93b8011f61827ef8b504d27f545d7e02d0e3081 |
| Tools/localization_utilities/synchronize_localization.py | 47d7f8e86f023bb487094af7e19067f53ba0ed67a68a78b1791bbc1ac7900863 |
| Tools/localization_utilities/dist/synchronize_localization.exe | 2c3228d0997c5c230ff501b88dd1423cee591962a64624e70ecfac1a77a3cae5 |

[Upstream commit](https://github.com/UiPath/Community.Activities/tree/97f06b962af8).
The DLL is AutoHotkey_H 1.1.24.00-H022, with its script interpreter exports
(ahkExec, ahktextdll, ahkFunction, ahkgetvar, etc.). Rizin inspection of the
exports and the C# wrapper shows caller-supplied script execution. Clipboard,
keyboard, screen and memory-loading capabilities are its documented public
feature surface, not evidence of a spying script. The
[AutoHotkey_H documentation](https://hotkeyit.github.io/v1/docs/AutoHotkey.htm)
also documents resource-based threads, MemoryModule, and in-memory execution.
Recognition uses product metadata and real exports, independently of basename.
It suppresses API-surface surveillance heuristics, not arbitrary attack rules.

The localization executable's extracted Python 3.6 bytecode agrees with its
shipped source: synchronize keys/comments in localized .resx files. The
bundled PSF runtime/extensions retain stale Authenticode directory entries
after their certificate blobs were stripped. For example, extracted _bz2.pyd
ends at 71168 bytes while its security directory still points at 71680 and
claims 6808 certificate bytes. python36.dll shows the same packaging shape.
Neither is evidence of certificate transplantation. CPython recognition
requires PSF product/publisher fields and an actual runtime or extension ABI.
The raw out-of-bounds-directory property remains notable.

No findings were identified as fetched PURL dependencies. These binaries are
vendored archive members. Both AutoHotkey.dll and synchronize_localization.exe
were scanned independently before and after the changes, as well as inside
the complete archive.

## Detection changes and controls

- Bare PE IRC command evidence moved to communications/irc/command, retaining
  matchers and scope. The protocol composite is notable; objective consumers
  now reference it explicitly. Bare ambiguous NICK/QUIT/MOTD tokens remain
  components. No ordinary IRC transport is labeled C2 on its own.
- Security status phrases moved from scareware into UI message wording.
  Their regex alternatives were split into distinct observations. A verdict
  composite now needs an independent restricted-cleaning demand.
- The input/screen/clipboard API triad moved from browser credential access
  to a notable display API co-occurrence; it requires no browser or credential
  source and establishes no surveillance data flow.
- The resource-loader/runtime-decoder composite was retired. Its case-fold
  table is not a decoder, and resource/thread/executable-allocation APIs do
  not establish a loader chain. Each constituent remains independently
  detectable in its existing capability home; no substitute catch-all added.
- The certificate heuristic was renamed to describe its actual structural
  evidence. Known signature-stripped native runtimes are an exception to
  these two malformed-certificate heuristics, with no archive-wide suppression.
- Directory and exact references were searched across the rule tiers. The
  generic observations removed from objective selectors intentionally cease
  to contribute attack evidence; exact positive consumers were repointed.
  QQpass retains the prior family selector's match population.

Controls were generated and scanned without execution in the task scratch
area. A PE with ordinary IRC command constants matches the notable protocol
composite and fails the worm-report objective. A PE with just the worm status
matches infected-file wording and fails the scareware verdict. Infection
wording plus a restricted-cleaning demand still matches the verdict.
Removing an AutoHotkey product field or required interpreter export prevents
the full library identity. Removing a CPython publisher field or extension
ABI prevents its identity and restores malformed-certificate detection.

Final input and isolated-member scan counts are recorded alongside the task's
raw JSON reports in scratch/triage-fallout/current*.final.json and ui*.final.json.
The judgment marker summaries are limited to 72 characters and live beside
the original samples, never in the trait repository.

## Confirmed final counts

| Input | Judgment | Hostile | Suspicious |
| --- | --- | ---: | ---: |
| 2556ed5385c2 | MALICIOUS | 3 | 1 |
| f23b974860bd | MALICIOUS | 3 | 7 |
| c8946ceef78e, all members | BENIGN | 0 | 0 |

The first count includes the engine-generated UPX diagnostic described above.
Two independent behavioral hostile findings establish the worm judgment.

Marker summaries (verbatim, suitable for the commit body):

```
IRC/NetBIOS worm: remove fake-AV verdict; separate protocol evidence
QQpass/myRunner: correct family name and registry-key taxonomy
UiPath activities: recognize AutoHotkey_H and stripped CPython DLLs
```
