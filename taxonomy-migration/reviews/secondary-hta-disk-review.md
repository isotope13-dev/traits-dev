# Secondary review: disk zeroing and two HTA launchers

No family or malware attribution is established. Classification uses only
supplied code; filenames and registry/MSI campaign labels do not gate verdicts.
Samples were read in full, inspected through rizin, and analyzed with
`atomscan` and `cleave facts`. None was executed.

## Identities and judgements

| SHA-256 prefix | Identity | Judgement | Hostile | Suspicious |
| --- | --- | --- | --- | --- |
| 4ae13037bfed | Two-line POSIX dd disk-zeroing script | BENIGN | 0 | 0 |
| 1d3733e6248e | Registry-backed JScript HTA PowerShell launcher | MALICIOUS, suspected only | 0 | 2 |
| 42377a6e3a60 | Concealed JScript HTA local MSI launcher | MALICIOUS, suspected only | 0 | 3 |

The disk script unconditionally overwrites `/dev/sda` from `/dev/zero` until
an error or end of device. This is destructive when run with write access,
but legitimate disk sanitization uses the same command. The supplied code
contains no evidence of sabotage or unauthorized execution. The malware
conviction is overturned; neutral disk-writing observations remain visible.

The registry HTA writes a User environment item, reads an HKCU registry value,
removes an arbitrary literal substring, and passes the result to PowerShell's
encoded-command option through Win32_Process.Create with a hidden-window
configuration attempt. The registry value is absent from the sample, so there
is no executable payload to decode or attribute and no evidence of a download.
It constructs Create input parameters rather than Win32_ProcessStartup, then
assigns ShowWindow to that object; this likely fails before the final call.
The traits therefore describe code syntax/co-occurrence and suspicious intent,
not successful payload execution, C2, network acquisition or persistence.

The MSI HTA minimizes, shrinks and moves its window off screen. It attempts
hidden `cmd /c del` on an MSI's Zone.Identifier stream, then attempts two
quiet installations of the same existing TEMP MSI: synchronous WSH Run and
Shell.Application.ShellExecute. It closes its own window afterward. No bytes
are downloaded, unpacked or written. No MSI is supplied. MOTW deletion and
window minimization alone are ordinary operations; the concealed installer
combination remains suspicious, not a confirmed hostile payload chain.

## Trait changes and placement review

Neutral device-zeroing atoms moved from impact/wipe to fs/disk/raw. Device
path/inventory observations moved to fs/path/device/storage. The existing
broad disk-impact profiles now require a second destructive act, recursive
filesystem-root deletion, rather than convicting on disk sanitization alone.
Overlapping zero-device command matchers were canonicalized.

Neutral HTA atoms moved from C2/dropper and anti-static namespaces to environment
access, string replacement, property assignment, process creation, command-line
options, executable paths and window control. The former WMI "remote download"
composite became a neutral HTA/Create co-occurrence observation. The two
suspicious registry profiles now require registry access, substring stripping
and encoded PowerShell syntax; the execution profile additionally requires HTA
markup and hidden Create syntax. Exact marker and registry-value names are not
required. COM ShellExecute moved to the desktop-opener mechanism. Generic Run
syntax moved to control-flow dispatch. Embedded JScript declaration moved to
runtime metadata. MOTW deletion remains a neutral operation; the concealed MSI
profiles moved to execution/lolbin and execution-policy bypass, at suspicious.

Exact and local consumers were rewritten for the moved canonical IDs. Relevant
ancestor selectors were checked: process execution, subprocess, desktop opener,
window control and executable paths. Leaf budgets were preserved by reviewing
and canonicalizing overlapping atoms, or moving independently misplaced
ShellExecute, COMSPEC, subprocess and property observations to their subjects.
The redundant text subprocess.call fallback now uses the parsed call atom, so
comments cannot establish that call. Source files retain their other rules.

## Focused checks

Static controls were generated under the session scratch directory and scanned
alongside the three samples. They were never executed.

| Control | Expected and observed result |
| --- | --- |
| dd zero input to /dev/null, count=1 | 0 hostile, 0 suspicious |
| dd zero input to /dev/sdb | 0 hostile, 0 suspicious |
| Administrative minimized HTA: User environment, ordinary split/join, hidden notepad WMI call | 0 hostile, 0 suspicious |
| Minimized HTA quietly installing an approved local MSI | 0 hostile, 0 suspicious |
| HTA attempting to unblock an approved MSI without concealed installation | 0 hostile, 0 suspicious |
| Registry HTA with different marker, environment and registry labels | Same 2 suspicious findings |
| Installer HTA with different application and MSI names | Same 3 suspicious findings |
| rm -rf /* together with dd disk zeroing | Both revised hostile disk composites match |

`cleave test-rules` measured precision 7.9 for dd-fill-block-device-wipe and
9.0 for unix-block-device-wiper, above the required 3.5 authoring threshold.
Final atomscan output preserves observable capabilities without unsupported
network/download/dropper claims. These focused controls establish the tested
boundaries; they are not a claim that the entire external software corpus has
been scanned.

Fixture expectations now use the canonical IDs and suspicion-only HTA floors.
The disk-mechanism corpus keeps a capability floor rather than assuming every
erasure primitive is sabotage; the supplied disk control also has a permanent
benign regression fixture. Windows interpreter syntax retains PowerShell flag
coverage needed by unrelated ClickFix profiles, while cmd execution atoms
continue to describe cmd command-mode syntax specifically.
The historical wipe.sh fixture prints its dd command through echo; its old
hostile floor was also corrected to the observed suspicion-only signals.
