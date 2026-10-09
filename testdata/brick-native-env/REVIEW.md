# Brick native environment stealer triage

The bytes confirm malicious behavior in all three pinned releases:

| Artifact | SHA-256 | Verdict |
|---|---|---|
| `@brick-v2/brand@999.0.2` | `744889a725784116bb1373274ca12448ec549cf80f6bf76126504048e5928ea2` | MALICIOUS |
| `@brick-v2/brand@999.0.1` | `60848d6142632eaa7f6824abeb2941011e9e49d82610580274a5b3a92d0575a3` | MALICIOUS |
| `@brick-v2/form@999.0.2` | `b64b30bf434e1dc85ca0a3b93ea74afa7cac1833b1d63bea5a53fe76b46e10d0` | MALICIOUS |

Each tarball contains `package.json`, a JavaScript entrypoint, and a Linux
x86-64 ELF Node-API addon at `prebuilds/linux-x64/metrics.node`. The entrypoint
exports a small no-op module/logger API and loads the addon in a try block with
an empty catch. There is no manifest install hook; activation occurs on import.

Rizin disassembly of `napi_register_module_v1` shows fork, a child-only setsid,
a call to `do_report`, and child exit. `do_report` queries hostname, uname,
UID/passwd entry and current directory. It iterates a fixed list of environment
names, calls getenv, escapes quotes and backslashes in nonempty values, and
builds a JSON object. Targets include AWS credentials, GitHub tokens, npm/Node
authentication tokens, Azure Pipelines SYSTEM_ACCESSTOKEN, and Actions runtime
and OIDC-request tokens. It resolves `oob.s4yhii.com`, connects an IPv4 TCP socket
to port 10002, then sends one plaintext HTTP/1.0 POST to `/native` containing
that object. Socket send timeout is ten seconds. This is credential theft,
not a recurring beacon, a command channel, or evidence of persistence.

The two 999.0.2 addons are byte-identical (SHA-256
`daedefd6a8a02449e29a163a1a92edc0859c0cdb814ec1024b6615fa78bdd375`).
Brand 999.0.1's addon has SHA-256
`3f8833d49735dfdfe9bdef504bbb53ff069cb48a3953d9af08659d1c5560cf26`.
Its code performs the same collection and transfer; 999.0.2 adds the package
name from `_METRICS_PKG` to the JSON report. Every archive and native addon was
examined with cleave facts; no concealed executable stage was needed to explain
the behavior. JavaScript flow-analysis limitations were resolved by reading the
small entrypoint and disassembling the entire native reporting function.

## Trait corrections

- Replace three overlapping trojanization/beacon/import wrappers with one
  archive correlation under `objectives/exfiltration/stealer/env`. No
  substitution of a legitimate library or recurring beacon was demonstrated.
  The description explicitly reports a shipped stealer plus a silent loader;
  archive membership alone does not prove an arbitrary loader invokes a member.
- Rename and tighten native env exfiltration to detached Node addon credential
  collection plus key/value formatting, JSON POST, connect and send. An arbitrary
  OOB hostname no longer gates conviction. Both hostile composites exceed the
  3.5 precision authoring bar (native: 11.1; archive correlation: 8.3).
- Add a neutral ELF rodata printf JSON-member format trait. Short formatting-only
  runs were absent from extracted text, so the matcher uses section-scoped hex.
- Move the three firing AWS credential-name atoms and GITHUB_TOKEN name atom
  from cloud/vcs to secret-name. Matchers, types and platform scopes are retained;
  exact references follow the IDs, and former cloud/vcs directory consumers keep
  the moved members explicitly. Higher os/env selectors retain membership.
- Move HTTP version strings from response to message. Protocol versions apply
  to request lines as well as responses; exact consumers follow the move. No
  bare response directory consumers were found. Other generic.yaml rules remain
  accounted for: http-response stays in the response leaf.
- Remove collector-chosen archive version text from version conviction. The
  package's declared version remains evidence. The naming leaf was already at
  its 100-rule budget; no new collector-name trait or directory was introduced.
- Describe prebuild path components and the manifest files allowlist precisely;
  neither matcher by itself proves platform selection or actual addon loading.
- Add notable setsockopt import and Actions/Azure CI credential-name findings.
  Native gethostname references, JS environment writes, and bulk enumeration
  remain useful differential observations at notable criticality.
- Preserve the npm telemetry exception's suppression set with an exact OR of
  its three enumeration/copy observations. A binary-only AWS pair cannot affect
  that JS/TS exception and is omitted there to retain the suppression budget.
  Ancestor enumeration consumers have no counting threshold; one has proximity
  with needs 1 and the OR introduces no new observation location.

No directory was split or newly introduced. Historical migration evidence was
not rewritten. `check.py` records repeatable static controls without executing
sample code or checking in the malware binary. Supply the original 999.0.2
archive and a scratch directory when running it.

## Validation evidence

- Renaming the endpoint, package version, native directory, payload basename and
  outer archive preserves two hostile package findings and the native finding.
- Removing credential names, detachment, POST or JSON-member formatting makes
  the corresponding native hostile trait absent. These patched files are static
  near misses, not a claim that modified malware is benign software.
- A payload-free optional addon loader has zero hostile and zero suspicious
  findings. Neutral capabilities remain visible.
- Positive and negative controls pass for moved credential names, HTTP version
  strings, CI token names, setsockopt imports and enumeration/copy operations.
- The selective npm telemetry exception matches the narrow package-manager event
  control and does not match when bulk environment copying is added.

Judgment marker lines (each within 72 characters):

```
@brick-v2/brand 999.0.2: native env theft; fix beacon/trojan claims
@brick-v2/brand 999.0.1: native env theft; fix beacon/trojan claims
@brick-v2/form 999.0.2: native env theft; fix beacon/trojan claims
```

Final atomscan and cleave JSON scans confirm exactly two hostile findings
for each original archive. The native member has one hostile finding; its
JavaScript loader has none. The two suspicious findings record the declared
999.x version and its placeholder shape. All static controls and the exact
telemetry-exception checks pass.
