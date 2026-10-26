# Package behavior review, 2026-10-26

All three supplied archives are **BENIGN** on the balance of static behavior,
packaging, and provenance evidence. This is a judgment about these artifacts,
not an assertion that arbitrary deployment of their capabilities is authorized.

## Identification and evidence

### 081537 — @tanstack/react-router 1.170.38

React routing library. The tarball SHA-256 exactly matches a fresh forager
retrieval from the npm registry. Its manifest has no install lifecycle hook;
the declared executable commands are developer build, clean, and test scripts.
Both CommonJS and ESM entrypoints lead to the shipped routing components.

Traced `link` from URL construction and protocol validation through navigation,
preloading, and IntersectionObserver callbacks. The protocol allowlist blocks
unapproved schemes. Traced `lazyRouteComponent` through the caller-supplied
importer, component selection, error handling, and sessionStorage reload guard.
The storage entry prevents repeated reloads after a missing application chunk;
it does not retain an implant. Traced `Asset` through server rendering and its
client hydration effect: it creates a script element, assigns caller-supplied
source, applies attributes, appends that same element, and removes it on cleanup.
This is real script execution capability and deserved a notable detection.
There is no hidden source fetch, unrelated command execution, or secret-transfer
path in those chains. Source and distribution implementations agree.

Fetched and inspected the four direct runtime dependencies at the declared
minimum/exact versions: react-store 0.11.0, isbot 5.1.22, history 1.162.4, and
router-core 1.171.32. Their relevant paths implement state subscription,
user-agent matching, browser history, routing, and server rendering. No hostile
stage was found. These are representative versions for ranges, not an invented
installed lockfile.

The evidence tipping the verdict is the coherent caller-driven routing and
rendering behavior, corroborated by matching registry bytes and implementation
sources. The external source's reason is unavailable. DOM script insertion and
browser storage are plausible causes of coarse malware screening, not evidence
that this particular source actually used those heuristics.

### 560163 — lightning 2.4.0

Lightning AI training/Fabric framework. Used the required
`forager fetch --all-wheels ... pkg:pypi/lightning@2.4.0`; the registry wheel is
byte-identical to the supplied wheel. The wheel's entrypoints invoke the Fabric
CLI. Root import configures logging and exports training APIs. `__setup__.py`
is packaging support, not a wheel installation trigger; its file-spec loader
loads the local packaging assistant when that module is explicitly used.

Traced both subprocess launchers: they reconstruct the current training script
or module argv, assign distributed rank/master environment variables, and
start sibling workers. The observer signals those workers and their parent
when a distributed worker fails. CUDA subprocess invocation queries
`nvidia-smi`; it is not a downloaded command. Traced the serving callback:
it starts its model server (loopback by default), polls HTTP `/ping`, posts
the configured sample to `/serve`, checks the serialized inference response,
and kills the temporary server. This is HTTP model validation, not ICMP traffic
or shell tasking. `model.eval()` switches model evaluation mode.

Traced MNIST download to cache files and then `torch.load`. Fetched both actual
S3 `.pt` resources and parsed their legacy pickle streams without unpickling or
executing them. The only reconstruction globals are torch tensor/storage
rebuilding and collections.OrderedDict; no execution/global-import gadget was
found. The transformer demo downloads WikiText as text and writes it as dataset
input. Fetched that URL as well. Checkpoint loading remains a real unsafe
serialization surface; its accurate notable detection was retained.

Fetched all nine direct base dependencies at explicit compatible releases:
PyYAML 6.0.2, fsspec 2024.6.1, lightning-utilities 0.10.0, packaging 24.1,
torch 2.4.0, torchmetrics 1.4.0, tqdm 4.66.5, typing-extensions 4.12.2, and
pytorch-lightning 2.4.0. Inspected source entrypoints and relevant loading paths,
including torch's legacy serialization handling and native-library initialization;
scanned the smaller distributions and relevant torch/PyYAML source. No hostile
chain was found. This does not claim a complete native-code audit of PyTorch,
every optional extra, or every version allowed by the dependency ranges.

The evidence tipping the verdict is the explicit distributed-training and
model-serving workflow and the inspected dataset contents. A missing deployment
lockfile and user model/checkpoint contents limit deployment conclusions.
Subprocesses, dynamic module loading, HTTP, and pickle-compatible checkpoints
could explain a coarse external malware label; its actual reason is unknown.
The supplied VT result was not used to establish the verdict.

### 1eeeb6 — @uipath/orchestrator-tool 1.202.0

UiPath Orchestrator administration CLI. The npm retrieval has the exact supplied
SHA-256. No lifecycle install hook or external runtime dependency is declared;
the dependencies are bundled. Traced `index.js` into command registration and
argument parsing, and the library entrypoint into its exported registration API.
The local dynamic imports resolve shipped filesystem/browser-launcher chunks.

Traced API configuration through the active auth context: the runtime client
uses the configured HTTPS authority, organization and tenant, Bearer token, and
optional folder headers. Generated SDK defaults do not override that client
factory. Job starts, releases, queues, assets, storage buckets, licenses,
permissions, and webhooks are explicit CLI administration operations. File
uploads/downloads use the API's returned access URLs and caller-selected files.
Token decoding, token refresh, local auth profiles, and refresh-token hash
breakers serve that authentication workflow. No browser-secret-store harvesting
or unrelated credential diversion was found.

Decoded the embedded Base64 literal: it is an Azure Application Insights
connection configuration, not program text. The bundled fallback telemetry
provider logs locally. Traced the `open`/powershell-utils code: it locates the
default browser, quotes the target, encodes a Start command as UTF-16LE/Base64,
and launches it with execFile/spawn. The policy-bypass and encoding capabilities
are real and remain notable. Container/WSL checks choose the correct opener;
they do not gate a hostile payload. The registry queries read browser association
and UiPath analytics configuration.

The evidence tipping the verdict is the authenticated, explicit administration
workflow and the absence of a concealed stage in the traced bundled code,
corroborated by the matching registry artifact. Without invocation arguments,
auth profile, job contents, or host deployment context, authorization of any
particular use cannot be inferred. Browser launching, encoded PowerShell,
credential handling and administration breadth are plausible screening triggers;
the external label's actual basis is unknown.

## Trait corrections and additions

No accurate detection was deleted or demoted. Original matcher bytes,
criticality, effective file types and platforms were retained for the moves;
explicit consumers were updated.

- Moved the two host-key assignment observations to source-assignment metadata.
  `key: machine.key` and `key: machineName` are API identifiers in this sample;
  their bytes do not establish key derivation or analysis gating.
- Moved the `releaseKey` literal to a source label observation. The match is in
  serializers/query fields, not a Socket.IO event registration. Existing RAT
  consumers retain the literal as supporting evidence.
- Moved `AUTH_ERROR_CODES` to identifier metadata. The raw token proves neither
  a complete error catalog nor trojanization.
- Moved the distinctive powershell-utils encodeCommand helper reference into
  library identity. The matched text alone establishes no hidden window.
  Its exact exclusion consumer remains connected. Broad hidden-process
  selectors intentionally no longer receive library-name evidence; those
  consumers require actual concealment, and the moved matcher has no hidden
  process claim to preserve.
- Moved both model/completion wording atoms and their wording-only group to
  natural-language metadata. Lightning's match says that model hyperparameters
  can be passed as a complete kwarg list, not that an LLM generates code.
- Retained the original while/ping/delay text pattern as source-shape metadata;
  the ICMP pacing composite now also requires a nearby ping process launch.
  The HTTP health loop is the demonstrated benign match. Actual paced ping and
  flood/ICMP exfiltration controls retain their supported detections.
- Added notable `dom-created-script-text-insertion`: a structured matcher binds
  script creation, textContent assignment and DOM insertion to the same variable
  within one statement block, excluding reassignment between those steps.
  It fires on TanStack's CJS, ESM, and TSX implementations. Wrong-variable,
  overwritten-variable, and never-inserted controls do not match.

Audited exact and ancestor consumers before relocating rules. The only broad
objective consumer affected by the release-key relocation is a CrystalX
exclusion; a bare schema label should not suppress a malware identity claim.
No malicious classification evidence was removed from that rule.

## Before/after verification

Controlled scans use local analysis, slow mode, no update, and `--follow=none`.
The baseline is the HEAD rule tree archived into scratch; the final scan uses
this worktree. This isolates rule changes from dependency-following output.
Archive-level counts are unique traits, not a sum of repeated member hits.

| Sample | Hostile before → after | Suspicious before → after | Notable before → after | Classifier before → after | Raw ML probability before → after |
|---|---:|---:|---:|---|---:|
| TanStack | 0 → 0 | 0 → 0 | 81 → 82 | BENIGN → BENIGN | 0.646142 → 0.598846 |
| Lightning | 0 → 0 | 0 → 0 | 209 → 209 | BENIGN → BENIGN | 0.411284 → 0.406214 |
| UiPath | 0 → 0 | 0 → 0 | 304 → 304 | BENIGN → BENIGN | 0.650543 → 0.704947 |

Every analyzed member also has zero hostile and suspicious findings before and
after. The reports contain 364 TanStack, 258 Lightning, and 14 UiPath analysis
units including each archive. Detailed ID/member deltas and retained attack
controls are in `review.json`. The models are v18.18 with the engine's older
feature-spec notice; probability is not a verdict or behavior proof. There is no
remaining sample rule/classifier disagreement and no material attack coverage
loss in the checked controls.

Focused regression: 13 fixtures, 31 assertions. Also compared pre-existing
out-of-batch ICMP credential exfiltration, Windows ICMP host-profile exfiltration,
Graph mailbox tasking, and CryptoAPI memory-staging fixtures before/after: every
suspicious/hostile trait remained. Positive host-bound loader, Socket.IO RAT,
and ICMP flood controls retained their original attack traits. The flood control
is copied into scratch because the shared flood objective deliberately excludes
test-directory paths. No such exclusion was weakened.

Reproduce the focused checks:

```
python3 testdata/taxonomy/package-runtime-behavior/verify.py --scratch-dir /usr/local/var/cyclotron/tmp.noindex/cyclotron-e78afdd4/scratch/review/regression
```

Original/final atomscan JSONL, full facts, member deltas, retrieved artifacts and
forager provenance are retained under the task's `scratch/review` directory.
Exactly one BENIGN marker is written beside each supplied sample. Final required
repository check: `make validate`.
