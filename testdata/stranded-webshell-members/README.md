These controls cover the stranded Webshells member review. Run the cases with
`python3 testdata/stranded-webshell-members/check.py`.

`findsock.c` iterates inherited descriptors from 3 to `getdtablesize()`, uses
`getpeername` to select the supplied IPv4 peer and port, then calls `setsid`,
duplicates that descriptor onto 0/1/2, closes the original and executes
`/bin/sh -i`. This is a socket-reuse shell, not an outbound reverse shell.

QSD dispatches unauthenticated request fields into `exec`, `chmod`, arbitrary
file reads/deletion/editing, uploads and MySQL queries. Its archive branch runs
`tar czf`, returns the archive bytes and removes the temporary archive. The
JavaScript Base64 encoder and PHP URL/Base64 decoder transport edited file
contents; they do not conceal executable code.

The ASP member reads `Request.Form("C")` into a command line executed through
`WScript.Shell.Run`. It redirects output to a webroot temporary file, grants
Everyone full control using `cacls`, reads the result into the HTTP response,
then deletes the file. Its machine-name and file-reading operations also
deserve capability coverage.

All three verdicts are MALICIOUS based on these execution paths. The archive's
confirmed verdict is retained. No specimen was executed.

Placement changes preserve the comparison atom's matcher and scope, moving it
from string search to memory comparison. Its sole grouping composite also
accepted string search, so the consuming BPF objective now directly requires
either operation. The conjunction, alternatives and proximity bound remain
unchanged. The `win.com cmd.exe /c` atom moves from script-host to command-mode
without changing its matcher or scope; the existing launcher cases follow it.
Neither observation by itself establishes a backdoor or privilege bypass.

Positive, negative and both-operation C controls distinguish comparison from
search. Routine ASP file serving and PHP archive serving controls must retain
their capabilities without hostile findings. Near misses use write mode,
archive listing and an inert function-name string.

The command-mode directory was at its 100-rule budget. Its WMIC
process-creation atom does not require a shell, so it moves to
`process/create/exec` with its matcher and scope preserved. Its explicit
Lua command-tools consumer follows it. Exec-directory consumers either exclude
Lua or already accept the shell ancestor; shell-only consumers intentionally
stop treating a generic WMIC process-creation reference as shell execution.
The existing spawn umbrella already includes the cmd command-mode observation
that accompanies the relocated win.com prefix. No ancestor mem/compare or
string/search directory consumers require extra alternatives.

Judgment marker notes:

- Pentestmonkey findsock shell: move comparison to memory traits
- QSD PHP backdoor: detect tar creation and stream output
- ASP Cmd Shell 5.1: detect file reads and hostname query
- Webshells Debian archive: retain confirmed malicious label
