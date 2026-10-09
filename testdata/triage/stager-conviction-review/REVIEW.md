# Second conviction review

Judgments use the code, not filenames, reputation, or the word "malware" in
placeholder hosts. No family attribution or reachable command server is claimed.

| Sample | Identity | Judgment | Current evidence |
| --- | --- | --- | --- |
| bee0b3bccbd4 | PowerShell archive stager and REST-evaluation cradle | MALICIOUS, suspicious-level evidence | 2 suspicious, 0 hostile |
| f6c8d5687297 | Python encoded-code and HTTP-response evaluator | MALICIOUS, suspicious-level evidence | 4 suspicious, 0 hostile |
| dbb0e4d2b09d | DOS first-match self-image overwriter | MALICIOUS | 3 hostile |

## Behavioral reconstruction

PowerShell stops on errors, downloads an archive to TEMP, extracts it, invokes
an EXE from the extracted directory, then evaluates an Invoke-RestMethod
response. It subsequently requests a process-scoped execution-policy bypass and
adds a Defender path exclusion. The previous rule incorrectly claimed remote
instructions ran before the archive program and did not bind a response to eval.
The replacement descriptions state co-occurrence, not inferred flow or ordering.
The placeholder hostname is not a PowerShell .EXAMPLE help directive.

Python decodes `import os;os.system('id')` and passes it directly to exec, then
passes an urllib response body to a separate exec. It writes no payload file.
The decoded command is an ordinary identity query, so an encoded os.system
reference is notable and cannot establish hostile intent. The combination of
concealed code evaluation and remote evaluation supports suspicious findings.
Atomscan still reports its existing `flow-query-incomplete` analysis gap; these
conclusions come from manual decoding and direct parsed calls, not an inferred
source-to-sink relation that the engine could not recover.

The DOS COM entrypoint uses AH=4Eh to search `*.C*`. It opens the default DTA
filename at PSP:009Eh using AX=3D02h, exchanges the returned handle into BX,
sets AH=40h, and adds 62h to DX to point at its own 0100h entrypoint. CL=1Fh
selects a 31-byte write under ordinary CH=0 entry conditions. It overwrites the
first matched host from offset zero and returns through the PSP termination
stub. It neither enumerates a second result nor preserves the victim prefix.
The trailing zeros are padding, not the replicated body. `*.C*` can also match
non-COM files, hence the corrected executable-compatible wildcard description.
Rizin's 16-bit disassembly verified all instructions. Binwalk was unavailable;
full byte inspection exposed no further embedded payload.

## Trait corrections and placement

- Security-policy command text moved from process creation flags to OS security
  policy; environment-rooted EXE paths moved out of DLL hijacking.
- Archive download/extraction/launch co-occurrence moved to neutral deployment.
  Defender exclusions and policy bypasses supply separate suspicious contexts.
- PowerShell help evidence moved to documentation and requires a line-start
  .EXAMPLE directive. Nested REST evaluation requires a real command AST node.
- Direct Base64-to-exec moved from control-flow logic to encoded code concealment.
  Encoded os.system and os.chmod references moved to their neutral operation homes.
  Duplicate urllib-response and Base64-expression rules were consolidated;
  remote evaluation is a parsed capability, not intrinsically hostile.
- Concealment/remote-evaluation composites describe co-occurrence accurately.
  Whole-file encoding properties moved from the legacy encoded namespace.
- The executable-path leaf was already at its 100-rule budget. Its Defender
  driver-directory observation moved to system paths, preserving its matcher.
  Moving the generic chmod observation also preserves the encoded-exec leaf cap.

Exact YAML consumers were updated. The directory-selector audit found only the
encoded-URL suppressor in the JavaScript junk-comment rule; dropping PowerShell
help from that selector cannot affect the JavaScript-only host. No new partition
or sparse sibling tree was added. Existing JSON and full-corpus expectations for migrated
properties were updated. Remote execution during setup retains its contextual
hostile detection without requiring unrelated Base64 concealment. Generic
archive staging and encoded identity queries no longer require hostile counts. Capability moves retain content matchers;
severity and parsing changes above intentionally correct unsupported intent or
quoted-text matches.

## Verification

Twelve controls cover actual and quoted cradles, comment-based help, ordinary
urllib bootstraps, unused encoded shell/permission code, executed encoded code,
a DOS overwrite variant with different size/count, an ordinary fixed-path image
writer, and a searched data-buffer writer. All expected trait matches pass. All
nine benign controls have zero suspicious and zero hostile findings.

Run `python3 testdata/triage/stager-conviction-review/verify.py --scratch-root <scratch>`.
The runner stages files outside test-directory suppressors before analysis.
Atomscan slow-mode scans of all three originals confirm the evidence counts.

Judgment markers live beside the original samples, outside the traits repository.
Their one-line notes are reproduced verbatim in the commit body.
