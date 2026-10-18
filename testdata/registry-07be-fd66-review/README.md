# Registry second review: versaWYS and koi-handler

The two primary archives retain MALICIOUS judgments under the queue's
behavior-based criteria. This review makes no malware-family attribution and
claims neither a compromised registry account nor an undisclosed installation
hook. Source, generated payloads, and managed IL were inspected independently
of scanner scores. Primary SHA-256 hashes were verified against the queue.

## versaWYS 3.6.0 (07be01194f0f…)

This is a PHP MVC application framework with Vue administration components.
Its PHP account-creation methods write the application's `versa_users` table;
they are not AWS IAM calls. The old IAM matcher accepted any camelCase
`->createUser(`. It now requires the IAM-style `UserName` argument key within
that parsed call. Controls cover real request shapes, a later argument key,
inline SDK construction, CMS methods, comments, and string-quoted examples.

The archive also ships two executable SweetAlert2 bundles, identifying versions
11.10.1 and 11.10.4, with the same regional sabotage routine at module load.
It requires a Russian browser language and a host ending in RU/SU/BY or the
punycode RF TLD. On first load it stores a timestamp; after more than three
days it schedules a callback after 500 ms. That callback sets the body style's
pointerEvents to none, appends a looping audio element pointing to a remote
MP3, then attempts playback after another 2500 ms. Playback rejection is
caught, but pointer blocking is not undone. This is intentional UI degradation,
not ordinary alert rendering. It is present in the distributed public assets;
this does not establish that every deployment loads these old copies. Current
Twig import maps instead select the installed npm SweetAlert2 dependency.

The exact extracted routines were evaluated in QuickJS with only mocked
browser objects and synchronous recording timers, without network/OS bindings.
Twelve cases covering first visit, two-day/four-day timestamps, English locale,
nonmatching hosts and BY hosts behaved as the static trace predicts. No audio
was fetched or played. Three existing hostile findings remain on the archive,
including one on each offending library member. No disclosure of this routine
was found in the application documentation reviewed.

The XLSX files implement spreadsheet parsing/writing. Their large character
mapping tables, ZIP compression routines, format-specific crypto, FileReader
and workbook export paths explain their notable findings. No additional
hostile behavior was established there.

## koi-handler 0.11.6 (fd663dcc11df…)

This is openly a multi-session reverse-shell listener and offensive toolkit.
It is not represented here as a covert PyPI implant. The entry point starts a
listener; actions are selected by an operator, using an existing session ID.
The supplied shell strings are executable payloads, not evidence that importing
the payload-generator module connects the review host to a remote server.

Payload construction was evaluated using only the two pure builder functions,
with an RFC 5737 documentation IP. The Base64 bash variant decodes to an
interactive /dev/tcp shell with stdin/output redirection. The UTF-16LE encoded
PowerShell variant reads commands from a TCP stream, executes them through
cmd /c, and writes the results back. Other variants couple a connected Python
socket to descriptors 0/1/2 and spawn a bash PTY. No generated payload was run.

The duplicate module does more than print templates: its Linux branch selects
an interface/IP and sends a constructed reverse-shell command through
KoiModule.exec to the remote session. Its Windows branch transforms the
PowerShell payload, uploads it, starts a hidden PowerShell child, and removes
the script afterward. The secrets module invokes remote commands to acquire
SSH keys, Git/AWS/PostgreSQL credentials, environment secrets and histories,
then parses and displays the results locally. KoiModule._try_exec reaches
_exec_clean and exec, whose sendall transmits the wrapper to the selected
session; this is remote collection, not reading the operator's local secrets.
The listener can suppress target shell history; the Ligolo deployment module
sets Defender path/process exclusions. Bash obfuscation includes hexadecimal
quoting, variable splitting, Base64 and forged kernel-thread argv[0] names.
PowerShell transformations split command names, format/hex/XOR strings and
encode commands. These do not conceal an additional fixed destination.

The retained verdict rests on functioning reverse-shell delivery/control and
credential acquisition with evasion. Those capabilities have legitimate
assessment uses; the verdict does not allege observed unauthorized deployment.
Four distinct existing hostile traits and accurate suspicious evasion traits
remain, across dev-tcp, PTY, stream-bridge and credential-access directories.

## Fetched Windows tools

The two exact requested URLs were fetched for separate static inspection.
RunasCs SHA-256 is 885079d33fb490a576301bcb9533cc99f08ded2f8a77745de161e2f1bc660377.
Certify SHA-256 is 45e24a06c38e2ffb00cb653f0067b2c44e44898558b3f1e29cdc39d1fcc344f4.
They are optional armory resources: populate_win.py fetches/cache-loads and
uploads them when invoked, and verifies the uploaded paths. This module does
not automatically launch them.

Managed metadata tokens and method bodies were decoded with dnfile/dncil,
including branch targets and resolved method/string operands. RunasCs Main
parses supplied credentials, command, logon type and optional remote endpoint,
then RunAs chooses process-creation routines. Its optional UAC path performs
LogonUser, integrity-level changes, impersonation and CreateProcessWithLogonW.
Its remote path creates/connects a Winsock socket and uses it for child handles.
Certify Main dispatches parsed commands. Certificate request execution validates
the CA and parameters, builds requested SAN identities, impersonates supplied
credentials if configured, and submits the request; the separate forge path
creates certificate/key material and exports PFX. Template assessment enumerates
AD CS objects and evaluates enrollment-abuse conditions. Neither binary was run.

`CreateProcessFunc` was merely a name fragment in RunasCs's selector names,
not shellcode evidence. The unused generic substring trait was removed; real
CreateProcessWithToken/WithLogon capability observations remain. The LogonUser
name matcher now accepts unsuffixed managed P/Invoke spelling, describes a
reference, and no longer hides that reference merely because a .NET framework
marker is present. Exact and suffixed API names share one canonical trait;
LogonUserCustom remains a near miss. Its only exact composite consumer remains
a notable token API cluster. No intent rule directly requires the modified atom.

Run `python3 testdata/registry-07be-fd66-review/check.py` for the five focused
static controls. Fixtures are staged outside testdata to avoid path suppressors.
Final atomscan scans retained the primary hostile coverage, removed the false
IAM/shellcode claims, and retained the new notable logon reference. Facts were
also extracted for both archives, flagged JavaScript/Python members, and the two
fetched binaries. Large bundled JavaScript reports flow-analysis limits; the
routine trace and mock evaluation do not depend on those incomplete graphs.
