# Stranded member review, 2026-10-19

The three container verdicts are retained without re-judging them. Each member
was identified by the supplied SHA-256, read in full, scanned with atomscan,
and inspected with `cleave facts`. No sample code was executed. The source is
plain C, PHP, Classic ASP, or JavaScript; there is no hidden executable layer
in these members. Deep directory nesting is packaging, not code obfuscation.
The PHP editor's Base64 and URL decoding transports edited file contents;
it does not evaluate those contents.

## Individual decisions

| Member | Verdict | Execution path and effects |
| --- | --- | --- |
| `webshells/php/findsocket/findsock.c` | MALICIOUS | `main` takes a peer IP and port; enumerates inherited descriptors using `getpeername`; compares both endpoint fields; duplicates the matching socket onto descriptors 0, 1, and 2; calls `execl` with `/bin/sh -i`. This hijacks an existing connected socket, rather than creating an outbound reverse connection or a listener. |
| `webshells/php/qsd-php-backdoor.php` | MALICIOUS | No authentication precedes the request dispatcher. The `c` branch executes `exec($_REQUEST['c'], $return)` and returns output. Other branches expose arbitrary file reads/downloads, directory listing, deletion, request-selected permission changes, cookie-selected uploads, and decoded file edits. The `gz` branch shells out to tar and returns the archive; the database branch submits supplied SQL with supplied credentials. Safe-mode checks only report configuration. |
| `webshells/asp/cmd-asp-5.1.asp` | MALICIOUS | `Request.Form("C")` becomes `szCMD`, interpolated into a WScript.Shell `Run` command using `win.com cmd.exe /c`. Output is redirected into the webroot, granted Everyone full control with cacls, read back into the HTTP response, and deleted. This is output cleanup, not self-deletion. There is no authentication gate. |
| `osinthell@1.6.9/p.js` | MALICIOUS | Invoking the exported function lists C, D, E, and F drive roots, joins each entry to its drive, checks `isFile`, then calls `fs.writeFileSync(full, '')`. Default write mode truncates existing files. Only immediate root files are visited; there is no recursion, disk-sector overwrite, secure erasure, or network transfer. Exceptions are swallowed per file and drive. |
| `osinthell@1.6.9/a.js` | BENIGN | Invoking the export fetches an image URL with Axios, writes response bytes into a temporary image, then attempts to display it using the desktop opener, MSHTA/WIA, a maximized borderless topmost WinForms window, and an MSHTA image document. These are image display operations; no downloaded JavaScript is evaluated and there is no input interception, dismissal prevention, credential access, or data upload. Window styling and unusual MSHTA execution remain visible. |
| `osinthell@1.6.9/v.js` | MALICIOUS | Invoking the export executes `del /F /S /Q C:\Windows\System32\*.dll`. This attempts forced recursive deletion of system DLLs and discards output/errors. Permissions can prevent deletion; there is no elevation mechanism. Generic detections remain suspicious because an offline servicing tool could issue the same command. |
| `osinthell@1.6.9/t.js` | MALICIOUS | Invoking the export synchronously sets `{default}` bootstatuspolicy to ignoreallfailures, then disables recoveryenabled. If the first call throws, the second is skipped by the enclosing catch. These commands inhibit recovery in this payload; the general matches remain suspicious because administrators also configure these policies. |
| `osinthell@2.0.5/a.js` | BENIGN | Invoking the export resolves a relative image path and returns if absent. In the supplied archive the ten parent segments resolve to `.../o/p/g/bck.png`, while the bundled asset is at `.../f/g/bck.png`; the guard therefore returns. If an image were present, the subsequent code would write a temporary HTML viewer and open it through the desktop handler and MSHTA. It contains no input lockout or destructive operation. |

The package entrypoint calls these exports from `sorgu`; requiring an individual
member defines its export without running its body. That context confirms the
call sites, but each verdict above follows the individual member's operations.
The decoder/flow facts report limitations on several source files; complete
manual source tracing was used rather than treating those gaps as exoneration.

## Trait changes and controls

- Retire `mshta-inline-fullscreen-image`: its matcher proved a fixed-position
  image in an inline MSHTA document, not a fullscreen window. Existing
  `css-fixed-position`, `fixed-viewport-style`, and
  `mshta-inline-about-document` retain the actual observations.
- Retire `script-forced-fullscreen-image`: a child-process import plus that
  image document establishes neither forced display nor inability to dismiss.
  Both image helpers now have zero hostile and one suspicious finding.
- Retire `node-multi-drive-empty-wipe`: a drive list, directory enumeration,
  and unrelated empty file write need not concern the same target. Moreover,
  truncating files is destruction, not disk wiping. Keep the existing
  `node-truncates-drive-root-files` rule, which requires a structural chain
  from roots through enumeration, joined entry path, file check and overwrite,
  plus an fs import. Clarify the structural trait's description to specify
  files at drive roots.
- Extend the 14 focused cases to forbid the retired claims. Existing controls
  distinguish a changed target, changed enumeration directory/collection,
  filtered files, non-root directories, duplicate roots, append mode,
  nonempty writes and standalone writes. Add a positioned-image viewer.

Findsock retains two hostile findings; QSD retains two; ASP retains three.
System32 deletion and boot policy inhibition each retain two suspicious
findings without upgrading ordinary maintenance capabilities to hostile.
The root truncator retains one precise hostile finding and one suspicious
structural finding: a second hostile label would duplicate the same destructive
operation or restore the unjustified co-occurrence rule. No new hostile claim
was invented to satisfy a count.

## Marker notes

These one-line notes are the marker contents for the extracted members:

- `Findsock C shell: no change`
- `QSD PHP backdoor: no change`
- `IIS 5.1 ASP command shell: no change`
- `Drive-root truncator: remove unbound disk-wipe detection`
- `OSINT image helper 1.6.9: remove forced-fullscreen claims`
- `System32 DLL destroyer: no change`
- `Boot recovery disabler: no change`
- `OSINT image helper 2.0.5: remove forced-fullscreen claims`

## Verification

All eight post-edit atomscan reports agree with the local Cleave findings.
All 14 focused fixture assertions pass, including absence of the retired IDs.
The image helpers each retain zero hostile and one suspicious finding.
