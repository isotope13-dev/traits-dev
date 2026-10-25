The three archive convictions are retained. Each of the six requested
members is independently MALICIOUS, based on its verified bytes. No sample
code, destructive command, or remote response was executed.

The universal macOS Installer is a native wrapper around a password and wallet
stealer. ARM64 entry 0x100000690 constructs a string and calls system at
0x1000006b8. The decoder XORs each byte with the state low byte, then updates
state = ((state * 0x3785) & 0xffffffff) % 35999, starting at 0x11667.
The modulus comes from the embedded build-time text 09:59:59. Ciphertext at
file offsets 19600 and 85472 decodes identically in both architectures.
The result is an osascript command that evaluates a second script assembled
from quoted lines and return separators. The final handler invocation is
present. This is executable embedded code, rather than a collection of strings.

The recovered script obtains a login password with a masked Installation
dialog and validates it using dscl . authonly, caching the result on disk.
It copies Chromium/Gecko login and cookie stores, wallet extensions and desktop
wallet stores, login.keychain-db, Safari cookies, Notes data and filtered
Desktop/Documents files into a random temporary directory. An empty-password
branch also queries the Chrome Keychain item. It archives the collection with
ditto, posts the ZIP with curl --data-binary to http://charge0x.at/log, and
removes both temporary data and ZIP. It downloads a Ledger Live replacement,
stops the legitimate application, removes its bundle using the phished password
with sudo, and extracts the replacement into /Applications. It also fetches a
shell command, inserts it into a KeepAlive/RunAtLoad LaunchDaemon using bash -c,
installs/bootstrap it with sudo, and falls back to nohup if bootstrap fails.
The LaunchDaemon specifies the current username: privileged installation does
not establish that its eventual command runs as root. Remote payload contents,
TCC grants, successful authentication, delivery and installation are unknown.
These theft and replacement paths are incompatible with a legitimate patch
installer, independently of the archive verdict.

parser-session 1.1.9 writer.js captures process.env and host, user, platform
and MAC information at module initialization. Its g helper converts hex pairs
with parseInt(..., 16) and String.fromCharCode. Its eight-entry table decodes
to require, axios, post, an HTTPS endpoint, headers, x-secret-header, secret,
and then. The exported function posts the captured data to
https://log-server-lovat.vercel.app/api/ipcheck/703 and evaluates the response
body with eval(r.data), discarding rejection. This serves secret export and
server-supplied code execution, rather than parser or logging functionality.
Existing rules bind the table slots, request operands and response callback;
their six hostile detections are retained. Automatic execution from this archive
is not proved: writer.js references ../package.json from src/lib although the
manifest is at the package root, and src/index.js names a .pnpm/httpreslog
module path absent from this tree. These broken paths affect reachability,
not the malicious purpose of the member's implemented function.

osinthell 1.6.9 exports four independent destructive functions:

* v.js invokes del /F /S /Q against the System32 DLL glob, suppressing streams
  and errors. It attempts recursive system-library destruction.
* f.js opens the physical disk read/write, creates a 512-byte zero-filled
  Buffer, and writes that buffer to the same handle at offset zero. The later
  bootrec /fixmbr command is a repair operation; it does not erase the preceding
  sector overwrite and cannot restore the wiped partition table.
* p.js enumerates C/D/E/F drive roots, joins each entry to its drive, checks for
  regular files and writes empty contents to that same path in default mode.
  This truncates root files, without recursing into subdirectories.
* t.js sets bootstatuspolicy ignoreallfailures and recoveryenabled No. The
  shared try block means first-call failure prevents the second call.

These functions require invocation; imports alone do not run their bodies.
index.js calls them from the exported sorgu method. Earlier resource-exhaustion
modules can prevent later calls from being reached, so successful package-wide
execution is not asserted. Each requested member still implements a destructive
operation with no documented servicing or recovery purpose. Privileges and
actual execution on a victim machine remain unknown.

Coverage and corrections

The installer already has 17 hostile detections spanning theft, collection,
exfiltration, cleanup, privilege use, wallet replacement and persistence.
The added notable constructed-evaluation trait covers its previously unreported
return-joined run script operation. It has no hostname, hash, handler identifier
or payload filename requirement. Controls distinguish ordinary joined evaluation
from a plain run script, a comment, and echoed script text.

The four tiny destructive modules support one independent hostile effect each.
Their existing 1/1/2/1 hostile counts are retained. The second p.js hostile trait
corroborates the same truncation operation; it does not prove another behavior.
No independent hostile behavior remains uncovered in these four members.
Tracing execution, ignored output/errors, disk writes, bootrec, enumeration and
boot configuration yielded existing notable/suspicious primitives, rather than
three additional hostile objectives. Neither matcher limitations nor a desire
to reach 3-5 traits justifies inventing or duplicating attack claims.

Retire npm-modules-buried-below-analysis-depth: its conjunction only required
a deep require path, short package description and npm-init test command.
These do not establish a scanner bypass or hostile payload. The actual archive
scan analyzes the requested deeply nested members, refuting its stated current
skip behavior. There are no exact YAML or expectations consumers of this rule.
The hidden-payload ancestor consumers expect actual concealed payload evidence;
they must lose this unsupported alternative. Existing hostile fixtures and
near misses were inspected before the change. All five destructive objectives
in the real archive remain detected after its removal. The unusual path-loading
observation and archive-member path metadata remain, preserving the supported
inspection-relevant technique rather than erasing it.

Move deep-single-letter-require-path from process/create/load/local to
os/module/load, because requiring a JavaScript module does not create a process.
Retain suspicious severity. Replace the text regex with a require call and
argument predicate. This excludes comments, quoted examples, seven directories
and a partial eighth component; it also accepts whitespace around the call.
The old process/create ancestor consumers require execution contexts, so they
must not inherit language-module loading. The destination and its ancestors
have no directory consumers requiring membership adjustments. No other consumer
or matcher is weakened. This is the 100th rule in the existing module-load leaf.

Verification and classifier limits

Run python3 testdata/taxonomy/stranded-depth-review/check.py for 11 direct
positive/near-miss checks. The existing testdata/stranded-current-review/check.py
passes 20 assertions on retained hostile and near-miss fixtures outside the
requested member paths. A harmless archive with the original deep-path/template
shape is added to the normal validation corpus: it retains the suspicious
module path and notable archive path observations, with zero hostile traits.

review.json records every before/after count, model output and changed archive
analysis unit. No supported attack detection was lost; only the unsupported
scanner-depth composite was removed and the module-loading ID was relocated.
The four tiny destructive members remain ML level -1 before and after despite
hostile rule coverage (probabilities approximately 0.971-0.988). Installer and
writer remain flagged at calibrated levels 0 and 1; archive levels remain
0/1/25. Model v18.18 also warns that it predates feature specification v21.
These are classifier/analysis limitations, not grounds to restore inaccurate
rules. Anonymous exported functions limit the flow graph; source structure and
bound AST matchers still establish their destructive operations.

All six markers are written beside the extracted members. Their exact one-line
contents are recorded as marker_notes in review.json for the commit body.
