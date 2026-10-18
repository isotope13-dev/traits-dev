# JVM triage taxonomy review

Reviewed on 2026-10-18 against TAXONOMY.md and RULES.md. This review covers the
traits authored or edited for the numeric Fabric JAR and its fetched Module.jar,
including the supporting PBKDF2 and delayed-self-delete corrections. Other
concurrent triages in this shared worktree are independent.

## Placement decisions

| Required observation | Canonical home | Boundary checked |
| --- | --- | --- |
| Byte-slice void descriptor in a class constant pool | metadata/binary/symbols/descriptor | Does not establish an import or a relationship to a constructor. Rare descriptor metadata is notable. |
| String constructor reference | micro-behaviors/data/string/conversion | Ordinary reference, baseline in JVM scope; no particular input value is claimed. |
| Repeated constant-mask/state XOR byte stores | micro-behaviors/data/decode/xor | The unrolled constant reconstruction differs from an isolated XOR operation; String conversion is required separately by the concealment consumer. |
| Long-state update, mask and byte XOR/store | micro-behaviors/data/encoding/xor | The symmetric operation alone does not choose encode or decode. The String/resource consumer supplies reconstruction context. |
| XOR reconstruction with String/resource context | objectives/anti-static/obfuscation/string/runtime-decrypt | Class-local probable string reconstruction; not bound source-to-constructor data flow. |
| Obfuscated ABI reader | objectives/anti-static/obfuscation/string/runtime-decrypt | ABI arithmetic does not establish C2 infrastructure. The archive compound requires the separately admitted account loader. |
| API-specific JVM method references | Their HTTP POST, JSON serialization, memory allocation/write, remote-thread and child-stdio homes | Implementation scope is not a JVM directory; import references are not runtime execution. |
| Remote allocation/write/thread API profile | micro-behaviors/process/inject/remote-thread | No required LoadLibrary call or DLL payload, so the DLL-specific leaf was too narrow. |
| DPAPI/Base64/GCM references | micro-behaviors/crypto/decrypt | Class-local reference profile; does not assert a traced value or algorithm for every operation. |
| NSS secret decoding with file copying/JSON | objectives/credential-access/keychain/extract | No Firefox artifact was required, so the Firefox-specific classification was unsupported. |
| Copied Login Data with JDBC queries/binary-column reads | objectives/credential-access/browser/chromium | Browser-owned source is independently required, class-local; not inferred from NSS/DPAPI alone. |
| Native credential collector | objectives/credential-access/browser/multi-target | Requires the browser source, NSS extraction, DPAPI and remote-thread preparation separately. |
| Credential collector with multipart POST | objectives/exfiltration/stealer/browser | Both source and sending roles are mandatory. Description explicitly states co-occurrence, not traced payload data. |
| Python archive extraction, ProcessBuilder and child-stdin accessor | micro-behaviors/process/fd/stdio | Neutral setup profile, notable; lacks evidence binding staged source to interpreter activation. No payload sink or T1059/T1105 is claimed. |
| Native collector, Python setup and resource-string decoding | objectives/anti-static/obfuscation/string/runtime-decrypt | Requires concealment plus admitted collector; no longer asserts an interpreter-stdin payload handoff. |
| Python embedded-runtime URL | micro-behaviors/communications/http/url/archive | Reference only; neither a download nor execution. |
| POST request-line/Host framing | micro-behaviors/communications/http/message | Construction/reference to framing; no sent POST is inferred. |
| PBKDF2 algorithm name | micro-behaviors/crypto/kdf/algorithm | Name reference only; no key-factory invocation or encrypted C2 claim. |
| Browser helper staging and delayed self-deletion | objectives/evasion/self-delete/file/delay | Preserved matcher and scope; no required upload, so exfiltration placement/T1041 was removed. |

The two over-budget destination leaves were reviewed before adding API atoms.
Existing Fastjson import and parse observations were moved out of JSON
serialization. Method-unspecified URLConnection opening moved out of HTTP POST
to client/initialize. Matchers and effective scopes were preserved for those
placement moves. The bare-OR URLConnection wrapper was raised from component to
notable to match its independently meaningful legs.

A separate Fastjson detection repair follows that move: Java call facts expose
`parseObject` without the receiver expected by the old symbol regex. A Java
method-invocation query now binds the JSON/JSONObject receiver and parse method,
and the Fastjson composite separately requires its package import. An
import-only control cannot satisfy parsing. This change is not represented as a
placement-only migration.

The exact `data/encoding` partition `[base64, xor]` was admitted in Cleave's
REVIEWED_SPARSE_TAXONOMY_PARTITIONS, with no global limit change. These are
algorithm-specific, direction-neutral observations; merging the schemes would
remove required distinctions. TAXONOMY.md documents that boundary and the new
client-initialization, remote-thread and descriptor homes. The API, source and
metadata scopes remain explicit. No sample name, C2 hostname, contract address,
class namespace or exact artifact size gates these new convictions.

## Detection changes and controls

`taxonomy-mapping.json` lists old-to-new IDs. Required consumers and expectations
were updated together. The Python profile changed from suspicious to notable
after moving to its neutral stdio claim; the hostile concealment compound adds a
required resource-string decoder. This is an evidence correction, not demotion
to hide a misplaced rule. The native browser collector adds an explicit Chromium
store-reading role. A derived JAR lacking that class must lose all three new
hostile findings. The method-descriptor property changed baseline to notable.

`check.py` exercises 11 cases, including original positives, separate-class
ABI/XOR, obfuscated ABI without account access, interface declarations without
native calls, generic secret APIs without a browser source, HTTP connection
opening without POST, untyped URL opening, and Fastjson parsing/import-only.
`build.sh` regenerates the inert JVM controls and the browser-source near miss
without executing sample code. The full corpus is checked with `make validate`;
run results and final sample findings are recorded in the assessment JSON files.

The two transfer artifacts are the original 62,322-byte first-stage JAR and the
original 6,987,570-byte next-stage JAR. The reduced regression JAR and synthetic
controls are not substituted for the originals.
