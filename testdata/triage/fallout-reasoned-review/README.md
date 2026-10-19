# First reasoned review

The specimens were inspected statically with Cleave facts, rizin and Capstone.
No specimen was executed. The supplied sandbox pages were inaccessible; the
verdicts below follow from the recovered code rather than their scores or the
collector-assigned family names.

| SHA-256 prefix | Identification | Verdict |
| --- | --- | --- |
| `7d9580cd3bcb` | Damaged HanSoft myRunner executable-association hijacker | MALICIOUS |
| `783c4f0d9d04` | Windows socket-tasked bot/worm, matching an Avzhan signature | MALICIOUS |
| `0565aa6c3a70` | Trojanized dnsub source archive | MALICIOUS |

## Evidence and limits

**myRunner.** The MFC timer handler at VA `0x401420` calls `0x4063c0`.
That routine opens/creates the EXE shell-open association at `0x406465`,
prepares its replacement executable with the file-copy helper at `0x405440`,
removes its extension with `strrchr` and a NUL store at `0x40650f`, appends
the quoted `%1` / `%*` wrapper arguments, and calls the registry-string writer
at `0x404610`. Its `RegSetValueExA` call is at `0x404644`.
The implementation also handles text-file associations and QQ installation
paths. POP3 RETR/UIDL wire commands and socket routines survive in the unnamed
mapped section. A substantial code region at RVA `0x9000` is zeroed: timer
calls to update/mailbox targets in that region cannot establish a working
attachment launcher. Neither the missing launch gate nor the corresponding
mailbox-loader hostile trait should be inferred from surviving strings.
The verdict concerns the surviving hostile implementation in damaged malware;
successful execution of this exact image is not established.

**Windows bot/worm.** The CRT entry at `0x4093bf` reaches `0x408640`.
The dispatcher receives a 0x404-byte record at `0x407b7d`, copies it and
branches on its task number. Task 8 reaches `0x407f02`, passing the forced
immediate reboot command to `system`. Other cases download/launch a file or
start task workers. The receive call uses the WS2_32 delay-import IAT entry
at `0x4045c0`; its descriptor at `0x4097d0` and ordinal table at `0x4098d0`
identify it as recv (ordinal 16), independently of the opcode trait's name.
The security-name calls at `0x4086ea` reach `0x408572`, which compares process
snapshot names, opens the selected PID and calls TerminateProcess at
`0x40862d`. The remote-copy routine tries admin$ and C$/D$/E$/F$ destinations,
then formats an AT command and invokes WinExec at `0x406eaf`.
The drive propagation path writes AutoRun directives and copies its own image
under a recycle-bin-style directory. The loop at `0x404ab0` XORs 0x2200
embedded bytes with 1 before the writer at `0x404ad0` saves them. The decoded
image identifies as the Windows default screensaver; it is not evidence of
an additional ransomware payload. The outer image claims Avira AntiVir in
its version resource. No WannaCry, Remcos or Gh0st lineage is inferred.

**dnsub.** `main.go` replaces the expected scanner startup with a synchronous
`exec.Command(...).Run()` PowerShell invocation hidden behind 1,832 spaces.
Its command saves an HTTPS response to a public Pictures path, certutil-decodes
that same file to a PowerShell script, and starts that script with execution
policy bypass and a hidden window. This unrelated, concealed payload chain
establishes malicious intent without knowing the remote script's contents.
The snapshot lacks imports/declarations needed to build the application, so
this is a malicious source implant rather than a verified runnable release.
The surviving helpers perform ordinary DNS lookups, HTTP banner requests and
CSV output. The workflow updates LOG and pushes repository changes; it does
not establish token theft. ZIP member CRCs and all five PNG chunk CRCs are
valid, with no bytes after the PNG IEND chunks.

## Trait corrections and controls

- POP3 command atoms search mapped sections irrespective of their names;
  headers and overlays remain excluded. The command-set composite accepts
  the existing Winsock client profile, including ordinal imports. Its
  description now states that evidence accurately.
- The Go PowerShell constructor moves from `process/create/direct` to
  `process/create/subprocess` and requires argument zero to be the executable.
  A new launch observation follows the receiver to `os/exec.Command` with
  that executable argument. Both concealed-loader hostile composites require
  this actual launch, so constructing a command or running an unrelated child
  cannot substitute for it. Run, Start, Output and CombinedOutput are covered.
- The `direct/` ancestor consumer in the source-structure composite explicitly
  retains the moved PowerShell observation. Its other ancestor consumers are
  JavaScript or Python scoped. Exact consumers and the three existing Go
  dispatch fixtures are updated. New subprocess findings do not add an
  observation to files lacking the existing Go command-construction finding.
- The directory-budget audit retires `subprocess::popen-import`: it neither
  proves process execution nor binds the imported name to Python's subprocess
  package. The engine's notable import fact retains the precise declaration.
- A stdin/stdout attribute assignment moves from process creation to
  `process/fd/stdio`, with an evidence-limited name and description. Two
  existing read/write transfer rules move unchanged from that directory to
  `process/io/stream`; their reverse-shell consumer follows them. There are
  no direct selectors of either moved leaf. All destination directories
  already exist; no directory budget is raised or new partition invented.

`check.py` generates private mutation controls in the supplied work directory:
named/unnamed sections, named/ordinal Winsock imports, absent UIDL and
overlay-only commands; executed/unstarted/visible/commented Go launchers,
PowerShell as an unrelated argument, an unrelated child launch; stdin
configuration, import-only Python and bound/unbound stream transfers; and a
bot dispatcher mutation that preserves its security-name and reboot strings.
All 20 focused controls passed. The existing three Go dispatch controls also
retain their expected findings. Final atomscan rescans with this checkout
retain hostile/suspicious counts of 2/2, 6/1 and 2/1 respectively.

Judgment marker lines:

```
myRunner hijacker: restore POP3 coverage for unnamed sections
Windows bot/worm: no change
dnsub trojan: require an invoked PowerShell command
```
