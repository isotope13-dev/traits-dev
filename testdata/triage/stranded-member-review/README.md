# Stranded member review

The three containing archives retain their confirmed MALICIOUS verdicts.
Each of the seven requested members was judged from its own source. Initial
and final atomscan reports, complete `cleave facts` output, and isolated
JavaScript API traces were retained in the task scratch directory. Archive
findings and ML scores were not used to establish a member's behavior.

| Member | SHA-256 | Verdict | Execution path and effect |
| --- | --- | --- | --- |
| webshells `findsock.c` | `2a55480945770a2db905b77b5b1ffdce59997b8e84c8f289fd3851ca3db2dc31` | MALICIOUS | Iterates inherited descriptors from 3 to `getdtablesize()`, calls `getpeername`, compares the peer to the supplied IP/port, then uses the matching descriptor for stdin/stdout/stderr and executes interactive `/bin/sh`. This hijacks an existing connection; it does not create an outbound reverse-shell connection. |
| webshells `qsd-php-backdoor.php` | `eaa0a356da7712bf0f70f0f2a80f30447ca702ef721543f3ef75afd2fcc6e9d8` | MALICIOUS | An unauthenticated request dispatcher passes parameter `c` to `exec` and returns its output. Other request-selected branches browse/read/delete/edit arbitrary paths, grant mode 0777, upload to a cookie-controlled directory, archive directories for download, and run supplied MySQL queries. Base64 and URL decoding transport edited file contents; they do not conceal an executable payload. |
| webshells `cmd-asp-5.1.asp` | `e5b91baf39dc8542b1ffb6f5a08f5bdf77a1bebeb579c9971b2580ab28f87eaf` | MALICIOUS | Reads POST field `C`, runs it through WScript.Shell with `win.com cmd.exe /c`, redirects output to a temporary web-root file, grants Everyone full control with `cacls`, reads the file into the response, and deletes it. There is no authentication gate. No privilege escalation is inferred. |
| osinthell 1.6.9 `a.js` | `5ca165dfa01840728e83447772dfbed18167529390fea6f6531b1956295d50a4` | BENIGN | Exported function requests a JPEG from Discord CDN using Axios GET/arraybuffer, writes the response to a temporary JPEG, and launches image presentation commands through START, MSHTA/WIA, PowerShell WinForms, and an inline HTML image. WinForms requests maximized, borderless, topmost display. There is no close-prevention, input block, credential capture, or arbitrary downloaded-code evaluation in this member. Remote response bytes were not fetched or judged. |
| osinthell 1.6.9 `v.js` | `2e5535f938bcd9fda49d0be615613ca66740bda689beba6489bce65fd80032f1` | MALICIOUS | Exported function silently attempts `del /F /S /Q` against the live C-drive Windows System32 DLL glob through imported `execSync`. It recursively targets OS libraries rather than application data. Windows permissions and file locks may prevent deletion; the attempted destructive action is explicit. |
| osinthell 1.6.9 `t.js` | `28db8a38c16dadfaa9a0ff23167469aced0db21185c50d1614f946f388afa962` | MALICIOUS | Exported function invokes `bcdedit` to ignore all boot failures and disable boot recovery for the default entry, suppressing child stdio and catching errors. Both commands share one try block, so failure of the first skips the second. This is recovery sabotage, with no encryption or ransom demand in the member. |
| osinthell 2.0.5 `a.js` | `1c33be9e0a79b4b566185a32f9eb21e99ae9c8a92738c0783d8c59da20b255e0` | BENIGN | Exported function computes a local PNG path and returns if it is absent. Its ten parent steps resolve to `public/a/.../p/g/bck.png`; the shipped PNG is at `public/a/.../g/bck.png`, so the package takes the return. If that path exists, it writes temporary HTML displaying the image and opens it with START and MSHTA. No downloaded payload, deletion, credential access, or lockout exists in this member. |

All seven members are readable source, with no hidden decoder or obfuscated
dispatch. JavaScript escape sequences were interpreted with QuickJS while
`require`, filesystem operations, process creation, and Axios were replaced
with mocks. No sample command or real network request was executed. The
1.6.9 image path was traced through the fulfilled asynchronous callback; the
2.0.5 function was traced with both missing and present image conditions.
Source inspection also confirmed that the package entrypoint calls these
exports from `sorgu`; importing a module alone does not invoke its export.

The remote shell members retain their existing two, two, and three hostile
findings respectively. The recovery module retains two suspicious findings.
The DLL-deletion module gains a second suspicious finding for an actual exec
argument targeting the System32 DLL glob. That generalized detection also
admits offline-image servicing, so its severity stays suspicious. Both image
members retain zero hostile and one suspicious inline-MSHTA finding.

Trait changes place socket peer queries under socket/query, WinForms
references under metadata/import/framework, and boot-recovery suppression
under impact/degrade/system/recovery. Exact consumers and the port-scanner's
former directory selector retain the observations they selected. Added
capabilities describe Axios GET configuration, explicit system-DLL command
arguments, and PowerShell window settings. The local-path description no
longer claims an image path is a script.

Run `python3 testdata/triage/stranded-member-review/check.py` from the repository
root. The 14 static controls cover positive and negative call arguments,
quoted deletion examples, recovery re-enabling, ordinary window settings,
anonymous-function Axios calls, unrelated method properties, socket-name
strings without calls, and WinForms references. These fixtures are analyzed
as data and never executed.
