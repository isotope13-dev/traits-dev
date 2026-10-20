The reviewed input is a 973-byte PHP behavioral reconstruction, SHA-256
`68d3d3e34f52eeb8a98d4800029a1552a24788a07d6a43c9c1626fd04a324738`.
Its comment explicitly disclaims recovered Rank Math source; no product or
malware-family attribution follows from that comment.

Before checking request input, it copies its own bytes to a filename derived
from the first 16 hex digits of SHA-256 of its directory, with a `.cache`
suffix, unless that path is already a file. It unconditionally overwrites the
local `.htaccess` with a PHP handler for `.cache`. This attempts to retain an
executable copy under a data extension. Apache must honor the override and
provide the corresponding PHP handler for activation to succeed.

When `cmd` is present in `$_REQUEST`, the script Base64-decodes it and XORs
each byte with the repeating six-byte key `xmmqhn`. The resulting string is
passed directly to `proc_open`, with three pipe descriptors. Stdin is closed;
stdout and stderr are echoed, then closed, and the process is reaped. There is
no authentication or command allowlist. The key conceals commands; it is not
an authorization check. This is an arbitrary remote command endpoint, so the
MALICIOUS judgment stands independently of scanner scores or registry origin.
The supplied file contains no further embedded payload or remote endpoint.
Review is static; no PHP runtime was available.

Detections now bind `.htaccess` to the write target instead of nearby text,
separate variable reads from the `__FILE__` constant, and recognize a nested
self-read-to-write copy. XOR loop findings require loop syntax; the transform
has no inferred encoding direction, and the redundant narrower matcher was
removed. Existing exact consumers of its renamed canonical trait were updated.
No directories were relocated. All changed rules retain their platform scope.
Stream-output evidence excludes the enclosing program span, and redundant PHP
opening-tag legs were removed from the POST/REQUEST command composites. These
prevent distant commands from appearing adjacent to handler configuration merely
because their composite evidence includes the beginning of the file.

Run `python3 testdata/php-cache-backdoor-boundaries/verify.py <scratch-directory>`.
The controls check direct self-copy versus unrelated reads and writes, actual
htaccess targets versus contents and backups, loop context versus a single
expression or comment, and renamed request keys and handler suffixes. Controls
are scanned as data and never executed. The broader existing controls are in
`testdata/htaccess-addhandler-persistence/verify.py`.
