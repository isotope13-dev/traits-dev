# Privilege text needs container context

Four generic observations move from container runtime to
`metadata/file/string/security`:

| Former runtime ID | Metadata ID |
|---|---|
| `docker-api-privileged-field` | `privileged-json-field-text` |
| `docker-privileged-flag` | `privileged-option-text` |
| `docker-sdk-privileged` | `privileged-assignment-text` |
| `privileged-pod-spec` | `privileged-field-text` |

A field, assignment or flag does not identify Docker, Kubernetes or an SDK.
Three field/assignment matchers preserve their exact predicates, effective scope,
exclusions and criticality. Their overlapping spellings are not blindly merged:
case, quoting, value forms, scopes and exclusions differ.

The flag needed a separate correctness repair: `word: --privileged` missed the
ordinary dash-prefixed option. Explicit boundaries now recognize an enabled bare
flag or `=true`, and reject `=false` and longer option names. Its description says
*enabled option text*, rather than claiming an actual Docker invocation.

The Docker privilege roll-up can no longer accept an arbitrary `Privileged` key.
Its API branch now uses a new `docker-hostconfig-privileged-field` observation;
its other branch retains Docker run/create context plus the enabled flag.
The new matcher recognizes a direct double-quoted HostConfig field, permitting
one bounded nested sibling before it. A Privileged field *inside* that sibling
does not qualify. This is configuration evidence, not proof of container launch.

The mapping ledger contains four relocations, one new observation and the tightened
roll-up. Nine surviving consumers change, and 14 direct/ancestor decisions are
recorded. The other exact consumers retain their independent container API,
DaemonSet, hostPath, mount, namespace, command or destructive-operation legs.
Generic privilege text is no longer inherited as container context or trusted
runtime-tooling evidence through directory references.

## Verification

Run the read-only controls with:

```sh
python3 docs/taxonomy-audit/controls/container-privilege/check.py
```

All **12 targeted checks pass**. HostConfig and enabled CLI forms retain or gain
the intended configuration finding. Generic fields, assignments, standalone
flags, a nested-only Privileged field, a disabled option and a longer option do
not qualify. A real field after a nested sibling is covered. No container or
sample code is executed.

Before/after atomscan shows the generic uppercase field and nested-only field
losing their false suspicious Docker finding (risk 36 → 2). Host-root/privileged
configuration remains suspicious. The previously missed ordinary CLI flag is
recovered without accepting the disabled form. These are observed control
results, not an ML accuracy claim.

Six new benign ZIP fixtures require the neutral subject and forbid the container
runtime claim for generic configuration. The full suite passes **1,808/1,808**.
The changed files produce no hygiene errors in the final validation run. Runtime
contains **74 rules**; **166 oversized directories and zero mixed nodes** remain.
Concurrent ASP/VBScript changes were recorded separately from this cohort.

## Limits and validator follow-up

The HostConfig matcher is a bounded source-text shape, not a general JSON or
language parser. Its double-quoted Privileged form matches the previously
supported Docker API spelling; arbitrary nesting, long prefixes and other
serializations need additional structured coverage. It does not prove whether
configuration was requested, returned, documented or applied. CLI composites
still use textual command context/proximity and need a separate invocation and
argument-binding audit.

Validator opportunity: flag `word:` values that start or end with punctuation
when their ordinary standalone spelling cannot satisfy the implemented word
boundaries. Test both standalone and embedded spellings before recommending a
replacement. For boolean-like command flags, test disabled values and longer
option names as well as presence. Scope-aware duplicate checks must preserve
field-case, quoting and exclusion differences rather than merging by description.
