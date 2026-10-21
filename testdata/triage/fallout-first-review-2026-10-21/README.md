# First reasoned review: iterquarry, Fabric mod, Fantazy

All three supplied samples are **MALICIOUS**. These decisions follow static
execution-path analysis, not the queue's labels, scanner scores or trait names.
No specimen was executed and no embedded controller, Discord endpoint or
payload-download endpoint was contacted. Registry artifacts were downloaded
for source and version comparisons without installing them.

## iterquarry 2.2.1 wheel

SHA-256: `b3780f4d1754872aa9d1ad1ab04215cc5f4d589c3a190075dba5b8ef93e1bfdb`

`__init__.py` imports `recipes`. That module reverses its large string literal,
Base64-decodes it, inflates it with zlib, and executes the resulting source.
The source was recovered with AST literal extraction and those data transforms;
`exec` was never called during analysis.

Most recovered code implements the advertised iterable helpers. However,
`pairwise()` consumes its input to construct `"[" + ",".join(repr(x) for x in
iterable) + "]"`, then passes that string as the password to
`libseal.load_sealed_sync`. The file is the packaged `quarry.libseal` and the
module is `quarry`. It then calls the loaded module's `buffer(PASSWORD)` before
returning `itertools.pairwise(iterable)`. Authentication and missing-method
errors are silently swallowed. This is a concealed execution and input-handoff
path inside an API advertised only as an iterable operation.

The dependency was inspected separately. Libseal's documented and implemented
operation is scrypt key derivation, AES-GCM authentication/decryption, gzip
archive extraction, then Python module execution through
`spec.loader.exec_module`. The default store is inside the installed libseal
package; loading reloads the mounted module. The container header in this wheel
has `LSL1`, version/KDF 1, N=16384, r=8, p=1 and a 16-byte salt. Its encrypted
contents were **not** recovered: candidate input/password authentication failed.
No credential theft, network send, persistence or destruction is attributed to
that unknown plaintext.

The wheel's 19 populated RECORD digests and sizes match its members. This
establishes internal consistency, not a trusted publisher. Registry comparison
found that 2.1.1 had the ordinary pairwise implementation; later releases added
the sealed-module path. Two earlier decryptable releases contained a local
Hello World launcher and then a hidden Discord Hello World sender. Those older
payloads do not prove the behavior of 2.2.1. The current release both packs its
source and replaces the sealed content with a much larger encrypted object.
Its description still asserts no third-party dependencies despite declaring
libseal, and does not disclose this execution/input handoff.

The deceptive, undocumented secondary execution path tips the judgement toward
malicious supply-chain behavior over an ordinary source protector or disclosed
plugin API. Its final effects and activation input remain unknown. This is a
coverage limit: retain the one existing hostile packed-module finding and two
accurate suspicious reverse/decoder findings, rather than invent a second
hostile behavior. The new member-name observation describes the `.libseal`
suffix only. The new neutral loader-call rule detects the manually recovered
source; the current analyzer does not expose that reversed/zlib source or the
unknown-type sealed member as analyzed code in the original wheel scan.

Libseal 1.1.3 was also scanned in isolation with
`atomscan --no-update --mode slow --follow=none -f json purl pkg:pypi/libseal@1.1.3`.
It had no hostile or suspicious findings. Its source matches its disclosed
library purpose; there is no dependency exception or benign-package exemption.
The API documentation is at https://pypi.org/project/libseal/.

## matrix-client-1.21v1.jar

SHA-256: `7b9be527c4524a65c56d4d47fc0026552811828bb5b53014ab869e25cf5896e8`

This is a trojanized Fabric mod retaining Toggle Sprint Display metadata,
resources and its GUI mixin, with a foreign obfuscated initializer wired into
`fabric.mod.json`. JADX source was checked against JVM imports and bytecode.
The initializer `i$I.onInitialize()` obtains the Minecraft session, adds the
username, UUID and access token to a JsonObject, and starts a background task.
Recovered constant-only string helpers give the actual JSON keys
`username`, `uuid`, `accessToken`, `C2` and `jarFileName`.

The endpoint resolver constructs an Ethereum address, issues `eth_call` through
a list of public JSON-RPC providers, and ABI-decodes the returned string into
the remote hostname. It uses selector `0x1f1bd692`. A separate helper resolves
A records through HTTPS DNS JSON requests to 1.1.1.1 or 8.8.8.8, then constructs
raw HTTP over SSLSocket with SNI.

The initialized session object is serialized by Gson and passed to that helper
for a POST to `https://<resolved host>/api/receive/sess`. The helper writes the
POST headers and serialized bytes to the TLS stream. The next step GETs
`/api/static/loading`, iterates the returned JAR entries into byte arrays, and
uses a custom ClassLoader to define them from memory. It instantiates
`com.example.Main` and reflectively calls `initialize(String)` with the same
serialized session data. Exceptions are swallowed. These are concrete session
export and remote code-loading paths unrelated to displaying sprint state.
No account theft success or final downloaded payload behavior was observed.

Existing three hostile findings are preserved. The new suspicious exfiltration
profile requires both the existing token-handoff loader and the raw TLS POST
transport. Its description explicitly states archive co-occurrence: YAML does
not prove the cross-class data-flow relationship traced manually above.

## Fantazy.x86_64

SHA-256: `f52e8860984b0073f335d2268c67e0211a79ad478a7902ee3b6dcd4d55c88f3b`

This is a small stripped, statically linked Linux x86-64 Mirai-lineage bot.
Rizin and Capstone confirm these paths:

- ELF entry `0x400194` supplies main `0x404ba0` to startup. Main attempts to
  disable a watchdog using ioctl, changes directory, rewrites its process name
  to `/var/Sofia`, forks, calls setsid, and closes standard descriptors. It
  initializes attack handlers and starts the Huawei and Telnet scanner children.
- Main receives length-framed commands through the recvfrom wrapper at
  `0x408fd0`/`0x408fdc`. At `0x4053bb` it bounds the byte-swapped length to
  1024. The three receives at `0x4053ef`, `0x405414` and `0x405440` resolve to
  that wrapper. The body buffer is passed at `0x40545e` to parser `0x400410`.
  The parser reads duration, vector, IPv4/prefix targets and options, then
  dispatches through `0x4001c0`, which forks and invokes a registered handler.
- Retained UDP handlers configure sockets and repeatedly invoke the sendto
  wrapper (`0x409018`, syscall 44) over supplied targets. These are flood loops,
  not isolated network API references.
- Scanner `0x405f40` forks, builds raw TCP SYN probes for port 23, installs
  weighted username/password pairs, handles Telnet negotiation and prompts,
  transmits credential candidates and retries. The credential-copy loop XORs
  bytes with `0x22`; recovered device defaults include xmhdipc, juantech and
  smcadmin.
- Scanner `0x403da0` constructs and sends a POST to Huawei's
  `/ctrlt/DeviceUpgrade_1`. The SOAP Upgrade body places a command substitution
  in NewStatusURL: BusyBox downloads a MIPS bot into a hidden temporary file,
  chmods it and runs it with a self-replication argument. The delivery address
  `94.154.43.26` is a **download server**, not evidence of the C2 address.
- The table lock/unlock loops at `0x4076a0` and `0x407720` XOR all four byte
  lanes of twenty DWORD keys across each table value. The effective byte key
  is `0x3a`. The controller and report-server name entries decode to `string`;
  the controller socket is configured for port 38241. This placeholder-like
  configuration limits claims about successful controller reachability. It
  does not erase the retained attack, autonomous scan or exploit paths.

The existing framed-command matcher missed a compiler layout using rsp+disp8
for the body buffer. Its added alternative binds all three receives and parser
call to their actual relative targets and requires the body-buffer displacement
to agree. The original alternative is unchanged. Existing consumers are the
credential-bot and framed-UDP composites; both now recognize this sample.

The old static-watchdog bot rule inferred a hardcoded C2 IP from static linking,
stripping, an arbitrary external address and watchdog paths. Its exact-ID
consumer audit found no external consumer; ancestor botnet references were also
inspected. The rule now additionally requires existing attack-task evidence
(x64/i386 framed code or ARM/MIPS compact task protocols), and its description
no longer mislabels an arbitrary address as C2. A code-erased copy retaining
all former predicates fires the old matcher in an isolated rules snapshot and
does not fire the corrected matcher. All underlying structural, address and
watchdog observations remain. Existing watchdog ELF controls outside this batch
were inspected/scanned; none was a positive for this old static-bot rule.

## Verification and detection changes

`atomscan` and `cleave facts` were run on each original sample. Final atomscan
runs used `CLEAVE_TRAITS_DIR=. --no-update --mode slow`, and findings were
compared by file path, including every reported archive member. Every original
trait ID and criticality remains on these three samples. The only changed
existing description is the corrected watchdog-bot claim.

| Sample | ML probability before | After | Hostile / suspicious after |
| --- | ---: | ---: | ---: |
| iterquarry | 0.99701566 | 0.99701566 | 1 / 2 |
| Fabric mod | 0.9977569 | 0.9993745 | 3 / 4 |
| Fantazy | 0.9999222 | 0.9999224 | 7 / 11 |

The ensemble continues to flag all three; there is no sample-level disagreement
with these judgements. The wheel has the code-recovery/coverage limit described
above. No supported attack detection was removed. The intended shared-rule
reduction is that static watchdog/address co-occurrence without task evidence
no longer independently yields the hostile C2 finding.

`check.py` passes 19 static controls: original samples, redirected receive and
parser calls, a mismatched body buffer, an alternate matching displacement,
architecture/section near misses, the old watchdog predicate set without bot
code, missing JVM source/transport roles, a standalone HTTP helper, sealed-name
suffix controls and loader-call versus import-only Python controls. The existing
`minimod-heartbreaker-review-2026-10-21/check.py` also passes its three cases,
including two other malicious JAR fixtures. The final repository check is
`make validate`; inline YARA precompilation is refreshed only if that check
reports a stale precompile fingerprint.

Judgement-marker contents:

```text
iterquarry 2.2.1: deceptive input-keyed code; marks sealed member
Fabric mod trojan: steals session token; adds TLS POST profile
Fantazy Mirai: Telnet/UPnP spread and floods; fixes C2 detection
```
