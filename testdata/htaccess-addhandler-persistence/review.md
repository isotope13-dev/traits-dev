# PHP and Apache backdoor review

The three supplied SHA-256 values match the sample bytes. All three are
MALICIOUS by functionality. These are source specimens, including an explicitly
labeled reconstruction; no malware-family attribution or deployment provenance
is established. No sample was executed; no sample-controlled endpoint was contacted.
The initial scans' PHP flow-call gaps do not change the manually traced paths.

## Cache payload installers

- `9fd8d005fbc97a3e77abf71a127243b66abaa0cd6d89cc74e5ab14a431f4a4c7`:
  WordPress cache webshell installer using FilesMatch/SetHandler.
- `2e10620e3db1c644ad44e5007d47b88c2d530c20b06b6075115fbbe84dfe07bd`:
  the same installer using AddHandler.

Both register `restore_cached_payload` on the WordPress `init` action. The
callback Base64-decodes 222 bytes, XORs each byte with the repeating six-byte
key `xmmqhn`, and writes the result to `runtime.cache` if that path is missing.
Manual decoding recovered identical 222-byte PHP payloads. Their complete
behavior is an `isset($_POST['command'])` guard, `proc_open` with the unfiltered
POST parameter as the command, three pipes, stdout returned via
`echo stream_get_contents($pipes[1])`, and `proc_close`. The outer source also
implements this same console directly. There is no authentication or command
allowlist. Stderr has its own pipe but is not echoed; stdin is not populated.

Each callback overwrites its directory's `.htaccess`. One uses a FilesMatch
regex ending in `.cache$` with SetHandler; the other uses AddHandler for `.cache`.
With a compatible Apache PHP handler and overrides enabled, either exposes the
recreated cache payload as executable PHP. This is recurring webshell restoration
and a disguised command endpoint, not ordinary cache management. Execution of
these effects requires the WordPress host, filesystem permissions, and Apache
configuration; source analysis does not establish a successful deployment.

Changes cover the previously missed FilesMatch alternative and cyclic XOR
reconstruction, record the ordinary init hook, and place child-output relay in
`process/io/stream`. The configuration hostile now also requires the concrete
request-command/output channel. Handler configuration by itself is a capability,
not proof of persistence or a backdoor. Co-occurring configuration and console
are described as such; the rules do not claim a bound handler-write data flow.

## Cookie webshell bootstrap

`0e765230949b8c3d2eca48543dc4249ec7ee305963acd68f384bc52f15e5475a` is
a shell reconstruction of a NetScaler-path Apache backdoor bootstrap. Its source
comment mentions public reporting but does not supply independently verified
provenance or prove a particular malware family.

The straight-line script applies mode 6555 to `/bin/sh` (setuid, setgid and
read/execute permissions), creates the web directory, and writes a hidden PHP
endpoint through a quoted heredoc. The endpoint sets HTTP 404 and no-store,
checks a hardcoded session cookie, then passes a URL-decoded task cookie directly
to `passthru`, which returns command output. The cookie check is an operator
secret, not application authentication. This is an intentional command backdoor.

The script appends Apache configuration enabling PHP for the hidden file and
`.deb` suffixes, maps CSS URLs to that file using Alias and AliasMatch, and sends
SIGHUP to the PID read from `/var/run/httpd.pid`. The CSS aliases and 404 response
conceal the command endpoint. The permission grant prepares privileged shell
execution; it does not prove a shell preserves effective UID or that elevation
succeeded. The setuid-grant composite now lives under privilege escalation, while
the package/signature handler atom lives as notable HTTP server configuration.

## Controls and reference audit

The focused verifier passes 18 cases, including both handler spellings with a
renamed POST key and `.dat` suffix, ordinary PHP mapping, handler-only writers,
documentation, distant co-occurrence, unrelated output pipes, request data only
in descriptors, XOR near misses, init registration, package-handler configuration,
and setuid grants with and without cookie webshells. Six existing Apache alias
controls also pass after updating the relocated atom's exact references.

All exact YAML consumers of moved traits were updated. Ancestor-selector review
found no descriptor/configuration ancestors consuming the relocated atoms. Three
C2/webshell ancestors consume the moved setuid composite's former branch; the
unchanged required cookie/static-alias composite subsumes the moved composite,
so its relocation removes no passing population from those selectors. No
package dependency or PURL is involved.

Final atomscan reruns report three hostile traits on each PHP sample and two
on the bootstrap, each spanning more than one objective subdirectory.
