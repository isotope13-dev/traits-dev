# Telegram password hooks and testmetest native sidecars

All three submitted samples are **MALICIOUS**, based on static reconstruction
and control-flow inspection. Neither Java nor native malware was executed.
`results.json` records before/after atomscan findings and model outputs.

| Input / member | Hostile before → after | Suspicious before → after |
|---|---:|---:|
| `f81d28380fbd/PasswordHook.java` | 1 → 1 | 2 → 2 |
| `14d30e64e627/PasswordHook.java` | 1 → 2 | 2 → 4 |
| `path-stream-utils-testmetest@0.0.1` archive rollup | 7 → 8 | 6 → 5 |
| `package/addon.node` | 4 → 5 | 4 → 4 |
| `package/addon_win.node` | 3 → 4 | 3 → 2 |
| `index.js`, `package.json`, `README.md`, each | 0 → 0 | 0 → 0 |

Archive rollups deduplicate member traits; do not add them to member counts.
All original hostile findings remain after canonical-ID relocation. The sole
suspicious-to-notable change is the Windows dot-prefixed script format string.
Its matcher proves neither a temporary directory nor the hidden attribute:
Windows does not hide files because their names begin with a dot. It now says
exactly what it matches under `micro-behaviors/fs/path-ops/join`. The Node
command template separately moved to `micro-behaviors/process/argument/file`. The native loader's hiding and execution
composites retain their additional evidence.

## Java control flow and judgement

`install()` resolves `org.telegram.messenger.SRPHelper`, intercepts every `getX`
method through Xposed, and executes its callback **before** password derivation.
The callback converts `event.args[0]` from bytes using UTF-8, then writes that
same value into SharedPreferences under `password`, committing with `apply()`.
The fragment's purpose is interception and retention of a Telegram password,
not SRP authentication itself. That security-boundary crossing and unnecessary
retention tip the judgement to malicious. Module packaging, caller identity,
and any owner-authorized instrumentation context are absent. These bytes do
not establish exfiltration or the application's complete deployment behavior.

The second file includes that exact implementation plus `installCompat()`.
It resolves the SRP helper's class and getX method, installs a compatibility
prehook, converts the same callback argument, and persists it with
`Pref.applyData("password", captured)`. New detection binds the callback
parameter, argument index, decoded local and stored value. Renaming local
variables preserves detection; substituting another argument source, stored
value, method or argument index prevents a hostile match.

The compatibility cache matcher binds the SRP hook and callback in one AST
pattern, so a nearby unrelated hook cannot supply the cache leg. Existing
Xposed capture rules remain intact. New neutral observations cover
Xposed interception and UTF-8 decoding. The fragments expose only one distinct
hostile behavior, implemented via one or two hook APIs. The 3–5 hostile goal
cannot be met honestly: there is no supported network send, evasion, separate
persistence mechanism, destruction or backdoor in either source fragment.

## Native loader execution paths

The package calls platform-selected native `.init()` both from postinstall and
`index.js`, swallowing exceptions. Its placeholder description does not account
for either native loader or the encrypted 8,267,868-byte `.napi_cache` member.

Linux `napi_register_module_v1` at `0x14d0` publishes `Run` (`0x1550`) as `init`.
`Run` tests CI/sandbox variables; reads PID 1 cgroup/cmdline, memory and CPU
information; and tests `TracerPid`. Positive analysis checks return without
staging. The following path parses its own directory from `/proc/self/maps`,
reads the adjacent dotfile (`0x1c11` onward), constructs XOR key `0x96` from four
constants (`0x1cc6`), transforms its buffer (`0x1d30`), forks and calls `setsid`
(`0x1df1`), writes `/tmp/.<pid>`, sets mode **0600**, and calls
`execlp("node", "node", path, NULL)` (`0x1e87`). Mode 0600 is not executable;
Node reads the source file. No loader-side removal or network fetch was found.

Windows registration jumps from `0x180003cba` to `0x180008120` and publishes
`0x180007740`. This function calls its gate at `0x180007d00`, returning on CI,
low memory/CPU, debugger, or analysis-tool process checks. The passing path
reads the sidecar, XORs it with the same key (`0x180007865` onward), writes
`%TEMP%\\.nc<pid>.js`, sets `FILE_ATTRIBUTE_HIDDEN` (`0x1800079d0`), and launches
`node "<path>"` using CreateProcessA with flags `0x08000208` and SW_HIDE.
It closes the process/thread handles without waiting. This is background
execution, not durable persistence by itself. No native self-delete was found.

The arbitrary addon/cache names no longer gate the sidecar-profile detection.
The new XOR-loop observation matches load/XOR/store instruction sequences,
independent of key and filenames. A separate hostile obfuscation composite
requires that observation plus the hidden Node staging profile. Its description
states co-occurrence; the matcher does not implement binary value-flow analysis.
Generic path/command formats and debugger imports were moved out of the
supply-chain objective. Execution chains moved to `execution/payload/file-exec`;
analysis gating moved to `anti-analysis/sandbox-detect/suite`. Package-hook
concealment remains a supply-chain inspection-evasion observation.

## Recovered payload

`recover.py` pins the submitted archive hash and reconstructs constants only:
XOR 0x96 → numeric character array → Caesar +12 → AES-128-GCM → Brotli →
custom-base64 table rotation (489) → PBKDF2/SHA-256 permutation decoding of
860 strings → AES-256-GCM/gzip extraction of 15 resources. The bundle-text
property equals the executed body byte-for-byte. No sample evaluator, import,
installer, network request or generated shell is run by the recovery script.

The clear bundle's main execution path collects filesystem and command-derived
credentials and GitHub/GitLab runner tokens, feeds collected results into its
streaming collector and sender dispatcher, and invokes repository/package
mutators using discovered tokens. Its filesystem collector reads selected
secret files and enumerates other home directories. Its runtime bootstrap
finds or downloads Bun, then supplies the recovered bundle on Bun's stdin.

Embedded resources include a process-memory reader, package republisher,
GitHub/GitLab workflows, and scripts installing persistent monitors through
systemd user services and macOS LaunchAgents. The Python monitor polls GitHub
commit search, verifies signatures, decodes tasks and executes received code.
The main bundle writes the recovered Python monitor (`Xc`) and passes its
installer (`qc`) to `bash -s`; its other persistence task similarly passes
`Zc` to bash. These resources are invoked, not merely inert embedded text.
The main bundle also evaluates a recovered update message. These actions,
together with covert installation and collection, establish a stealer/worm
with persistent C2 rather than legitimate path utilities or a placeholder.

The native loaders are corroborated by the supplied
[JFrog analysis](https://research.jfrog.com/post/beyond-testmetest-42-hijacked-github-repos/),
retrieved using forager with provenance preserved in scratch. Attribution to a
specific operator is unnecessary to the verdict.

## Checks and limitations

`verify.py` passed 12 controls covering positive compatibility capture,
renamed locals and addon/cache names, source/value/index/method and cross-hook near misses,
UTF-8 decode versus encode, and a native XOR loop without hidden staging.
Original and renamed sidecars both retain hostile detection. The separately
fetched `pkg:npm/@iobandamwer/native-helper@0.0.1` also retains every original
hostile behavior: archive 7H/6S → 8H/5S, ELF 4H/4S → 5H/4S, PE 3H/3S → 4H/2S.
This artifact and its `.forage.json` remain in scratch.

Both Java files and the npm archive remain HOSTILE in atomscan. The PE member
previously had no calibrated ML alert (`lvl=-1`, confidence 0), despite its
hostile rules; afterwards it has `lvl=25`, confidence 92. The JavaScript loader,
manifest and README still have no member-level hostile/suspicious findings;
they are interpreted in their archive context. Model v18 warns that newer
feature-spec fields are unavailable; no verdict flip or attack-coverage loss
was hidden by changing a score.

The scanner does **not** automatically perform this custom XOR/AES/permutation
recovery. The original archive gains native XOR/staging coverage, but its deep
credential collection, propagation and persistent C2 are established by the
static derivative. Existing rules recognize several recovered behaviors;
whole-bundle flow budgets and obfuscation still limit automatic deep coverage.
Recovered code and approximate class-context slices are analysis derivatives,
not original samples or automatically runnable fixtures. Runtime success and
all victim-specific branches were not observed.

Reproduce with the original sample paths and a scratch directory:

```sh
python3 testdata/triage/native-sidecar-password-review/recover.py ORIGINAL.tgz SCRATCH
python3 testdata/triage/native-sidecar-password-review/verify.py SAMPLES_DIR SCRATCH
```
