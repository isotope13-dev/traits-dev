# Stranded member review

The three archive convictions remain unchanged. Each of the 34 listed members
was inspected independently and its supplied SHA-256 verified. There are 29
malicious members and five benign members. Judgment markers are adjacent to the
actual extracted files; Debian extraction omits the report's `data/` prefix.
The PHPInfo GIF member was recovered from Payloads/PHPInfo.zip without extracting
unrelated content. The JSON manifest records the exact paths, hashes, counts,
and marker notes.

## Confirmed archive labels retained

| Archive | SHA-256 | Label |
|---|---|---|
| danielmiessler-SecLists-2025.3-source.tar.gz | `8fa88740c36777012f637ebb844de43d1020fb4273e080019d5f0c80360f433f` | MALICIOUS, unchanged |
| laudanum_1.0+r36-0kali6_all.deb | `c3f630db99ff2233200805aca89a8d37fc91aa46953e3667e85fbff148099ebf` | MALICIOUS, unchanged |
| webshells_1.1+kali8_all.deb | `d183821e0d760adcbaf65690b0342010c0c5b4a9849117787009b99f15bb4110` | MALICIOUS, unchanged |

## Behavioral findings

The WARs deploy a JSP that executes the HTTP `cmd` parameter through Java Runtime
and returns stdout. Laudanum PHP and ASP shells pass request commands to process
creation and render output; PHP authentication/IP checks do not make that remote
execution payload inert. The WordPress template bypasses authentication. The
WordPress plugin supports command dispatch, self-permission/attribute changes,
and a reverse-shell branch. A branch references an uninitialized IP variable;
its working request command dispatch independently establishes the judgment.

The two PHP reverse shells connect an outbound socket, start an interactive
shell, and relay socket input and shell stdout/stderr. hidden.php imports request
variables and immediately invokes a caller-selected function with caller-selected
arguments. Findsock scans inherited socket descriptors, identifies the peer,
redirects standard descriptors and starts `/bin/sh -i`; it reuses a socket rather
than creating an outbound connection. QSD executes request commands and supports
file listing, editing, deletion, uploads and SQL queries. The IIS ASP shell uses
cmd.exe with temporary output, grants its output file access using cacls, renders
it and deletes it.

The three C stubs request UID zero (and GID zero in one), then execute a shell.
They need existing privilege or setuid installation; they contain no independent
kernel exploit. Their privileged-shell detections were retained.

Each traversal ZIP stores `hacked\n` at a parent-relative index.php path. These
are crafted web overwrite probes, not shell programs. They have two suspicious
structural findings. zbxl.zip has 190,023 entries, overlapping compressed ranges
and declares 4,507,981,427,706,459 expanded bytes, about 4.5 PB. Its three suspicious
structural findings are sufficient evidence without claiming that the resource
impact actually occurred. Neither traversal entries nor the bomb were expanded.

The two Jhaddix files are inert independent XSS vectors, including decoded alert
and challenge examples, rather than an HTTP-response execution chain. The CGI
files are path/query fuzz dictionaries. Their single suspicious IIS command-query
finding describes a real test vector. The PHPInfo probe contains GIF magic and
`phpinfo()` only; it has no request-driven execution or payload loader. One
suspicious disguise finding accurately describes its mixed content.

## Placement review

Pass one classified matcher evidence independently of suspected intent. Pass two
checked the target operation, nearest alternatives, effective scopes, exclusions
and consumer references. All destinations below are existing leaves. Neutral
atoms no longer imply debugger detection, exploitation or supply-chain compromise.
Actual objective composites retain the evidence needed for their claims.

| Old observation | Canonical destination | Boundary and near miss |
|---|---|---|
| PHP command form field | micro-behaviors/ui/window/form-input::php-command-named-form-control | command input/textarea; a form named shell is insufficient |
| Legacy getter definition | micro-behaviors/data/property/define::js-legacy-getter-definition | property definition, not a debugger oracle by itself |
| Bare object console log | micro-behaviors/os/console/io::js-console-log-bare-object | logging, not debugger detection; raised to notable |
| Eval wrapping identifier call | micro-behaviors/process/interpreter/eval/direct::js-eval-nested-identifier-call | direct eval syntax, not supply-chain trust abuse |
| Emscripten script bridge | micro-behaviors/process/interpreter/eval/indirect::emscripten-run-script-reference | named interpreter bridge reference, not hidden-payload intent |
| Function named exploit | micro-behaviors/data/control-flow/dispatch::js-exploit-named-function-call | call syntax, not successful exploitation or top-level context |
| eval(unescape( bytes | micro-behaviors/process/interpreter/eval/direct::js-eval-unescape-byte-prefix | literal byte prefix; unescape alone insufficient |
| Script/image extension mismatch | metadata/file/extension/mismatch::script-content-as-image-extension | analyzed artifact property, not independent exploitation |
| GIF-prefixed PHP composite | objectives/evasion/masquerade/extension-mismatch::gif-prefixed-image-named-php | mismatch plus GIF magic, not demonstrated upload exploitation |
| XSS string fragment | micro-behaviors/data/embedded/payload/source::js-xss-probe-string-fragment | embedded vector content, not privilege escalation |
| Embedded PowerShell file read | micro-behaviors/fs/read/file/full::embedded-powershell-read-file-variable | full-file read, not eval; write-only near miss |
| Laudanum project/contact | well-known/dual-use/remote-admin/laudanum | consolidate the same entity; title plus execution still required for hostile identity |

The two eval-variable atoms were equivalent parsed direct eval(identifier) calls;
consumers now use js-eval-variable-argument. Direct eval and member eval controls
check their distinction. computed-window-member-call was a narrower subset of
window-double-bracket-call, with identical scope, and all five consumers already
used both as alternatives. The redundant atom and its five references were
removed. Eval/direct and control-flow/dispatch each remain at the 100-rule cap.
No new directory partition was invented to evade the cap.

The misleading standalone corroborating-move group was inlined into its sole
webshell consumer. Its reflection/callback/socket/chattr alternatives continue
to require request assignment and command execution. The fetched-response eval
sink group was removed: generic eval never proved that fetched content was its
argument. Both ActiveX consumers now require direct responseText evaluation. The eval
matcher requires the closing parenthesis, excluding responseText.length and
properties whose names merely start with responseText.
This deliberately stops conviction of merely co-occurring HTTP and eval tokens;
indirect assignments without a demonstrated response-to-eval link are no longer
sufficient for those composites.

ICMP code evidence now requires ICMP context, MIME charset evidence requires a
Content-Type header, and relative executable text requires a complete command
token and an argument or trailing shell operator. The untyped shell-out matcher is described as a literal reference.
Directory selectors were reviewed as well as exact references: neutral atoms
leaving objective branches should no longer count toward objective profiles;
Laudanum no longer belongs to an offensive-tool blanket selector. Effective
language/platform scopes and exclusions were retained for placement-only moves.
The relocated nested-eval and XSS-literal observations intentionally no longer
suppress testing, Emscripten, or whole library profiles: these neutral syntax
claims remain true in those contexts. Their objective consumers retain their
own context exclusions. Broad recursive exclusion expansion stalled positive
debug controls; removing the intent-based exclusions also fixes that problem.
Irrelevant inherited objective ATT&CK/MBC mappings were
not copied onto neutral observations. GIF camouflage uses T1036.008 instead of public-application exploit
T1190. No inline YARA was changed.

## Verification

Every member and outer archive received atomscan and cleave facts inspection.
Source control flow, discovered/decoded strings and ZIP central/local headers
were inspected. Rizin confirmed the PHPInfo byte prefix and lack of a native
executable; binwalk was unavailable. The final member rescans meet the requested
counts: executable malicious members have 2–4 hostile traits; the crafted ZIPs
have at least two suspicious traits; benign members have zero hostile and at
most one suspicious trait. Counts below include unique nested WAR findings.
41 regression controls with 44 rule assertions passed; the tightened ActiveX
positive also matched with hostile precision 8.6. Controls and their reusable
runner are in
[testdata/triage/stranded-member-observations](../../../testdata/triage/stranded-member-observations).
They run from neutral paths to test production behavior rather than test-directory
suppression. The existing testdata/triage/stranded-members controls were preserved.
Full validation identified two directory-listing captures that still matched
bare root entries after nested path prefixes were excluded. Requiring an
argument or trailing shell operator fixes that count-gate inversion; the new
bare-path listing control and both command/path controls pass.

## Individual judgments

| Extracted member | Judgment | Hostile / suspicious | Identification and marker note |
|---|---|---|---|
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/jsp/cmd.war` | MALICIOUS | 4 / 3 | JSP command WAR: direct request execution; no change |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/php/shell.php` | MALICIOUS | 2 / 0 | Laudanum PHP shell: require command input, not a named form |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/wordpress/templates/shell.php` | MALICIOUS | 2 / 0 | Laudanum WP shell: match command textarea; preserve execution |
| `8fa887/SecLists-2025.3/Web-Shells/WordPress/plugin-shell.php` | MALICIOUS | 2 / 0 | WordPress shell: retain command and reverse-shell detections |
| `8fa887/SecLists-2025.3/Web-Shells/laudanum-1.0/asp/shell.asp` | MALICIOUS | 2 / 0 | Laudanum ASP shell: consolidate identity; command execution |
| `8fa887/SecLists-2025.3/Fuzzing/XSS/robot-friendly/XSS-Jhaddix.txt` | BENIGN | 0 / 0 | Jhaddix robot XSS list: require response-to-eval linkage |
| `8fa887/SecLists-2025.3/Fuzzing/XSS/human-friendly/XSS-Jhaddix.txt` | BENIGN | 0 / 0 | Jhaddix human XSS list: require response-to-eval linkage |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/tiny-shell.c` | MALICIOUS | 2 / 0 | Tiny UID-zero shell stub: existing detections accurate; no change |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/root-shell.c` | MALICIOUS | 2 / 0 | Root UID/GID shell stub: existing detections accurate; no change |
| `8fa887/SecLists-2025.3/Miscellaneous/Source-Code/c-linux/root-shell2.c` | MALICIOUS | 2 / 0 | Root bash shell stub: existing detections accurate; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Bombs/zbxl.zip` | MALICIOUS | 0 / 3 | zbxl ZIP bomb: overlapping data declares 4.5 PB; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-01.zip` | MALICIOUS | 0 / 2 | Traversal depth-01: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-02.zip` | MALICIOUS | 0 / 2 | Traversal depth-02: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-03.zip` | MALICIOUS | 0 / 2 | Traversal depth-03: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-04.zip` | MALICIOUS | 0 / 2 | Traversal depth-04: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-05.zip` | MALICIOUS | 0 / 2 | Traversal depth-05: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-06.zip` | MALICIOUS | 0 / 2 | Traversal depth-06: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-07.zip` | MALICIOUS | 0 / 2 | Traversal depth-07: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-08.zip` | MALICIOUS | 0 / 2 | Traversal depth-08: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-09.zip` | MALICIOUS | 0 / 2 | Traversal depth-09: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Payloads/Zip-Traversal/depth-10.zip` | MALICIOUS | 0 / 2 | Traversal depth-10: parent-path web overwrite probe; no change |
| `8fa887/SecLists-2025.3/Discovery/Web-Content/LEGACY-SERVICES/CGIs/CGI-XPlatform.fuzz.txt` | BENIGN | 0 / 1 | CGI-XPlatform list: tighten ICMP, MIME and command references |
| `8fa887/SecLists-2025.3/Discovery/Web-Content/LEGACY-SERVICES/CGIs/CGIs.txt` | BENIGN | 0 / 1 | CGIs wordlist: tighten ICMP, MIME and command references |
| `8fa887/PHPInfo/phpinfo.php-1.gif` | BENIGN | 0 / 1 | PHPInfo GIF probe: describe disguise, not upload execution |
| `c3f630/usr/share/laudanum/jsp/cmd.war` | MALICIOUS | 4 / 3 | JSP command WAR: direct request execution; no change |
| `c3f630/usr/share/laudanum/wordpress/templates/php-reverse-shell.php` | MALICIOUS | 2 / 0 | WP PHP reverse shell: socket-to-process stream relay; no change |
| `c3f630/usr/share/laudanum/php/php-reverse-shell.php` | MALICIOUS | 2 / 0 | PHP reverse shell: socket-to-process stream relay; no change |
| `c3f630/usr/share/laudanum/php/shell.php` | MALICIOUS | 2 / 0 | Laudanum PHP shell: require command input, not a named form |
| `c3f630/usr/share/laudanum/wordpress/templates/shell.php` | MALICIOUS | 2 / 0 | Laudanum WP shell: match command textarea; preserve execution |
| `c3f630/usr/share/laudanum/asp/shell.asp` | MALICIOUS | 2 / 0 | Laudanum ASP shell: consolidate identity; command execution |
| `c3f630/usr/share/laudanum/php/hidden.php` | MALICIOUS | 2 / 1 | Laudanum hidden PHP: arbitrary request-driven call; no change |
| `d18382/usr/share/webshells/php/findsocket/findsock.c` | MALICIOUS | 2 / 0 | Pentestmonkey findsock: inherited socket shell reuse; no change |
| `d18382/usr/share/webshells/php/qsd-php-backdoor.php` | MALICIOUS | 2 / 6 | QSD PHP backdoor: request commands and file management; no change |
| `d18382/usr/share/webshells/asp/cmd-asp-5.1.asp` | MALICIOUS | 2 / 1 | IIS 5.1 ASP shell: command output, ACL grant and cleanup; no change |
