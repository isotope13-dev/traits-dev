# Six stranded members

All six members are MALICIOUS based on their complete source, independently
of their confirmed enclosing archives. SHA-256 values were checked against
the queue. `atomscan --no-update --mode slow` and `cleave facts` were collected
for both archives and all six members. The original and final scan reports
and facts are saved in the task scratch directory, `stranded-analysis`.
No specimen code or destructive command was executed.

| Member (SHA-256 prefix) | Execution path and effect |
| --- | --- |
| `findsock.c` (`2a5548094577`) | Requires peer IP and port arguments; loops over inherited descriptors starting at 3; `getpeername` supplies the peer tuple; matching IP and port lead to `setsid`, `dup2(fd, 0/1/2)`, close, and `execl("/bin/sh", "/bin/sh", "-i", NULL)`. The selected live connection becomes an interactive shell. This is socket reuse, with no new outbound connection or listener. The PHP companion passes the current HTTP client's address and port to this helper. |
| `qsd-php-backdoor.php` (`eaa0a356da77`) | Unauthenticated request dispatch calls `exec($_REQUEST['c'], $return)` and prints the output. Additional branches read, modify, upload, download, delete, and chmod caller-selected paths; connect to a caller-selected MySQL server and execute its supplied query. The archive branch interpolates a requested directory into `cd ...; tar czf ... *`, serves the archive and deletes it. The editor URL-decodes Base64-decoded POST content and writes it to the request-selected stream. Encoding transports editable content; it is not concealed executable code. |
| `cmd-asp-5.1.asp` (`e5b91baf39dc`) | `Request.Form("C")` becomes `szCMD`, concatenated into `win.com cmd.exe /c` through `WSCRIPT.SHELL.Run`. Command output is redirected to a generated file under `C:\inetpub\wwwroot`; another command grants Everyone full control with cacls; the response reads and displays the file; a final command deletes it. This provides a remote shell and output cleanup, not privilege elevation. |
| `p.js` (`d6f337222fab`) | Exports a function that enumerates C/D/E/F drive roots, joins each entry to its originating root, checks that it is a regular file, then overwrites that same path with an empty string using default write mode. It destroys existing contents at the roots; it does not recurse into directories. Per-drive and per-file catches allow subsequent work after failures. |
| `v.js` (`2e5535f938bc`) | Exports a function invoking `del /F /S /Q C:\Windows\System32\*.dll` via `execSync`. This attempts forced, recursive, quiet system-DLL deletion. Output and errors are discarded. Permissions can prevent deletion; the code does not elevate privileges. The two applicable deletion traits remain suspicious because general System32 deletion patterns can appear in image maintenance. |
| `t.js` (`28db8a38c16d`) | Exports a function that invokes bcdedit to set the default boot entry's `bootstatuspolicy` to `ignoreallfailures` and `recoveryenabled` to `No`. Output and errors are discarded. Both calls share one try block, so failure of the first skips the second. The two general boot-policy traits remain suspicious because administrators may intentionally use these settings. |

The JavaScript modules execute their destructive functions when invoked, not
on import. The package entry point imports them and calls them from exported
`sorgu()`. There is no decoder hidden in the alphabetical directory nesting
or the short names. All executable statements in these six files were traced;
no encoded payload or further obfuscation was found. The ASP facts lack a
flow graph and the JavaScript flow producer omits anonymous function bodies;
manual source tracing and parsed call records supplied those relationships.

The Debian extraction strips the archive's `data/` component. Verdict markers
are beside the actual extracted files under `extract/d18382/usr/...`; the
other three are beside their `extract/0807ef/package/...` members. No archive
was re-judged.

## Trait changes

* Move the existing drive-root literal-list matcher unchanged from
  `fs/enumerate/directory::node-multiple-drive-roots` to
  `fs/path/drive-root::windows-drive-root-literal-list`. Its name and
  description now assert consecutive path literals, not enumeration. Preserve
  confidence, severity, format, platforms and regex. The old ID has no exact
  consumers. The ancestor `directory-listing-evidence` roll-up intentionally
  stops treating bare path literals as directory enumeration. Broad filesystem
  capability profiles still see a filesystem path observation. Other rules in
  the source file remain unchanged.
* Move the three firing PHP MySQL symbol matchers to `data/db/access`
  (connect), `data/db/config` (select default database), and `data/db/query`
  (query). Matchers, confidence, platforms, formats and severity are preserved.
  Descriptions say API references, matching the symbol evidence rather than
  claiming runtime execution. Update the local administration/query-console
  composites, MySQL connectivity roll-up, and webshell database consumer.
  The remaining MySQL rules retain their existing definitions. The only broad
  MySQL directory consumer is a Python-only socket exclusion; these PHP-only
  moves do not affect it. No broad database ancestor consumer needs expansion.
* Add notable PHP observations for `file_get_contents` with a direct
  GET/POST/REQUEST subscript source, and `fopen` with a direct request subscript
  and a known writable mode in the same call. The first fills the gap between
  the baseline read API and the existing variable-name-only source query.
  The second binds source and mode structurally instead of combining unrelated
  request references and file opens. Both describe neutral stream operations;
  neither asserts a write, malicious file selection, or payload execution.

The two new PHP traits are additive capabilities, not additional hostile
verdicts. Existing hostile shell and destruction detections are retained.
All members meet the requested coverage: two hostile traits for Findsock,
QSD and p.js; three for the ASP shell; two suspicious traits each for v.js
and t.js. The latter two are individually malicious based on their complete
functions, without raising general-purpose detections to hostile.

Run `python3 testdata/stranded-six-member-review/check.py` for the focused
controls. These include bare roots versus real directory calls, subdirectory
paths, all three request sources, PHP function-name case, writable and
read-only modes, quoted code, unrelated requests and file paths, request data
in a different argument, and relocated MySQL facts. The controls analyze
source only.
