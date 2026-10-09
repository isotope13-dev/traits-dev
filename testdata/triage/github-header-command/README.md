# GitHub command and PHP header-shell controls

The fixtures are static source; never compile or execute the command fixtures.
`cases.json` records expected positive and negative detections. Five benign
controls cover repository reads and decoding plus an unrelated constant command,
ordinary autostart registration, issue comment parsing/decryption, local Apache
configuration I/O, and decoded header display. Two attack controls distinguish
variable shell command execution and decoded header-to-system execution. Two
additional controls distinguish a MachineId field from a helper declaration.

## Sample review

All three supplied SHA-256 digests were verified. Facts contain no parse errors
or hidden executable layer. These are transparent source examples, not recovered
native executables; Rizin reports no native code for the C# source. The verdicts
classify the implemented backdoor behavior, without attributing these examples
to a deployed family or treating their comments as reputation evidence.

- `efe9080720de`: GithubDeadDrop source exposes a GitHub-response-to-Base64-to-
  cmd.exe chain and an HKCU Run registration method. Its issue search extracts
  an HTML comment, decodes it, and attempts AES-CBC decryption. Key material is
  a 16-byte MD5 digest, not AES-256. ApplyRoute is empty: route rotation is not
  implemented. There is no standalone entrypoint in this file.
- `b6d454baeaec`: ShelbyLoader-style source implements Run -> host/user
  fingerprint -> persistence -> upload/poll. It uploads the encoded fingerprint
  using PUT, polls tasks every 63 seconds, and passes decoded command text to
  cmd.exe /c. HTTP 403 delays an hour; 401 enters the fallback. Its fallback only
  prints recovered owner/repository/token fields. The assigned AES key is again
  16 bytes, regardless of the preceding KeySize=256 setting. This is source
  imitating a loader, not evidence of a particular deployed family.
- Both C# clients decode the entire Contents API response directly rather than
  extracting JSON's content field. Standard JSON responses cannot be decoded
  this way; successful execution against GitHub is not established by static
  inspection. The traits describe the source's command path, not successful
  operational C2 or successful fallback configuration rotation.
- `866bead5fff1`: WHIPSHOT-labelled PHP backdoor checks an MD5 hash of an
  authentication header, returns 404 for rejected access, appends AddType rules
  for .local_journal and .ico to /etc/httpd.conf, and directly executes a
  Base64-decoded command header. system() streams command output; its return
  value is only the last output line, which is Base64-encoded in a comment.
  Writing configuration requires file permissions and Apache reload behavior;
  the sample does not implement privilege escalation or reload Apache.

## Trait corrections and reference audit

Neutral Run paths now use the canonical registry-key traits. Run persistence
requires the admitted GitHub command backdoor and a registry write; ordinary
updaters no longer receive a hostile verdict. Direct managed registry writes
were consolidated into registry/write; exact consumers were updated. The only
access-directory consumer is PE-scoped, so the moved source-only atom never
contributed to it. No bare manipulate-directory consumer was found.

HTML-comment Regex.Match is now a structured call/argument fact under string
search. The issue-comment objective also requires the command channel. The
redundant C# shell-execution objective was removed; the remaining command rule
requires the explicit cmd.exe /c variable-command call. That call has a neutral
shell trait; the generic Process.Start trait excludes it to preserve mechanism
classification. Generic Apache nonstandard PHP suffixes moved to HTTP server
route configuration, with underscore suffixes recognized. The sole exact
consumer was updated. Variable file_get_contents moved from HTTP to file read;
its sole exact consumer remains a URL-context composite. Base64 preceding
UploadString moved to HTTP client/managed, became notable, and lost the
unsupported exfiltration mapping; all exact consumers were updated. Bare upload
selectors intentionally no longer count that generic string send as file upload.

Credential type vocabulary moved from closed file/string to parse/vocabulary;
its exact scanner consumer was updated, and there are no direct credential-leaf
selectors. Shell-kind vocabulary moved out of webshell objectives, preserving
its exact and self-label-directory OR consumers. Parent selectors remain
subject to their existing contexts; no whole-category replacement was made.
MachineId field matching was tightened so a helper declaration supplies no
host-field or discovery claim.

Final sample targets: 3 hostile traits per C# source, 2 per PHP source.
Authoring precision for the C# hostile rules is 5.4, 7.1, and 8.3 respectively.
Benign controls must have zero hostile traits. No family identity was added.

PHP hostile precision: 6.2 and 5.8. All nine fixture expectations passed,
including zero hostile findings on all seven benign controls. Final atomscan
scans confirmed the 3 / 3 / 2 hostile counts.

Judgement marker contents (verbatim commit-body lines):

GithubDeadDrop source: constrain C2; relocate neutral observations
ShelbyLoader-style source: detect command C2 and Run-key writes
WHIPSHOT-labelled PHP shell: move file reads and handler config
