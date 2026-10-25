Second review: angular-electron 12.0.0, P7 reconstruction, my-auto-follow 1.0.7

All three originals were scanned with atomscan and cleave facts. Relevant
archive members also received facts extraction. Reports and Forager artifacts,
including .forage.json provenance, are in the task scratch/acquit-review tree.
No specimen code, remote task, or authenticated WhatsApp operation was run.

Verdicts and execution paths

angular-electron 12.0.0: BENIGN. This is Portal de Vendas, a Portuguese sales,
freight, invoicing and reporting client, packaged using an Angular/Electron
starter. resources/app.asar/package.json names main.js; that entry registers
Electron app events and creates a BrowserWindow. Normal startup constructs a
file: URL for the bundled index.html. --serve selects localhost:4200. The host
argument is stored in localStorage and used as an HTTP API base, not as the
renderer document's origin. The renderer queries /auth/config and supports
Keycloak authentication; its other API paths implement the sales application.
Its --host/--modoOperacao interpolation into executeJavaScript and its weak
renderer settings are security-relevant, but establish no malicious intent.

The renderer includes SweetAlert2 11.6.13. Its actual routine requires both a
Russian navigator.language and location.host ending in .ru/.su/.xn--p1ai. It
persists swal-initiation, waits more than three days, disables body pointer
input, then attempts looping remote audio. The packaged file: document has an
empty host; localhost development mode also fails that host gate. Loading a
remote API backend does not change location.host. Thus this bundle carries
real sabotage code without an activation path in its supplied renderer
startup. Preserve all three hostile code-presence findings, including those
on app.asar and the renderer; do not erase a genuine bundled routine to force
a benign label. Add notable declarations of contextIsolation:false and
nodeIntegration:true in webPreferences. The existing code-execution API
reference and network capabilities stay visible. Native runtime analysis was
provided by the archive scan; a separate bounded Rizin startup inspection
timed out and supplies no additional native-code conclusion. Reuse of this
renderer on a matching web origin is different deployment context, not shown
by the package startup.

The separately recovered github.githubassets.com code-view asset is BENIGN:
a GitHub React/Rspack code-view interface. Its repository navigation, editing,
source-display and same-service request handlers fit its purpose. It was
encountered through a core-js license's GitHub HTML page; it is not an
application payload or execution dependency. It retains zero hostile and zero
suspicious findings. Its original fetch URL and provenance are preserved.

p7-agent-reconstruction.js: MALICIOUS on behavior. This is explicitly a Node
behavioral reconstruction, not recovered P7 spyware and not an exploit. It
reads a JSON dump from /private/var/tmp through a keychain-named helper and
POSTs the result; this establishes neither native Keychain access nor the
contents of a genuine credential store. Its 15-second poll POSTs process.pid,
parses a returned JSON task, evaluates task.code, sends the result, and accepts
a remotely selected path for readFileSync-to-POST upload. Remote sleep tasks
replace the interval; exit stops it. The timer is installed at module load,
and uploadSecrets is called immediately. An absent local dump or transport
failure can prevent successful operation; no runtime success is asserted.
The sole active purpose is a remote code/task and file-transfer agent using
live HTTPS endpoints, without a dry-run or user-approval gate. That tips the
judgment despite plausible research use; deployment authorization is unknown.
No family attribution, browser exploit, credential acquisition, persistence,
privilege escalation, or cleanup is established. Existing suspicious
keychain-helper wording is appropriately limited to the helper's name and
its HTTP body relationship.

The new beacon rule binds the same callback name at a top-level setInterval
and its function declaration. In that function it binds fetch response -> JSON
object -> switch-selected object member -> eval. Adjacency rejects intervening
reassignments. A hostile composite additionally requires an eval-result HTTP
body. This adds actual repeated task polling rather than another alias for
remote evaluation. Result upload is an independently required same-file
observation; its description does not claim that an unrelated upload belongs
to this callback. Quoted plain-source layers are excluded.

my-auto-follow 1.0.7: MALICIOUS. The manifest is a modified Baileys library and
its README advertises private personalized socket behavior, not the remote
roster subscription policy. The ESM export reaches makeNewsletterSocket via
the socket-factory chain. That factory unconditionally schedules a two-minute
callback, fetches a publisher-controlled GitHub JSON array, and follows its
channel IDs every eleven seconds, suppressing errors. executeWMexQuery wraps
an authenticated w:mex query to s.whatsapp.net. The host caller supplies no
target or opt-in. The balance favors unauthorized subscription/engagement
manipulation despite the auto-follow package name; authorization to change
those specific accounts is absent.

The CommonJS export is materially different: config.autoFollow must be true;
a five-second timer follows a preset decoded from Base64. It decodes to a
newsletter JID. No enabling default exists in the shipped configuration. Keep
this as a capability, not an autonomous hostile follow. Bundler renaming to
executeWMexQuery2 previously hid its valid FOLLOW-selector calls; accept
numeric suffixes. Also stop the Base64-target syntax matcher at semicolons and
require FOLLOW after an argument comma: the old matcher could attribute a
later decoder to an earlier generic wrapper call. Inspect both consumers and
retain their encoded-follow attack coverage.

antiban.js is a bundled, optional automation helper. ContentVariator can insert
zero-width characters, while wrapSocket implements rate limiting and optional
auto replies. Configured webhooks report risk status; destinations are caller
configuration, not a fixed secret collector. The wrapper's send path forwards
the original content; shipping the variator does not prove unsolicited bulk
messaging. messages-media.js uses ffmpeg for thumbnail generation, downloads
requested media, derives media keys and encrypts/uploads media to WhatsApp.
Those execution, network, encoding and crypto capabilities remain notable.

Corrections and preservation

Remove two hostile fork-branding wrappers: a Git-sourced dependency alone does
not establish substitution/trojanization, and Baileys identity plus optional
zero-width variation does not establish a hostile bulk campaign. Git URLs can
also pin immutable commits. Preserve the suspicious zero-width evasion finding
and all underlying notable dependency/network/crypto observations. Relocate
the non-upstream Git-declaration helper to dependencies/manifest/source, with
an accurate name/description that makes no mutability claim. Its matcher and
upstream exclusions are retained. It is now an unconsumed OR helper, which
the engine filters from emitted scan output; its source atoms remain visible.
Do not add a redundant condition merely to force it into the report.

Before correction, audit exact consumers and every ancestor directory selector.
Neither removed hostile wrapper has an external exact consumer, and no broad
selector consumes its fork-branding ancestry. The relocated metadata helper's
only broad dependency-directory consumer is an exclusion; its Git-source atoms
already satisfied that exclusion, so the move cannot newly suppress it.

Inspect Forager-recovered @xrelly-stack/bails 2.3.6, the old wrappers' documented
positive outside this batch. It actually ships the same optional variator and
Git bridge source; those facts do not demonstrate a payload or unauthorized
operation. Keep its suspicious/notable evidence. Separately recover and trace
@elfhkry666/baileys 0.3.25, whose connection-open handler really decodes a fixed
channel and follows it silently. Compare its original and revised findings.
Run the existing 15-case shared follow-guard suite, including the original
roster-connect, connection-hardcoded and follow/mute positive fixtures.
The new focused suite checks renamed JS/TS task callbacks, unrelated timers,
local code, one-shot calls, reassignment, quoted source, bundler call suffixes,
metadata selectors, wrapper near misses, Electron declarations, Git transport,
immutable Git pins, registry dependencies, and upstream Baileys exclusions.

The three retained hostile WhatsApp traits describe one supported abuse with
factory-trigger, remote-roster and staggered-loop evidence. This does not prove
three unrelated attacks. No additional theft, payload execution, persistence
or privilege boundary crossing was found to justify a different hostile
objective. The caller-gated CJS branch and optional automation primitives must
not be promoted to meet a quota. No supported hostile behavior remains without
coverage; no matcher limitation prevents an evidenced additional objective.

Scan comparison

comparison.json contains original and controlled before/final classifier data,
all member hostile/suspicious counts, and changed notable-or-higher findings.
Initial bare --follow syntax treated its following word as an extra input;
its artifact reports remain preserved. Use explicit --follow=none and an
archived HEAD ruleset for controlled comparisons, excluding incidental fetched
references from package counts. This accounts for otherwise unrelated
low-tier/umbrella presentation differences. Asset scans are separate.

The WhatsApp archive model changes from a hostile calibrated level to level
-1 (benign) after the inaccurate convictions disappear, despite three retained
hostile follow findings. This is a classifier miss; restore neither false
wrapper nor duplicate hostile rules to compensate. The model logs also report
feature specification v18 versus expected v21. The Electron model is benign,
consistent with the packaged local-origin behavior; its retained hostile
static routine findings are deliberate. The P7 model remains hostile.

Exactly one reasoned marker is written beside each original specimen.
The final operation is make validate; no inline YARA changes require precompile.
