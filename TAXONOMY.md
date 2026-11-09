# cleave Taxonomy

Where a trait goes, and why. Two authors — human or model — interpreting the
same required evidence should choose the same directory. Use the semantics of
the operation, API, target or configuration; do not depend on the sample's
reputation or the consuming composite's story. Equivalent behaviors share a
home across languages and implementations.

This is the authoritative placement contract; [RULES.md](RULES.md) covers rule
syntax and matchers. Validator admission and migration acceptance are tracked
separately, in [NEW_TAXONOMY_PLAN.md](NEW_TAXONOMY_PLAN.md) and
[taxonomy-migration/](taxonomy-migration/README.md); a documented target proves
neither. The retired proposal is in the
[document archive](taxonomy-migration/research/document-authority/README.md).

**How to use it.** Read through the
[directory rules](#directory-budgets-and-placement-contracts) once, then place
each rule with the [placement procedure](#placement-procedure) and check the
[worked placements](#worked-placements). *(legacy: X)* marks a home
mid-migration ([reading paths](#reading-paths)).

## Philosophy

The taxonomy is a precise, defensible catalog of malware behaviors and
characteristics — and of ordinary software's, since malware is built from
ordinary capabilities. It aims for Linnaean rigor (one reasonable home per
observation, each child refining its parent, documented boundaries between
neighbors), borrows [MBC](https://github.com/MBCProject/mbc-markdown)'s split
of objectives, behaviors and methods, and follows Pike's economy: the fewest
predictable categories that keep different claims apart.

**Classify evidence by the behavior or objective it most plausibly indicates.**
Prefer meaningful operations, targets and purposes over their syntactic
representation. Choose the most specific interpretation supported by
distinguishing evidence; when purpose remains ambiguous, retain the shared
behavior or subject. The description must distinguish what was observed from
what is inferred. "Most likely" is grounded in the matcher's required evidence,
not in the most alarming explanation or the sample's known reputation.

Use `micro-behaviors/data/retrieve` for an acquisition observation that
explicitly admits distinct data sources, such as either a remote response or
an image. Prefer a source-specific retrieval or extraction subject when the
evidence selects one.

`micro-behaviors/crypto/key/recover` groups evidence of key recovery, including
combinations of public-key and recovered-secret-key terminology. Descriptions
must distinguish names and co-occurrences from a demonstrated algorithm.

SMB communication and protocol-specific supporting observations use
`micro-behaviors/communications/smb`; a protocol marker alone remains a
component and does not claim a successful connection.

`metadata/` is for observations that do not imply a behavior or objective.
When the required evidence reasonably points to an operation or purpose, put
the trait in the best-supported `micro-behaviors/` or `objectives/` subject,
even when it is indirect, partial, or expressed as configuration. A likely
dropper configuration belongs with the dropper objective; interpreter and
stdin clues that suggest execution belong with interpreter-stdin behavior.
Do not require proof of data flow or execution before classifying the likely
behavior. Keep the description faithful to the observed evidence and use
severity and confidence to communicate uncertainty. Use metadata only when no
meaningful behavior or objective can reasonably be inferred, and organize
those observations by their actual subject rather than a generic profile.

1. **Catalog observations, not specimens.** A sample yields many findings, each
   placed separately. Its reputation, its family, where its other rules live
   and spare directory capacity never choose a home.
2. **The matcher is the identity.** Name, description and directory reflect
   the meaning supported by the matcher, not just its grammatical form or the
   consuming composite's intent
   ([Matcher defines identity](#matcher-defines-identity)).
3. **One canonical home (the Single-Trait Rule).** MBC files Process Injection
   under both Defense Evasion and Privilege Escalation; cleave defines each
   observation once, at its most specific supported home, and composites
   reference it. Define each matcher once too: copies drift, double-count, and
   split one signal across two ML features.
4. **Each level narrows.** A child keeps its parent's meaning and answers the one
   question the parent asks of all its children. Synonyms and "everything else"
   buckets are not children.
5. **Four claims, four tiers:** mechanics (`micro-behaviors/`), intent
   (`objectives/`), properties (`metadata/`), identity (`well-known/`). An
   embedded AES implementation is a capability; a manifest naming a crypto
   dependency is metadata; a fingerprint showing the file *is* that library is
   identity; encrypting a victim's files for ransom is an objective.
6. **Claim no more, and no less, than the evidence supports.** Static evidence
   can support a probable capability or objective without proof of execution.
   Interpret operands, API semantics, targets and configuration effects before
   falling back to syntax. A reference alone does not establish an operation,
   but can still identify a meaningful behavioral subject. The directory names
   that subject or the supported inference; the description states the actual
   evidence and its limits. Never invent an algorithm, data flow, target or
   purpose, or discard one that the required evidence supports.
7. **Implementation is scope.** Language, platform, file type, backend, API
   spelling and matcher type go in `for:`, `platforms:`, the filename and the
   trait ID, not in directories — unless the platform *is* the technique
   (systemd, `LD_PRELOAD`, Winlogon).
8. **Shortest precise path.** When a directory reaches its budget, it is time
   to divide it up and reorganize the surrounding taxonomy. Review the shared
   parent and its siblings first, including earlier overflow. Divide on durable,
   evidence-supported distinctions that improve precision and leave room for
   future growth. Symmetry, count alone and ML feature depth do not define a
   distinction. Prefer breadth when siblings are equally exact.
9. **Criticality never fixes placement.** Fix a misleading classification by
   moving, renaming or tightening the rule, never by demoting it.
10. **Preserve detection.** Moves keep matchers and effective scope; detection
    fixes are separate, tested and recorded.
11. **Choose the fastest sufficiently precise matcher.** Prefer structured facts and values, then text/regex; use `hex` for simple byte patterns, YARA for richer byte signatures, and tree-sitter only when its structural accuracy is needed. Before tree-sitter, consider a composite of nearby facts or text traits. See [matcher selection](RULES.md#which-one-should-i-use) for the performance and precision tradeoffs.

## Placement procedure

1. **Write the observation and its most plausible meaning.** Identify the
   operation, affected resource and apparent purpose supported by the matcher.
   For a composite, use its *required* evidence. State what remains unknown;
   uncertainty about purpose does not erase an identifiable operation.
2. **Choose the tier** ([Tiers](#tiers)).
3. **Choose level 1:** facility, objective, artifact subject or entity class.
4. **Apply the branch's boundary and ordered tests.** Required results beat
   incidental context.
5. **Stop at the most specific home the evidence supports.** Evidence lacking
   the algorithm, mechanism or subtype stays in the broad operation leaf
   (`crypto/encrypt`, `crypto/cipher`).
6. **Check the nearest competing leaf.** If both fit, add a deciding example and
   counterexample here first. If competing purposes remain equally plausible,
   use their shared behavior or subject. Before choosing generic syntax,
   naming, literals or profiles, explain why the evidence supports no more
   meaningful placement.

### Behavioral meaning and incomplete evidence

Placement answers **what this is evidence of**; the description answers
**what was observed**. A neutral capability can be informative without being
malicious. Assigning a function to an object's member, disabling certificate
verification and configuring automatic startup can each have behavioral meaning
without establishing an attack. Lack of malicious intent is not a reason to
file a supported operation as generic syntax.

Incomplete evidence retains its subject. A distinctive Startup HTA path
assignment is evidence concerning startup persistence, although it does not
establish a write, installation or execution. A generic `.Path = value`
assignment has no such distinction. Place a reusable path reference with the
path or autorun subject; an objective-specific clue may live with that
objective when its required context distinguishes that purpose. Describe it as
evidence or an indicator, never as a completed result. Merely being useful to
an objective's composite does not make an observation objective-specific.

Use `component` only when the observation is incomplete as a standalone fact,
not merely because it is incomplete evidence for a larger objective. Neither
placement nor criticality supplies missing evidence. Consumers, including
directory selectors, must still require the roles needed for their own claim;
an indicator of persistence cannot substitute for installation or activation.

| Required evidence | Meaning and placement | Unsupported extension |
|---|---|---|
| Recognized Base64 decoding call assigned to an object member | Decoding capability under `data/decode/base64`; assignment is incidental. | Concealment or payload execution. |
| Indexed XOR expression with operation context | Bit manipulation under `data/bitwise`; describe the matched expression. | A cipher, decoding loop or obfuscation without distinguishing context. |
| Assignment disabling verification on an identified TLS client | TLS verification disabling under `communications/tls/verify/disable`. | Malicious interception merely from disabling verification. |
| Startup HTA path assignment | Startup persistence evidence, with the reference-versus-installation limit explicit. | That an HTA was written or will run. |
| Unidentified member assigned `false` | Generic assignment syntax when no resource or effect is established. | Security bypass based on an evocative variable name. |
| `NODE_OPTIONS` assignment specifying `--require` or `--import` | Runtime preload configuration under `os/env/runtime`. | That a child process started or an attacker hijacked it. |
| An authentication parameter set to `admin/admin`, or a literal default-password assignment | Credential configuration evidence under `os/security/auth/password`; describe the literal or setting. | That authentication succeeded, the value is a live secret, or default credentials were abused. |
| Parsed C# compound XOR/subtraction, or an indexed XOR expression | XOR under `data/bitwise`, subtraction under `data/arithmetic`; assignment does not erase the operation. | A cipher or concealment without algorithm or reconstruction context. |

Regex, AST and binary matchers follow the same semantic test. Consider their
effective scope: matching an example or quoted code does not establish that
the containing artifact implements it. Strengthen insufficient matchers with
focused tests rather than silently upgrading their claims or permanently
discarding their intended behavioral meaning.

For composites:

- **Required evidence decides.** `all:` requires every condition; `any:` requires
  its `needs:` threshold (one by default). A named subtype must hold for every
  passing combination. Alternatives that all establish Base64 encoding can
  support that home without `all:`; an alternative that can be bypassed cannot
  establish a mechanism. `needs:` counts `any:` matches only.
- **Count roles, not traits.** `needs: 2` can be met by two indicators of one
  source. Require each role (source, transfer, sink) separately; an `any:`
  mixing endpoints and sources can convict on endpoints alone. A directory
  selector can count both an atom and a composite derived from it; test that
  one observation cannot satisfy a threshold intended to require two roles.
  Check proximity separately: one nearby constituent can make a compound match
  appear nearby while another required constituent is distant.

- **The result owns the composite.** Trigger, carrier, transport, encoding and
  language are referenced facts, not homes.
- **Infer intent from the whole evidence.** Independent, specific clues can
  support the most likely objective without a proven data flow. For example,
  browser credential SQL, credential decryption and a webhook together support
  a credential-stealer classification. Describe the inference and matched
  evidence without claiming a completed transfer or a binding the rule does not
  establish. Generic tokens or unrelated operations alone do not suffice.
- **Analyst test:** would this path help explain what the program likely does?
  Passing validation is necessary; a less informative path is still a regression.
  Preserve algorithms, sensitive targets and lifecycle context in IDs and
  descriptions when they no longer choose the directory.
- **Migration must preserve meaning as well as matching.** Before replacing a
  behavioral home with syntax or a profile, write down the behavior and purpose
  an analyst could infer before and after the move. Lack of proven execution or
  data flow alone does not justify losing a supported inference. Keep the
  shared operation when purpose is uncertain; keep a declared functional
  interface when implementation is unknown. Put uncertainty in the description,
  rather than erasing the subject from the path. Review siblings and consumers
  together, including the effect of changed directory-selector membership.
- **One result per composite.** Split unrelated results; keep a joint rule only
  when the relationship is the observation. There is no `misc/`, `combined/` or
  `behavioral/` overflow.

## Tiers

| Tier | Holds | Does not claim | MBC analogue |
|---|---|---|---|
| `micro-behaviors/` | Probable capabilities, simple or compound, and evidence specific to their operations or resources | Malicious intent or observed execution; a reference alone does not establish an operation | [Micro-behaviors](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
| `objectives/` | Supported attack claims and explicitly described objective-specific evidence | That every constituent operation is malicious, or that an indicator establishes the whole objective | [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions) |
| `metadata/` | Artifact structure, format, declarations, provenance, measurements | That declared behavior runs, or that provenance identifies a product | — |
| `well-known/` | Identity of recognized software or malware families | That a shared capability or dependency identifies the artifact | [Corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) |

**Choose in this order:**

1. The matcher shows the artifact *is* a specific, recognized product or
   malware family → `well-known/`.
2. Required evidence supports an attacker goal, unauthorized result or abuse
   mechanism → `objectives/`. One structured matcher can qualify (an AMSI
   patch); being common in malware cannot. Objective-specific indicators follow
   the incomplete-evidence contract above and must identify their limited claim.
3. A probable capability, or evidence specific to its operation or resource,
   with no attack claim → `micro-behaviors/`.
4. An artifact property or declaration with no stronger supported behavioral
   meaning → `metadata/`. Generic representation is the final placement choice.

**References** (validated):

| Tier | May reference | Why |
|---|---|---|
| `micro-behaviors/` | `micro-behaviors/`, `metadata/`; `well-known/{app,dual-use,game,lib,tool}/` only for false-positive exclusions | Capabilities must not depend on intent or families. |
| `objectives/` | `micro-behaviors/`, `objectives/`, `metadata/`, `well-known/{app,dual-use,game,lib,tool}/`; never `well-known/malware/` | Families build on objectives, not the reverse. |
| `metadata/` | `metadata/`; `well-known/{app,dual-use,game,lib,tool}/` only for benign context | Properties must not depend on behavior. |
| `well-known/` | Everything | — |

If a capability needs an objective, one of them is misfiled or the dependency
should go.

Atomic and composite are rule forms, not tiers. A neutral operation stays in
`micro-behaviors/` whatever consumes it — Swift `Data(base64Encoded:)` is
`data/decode/base64` even inside an anti-static composite — and a compound
neutral capability stays neutral. An atom belongs in `objectives/` when its
matcher supports the attack claim or distinguishes evidence for that objective
under the incomplete-evidence contract. Generic operations stay in their
capability homes even when used by attack composites. Family-specific fragments
belong with the family in `well-known/`. Apply the criticality and dependency
requirements in [RULES.md](RULES.md) as well; placement guidance does not itself
change validator admission.

## Criticality and identity

### Levels

| Level | Meaning | Allowed in |
|---|---|---|
| `exception` | Benign-context composite that suppresses or downgrades another rule; never emitted ([below](#exception-composites)). | Composites; any tier |
| `component` | Too incomplete to state a fact alone: `&cc=`, one token of a family signature, half a marker. Composite membership does **not** make a trait a component. | Any tier |
| `baseline` | Clear but near-universal within the trait's `for:` scope (`read`, `mmap`; `USER32.dll` in a Windows GUI PE). | Any tier except `well-known/` |
| `notable` | A behavior, purpose or identity an analyst would want to see change in a version diff, even when benign: communications, code execution, crypto, encoding/decoding, privilege operations, sensitive file access, registry access, persistence surfaces, program identity, signing. | Any tier |
| `suspicious` | Evasion, intent concealment, or security-boundary crossing where legitimate use remains plausible. | Any tier; rare in `metadata/` |
| `hostile` | Clear attack pattern with no legitimate use; authoring bar precision ≥ 3.5 ([RULES.md](RULES.md#criticality-levels)). | `objectives/`, `well-known/` |

In `metadata/`, a fact that *identifies* something — signer, compiler, declared
import, runtime — is `notable`; `baseline` is for properties most files of that
type share. `well-known/` does not admit `baseline` rules: a useful named
entity or filename observation is `notable`, while an incomplete identity
fragment is a `component` and must feed a positive detection. A benign-context
composite may instead be `exception`; it is intentionally used for suppression
and is not a suppression-only building-block violation.

Product-specific account operations and related observations follow the named product. Generic role names remain generic evidence and do not by themselves identify a product.

Program- and vendor-specific observations belong with the named entity in
`well-known/`. A self-reported version field, resource string, or certificate
subject is a claim or observed field, not proof of authorship or signature
verification. Use a verified signature with the signer evidence when claiming
signed ownership. Low-tier non-malware name and signer facts do not need an
arbitrary size range; size and section constraints must reflect the evidence
and preserve legitimate carriers.

A reviewed non-malware preference-name fact can likewise be useful without
claiming the artifact is that product. The Plex `TranscoderH264Options` binary
observation has a validator allowance scoped to its exact trait and literal;
it reports the preference name's presence. It is not a general exemption for
unscoped binary signatures, higher criticalities or malware identities.

`component` and `baseline` remain available while composites are evaluated,
but report finalization may omit unreferenced low-tier findings. Downgraded
findings are retained; other retention and rescue rules also apply. Check both
matching and report emission when evaluating ML visibility. None of this makes
demotion a placement fix: a misleading observation still supplies the wrong
meaning to consumers. Use `notable` for an informative standalone fact and
repair the matcher or taxonomy when its claim is wrong.

### Prefer strong atomic traits

- **Membership does not set criticality.** A complete call, import, command,
  protocol operation, path access or product identity that informs on its own is
  `notable` (`urlopen()`, `execve`, AES use, a registry write).
- **Standalone test:** if the only honest description of the finding on its own
  is "fragment" or "part of", it may be a `component`; otherwise it is not.
- **Strengthen before settling for a component:** a structured matcher, call
  argument, anchored token or proximity bound.
- **Never demote to hide duplicate output;** consolidate instead.
- **A bare `any:` composite shares its legs' criticality.** With no `all:`,
  `unless:`, `not:`, `downgrade:`, `needs:`, size or scope, and the same
  `for:`/`platforms:`, it fires exactly where a leg fires. Raise the legs or add
  the filter that earns the higher level.
- Criticality is part of the [ML feature](#ml-features); set it from
  confidence, never to shape features.

### Matcher defines identity

**A trait's name, description and directory must reflect what its matcher
supports**, at every criticality. This includes a defensible behavioral
interpretation, not only a transcription of syntax. State the observed evidence
precisely and distinguish an indicator from an established operation or result.

A regex that only reads `$_SERVER['HTTP_REFERER']`, named
`http-referer-to-reflection` and filed under
`objectives/command-and-control/backdoor/webshell/…`, is mislabeled (it never
checks reflection) and misplaced (reading a request header is a neutral
capability). The reflective dispatch lives in the composite's other legs. Move
and rename the atom to a `micro-behaviors/communications/http/…` capability
("reads the Referer header") and reference it from the webshell composite.

### Names an attacker or a collector chose

**A trait may match a filename; a conviction may not depend on one the attacker
or the collector picked.**

- **Mandated by the format** (`SKILL.md`, `package.json`, `AUTOEXEC.BAT`,
  `MANIFEST.MF`): a platform property, fine to require in `all:`; a `notable`
  fact in `metadata/`, `micro-behaviors/` or `well-known/app/`.
- **Chosen by the attacker** (a dropped `motivate.bat`, a `_runtime.js`
  sidecar, a campaign token, a C2 hostname): real evidence, but the next build
  can rename it for free. It corroborates in `any:`; it never gates in `all:`.
- **Chosen by a collector** (the outer archive's name, such as
  `Win32.Volk.7z`): assigned when the specimen was filed; no attack information
  at any criticality.

The line is container versus member: the format or the attacker names a member;
whoever downloaded it names the container. **Every conviction needs a
content-derived required leg.** One built only from name, exact size and metric
counts is a file hash in disguise.

### Filename-based suppressions

A scanned filename or path can be chosen by an attacker or by whoever collected
the sample, so prefer content evidence when establishing an exception. A rule
may use at most one path-only trait in `unless:` and at most eight in
`downgrade:`. These limits apply to all criticalities, including building blocks
of hostile composites. A file under `testdata/` is not necessarily a test.

Count distinct path-only traits behind directory references and path-only
composites, so grouping alternatives cannot evade the limits. A composite that
requires independent content evidence is not a path-only trait. Allowed
path-based suppressions continue to operate at runtime.

Each `unless:` may select at most 64 distinct rules after expanding directory
references and referenced composites; a `downgrade:` may select at most 256.
Count duplicate references once. Narrow a broader suppressor to evidence that
actually establishes the intended context.

### Exception composites

`crit: exception` is the home for "looks alarming, but is a recognized benign
program or toolchain". The loader enforces the first three rules:

- Composite only.
- Referenced only from `unless:`/`downgrade:`, never as evidence, and
  referenced by something.
- Every leg is a named trait resolving to `notable` or another `exception`; no
  inline matchers.
- It may live anywhere; name it for what it recognizes or suppresses.

A directory reference in `all:`/`any:` skips exceptions beneath it, so folding
in a directory never inherits a suppressor. Only an exact `dir::id`, or a
directory reference inside another exception, reaches one.

A rule in `objectives/` or `well-known/malware/` whose ID or description signals
suppression (`benign`, `*-context`, `*-fp`, `*-exceptions`, `false-positive`,
allowlisting) is misplaced: make it an exception, or rename it for what it
detects. Never key an exception on something the attacker controls (a name, a
classifier field), and test the exact suppression it performs.

## Directory budgets and placement contracts

### Structure and limits

**Rules normally live only in leaves.** This applies equally to traits,
composites and aliases. The reviewed exception is the item taxonomy under
`objectives/exfiltration/stealer`: a rule belongs at the most specific item node
its required evidence supports, including a meaningful ancestor when the item
subtype is unknown or alternatives span its children. A broad credential rule
therefore stays at `credential`; it is never copied into its children or filed
under an invented `other` class. This exception does not authorize parent rules
elsewhere. Parents remain referenceable; a single child is fine if it adds
meaning. Validation enforces leaf-only placement outside the explicitly reviewed
item ancestors above; review the moved parent and its descendants against this
contract as well as running the validator.

| Validator check | Limit |
|---|---|
| Rules per directory | **80** traits plus composites is the forward maximum, summed over its YAML files and criticalities. Enforce the same limit on both the physical directory and the ID namespace: explicitly qualified IDs must not hide either population. New and reorganized leaves stay below 80; 72 rules triggers a neighborhood review and split. Existing larger leaves remain migration debt under the engine’s current 93-rule gate. A category-specific exception requires a complete relevance audit and explicit approval; filenames create no budgets. |
| Subdirectories | Hard error above 150 immediate subdirectories. Split broad catalogs by a stable function with a tiebreaker. |
| Depth | Soft warning beyond five levels below the tier (`objectives/a/b/c/d/e/f/x.yaml` warns). Soft warnings fail `make validate`; `cleave validate --soft` only reports them. |
| Sparse siblings | For behavior and objective parents, a soft warning when ten or more child directories average eight or fewer rules per child. Reports child count, total rules, and average rules per child; strict validation fails until the parent is reviewed. Named-entity catalogs and metadata are outside this heuristic. |
| Sibling stems | Soft warning on shared stems. A shared stem is not synonymy (account identity ≠ process accounting); document the boundary or merge. |
| Platforms | Soft warning at four or more. `platforms: [all]` only in `ALL_PLATFORM_DIRECTORY_ALLOWLIST` (same file). |

`platforms: [all]` is allowed only where a fact means the same on every OS:
`metadata/package/description/{disclosure,function}`,
`metadata/package/documentation/{claims,security-advisory,source}`,
`metadata/registry`, `metadata/filename`, `metadata/path`,
`micro-behaviors/communications/url/host` and
`objectives/supply-chain/security-hold`. Security-holding status is independent
of the target OS; its policy classifier does not assert code portability.
Naming properties record the scanned
filename or naming measurements; OS-specific path rules still require their
own explicit platform scopes. An AUR package targets Linux, and source code
alone does not prove portability.

**Approaching the cap triggers division and reorganization.** At 72 rules,
review and split the directory before it reaches the forward maximum of 80.
Apply this to destinations and their affected siblings during migration;
existing larger leaves remain review debt under the temporary 93-rule engine
gate. Treat the cap as a signal to redesign the category's boundaries,
including its parent and siblings, rather than just trim its count. Establish
durable divisions into more precise, evidence-supported subjects or behaviors,
with reasonable room for future rules. Review the entire directory and its
siblings at the same time:
check each matcher against its claimed subject, relocate misplaced rules, and
consolidate equivalent matchers after comparing effective scope and conditions.
For consolidation, compare the expanded `for:` sets and effective defaults,
not just the predicate or the apparent meaning of a group name. In particular,
do not assume `source` includes every script language; cleave's current source
group excludes Ruby. A canonical rule must cover the union of the original
scopes before a duplicate is retired. Verify the affected consumers' type
gates and test each added language explicitly.
Include broad observations in the design and remove levels that merely restate
their parent or name the evidence carrier. A split is valuable when its children
express real distinctions; capacity alone, language, backend, rule form, or an
`other` bucket cannot justify a category. If the full leaf alone does not admit
a sound division, broaden the redesign to its parent or the next common
ancestor and redistribute the affected siblings together. Preserve accurate
placement throughout that redesign. Category-specific exceptions require a
complete relevance audit and explicit user approval. Historical larger-budget
reviews are audit evidence, not waivers.

**Review the neighborhood, not just the full leaf.** Inventory the parent's
children, including undersized siblings, and follow related subjects outside
that parent. A sibling may contain overflow from an earlier cap. Compare its
admission evidence with the full leaf before adding any new category. Record
the rules moved in both directions, the resulting populations, and the boundary
that explains each placement. A lower count alone is not evidence of improvement.
The same observed operation must reach the same home regardless of which leaf
previously had room. Keep genuine protocol or operation refinements distinct;
merge synonyms and remove divisions whose only explanation is past capacity.

Choose the review root at the lowest common ancestor that contains the
competing placements; move up another level when the parent's own boundary
caused the overlap. Existing siblings are not presumed correct: they may hold
overflow from an earlier budget. Redesign that shared classification before
adding children to the full leaf, and apply the resulting admission rules to
every affected sibling, including those below the cap.

### Splitting a directory

A split must place **every** existing rule, including the broadest, before
anything moves. Each new parent needs a contract stating:

1. The one question its children answer, and the evidence to enter.
2. Each child's definition, exclusions and nearest sibling.
3. A precedence rule for matchers that fit several children.
4. An example and a counterexample.

If the children cannot hold the broad observations without overlap or
overstatement, revise the split or keep a precisely named broad operation leaf.
Never invent specificity or create `other`.

### Small subject catalogs

A subject need not have a directory for each operation. The reviewed sparse
catalogs keep their distinct facts in IDs and descriptions at their shared
subject: for example `fs/swap` keeps on/off facts, `fs/link` keeps link kinds,
`os/signal` keeps dispatch/handler facts, and `persistence/login/winlogon`
keeps Userinit and credential-provider facts. This combines directory levels,
not predicates or criticalities. When a split by operation is useful, name each
child for the operation itself, such as `read` or `write`, rather than adding
an intermediate `operation` directory. Use `operation` only when it accurately
names the evidence and a more specific operation is not supported. Review every
consumer when a directory moves:
its required evidence decides whether a moved member still belongs in that
condition. A bare filename, for example, does not become a benign software
identity because an old identity directory contained it. Preserve the intended
roles and threshold when replacing a reference: an `all:` condition is one
required role, while `any:` with `needs` can count multiple matching children.
Use existing references and meaningful composites; do not add migration-only
grouping rules.

A collapse does not excuse a wrong parent. Process-injection payload chains
belong in `execution/payload/process-inject`, not C2 dropper catalogs.
PowerShell command text, options and type/member names are source properties;
actual child creation, in-process hosting and invocation retain their distinct
capability homes. Ordinary license checks and availability aborts are not
attacker execution triggers. A destructive result owns its compound, with a
required destructive target; a generic cleanup API beside an auth failure is
insufficient evidence of a wipe.

### Naming

A segment names a **subject**: what the traits beneath it detect. It must finish
"…the parent, specifically the ___ kind."

| Fails | Examples | Instead |
|---|---|---|
| Catch-alls | `core`, `common`, `general`, `misc`, `other`, `combined`, `behavioral` | Split by what each child detects. |
| Judgments | `anomaly`, `quality`, `suspicious`, `notable`, `legitimate`, `benign`, `known-good`, `safe`, `trusted`, `whitelist` | File the fact by subject; `crit:` says how unusual it is. |
| Rule forms | `metrics`, `threshold`, `scoring`, `pattern`, `indicators`, `marker(s)` | Put a count with what it counts; the threshold goes in the trait name (`few-basic-blocks`). |
| Adjectives | `sparse`, `dense`, `structural` | Partition by subject, not value. |
| Synonyms of the parent | `process/create/shell/invoke` | Merge up. Verb piles (`launch`, `invoke`, `spawn`, `run`) are the usual culprits. |
| Implementation containers | `library`, `lib`, `stdlib`, `framework`, `wrapper`, `runtime`, `provider` splitting one technique by backend | Apply the [substitution test](#implementation-layers). Fine when they name a real resource (`fs/path/library`, `os/env/runtime`, `well-known/lib`). |
| Matcher input form | `source`, `ast`, `javascript`, `python`, `pe`, `windows` | Use scope and filenames. `ast/` is a subject only when the analyzed program manipulates an AST. |

Short names are fine when the parent supplies context (`exec`, `poll`, `proxy`).

**One level, one question** (principle 4). `fs/path/` asks
*what the path points at*; siblings answering *whose* (`application/`) or *what
is done with it* (`construct/`) give one rule several homes — which is how
`fs/path/config/app/` and `fs/path/application/config/` came to hold the same
subject. Keep the axis that distinguishes behavior; move the others to filenames
(`config/app/vscode.yaml`).

`fs/path/system/{root,runtime,state,driver}` distinguishes operating-system
directory roots, installed runtime locations, system state, and driver paths.
Application state, executable and script paths, media paths, and directory
changes retain those subjects even when they mention a system location. A path
reference alone does not establish discovery, writing, payload staging, or
execution. When the evidence still points to a likely operation, keep the
partial behavior clue in the corresponding `micro-behaviors` subject and
express uncertainty in its severity and confidence. Keep a profile only when
the observations do not support one likely operation or objective.

**A trigger is not an objective.** What a payload does, what sets it off and
where it came from vary independently. A directory level per axis copies every
objective under every trigger, as `objectives/supply-chain/install-hook/` did.
The behavior owns the directory; the trigger is a referenced trait
(`metadata/package/scripts/lifecycle::…`). A level naming *when* or *how*
rather than *what is achieved* breeds duplicates.

### Reading paths

Paths are relative to their tier. `{a,b}` lists siblings; `<protocol>`,
`<mechanism>` and the like name a child's axis, not a literal directory.

- **A plain path** admits rules under its contract. Create a missing one only
  after the validator check in [migration rule 1](#migration-status-and-legacy-branches).
- ***(legacy: X)***: new rules go in the target; X keeps its existing rules,
  takes no new ones, and stays valid until empty
  ([migration map](#migration-map)).
- **Reserved:** documented, with no directory yet.
- **Retired / closed:** no new rules; existing ones migrate by claim.

Some homes named here are parents today (`mem/alloc`, `fs/read`, `fs/write`,
`crypto/kdf`, `data/{parse,serialize,format}`, `http/{client,server}`,
`process/{identity,info,enumerate,exit,terminate,control,daemonize}`): use the
matching child, never the parent.

### ML features

The pipeline builds features from **path prefix plus criticality**. The
extractor keeps the first three segments including the tier
(`objectives/evasion/kernel-hide`), so only two levels below the tier get a
direct feature.

- Directories are the feature space; criticality is signal strength.
- Group by shared behavior; no single-trait directory for a trait that fits an
  existing one.
- The prefix limit may change; never erase a real distinction to fit it.

## Capabilities: `micro-behaviors/`

Value-neutral observations of what code can probably do — MBC's
micro-behaviors: "low-level, support many objectives, and aren't necessarily
malicious". If the ID, description or matcher implies unwanted, deceptive or
abusive behavior, that part belongs in `objectives/`; only the mechanic stays
here. An OS API goes to its resource: filesystem calls to `fs`, memory to `mem`,
processes to `process`.

| Facility | Admits | Not here |
|---|---|---|
| `communications` | Exchange with peers: protocols, channels, addresses. Level 2 is the protocol or transport; level 3 the operation. | Local interface or route state (`network`); control or theft (objectives). |
| `network` | Local network resources: interfaces, routes, neighbors, resolver configuration, forwarding, traffic policy, tunnels, connectivity, shares. | Wire protocols (`communications`); reconnaissance (`objectives/discovery/network`). |
| `crypto` | Primitives and operations, keys, derivation, hashes, certificates; `provider/{cryptoapi,library}` for cryptographic implementation APIs. | Encoding (`data`), randomness (`os/random`), the file's own signature (`metadata/signed`), library identity (`well-known/lib`). |
| `data` | Transforming, interpreting or organizing data; control-flow constructs. | Data merely present (`metadata`). No `text/`, `strings/` or `words/` buckets. |
| `fs` | Files, directories, paths, filesystem properties. | Raw device I/O (`hardware`). |
| `mem` | Address spaces, memory objects, access, permissions. | Execution transfer (`process/inject`); in-memory decompression (`data`). |
| `hardware` | Device and peripheral I/O or control. | Host property queries (`os/sysinfo`); windows and widgets (`ui`); surveillance (objectives). |
| `process` | Operations on execution contexts: creation, lifecycle, coordination, process attributes, descriptors and standard streams, interpreters, attach/hook/inject. The required evidence must identify that execution-context subject. | Merely running inside a process or invoking a command-line tool is insufficient. Generic streams (`data/stream`), HTTP interception (`communications/http`), console control (`os/console`), repository operations (`revision-control`), agent policy (`data/llm`), and document operations (`data/document`) retain their subjects. Privilege is `os/privilege`; durable activation is `objectives/persistence`. |
| `revision-control` | Repository operations and policy: history, changes, references, publication and repository access. `git` covers Git operations; `repository` covers other repository and forge operations. | The incidental subprocess used to run a repository command is not the result being classified. |
| `dylib` | Native library loading, unloading, enumeration, symbol lookup. | Language modules (`os/module`); manual API resolution (`os/api-resolution`). |
| `metaprogramming` | The program inspecting, generating or transforming program structure: `ast`, `generation`, `reflection/{inspect/{class,member},resolve,invoke}`. `generation` includes turning supplied source or an AST into an executable representation without requiring its invocation; reflection inspection reads class/type or member metadata, resolution finds members, and invocation calls a resolved member. | Running compiled/generated code (`process/interpreter/eval/constructed`); an undifferentiated compiler-process launch (`process/create`; identified compilation belongs in `generation/compile`); loading, defining or activating executable classes (`process/interpreter/runtime`); an AST the *analyzer* uses to match. |
| `os` | Host services without a more specific facility: registry, services, environment, accounts, privilege, security controls, kernel, packages, autorun, sysinfo, telemetry, clipboard, console. | File, process and network operations, even through an OS API. |

| `time` | Clocks, waits, elapsed time, in-process scheduling. | OS task registration (`os/autorun`, `os/service`); evasion gates (objectives). |
| `ui` | Presentation and interaction. | Display hardware or capture (`hardware/display`); deception (objectives); framework identity (`well-known/lib/ui`). |
| `browser-extension` | Extension-host surfaces with no neutral home: `action`, `lifecycle`, `management`, `tabs`; engine-emitted `host-access/<host>` and `permission/<perm>`. | Storage, messaging, HTTP, scheduling and injection keep their usual homes; manifest authority is `metadata/permission`. |

Apple event codes for opening, quitting, activating or manipulating an application
object belong in `os/application/control`; the code is a reference and does not
establish a file target or a completed operation. An Apple event that runs script
belongs with interpreter evaluation, and unbound shell, delay or load combinations
remain evidence profiles.

Scheduled-task evidence under `os/autorun` is grouped by its role:
`task-action`, `task-principal`, `task-registration`, `task-config`, and
`task-trigger`. A principal or action reference does not alone establish that
a task was registered or ran. RouterOS scheduler operations use `routeros`;
commands that start or stop an existing task use `control`.

### Communications and local networking

HTTP headers belong with their actual subject: `header/client` for client or
device identification, `header/referer` for Referer evidence, `header/upload`
for upload protocol fields, named services
for their protocol-specific headers, and upload, telemetry or key exchange
for those operations. `header/custom` holds remaining custom header evidence.

Socket transmission under `communications/socket/send` separates `datagram`,
`stream`, and generic `message` operations from `content`-specific sends and
`reference`-only API evidence. A symbol or decoded name alone does not prove
that a send occurred. Generic stream conversion and writing remain in `data`.

HTTP authentication uses evidence-specific homes across its existing siblings.
`oauth` requires OAuth protocol, grant, authorization, client or permission-scope
evidence. An access/refresh token field or browser token read alone belongs to
`token-auth`; it does not establish an OAuth grant. `jwt` holds JWT serialization,
claims and algorithm choices. `authorization-header` holds the Authorization
field and its credential construction; custom token headers belong to
`token-auth`. `basic-auth` holds Basic authentication and its client handlers.
`auth` retains authentication operations for which a more specific mechanism is
not established. Required protocol evidence takes precedence over a generic
token name; a header construction takes precedence over the representation of
its token. For example, `grant_type=refresh_token` identifies an OAuth exchange,
while `refresh_token` by itself identifies a token field. Neither is evidence
of credential theft or proof that surrounding code is benign.

Authentication review checkpoint (85-rule cap): 48 rules were relocated across
these existing homes, with qualified references updated and effective defaults
preserved. Direct populations changed as follows:

| Home under `communications/http` | Before | After |
|---|---:|---:|
| `oauth` | 103 | 85 |
| `auth` | 93 | 84 |
| `token-auth` | 55 | 66 |
| `jwt` | 6 | 16 |
| `authorization-header` | 46 | 51 |
| `basic-auth` | 12 | 13 |

The `oauth::oauth` union now requires protocol or endpoint markers; generic
access/refresh field names alone no longer establish OAuth. Directory consumers
inherit the refined subject: OAuth exclusions lose token-only evidence, while
Authorization-header consumers gain the moved header constructions and lose
header-free token configuration and Basic-handler evidence. This does not make
authentication evidence a general benign-code exception. Further review must
address the remaining Graph resource API observations in `oauth`, HTTP service
siblings, and broad authentication-based exclusions in objective rules; these
counts are a relocation checkpoint, not a waiver or a completed neighborhood audit.

Microsoft service review: directory users, organizational relationships,
service principals, roles, delegated authority and authentication-method
configuration belong together in the existing `http/services/entra-directory`.
That resource question applies across Graph endpoints and device-registration
services. Mailboxes, calendars and document resources are not directory identity;
cross-resource Graph context remains in `http/services/microsoft`. Azure compute,
blob storage, Key Vault, DevOps and Dataverse retain their existing resource
homes. A Graph hostname alone does not identify a directory operation. Conversely,
a relative directory-role path can identify its resource without a literal host.
A generic `/lists/<id>/items` fragment belongs in `http/url/api-path`; the
Graph-host composite supplies the service context. OAuth scopes and grants
retain their protocol role; mail or task API references do not establish OAuth.

This review relocates 18 directory-identity rules from `microsoft` to
`entra-directory` and four resource-path observations out of `oauth` (three to
`microsoft`, one to `url/api-path`). The resulting direct counts are 85, 38, 81
and 78 for `microsoft`, `entra-directory`, `oauth` and `url/api-path`, respectively.
Explicit consumers keep their evidence references. Endpoint and response-field
co-occurrence descriptions must distinguish an operation's interface from an
observed invocation, traversal, read/write channel or synchronization loop.
Classify the likely operation supported by that interface, while retaining the
evidence limitation in its description; do not infer an executed loop from a
pagination field or credential retrieval from two endpoint names alone.

Code-forge service operations share a home across REST, GraphQL, SDK calls
and CLI commands when they establish the same repository or collaboration
operation. An SDK import alone establishes named-library use, not a repository
read or write. GitHub API clients therefore live under
`well-known/lib/network/code-forge/{octokit,pygithub,ruby-github-api,github-actions-client}`;
package-identity composites retain their explicit package/repository evidence,
so importing a client does not identify the scanned artifact as that library.
Credential-bearing headers belong in `authorization-header`, authenticated
client construction in `token-auth`, and a generic enabled `recursive` option
in `data/config/syntax`. The GitHub operation composite supplies the repository
tree context. `services/github` separates repository operations, collaboration,
automation, security, releases, account lookup, inference and client references.
A GitHub uploads
host is named-service evidence; release publication requires additional
transfer clues. Ordinary file-upload commands are behaviors, with exfiltration
intent supplied by the surrounding evidence.

libcurl imports and request setup belong with HTTP client behavior; they do not
by themselves establish a download or command-and-control channel. For curl
output paths, `-o` names a local destination, while `-O` requests a remote
filename and does not make the following argument a local output path.

For HTTP headers, classify by the required field's protocol role. `header/host`
holds explicit server-authority selection; `header/forwarded` holds original
client or target information conveyed by proxies, including forwarding fields
combined with URL-host reassignment. Setting `Host` belongs in the former;
reading `X-Forwarded-For` belongs in the latter. Neither alone proves spoofing.
Message framing belongs in `content-length` or `transfer-encoding`; a joint
Content-Length/chunked observation belongs with the length-conflict observations.
`security` holds browser policy and anti-CSRF controls, while credential-token
headers belong in `token-auth`. A custom spelling does not override a known
role: `X-aws-ec2-metadata-token` is credential evidence, not a CSP-like security
policy or an unclassified custom field. `custom` retains application-defined
fields whose required evidence establishes none of those more specific roles.
The sibling review relocated 29 rules and removed two unsupported C2/channel
co-occurrence composites: `custom` now has 73, `host` 8,
`forwarded` 9, `security` 24, `content-length` 9 and `transfer-encoding` 4.
PHP AJAX- or command-named request-header access is notable capability evidence.
The header name does not establish an execution sink or a remote command channel.
Match the PHP access expression in source; a string-literal matcher for the
whole expression would miss ordinary code and only recognize quoted source.

| Home | Admission and boundary |
|---|---|
| `communications/<protocol>/<operation>` | ADB, Finger, DNS, FTP, TFTP, SSH, TLS, WebSocket, RPC, gRPC, email, messaging, IRC, MCP, ICS protocols (`modbus`, `dnp3`, `s7`, `bacnet`, `ethernet-ip`, `opcua`, `profinet`). Children are operations (connect, authenticate, send, receive, serve, configure). A vendor, SDK or client library is not a protocol. |
| `communications/adb` | ADB protocol, authentication and synchronization evidence. Classify specific actions such as APK installation, idle-limit changes, file execution and port configuration by their operations. |
| `communications/finger` | Finger protocol commands and queries. Classify subsequent payload retrieval or execution under the appropriate execution objective. |
| `communications/ssh/{client,connect,configure,keys,server,transfer}` | SSH client activity, connections, client configuration, key handling and identity-file options, server activity, and file transfer. An identity-file option is key-use evidence, not proof of a connection; enabling `PermitLocalCommand` configures the client and does not establish command execution. |
| `communications/http/{client,server}` | Method-unspecified client use; server-side handling. No `request` leaf duplicating `client`. |
| `communications/http/url/api-path/{agent,command,resource,route,task,telemetry}` | API and REST path references grouped by the named subject or route. Agent paths include registration and signaling; command and task paths name their respective resources; telemetry includes heartbeat and check-in paths. A route reference alone establishes neither a request, product identity, endpoint operation nor hostile intent. Shared OpenTelemetry ingestion paths are protocol evidence, even when used by a named service. Generic paths and resource URLs use the corresponding `communications/url` subject; the former `http/url/path` leaf is retired. |
| `communications/http/{get,post,put,patch,delete,head,options}` | A required method. `head` is the HEAD method, distinct from the `header` field category. |
| `communications/http/{download,upload}` | A response saved as an artifact (ordered retries in `download/fallback`); a file or attachment sent. GET alone is `get` and POST alone `post`; neither is upload, exfiltration or execution. |
| `communications/http/{header,cookies,auth,redirect,response,form}` | Classify a header by meaning: authentication → its auth leaf (`oauth` incl. device code, `token-auth`, `jwt`, `basic-auth`; `auth` when unknown), `user-agent`, `cookies`; otherwise `header`. A cookie-jar path is `fs/path/cookie`. |
| `communications/http/services/<provider>` | A named service endpoint with no operation; an operation goes to its own leaf. Cloud metadata: provider host or path → `services/<provider>/metadata`; headers such as `Metadata-Flavor` → `header/custom`. |
| `communications/http/log-sink` | Log, event, and crash-report intake endpoints and writes to those sinks. An intake URL or header alone does not establish that an event was sent. |
| `communications/socket/{create,connect,bind,listen,accept,send,receive,close,configure}` | Lifecycle and I/O. An operation beats a transport-only fact (`tcp`, `udp`); `dial`, `wrapper-connect` and `state-connect` are not operations. Hand-built HTTP over a socket is `http/direct-socket`. |
| `communications/tls/{initialize,verify}` | TLS apart from the application protocol: setup; peer verification (`verify/callback`; `verify/disable` only for explicit disabling). Setup is not a connection; a callback or suppressed warning does not disable verification. |
| `communications/ip/{literal,parse,construct}` | Address syntax, including private ranges and defanged notation. Address text proves no connection. |
| `communications/url/{parse,construction,host,scheme,path,query,user-info}` | Generic URL structure and endpoints. HTTP scheme spelling does not create a second query taxonomy: query references use `query`, construction uses `construction/query`, and extraction or traversal uses `parse`. The former `http-query` and `http-encoded` leaves are retired; encoding alone does not establish construction or decoding. The former `http-path` subtree is retired; classify endpoint paths by their resource or request subject, with schemes and construction under their generic operation subjects. Encoded scheme spellings belong to their encoding; product-specific repository and installer references belong with the named product without claiming the containing file is that product. HTTP endpoint and API-route facts remain in `http/url`; outgoing query-bearing requests use `http/request/query`, and incoming request-parameter access uses `http/server/request`. Under `host`, `name` is for hostname identity or syntax independent of a callback role (domain references, suffixes and IDN form); `dynamic-dns` groups names provided by dynamic-DNS services; `security-service` groups security product and threat-intelligence service references; `label` records the spelling or shape of individual hostname labels; `oob` is for recognized out-of-band callback services and callback-specific host patterns. When a host is known for its callback role, use `oob`, not `name`. Within `oob`, `endpoint` records recognized callback services and unions, `package`, `execution`, `discovery`, and `request` record the corresponding accompanying evidence, `encoded` records encoded endpoints, and `label` records generic callback-shaped hostnames. General hosting, reserved examples and messaging endpoints keep their own subjects. Endpoint recognition alone does not establish contact, exfiltration, or hostile intent; behavior with an established transfer belongs under `objectives/exfiltration/oob`. `user-info` records the authority text before `@`, including hostname-shaped credentials; the destination hostname after `@` belongs under `host`. Neither establishes authentication or contact. A Wayback URL targets the archive, not its inner path. |
| `communications/url/resource-path/{identity,content,collection,file,media,archive,administration,automation,configuration,commerce}` | Path references grouped by the resource or function they name: accounts and credentials, messages and content, reports and collection, generic files, media, archives, administrative and automation surfaces, configuration, and payment or retail resources. A path alone does not establish a request or completed operation. Paths without an identifiable subject stay in neutral path evidence. |
| `communications/telephony/{call,divert}` | Telephone and application-managed VoIP calls, call control, and call-forwarding/USSD observations. Framework imports are metadata; a method name without a receiver does not establish a telecom call. Call forwarding is telephony, not `messaging/divert`. |
| `communications/ipc/<mechanism>` | Local channels: pipes, named pipes, Unix sockets, D-Bus, XPC, Binder, native-messaging hosts. Descriptor duplication is `process/fd`; shared-memory allocation is `mem`. IRC is a network protocol: `communications/irc`. |
| `communications/messaging` | Messaging operations by behavior: `send`, `receive`, `contact`, `group`, `configure`, `register`, and `channel` for persistent channel identity, subscription, mute, or attribution. A message sent through a channel remains `send`. `service-reference` records messaging-service names or endpoints without claiming contact or use. Protocol or platform refinements are appropriate when they identify a distinct mechanism; the platform host otherwise belongs under `http/services/<platform>`. |
| `communications/{proxy,capture,transfer,benchmark,flood}` | Relays (`proxy/socks` for SOCKS, `tunnel` to build an encapsulated channel, `relay` to forward over one), packet capture, protocol-neutral send wording, throughput tests, repeated sends. Attack traffic is an impact claim. |
| `network/interface` | Interface `identity` includes names and MAC addresses; `query` covers enumeration and address discovery; `configure` covers changing interface settings; `command` holds command references whose operation is not determined. Wi-Fi and Bluetooth radios and WLAN profiles → `hardware/wireless`. |
| `network/{connections,route,neighbors,dns,forward,qos,tunnel,status,share}` | Connection inventory, routes, ARP caches, resolver configuration, forwarding, traffic policy, OS tunnel interfaces (TUN/TAP, WinTun), connectivity, share mapping. DNS wire traffic stays `communications/dns`; application-level forwarding is `communications/proxy/tunnel`. |

`communications/url/query` references answer **what does the query represent
or select?** Its children classify the required content, not its scheme,
language, encoding or original overflow directory:

| Child | Required content and boundary |
|---|---|
| `command` | Command-labelled fields, OS command tokens or shell control syntax in query values. These establish neither command execution nor an injection attempt by themselves. |
| `prompt` | Prompt/instruction or explicitly chat/agent-qualified query fields, including their nearby URL/template context. A bare `q` or `task` field does not establish an AI prompt. |
| `credential` | Password, token, cookie or session-named query fields. A field name does not establish acquisition or export of an actual secret. |
| `mailbox` | A mail/eml query value containing mailbox-shaped content. An at-sign does not establish a valid address, harvested mailbox or transmitted message. |
| `profile` | Explicit visitor/product/device properties such as user ID, brand/manufacturer, platform, device model, hardware ID, IP address or country. Brand/manufacturer fields do not necessarily identify the host device; these references do not prove fingerprinting or a transmitted report. |
| `tracking` | Attribution and event/stage fields, including UTM and affiliate markers. Stage labels naming credentials or wallets do not establish collection of those items. |
| `selection` | Request options, callback/response selection, task or poll actions, pagination/chunk controls, recurrence and status fields. No selected action is claimed to have run. |
| `endpoint` | A query value containing another URL, including an encoded URL or executable/image target. Neither a redirect nor retrieval is established. |
| `structure` | Query syntax or content whose purpose remains unspecified: untyped `q`, `type/data`, alphanumeric UUID-labelled values, UID-array notation, placeholder values, generic percent encoding, or mixed command/session/token alternatives with no common narrower subject. This is a neutral fallback after interpreting the required evidence, never a home chosen for spare capacity. |

Operation evidence takes precedence over these reference classes: `urlencode`,
URLSearchParams construction/set/append and query-value interpolation belong
in `url/construction/query`; query extraction and bound traversal belong in
`url/parse`. A generic `params.get('code')` spelling identifies a keyed lookup
but does not identify URLSearchParams, OAuth or VS Code. Preserve that limited
observation in source-call metadata until the surrounding matcher establishes
the resource. A computed query-object method with a callback does not establish
iteration when the method is unidentified.

For a reference spanning content classes, use the required semantic subject:
a prompt near a nested URL remains `prompt`, while the independent nested-URL
atom is `endpoint`. A mixed OR over command, session and token keys cannot claim
that every alternative is a credential; its shared fact is `structure`. Do not
copy broad observations into each narrower child. Proximity establishes context,
not that one query's prompt contains another query's URL or that an encoded
value came from a nearby command. A transmitted query with a bound source value
records that operation; a theft objective additionally needs evidence supporting
the acquisition/export claim. Product-specific configuration signatures belong
with the named program in `well-known/`, while generic property names such as
`unique` or `ttl` remain source metadata. Named service endpoints retain their
service homes; generic query fields are not program identity.

A messaging account-deletion request establishes the requested operation, not
its success or authorization. A vault glob or method-name string alone does
not establish credential access. When executable code is generated for a child,
bind the generated value to the child's code argument before claiming that
particular code is launched; a separate nearby launch is insufficient.

A browser extension manifest's declared network-ruleset ID or path is a
manifest property; it does not establish that the ruleset file is present,
enabled or applied. A `fetch` call using a dynamically named URL is a request
observation, not proof that the value is remote or contains filtering rules.

Bluetooth-specific radio, peer and GATT observations share
`hardware/wireless/bluetooth`, regardless of language or SDK. Wi-Fi and
protocol-ambiguous or multi-radio observations stay in `hardware/wireless/network`.
A Bluetooth HCI recording command belongs with packet capture. A named API or
co-occurring discovery and write do not establish a completed peer transfer.

An Android cellular transport request or process-to-network binding concerns
network selection under `network/connections`; it does not identify a particular
interface or prove a connection succeeded. A WinPcap device path is a kernel
device-location reference, not evidence that packets were captured.

`communications/http/request/{body,credentials}` are retained subject branches,
not duplicates of generic `client` use. `body/<item>` describes what enters a
request: `construction` when no item is established, otherwise `credential`,
`command-output`, `application-state`, `file`, `environment` or `injection`.
`credentials/<origin>` describes credential provenance: `file`, `environment`,
`ci-credential`, `literal`, `application-state` or `unspecified-origin`.
An actual HTTP method belongs in its method leaf; uploading an artifact belongs
in `upload`; an inferred theft/export chain belongs in `objectives/exfiltration/stealer/<item>`.
A body field or credential reference alone claims neither transmission nor theft.
Do not rename these meaningful subject branches merely to eliminate `request`.

Don't duplicate WebSocket under HTTP, or a client library under each HTTP verb.
A port literal is not a service, scan or authentication state.
A Node HTTP module binding is an import observation, not a request. A generic
`.aread()` or `.aiter_bytes()` call is stream evidence unless its receiver or
required context identifies an HTTP response. An HTTPS-prefix test does not
itself select a client, and handling a `requests` exception does not prove a
request occurred. Consumers that require an HTTP request must require a request
observation separately.

Protocol configuration follows the configured facility, not its INI/JSON
carrier. `communications/irc/configure` admits recognized endpoint, identity,
transfer-policy, script-list and saved client-control settings. A protocol-ambiguous server/port setting stays in
`communications/socket/configure` and declares an endpoint, not a connection; a warning-disable setting
changes transfer policy, not proof of a received file. A custom variable named
`%flserv` or `%flport` alone does not establish either role. Saved values must
be described as saved state, not evidence that an action succeeded.

Use a stronger subject when it is required: DDE server settings belong with
DDE, a scanner's range/active/result fields with network-survey evidence, and
mining algorithm or donation settings with mining. Neither generic `pools`
nor an unspecified `Port` directive identifies those purposes. Named script
registrations retain their interpreter/configuration meaning; composites that
establish a deceptive role or transfer policy retain the corresponding
objective. A field name such as `telegramEnabled` identifies the setting but
does not prove its value is true or that a message was sent.

Parsing configuration is a separate data operation; recognizing its section
syntax is format metadata. Bare path references keep their `fs/path` homes.
A matcher requiring a recognized facility setting together with its value
belongs with that configured facility. The IRC children distinguish command
vocabulary/construction (`command`), event registration (`handler`) and declared
settings (`configure`); none substitutes for actual message transmission.

`communications/http/upload/file` holds file-upload calls and specific
file-backed upload indicators, including partial API and command evidence.
These indicate an attempted upload; they do not prove that it succeeded or
that a particular file reached the destination. A generic stdin body, endpoint, configuration field, or file and HTTP clues
merely co-occurring belong with their observed subjects unless they point to a
likely upload operation. API names and declared settings remain references
under the relevant operation or configuration; they do not establish a completed upload. Captured media and
ciphertext entering request bodies belong to their `request/body` subjects.

`hardware/display/screenshot` records likely host-display capture behavior,
including partial indicators. Use `display` for a whole-display target, `window`
for a window target, `reference` for generic capture names and `unspecified`
when the target or operation is not more specific. Named capture libraries belong
in `well-known/`; general graphics without a likely capture purpose belongs with
its observed operation. A reference or co-occurrence does not establish a call,
successful capture or exfiltration. Browser-page screenshots and canvas
serialization are image operations under `ui/graphics/image`.

`mem/protect/modify` records memory-protection calls and syscalls, separating
executable permissions from changes whose permissions are unspecified. Memory
allocation, protection constants, indirect-call byte patterns, and unbound API
names remain separate evidence. A process-handle API can target the caller;
without a bound target it does not prove a remote process was modified.
A protection request does not prove that it succeeded or that code ran.

`communications/socket/connect` groups attempted connections by a concrete
endpoint, TCP, or an otherwise unspecified transport. A specific `connect`
call or operation-specific API reference belongs here as partial evidence of
an attempted connection; it does not establish that the connection succeeded.
A generic socket constructor, import, syscall wrapper name, or unresolved
method reference belongs with the socket operation or its neutral symbol subject. Dial aggregates must require an actual connection
observation.

`fs/write/file/full/{string,bytes,unspecified}` records APIs that write a
supplied value to a file, classified by the observed value. It does not imply
that existing contents were truncated or that the write succeeded. Use the
sibling `fs/write/file/unspecified` when an API or method reference suggests a
file write but does not establish whether it replaces, appends, or otherwise
changes only part of the file. Descriptor and stream writes belong with their
actual I/O operation. A partial API reference remains a write behavior clue;
use severity and confidence to reflect its limits. Writes to a specific
configuration or agent-instruction target belong with that target.
Source-level write calls and operation-specific partial clues belong in the
write taxonomy even when the surrounding file also contains unrelated context.
Read-filter-write sequences belong under `fs/write/file/transform`; proximity
alone does not establish that the read and write use the same file.

Proxy and tunnel classifications follow the evidenced operation. An actual
forwarding flow belongs under `communications/proxy/relay`; configuration
changes belong under `communications/proxy/config`. Command text, tunnel provider names, proxy API names, unbound transport
co-occurrences and frame field names belong with their observed communication,
named provider, or neutral format subjects. Their presence
alone proves neither a live tunnel nor a link between sockets. A call to
install a tunnel client is `os/package-manager/runtime-install`, not network forwarding.

`communications/http/client/initialize` records construction or opening of an
HTTP client or connection object without a required request method. An
`HttpURLConnection` cast beside `openConnection()` belongs here; a bound POST
method belongs in `http/post`, and an arbitrary `openConnection()` without an
HTTP receiver does not establish this subject. Opening the object does not
prove network transmission. Library spelling belongs in the ID and scope.
`communications/http/client/script` records script-element and script-loading
evidence; `client/frame` records frame-loading evidence. Other resource or
element source observations stay in `client/resource` when the resource type
is not established. A source reference does not prove execution or compromise.

### Cryptography

**Operation beats presence.** An AES encryption call is `encrypt`; an AES
implementation signature (tables, S-box) is AES presence — two observations,
not one matcher copied. A direction-specific constructor goes with its
direction but claims initialization, not transformed bytes; imports and
constructors alone never map to MBC Encrypt Data.
Name the operation directly in the path, such as `encrypt` or `decrypt`; do
not add an `operation` level when the specific verb already supplies it.
Unbound text that merely resembles an operation name remains text evidence.

| Home | Admission and boundary |
|---|---|
| `crypto/symmetric/<algorithm>`, `asymmetric/<algorithm>`, `hybrid` | Primitive or implementation presence with no narrower operation ("contains AES", not "encrypts files"). `aes/initialize` records a non-directional constructor; `aes/mode` records mode-specific presence; `aes/transform` covers an AES operation whose direction is not established. `hybrid` is symmetric payload crypto plus asymmetric key wrapping. |
| `crypto/primitive` | Evidence spanning distinct primitive families when no single algorithm or operation describes the group. A marker is partial evidence, not proof that the primitive was used. |
| `crypto/{encrypt,decrypt,sign,verify}` | The operation, whether or not the algorithm is known. `decrypt/transform` separates symmetric and asymmetric methods from decryption whose method is unspecified; constructors remain in `decrypt/initialize`. |
| Public-key signatures | Signing and verification use `crypto/sign` and `crypto/verify`. Named primitive presence stays with its algorithm; an undirected class or symbol reference stays in metadata. MACs, key formats and the file’s own signature retain their own subjects. The former `crypto/asymmetric/signature` directory is retired. |
| `crypto/cipher/{mode,io,authentication,reference,unspecified}` | Cipher behavior without a more specific algorithm or direction. Separate mode selection, cipher-stream I/O, authentication-tag handling, named references and otherwise unspecified cipher use. Put algorithm-specific evidence under that algorithm when it is established. |
| `crypto/hash/{digest,hmac}` | Cryptographic digest or MAC, including implementation presence; CryptoAPI hashing is `digest`. `digest/<algorithm>` (`md5`, `sha1`, `sha2`, `sha3`, `blake`) holds rules whose matcher names the algorithm, whatever the language; `digest/unnamed-algorithm` holds evidence that names none (`createHash(alg)`, `ComputeHash`). A digest compared against an embedded value is `os/security/auth/digest-comparison`. Mining markers are not hashing: Stratum protocol references are `communications/blockchain/stratum`, while mining-specific capabilities are `communications/blockchain/mining`. Hash-based proof-of-work belongs in `crypto/hash/proof-of-work`; it also supports non-mining uses. Noncryptographic checksums → `data/checksum`. |
| `crypto/kdf` | Key derivation, whether or not the algorithm is known (PBKDF2 parameters, salt). |
| `crypto/key/{generate,import,export,exchange,derive,representation}` | Key lifecycle and representation. Bitcoin WIF is a key representation, not a mnemonic. |
| `crypto/certificate` | Parsing, validating, installing and storing certificates. The file's own signature is `metadata/signature`. |
| `crypto/analysis` | Cryptanalysis observations, such as chosen-plaintext and key-guessing clues, without assuming a specific cipher family, target credential or hostile use. |
| `crypto/provider` | Provider acquisition and release with no narrower operation; `CryptHashData` is hashing. No remainder bucket. |
| `crypto/mnemonic` | Seed-phrase wordlists, generation and validation. Not a KDF (BIP-39 separates them). A bare `self.wordlist` is `data/collection`. |

`crypto/key/derive` records public-key or account-address derivation from existing key material, including partial operation references; key derivation functions remain in `crypto/kdf`. Within `crypto/key/representation`, `encoded` takes recognized key formats and armor, `material` holds other key or IV material and assignments, and `reference` holds names or key-object references without required material. An encoded format takes precedence over material.

`crypto/decrypt` divides decryption evidence by stage: `initialize` holds
selecting or creating a decryptor, including a specific API reference;
`transform` holds decryption calls, algorithms and partial evidence of the
transform. A `CreateDecryptor` reference is initialization, while a `decrypt`
call belongs to transformation. Neither establishes that plaintext was produced.
Mixed decryption and unrelated network or resource co-occurrences stay in their
respective profiles rather than asserting one bound operation. Explicit XChaCha20
transformation and operation-specific XOR, HMAC and key helper references
belong to their behavioral subjects even when only names are available.

`crypto/encrypt` separates `initialize`, `transform`, `file`, `sensitive`,
`reference`, and `unspecified` evidence. References do not establish a call;
file and sensitive-data subjects require evidence of that subject, while mixed
stages stay unspecified. Cipher authentication-tag retrieval belongs under
`crypto/cipher/authentication`.

`crypto/symmetric/stream/rc4` divides by the evidence's algorithmic role.
`key-schedule` holds key scheduling and initialization clues; `transform` holds
keystream generation and buffer transformation; `cipher` holds cipher
construction, named references and combined evidence spanning those phases.
Combined KSA and PRGA evidence takes precedence into `cipher`. A KSA loop is
`key-schedule`; generic array swaps without cipher evidence remain source syntax.
A PRGA buffer XOR is `transform`; an unrelated LFSR XOR is not RC4.

`crypto/symmetric/stream/sigma` holds the sigma constant shared by Salsa and
ChaCha; it does not select either algorithm. Algorithm-specific calls belong
to their respective families, including XSalsa under Salsa. Direction-neutral
stream-cipher names and transformations use `stream/reference` and
`stream/transform`; a known encrypt or decrypt direction still takes precedence.

**Signature direction needs evidence.** A reference to
[`java.security.Signature`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/security/Signature.html)
supports public-key signature capability; it does not choose signing or
verification. Every passing alternative must establish that public-key subject.
A bare `Signature` name, key import or hex string does not. WebCrypto's
[`sign` and `verify` also support HMAC](https://www.w3.org/TR/2017/REC-WebCryptoAPI-20170126/#hmac);
those method names alone do not establish asymmetric signature support.

<a id="implementation-layers"></a>**Implementation-layer substitution test.**
Swap the library or backend for another that performs the same operation. If
only the directory would change, the level is not a subtechnique.
`crypto/library`, `http/lib`, `aes/runtime-library`, `string/library` and
`process/create/stdlib` fail; renaming them `framework`, `provider`, `wrapper`
or `runtime` does not help. Embedded library code follows its capability; a
dependency declaration is metadata; the analyzed library's own identity is
`well-known/lib/<function>`. Linking style, vendoring and handwritten code are
evidence differences, not techniques.

**Ledgers and wallets are not crypto primitives.** Transaction construction,
authorization (allowances, permits), financial-transaction signing, submission
and record queries → `data/transaction/{construct,authorize,sign,submit,query}`;
chain RPC → `communications/blockchain/client`; provider-specific endpoint
references → the provider in `well-known/`; RPC fields and provider sets → the
evidenced blockchain protocol or operation; wallet UI → `ui/controls/wallet`; wallet files
→ `fs/path/wallet`. Signing arbitrary messages is `crypto/sign`.
An indexed XOR expression printed as a character is `data/bitwise/xor-forms/indexed`; it does not alone establish decoding or delivery. An XOR-named function without an observed operation is source function naming; XOR cipher or key wording in a string literal is a cryptography literal, not an implementation.

A keyed XOR cipher is `crypto/symmetric/xor`; XOR scrambling is
`data/{encode,decode}/xor`; a bare XOR instruction is neither.

### Data

| Home | Admission and boundary |
|---|---|
| `data/{encode,decode}/<scheme>` | A required direction. Keep a scheme child only if the matcher establishes it: Base16 → `hex`, `base32`, ASCII85/Z85 → `base85`, standard and URL-safe → `base64`. Repeated decoding is a refinement; origin or spelling (`request-base64`) is not. `DecodeString` without its receiver does not identify Base64. |
| `data/encoding/<scheme>` | Direction-neutral scheme evidence (an embedded Base64 alphabet); asserts no operation. |
| `data/{compress,decompress}/<algorithm>` | Directional compression; languages and libraries share the algorithm leaf. |
| `data/codec` | Direct evidence for a codec interface or support spanning directions; keep a known scheme in the trait ID. A flat leaf may remain until a matcher-proven child axis fits every rule. Unknown scheme alone does not admit a child; never add an `unknown` or `other` bucket. Size alone does not justify a split. |
| `data/compression` | Composite findings that relate encoding/decoding to compression/decompression or span codec schemes or directions; direct codec evidence stays in `data/codec`. |
| `data/{parse,serialize,format}/<format>` | Parsing representation into objects; serializing objects into representation (JSON, YAML, protobuf, pickle; general record fields in `serialize/schema-object`, host and system fields in `serialize/schema-system`, credential-shaped records in `serialize/schema-credential`, cookie fields in `serialize/schema-cookie`, and payment fields in `serialize/schema-payment`); formatting (`format/string` for number text, `format/credentials` for token shapes). Format identity alone is metadata. |
| `data/archive/{create,extract,list,modify}` | Code that manipulates archives. A rule binding a member to its extracted file is `extract`, though it also writes. |
| `data/{string,buffer,collection,property}/<operation>` | Operations on strings, byte buffers, collections (DOM trees in `collection/dom`) and object members (`property/{access,assign,define,enumerate}`), classified by receiver and operation, not method name. |
| `data/{arithmetic,bitwise,checksum,reassembly,transaction}` | Numerical arithmetic; bit manipulation; noncryptographic integrity checks; reassembly; ledger transactions. |
| `data/db/<operation>`, `data/config/<operation>` | Database and persistent-store operations, engine in the filename: `read`, `write`, `delete`, `enumerate`, `open`, `monitor`, and schema (`schema/{introspection,relational,stored-code,delete}`). Rows, documents and key/value entries share their operation; `write/row` and `delete/row` collapse to `write` and `delete`. Dropping a database or schema object is `schema/delete`; clearing stored entries is `delete`. Configuration reads and writes; a configuration file path is `fs/path`. |
| `data/control-flow/{branch,loop,dispatch,error-handling,assert,return,sequence}` | Execution-path constructs. A method named `Run`, an indexed invocation or a computed call is `dispatch` until its receiver shows a launch. `dispatch` answers *how is the callee selected?*: `named` (a fixed name such as `Run` or `Create`), `computed` (a runtime expression: bracket access, a variable function, an indexed callback), `selector` (a `switch` or lookup on a command or decision value) and `indirect` (a machine-level pointer or register call). The first row that fits wins; a call through a computed name that is also a known launcher stays `computed` until its receiver shows a launch. |
| `data/stream/{read,write,transfer,buffer,configure,record}` | Generic stream access and data movement, buffering, readiness/blocking settings and recording. File or peer-specific operations retain `fs` or `communications`; explicit process standard-stream operations use `process/stdio`. A method named `write` alone does not identify a stream. |
| `data/document/<operation>` | Manipulating document properties, embedded objects, spreadsheet cells and document opening. Document event callbacks are `os/application/hook`; the scanned document's own format and macro counts remain `metadata/document`. |
| `data/{embedded,llm}/<operation>` | Embedded resources; model inference, sessions, permission policy and tool calls. An agent permission setting or tool declaration does not establish child-process creation. Prompt text that overrides policy is `objectives/evasion/security-bypass/llm`. |

`data/property/access` records member lookup or a property value read. Selecting
a constructor or calling a computed member is `control-flow/dispatch/computed`;
returning an indexed result is `control-flow/return`. Installing a Proxy getter
is `property/define`. A required ordering between calls and member reads belongs
in `control-flow/sequence`. Literal-array indexing stays with `collection/array`.
Passing a member value to a directly named callback is `control-flow/direct-call`;
a DOM selector that binds collected password values belongs with
`ui/window/form-input`. A bare method-call spelling remains source-call metadata,
and a dictionary token or field-name string remains literal or naming metadata.
These distinctions depend on the required operation, not available directory space.

`data/control-flow/loop` answers **what controls repetition?** Its children are
`unconditional` (no header continuation test, or a backward unconditional jump),
`counted` (a numeric range, bound or stride), `collection` (element/key traversal
or a recognized iteration callback), and `conditional` (another continuation
condition). An unconditional header does not prove the body cannot break or
exit; a numeric bound does not prove progress or termination. When multiple
properties appear, an explicitly unconditional header wins, then an explicit
numeric counter, then collection traversal, then another condition. Each rule
is placed once according to its required evidence.

Review the former `iteration`, `status` and `jvm-loop-method` populations with
these children. AWK `while (1)` belongs with unconditional loops; a foreach over
users belongs with collection traversal, regardless of its original leaf. A
bare label or GOTO does not prove repetition: labels are naming metadata and
GOTO is `data/control-flow/transfer`; a loop requires a backward edge. A method
named `repeat`, `retry` or `keepAlive` with no established receiver is naming
metadata. A `range(...)` call without a loop constructs a sequence; a bare
`.iter()` spelling with an unidentified receiver is a method-name observation.
Loop-clause words that do not establish the continuation behavior remain
source-syntax metadata. Try-protected loops belong with `error-handling` when
that protection is the required distinction; a switch in a loop is selector
dispatch. The `loop` prefix denotes repetition evidence, so prefix consumers
must be reviewed when misplaced labels or method names leave this family.

`data/control-flow/error-handling` distinguishes `try`, `catch`, `register`,
`retry`, `signal`, `suppress`, `report`, and `reference`. Keep bare error names
and exception-constructor text as references; they do not establish that an
exception was thrown, handled, or concealed.

`data/control-flow/branch` requires a choice of execution path or value. It
is not a general home for every operation appearing in a condition. A buffer
comparison stays `mem/compare`, a port test stays `communications/socket/port`,
and an early return stays `data/control-flow/return`. JSON decoding, grouping,
frequency ranking, collection filtering and miner startup keep their own
subjects even when they occur in an `if` or `switch`. A response-header switch
that selects a handler is selector dispatch; a switch with no callee evidence
is a branch. Looking up a command-keyed map entry alone does not prove that
entry was invoked.

Membership testing without a required control transfer belongs in
`data/collection/membership`; constructing a set is `collection/create` and
intersecting or pruning its members is `collection/filter`. `collection/group`
groups elements by a field; `collection/frequency` counts or ranks occurrences;
`collection/measure` measures cardinality. `collection/atom-table` covers
local and global Windows atom-table operations without assuming IPC.
Generic frequency operations do not
require an LLM or a voting objective. A model-specific decision context stays
`data/llm/decision`, with the description distinguishing co-occurrence from a
bound model-to-action flow.

The former `control-flow/analysis` bucket is not an admission category. File
syntax density is metadata, computed calls are computed dispatch, caught-error
processing is error handling, and a bare `iter`/`for_loop` name is naming
metadata. Mixed OR-profiles that include names, traversal APIs and actual loops
must describe their shared source indications; they cannot assert that every
alternative establishes iteration. Similarly, fetched data, membership tests
and host queries without binding evidence do not prove remote authorization
or gated execution.

YAML `load`/`Unmarshal` belong in `data/parse/yaml`; `dump` belongs in
`data/serialize/yaml`. A format conversion follows its required output:
`YAMLToJSON` belongs in `data/serialize/json`. A package import by itself
is import metadata. Direction-neutral JSON or property-list APIs such as
`NSJSONSerialization` and `NSPropertyListSerialization` belong in `data/codec`;
their names do not establish serialization rather than parsing. A dictionary
bridge belongs with map operations, and a payload-named assignment without a
conversion call remains assignment syntax. A list append containing a key/value pair does not prove
YAML parsing or duplicate-key support, and a commented-out guard is comment
evidence rather than an active parser policy.

Database placement asks **what does the required evidence do with stored data?**
Use an identified operation before a backend reference. `localStorage.getItem`,
a Redis key enumeration, and a SQL SELECT of stored columns support `read`,
`enumerate`, and `read` respectively. `setItem` and an INSERT share `write`;
`removeItem`, FLUSHALL and DELETE share `delete`. `open` requires a database
opening/connection operation or an API specific to it, not a database name.
`monitor` registers for changes. The description distinguishes an API reference,
query text, call, and bound result; moving query text does not prove execution.

`query` holds query preparation/execution whose result remains unspecified and
query expressions that do not themselves require reading stored values. A
`SELECT` invoking an unidentified function is not necessarily a record read.
Constructing a query object (`HKSampleQuery`) is query preparation; invoking
`readRecords` against an identified record store is a read. Preserve this
distinction instead of labeling every query-related API as retrieval.
`access` holds store/interface references or interactions whose direction is
not fixed; a read-or-write alternation belongs there. An identifiable store
reference is more informative than generic source syntax, but does not gain
a read or write claim. `sql` is retired: route by the required operation or interface, not the SQL spelling.
`read/column` holds named projections and column-reader APIs; `read/key-value`
holds associative storage lookups; `read/records` holds record/result-set reads
and their query references when no narrower column or key-value claim is
required. A known column projection takes precedence over a general record
query. These homes preserve whether the evidence is a query, reference or call.
SQL editor integration belongs under `ui/controls/editor`, named service routes
under `communications/http/services`, and connection diagnostics retain their
connection or query context. A method reference can retain its operation
without claiming that it executed.
Stored credential operands retain their significance in IDs and descriptions;
ordinary credential reads do not alone establish theft. Method replacement
belongs with function interception, and storage-path strings remain paths.

`data/source` is retired: its rules split by evidence form. Syntax manipulation goes
to `metaprogramming`, execution constructs to `data/control-flow`, artifact and
language facts to `metadata`. A function *defined* with a utility's name is not
a call to it.

Within `data/bitwise/xor`, `indexed` records array and indexed-operand transforms, `scalar` records scalar or character XOR, `state` records XOR tied to mutable state, `expression` records generic source-level XOR expressions, and `instruction` records native XOR instruction sequences. State takes precedence over indexing; a stream XOR driven by a xorshift state belongs in `state`. Nearby modulo and indexed-XOR source observations without a proven relationship follow the likely bitwise operation and retain an explicit co-occurrence description. SIMD XOR mnemonics are instructions, not evidence of a cipher; native indexed XOR loops remain indexed transforms unless decoding is supported. A counted loop followed by an indirect jump is control flow, not evidence that the loop decrypted anything. LODSB, STOSB and LOOP text remains instruction evidence; adding XOR establishes a byte transform but not necessarily decryption. Unbound instruction-text co-occurrences belong with the observed instruction sequence or likely operation, without claiming a data flow.

`data/bitwise` holds XOR, masks, shifts and Boolean combinations whose
required operations manipulate bits. Its `xor`, `mask`, and `shift` leaves
group their respective operations; `mixed` holds combinations or alternatives
that do not fit a single operation. `data/arithmetic` holds numerical
operations and expressions that require or permit a mixture of numeric and
bitwise operations. A mask followed by division remains arithmetic; a mask
followed by a shift is bitwise. This is an operation distinction shared across
languages, not a claim of encryption. A bare caret cannot establish XOR in
languages where it denotes exponentiation. Similarly, JavaScript `+= 2` can
concatenate text; without known operands, retain its assignment syntax.

A required buffer-wide transform takes precedence over its individual
operators. Known XOR byte transforms belong in `data/encoding/xor` when their
direction is unspecified; additive, complement and mixed byte transforms can
remain in `data/codec`. An isolated indexed XOR expression or generic iterator
mapping does not establish byte encoding. A rolling byte hash is `checksum`,
and a PRNG state update is random generation, even when both use XOR. Encoded
product names retain their product-reference subject.

`data/decode/xor` separates `reconstruction` (required character, hex or Base64 reconstruction), `feedback` (evolving key/state), `repeating-key`, `constant`, and `transform` (other supported XOR decoding). Reconstruction takes precedence when its additional step is required, then feedback, repeating key and constant. A bare XOR operation belongs in `data/bitwise/xor`; a PRNG or complement alone does not establish XOR decoding.

`data/encoding/xor` records direction-neutral XOR scrambling structure. A
state-update/byte-XOR/store sequence fits even when the same loop can encode
and decode. Classify a required fixed key under `fixed-key`, a repeating key
under `cyclic-key`, and an operand that evolves through state, position or
feedback under `evolving-operand`. Use `unspecified-key` when a transform is
established but its keying mechanism is not. A bare XOR instruction does not
establish scrambling. Required reconstruction context can establish decoding
in a consuming rule; the atom must not acquire a direction from its consumer.

### Files, memory and hardware

A path containing a person's name is a path observation, not by itself a VM
or sandbox check. Classify it by the path subject; an actual environment
probe or avoidance decision can supply the anti-analysis behavior.

| Home | Admission and boundary |
|---|---|
| `fs/file/{create,open,close,move,rename,stat,io-mode}`; `fs/file/copy/{call,command,source-destination}` | File-object operations. Copy separates function calls, command syntax, and rules requiring source/destination context. Text/binary mode is `io-mode`; permission bits are `fs/chmod`; share and disposition flags are `open`. |
| `fs/read`, `fs/write`, `fs/delete/{file,directory,path}` | Content I/O; deletion by what is removed. Use `delete/path` when an operation can remove a file or an empty directory and its target is unknown. A sensitive filename creates no second home. A package import or path-existence check does not establish deletion; assigning a replacement to a deletion function records interception evidence. |
| `fs/directory/{create,readdir,traverse}`, `fs/search` | Create; list one directory; recurse; select by name, extension or content. `readdir/{native,command,language}` separates enumeration interfaces, shell commands and language forms. `search/{command,name,content,sensitive-file}` separates the selection predicate. A required predicate makes it `search` even when recursive. `fs/enumerate` is drive and device inventory only. |
| `fs/path/<resource>` | A location, classified by **what it points at**, not its owner or an ancestor's name (`/Library/Caches` is `cache`). For secrets, the first that fits: `password-store`, `cookie`, `private-key`, `public-key` (authorized_keys, known_hosts), `token`, `secret-config`, `config`; a generic secret directory (`/run/secrets`) or cross-family union is `credential`. Others: `wallet`, `account-db`, `certificate`, `app-data`, `personal`, `cache`, `font`, `library`, `log`, `metadata-store`, `system`, `temp`, `socket`, `stream`, `extension`, `application/{bundle,browser,executable}`. A path never proves access. |
| `fs/path-ops` | Pathname manipulation: join, normalize, parse and match remain distinct trait IDs (`Path.Combine`, `realpath`, `GetDirectoryName`). |
| `fs/{acl,attributes,chmod,chown,link,lock,sync,watch,quota}` | Permissions, attributes, ownership, links (`hardlink`, `symlink`, `junction`), file locks (not `.lock` names), sync, change monitoring, quotas. |

| `fs/temp/{file,directory}`, `fs/volume`, `fs/disk/{partition,raw}` | Creating temporary objects (a temp *location* is `fs/path/temp`); mounts; partitions and raw disk. Disk inventory is `os/sysinfo/disk`. |
| `fs/swap/{on,off}` | Activating or disabling swap. Storage-header initialization (`mkswap`) belongs in `fs/volume/format`; raw zeroing remains `fs/disk/raw` until required evidence establishes formatting. |
| `mem/{alloc,free,resize,copy,fill,compare}` | Allocate, release (`HeapFree`), resize (`HeapReAlloc`), copy, fill, compare. |
| `mem/alloc/unified` | Allocation in a unified host/device memory model, such as CUDA managed memory. Ordinary process-heap allocation stays in `alloc/heap`; a virtual mapping stays in `mem/map`. Call-shaped text records syntax, not proof of execution. |
| `mem/local-storage` | Thread- and fiber-local storage allocation, lookup, assignment and release. TLS here means thread-local storage, not transport security. These APIs do not create or schedule execution contexts. |
| `mem/{map,unmap}`, `mem/create`, `mem/anonymous/create` | Mappings (`mremap` is `map`, not proof of a size change); shared and image-section objects; private heap creation (`create/heap`, distinct from allocating from a heap); anonymous file descriptors (`memfd_create` proves no execution from it). An unbound heap API and flag observation is a memory profile. |
| `mem/{read,write,protect,query,advise,lock,gc,sync}` | Access (local, remote or physical, when established), permissions, inspection, advice, pinning, GC, cache visibility. RWX alone is neutral; writing to another process transfers no execution. |
| `mem/load` | Loading code or data into memory when the operation is not more specific; use the established copy, read, write or map operation when supported. A loader name is a reference, not proof that loading or execution occurred. |
| `mem/combined` | Composites needing one alternative across memory operations. |
| `mem/{heap-spray,stack-pivot,overflow}` | The required spray layout, stack redirection or out-of-bounds write; allocation, stack access or an unsafe API alone is not enough (MBC C0006, C0009, C0010). |
| `hardware/{input,display,block,flash,gpu,wireless,smartcard,serial,iokit}/<operation>` | Device I/O and control. Input: `event`, `device`, keyboard `hook`/`listener`/`poll`/`layout`/`simulate`, mouse `position`/`simulate`, and `media` for audio-or-video interfaces (`getUserMedia`). A generic window hook is `ui/window/hook`. |

Executable-permission evidence separates hidden targets, executable creation
modes and setuid cases from ordinary mode changes. The `executable/evidence`
roll-up preserves reviewed consumers of the former mode leaf; additions to
its selected directories require consumer review. String concatenation uses
`data/string/concat/{join,append,expression}` for the evidenced operation.

### Process, OS, time and UI

Window API and handle references belong with the window operation they suggest;
record references and co-occurrence without claiming they establish a hide
operation. A supported concealment objective belongs under
`evasion/process/hidden/window`. Hidden startup configuration belongs under
`process/config/window` until there is evidence of process creation.

| Home | Admission and boundary |
|---|---|
| `process/create/<mechanism>` | Creating an execution context; see [process creation](#process-creation). |
| `process/config` | Launch records, child-process settings and creation-option references. These describe a proposed execution context without proving it was created. Application-specific settings retain their application resource. |
| `process/thread/{create,lifecycle,enumerate,group,priority,config,terminate}`, `process/fiber` | Thread or fiber management; a fiber is not a thread or a new process. Fiber creation, callback and switching references and their co-occurrence with memory operations belong to `process/fiber`. Distinguish co-occurrence from evidence that binds memory to a fiber callback. |
| `process/sync/{mutex,semaphore,event,critical-section,condition,join}` | Coordination between execution contexts, including reader/writer locks and condition variables; memory visibility is `mem/sync`. Atomic list operations remain `data/collection/list`; a lock-free list is not itself thread coordination. |
| `process/work/{queue,pool,task}` | Queue and pool management; task submission, completion, waiting, cancellation and future/result access (`QueueUserWorkItem`, `dispatch_async`). These do not establish thread creation. Joining a thread is `process/sync/join`; timer callbacks are `time/schedule`. |
| `process/thread/{create,worker,config,runtime}` | Thread creation, JavaScript worker execution contexts, thread-specific configuration, and runtime references. A `worker_threads` import or worker label alone does not create a thread. Generic worker-count text and unrelated pool-builder names remain neutral evidence; `xargs` work dispatch is `process/work/queue`. Creating or submitting a Windows thread-pool work item belongs in `process/work/task`, not thread creation. |
| `process/{identity,info,enumerate,argument,resources,pid}` | Current identity; attributes (`info/name` for generic process labels, thread names and name-related diagnostics); listing; arguments; limits; PID files (a PID value is not one). A recognized application's name retains its functional subject under `os/application/target`, even when spelled as a process image. |
| `process/{exit,terminate,control,daemonize}` | Ending this process (`exit/handler` for exit callbacks); killing another (a signal API without the kill signal is not); other state changes; detaching (`fork`+`setsid`). |
| `process/lifecycle/<operation>` | Lifecycle; a guard blocking a second instance (mutex, PID file, lock) is `single-instance` (MBC B0024), while a mutex alone is `process/sync/mutex`. |
| `process/debug/tool-markers` | References to debugging or tracing tooling, including executable names and paths. A reference proves neither a running debugger, a tool-owned artifact, nor an anti-analysis check; those require independent operation and target evidence. |
| `process/fd/{query,control,close,dup,stdio}` | Descriptor operations, including standard-stream redirection and descriptor duplication. Creating an IPC pipe is `communications/ipc`. |
| `process/stdio/{configure,read,write,relay}` | Reading, writing or relaying explicitly identified stdin, stdout or stderr, including captured child output and peer-to-child relays. Child standard-stream configuration belongs in `process/stdio/configure`; descriptor redirection and duplication remain under `process/fd/stdio`; generic streams are `data/stream`. A `.write()` call or an arbitrary `getInputStream()` receiver does not establish a process resource. `process/io` is retired and banned. |
| `process/tty/<operation>` | Terminal interaction and PTYs. |
| `process/interpreter/<operation>` | In-process execution: `eval/{direct,indirect,constructed,decoded,source}` plus `bof` (Beacon Object File host APIs), `wasm`, and `vm`. `eval` executes supplied code in an existing interpreter. Launching an interpreter is `process/create`; compilation without required invocation is `metaprogramming/generation`; language identity is metadata. |
| `process/{attach,debug,hook,inject}/<mechanism>` | Attaching, debugging, intercepting and transferring execution, with no established attacker purpose. |
| `process/deploy/<sink>` | Neutral acquisition- or staging-to-activation chains (an updater fetching and launching its image), by the [payload sinks](#payload-activation-and-staging). |

| `dylib/{load,unload,lookup,enumerate}` | Native loader operations. Language modules are `os/module`; export walking or API hashing is `os/api-resolution`; hiding import identity is an anti-static claim. |
| `os/registry/<subject>/<operation>` | Prefer the affected key subject when known: `autostart`, `association`, `browser`, `com`, `credential`, `desktop`, `environment`, `explorer`, `hive`, `network`, `network-provider`, `policy`, `print`, `process`, `scheduled-task`, `service`, `session-manager`, or `software`. Use `reference` for an observed key path, `create` for key creation, `write` for supported value mutation, and `clear` when either emptying or deleting a value has the same effect; an unknown target falls back to `value/write`, `read`, `open`, `delete`, `create`, `copy`, `close`, `enumerate` or `monitor`, or broader `access`. Opening or creating a key alone does not establish a value read or write, and names or paths do not establish access. Remote registry operations belong under `registry/remote`; importing a registry file is `registry/import`. Use `hive` for hive references and save, restore, replace, load or unload operations; reserve `offline-hive` for an offline hive itself. When the evidence supports a clearer outcome, use that behavior instead: a Run value that names a startup program or an appended Winlogon startup program belongs in persistence, Registry Editor lockout in impact, unsafe ActiveX enablement in security bypass, and ServiceDLL replacement in service-host behavior. Execution-policy and firewall configuration clues use their security-control subjects; code-integrity policy commands use kernel security, even when they use the registry. Distinguish a control path co-occurring with write APIs from a write bound to that path. An operation-specific API or control-path co-occurrence can serve as partial evidence of that behavior; describe the uncertainty. Generic API names and unbound combinations with no identifiable operation belong in metadata. Only a Run-key write with durable activation is persistence. LSA, firewall, network and SafeBoot references follow their security, network or boot subjects; authentication-package paths are autostart surfaces. A path reference does not establish a write. |

| `os/service/<operation>` | `create`, `start`, `stop`, `delete`, `configure`, `query`, `dispatch` (running as a service), `control` (no verb). A definition field alone is configuration; user or system scope is evidence, not a branch. `launchd/config` groups configuration for either kind of launchd job. |
| `os/env/<subject>`, `os/env/<operation>` | The first required meaning wins: CI-issued credential (`ci-credentials`) → other credential (`secret-name`, e.g. `AWS_SECRET_ACCESS_KEY`) → interpreter or loader configuration (`runtime`: `BASH_ENV`, `NODE_OPTIONS`) → filesystem location (`path`) → CI job metadata (`cicd`) → user identity (`user-info`) → service configuration (`provider`). Otherwise use the operation: `read`, `enumerate`, `write`, `test`. A name is a reference, not a read; reading a secret is not theft. |
| `os/{user,group,privilege,security}/<operation>` | Principals and authority; classify account creation, modification, deletion and lookup by operation; PHP script-owner queries are file metadata operations, and group deletion under `group/delete`. Security controls include `security/auth` and `security/jailbreak`. Crossing to higher authority is an objective. |
| `os/kernel/<facility>`, `os/{syscall,bpf,container,virtualization}` | Kernel facilities (`kernel/driver` for driver installation and loading, MBC C0037/C0023, not ordinary service creation); direct syscalls; BPF; namespaces (`container/namespace`) and container runtimes; hypervisors. |
| `os/module/load`; `os/{api-resolution,linker}` | Language-module loading; manual API resolution; dynamic-linker configuration (`linker/{audit,env,load-path,symbol-version}`). Ruby `require` caches a module; `Kernel.load` evaluates the source file on each call. Native libraries belong under `dylib`. |
| `os/autorun`, `os/package-manager`, `os/sysinfo/<property>`, `os/random`, `os/telemetry` | OS task and autorun registration (malicious durability is persistence); package operations, including package-manager configuration under `os/package-manager/config`; host properties (`hostname`, `platform`, `hardware`, `disk`, `locale`, `profile`); randomness; logging and analytics. |

| `os/command/lookup` | Resolving or checking availability of commands, including shell built-ins such as `command -v`; a lookup alone does not execute the command. |
| `os/{clipboard,console,event,signal,exception,message,com,wmi}` | Host facilities. Clipboard by operation: `read`, `write`, `monitor`. COM or WMI evidence with a known function goes to that function. |
| `os/application/shell-namespace` | Operating-system shell item namespace operations, including virtual items as well as filesystem objects. PIDL manipulation belongs here; resolving a concrete filesystem path belongs in `fs/path`, and an icon drawing operation in `ui/graphics/icon`. A single shell-item API is an observation, not proof of filesystem mutation. |
| `os/application/target/<function>` | An app or package cited as the program's target (wallet brands, `SpringBoard`); neither discovery nor the file's identity. Children classify the referenced product's function, not the reference's spelling or encoding. |
| `time/{query,sleep,timing,schedule}` | Read time; wait; measure elapsed time (`timing/check`); schedule in-process callbacks (`schedule/timeout` for alarms). |
| `ui/{controls,dialog,graphics,help,menu,terminal,wallpaper,window}` | Credential-entry controls (`controls/credential`), wallet UI (`controls/wallet`), drag-and-drop interaction (`controls/drag-drop`), prompts (`dialog/prompt`), `--help` text (`help`), window hooks, enumeration and notifications. Deceptive hiding is evasion. |

Group Policy operations and preference configuration belong under `os/security/gpo`; NETLOGON and SYSVOL share paths belong under `network/share`. Field-name and nearby command clues can support a possible policy or task operation without establishing mutation, payload transfer, or destructive intent. Preserve those limits in the rule claim.

Enterprise update publishing and assignment operations belong under `os/application/update`; isolated SCCM fields remain installation metadata. Abuse of an update channel to deliver concealed or forged content belongs under `objectives/supply-chain/hidden-payload/update-service`. Routine deployment configuration alone does not establish a hostile update.

A bound flow from credential-named environment entries into an HTTP request
body is a credential-bearing HTTP operation, not merely an environment-name
reference. `PWD` alone can denote the working directory; environment-access
proximity to that token does not establish a password or credential read.

**Process admission is about the affected resource, not the host.** A native
function detour or runtime-method hook alters execution and fits `process/hook`.
Intercepting HTTP requests, wrapping console logging, overriding web storage,
handling window events, or registering application callbacks belongs with that
resource. An embedded browser is `ui/window/webview`; its native message bridge
is `communications/ipc/bridge`, while an explicit JavaScript evaluation keeps
`process/interpreter/eval`.

Standard-library imports remain metadata until use is established. A familiar
method name in an unbound destructuring expression does not identify its module.
Runtime-independent API-name references retain a naming category, without
claiming invocation.

Creation requires evidence of creating an execution context. Loading modules
uses `os/module/load` or `dylib/load`; compiler operations use
`metaprogramming/generation/compile`, with build flags under `metadata/build`.
A generic launch of an unspecified compiler remains process creation; a rule
that identifies compilation should retain that more informative operation.
Installer operations belong with package management; a package format does not
define a creation mechanism. Interpreter names and imports are metadata; COM
construction, property assignment and decoded method references retain those
operations. Language and wrapper buckets such as `shell/lang`, `shell/bridge`,
`interpreter/jscript` and `create/flags` are retired. Browser configuration is
`os/application/config`; execution-policy settings are `os/security/execution-policy`.
Macro events are application hooks, not process creation. Macro atoms for
memory, networking, strings and COM retain those facilities.

`revision-control/git/{read,write,transfer,configure}` separates repository
inspection, local mutation, remote exchange and configuration. Mixed operations
without a narrower common purpose remain `revision-control/repository`.

The retired process paths and their replacement guidance are enforced by
[`scripts/review/process-taxonomy-policy.json`](scripts/review/process-taxonomy-policy.json)
in `make validate`. Bans apply to whole subtrees, including newly nested leaves;
renaming a bad category does not exempt it from the execution-context test.

`os/application/target` asks **what function does the referenced software serve?**
All children record references, not installation, use, discovery, or ownership.
Use the narrowest function required by every passing alternative:

| Child | Admission and boundary |
|---|---|
| `wallet` | Wallet products, their stores, registered wallet-extension IDs, or catalogs confined to wallets. Wallets take precedence over the broader financial-services class; a bare exchange/payment-service name is `finance`. |
| `finance` | Exchanges, payment services and DeFi protocols without required wallet identity. Stripe fits; a MetaMask extension ID is `wallet`. |
| `browser` | Browser products and browser toolbars. Brave fits; a required Brave Wallet extension ID is `wallet`, and a media-player ActiveX control is `media`. |
| `development` | Editors, IDEs and language-runtime programs referenced by name. PyCharm and `node.exe` fit; an actual Node invocation is process creation, and a declared package dependency is metadata. |
| `productivity` | Document, spreadsheet, presentation, mail and note-taking applications. Word and OneNote fit; a document filename without a product reference belongs with its file role. |
| `security` | Defender, bot-defense and CAPTCHA products. A named security product fits; a rival malware/campaign name is `malware`. |
| `agent` | Named AI-agent products and agent packages. Hermes and OpenClaw fit; a generic word such as "agent" does not identify a product. |
| `system` | Platform application stores, platform services and desktop-shell components. Finder and Play Services fit; a browser name is `browser`. |
| `network` | Communication, file-transfer, VPN and remote-session clients. Discord, rclone, OpenVPN and LiveDesk fit; document/mail applications take `productivity` precedence, a server implementation is `server`, and a routing administration tool is `utility`. |
| `cloud` | Cloud-platform and infrastructure-provider names. GCP fits; a named bot-defense product is `security`. |
| `server` | Named application, web and database server implementations. Tomcat, nginx and SQL Server fit; an HTTP method or generic server API is a protocol capability. |
| `media` | Media-player products and their controls. RealPlayer fits; BaiduBar is `browser`. |
| `game` | Game products and their platform controls. Ourgame's GLWorld control fits; an ordinary media player is `media`. |
| `utility` | Diagnostic, administration and application-maintenance tools without a narrower required product class. CPU-Z, wmiexec and named application updaters fit; an app-store identifier is `system`. |
| `malware` | Rival malware or campaign names cited as targets. TeamPCP fits; this reference never identifies the analyzed file as that malware. |

The broadest current observations are multi-product references confined to one
function, such as wallet catalogs. A future observation spanning functions must
resolve its full population and a supported broad home before admission; it
must not be copied into several children. The placement inventory and unchanged
definition checks are recorded in
`taxonomy-migration/batches/stranded-target-functions/`.

**Referenced products are subjects, not process operations.** The same Firefox
name belongs in `target/browser` whether found in text, a string table or
bytecode. A name alone proves neither a running process nor interaction with
that product. Keep required installed locations in
`fs/path/application/executable`, browser profile/data locations in
`fs/path/application/browser`, and proxy preference names with proxy
configuration. A bare `firefox.exe` is a browser reference; a required
`Mozilla Firefox\\firefox.exe` installation path is an executable-location
reference. Generic `install_42.exe` spelling has no identified product or
operation and remains a filename observation. This precedence avoids sibling
overflow between basename, process-name and application-path catalogs.

Stream identifier names alone are source naming properties. A `stream_handler`
symbol reference belongs in `metadata/lang/source/naming/function`; a bare
`stream_stop` token belongs in `metadata/lang/source/naming/action`. Neither
establishes stream handling or shutdown. The direct stream catalog review
retains its read, write and relay observations while relocating these names;
their matchers, effective scopes and criticalities stay unchanged, and exact
consumers follow the moved observations. A bound shell/FIFO/Netcat feedback
loop remains a stream capability, with its declared FIFO under `fs/pipe` and
the reverse-shell result under `objectives/command-and-control/reverse-shell`.

Apply the same distinction across source names: a callable identity or a
population of function declarations belongs in `naming/function`; bare
action-word tokens belong in `naming/action/token`; an action word found in a
function name belongs in `naming/action/function-name`; a name identifying a
resource belongs in `naming/resource`; a source-module, package, or dynamic
library name or import path belongs in `naming/module`. These are vocabulary
observations, not proof that the named operation ran or module loaded.

An isolated partial string or source snippet belongs in
`metadata/lang/source/literal/fragment/single`; evidence requiring several
separated fragments belongs in `fragment/sequence`. Neither placement implies
that the fragments were concatenated or executed. Use a more specific subject,
including `well-known/` for a supported product or vendor identity, when the
evidence establishes one.

`process/interpreter/eval/` answers one question: **how does supplied code begin
executing inside an existing interpreter?** Admission requires execution, not a
compiler name, source-shaped string, constructor reference, or code object that
is merely produced. Its children are:

| Child | Definition and boundary | Example | Counterexample |
|---|---|---|---|
| `direct` | A recognized evaluator consumes source, a form or an expression directly. Input provenance stays in the trait name. | `eval(decoded)`; Python `exec(code)`; shell `eval "$cmd"`. | `compile(source, ..., "exec")` produces a code object but does not run it. |
| `python-builtins` | Python `eval` or `exec` built-ins and their direct argument evidence. | Python `exec(decoded)`; `eval(mapping.get(...))`. | A generic shell `eval` command stays in `direct`. |
| `indirect` | The evaluator is reached through an alias, global/member lookup, callback, bridge or other computed dispatch. The matcher must still establish evaluator semantics. | `(0, eval)(code)`; passing `eval` as a promise callback. | Calling an arbitrary variable or computed member is `data/control-flow/dispatch`. |
| `constructed` | Required evidence both creates or obtains an executable unit and invokes that unit. | `new Function(body)()`; `exec(compile(source, ...))`; `ScriptBlock.Create(text).Invoke()`. | `new Function(body)`, `ScriptBlock.Create(text)` and Lua `load(text)` without invocation are `metaprogramming/generation`. |
| `source` | A file is evaluated in the current interpreter context rather than launched as a child. | shell `source file`; PowerShell `& "file.ps1"`. | Node `Module._compile` is `os/module/load`; `bash file` creates an interpreter process. |

Precedence is `source` for a required file, then `constructed` when creation and
invocation are both required, then `indirect` when dispatch obscures or reroutes
the evaluator, then `python-builtins` for Python built-in calls, otherwise
`direct`. A decoder, decryptor, HTTP response or object
field does not create another child: those facts qualify the input, not the
execution mechanism.

Within `metaprogramming/generation`, classify the generated result or operation:
`function` constructs a callable/code object (JavaScript `Function`, PowerShell
`ScriptBlock.Create`, expression-tree compilation); `compile` compiles source
or invokes an identified compiler/toolchain; `source` constructs source text;
`transform` edits program structure or source; `format` formats source; `emit`
emits instructions or assembly/module structures. Mere execution remains under
`process/interpreter`; compilation does not establish invocation. Generic
process-launch evidence stays under `process/create`, while compiler flags and
build configuration stay under `metadata/build`.

`os/module/load/{name,path,memory,class}` distinguishes module loading by the
identified input or resolution mechanism: a module name, file path, in-memory
representation, or class-loader facility. Library references belong with the likely capability they support; named-product
evidence belongs in `well-known/`, and neutral linker or symbol facts in
`metadata/binary/`. Native loading uses `dylib/load`. A library name, import, or isolated export
neither proves the observed file is that library nor makes it benign. Avoid
blanket suppression on library-reference directories, especially when looking
for a compromised library. Modifying loader entries is `os/module/configure`,
and unbound loading/API co-occurrences are profiles.

Command approval, refusal and classification belong in `os/security/command-policy`;
redacting command secrets belongs in `os/security/redaction`. A command mentioned
inside a policy still retains its own resource when matched independently of the
policy. Audio playback is `hardware/audio/play`; cloud provisioning and resource
administration are `os/virtualization/{deploy,configure,delete}`.

#### Process creation

`process/create/<mechanism>` is an ML feature; finish "creates an execution
context by ___". **The first matching row wins:**

| The matcher shows | Directory |
|---|---|
| A thread in the current process | `process/thread/create` |
| A fiber | `fiber` |
| A clone of the current process | `fork` |
| A new shell parsing command text (`sh -c`, `cmd /c`, `shell=True`, a pipeline, `bash "$f"`, `%COMSPEC% /c`) | `shell` |
| A shell command invokes an explicit executable path (`./program`, `/dev/shm/program`) | `path-execution` |
| A program launch selects its executable from a computed variable or expression | `variable` |
| A shell invokes a variable command target | `shell/variable-command` (the target may resolve to a shell builtin) |
| An interpreter is handed source text (`node -e`, `python -c`) | `process/deploy/interpreter-command` |
| A Windows Script Host execution or script-moniker API | `process/interpreter/wsh` |
| WScript.Shell Run with an executable target | `exec` for a fixed target, `variable` for a computed target; unbound call text remains metadata |
| A process-starting cmdlet such as Start-Process or its saps alias | `cmdlet` |
| A library object standing for the child (`Popen`, `NSTask`, `ProcessBuilder`) | `subprocess` |
| Opening or dispatching a URL by its scheme or a URL-specific handler | `communications/url/open` |
| The desktop opener choosing the handler (`ShellExecute`, `open`, `NSWorkspace`) without a required URL target | `micro-behaviors/os/handler/open` |
| An API starting a child image from an argument vector or command line (`CreateProcess`, `posix_spawn`, `WinExec`, `WshShell.Run` with an executable path) | `exec` |
| Replacing the current process image (`execve`, `execveat`, `os.execv`, `pcntl_exec`) | `micro-behaviors/process/replace`; replacement does not require a new process |
| Only an executable name, launch flag, permission, import or API symbol reference | Its path, configuration or metadata observation, not process creation |

A DOS interrupt service-number comparison belongs with DOS interrupt evidence;
it identifies a tested service, not a dispatched process-creation call.

Within `shell`, `interpreter` records invocation of a shell, while `reference`
groups shell API names, command-shaped text and co-occurring clues that do
not establish an invocation. An implementation language such as VBA does
not define a separate shell-creation mechanism.
Descriptions preserve the distinction between an API reference and a call.

Remote targeting alone is not a creation mechanism. Named PsExec and Impacket
references belong to those tools; WMI command evidence belongs with WMI.
Unbound command, target and output clues follow their most likely communication
or process subject without claiming a bound flow.
A `ComputerName` argument can name the local machine and does not by itself
establish lateral movement.
`Start-Process` is a command invocation; a .NET `Process` object or start-info
descriptor is configuration until a start call is observed. Unbound object and
call names, or independent network and process clues, follow their observed
subjects without implying a relationship.
Clone-only syscall evidence without resolved flags may represent a process or a
thread; use `os/syscall/clone` rather than claiming a fork. A combined
fork-or-clone observation remains partial evidence of process creation. Fork
and clone symbol names are references, not calls.
A `daemon` symbol is daemonization evidence; loading the gawk fork extension
is an import, not a fork call. Unbound fork and shell references are partial
process evidence, not proof that the fork launched a shell.
An assigned fork result is not a branch on that result. Independent fork,
loop and interpreter observations follow their observed subjects when their
relationship is not established.
A pipeline into `su -c` belongs with shell pipelines. Unbound sudo and exec
text follows the indicated command or process subject; a Windows window-station name is a desktop
observation and does not indicate sudo or process creation.
Requests for a root shell belong with privilege elevation; they do not establish that elevation succeeds. Android permission grants, accessibility-setting references, device-password
changes and policy-manager imports retain those distinct subjects. Supplying
sudo's password on stdin belongs with privilege elevation.
RunAs option text and an unexecuted sudo argument list are launch
configuration; an isolated `runas` token is a command reference. A helper
import or an unbound UAC-policy profile does not establish elevation.
Classify `system` calls by their supported operation, not their API name:
shell command evaluation, direct program invocation and URL opening are
distinct. Unbound alias imports and calls follow their import and call subjects.
Downloaded input handed to an interpreter belongs in `process/deploy/interpreter-stdin/network`; decoded input belongs in `interpreter-stdin/decoded`, and other or unknown input in `interpreter-stdin/input`; command calls and unbound pipeline text follow their own subjects.
WMI process creation belongs with process creation; event subscriptions and
event-class references belong with WMI events. A hidden-window clue alongside
a WMI create call does not by itself bind that setting to the created process.
PowerShell jobs belong with task execution; decoded source piped to an
interpreter belongs with interpreter-stdin deployment. A command-line option
reference alone does not establish that the command ran.
Encoded ShellExecute spellings are open-handler observations until a call is
established. An explicit RunAs call is an elevation request; a hidden
show-command is a launch-visibility option.
Locality alone does not define a shell mechanism. Classify variable commands,
process replacement, discovery, and supporting call or import observations by
their subject. A generic member-call spelling remains syntax when its receiver
does not establish a more specific operation.
Temporary paths likewise do not define a shell mechanism: distinguish command
launch, process replacement, script sourcing, compilation and staged download
execution. Download and executable-permission clues alone do not prove a launch.
A webshell role does not define a shell mechanism. Classify request-fed
commands, discovery and compilation by behavior, and named-family strings
under their family. Compiling and running a program alone does not establish
that it binds a network socket.
Database configuration and stored code retain their database subjects;
database-hosted shell commands and COM operations follow the operation they
invoke. Co-occurring configuration and command text does not establish that
one caused the other.
Encoding alone is not a shell-creation mechanism. Classify decoded-source
handoffs, interpreter arguments, transport encoding and command fragments by
their respective behavior or evidence.
`process/config/target` records configured launch targets, including Python
process targets, Rust command paths and parsed shortcut targets. A target describes what activation would invoke; it does not
prove activation occurred. A raw executable path elsewhere in a shortcut does
not establish that path as its target.
`process/config/parent` groups parent-process launch attributes and related
configuration clues; querying an existing parent belongs with process identity
or information queries. `process/config/window` groups window visibility
settings and related launch-configuration evidence.
Window options, serialized names and unbound WMI startup clues are not process
creation by themselves. Keep hidden-launch evidence separate from those
configuration and profile observations; a generic hex literal does not name a
Windows flag without context.
Classify shortcut paths by their evidenced target or working-directory subject;
classify generic path references by the filesystem or URL subject they name.

Package-triggered execution is organized by the triggering phase: `execution/trigger/package/build` for build and setup machinery, `package/lifecycle` for installer and package-manager lifecycle hooks, and `package/import` for module-import triggers. A Python `.pth` startup hook belongs with Python startup persistence; a filename or hook declaration alone does not establish an executed payload.

`process/deploy/file-exec/open` records a downloaded executable staged and
handed to a file opener; it does not claim that the handler actually ran it.
A response written to a temporary script and passed to a process runner is
`process/deploy/file-exec/command`, including an attempted flow whose file
constructor may prevent execution. Calculator call-shaped text belongs with its observed command or application subject; a `Start-Job` call is background
work under `process/work/task`.
An HTML Help item naming a CHM is help navigation, not a process launch.
Lua `loadstring` creates a function; an invocation of that result supplies
execution evidence. Source identifiers and input-field text do not establish
that text came from a model or was passed to a process.
Go `exec.Command` constructs a command; starting or running it is a separate
operation. A JSON response and nearby command text do not by themselves identify
the response as model output or establish command execution.

URL opening records URL-handler calls and API references, including non-HTTP
schemes; an API reference alone proves neither dispatch nor a network connection.
For example, opening a `mailto:` URI
belongs in `communications/url/open`, while a generic `ShellExecuteW` import
belongs in `micro-behaviors/os/handler/open` because its target is unknown.
Handler dispatch can open a document or URL without establishing that a new
process was created; use process creation or replacement only when the
evidence supports that operation. In the registry, an
`OpenSubKey` reference belongs in `os/registry/open`; a query of a value goes
to `os/registry/read`. The 89-rule registry-access and shell-execution leaves
were reviewed with these neighboring operations: seven key-opening rules moved
to registry open, and five URL-dispatch rules moved to URL open, leaving 82 and
84 rules respectively in the original leaves.

`process/stdio/configure` groups child standard-stream and Windows standard-handle setup, including partial field and option evidence; stream reads, writes and relays retain their respective operations. Temporary-file writes and installer-hook clues follow their own subjects.

`process/create/subprocess/{configure,launch,capture}` distinguishes preparing
a child-process command, launching it without required output capture, and
launch interfaces that return or pipe its output. Launch APIs and API references
retain their operation; a configured command is not proof of launch. Explicit
output capture takes precedence over broad launch evidence.

`process/thread/{create,config,lifecycle,terminate,enumerate,priority,runtime}`
records one thread operation per child. Synchronization remains under
`process/sync`; scheduled work remains under `process/work`.

An explicit shell argument beats the wrapper. An API's optional features are no
evidence that this call uses them, and the launched executable does not change
the mechanism. Under `shell`, pick one command-form axis (interactive session,
command text, script file, pipeline).
Request-sourced commands require evidence connecting the input to the command;
a request-member reference alone is source syntax. Variable commands and known
input sources can be grouped by provenance, interpreter selection by its target,
and temporary staging by the observed staging and execution. Build markup,
argument snippets and unbound operation references belong with those observations,
not under process creation merely because they mention a command.
Pipeline syntax in documentation, standalone string literals or compiled data is a
command observation; an execution claim needs evidence of a launch site.
Constructing a command object or assigning its executable is setup, not a
process start.

`process/inject/remote-thread` records remote-thread APIs and their accompanying
remote-memory preparation. It does not require a DLL payload: allocation,
writing and `CreateRemoteThread` references fit; allocating and writing without
an execution-transfer API do not. `process/inject/dll` needs DLL-loading
evidence. Neither an API profile nor a JVM interface declaration proves that a
particular buffer became the thread's entry point. Imported method references
and declarations remain distinct evidence.
`process/inject/procfs` groups process-memory injection evidence specific to
procfs, including an injection identifier naming that mechanism; a path and
shellcode write support a stronger inference. `process/inject/reference` holds
injection-specific command and status clues whose mechanism is unspecified.
These references do not establish that injection occurred.

## Attacker behaviors: `objectives/`

**Admission comes before placement.** Required evidence must support the attack
claim — a target, deception, unauthorized action or attack-specific
relationship — not just the mechanics. Static inference suffices. Ordinary
download-and-run, secret access or service registration does not qualify, nor
do reputation, optional clues or two unrelated APIs. State the admitting fact
in the description.

Level 2 names the behavior; level 3, the mechanism, target or source that
distinguishes it.

| Objective | Level 2 | Admission and nearest neighbor |
|---|---|---|
| `anti-analysis` | `debugger-detect`, `sandbox-detect`, `vm-detect`, `emulator-detect`, `tool-detect`, `environment-detect`, `fingerprinting`, `timing`, `geofencing`, `anti-tampering`, `self-modify`, `self-terminate`, `process-tree`, `browser-detect` | Probing, gating or interfering with analysis environments; the required probe picks the child (a VM artifact is not a sandbox artifact). Ordinary environment queries and sleeps stay capabilities. |
| `anti-static` | `obfuscation/<concealment>`, `pack/<unpacking-mechanism>`, `polyglot/<interpretation-conflict>` | Obstructing static recovery of code or data (disassembly, decompilation, string extraction). Identifier patterns deliberately chosen to obscure names belong under `obfuscation/name-mangling`; ordinary variable assignments stay in `data`. Encoding, compression, entropy or section shape alone is not concealment; a named packer is `well-known/`; stock UPX output is notable layout, not hostile. |
| `collection` | `keylog`, `clipboard`, `screenshot`, `audio`, `camera`, `touch`, `messaging`, `email`, `network`, `app-data`, `database`, `file-targeting`, `file-copy`, `archive`, `monitor`, `activity`, `multi-source` | Targeted acquisition or staging **without** a required send. Credentials → `credential-access`; reconnaissance → `discovery`; source plus send → `exfiltration`. `network` means captured traffic. |
| `credential-access` | By source: `browser`, `cloud`, `credential-manager`, `keychain`, `env`, `files`, `ssh`, `wallet`, `email`, `messaging`, `dev-tools`, `wifi`, `registry`, `memory`; by acquisition: `capture`, `cracking`, `phishing`, `theft`, `validation` | Acquiring authentication material or a targeted secret store, by the [credential-source order](#objective-boundaries). Source-specific distinctions such as provider, smartcard, system and store live beneath their store family; validation and session reuse live beneath `validation`. |
| `discovery` | `account`, `host`, `system`, `network`, `process`, `cloud` | A reconnaissance survey, by surveyed resource: `host` = installed software, security products, browsers; `system` = machine, hardware, OS; `process` = running processes; `network` = interfaces, peers, probes, scans; `account` = principals; `cloud` = provider resources. One generic query stays a capability. |
| `command-and-control` | `channel/<transport>`, `beacon`, `remote-command/<dispatch>`, `backdoor/<access-surface>`, `reverse-shell/<io-coupling>`, `botnet`, `infrastructure` | Attacker control, tasking, access or communication. Payload delivery is [execution](#payload-activation-and-staging); a protocol name is not C2. |
| `execution` | `payload/<sink>`, `staging/<operation>`, `exploit`, `interpreter`, `lolbin`, `lure`, `trigger`, `database`, `activex`, `automation`, `compile`, `lnk`, `wmi`, `autoinstall` | Unwanted execution through an exploit, deceptive invocation, trusted execution surface or admitted payload chain. Generic execution APIs stay in `process`. `database` is database-hosted execution (CLR procedures, `xp_cmdshell`, OLE Automation). |
| `exfiltration` | `stealer/<item>`; transport-only: `http`, `dns`, `ftp`, `cloud`, `messaging`, `llm`, `oob`, `side-channel` | Unauthorized transfer. An acquisition-to-send chain is classified by its stolen item and beats transport; a transport child needs an established theft claim whose item kind is not established. A POST, an endpoint or ordinary model inference is not exfiltration. Header, query and body are distinct HTTP carriers. |
| `evasion` | `anti-av/<control>`, `security-bypass/<control>`, `masquerade/<deception>`, `decoy`, `file-hiding`, `kernel-hide`, `indicator-removal/<record>`, `self-delete`, `process/<concealment>`, `fileless`, `hijack-execution-flow`, `hosts-file`, `quarantine-removal`, `tcc-manipulation`, `file-unlock` | Hiding activity from users, admins or deployed security products, or bypassing their controls. |
| `impact` | `destroy/<resource>`, `wipe`, `ransom`, `dos`, `degrade/<target>`, `infect/<host-artifact>`, `crypto-manipulation`, `cryptojacking`, `deface`, `services`, `system`, `ui`, `spam` | Destruction, disruption, extortion, unauthorized modification or resource abuse. Ordinary deletion or encryption is neutral; spam needs unsolicited-message abuse, not volume. |
| `lateral-movement` | `exploit/<remote-surface>`, `brute-force/<service>`, `pass-the-hash`, `smb/<mechanism>`, `ssh`, `worm`, `usb-worm`, `social-engineering` | Reaching or spreading to **another** system. A mechanism-specific exploit or credential reuse beats a generic protocol home. Scanning is discovery; local cracking is `credential-access/cracking`; infecting local files is `impact/infect`. Neutral remote administration, WMI and process creation stay under `micro-behaviors`; propagation requires evidence of reaching another system. |
| `persistence` | `login/<surface>`, `system/<surface>`, `firmware/<surface>` | Durable, unwanted reactivation, [by trigger](#persistence-follows-the-trigger). |
| `privilege-escalation` | `exploit/<boundary>`, `elevation-control/<bypass>`, `token-manipulation`, `hijack-execution-flow/<surface>`, `modify-service`, `kernel-modules`, `install-certificate`, `process-injection` | A required crossing to greater authority. A privileged API, requested permission, `sudo` text or injection alone is not one. |
| `supply-chain` | `impersonation/<deception>`, `trojanized/<trusted-input>`, `hidden-payload/<inspection-evasion>`, `security-hold` | Abuse of component selection, distribution, or build and update trust; [package scope is not enough](#supply-chain-trust). `security-hold` is the explicit classification-policy exception below. |


Firewall degradation separates `disable`, `rules`, `policy`, and `service` by
the affected control. API endpoints and ordinary policy fields are capability
or metadata evidence until a harmful action is supported.

### Objective boundaries

- **Analysis environment.** Classify an analysis-directed hostname check under
  `sandbox-detect/hostname`, a sandbox score or its exit gate under
  `sandbox-detect/score`, and a broader execution gate under
  `sandbox-detect/enforcement`. A bare routine name, diagnostic message or
  ordinary conditional is a reference to describe under metadata or a generic
  capability; it does not establish that an evasion check ran. When an export
  of a specific resource is required, use the corresponding exfiltration
  objective, with the analysis check as supporting evidence.
- **Agent approval.** Place attempts to bypass an agent's authorization,
  consent or approval gates under `evasion/security-bypass/llm/approval`.
  General instruction-priority overrides remain in `llm/override`; a user's
  actual authorization and isolated, user-directed harness configuration are
  not themselves evidence of a bypass.
- **Exported system information.** Put exported account inventories under
  `exfiltration/stealer/system-info/account` and host or user identity
  profiles under `system-info/identity`. Exported online-account identity
  information without a required host profile belongs under
  `stealer/account-identity`. An account database such as
  `/etc/passwd` is not by itself a password or credential store.
- **Credential source.** Classify deceptive capture as `phishing`, hash or
  password recovery as `cracking`, live interception as `capture`. For stored
  secrets, use the *immediate* store — OS keychain, credential manager,
  environment, cloud secret service — else the required application or
  key-format store (browser, SSH, wallet), else `files` for generic extraction.
  Certificate/private-key store export is `keychain` (including Windows
  CAPI/CNG stores); Credential Manager password-blob access is
  `credential-manager`.
  Process-memory extraction is `memory`; registry keys and hives, including an
  offline SAM, are `registry`. An application store beats its file or registry
  container; the final source beats any key used to unlock it.
- **Export follows the item.** Credential acquisition keeps its store-based
  classification above. An export uses the [stolen-item taxonomy](#collection-credentials-and-theft):
  a private key from an environment variable, file or keychain has the same
  `stealer/credential/value/key` home. Its acquisition store remains referenced
  evidence. Never infer an item subtype from the store alone.
- **Phishing pages and their hand-offs.** Under `credential-access/phishing`,
  place a page, attachment or app by what *it* does to the visitor:
  `landing` solicits or collects credentials or contact data (a login form, a
  password prompt, a harvest POST, the branding and bot screening that dress
  such a page); `redirect` only forwards the visitor to the next hop (instant
  refreshes, traffic brokers, hosting-platform hops, OAuth error bounces,
  decrypted next-hop URLs); `login-redirect` is the narrower kit hand-off stub
  that forwards to a tokenized login URL; `mfa` targets one-time codes and MFA
  secrets, including extensions that read them from pages; `webview-wrapper`
  is an app that presents phishing pages, remote or bundled, in an embedded web
  view; `link-deception` disguises a link's real target. Precedence: collecting
  beats forwarding (a page that posts the password and then redirects is
  `landing`), and a tokenized-login forward is `login-redirect`, not `redirect`.
  An MFA-code harvest is `mfa` even when it also takes the password. Example:
  a blank attachment that refreshes to `anexodocumentos` is `redirect`; the
  login page it lands on is `landing`. Counterexample: a credential-relaying
  reverse proxy is `mfa-relay`, not `landing`.
- **Activation before delivery detail.** An admitted acquisition- or
  staging-to-activation chain is placed by its sink; language, transport,
  encryption and carrier are supporting facts.
- **Control before payload.** A reusable operator request-to-command surface is
  C2; activating one acquired payload is a payload chain.
- **Mechanism before intent.** Neutral hooking and injection stay in
  `micro-behaviors/process/{hook,inject}`; evasion, credential or escalation
  composites add their own result. Common use is not stealth.
- **Stopping defenders is impact; blinding them is evasion.** Killing EDR or
  flushing firewall rules → `impact/degrade`; AMSI, ETW, indirect syscalls or
  Defender exclusions → `evasion/anti-av`.
- **Narrow effects beat broad.** Secure erasure → `wipe`; extortion → `ransom`;
  exhaustion → `dos`; other destructive deletion → `destroy`; code inserted into
  a host file → `infect`.
- **Mount-derived device wipes.** Put a destructive disk-write objective under
  `impact/wipe/disk/mount-derived-device` only when source evidence links a
  device selected from `/proc/mounts` or `findmnt` to the write target. Mount
  enumeration, a `/dev/` string, or `dd` with an unrelated output does not
  establish that link; keep those observations in their behavior homes.
- **Several outcomes:** place by the distinguishing result — source plus send →
  exfiltration; cross-host installation → lateral movement; higher-authority
  execution → privilege escalation; durable reactivation → persistence; else
  payload activation. Unrelated outcomes are separate composites.

Allocator-log exploitation belongs in
`privilege-escalation/exploit/allocator-logging` when required evidence targets
a privileged file or embeds a privileged command in allocator settings. A
`MallocLogFile` assignment targeting `/etc/crontab`, a root sudoers cron command
embedded in `MallocStackLoggingDirectory`, and their bound handoff to `rsh`
belong here. Ordinary allocator logging configuration does not: it stays a
neutral runtime configuration observation. The allocator mechanism owns this
exploit, rather than the cron carrier or the generic `vulnerabilities` catalog.
The handoff rule must bind the malicious settings to the launched process;
unrelated logging settings beside an `rsh` call do not establish that link.

A crack attribution tuple belongs with licensing-bypass evidence under
`evasion/security-bypass/licensing`; it does not identify a recognized software
family. The tuple requiring `PaddleAPICheck`, `paddle`, and `K'ed by TNT` in one
constant span fits here. A bare license-check API identifier does not establish
a bypass or product identity.

Default-credential spraying requires repeated authentication against the
loop-selected remote targets. An unrelated loop, or a loop that repeatedly
connects to one fixed host, does not establish a multi-host spray. Bind the
session receiving the default credentials to the selected target. Likewise,
commented PE editing examples cannot supply an active shellcode assignment;
the Go shellcode-insertion role requires a parsed assignment.

### Command and control

| Child | Admission | Not this |
|---|---|---|
| `reverse-shell` | An **outbound** connection coupled to a shell's I/O. | Socket and shell without that coupling; a listener (`backdoor/bind-shell`). |
| `backdoor/bind-shell` | A listener handing an accepted client a shell. | A handler taking independent tasks (`backdoor/dispatch`, `remote-command`). |
| `backdoor/webshell` | A server page or hook that executes operator requests; children name what the request drives (`request/<sink>`, `intercept/<hook>`) or the shell's role (`relay`, `stager`, `upload`, `recon`, `file-manager`, `auth`). | A handler that only reads request headers. |
| `backdoor/*` | Other unauthorized access: auth bypass, RAT command sets, implants. | Generic dispatch; carriers (`binary`, `script`, `native-source`). |
| `remote-command` | Received tasks tied to execution; a response written back strengthens it. | Socket plus execution, or output to a socket, without received tasks. One HTTP request is not polling. |
| `beacon` | Repeated check-in or heartbeat. | Ordinary timers and telemetry. |
| `botnet` | Fleet membership or distributed tasking. | A DDoS action or device platform alone. |
| `channel/<transport>` | A transport shown to carry attacker control. | Generic transport APIs. |
| `channel/dns` | DNS tasking or check-in, including generated-domain rendezvous. | A DoH endpoint, domain generation or lookup without a control role (`micro-behaviors/communications/dns`). |
| `infrastructure` | Endpoints or rendezvous with a demonstrated C2 role. | Ordinary hosting and chosen labels. |

Webshell request handlers are grouped by the input when it is known: `query`,
`form`, `header`, `cookie`, and `body`. Use `parameter` when request parameters
are known but their transport is not, and `command` for broader command sinks.

Within `botnet/iot`, `flood` groups distributed attack tasking, `propagation`
groups deployment and reinfection, and `control` groups other fleet control
or beaconing. A recognized family-specific marker belongs in `well-known/`.

**Reverse-shell level 3: the first required relay mechanism wins.** `dev-tcp`
(shell pseudo-device) → `netcat` (netcat in connect mode owns the relay) →
`pty` → `fd-redirect` (socket as the shell's inherited descriptors) →
`stream-bridge` (explicit copying between socket and child streams, including
`telnet | sh | telnet` and FIFO cycles on one path). Encoding, syscall and
language are not mechanisms; `encoded`, `socket-exec`, `stdio`, `syscall` and
`dup` are retired.

**Webshell precedence:** request input loading compiled code into the server
(`defineClass`, `Assembly.Load`, deserialization, JNDI) → `code-load` >
in-process evaluation (eval, EL, ScriptEngine, XSLT) → `eval` > an OS command →
`command`. Request hooks: `handler-patch` > `container-registration` >
`module`. Tunnels: SOCKS framing → `channel/tunnel/socks` > HTTP-carried socket
relay → `http` > generic proxy chains → `proxy`.

`ui/help/{command,interaction,account,message,navigation}` groups help
observations by what they convey. The `ui/help/` parent remains their recursive
union for existing consumers.

`communications/http/curl/{command,body,binding}` separates command-line
invocation, request bodies and library bindings. The `curl/` parent remains
the recursive union for consumers that need all three.

`fs/path/temp` records temporary directory and helper references;
`fs/path/temporary-artifact` records paths naming particular temporary files.
A consumer that intends both must reference both directories.

Document interpreter execution is organized by surface under
`execution/interpreter/document/{addin,command,macro,pdf,xml}`. An Office
external-link class, URL, or embedded document by itself belongs with its
observed metadata; it does not establish payload execution.

### Payload activation and staging

A payload chain needs **acquisition or staging and likely activation**, plus
admission. A direct link is strong evidence, but sufficiently specific,
coherent operations can support the inference without proven data flow.
Admitted chains go in `execution/payload/<sink>`; the same chain in an ordinary
updater goes in `micro-behaviors/process/deploy/<sink>`. Choose **one** sink;
reference source, concealment and trigger facts, and describe uncertainty.
These include probable droppers: coherent acquisition and activation clues can
indicate delivery of an additional payload without proving a completed transfer
or execution. MBC's Install Additional Program (B0023) covers installing a
second program, including dropper cases; a download-and-launch chain alone
does not necessarily establish installation. Ingress Tool Transfer (E1105)
describes acquisition separately from activation.

Supporting staging clues that specifically indicate HTTP acquisition belong in
`execution/staging/http`, including clues combined with later local
storage or launch. Transfer chains that allow several protocols belong in
`execution/staging/transfer`; generic acquisition and storage clues remain
in their broader subjects. Describe co-occurring operations without
claiming they act on the same payload unless the matcher connects them.

| Sink | Required activation |
|---|---|
| `process-inject` | Execution moved into another process (`hollow`, `remote-thread`, `thread-hijack`). |
| `image-map` | A native image mapped for execution in this process. |
| `module-load` | Staged code loaded by a module or assembly loader (`Assembly.Load`, `AppDomain.AssemblyResolve`, `Module._compile`, dynamic `require`, WASM instantiation of staged bytes). |
| `memory-branch` | Staged executable bytes copied into executable memory and activated by a direct branch, callback, or local thread, without requiring a module loader or a launched file. |
| `script-eval` | Staged source evaluated by an interpreter (`eval`, `new Function`, `iex`, or explicit inline evaluation such as `node -e`). The child-process launch is supporting evidence; no staged executable file is implied. |
| `interpreter-stdin` | Staged source piped to a new interpreter. |
| `file-exec` | A staged file launched via `command` (a shell parses the launch), `spawn` (a process API starts a child), `replace` (the current process image is replaced, such as by `execve`) or `installer` (an installer transaction such as `msiexec`). |

`module-load/{network,embedded,transformed,input}` partitions module activation
by indicated source: network retrieval, embedded resource, otherwise decoded
or decrypted input, otherwise an input whose origin remains unknown. Choose the
most specific supported source, with network taking precedence over an embedded
resource or transformation.

`memory-branch/shellcode` groups rules that establish local shellcode
activation. Shellcode bytes, API names, or loader markers without an activation
path belong in a supporting profile instead.

Exploit shellcode is subdivided by the intended payload or technique:
`browser` contains browser exploit carriers and their spray/decoder behavior;
`command-and-privilege` contains shell and privilege payloads built from
syscall-level shellcode; `parasite` is reserved for code-replacement and
jump-back stubs; `windows-loader` covers shellcode that resolves APIs or maps a
PE image; `wasm` covers native payload clues embedded in WebAssembly; and
`source-construction` covers code that builds shellcode for an exploit. Generic
byte strings and instruction fragments without a supported payload claim
belong in binary instruction metadata.

File profiles group related observations under `profile/script`, `profile/com`,
and `profile/tunnel`; their children describe the relevant operation or
subject instead of adding more unrelated leaves at the profile root.
An installation profile may describe neutral package properties or unresolved
co-occurrence. A rule that says an installer creates a directory, writes state,
downloads a file, starts a helper, or opens an install session belongs under
the corresponding `micro-behaviors` operation, even when the matcher sees only
an API name or a partial indicator. Keep the profile only when the evidence
does not support a likely operation.

Within network evaluation, `package-hook` groups package initialization or
installation contexts, and `in-process` covers other direct evaluation.

`script-eval/{blockchain,network,transformed,input}` groups a payload evaluator
by its indicated source: blockchain-derived code or destinations, another
network response, otherwise decoded or decrypted source, otherwise an input
whose origin remains unknown. A blockchain source takes precedence over a
general network source, and a network source over a transformation, when the
evidence supports it. Fetch/eval co-occurrence and embedded command text follow the most likely
interpreter or network behavior; descriptions must say when the connection is
inferred rather than established.
Within `network`, `decoded` requires reconstructed fetched code; otherwise
`constructed` requires a function-constructor sink. The remaining sinks are
`child` for a separate interpreter command, `script-element` for browser script
insertion, `vm` for evaluation in a VM execution context, and `in-process` for
other evaluation in the current interpreter. A VM context does not by itself
establish a security boundary. A decoded
URL or obfuscated evaluator alone does not establish decoded response code.

Within `transformed`, classify the activation mechanism as `shell` for shell
command execution, `child` for a separately launched interpreter, `constructed`
for a Function or ScriptBlock constructor, and `direct` for the remaining
evaluation sinks, in that order. Classify uncertain construction or unbound
clues by the likely capability or objective when one is supported, and describe
the clues without asserting a completed chain.

`file-exec` is split by launch mechanism: `command/*` (a shell or script host parses the launch), `spawn/*` (a process API launches a child; `native` for compiled images, `runtime` for language runtimes, `archive` for archive-related launches, `sfx` for self-extracting archive launches and `handler` for shell-associated file launches), `download/*` (direct network acquisition tied to likely activation; `native` for compiled images, `runtime` for source or bytecode handed to a language runtime, and `script-host` for a script handed to WSH, PowerShell or another host), `replace` (a staged file replaces the current process image), `detached` (hidden or background launch), `installer/*` (an installer transaction; `package` rules read the installer file, `script-package` rules concern script payloads in that file, and `invocation` rules read whatever launches it) and `shellcode`. Each matcher and description must retain the launch mechanism. `command/chmod` groups shell payload chains that change executable permissions before launch; `command/fetch` covers acquisition-and-launch chains without that requirement. `command/browser-control` groups browser-hosted COM scripts that save and launch fetched files; `command/script-host-download` covers other script-host download-and-launch chains. `command/browser-cache` covers script launches involving browser cache recovery; `command/browser-profile` covers profile-entry copying and execution when no cache path is established.

Keep network acquisition and activation in the same behavior or objective when their combination suggests that chain; source-language or vendor names alone do not define a child category. Do not demand proof that a downloaded object flows to a process before classifying the likely operation. Describe references and configuration as such rather than asserting an observed execution.

`spawn/decrypted` groups admitted chains that launch after decryption when the
executable type is not established; use a more specific spawn target when the
matcher identifies it.

`image-map` and `interpreter-stdin` are admitted sinks: they distinguish native
image activation from a new interpreter reading staged source. A mapped image
or stream reference alone does not establish activation or a linked payload.

Process observations and co-occurrences belong with their most likely
operation or objective. A specific call or API reference that indicates
evaluation, launch, or another process operation belongs in its
`micro-behaviors` subject even when the payload source or full chain is unclear;
use severity and confidence to show that uncertainty. Truly neutral API names,
imports, and configuration observations follow their symbol or configuration subject. An import or generic symbol mention alone is
not evidence that the operation was called.

`exfiltration/stealer/source-code` groups exfiltration of source and revision
patches. `exfiltration/stealer/system-info/host-user` groups findings that
combine host and user identity; broader fingerprints and single-subject
findings remain in their respective categories.

Host-profile discovery remains under `discovery/host/fingerprint` when no
transfer is established. Package format fallback and command-entrypoint
impersonation remain distinct under `supply-chain/impersonation/registry`.

Base64 API and source-call decoding remains in `data/decode/base64`;
command-line decoding belongs in `data/decode/command`. The explicit
`base64-api-or-command` union preserves consumers that accept either mechanism.

Token-format evidence is divided by subject into `data/format/{discord-token,
github-token,registry-token}`; generic credential formats remain in
`data/format/credentials`. User-level systemd persistence belongs in
`persistence/system/service/systemd-user`; `systemd` retains system-wide
and unscoped service evidence.

The former `metadata/build/toolchain` catch-all is retired: compiler clues,
build targets, command lookup, and source-generation operations use their
respective subjects. A named tool reference does not prove tool execution.

`metadata/build/architecture` records build-architecture label text; the
labels alone do not establish the architecture of the analyzed file.

`metadata/build/makefile-shape` records Makefile targets and recipe layout;
an empty target set alone does not establish a malicious build bypass.

`metadata/build/msbuild` groups MSBuild project, task and lifecycle
declarations. Receiving a project path does not establish that a task edits it.

`micro-behaviors/fs/read/file/credential` groups reads of credential and
package-authentication files; path references without a read stay with their
path subject. Ordinary registry publishing or an API-key name alone does not
establish credential theft.

Host-fingerprint and identity exfiltration belong under their respective
`exfiltration/stealer/system-info` subjects. Install-hook context remains a
condition, not the organizing subject. DNS commands and callback host
references alone do not establish exfiltration.

Unresolved API and memory co-occurrences follow their likely behavior, with
descriptions that preserve their uncertainty. Injection-specific references
and partial operation evidence belong under
`micro-behaviors/process/inject`, even without a complete transfer and
activation path; descriptions must distinguish references from execution.
Runtime process-memory API clues belong under `inject/runtime/memory`, hook
clues under `inject/hook`, and ptrace injection clues under `inject/procfs`;
ptrace attachment constants alone belong under `process/attach/debugger`. Confirmed execution in another process belongs under
`objectives/execution/payload/process-inject`; local executable-memory
activation belongs under `objectives/execution/payload/memory-branch`.

Co-occurring network and process evidence follows the most likely supported
communication or execution behavior and states the observed relationship. For
example, an HTTP reference near an execution call does not establish that the
downloaded content was executed; a bound download-and-launch belongs with the
supported execution behavior. The legacy `network-context` branch is retired:
place its rules by the supported communication, process, execution,
exfiltration, or named-tool subject, and describe unbound observations as such.

`communications/rpc` records RPC protocol fields and API references;
`communications/blockchain/wallet` records wallet method names and their co-occurrence. Such names
do not by themselves establish a request, an account access or a signing flow.
Encoding API and syntax references belong with the evidenced codec, operation,
format, or literal; an API name alone does not establish a completed transform.

MCP protocol names, declared agent settings, and tool names or decorators
follow their protocol, configuration, or neutral naming subjects. A protocol string, tool name
or configuration entry does not establish that a client sent a request or a
server handled it. `communications/mcp/server` requires an actual server-side
operation, and writing client configuration belongs with filesystem writes.
Do not suppress a finding merely because an MCP-related marker is present;
require a specific benign context relevant to the finding.

Static references to system management helpers and configuration follow the
indicated operation, named tool, or neutral configuration subject. A helper name or API reference
alone does not establish that the operation ran or that another command is benign.

COM follows the same distinction. Actual object creation and method calls
belong to their COM operation or the function they perform. Class IDs, ProgIDs, interface and API names, encoded names, registration
fields, and shortcut API references follow the named component or the
operation they most likely indicate.
An identifier or imported API does not establish activation, invocation, or
that the named software is present. A registration field alone does not prove
that it was written; an encoded name does not establish its eventual use.

Native executable request profiles, WebClient retrieval, package-hook requests and named account endpoints follow their respective subjects. HTTP request clients retain generic client calls; endpoint, method, executable-download and package-specific clues follow their respective request subjects.

Installer metadata follows its subject under `metadata/installer`, including layout, configuration, package properties, bundle contents and resources. Move observations that indicate a likely operation to its behavior or objective. Self-extractor and cabinet carrier text and related carrier profiles belong with installer archive profiles; executable setup directives belong with installer process configuration. Installer plugin references and related co-occurrence profiles belong with installer plugins. Generic uninstaller names retain their lifecycle subject.

Legacy `metadata/file/profile/staging` observations should move to the most
specific supported operation or likely deployment objective. Names and
configuration fields without behavioral implications follow their own subject.
High entropy, an unsigned file, an unknown installer version marker or a zero
checksum alone do not establish encryption, tampering or payload execution.

The legacy firmware profile is retired. Firmware observations use their
format, operation, or likely objective; short VXWS text clues are firmware
format context, and the SWXV code bytes are a section-byte observation. None
alone identifies a platform or establishes a payload. A firmware-looking path alone does not establish that firmware was
downloaded, updated or executed; retain an isolated path with its path subject.
Executable and spawn configuration fields belong with process configuration;
temporary path fields belong with their path subject. Those fields alone do
not establish that a process was launched or a file was downloaded.

URL and download-option clues follow the indicated communication subject;
unresolved shell references follow the likely shell operation and retain their
uncertainty in the description. A
variable command invocation in a shell belongs under
`process/create/shell/variable-command`, even when its reconstructed contents
are unknown. Named commands belong with the operation or target they indicate.

Financial terms alone do not establish a lure, theft or a malware family.

`metadata/package/files/android-assets` records Android asset and resource
member facts. Combine those facts with APIs and permissions under the likely
operation or objective when the evidence supports one; an asset name alone
does not establish that a payload was staged or executed.

`metadata/package/files/msi` separates installer identity, content and
configuration. MSI command and privilege-request clues belong with the
corresponding behavior. Product names, publisher fields and file size alone
are not proof that an installer is fabricated or malicious.

Evaluation references are partial interpreter behavior; use the likely
`process/interpreter/eval` mechanism without claiming that a call occurred.
Source showing an evaluator applied to file or URI content belongs under
`micro-behaviors/process/interpreter/eval/source`; its description should
identify the observed source without claiming the code ran. Evaluation of
decoder results belongs under `process/interpreter/eval/decoded`, distinct from
unqualified direct evaluation. Unsafe YAML
loading near an HTTP request belongs under `micro-behaviors/data/parse/yaml`;
proximity alone does not establish that the response was parsed.

**Describe the likely chain.** A download, URL, encoded blob, execution API,
installer identity or loader-like name alone is not a payload chain. A direct
link between a payload and its sink is strong evidence; a coherent combination
of operations can also indicate a likely chain without proving data flow.
Describe the evidence and its uncertainty rather than asserting a connection
the rule does not establish. Script, HTA, WSH, MSI and package formats are
carriers, not sinks. `regsvr32 /i:` with `scrobj` is
`execution/lolbin/regsvr32`. An auto-open document trigger with a process call
but no payload evidence is `execution/trigger`.

Within `execution/payload/file-exec/command`, `interpreter-stage` groups
batch chains that prepare and launch an interpreter stage; `script-host-interpreter`
groups script-host chains that invoke an interpreter stage, and
`script-host-wmi` groups script-host chains that launch via WMI. These are
execution mechanisms, not evidence that the carrier alone is malicious.

`anti-static/obfuscation/string/name-split` groups evidence of concealing
program, switch or member names by splitting their spellings. Generic
fragmentation and reconstruction remain in their respective subjects.

`execution/payload/script-eval/network/stream` groups evaluation associated
with streamed or event-delivered network content. Other in-process network
evaluation remains under `network/in-process`; streaming is a mechanism,
not proof that every matched event flows into the evaluator.

Combined network and process evidence belongs with its likely operation or
objective, such as staged execution, remote control or scheduling. Describe
partial and co-occurring evidence as such; a path need not prove data flow.

`anti-static/obfuscation/encoding/xor` separates concealed strings, paths,
execution and otherwise unspecified XOR concealment. Generic XOR operations and
name references belong in `micro-behaviors/data/bitwise/xor` or
`data/encoding/xor`; XOR alone does not establish concealment.

`micro-behaviors/communications/http/download/cli` groups command-line
download evidence by web cmdlet, curl/wget, other utilities, and combinations
of tools. The parent includes all children for recursive references.

`metadata/package/config` separates tooling, runtime, manifest, reader,
format and exclusion observations by their configuration subject.

`micro-behaviors/os/application/update` groups evidence of application update
operations or coherent update mechanisms. Update endpoints, command text and
API references do not alone establish maliciousness or an observed replacement.

`metadata/archive/profile/{executable,script,document}` groups archive-level
co-occurrence of member and content observations by subject. Archive scope
does not establish that independently matched facts belong to the same member.

`well-known/lib/development/{parsing,babel-toolchain,type-definitions}`
groups parser libraries, Babel packages, and TypeScript definition packages
by their roles; individual product identities remain below each group.

`micro-behaviors/metaprogramming/generation/build` covers build-system
orchestration such as cargo, make and project builds. Per-source compilation
and runtime compilation stay under `generation/compile`.

`objectives/command-and-control/backdoor/construction` covers probable
construction of backdoor or bot implants; generic build and template markers
do not establish that objective on their own.

`anti-static/obfuscation/payload/builder` groups probable construction of
concealed executable payloads. A generic compiler, executable write, random
buffer or tool name alone does not establish that intent.

`anti-static/obfuscation/payload/browser-download` groups likely concealed
browser delivery of reconstructed encoded payloads. Generic file exports,
independent Blob and click clues, and download names alone belong with their
observed behavior or supporting profiles.

**Staging without activation** needs executable-payload preparation plus
admission. Partition by operation, in precedence order: `reconstruct`
(synthesis or decoding) → `extract` (an embedded or container member) →
`acquire` (external fetch) → `store` (placement), as
`execution/staging/<operation>`. Shell-mediated payload execution after a
network fetch can be grouped in `execution/payload/file-exec/command/fetch`;
fetch, decode, file write and launch together can support that likely objective
without proving the data flow between them.
`command/hidden-file` groups chains involving a hidden staged file or path,
including partial evidence of such a chain; `command/hidden-window` groups
command-mediated staging or execution with a hidden or minimized window.
`command/archive` groups chains involving archive extraction and launch.
The remaining shell execution chains need the same neighborhood review.
`execution/payload/file-exec/download/{native,runtime,script-host}` groups
network acquisition tied to likely activation, classified by the acquired
payload's activation target. `spawn/hidden-window` groups chains that explicitly hide
the launched window; other runtime launch chains remain in `spawn/runtime`
pending the same review. The carrier (archive, encrypted blob, stub,
runtime) is evidence, not the partition. Ordinary extraction stays
`data/archive/extract` or `data/embedded`; encoded bytes alone are
`metadata/file/encoding`.

### Collection, credentials and theft

Classify **the item that leaves**, using the acquisition and send evidence.

`exfiltration/stealer/<item>` answers one question — **what data does this
matcher require to be exported?** Storage location, application, language,
transport and activation trigger remain referenced facts. Every theft rule
requires acquisition/content evidence and a send; a source-only selector,
payload field, route literal or imported client belongs in its own observation
home. A bounded co-occurrence can remain suspicious when described as such;
it must not claim a data binding the matcher does not establish.
Security-hunting query text describes the events it searches for; it does not
establish that the file itself performs the transfer being investigated.

| Required exported item | Home beneath `stealer` |
|---|---|
| Authentication material whose exported form is unknown, or alternatives spanning values and whole authentication records | `credential` |
| Selected secret values whose kind is unknown, or alternatives spanning secret kinds | `credential/value` |
| A selected password, protected password/verifier field or pre-shared authentication password | `credential/value/password` |
| A selected bearer, API or OAuth token | `credential/value/token` |
| A selected login-session token, session cookie or authentication session | `credential/value/session` |
| A selected cryptographic secret/private key | `credential/value/key` |
| A mnemonic, seed phrase or recovery secret | `credential/value/recovery-secret` |
| A stored authentication database, cache, keyring or credential-record set exported as a record/container | `credential/record` |
| Browser login records or stores | `credential/browser-record` |
| Keychain or keyring credential containers | `credential/keyring-record` |
| Wallet keyring containers | `credential/wallet-record` |
| Secret-bearing files selected by credential-specific paths, without a narrower required secret value or record type | `credential/file` |
| Configuration files or settings, without a required extracted secret type | `configuration` |
| A broad process-environment snapshot, or environment values without a required credential type | `configuration/environment` |
| Application storage/profile state with its content type left open | `application-state` |
| Chat-application session or local state without a required selected secret | `application-state/chat` |
| Browser state with alternatives spanning cookie and login stores or browsing records | `application-state/browser-state` |
| Cookie state, without assuming every cookie authenticates a session | `application-state/cookie` |
| Browsing/history/activity records | `activity` |
| Captured input values, keystroke/touch records or clipboard content without narrower semantic content | `input` |
| Media content: static images, sound or ordered visual streams, with modality in the trait ID and description | `media` |
| Payment-card and associated billing data | `financial/payment-card` |
| Messages, mailboxes, SMS | `message` |
| A database dump or row set without a narrower required semantic item | `database` |
| Online-account identity information without a required host profile | `account-identity` |
| Captured web-page text or markup | `page-content` |
| Files whose contents have no narrower required item class | `file` |
| Files collected from a directory tree and sent outward | `directory-tree` |
| Directory listings or file-path inventories sent outward | `directory-listing` |
| Documents selected for export | `document` |
| Capture-the-flag challenge material selected for export | `challenge-flag` |
| Command output without a narrower required information subject | `command-output` |
| Account inventories and account-database contents, without an established secret type | `system-info/account` |
| The host name as the required exported identifier | `system-info/hostname` |
| Host report: identifiers / OS and runtime / installed software / running processes / network inventory | `system-info/{identity,platform,software,process,network}` |
| Host report spanning or leaving open several of those | `system-info/profile` |
| Workspace/repository metadata report | `system-info/workspace-profile` |
| Two or more independent item families, **each required** | `multi-item` |
| Theft established, but alternatives or untyped content proves no narrower item family | `stealer` itself |

GitHub Actions token-transfer clues use `credential/value/ci-token`;
other CI secret-transfer patterns use `credential/value/ci`. Local collection
or staging without an established transfer belongs in credential access, and
ordinary HTTP command syntax stays in micro-behaviors. A malicious install-hook
chain may retain its installation-trust context under supply-chain.

**Precedence and counterexamples.** A selected wallet private key is
`credential/value/key` regardless of acquisition store. A complete `.env` file is
configuration; a selected private-key field loaded from that file is a key.
A whole environment dump stays `configuration/environment`; possible tokens
inside it do not create a token-export predicate. A browser cookie is cookie
state unless the required evidence identifies an authentication token. A
password database exported as a whole is a credential record; a selected
password value is a password. These classify the object the matcher actually
selects, rather than every possible constituent of a container.

`multi-item` counts required exported item families, not acquisition stores or
traits. A wallet key plus an SSH key is still credential material; desktop and
camera video are both video. An `any:` over selected passwords and tokens stays at
`credential/value`. A screenshot import beside a credential exporter does not prove
a second exported item. When alternatives share only the theft objective,
retain the rule at the meaningful `stealer` ancestor. Broad rules must never
be duplicated across descendants.

`stealer/media` records exported sound, static images and visual streams in
one leaf. Distinct modalities remain explicit in each trait ID and description;
small modality directories add no useful catalog boundary. A screenshot and
camera still are both images; desktop and webcam streams are both video.
Device, API, codec and transport never choose a theft home.

The complete item-placement inventory and source-facet review are in
[the review-pool migration audit](docs/taxonomy-audit/triage/review-pool-20261026/item-placement-audit.json).
The former store/application branches (`env`, `cloud`, `browser`, `wallet`,
`keychain`, `dev-secret`, `ssh`) are retired objective homes; their acquisition
observations remain in the capability and credential-access tiers.

**Credential form precedes secret kind.** At `credential`, the question is
*what form of authentication material is exported?* `value` requires selected
secret values; `record` requires an authentication record/store exported as a
record or container. Within `value`, children answer *which secret kind?*
(`password`, `token`, `key`, `recovery-secret`). Selection is substantive: an
API-key environment read followed by export can support `value/token`; a
whole environment snapshot beside an API-key name cannot. A whole login
keychain is `record`; a selected private key extracted from it is `value/key`.
An environment-filtered secret union stays at `value` when its passing
alternatives span several secret kinds. A union admitting both whole records
and selected secrets stays at `credential`.

Do not guess that a file is a credential store from a chosen output filename,
or that an arbitrary `getWalletFiles()` helper acquires wallet secrets. Keep
its proven body/data-flow observation as a capability. An endpoint name,
credential path and encryption reference do not jointly establish acquisition
or export. Retire an unsupported compound rather than transplanting that
claim to a broader theft leaf. Never remove a failed required role from a
consumer and thereby broaden it; re-establish the result from its remaining
required evidence or retire that consumer too.

**Local acquisition** remains under `collection/` or `credential-access/` by
the acquired subject and acquisition operation. In
`collection/keylog`: `hook` (hook or listener), `polling` (key-state queries),
`device` (input-device reads with recording context), `terminal`; `capture` is
legacy. Keyboard events, hooks and evdev reads stay
`micro-behaviors/hardware/input` until recording, staging or surveillance is
shown; synthesized keystrokes are `hardware/input/keyboard/simulate`.

`collection/file-copy` keeps three distinct collection claims: `bluetooth`
requires Android Bluetooth/OBEX file-transfer evidence; `document` identifies
document/PDF text-extraction capability; `sensitive` requires file copies or
staging selected by sensitive names or roots. These partition by transfer
mechanism, content class and target selection, respectively. Keep them separate
while those claims remain distinct; generic file access stays under
`micro-behaviors/fs/` and does not qualify as collection by itself.

### Persistence follows the trigger

Level 2 is the event that reactivates the code; level 3, the activation
surface.

| Level 2 | Admission | Not this |
|---|---|---|
| `firmware` | Below the OS: boot records, firmware, NVRAM. | Ordinary firmware queries or updates. |
| `login` | A login or session start: Run keys (`registry`, even under HKLM), startup items and shortcuts (`startup`), `winlogon`, XDG autostart (`xdg`), shell profiles (`shell`), login-triggered tasks. | HKLM vs HKCU, or the run-as user, does not decide the trigger. |
| `system` | OS-managed, login-independent: services (`service`; svchost DLLs in `service/loader`), `driver`, `safeboot`, boot scripts (`init`), cron and timers (`cron`), WMI subscriptions (`wmi`), application or platform hooks (editor extensions, git config and hooks). | Detaching (`fork`/`setsid`: `micro-behaviors/process/daemonize`), hiding, or a long-running loop. |

The registry is storage, not proof of login persistence. Service managers use
`service`, not a `systemd` sibling. Platform, privilege and file location are
scope. Authorized-key backdoor installation belongs in
`command-and-control/backdoor/ssh`; a password-spray chain that prepares a
remote key install belongs in `lateral-movement/ssh/deploy-backdoor`. Key and
path references without an installation remain evidence, as does a service
override and nearby write without a bound key. Account provisioning and
privilege configuration belong in `micro-behaviors/os/user/modify`; an
unauthorized account with independently supported backdoor context belongs in
`command-and-control/backdoor/account`.

### Supply-chain trust

**Security-hold classification policy.** `security-hold` classifies the affected
dependency as `hostile`, including an inert npm replacement or a
vendored copy. This is an explicit exception to the usual requirement for
artifact evidence of an attack. The finding describes security-holding status,
not payload execution, and must explicitly identify the hostile subject as the
affected dependency, whether scanning it directly or through a declaring package.
An npm manifest must carry both `0.0.1-security` and the
canonical npm security-holder repository in that same manifest; an authoritative
registry record may instead supply its security-hold flag or holder description.
A manifest whose declared dependency the registry has placed under a security
hold is also classified `hostile`: the finding must explicitly identify the
dependency as the hostile subject and is attributed to its declaring manifest.
It does not assert that the manifest's own code is hostile or that the
dependency was executed.
A version, repository reference, README mention, ordinary deprecation, or
unresolved dependency alone does not establish this classification. Metadata
observations retain their own criticality; the hostile classification belongs
only to `objectives/supply-chain/security-hold`. Archive parents inherit a
matched member's finding, but different members must not supply separate legs.

Read the claim without the package name. If it still only says "steals
credentials" or "runs a downloaded payload", that result owns the composite;
the lifecycle hook (`metadata/package/scripts/lifecycle`) or package-manager
call (`micro-behaviors/os/package-manager`) is referenced.

In precedence order:

1. `trojanized` — required modification or substitution of a legitimate input:
   dependency or update substitution, build pipeline (`build-pipeline`; CI
   authority abuse in `ci-pipeline`), configuration poisoning. A wholly
   malicious package is not trojanized.
2. `hidden-payload` — concealment that abuses package inspection or declared
   contents (`remote-loader`, `native-extension`, `encoding`, …). Generic
   obfuscation is `anti-static`; a full activation chain is a payload chain.
3. `impersonation` — deceptive name, provenance, function or contents
   (typosquat, dependency confusion, brand, clone). Mere name similarity is
   metadata.

### MBC and ATT&CK correspondence

| Local objective | Catalog correspondence |
|---|---|
| `collection`, `credential-access`, `discovery`, `command-and-control`, `execution`, `exfiltration`, `impact`, `lateral-movement`, `persistence`, `privilege-escalation` | The same-named MBC objective and ATT&CK tactic; each mapping still needs a matching behavior or technique. |
| `evasion` | MBC Defense Evasion and the applicable ATT&CK technique. |
| `anti-analysis`, `anti-static` | MBC Anti-Behavioral Analysis (OB0001) and Anti-Static Analysis (OB0002); no ATT&CK tactic. |
| `supply-chain` | No MBC objective. ATT&CK T1195 covers supported supply-chain compromise, not every package-borne attack. |

Placement and catalog mapping can differ: ingress tool transfer may map to MBC
E1105 from a staging leaf.

## Artifact properties: `metadata/`

Classify the property or declaration asserted — not the parser, and not the
file carrying it. A parser exposing a company name, API or credential does not
change its meaning; a text matcher over a structured field is still about that
field. Strings are *content*: a string evidencing a capability, objective or
identity goes with that subject.

Source interface-name observations are grouped by the subject named: network, filesystem, execution, presentation, runtime or encoded references. A name alone does not prove that an interface was invoked or that a program is present.

`lang/source/naming/population` records measured source identifier populations,
including parsed source embedded in other carriers. Name entropy or repetition
alone does not establish concealment; function-name counts and individual
literal shapes follow their more specific subjects.
`lang/source/literal/string/population` records parser-derived string counts,
lengths and ratios. They describe the analyzed source layer and do not establish
that strings are used, decoded or concealed; whole-file and binary string
measurements follow their own subjects.

Within natural-language metadata, `lang/natural/credential` records wording
whose subject is a password, secret, API key or credential transfer; a token
setup instruction belongs there, while generic approval wording remains in
`lang/natural/phrasing`. Such wording alone does not establish credential use
or theft. This separates seven credential observations from the 92-rule
phrasing leaf, leaving 85 there and seven in the credential leaf.

| Level 1 | Level 2 (level 3 refines it) | Boundary |
|---|---|---|
| `arch` | Instruction-set or ABI target, by family | Parsed target fields (ELF `e_machine`); a word such as `mips64` in `.rodata` identifies nothing. Header-field validity is `binary/header`. |
| `binary` | `header`, `section`, `symbols`, `code`, `instruction`, `resource`, `linking`, `layout`, `debug`, `provenance`; a property of that part | **Facts about a part, never what it means:** "three imports" → `symbols`; "imports `GetProcAddress`" → a capability; "exports impersonate `version.dll`" → an objective; "exports are libcurl's ABI" → `well-known/lib`. A part's measurement and malformation share its directory; `crit:` says how unusual. |
| `build` | `bundler`, `minifier`, `transpiler`, `generated`, `ci`, `config`, `manifest`, `artifact`, `reproducible`, `vcs`, … by transform or pipeline function | What a tool left in the file (bundled, minified, transpiled), grouped by function; the tool goes in the trait name (`esbuild-bundled`). "This file *is* webpack" is `well-known/`; compiler attribution is `lang/compiler`. |
| `document` | `pdf`, `office`, `rtf`, `html`, `ole`, `chm`; a parsed part or property | Structure, not the behavior of embedded code. Magic alone is `file`. |
| `filename` | `identity`, `name-form`: own basename and stem | A property of the scanned name, without parent-directory context. An embedded or referenced name belongs to its own subject. |
| `path` | Own scanned location and directory relationships | Parent components, source-tree location and multi-component paths. A path mentioned in code is `micro-behaviors/fs/path`; an archive table entry is `archive/member/path`. |
| `archive` | Container facets and member fields (below) | Properties of the scanned container or its recorded entries; code operating on archives is a capability. |
| `file` | `format`, `magic`, `extension`, `size`, `encoding`, `entropy`, `line`, `text-distribution`, `catalog`, `padding`; remaining whole-file properties | This legacy umbrella grants no default home: a specific subject beats a generic text bucket. `file/string` and `file/literal` are **closed**: move each rule to the subject it evidences. A context-only literal can retain a behavioral subject under the incomplete-evidence contract; it must not claim the complete operation. When no subject is supported, review its reusable literal property or consumer representation. The validator rejects every definition in both retired namespaces. See the [validator enforcement record](taxonomy-migration/research/document-authority/literal-validator-enforcement.md). |
| `hardening` | `build`, `layout`, `memory`, `mitigation`, `sandbox` | Absence is a value of a mitigation, not a "missing" subject. Using a security API is a capability; bypassing one, an objective. |
| `image` | `pixel`, `segment`, `trailing`: decoded-image measurements, segment totals, trailing layout | Whole-file byte entropy is `file/entropy`. A metric name proves no color channel or end marker. Rendering and capture are capabilities. |
| `font`, `media` | *Reserved:* font table and container validity; cross-carrier byte coverage | Whitelisted; create with the first supported rule. |
| `import` | `builtin`, `module` (source-local named modules), `package`, `framework`; engine-emitted `<lang>/<module>` nodes | A dependency reference, not library identity or proof of use. `import base64` supports both directions, so it is an import fact, not `data/decode`. |
| `lang` | `source`, `compiled`, `scripted`, `compiler`, `runtime`, `version`, `encoding`, `natural`, `locale`, `generated`, `upstream` | "Built with compiler X" is here; "this file *is* compiler X" is `well-known/`. Code transformation is `build`; runtime reflection is `metaprogramming`. Engine-emitted `metadata/lang/embedded::<language>` marks detected source inside a containing file; it does not say that source ran. |
| `package` | A manifest field or package role (below) | Properties of the distributed component, not its runtime behavior. |
| `permission` | Declared authority by protected surface (`host`, `clipboard`, `storage`, `network`, …); grant scope and manifest-level profiles combining declared authority or target scope | A hostname without grant context is not a permission; a grant or target profile does not prove API use, injection, interception or theft. Invoking an API is a capability. |
| `registry` | Package-registry publication records: release history, reach, custody, listing claims | Not the Windows registry (`micro-behaviors/os/registry`). Reputation is not a verdict. |
| `signature` | Engine trust states `verified`, `unverified`, `self-signed`, `invalid`; YAML `absent`, `ad-hoc`, `claim`, `certificate`, `entitlements`, `code-directory`, `resource`, `script` | Only `verified/` proves a signer, and it holds engine findings only. Every other path is a claim or a structure; signer names alone do not establish a valid chain. |
| `vendor` | OS or platform vendor provenance (Apple, Microsoft, NetBSD, GNU) | Certificate fields are `signature`; manifest vendor fields are `package`; third-party products are `well-known/`. |

`package/description/marketing` records generic promotional wording and its
co-occurrence with package fields; `function` records claims of a specific
capability or purpose. Marketing wording does not establish intent.

`package/description/ai-tooling` groups package claims about AI agents,
assistants, and related tooling. A description is a claim about purpose; it
does not establish execution or trojanization.

Named dependency references belong under `package/dependencies/<subject>` when
the library has a clear subject, such as `network`, `crypto`, `storage`,
`browser-automation`, `development`, `presentation`, `serialization`, `system`,
or `logging`.
Use `declaration` for named dependencies without a supported functional subject;
`identity` is retired because it adds no meaning. Combinations of declared dependencies
belong under `package/dependencies/composition`. A dependency or combination
describes available libraries, not their use or a stealing objective. `presence`
describes field or dependency presence and absence.

`lang/source/interface/<subject>` holds declared API surfaces with a supported
functional subject. `crypto` includes encrypt/decrypt exports, crypto factory
exports and their nearby crypto imports. An arbitrary object-member assignment
stays in syntax; an export named `encrypt` does not establish encryption or
library identity. A composite additionally requiring crypto API use belongs
with the capability (`micro-behaviors/crypto/provider/library` when no narrower
operation is required). Import/export proximity alone remains a declaration.

The [behavior and intent repair](docs/taxonomy-audit/taxonomy/behavior-intent-repair/README.md)
records worked migration reversals: credential search plus sensitive-file and
multipart clues → `credential-access/files/theft` as upload preparation;
service listing and stop/disable with miner or rival clues →
`impact/degrade/services` as disruption evidence; calculator launch clues with
an install hook → the supported execution subject with hook context
as execution indicators. None asserts completed transfer, a bound service target, a malware
family, or a launch bound to the hook. Generic search, ordinary service
administration without those contextual clues, and calculator launch alone
retain their neutral homes. Service cleanup messaging plus unit configuration
clues remains `micro-behaviors/os/service/config`, not proven disruption.

`data/encode/serialized-json` holds operations that encode serialized JSON,
including JSON-to-Base64 calls. Nearby JSON and encoder names without a bound
data flow are operation references; they do not establish a JSON encoding or
an HTTP masquerade. Generic Base64 conversion remains under `data/encode/base64`.
`data/decode/embedded/base64` records decoding of embedded Base64 literals;
`data/decode/to-file` records decoding that writes to a file. Decoder names and
accessor references alone do not establish decoding.

`file/profile/shortcut`, `lexical`, `screen-capture`, `agent`, `file-operation`,
and `memory` group evidence by subject and then by the observed form. Their
children distinguish, for example, shortcut script references from extensions, capture
APIs from library references, and file-read clues from write clues. These are
profiles of evidence; the group name alone does not establish the operation.
Browser state and automation profiles use `file/profile/browser`; agent session
clues use `file/profile/agent/session`. Defensive scanner evidence is grouped
under `file/profile/scanner` by its subject. References to a scanner subtype
must keep that subtype rather than expanding an exclusion to every scanner.
`file/profile/security` separates policy, hunting and blinding evidence.
Document parsing, format and viewer clues use `file/profile/document`; generic
URL and filesystem path observations remain with their own subjects.
`file/profile/open-handler` records unbound handler names, selectors and command
strings; an actual opener invocation retains its behavioral home.

`file/profile/process` groups profiles whose required evidence concerns a
process operation or its references. A set of API names or command clues is a
profile of those references, not proof that a process was launched or that its
inputs and outputs are connected. Mining configuration profiles belong in
`file/profile/blockchain`; named-tool co-occurrences belong in
`file/profile/tool-reference` and do not identify the analyzed file. Profiles of
network activity, installation, LLM sessions, agent configuration, archives,
and cryptography use their corresponding subject names. Installation profiles
record operation or option references; `installer-layout` records file and
sidecar relationships. An agent configuration or archive reference does not
prove a file was written, a private child launched, or an archive created.

A PDF JavaScript API name, even one associated with a historical vulnerability,
is an API reference. Claim exploitation only when the required evidence supports
the exploit mechanism; neither a script action nor the API name proves a
vulnerable version or malicious payload.

`binary/instruction/cil` records CIL instruction sequences;
`binary/instruction/call` records call shapes and their local argument setup.
Other native and instruction-set-independent sequences remain in `sequence`.
An unbound call sequence does not identify its callee or establish a payload
flow.

`binary/symbols/name/process` groups process-related symbol-name and name-text
observations. A matcher that observes the same name in native binaries and
source text keeps those scopes together. A name does not establish that the
referenced operation was called.

`metadata/file/encoding` is split by observable transform family: `base64`,
`hex`, `xor`, `url`, `escape`, and `compression`; `container` records an
encoding or armor represented by a format wrapper, and `shape` records
encoding-like structure without a supported scheme claim. `metadata/lang/encoding`
uses `base64`, `hex`, `xor`, `url`, `unicode-escape`, `wide`, and `shape` for
the same distinctions in source representation. Every child describes the
observed representation without asserting a decoder call, concealment, or
execution; a recovered layer is recorded as the child file's encoding chain,
not as a finding.

Text shaped like `require('../common')` or `function test()` does not alone
establish a package test-harness role. The rule combining those alternative
source forms belongs in `metadata/lang/source/shape`; a single call form belongs
in `metadata/lang/source/syntax/call`, outside broad `metadata/package/testing`
selectors. An actual module-loading call belongs
under `micro-behaviors/os/module`; a corroborated test-harness role belongs
under `metadata/package/testing`. Preserve explicit consumers when relocating
weak source context rather than granting every test exclusion that context.
System-information field and identifier references belong with their likely
hardware, user, hostname, platform, network or geographic subject. A name
alone does not establish a structured record or information collection; a
required source construct belongs in `metadata/lang/source`.
`micro-behaviors/os/privilege/reference` records OS privilege names in source
or compiled content as partial privilege evidence. A name alone does not
establish that a privilege is present, enabled, requested, or manipulated.
Token evidence separates impersonation, adjustment, integrity and session
operations, API-name references, and other token use. References and
co-occurrences must not claim that an operation succeeded.
JVM constant-pool method-reference counts belong in `binary/symbols/count`;
zero references does not imply that a class declares or executes no methods.

`metadata/lang/encoding/shape/alphabet` records ordered character-set
observations in source or binaries, alongside its `shape/character` and
charset-table neighbors. A recognized sequence alone does not imply encoding,
decoding, or any other operation.
`shape/character` also records invisible-character populations, literal
properties and token splitting. A count remains a measurement even when the
characters appear in legitimate text; unrelated content must not suppress it.

`metadata/lang/locale/timezone` records timezone names and catalogs, while
`metadata/lang/locale/catalog` records translation message catalogs. A timezone
name alone does not establish geofencing. Locale registration, selection and
locale-aware formatting are behaviors; place their evidence under
`micro-behaviors/data/format/locale` or the more specific operation it supports.
Country-code tokens and clusters are partial evidence for country-aware
processing, not proof that a program queries a locale or restricts execution.
Country selector data belongs with the UI selection it supports; translated UI
labels belong with UI localization. Describe the observed evidence precisely.

`metadata/lang/source/literal` records reusable properties of literal objects,
such as a numeric sequence inside a string or quoted source text. It is not a
fallback home for strings or constants whose placement is unresolved. Choose
the subject or identity before the literal's type: a hardcoded string specific
to a single malware family belongs under that family's `well-known/` home;
a marker establishing package or product identity belongs under its
`well-known/` identity; an ordinary dependency reference belongs under
`metadata/import`. A subject-specific constant belongs with the subject it
actually establishes. Quoting a marker
does not turn family identity into generic source metadata.

Within `literal/string`, use `command` for command tokens, `expression` for
source-expression fragments, `property` for attribute or configuration keys,
`shape` for string structure, and `label` for reusable labels without a more
specific identity or subject. A literal alone does not establish execution.

Replace the legacy `literal/value` bucket with object types as its rules pass
review. New rules must not enter `value`.

| Child | Admission |
|---|---|
| `string` | Reusable properties of string contents or shape, with evidence that the content is quoted or parsed as a string. Quoted source text does not establish that the quoted operation executes. |
| `integer` | Integer literal values or numeric properties, with evidence of an integer object rather than digits inside a string. |
| `hex` | Explicit hexadecimal representations or their reusable structure. This representation has its own home even when quoted; a known signature, control code or family marker still goes to its subject or identity. |
| `array` | Array literal contents or structure, with evidence of an array object. A numeric sequence inside a string remains a string. |

Audit every rule's matcher, effective scope, consumers and provenance before
retaining or relocating it. Bare words, call syntax, identifier names and
family-specific fragments do not qualify merely because they were previously
stored in `value`. Do not split these object types by language or platform to
meet a count limit. A category-specific budget exception requires a complete
relevance audit and explicit user approval first.

`source/naming/source-text` holds identifiers and name text referring to source
content, including generated or returned source. Such a name alone establishes
neither a model origin nor compilation or execution.

**Source syntax.** `metadata/lang/source/syntax` asks **which grammatical construct is present?**
Enter this branch only after considering behavioral meaning and subject-specific
placement. Its children describe observations whose substantive claim is the
construct's source form. A text or literal matcher may observe embedded code,
examples or comments; evaluate that scope before attributing capability to the
artifact. An identifier alone does not establish its suggested operation, but
a recognized operation does not lose its meaning because it appears inside an
assignment. Language, API and parser remain scope and filenames, not children.

| Child | Required property | Boundary and deciding example |
|---|---|---|
| `assignment/{name,member,call,value}` | Assignment syntax, grouped by the required target or, when no target is required, the assigned value. | Use `member` for member or indexed targets, `call` for call-shaped targets, `name` when a target name is required without a more specific target form, and `value` when the target is unconstrained. A required `const`, function or type declaration goes to `source/declaration` when its structure is the claim; a name-focused observation goes to `source/naming`. A mapping entry goes to `key-value`. |
| `call` | A call-shaped expression or argument relationship without a more specific supported operation or subject. | An unidentified `handler({...})` call can fit. A recognized decoding or network operation belongs with that capability. A bare `EventDispatcher` name establishes no invocation. |
| `command` | Command words, options, operands or pipelines whose substantive claim is command structure. | An argument-list shape with an unidentified command fits. A recognized file copy belongs with file copying. A parenthesized method invocation goes to `call` only when its meaning is likewise grammatical. |
| `directive` | Source-processing directives, event annotations or named language sections. | ASP.NET `<%@ Page ... %>`, MIDL `cpp_quote`, `@event timer.action`, and YARA `strings:` fit. A type or rule declaration goes to `source/declaration` when its structure is the claim; a name-focused observation goes to `source/naming`. An ordinary mapping key goes to `key-value`. |
| `key-value`, `identity-field`, `credential-field`, `rule-field` | Named key/value entries or markup attributes, grouped by subject where a narrower field category applies. | Account and host fields belong in `identity-field`, credential fields in `credential-field`, and rule-catalog fields in `rule-field`. Generic `"command": "..."` and HTML `href="...?q=..."` fit `key-value`. `obj.command` goes to `member`; assignment to a standalone variable goes to `assignment`. |
| `member` | A qualified name, member selection, subscripted member, or template field reference. | `Net::HTTP`, `exports.KNOWN_C2_DOMAINS`, `obj['a' + 'b']`, and `{{.Field}}` fit. If invocation parentheses are required, use `call`; a field's initializer belongs in `key-value`. |
| `operator` | An operator or cast relates expressions or a value and a type. | A function-pointer cast and a comparison against an epoch constant fit. A function-pointer declaration belongs in `source/declaration`; a large numeric call argument belongs in `call`. |
| `type-expression` | A source expression naming a type, with no required value being cast. | PowerShell `[char[]]` fits; a required `-as [type]` cast belongs in `operator`. |

**Within syntax only, choose by the required grammatical relationship.** These
tests never override a supported operation, target or purpose. A declaration
introducing a binding or type goes to `source/declaration` when its structure is
the claim; name-focused observations go to `source/naming`. An assignment
without declaration evidence stays in `syntax/assignment`. A field entry
beats an incidental member name in its value. For expressions, required
assignment beats a nested call, a call/argument relationship beats incidental
member access, and a cast/comparison beats its operand's spelling. A shell
command's words and options belong together in `command`, even when serialized
as an argument array. An API name alone never acquires call semantics.

A declaration whose substantive evidence is the identifier or its spelling
belongs with source naming; a declaration whose structure matters independently
of the name belongs in `source/declaration`. Neither a name nor a declared
base class proves that the named behavior ran.

`call/construction` records source forms that create an object or command
configuration, including a command-builder factory. A constructor or factory
reference alone does not prove construction, and construction does not prove
the object was started. An actual call whose receiver or purpose is unknown
can instead be named dispatch; its name alone does not establish the resource.

Within `lang/natural`, `vocabulary` describes words or token sets; `diagnostic` records
error and rejection messages; `phrasing` describes other multiword clauses and their stated relationships, such as an action
paired with omission of review. A clause alone does not establish an agent
directive or prove that its described action ran.

After semantic placement has been considered, use the existing neighboring
subjects when no single syntax construct is the claim: `source/naming` for
identifier vocabulary and function-name populations,
`source/literal` for array values or the contents and line shape of literals,
and `source/origin` for a source layer's carrier or extraction provenance.
`source/shape` holds source-context profiles spanning constructs, declarations
or source-file evidence: the Delphi/YARA source signatures, Haxe basename or
package declaration, frontend member-or-hook literal profile, scanner schema
exception, source-catalog label and encoding-related source profile. A single
assignment does not become a whole-source profile because it is counted.
Lifecycle event names belong in `source/naming/event` when no registration
or execution is established; a named hook alone is not a package operation.

The [source syntax move inventory](docs/taxonomy-audit/taxonomy/source-syntax-placement/migration.json)
places all 101 former direct rules. The audit found no identical effective
definitions to consolidate. Matchers, defaults, scope, criticality and explicit
dependencies are preserved. PHP path and command references follow the indicated path or operation; their
contents alone do not establish that an interactive panel exists or that a
command runs.

Raw signed-entitlement keys are emitted as runtime facts under
`metadata/entitlement/<category>::<key>`. The rules in
`metadata/signature/entitlements` interpret those facts into named properties;
the raw entitlement IDs are engine output, not duplicate YAML declarations.

`metadata/package/testing/presence/suite` records names and paths associated
with test suites or testbeds. A directory or filename is a location clue; it
does not establish that tests ran, that all contents are fixtures, or that
contents are safe. The `harness` sibling covers evidence for test machinery,
while `path` retains other testing-location observations pending review.

Documentation claims about agent oversight, anti-bot evasion and CAPTCHA
solving have separate subject homes. They report what a document says; they do
not establish that an agent obeys a policy, that evasion occurred, or that a
CAPTCHA was solved. CAPTCHA solving alone does not imply anti-bot evasion.

`metadata/package/documentation/security-exercise` records documentation
about authorized assessments, security playbooks and CTF exercises; generic
prerequisite, syntax and pattern headings remain markup observations. Text
claiming authorization or a training setting is not proof that an operation
is authorized or harmless. Agent-specific injection guidance and other
security-testing documentation retain their own subjects.

Testing-presence observations are grouped by subject: certificate fixtures,
secret-detector fixtures, safety evaluations, and snapshots have separate
homes. A directory name or certificate field is evidence of a location or
field, not independently proof that the content is safe or that a test ran.
Snapshot-directory paths and unbound certificate-directory observations do not
establish benign fixture context.

`metadata/path` classifies the scanned file's own location by its supported
subject: `software` for paths naming a software tree or artifact,
`development` for source, build, examples, and test locations, `installation`
for installer and provisioning locations, `system` for service and session
locations, `directory` for generic directory-component clues, `shape` for
path spelling, and `storage` for data-location subjects. A software-named path
is a reference, not proof of product identity; a test-named path does not by
itself prove that its contents are harmless. Referenced filesystem paths and
archive member paths have their own homes.

`metadata/filename/document-theme` records filenames invoking documents,
business records, or images; the name alone does not establish deception.
`metadata/filename/shape` records measurable name forms such as hashes, short
stems, and generated-looking names. Scanned directory context belongs in
`metadata/path`, even when a name observation is used alongside it.

`metadata/file/format/desktop-entry` holds desktop-entry field and structure
observations; launch command semantics have their own behavioral or package
entrypoint homes. The scanned file's display-session location is a path
observation in `metadata/path/system`, not an entry field.

`metadata/file/format/news` identifies serialized news records and generated
briefings; `metadata/file/format/threat-intelligence` identifies indicator
records, blocklists, and threat-report fields. These describe document subjects,
not the behavior of quoted content. Other security corpora remain under
`file/format/security-corpus` when they are detection inputs or rule datasets
rather than threat-intelligence exports.

`metadata/file/format/console-font` holds console-font format signatures and
fragment-manifest structure. A matched header prefix alone does not establish
whole-file validity. The reserved `metadata/font` home is for font-table or
cross-carrier properties, not a duplicate format identity.

**`metadata/file/profile` is retired.** Place evidence under its most likely
behavior or objective when it indicates one, including partial evidence. Place
truly neutral measurements, formats, names, and configuration under their
actual subjects. Descriptions must distinguish a reference or co-occurrence
from a completed operation, and named products belong in `well-known/`. Review
semantics with representative controls; general validation does not prove them.

**Archive boundaries follow the observed property.** Member names and member
table observations belong in `archive`, even when the name is a hash,
lure, extension or signing-file label. The scanned file's own basename belongs
in `filename`; an extension-only observation belongs in `file/extension`.
Parsed container-kind declarations (cabinet, Phar) belong in `file/format`,
signature bytes in `file/magic`, and bytes specifically in a PE resource in
`binary/resource`. Phar signature presence and scheme belong in
`signature/certificate/format`; they establish neither signature validity nor a trusted
publisher. A member called `BNDLTOOL.RSA` remains a member-name observation.
Within `binary/resource`, `label` records generic tokens, names and captions
observed in the resource section; a text match there does not establish a
resource-directory name or product ownership. `table` holds directory and
count facts, while `representation` describes content shapes. Named product
or vendor identity belongs with the corresponding `well-known/` entity when
the evidence supports that association.

The live profile children have distinct jobs: `field-presence` records whether
a parsed field exists; `function-population`, `identifier-population`,
`operator-population`, `string-population`, and `token-population` measure
defined populations. Operator populations count parsed source operators; they
do not establish execution or a purpose for those operators.
The remaining children are:
`installer-layout` records file and sidecar relationships; `markup` records
parsed markup or document-content patterns; `structured` records an explicit
relationship among structured fields; `syntax-tree` records parsed tree
measurements without inferring a purpose. `cryptography`, `mobile-config`,
and `tls` group neutral observations by
subject without granting them broad source-context exclusions;
`identity` records static artifact context, not a known product identity;
`tool-reference` records references, not tool use or identity. Existing
`operation-cooccurrence` composites are under individual semantic review: the
frozen `528223c70b` review counted 89 composites in 33 files; its later
reconciliation at `797f566790f5807fde21e613c19545d516430e05` counted 82 in 30
files. These are dated snapshots, not live-tree counts. Same-file presence does
not prove that operations are related. Add no new rules to
`operation-cooccurrence` or `tool-reference` until their boundaries are
reviewed. A fact with a specific behavioral or metadata subject belongs there
instead of in a profile.
The [measured-population contract](taxonomy-migration/contracts/file-populations.md)
defines the population leaves; its rule-by-rule and metric-producer review
remains open.

`file/catalog/<kind>` holds embedded or standalone reference tables, indexes,
and catalogs. `file/catalog/kernel-header` records scoped marker sets found in
OS/SDK headers; a copied marker set does not establish that the whole file is a
header. Catalog markers prove neither use, contact, intent, nor product
identity. `file/catalog/pattern-rules` records a named pattern-rule table
declaration; it proves that the catalog exists, not that its entries are used,
that the table has a threat purpose, or that it has a particular provenance or
product identity. A rule claiming a specific source needs separate schema and
provenance evidence. `file/catalog/unicode` records Unicode tables and lexicons;
source escape syntax belongs in `metadata/lang/encoding/unicode-escape`, and an
isolated escape does not establish table or non-prose context.
Unicode text and literal populations follow their observed properties or
supported behaviors; writing-system mixtures and localization alone do not
establish concealment.
`file/catalog/service`
records service-name references, embedded service configuration markers and
service fingerprint tables (Nmap's HTTP fingerprints); a name mention does not
establish service use, while a provisioning composite must include the relevant
configuration and behavior evidence.

The children of `file/catalog` answer one question: **what kind of entry does
the embedded or standalone reference table list?** Entry is a table's shape
(many records of one kind, or a named table declaration), never one mention;
a single name, path or identifier belongs with its own subject. A catalog marks
its entries as data, so these rules mostly serve as benign context for
detectors that would otherwise read the listed names as behavior. None of them
identifies the analyzed file as a product, which belongs in `well-known/`.

| Child | Admission and boundary | Example | Counterexample |
|---|---|---|---|
| `package` | Inventories of software packages or modules and their versions, hashes or importers: distribution indexes, package-name lists, dependency reports. Declaring a dependency is `metadata/package`; importing one is `metadata/import`. | Debian `Packages` index; `depaware.txt` | A `requirements.txt` that installs them |
| `network` | Tables of hostnames, domain suffixes or network-address assignments: blocklists, the Public Suffix List, OUI vendor registries, widget-source host registries. Contacting a host is a communications capability. | Ad-blocker domain set; IEEE OUI registry | One hard-coded C2 domain |
| `file-type` | Mappings from file names, extensions or MIME types to a type, icon or syntax: MIME databases, extension tables, editor filetype registries, packed build-manifest name tables. Opening or targeting those files is a behavior. | mime-db table; Neovim filetype map | A stealer's list of wallet file names |
| `vocabulary` | Language and API vocabularies: keyword and highlighting lists, symbol indexes, function-signature and API-version tables, error-code tables, tokenizer vocabularies and word-frequency lists. Calling a listed API is a capability. | Notepad++ `langs.xml`; BPE `vocab.json` | Source that calls the listed functions |
| `policy` | Catalogs of access-control policy documents, such as a cloud provider's published managed IAM policies. A policy the package grants or attaches is a privilege or cloud-configuration subject. | AWS managed-policy dataset | An IAM policy granting `s3:*` |
| `pattern-rules` | Named detection-rule tables and rule-definition files, including this repository's own trait YAML. | Elastic SIEM rule; cleave trait file | A program that runs those patterns |
| `threat-pattern` | Threat-knowledge records: IOC tables, adversary-technique datasets (MITRE ATT&CK), feed reports. | ATT&CK `enterprise-attack.json` | A loader carrying its own C2 list |
| `exploit`, `module-index` | Exploit inventories and exploit-module indexes. | Metasploit module index | An exploit implementation |

Precedence when a table fits several children: `pattern-rules` and
`threat-pattern` first (their records describe hostile content, which the
other children would misread as behavior), then the most specific entry kind:
`policy`, `network`, `file-type`, `package`, `vocabulary`. A host blocklist
that also names products is `network`; a dependency report naming domains is
`package`. The retired `file/catalog/identity` leaf mixed these kinds and also
held non-catalog rules: PDPOP registry and library names moved to
`micro-behaviors/os/registry/key/reference` and
`micro-behaviors/fs/path/system/library`, the Apple Calendar bundle identifier
to `micro-behaviors/os/application/target/productivity`, and the Linux kernel's
SELinux policy installer to `well-known/app/system/linux-kernel`.
`lang/source/comment` records source-comment
content and shape measurements; HTML markup belongs with the document. Comment
text indicating a specific behavior or intent belongs with that subject and
must be described as a claim, not executable code or a verified fact. Source declarations,
names and function-population metrics belong in their source subjects; names
do not prove calls. Binary method anatomy belongs in `binary`.
`metadata/import/count` records parser-reported import counts; named module
references belong in their respective `metadata/import` subjects, and neither
proves use. Source attribution or license notices belong in
`metadata/lang/source/attribution` when either alternative suffices.
`file/padding` requires an observed filler span, not a whitespace ratio.
`file/arithmetic` is retired: parsed operator populations follow their source
or syntax subject; actual arithmetic operations belong in
`micro-behaviors/data/arithmetic`.

`binary/symbols/descriptor` records type-descriptor shapes in executable
constant or symbol tables. A JVM byte-array/slice method descriptor belongs
here without asserting that the method is imported or that a particular
constructor uses it. An imported method name belongs with its capability;
an import count belongs in `binary/symbols/imports`.

The existing `file/data-blob` and `file/policy` branches are closed to new
rules. They mix unrelated claims and have no residual catch-all home: migrate
each rule by its evidenced property or subject. Whole-file entropy, file
signatures, names, and string metrics use their specific homes; declarations
of authority, hardening, package configuration, and document content use
`permission`, `hardening`, `package`, and `document` subjects respectively.

**Argument syntax** (`lang/source/syntax/argument`) records textual CLI
options or argv fragments without requiring a complete command. Full command
forms remain in `syntax/command`; programming-language call-argument forms
use `syntax/call/argument-identifier` when an identifier or property argument
is the observed distinction and `syntax/call/arguments` for other forms. A bare `dumps(metrics)` beside a JSON-looking
filename does not establish JSON serialization. Counts of recovered string
candidates belong with text-distribution or binary-layout observations when they
do not indicate a more specific behavior. Generic option text spanning binaries
and source belongs with the relevant process argument; an option does not identify a particular program
or prove that it was passed to a running process. Process options with supported
purpose may be grouped under `process/argument/visibility` or `lifecycle`.

**Additional source-construct boundaries.** Markup attribute syntax belongs
in `lang/source/syntax/attribute`, Go struct tags in `annotation`, Rust match
arms in `match-arm`, and multi-field object shapes in `object`. A single
object key/value pair stays in `key-value`; a complete module/package
statement belongs in `declaration`. Literal field names do not prove an API
call, account operation or HTTP body. These are grammar properties, independent
of the language filename and matcher backend.

**`file/entropy`** is Shannon entropy over the whole analyzed byte sequence.
Region, section, string and decoded-pixel entropy belong with those subjects.
Entropy alone proves no encoding, encryption or hidden payload. The
[image-property contract](taxonomy-migration/contracts/image-properties.md)
covers decoded measurements and parser boundaries.

**`package` level 2 follows the field:** `name`, `author`, `maintainers`,
`vendor`, `description`, `license`, `homepage`, `repository`, `version`,
`runtime`, `entrypoint`, `scripts`, `dependencies`, `ecosystem`, `manager`,
`workspace`, `keywords`; there is no `manifest/` container. Non-field roles:
`files` (members and layout), `documentation`, `testing` (by harness, fixture
or assertion role, not language), `integrity` (checksums, content agreement),
`config`, `publishing`.

- `scripts/{lifecycle,build,command}`: a rule identifying a trigger follows
  the **declared trigger**; a rule identifying command text within the script
  value belongs in `command`, with its trigger retained in the matcher. For
  example, the word `mysql` in `scripts.postinstall` is a command-value property,
  not host discovery or proof of execution. Install and uninstall triggers
  belong in `lifecycle`; declared build triggers belong in `build`; unbound
  command text belongs in `command`.
- `dependencies/<facet>`: the dependency property being observed, directly under
  `dependencies`; `manifest` repeats the carrier and adds no classification.
  Declared, resolved and shipped status remain explicit in the fact path,
  matcher, scope and description. Legacy `declaration`, `lockfile` and `archive`
  catalogs remain closed to new rules while their individual properties are
  reconciled; they are not models for new children.
- `documentation/{claims,security-advisory,source}`: asserted properties,
  advisory references, documentation location. A claim read from the
  manifest's `description` field is `description/<subject>`.
- `files/name` holds member-name patterns (a name suggesting a key is not a
  key); `files/archive-member` holds parsed member structure. Parsed facts about
  the scanned archive (encrypted members, duplicates, traversal segments) are
  metadata; `micro-behaviors/data/archive` is for code that manipulates
  archives.
- A quality judgment (empty, suspicious, incomplete) is a value, not a subject:
  there is no `quality/` or `tooling/`.

**Dependency facets: the first that describes what the matcher reads
wins.**

1. `identity` — the manifest declares a named package (`lodash`) or one of a
   closed set of named implementations of a specific standard (the MessagePack
   dependency alternatives). The exact names determine membership. This records
   the declaration, not proof that the artifact implements the dependency; it
   is not a bucket for arbitrary functional categories.
2. `name-form` — the name's shape (`-linux-x64`, a `.js` suffix); it would match
   a package that does not exist yet.
3. `source` — the right-hand side as a location (`git+ssh:`, `file:`,
   `workspace:`, `github:`, a URL or path).
4. `range` — the right-hand side as a version (`*`, `latest`, `^1.2`).
5. `reconciliation` — declared versus imported (phantom or unused).
6. `presence` — whether the field exists.
7. `count` — how many entries.
8. `composition` — a required combination of declared dependencies, rather
   than one identity or an arbitrary functional category. A runtime import
   combination does not establish a declared dependency combination.

Ecosystems share a facet and differ by filename (`identity/npm.yaml`,
`identity/cargo.yaml`).

**Names and archive properties: ordered placement.** The question at the
metadata root is *which artifact subject has this property?* `file` adds no
information to a filename, path or archive subject and is removed from those
paths. Remaining legacy `file` subjects are not permission to add another
carrier level.

`filename` asks whether the scanned basename names a known conventional file
or follows an open-ended spelling pattern. `identity` holds exact names and
finite sets of conventional names (`package.json`); this identifies the name,
not the software. Names specific to recognized programs belong with that program
in `well-known/`, where they are explicitly labeled as filename observations and
not treated as proof of identity. `name-form` holds patterns allowing arbitrary
versions, hashes, prefixes or suffixes (`Qt5Core-<hash>.dll`). A regex enumerating
a closed set belongs in `identity`; matcher backend does not choose the child.
A required parent directory instead belongs in `path`.

For the scanned object, a generic basename/stem-only matcher goes to `filename`;
a program-specific name goes to its `well-known/` home, and a matcher over its
location goes to `path`. A file called
`package.json` is a filename property; a file below `node_modules/x/` is a path
property; source text mentioning `~/.npmrc` is neither. Preserve the original
matcher domain: do not change a path matcher into a basename matcher during a
move, even when its current description says “filename.”

`archive` asks *which container property or member field is observed?*

| Facet | Required observation | Neighbor and counterexample |
|---|---|---|
| `member/extension` | Entry-name suffix/extension, with no named stem required | `.csv` is a suffix; `invoice.csv` is `member/filename`. It does not establish CSV contents. |
| `member/filename` | Entry basename, stem, token or name shape | `settings_12.ini` qualifies; `assets/settings.ini` with a required parent is `member/path`. |
| `member/path` | Entry directory relationships, separators, traversal or rootedness | `../etc/x` qualifies; the scanned archive's own directory is `metadata/path`. Aggregate counts of these same path properties stay here. |
| `member/size`, `member/time` | Recorded entry sizes or timestamps | One oversized entry is `size`; total unpacked bytes describe container `layout`. |
| `layout` | Container contents, counts, aggregate sizes or relationships between entries | A script beside a library qualifies; one `.js` suffix alone is an entry extension. |
| `compression` | Declared codec or expansion relationship | A compression ratio qualifies; entropy alone does not identify compression. |
| `encryption` | Encryption declarations or bounded cipher-method bytes in the container | An encrypted-entry flag qualifies; this is not code that encrypts a victim file. |
| `parsing` | Container parse success/errors or absent recovered facts | An unreadable directory qualifies; a parser error does not prove deliberate corruption. |
| `serialization` | Structured serialized values/classes in archive metadata | PHAR metadata classes qualify; a class-name occurrence elsewhere does not. |

When several fields are required, the asserted result owns the rule. A
relationship between members or between a member and container facts is
`layout`; merely restricting a suffix matcher to CAB files remains
`member/extension`. Packaging ecosystems and container implementations stay in
scope and filenames. These generic member fields have one home under
`archive`; `package/files` is for packaging-specific roles and layout, not a
second generic entry-name catalog.

The archive parser supplies the same `archive.*` value fields across container
formats. Queries confined to those fields may cover the archive family; a
package-only field or a native-binary field does not gain that scope from its
directory. `for: [archives]` expands to concrete formats and accepts exclusions.
When replacing an explicit scope, preserve its concrete members and platform
gates; do not silently include additional formats. Partial extraction is a
`parsing` property, not evidence of deliberate anti-analysis.

**Certificates: classify by the role the matcher reads.**

| Matcher evidence | Home | Does not establish |
|---|---|---|
| Leaf signer distinguished-name fields | `signature/certificate/subject` | Product identity |
| Issuer distinguished-name text | `signature/certificate/issuer/name` | That the named authority issued it |
| Exact verified-chain thumbprint of a Microsoft code-signing CA | `signature/certificate/issuer/microsoft` | Microsoft authorship when the CA attests third parties |
| Exact thumbprint of a Microsoft third-party component CA | `signature/certificate/issuer/attestation` | Microsoft platform provenance |
| Presence, length or shape of chain entries | `signature/certificate/issuer/chain` | Any authority's identity |
| Verification, digest integrity, nested signatures | `signature/certificate/integrity` | Signer identity |
| EKU, key usage, other constraints | `signature/certificate/security` | That the signature verifies |

**Script-signature markers** belong in `signature/script`. A `SIG` begin/end
marker is evidence of marker text only; it does not establish signature
validity, signer identity, or trust. Keep it separate from certificate
verification and signer fields.

Trust comes from pinned CA thumbprints, never names. Installing or verifying a
certificate is `micro-behaviors/crypto/certificate`.

**Metadata tie-breakers:**

| Choice | Deciding question |
|---|---|
| `binary` vs `file` | Executable or object anatomy → `binary`; whole-file format, extension, magic or size → `file`. |
| `binary` vs `document` | Executable anatomy → `binary`; OLE, OOXML or PDF object structure → `document`. |
| `binary` vs `lang` | Structure → `binary`; the producing language or compiler → `lang`. |
| `build` vs `lang` | Orchestration (cmake, docker, CI) → `build`; language toolchain → `lang`. |
| `build` vs `package` | Transform output → `build`; project hygiene → the `package` subject (`documentation`, `testing`, `config`, `logging`, `error-handling`). |
| `package` vs `permission` | Ordinary fields and members → `package`; declared authority (permissions, host grants, OAuth scopes, content-script scope) → `permission`. |
| `signature` vs `vendor` | Signature chain or entitlements → `signature`; vendor identified by strings or resources → `vendor`. |

Engine-emitted IDs (imports, permissions, signers, browser-extension host
grants) keep their producer schema. Reference them; never shadow them with YAML
copies or move them without an engine change.

File hiding by file-attribute changes shares `objectives/evasion/file-hiding/attributes`
across implementations: Windows Hidden/System flags and BSD chflags do not
need separate children named for their APIs. Moving chflags retains its exact
matchers, scopes and levels. There are no exact or directory consumers of the
retired chflags branch or the attributes leaf in the reviewed snapshot.

Indexed integer/address table layouts belong in
`metadata/binary/layout/table`. An indexed integer and address table does not
prove an attack dispatcher or even callable targets. Symbol-table anatomy stays
in `binary/symbols/table`; instructions stay in `binary/instruction`, and
embedded file images in `binary/layout/embedded`.
Whole-binary extracted-string counts, entropy counts, and sentence ratios use
`metadata/binary/layout/strings`; a measurement does not imply concealment or
locate the strings in a particular section.

## Known entities: `well-known/`

A catalog of recognized software, projects and malware families, not a second
behavior tree. Depth is usually class/function/entity; skip the function level
when it adds nothing. Distinguish an artifact identity, a program-specific
reference or fragment, and a behavior required for a named variant. A directory
name does not turn every observation beneath it into proof that the scanned
artifact is that product, an implant, or an attack.

**Entry bar.** The entity is known by name outside this repository — at least
one in a thousand developers or security engineers would recognize it — and its
rule pays off across many samples. An obscure typosquat or one withdrawn
release is an *instance* of a technique; the technique rule in `objectives/`
catches it and the next hundred. A directory holding only a package-name match
is an allowlist, not an identity: tighten the matcher that fired or add an
exception.

**Identity needs discriminating evidence.** A generic API, a dependency, an
embedded implementation or a signer name does not show the artifact *is* the
product; a family-specific configuration fingerprint does. No general-purpose
traits here, even at low criticality. Identity never blanket-suppresses an
entity's behaviors. Program-specific filename observations may live alongside
that program's evidence, but a basename alone does not establish identity or
justify an exclusion; rules and consumers must preserve that distinction. A
filename-only rule is at most `notable`, and its description identifies the name
as the observation. An incomplete fragment may be `component`. A filename-only
rule does not need an arbitrary file-size bound; content-based binary identity
rules still require a meaningful size bound. A reviewed, explicitly named
product-reference observation may have a matcher-specific exception when its
meaning is independent of file size; it must not claim verified identity.

**A framework is not its payload.** Offensive C2 platforms have a shared
catalog at `tool/offensive/command-and-control/<project>`: operator consoles,
servers, build recipes and project-specific interfaces belong with the project.
Remote-administration products whose ordinary purpose is administration retain
`dual-use/remote-admin`; proxy/tunnel products retain `dual-use/tunnel` even
when used in an offensive workflow. Libraries and ordinary dependency imports
retain their library or import homes. Do not classify every security utility
as a framework: scanners, process monitors and anti-analysis test harnesses keep
their own function and named-entity homes. Under `tool/offensive`, group
reconnaissance, web assessment and credential-access tools by that function
before the named project; other tools retain their best-supported function.
The old mixed `offensive/frameworks` leaf is retired.

An implant claim requires implant-specific evidence. A Sliver operator client
type, license display, threat-intelligence monitor or WireGuard transport is
project functionality, not an implant signature or a hostile operation. A
module path next to a getter named `GetImplantBuilds` does not establish an
implant. Likewise, generic `NTLM HASH`, session-handler names and numeric `-S`
options do not identify SMBExec, Sliver or Nmap on their own. Retain the most
specific supported operation or name observation outside the entity catalog;
reference it from a discriminating project fingerprint when useful. Do not
alter criticality to make a placement legal. Independently correct a verdict
that labels ordinary license display or a scanner's debug-module identity as
hostile; test the intended operation and real payload evidence separately.

Audit every path through an identity composite, not just its strongest leg.
A `needs: 2` rule over two named-project markers and two generic fragments must
not identify the project from the generic pair alone. Require a discriminating
project alternative as well, or a genuinely distinctive configuration/ABI
fingerprint. A common name near HTTP/2 and MIME/JWT markers is not automatically
a C2 family. Co-occurring process creation and a scanner reference do not bind
that scanner to the launched command. Descriptions must preserve these limits.

Scanner evidence is organized by what it examines: threat signatures, secrets,
web content, vulnerabilities, policy, and collected evidence follow the
corresponding detection behavior or evidence subject. Generic identifiers and prose remain neutral
naming or vocabulary observations. Only evidence that identifies a particular
product belongs under that product in `well-known/tool/detection/`; preserve
reviewed exception coverage explicitly when splitting a former shared category.

Defensive tools that audit AI-agent configuration, skills, permissions or MCP
interfaces share `tool/detection/agent/<project>`. This groups tools by what
they audit, not by a language, package manager or generic scanner class name.
The `agentskillmap` and `skillmap` distribution observations identify one
project and share its canonical home. A reference to an old subset must not
silently expand to every observation in the merged directory: preserve the
selected cohort, including its file types and suppression semantics. A generic
`vulnerable-configs` path is a path observation; it identifies no scanner and
cannot independently establish a known-good package or suppress execution.

**The first class that fits wins.** (`malware/supply-chain` is legacy: delivery
does not choose a family's identity.)

| Class | Admission | Level 2 |
|---|---|---|
| `malware` | A recognized malicious family, with family-specific evidence. A legitimate product's name cannot establish a malicious variant. | Defining role: `backdoor`, `botnet`, `downloader`, `dropper`, `exploit`, `keylogger`, `miner`, `ransomware`, `rat`, `rootkit`, `stealer`, `trojan` (only when nothing narrower fits), `virus`, `webshell`, `worm`. One per family, by its most distinctive purpose; actor attribution goes in descriptions. |
| `unwanted` | A recognized PUA, adware or riskware family whose distribution or operation is itself unwanted. | The family directly; no `pua/`. |
| `lib` | A library, framework or runtime. | Function: `ai`, `cloud`, `concurrency`, `crypto`, `data`, `datetime`, `development`, `format`, `media`, `native`, `network`, `observability`, `platform`, `runtime`, `stdlib`, `testing`, `ui`, `vendor-sdk`, `web`. |
| `dual-use` | A legitimate product whose primary purpose is abuse-relevant. | `access-control`, `credentials`, `packaging`, `remote-admin`, `transfer`, `tunnel`. |
| `game` | A game or platform, or a game-specific mod, cheat or anti-cheat. | The game, or an existing class. |
| `tool` | A professional developer, administrator or analyst utility. | `browser`, `detection`, `development`, `forensics`, `media`, `offensive`, `packaging`, `reverse-engineering`, `sysadmin`. |
| `app` | An end-user application, suite or platform component. | `ai`, `browser`, `browser-extension`, `communication`, `data`, `development`, `enterprise`, `finance`, `infrastructure`, `media`, `network`, `productivity`, `publishing`, `security`, `storage`, `system`, `utility`. |

**Function collisions:**

| Competing | Owner |
|---|---|
| `lib/testing` vs `lib/development` | Test execution, assertions, mocks, fixtures → testing; compilers, build, lint → development. |
| `lib/format` vs `lib/data` vs `lib/media` | Parsing and serialization → format; query, storage, data models → data; audio, video, image codecs → media. |
| `lib/network` vs `lib/web` vs `lib/ui` | Protocol or transport client → network; server or app framework → web; visual components → ui. JavaScript does not make all three web. |
| `lib/cloud` vs `lib/vendor-sdk` | Cloud control-plane SDK → cloud, even for one provider; other single-vendor SDKs → vendor-sdk. |
| `lib/platform` vs `lib/runtime` vs `lib/native` | OS or device integration → platform; language execution or FFI → runtime; libc, allocator, ABI → native. Being compiled does not make it native. |
| `lib/stdlib` vs a domain | Extends or polyfills the language's own standard library (lodash, six) → stdlib; anything with its own domain keeps it. Small size is not stdlib. |
| `app/development` vs `tool/development` | Integrated IDE → app; standalone compiler, build or CLI → tool. |
| `app/security` vs `tool/{detection,forensics,offensive,reverse-engineering}` | Deployed end-user protection → app; analyst workflow → tool. |
| `app/infrastructure` vs `app/network` vs `tool/sysadmin` | Deployment or control plane → infrastructure; ordinary network app → network; operator utility → sysadmin, unless dual-use wins. |

Before adding an entity, search every bucket for its name and aliases; a
classified entity moves only with its references.

## Worked placements

Cases where the deciding fact spans sections. Objective rows assume required
evidence establishes the abuse. *mb* = `micro-behaviors/`, *obj* =
`objectives/`, *meta* = `metadata/`.

| Required observation | Home | Nearest alternative and deciding fact |
|---|---|---|
| Bare `memcpy` symbol in a malware sample | mb `mem/copy` | Attribution adds no family-specific evidence. |
| `BASH_ENV` referenced inside a CI attack | mb `os/env/runtime` | Still runtime configuration; `cicd` needs CI-specific evidence. |
| Attack harvests AWS secrets from environment variables | obj `credential-access/env/…` | The immediate source beats the cloud issuer. |
| Attack extracts a browser secret from an OS keychain item | obj `credential-access/keychain/…` | The immediate store beats its browser consumer. |
| Attack decrypts a browser password database with a keychain-derived key | obj `credential-access/browser/…` | The database is the final source; the key only unlocks it. |
| Host and user profile sent through Telegram during npm preinstall | obj `exfiltration/stealer/system-info/profile` | The profile is the source; Telegram and the install hook are referenced context. `exfiltration/messaging/telegram` applies only without a narrower source. |
| `Zone.Identifier` stream name | mb `fs/path/stream` | Removing Mark-of-the-Web needs modification evidence. |
| Raw GitHub URL ending in `.png` | mb `communications/http/url/github` | A suffix proves neither response bytes nor steganography. |
| Send email (B0020); victim abused to send spam (B0039) | mb `communications/email/send/…`; obj `impact/spam` | Legitimate bulk mail is the near miss for spam. |
| Conditional execution (B0025) | mb `data/control-flow/branch` | Analysis-targeted gating is `anti-analysis`; an admitted activation guard is `execution/trigger`. |
| Execution dependency (B0044) | meta `lang/runtime` or `package/dependencies` | A dependency shows neither process creation nor an environment check. |

Encoded API names follow the named API or encoding subject until call syntax or behavior is supported. Unbound process-creation API combinations follow the likely process operation and describe their uncertainty.

## Migration status and legacy branches

The tree is mid-migration. While a transition is open:

1. **New rules go in an admitted target home.** First confirm the validator you
   run accepts the destination (`directory_whitelist.rs`) and that the proposed
   partition satisfies the uniform directory limits. A documented target may
   still require validator admission, coordinated through the migration plan.
2. **Directory references don't follow moves.** A composite referencing a
   legacy directory misses rules added to its target. Find its consumers
   (`rg 'legacy/path'`) and check which members each should select before
   rewriting it: adding a target directory can broaden a composite or its
   exclusions. Verify with positive and near-miss fixtures.
3. **Moving rules is a migration batch:** account for every rule in the source;
   preserve matchers and scope; update consumers, defaults, exception references
   and external mappings together; record fixtures and corpus results.

Applied so far: memory operations into
`mem/{map,unmap,free,resize,copy,fill,compare,query,combined}`;
direction-neutral codecs into `data/codec` and `data/compression`
(`data/compress/combined` retired); `communications/http/ssl` into
`communications/tls`. Acceptance evidence and known gaps are in the migration
plan. Recent role and compatibility reviews are indexed in
[legacy category review batches](docs/taxonomy-audit/taxonomy/legacy-role-migrations.md).

### Migration map

*Staged*: a reviewed batch in `taxonomy-migration/batches/`, not yet applied.
*Partial*: some rules moved. *Open*: no accepted batch.
**Retire** means empty the legacy namespace. **Selective review** means keep
valid rules and move only mismatches; branch population is not a move count.
See the [bounded behavior migration](docs/taxonomy-audit/taxonomy/bounded-behavior-migration/README.md)
for current mappings, resource splits and reference-set checks.

| Legacy home | Target home | How rules move | Status |
|---|---|---|---|
| meta `file/encoded`, `lang/encoded` | meta `file/encoding`, `lang/encoding` | Representation and recovered-layer facts retain distinct meanings | Applied (rule directories migrated; both old directories are rejected; the decoded-layer emitter `lang/encoding/layer::<scheme>` is retired in favor of the child file's encoding chain) |
| mb `data/db/sql` (retire) | mb `data/db/{read/{records,column,key-value},query,open,config,write,schema}`, editor and protocol subjects, or declared metadata | Preserve query targets and the distinction between reference, preparation and execution | Applied (70 rules; no compatibility alias) |
| mb `process/create/spawn` (retire) | `create/{exec,hidden,subprocess/launch,shell/encoded}` | Classify the operation, not API spelling | Applied (11 rules; crowded destination siblings reorganized) |
| obj `exfiltration/serialization` (retire) | `exfiltration/stealer/credential` for supported export; `data/serialize/{schema-credential,envelope,binary}` for preparation/format evidence | A serialization format is not a stolen item or proof of transfer | Applied (12 moved; unreferenced synthetic QNX rule removed) |
| mb `os/network/{forward,neighbors,qos,route}` | mb `network/<same>` | Same subject | Applied |
| mb `os/network/{connections,dns,share,status,tunnel}` | mb `network/<same>` | Same subject | Applied |
| mb `os/network/interface` | mb `network/interface` | Same subject | Applied (the last adapter-binding rule moved; no YAML rules or live YAML references remain in `os/network`) |
| mb `os/network/mac_address`; `webextension` | mb `network/interface`; mb `communications/proxy/config` | MAC addresses are interface identity; WebExtension rules configure browser proxies | Applied |
| mb `communications/ipc/irc` | mb `communications/irc/{command,handler}` | IRC is a network protocol | Applied |
| mb `communications/http/url/*` (generic URL facts) | mb `communications/url/<facet>` | Generic syntax to URL facets; HTTP endpoint, API-route and request facts stay | Applied (generic facts moved; the remaining HTTP URL API leaves contain API and REST path evidence; construction, path, query, scheme, encoded, host/domain/port/TLD, fragment, external-IP and navigation batches moved; the remaining path leaf was retired by separating API routes from generic SQL diagnostic and raw identifier path fragments; executable and document URL references moved to resource URLs, retail path fragments to resource paths, embedded HTML links to markup, and package-registry observations to construction, service, bytecode or network profiles; the legacy telemetry URL leaf was retired by separating resource paths, service and API paths, literals, and HTTP request lines; the PHP endpoint leaf was retired by separating URL and query shapes, script paths, names and co-occurrence profiles; generic endpoint URL shapes, URL assignment and construction, Google host references, and JVM path bytes moved to their respective subjects; request targets, API and resource paths, and unbound endpoint co-occurrences were separated; configuration and admin API paths moved by route evidence, and a mixed remote or encoded URL alternative moved to a network profile; file-management route registration and resource paths were separated, while scanner path and identifier observations no longer claim exploitation; the remaining named host, service and API references and network profile were relocated, retiring the generic HTTP endpoint leaf; documentation IP suppression now requires the IP and route in one URL; generic CGI and OAuth paths no longer claim a particular vendor; preinstall command URL values moved to package scripts and recognized out-of-band callback URLs to their host subject; unbound collect and header text moved to endpoint profiles, an arbitrary tgfrg path no longer implies audio transfer, and audio export requires POST evidence; login parameters alone no longer claim forgery; a formatted beacon URL no longer claims a POST or PAN-OS platform; GitHub raw-content, Gist and API references moved to the named service, base-URL assignment to construction, and WinInet cooccurrence to a neutral network profile; unrelated filename and documentation filters no longer hide raw URL facts; public forge URLs now resolve to their actual named services and Git receive-pack paths to Git transfer; fake cross-product domain combinations no longer count as known forges; named GitHub repository and release references moved to their projects; a Tesseract model URL no longer identifies the containing file as the OCR library; media and installer URL shapes moved to URL resources, image markup to its document/request subject, and parsed PDF action links to PDF actions; PDF annotation context no longer uses unrelated cloud URLs as action evidence; archive URL syntax, PDF actions, Python runtime references and payment-themed filename evidence moved to their subjects; an HTML doctype no longer suppresses archive URL facts and an unbound filename/refresh pair no longer asserts a confirmed hostile download; MediaFire, pCloud, Yandex Disk and Zoho URLs moved to their services; content-delivery, Amazon Web Services and Microsoft Azure applications were grouped to reduce the crowded infrastructure level; broad Zoho account/API references were separated from WorkDrive-specific URL evidence, retiring the legacy cloud URL leaf; Dropbox, Google Drive, Alibaba OSS, Tencent COS, Filen and Koofr references were separated by service; cross-provider URL cooccurrences moved to a network profile and an unbound download query remained generic; named S3, GCS, R2 and other object-storage URL references moved to their services; unrelated SDK or fixture strings no longer suppress those observations, and GCS/token cooccurrence no longer claims an authorized client; Discord, Google Drive and MEGA URL references were separated by named service, generic PE URL suffixes moved to URL resources, and executable-link facts no longer imply hostile intent solely from a storage provider; CDN provider URLs moved to named services, provider cooccurrence to a network profile, and lookalike domains to brand masquerade; genuine CDN references no longer suppress separate lookalike evidence; shortener service names moved to URL reference evidence, navigation proximity moved to window navigation, StepSecurity to its named service and the provider-neutral translation path to URL resources; the crowded endpoint leaf was divided by collection POST, transfer-route and resource-route evidence; collect URL literals and RouterOS cooccurrences no longer assert exfiltration or a QNX platform by themselves; generic explain, comments and query path fragments no longer independently claim SQL evidence; PeopleSoft, NGINX Unit and Vite product paths moved to their named identities; ESET and GlobalProtect product paths moved to their named identities with reviewed whole-file validator allowances while the Vite traversal behavior remains separate; API-specific and transport-specific leaves remain); generic publish, messages, results, sysinfo, upload, payment and token path fragments moved out of API paths, with an unrelated source-tree suppression and unsupported exfiltration tags removed; the crowded resource-path leaf was divided by identity, content, collection, file, administration and commerce subjects, while paths without a supported subject moved to neutral path evidence; generic account, message, screenshot and web-page paths moved to their resource or path subjects; upload-session suffixes remain neutral without upload evidence, and an actual version-manifest URL moved to the HTTP resource facet; PHP query and URL shapes, generic repository and list paths, dynamic logout templates, short URL shapes, and peer URL cooccurrences moved to their supported subjects; JMX query evidence moved to URL query and JBoss and Traktrain references moved to their named products, while unrelated URL exclusions no longer suppress a short-URL observation; numbered-host and tracking observations, PDF action URLs and route-configuration fields moved to their evidence subjects; generic hostname shapes no longer imply FakeCaptcha, and unbound NGINX Unit configuration clues no longer assert a live hijack; generic task, heartbeat, command, registration and file-prefix paths moved to resource or query subjects, and collection/data API path observations no longer claim exfiltration; generic timeline and loopback-agent routes moved to HTTP path references, their composite no longer asserts a Plex identity without a named marker, and a private URL that also matches health and status moved to its network host subject; the API service leaf retired: capture and MCP REST paths moved to API subjects, an addKey query to query evidence, and the NITRO path to NetScaler; a documentation-only MCP target remains non-hostile without suppressing a separate non-documentation target URL and size bounds no longer hide development-path observations; Sentry ingestion references moved to the named service with a domain-label boundary, generic trace and telemetry paths to resource subjects, and path-only observations no longer claim exfiltration or depend on a binary size ceiling; a generic result path, chat-or-agent URL and IDE-action cooccurrence moved to their supported subjects; unrelated Bitwarden and hashed-record context no longer suppresses separate API path observations, and API path names no longer assert transmission; FileUpload, message-limit and universal-transcode path fragments moved to generic URL subjects, while admin API paths no longer imply command-and-control; a generic native upload URL moved out of API paths, a PHP upload URL no longer carries command-and-control tags or a file-size ceiling, and Java collection paths alone no longer count as exfiltration; the class-file collection matcher now inspects bytecode text with a path boundary |
| mb `crypto/symmetric/<alg>/{decrypt,…}`, `crypto/asymmetric/{encrypt,signature}` | mb `crypto/{encrypt,decrypt,sign,verify}` | Operations move; presence stays | Applied (operation-specific and asymmetric signature legacy directories and live YAML references are absent; asymmetric encrypt name-only evidence moved to source naming; signature observations were separated into key, primitive, operation, naming and text subjects; regression examples are under `testdata/*/generated/taxonomy/signature-operations`; generic symmetric encrypt leaf retired: calls → encrypt, native API names → binary symbol names, bytecode text → bytecode metadata, package import → module import; generic symmetric decrypt leaf retired: calls → decrypt, local helper import → module import, PEM/API text → cryptography profile, and unbound command options → command syntax; GPG command and re-encryption call → encrypt, GPG argument and literal observations → command syntax, unrelated encryption/enumeration/deletion evidence → component profile; directory consumers enumerate their previously reachable members; AES and Kerberos decrypt symbol references → binary symbol names, with unbound XOR co-occurrence → cryptography profile; Fernet-context decryption and CryptoJS AES direction evidence moved to decryption or encryption; AES-GCM decryptor initialization, decryption-related cooccurrence and an OpenSSL AES decrypt command moved to their stages; C# decryptor setup and VB6 encrypt/decrypt declarations moved to their stages, while unbound AES, hex and byte-slice clues moved to a profile; Node cipher constructors moved to directional operations, a generic fixed buffer to buffer allocation, and the hardcoded-key consumer now requires a key-named value; Go CFB/CTR, key and IV evidence was separated by supported subject without assuming AES; Python padding names and directional crypto evidence were separated from AES presence; AES-GCM object-construction alternatives remain presence evidence; the crowded decryption leaf was split by initialization and transformation, with unbound co-occurrences moved to profiles; Fernet-context encryption moved to encrypt and an incorrectly labeled DES constructor moved from Triple DES to DES; RC4 was divided into key scheduling, keystream transformation and combined cipher evidence; additional generic syntax and an unrelated LFSR transform moved to their actual subjects; generic indexed-array and XOR syntax moved out of RC4, VB module and string-conversion evidence moved to their subjects, and unbound crypto/HTTP cooccurrence moved to a profile; Node DES and Triple DES CBC decipher initialization moved to decryption initialization, while unbound .NET DES provider/decryptor co-occurrences moved to cryptography profiles; the Fernet leaf was retired: imports, class symbols, bytecode references and literal forms moved to their subjects, with unbound context in cryptography profiles; a generic Base64 literal beside a Fernet symbol no longer claims an encryption operation or hardcoded key, and its matcher now examines the parsed literal value; the AEAD method-name evidence moved to cipher observations; OpenSSL random-byte generation moved to OS randomness, AES command evidence to cipher observations, and unbound command co-occurrences to cryptography profiles without claiming a generated session key; ransomware and hybrid-encryption consumers now require an OpenSSL AES encryption command rather than accepting an explicit decrypt command; the Blowfish leaf was divided: source imports, direction-neutral cipher initialization, cryptography profiles and algorithm words moved to their subjects; the GitHub decryption claim now requires a decrypt call rather than treating an import as decryption; serialized AES/decrypt names and Go ChaCha method-name text moved to bytecode and symbol-name evidence, and the AES-CCM constant is described as a reference rather than usage; AES-GCM imports, type and helper names, literal values, configuration co-occurrences and unrelated syntax observations moved to their evidence subjects; a Go symbol-name check no longer claims construction, a five-megabyte limit was removed from a plain name match, and generic context-encryption markers no longer claim an AI-chat identity; direction-specific XChaCha encryption and TEA or stream decryption evidence moved to their operation leaves; a three-call block loop and the symmetric SystemFunction033 API no longer claim a direction; XOR name and numeric co-occurrence clues moved to evidence subjects, a rotate/NOT loop moved to bitwise operations, and direction-neutral instruction patterns no longer claim encryption or require arbitrary size minima; AES script and .NET data leaves retired: inverse-cipher name co-occurrences → decryption profiles, the RCON assignment → source naming, and decryptor, Rijndael and CBC names → their supported subjects; Triple DES and decryptor name proximity moved to a decryption profile without implying a bound call; a generic DES constructor and aggregate no longer claim CBC or map neutral cipher references to obfuscation; AES runtime-library retired by separating mode references, key representations, named TikTok material, crate references and cipher profiles; fixed key and IV observations no longer vanish for test-vector values or unrelated XOR and filename context; AES library retired: algorithm, mode, constructor, bytecode, dependency, key, filename and cryptographic-context evidence separated; library names and imports no longer claim usage, and a kernel-source marker no longer suppresses separate AES text; AES package, CCM, CTR, GCM and VB6 leaves retired: constructors, mode and name references, dependencies and key-generation evidence moved by claim; generic counter-cipher text no longer establishes AES, and AES dependencies no longer suppress separate CBC dependency facts; AES-CBC constructor and decipher-initialization clues moved to their operations, Java AES factory text moved to initialization, and mode names no longer claim network encryption or a selected cipher without evidence; XOR source-loop evidence moved to reconstruction, bitwise operations and syntax or composition subjects, and a hex-shaped PHP class no longer claims MD5; generic native and PowerShell XOR loops, scalar operations and index handling moved to bitwise or control-flow subjects; Salsa and XSalsa calls were separated from ChaCha, shared sigma evidence moved to its own stream-cipher subject, and generic keystream references and transformations were separated; feedback decoding moved to its operation and no longer has an unrelated whole-file size bound) |
| mb `crypto/native`, `crypto/library/{provider,cng,cryptoapi}` | mb `crypto/provider` | Operations go to their own leaves | Applied (provider and CryptoAPI rules moved) |
| mb `crypto/library/*` (other children) | Primitive family, operation, `data/transaction`, `communications/blockchain`, `crypto/key`, or the observed name/text | By claim | Applied (provider and blockchain operations moved; crypto and API names → metadata; unbound call text and marker co-occurrence → cryptography profile; no legacy YAML rules or live YAML references remain) |
| mb `crypto/asymmetric/{key,ecdh}` | mb `crypto/key/{generate,import,export,exchange,representation}` or the observed syntax/name | By claim | Applied (ecdh → exchange; key generation, import and representation → their subjects; git-secret reveal → decryption; wallet and library names → source naming; unbound key-recovery terms → cryptography profile; no legacy YAML rules or references remain) |
| mb `crypto/symmetric/{analysis,ciphertext}`; obj `credential-access/cracking/public-key` (generic reduced-round clues) | mb `crypto/analysis`; source naming and crypto-envelope context | Cryptanalysis does not by itself identify the cipher family or a credential target; ciphertext naming does not prove symmetric encryption | Applied (cryptanalysis and ciphertext clues moved by subject; generic research indicators no longer claim public-key credential cracking) |
| mb `crypto/symmetric/key`; mb `crypto/key/representation` (crowded) | mb `crypto/key/{representation,derive,import,export}` and evidence profiles | Split key evidence by supported operation or representation; references and placeholders do not establish encryption or malicious intent | Applied (symmetric key leaf retired; representation split by encoded format, material and references, with import, export and derivation moved by operation; unrelated path and tool contexts no longer suppress key facts) |
| mb `crypto/hash/{crc32,fnv}` | mb `data/checksum` | Noncryptographic | Applied |
| mb `data/source/*` | mb `metaprogramming/*`, `data/control-flow/*`, `data/property/*`; meta `*` | By claim | Applied (source syntax and naming, metadata, reflection, control flow and property operations routed by claim; no YAML rules or live YAML references remain under `data/source`) |
| mb `data/encoded` | meta `file/encoding` or mb `data/decode/<scheme>` | Presence vs operation | Applied |
| mb `data/decode/{request,reflection,environment,native}-base64` | mb `data/decode/base64` | Origin is not an algorithm | Applied |
| mb `fs/shell-ops` | mb `fs/{read,write,delete/*,file/*}`, `ui`, `os/application/shell-namespace`, or meta `binary/symbols` | By evidenced subject; an unspecified Shell32 file operation is a symbol reference | Applied (all 42 rules and references moved; the legacy directory has no YAML; see [migration inventory](docs/taxonomy-audit/taxonomy/shell-subjects/migration.json)) |
| mb `fs/traversal`; `fs/enumerate` (non-inventory) | mb `fs/directory/traverse`; `fs/directory/readdir`, `fs/search` | Inventory stays in `fs/enumerate` | Applied (traversal, directory listing, and permission search moved; volume-capacity observations moved to disk system information; drive inventory no longer holds current-directory names, unbound traversal clues or infection evidence; bytecode names, media identifiers and unbound drive/file combinations moved to evidence profiles, with an unsupported size cap removed; media, drive and network clues no longer claim removable-media exfiltration; mount-manager paths and diagnostic text were separated from volume-enumeration clues; single-directory reads, unbound names and module imports were separated from recursive traversal; root-path selection is no longer treated as a walk without traversal evidence; combined listing-or-traversal capabilities use directory enumeration and unbound Dirent clues remain a profile; volume/device inventory remains) |
| mb `fs/directory/mkdir` | mb `fs/directory/create` | Rename | Applied |
| mb `fs/memory/mmap`, `mem/alloc/map` | mb `mem/map` | Any backing | Applied |
| mb `mem/c-runtime/functions`, `mem/alloc/{executable,heap,managed,…}` | mb `mem/{alloc,free,resize,copy,fill,compare}` | By operation; allocator only when established | Applied (retired C-runtime, executable and managed allocation homes have no rules or live YAML references; heap, virtual and unified allocation remain by the supported memory subject; C-runtime allocation → `alloc/heap`; PowerShell `Marshal.Copy` → `copy`; Rust alloc_zeroed, dealloc and realloc split by operation; available-byte division → source syntax; managed leaf → unified host/device allocation, with no legacy rules or YAML references; Java memory-flag references → protection and named-flag evidence, JavaScript allocator/flag text → combined memory evidence, Lua/Python/PowerShell VirtualAlloc observations → virtual allocation; unbound push immediates → binary instruction operands; Windows kernel pool allocator and flags → heap allocation, safebuffers text → build hardening, hashed VirtualAlloc bytes and source call text → virtual allocation, commit/protection constants → combined memory evidence, unbound calls → instruction observations, delegate API text → API resolution; executable leaf fully moved to observation-specific homes; BIOS 413 assembly text → instruction operands; neither legacy leaf has YAML or live references; a bare megabyte value moved to numeric evidence and byte-collection constructors moved to collection creation because neither establishes heap placement; VirtualAllocEx evidence moved from remote to virtual allocation because its handle can identify the current process; cross-process claims require separate target evidence; heap review moved an unbounded retention loop to memory exhaustion, generic alloc tokens and Rust Layout construction to evidence subjects, and pool flags to named flags; common import counts and runtime labels no longer downgrade heap creation, and the executable-heap clue no longer has an arbitrary size ceiling; virtual allocation evidence no longer disappears in Go, Bun, WOW64, game-mod or unrelated plugin contexts; register-call patterns are described as patterns rather than resolved APIs, misleading process-injection tagging was removed, and three binary-size ceilings were dropped; unbound resource/allocation and allocation-name/number combinations moved to memory profiles and a bare MEM_COMMIT name moved to flag evidence; HeapCreate moved to heap creation and its unbound executable-flag co-occurrence to a memory profile; unbound MEM_COMMIT and MEM_RESERVE names moved to source naming, Python VirtualAllocEx no longer claims process injection on its own, and allocation/write API evidence no longer implies a remote target or disappears in library contexts; general PE allocation-API consumers now use the import-or-name aggregate, while importless and encoded-name consumers remain text-specific; heap and virtual allocation descriptions distinguish API names from calls, and RWX call text is notable rather than suspicious on its own) |
| mb `mem/decompress` | mb `data/decompress/<algorithm>` | A data transform | Applied (no rules remain under `mem/decompress`; algorithm rules are in `data/decompress`) |
| mb `process/threading/*` | mb `process/{thread,sync,work}`; IPC to `communications/ipc` | `queue` → `work`; locks → `sync`; thread creation/concurrency → `thread` | Applied |
| mb `process/fork` | mb `process/create/fork` | Duplicate | Applied |
| mb `process/user` | mb `process/identity` or `os/user` | Current process vs principal administration | Applied (user queries moved by subject; no legacy YAML rules or live YAML references remain) |
| mb `process/create/{launch,direct,spawn,execv,spawnv,stdlib,wrapper,…}` | mb `process/create/<mechanism>` | [Process creation](#process-creation) | Partial (`stdlib` class and symbol references → JVM imports and binary names; `wrapper` generic calls and call-like text → source syntax; both leaves have no YAML or live references; `execv` source constant, native name text and argument text → naming and syntax subjects, macOS syscall → syscall invocation after recursive suppressor review (current syscall fact production is ELF-only); unbound HTTP/exec correlations → operation-cooccurrence profile; Python exec/spawn calls → process replacement or child creation and name-only variants → binary name/import subjects; a JVM Runtime.exec method reference → JVM imports; C++ library symbols → binary names and unbound process combinations → co-occurrence; Deno process call, constructor, runtime path and flag literals → their subjects, with unbound HTTP/command clues → network profile; `launch` text → source syntax and text-shape observations, with bound install-hook and FTP findings retained separately; `launch`, `direct`, `execv` and `spawnv` have no YAML or live references; native process symbol names and unbound pipe/exec combinations moved to metadata; download and execution names without a required launch and unbound macOS calculator arguments moved to their observed subjects; `spawn` is now retired, `exec` separates current-image replacement into `process/replace`, and `subprocess` separates configuration, launch and output capture; Go and Rust command constructors, including PsExec configuration, moved to configure, while Python bytecode API and result-name co-occurrences moved to bytecode evidence; direct Bun, Deno and Python image-spawn calls moved to exec, Go Cmd.Run to subprocess launch, and Perl open3 to subprocess I/O; an unbound PowerShell command string remains component evidence; popen retired by separating PHP and Perl shell calls, Ruby subprocess calls, pipe capture and neutral profiles; generic web-asset references no longer independently identify Upstyle; retired creation buckets are enforced by the process policy; shell-subprocess retired by separating shell creation from bytecode references, and api-system retired by separating unbound system symbols, application parameter text and binary profiles; argv-launch and background retired: argument-vector execution, subprocess evidence, backgrounding, detachment and package-triggered fetch clues moved to their mechanisms; shell background jobs are no longer described as necessarily detached; the package-trigger leaf was split by build, lifecycle and import phase, and Python startup evidence moved to Python startup persistence; the crowded interface-name leaf was split by evidence subject before further process dispatch review; command-handler retired: GitHub-sourced command execution, Go command construction, queue operations, diagnostics and unbound names moved by subject; embedded retired: Office/MSI API-name text, x86 instruction sequences, byte-copy and XOR loops moved by subject, and unresolved indirect calls no longer independently establish a hidden launch or exploit; a Windows Go matcher now handles an unset pclntab text address and no longer rejects files over 64 MiB; indirect retired: event-to-module dispatch, spawn-call syntax and import co-occurrences, and Conhost command text moved by subject; runtime-host retired: .NET executable-name references moved to their runtime, unbound PowerShell host references to profiles, and MSBuild declarations to build metadata; the prebuild command-host reference no longer uses an arbitrary 200-character ceiling, and unrelated vendor context no longer suppresses PowerShell reference profiles; variable-spawn retired: variable-argument call text and unbound launch or fetch/write co-occurrences moved to their evidence subjects; the crowded call-argument leaf was split to group identifier-argument evidence; managed retired: named Rundll32 evidence, process configuration, stdout setup, actual process starts and unbound Runtime/exec text moved to their subjects; the crowded subprocess-launch leaf was reviewed and relieved of name-only or unbound evidence; root-shell and output-root-shell retired: helper calls, imports, function names, job calls, stdout literals and script-field text separated by evidence; service-api, server and sshtty retired in favor of MCP registration, call-argument syntax and named product references; self-respawn retired: the detached CLI exception moved to process lifecycle, mIRC exit relaunch to the named application, and unbound Node call/environment and filename clues to syntax or profiles; registry Run-key and Winlogon API co-occurrences moved to registry profiles; arbitrary whole-file size ceilings and unrelated context suppressions were removed, and the Run-key action now lives under registry write/autorun; vb-shell and the empty vb6 carrier retired: NirCmd, shell, Run-key, file-delete, DEP setting, declaration and call-text evidence moved by subject; unbound shell and staging combinations are profiles; the exec leaf was reviewed with its directory-wide consumers, and unbound API names, installer configuration, package-script references, and evaluation or transformation co-occurrences moved to their evidence subjects; unbound HTTP, checksum and command co-occurrences moved to network-process profiles, and an mshta name moved to its named utility without asserting execution; neither enters consumers of the system-call directory; a duplicate SSH option observation was consolidated under the SSH client, decoded PowerShell evaluation moved to interpreter evaluation, OpenShift download exceptions moved to the named product, and unbound TMPDIR copy/chmod/launch clues moved to a staging profile; the crowded SSH client leaf was split by key-use and client configuration, and an unreferenced sentinel removed; a main-name path reference and an unbound PKGBUILD noextract/invocation pair moved to path and staging evidence, and the former runner composite now also requires an execution observation; the crowded desktop-opener leaf was separated from URI dispatch, HTML Help navigation, and downloaded-file opening; variable-target and application-name observations no longer assert a browser URL or updater; shell-command evidence was separated into upload, download, chmod, background execution, SSH, URL-opening and source-name subjects, shell-parsing calls were moved from direct process creation, Base64 command output to encoding, and unbound command text and encoded markup clues to their evidence subjects; process-target configuration and thread-pool task operations were separated from thread creation, and the workers leaf retired by distinguishing worker contexts, thread runtime, concurrency settings, queued commands and neutral names; inline-script retired by separating socket clues, interpreter commands and embedded command text; source names and input-field text moved out of process creation, Lua compilation no longer independently counts as invocation, and generic JSON/command clues no longer claim model provenance; Go command construction is separate from launch; fiber creation and callback references moved to fiber management and unbound memory combinations to memory profiles; the legacy process-creation fiber leaf is retired; the native carrier leaf was separated into a Lua CreateProcessW call and launch window configuration, so the flag alone no longer counts as process creation; parent-attribute name references moved to launch configuration and unbound Explorer launch clues to a process profile, without attributing injection to the attribute name alone; local-exec retired by separating command targets, shell interpreter launches, backgrounding, staged execution, subprocess calls and unbound syntax; the directory-wide consumer preserves its previous alternatives, and unsupported exfiltration tags were removed from a nohup observation; remote creation retired by separating WMI command text, named PsExec and Impacket references, and unbound remote-administration profiles; a generic WMIC and admin-share combination no longer asserts hostile intent or a PAN-OS identity; shortcut creation retired by separating configured targets, command clues, window settings, URI references and path observations; target matching requires executable basename boundaries and unbound WScript text no longer claims a target; Start-Process retired by separating PowerShell command invocation, .NET process configuration and launch, named SDK declarations, encoding clues and unbound profiles; the crowded subprocess launch leaf was relieved of shell launches, imports and unbound co-occurrences; the hidden-launch leaf was split by window-option, WMI configuration, serialized evidence and shortcut targets; an optional hidden flag no longer makes a normal PowerShell launch appear hidden, and unrelated tool context no longer suppresses a hidden-window text fact; unbound Go executor constructor and method calls moved to source-call evidence; the child-process API aggregate now describes its name-only alternatives and is no longer suppressed by an unrelated UI marker; Python system-call aliases now pair a matching os import with the observed receiver call instead of inferring os from the receiver name alone; Go Node command constructors moved to subprocess configuration, and unbound Python argv text and JavaScript helper arguments moved to execution evidence profiles; interpreter subprocess calls moved to process creation, including the common Python argument-list form, and their unbound input-name co-occurrences moved to script-evaluation profiles; Node inline commands configured in npm scripts moved to package-script evidence, with unrelated script exclusions removed; Node spawn call observations no longer disappear on test paths or test-related text; an unbound importlib and child-launch pair moved to a script profile, and unrelated test or kernel-source context no longer suppresses these process clues; npm inline Python, shortcut MSHTA arguments and an unbound Python argument fragment moved to package, shortcut and execution profiles; a bare PowerShell background-job call moved to subprocess launch; MSHTA about-document text no longer disappears because another about:blank string occurs and is notable command evidence; Python inline-interpreter list rules now require the interpreter and -c in the first two positions; SSH inline-interpreter commands moved alongside other SSH client commands; Apple-event delay, script-loading, URL-opening, compiler-name and desktop-opener observations moved to their respective subjects; the mixed Apple-event leaf was retired by separating shell and script execution, application control, compilation, collection measurement and neutral profiles; its persistence consumer enumerates the prior evidence; the WSH carrier leaf was retired: loop syntax, command-string text and unbound COM/file clues moved to their subjects, without claiming that generic ReadyState evidence is XMLHTTP; the Gradle carrier leaf was retired by separating generic exec blocks and names, calculator configuration and shell command text; unbound calculator or encoded PowerShell clues no longer claim a build-system exploit; script automation was separated into browser evaluation, launch and profile-copy behaviors, a named Playwright import, System Events application targeting and generic JXA/CDP evidence; the automation carrier leaf is retired; the osascript carrier was separated into interpreter commands and input, application targeting, module loading, delay, deletion and supporting script or shell evidence; the remaining script-file carrier was separated into command invocation, in-process sourcing, backgrounding, script paths, package configuration and unbound evidence, retiring the script creation parent; the shell script-host and package carrier leaves were retired by separating process commands, interpreter and library evidence, package execution and configuration, and unbound profiles; the input-source leaf was retired by moving partial Finger command-loop evidence to the Finger channel; the shell spawn bucket was retired by separating process creation, replacement, interpreter launches, paths and command-text evidence; the shell script-file carrier was retired by separating interpreter launches from direct path execution; the shell request bucket was retired by separating interpreter and constructed-command behavior from webshell and remote-command objectives; the native shell carrier was retired by separating imports, process replacement, command calls, macro definitions and profiles; the shell stdin-feed carrier was consolidated into interpreter input, with network and calendar payload behavior kept in objectives; the remaining shell launch bucket was separated into interpreter and replacement operations, command text and supporting profiles; package lifecycle and task command pipeline declarations moved from shell pipelines to their configuration subjects, with path-based dependency suppression removed; the subprocess request and package carriers were retired: request-fed execution moved to subprocess launch, and unbound subprocess launch clues moved to profiles; an exec-named call with a module-relative path became a process profile and its consumers no longer claim a bundled cross-platform payload; generic Run syntax, encoded text fragments and unbound hidden-window options moved out of process creation into supporting profiles; MSHTA command text and an osascript/curl co-occurrence moved out of inline process evaluation; neighboring command observations were separated by subject; interactive-shell review moved execl to process replacement, generic cmd proc_open to subprocess launch, and pickle text to a process profile; shell command-string review separated AppleScript import and text references and a JXA symbol from executed calls, and Go PowerShell construction from process launch; variable command review separated shell command-position calls from positional-function and batch substitution text; clone syscalls with unresolved flags moved to their syscall operation and fork/clone symbol names to symbol metadata; an Xcode build-setting pipeline and fetch/nohup command text moved to their configuration and execution-evidence subjects; default-opener review moved a direct fodhelper path launch and unbound command or method text to their respective subjects; background output-discard moved to daemonization and unbound hidden-PowerShell clues to profiles, without large-file or signature suppression; explicit relative, temporary and home executable paths consolidated under path execution, with unrelated context and filename suppressions removed; shell-interpreter review separated generic command text, serialized text and unbound run calls from launches, removing unrelated text suppressions; HTTP-client pipeline syntax, illustrative pipeline text and JVM string observations were separated from shell execution; cross-interpreter curl pipeline text moved to syntax, and independent stdin/installer clues moved to profiles; process-API review moved named shell commands, explicit paths and browser-control calls to their mechanisms, removing unrelated log suppressions; download-to-interpreter command syntax is grouped by operation separately from executed shell lines; inline Ruby socket/process clues and an ELF-embedded urllib command moved from process creation to supporting profiles; unbound hidden-window settings and source or option co-occurrences moved to configuration and profiles; fork and clone syscall evidence was separated, and Ruby fork string references moved to a profile; mixed desktop-opener API and encoded-string clues moved to open-handler profiles while direct calls remain behaviors; unbound macOS opener background options and xdg-open command text likewise remain opener observations; shortcut PowerShell, ordinal, nested-link and network-share arguments moved to their argument subjects without implying activation; temporary-path execution, shell variable-command execution, and batch background commands moved to their more precise mechanisms; batch executable and temporary-directory launches consolidated with path execution; direct Windows tool and kubectl calls moved to image execution, JVM cmd to subprocess launch, and shell PHP invocation to interpreter launch; WScript Shell Run clues grouped by launch mechanism, with the unknown bracketed method retained as a supporting call observation; Windows command-mode launches, delete command text, and constructed ping command bytes separated by operation; Start-Process and saps launch clues grouped by that mechanism; XMRig invocation moved to mining behavior, tar checkpoint commands and Lua launches to their execution mechanisms, and shortcut call-operator text to shortcut evidence; remaining command rules separated into path or variable launches, root-directory change, shell command mode, and launch or automation evidence; computed executable targets separated from fixed executable paths, preserving both former directory consumers; Desktop Entry and Compose shell targets moved to launch configuration, lifecycle hook text to package scripts, and Explorer document or image command clues to open-handler evidence; crowded package lifecycle evidence separated by installation, discovery, and network subjects; credential path evidence split into developer stores and home-bound store paths; source-build installation separated from package-script declarations and installer namespace, diagnostic and argument observations; install-hook calculator execution evidence moved to the lifecycle execution objective, retaining the distinction between bound calls and co-occurrence; runtime-install option and helper-name observations separated from actual installation; declaration names separated into enum members and control-flow labels, without inferring Protobuf from generic enum syntax; country-code evidence separated from translation catalogs and general locale observations; bound process detachment, hidden-window options, mining options and generic tuning flags separated from command-option profiles; credential, cryptographic-key and personal-data property reads separated from generic property access; repetition and command-handler names separated from generic runtime naming, without treating those names as proof of a loop or remote agent; Android permission requests, idle-limit exemptions, accessibility setup, scope changes and elevation failure messages separated from privilege elevation; inline Python, Perl and Node interpreter commands consolidated under interpreter-command; process/create/eval retired, with interpreter commands and staged-source reuse grouped by input operation; variable batch commands, PHP relative-path launches and scoped package installation separated from generic shell-command execution; Python curl process and shell stdin clues separated from their combined pipeline evidence; interpreter launch and variable-target clues separated from shell command-mode evidence; Start-Process temporary paths, variable targets and hidden-window launches grouped by their more specific behavior; shell command-mode, process replacement, background launch and inline Perl evidence separated from generic shell execution; Node npx and Python interpreter launches grouped with their subjects, preserving process-directory consumers; Node Lua launch and extconf build delegation likewise moved to their subjects; Python subprocess targets separated into interpreter, stdin, JAR and curl command subjects; touch invocation, variable PHP command and decoded or forwarded argv separated by operation; Telegram session, Android account, temporary hive and configuration URL references moved to their subjects, and shadow-file sync registration to credential collection; printed curl-to-shell guidance and related process-reference facts moved to their script-content subjects; platform-selected and request-supplied executable targets moved to variable process creation, and interpolated shell commands to variable shell execution; Netcat shell command evidence moved to remote-command and request-bound ColdFusion cmd execution to webshell, without asserting connect versus listen for Netcat; explicit shell -c and cmd /c invocations grouped under command-mode; interactive shell descriptor-redirection evidence grouped with remote shell control without asserting a socket or connection direction; PowerShell DNS TXT capture and evaluation clues moved to DNS tasking; the exec leaf was reduced from 87 to 69 rules by separating API-name references, relaunch evidence, runtime and co-occurrence observations; directory consumers retain applicable moved members; subprocess launch was reduced from 79 to 69 rules by moving method references and unbound sparse-binary observations to their evidence subjects, with applicable directory consumers preserved; kernel usermode-helper symbol-only evidence → binary symbol metadata, while process-creation consumers require the call trait; the child-process API aggregate is component evidence, not an independent launch claim; remaining branches need selective claim review) |
| mb `process/interpreter/reflection` | mb `metaprogramming/reflection` | Code as code | Applied |
| mb `process/script` | The actual execution mechanism (`process/interpreter/wsh` for WSH) | A carrier is not a mechanism | Applied |
| mb `os/env/{enumeration,dump}`, `modify`, `{check,gate}`, `user-paths` | mb `os/env/{enumerate,write,test,path}` | Other topic leaves move to the subject they require | Applied (all six named legacy environment-operation directories are empty; further topic review is selective) |
| mb `os/registry/access` (mixed historical cohort) | Registry operations and key subjects; host discovery, certificate stores, imports and evidence metadata | Keep neutral access only where no narrower operation or subject is supported | Applied (historical access rules separated by claim; generic write-or-delete compatibility group replaced by write evidence, dump-filter clearing includes emptying and deletion without treating both as writes, and the remaining multi-operation co-occurrence moved to registry key lifecycle behavior) |
| mb `os/registry/manipulate` (retire) | Registry read, write, delete, key and hive operations; subject-specific persistence; metadata for names and co-occurrences | Classify by supported operation or outcome; do not treat generic setters as registry-specific without context | Applied (69 legacy rules reviewed; redundant API alias retired, Winlogon persistence and key-specific operations moved, and a set/delete co-occurrence no longer suppresses Run-key evidence as a presumed uninstaller) |
| mb `os/service/driver` | mb `os/kernel/driver` | Drivers are not services | Applied |
| mb `dylib/library`, `ui/framework` | meta, a capability, or `well-known/lib`, by claim | Implementation containers | Applied (`usb_init` export → `metadata/binary/symbols/exports`; libm imports → `metadata/binary/symbols/imports` ([inventory](docs/taxonomy-audit/taxonomy/libm-imports/migration.json)); terminal-editor project/version text → `metadata/binary/provenance/build`; TLS library names → `fs/path/library` ([inventory](docs/taxonomy-audit/taxonomy/tls-library-names/migration.json)); MFC42 name → `fs/path/library` and all three MFC API names → `metadata/binary/symbols/name/token` ([inventory](docs/taxonomy-audit/taxonomy/mfc-references/migration.json)); `ui/framework` has no YAML rules or live YAML references; both dylib/library and ui/framework are empty; remaining library observations are a selective subject review) |
| obj `command-and-control/dropper/{process-inject,image-map,module-load,script-eval,interpreter-stdin,file-exec}` | obj `execution/payload/<sink>` (admitted) or mb `process/deploy/<sink>` (neutral) | By sink; admission picks the tier | Applied (No active YAML rules remain in the legacy dropper tree; `file-exec` applied in command, detached, installer, shellcode and spawn categories, including `spawn/fetch`; the legacy directory is removed; image-map applied: call-bound RC4 mapping → payload/image-map, independent crypto, HTTP and memory evidence → operation-cooccurrence profiles; interpreter-stdin applied: impersonated postinstall → payload sink, archived preinstall pipelines → neutral deploy, unbound combinations → profiles; module-load partial: unbound .NET, Node, JVM and MSI combinations → profiles, Netz source references → tool-reference, batch and other admitted loaders → activation sinks, and generic fragments → their encoded, syntax and operation subjects; the final MSBuild rules → build facts, proxy execution, process injection and module activation, retiring the legacy module-load subtree; script-eval partial: detached interpreter input, scheduled execution, polling control, response and function-constructor chains, and neutral remote-source observations moved by subject, retiring remote-code; response-pipeline atoms, execution chains and supporting clues moved by subject, retiring that subtree; response-eval batch, Node module-response, HTTP, wrapper, shell and Python rules moved by execution sink, capability or evidence profile, retiring the response-eval subtree; embedded file-range, decoded command, encrypted runtime and remaining JavaScript and PowerShell chains moved by sink or evidence subject, retiring the legacy script-eval subtree; blockchain-derived source moved to its dedicated sink and transformed evaluation divided by activation; browser navigation and command dispatch split by operation and tasking channel, and Base64 encoding split by input/output behavior; binder source calls, overlay and VB6 URL observations moved to capabilities or profiles, VB6 write/launch chains to execution sinks, and remaining VB6 text and system-management clues to their subjects, retiring binder; mixed-encoding shell execution, XOR network diagnostics and retry clues moved by claim, retiring obfuscated and empty misc; PowerShell Node/Python bootstrap rules split into hidden launch, encoded observations and construction profiles; Node bootstrap components moved to path, identifier, archive, process and interpreter subjects, with final findings routed by execution, persistence or supporting evidence, retiring node-bootstrap; update/install capability, generic paths and commands, and Rifle-specific clues moved by subject, retiring fake-update; cabinet payload findings split into archive content, lure, masquerade and download subjects, retiring cabinet-payload; PyInstaller, MSBuild, C++/Rust build and VBA macro builder rules split by product, compilation, source evidence and trigger; C and Go concealment-builder evidence, dnlib and BuildInfo observations, generic task paths, .NET placeholder and crypter findings, and Python construction, encoding and panel clues moved by claim, retiring builder; MSI delivery split into installer execution, installation and cryptography profiles, tool identity and registry-path evidence; unsupported signing and banker attribution removed, and Kinsing reference profiles separated from the crowded tool-reference directory; document RTF and XLM obfuscation and RAR member profiles moved by evidence, with unsupported CVE and traversal claims corrected; VBA document payload, macro evidence, persistence and WMI behaviors moved by claim; browser-control launches separated from script-host downloads; the remaining document-delivery rules split into path, scheme, encoded text, embedded-document, execution, staging and evidence profiles, retiring the document subtree; oversized document-interpreter rules split by execution surface; HTTP delivery split into network-backed evaluation, acquisition, propagation, operator infrastructure, family identity and neutral evidence, retiring its subtree; temporary artifact paths and subject-specific function names separated from crowded neighbors; fetch-exec shell and direct-IP rules and their existing neighbors split into executable-permission and other fetch-and-launch sinks; remaining fetch-exec rules split among network evaluation, file launch, quarantine bypass, package hooks and supporting evidence, retiring the fetch-exec subtree; download rules split into installer invocation, family markers, network/PE profiles, Flash and Android observations, and blockchain-backed execution; unsupported family and execution claims corrected; remaining Android, shell and JavaScript download rules moved to installer, execution, capability or evidence subjects, retiring the download subtree; curl split into command, request-body and library-binding children while preserving parent selectors; HTML macro lures, page observations, browser-download and remote-script evidence moved by claim; help guidance split by subject while preserving recursive downgrade scope; HTML carrier and activation rules split among markup and script profiles, execution sinks, payload concealment and product-specific evidence; ScreenConnect installer and client evidence separated; the remaining HTML drive-by rules split into browser download behavior, encoded browser payload delivery and supporting evidence profiles, retiring the HTML subtree; ClickFix browser-cache rules split into operation and path observations, cache or profile execution sinks, and clipboard delivery, retiring that leaf; ClickFix remote-command rules split into acquisition and execution, clipboard delivery, registry persistence, and supporting command, path and evidence profiles, retiring that leaf; ClickFix shell and clipboard rules split by LaunchAgent persistence, interpreter operation, network execution, verification and command lure, product URLs, URL queries and supporting evidence, retiring the ClickFix delivery subtree; execute-download device, archive and installer rules split by execution, persistence, acquisition, product identity and supporting evidence, retiring those leaves; batch, WSH, Lua, MSIX, Node and PHP script rules split by execution sink, staging, persistence and observed evidence; HTTP CLI download rules grouped by command family, preserving parent references; remaining script rules split into autoloaded execution, remote-share and interpreter sinks, agent instructions, product evidence and supporting observations, retiring the script leaf; execute-download file rules split into CI staging, native execution, WSH, injection, indicator removal, package payloads, named family indicators and supporting evidence, retiring the file leaf and execute-download parent; sideload rules split into product identity, DLL proxy masquerade, process injection, import concealment and supporting profiles, retiring the sideload subtree; downloader rules split among HTTP tasking, persistence, self-deletion, execution and supporting observations; Python encoded-command fragments and combinations moved to encoding, process profiles, evaluation sinks and install-time behavior; the remaining Python downloader rules moved by acquisition, execution and import-time intent, retiring its directory; network download-and-launch split by activation target, with archive-backed chains routed to spawn/archive; package configuration split by subject; other dropper branches remain) |
| obj `command-and-control/dropper/staging/*`, `staging-xor`, `staged-loader` | obj `execution/staging/{reconstruct,extract,acquire,store}` | By operation | Applied (No active YAML rules remain in the legacy dropper tree; its tracked historical backup was preserved under `docs/taxonomy-audit/retired-rule-backups`; `staging-xor`, `staging/archive`, `staging/installer`, `staging/nsis-installer`, `staging/self-extracting`, `staging/signed-nsis-bundle`, `staging/signed-bundle`, `staging/memory`, `staging/encrypted`, `staging/native`, `staging/encoded/script`, `staging/encoded/environment`, `staging/encoded/carrier`, `staging/file`, `staging/http`, `staging/interpreter-stage`, `staging/compressed`, `staging/disk`, `staging/image-disk`, `staging/image-map`, `staging/managed`, `staging/public-folder`, `staging/packing`, `staging/resource`, `staging/runtime`, `staging/script`, `staging/steganography`, `staging/stub`, `staging/temp`, `staging/tiny-pe` and `staging/zip-stage` reviewed and removed; encrypted staging retired by moving reconstruction, cryptography, naming, path, evaluation and evasion observations to their subjects; native payload staging retired by moving ELF and JNI observations to profiles, syscall replacement and hollowing to execution sinks, and EXE/DLL download clues to acquisition; Go/Rust embedded-ELF, Mach-O and GUI observations moved to profiles, editor activation to the fetch-and-spawn sink, and a filename to its path subject; surrogate product-name, embedded-PE and COM observations moved to product references and profiles, with the explicit Active Setup hijack retained as persistence; Access Bridge, MavInject, resource-name, hex/API and PowerShell observations moved to profiles, and dead ratio/product-pair placeholders reviewed; custom-alphabet/cryptography/command and RC4/Rundll32/anti-analysis combinations moved to cryptography profiles without asserting a payload chain; zero-buffer and .NET cryptography observations moved to AES mode and cryptography profiles without assuming decryption or execution; encrypted and obfuscated Android core moved to archive packing, Hashcat path to well-known, MinGW XOR/API clues to PE profiles and ZEROCRYP text/overlay clues to their subjects; BNDL/ChaCha and endpoint observations moved to archive profiles while the temp-file launch chain remains under its execution sink; source XOR/memory and RC4/resource combinations moved to profiles, with thread hijacking retained as an injection objective, and HackSkills documentation moved to well-known; passworded-archive download, signing, attributes and Apple-style paths moved to acquisition, archive profiles, explicit quarantine bypass and masquerade, and VS Code timing/CI references moved to well-known; Windows overlay and API combinations moved to overlay profiles and the Canonical claim to vendor masquerade; CLR configuration and overlay evidence and the Strictor resource signature moved to subject profiles, with a filename suppression removed and a redundant Pack-v3 stage retired; AES/CNG filename and API clues moved to path and PE profiles, timer callback and Defender exclusion to evasion objectives, and the neighboring Defender category split by action; PowerShell data locale, HTTP, indexed invocation, layered encoding and image steganography evidence moved to their subjects, with nearby string categories split by reconstruction mechanism; nearby version-resource claims split Microsoft and Windows component identities into a dedicated sibling, and diagnostic utilities from other Microsoft utility claims; batch carrier and WSH fragments, temporary-script and native temporary-file clues, managed names, security and network-reflection profiles, resource API profiles, PyInstaller bundle observations, Lua propagation and implant identifier clues, PHP percent-u encoding shapes, JavaScript and JCL source clues, DLL exports, GitLab URLs, archive layouts, Windows archive URL and path observations, Android asset profiles, financial and registry profiles, restored WinHTTP and cleanup evidence, Node archive-extraction references, archive-name and Google Drive text profiles, decoded PowerShell batch actions, and Go, Lua, VB and .NET file-write, resource, reflection and encoding references, and runtime-based acquisition, evaluation and file-execution chains moved to their subjects; the remaining stager rules moved by activation, syscall, binary profile and configuration evidence, retiring the staging subtree; remaining staged-loader rules moved to their manifest, identifier, profile, module-loading and memory-branch subjects, retiring that subtree as well) |
| obj `command-and-control/dropper/*` (`delivery`, `execution`, `behavior` and the rest) | A payload sink, staging operation, C2 result or neutral capability | By claim | Applied (No active YAML rules remain in the legacy dropper tree; the `compat` leaf held only synthetic missing-rule sentinels; those and their dead ComfyUI consumer were removed; AppData, editor-bootstrap, character-reconstruction, Elex, lifecycle, Bun, MPRESS, licensing and npm CLI rules moved by action, evidence or family identity; an impossible proxy-loader composite was removed and overlapping MPRESS alternatives merged; fragmented WSH and Python-script rules moved to literal evidence, execution and subject profiles, with script-oriented Run-key registrations split into registry-script; standalone runtime rules moved by execution and evidence, with AppData, environment-read, runtime-platform and adjacent crowded neighborhoods split by subject; string concatenation and executable-mode neighbors split by operation and target; remaining branches need review) |
| obj `collection/email-harvest` | obj `collection/email` | Rename | Applied (legacy directory and references are absent) |
| obj `credential-access/windows-registry` | obj `credential-access/registry` | Rename | Applied |
| obj `credential-access/{dump,theft,validation}` | obj `credential-access/<source or acquisition>` (`memory`, `files`, `credential-manager`, `capture`, `validation`, …) | Dump is not memory; source and acquisition distinguish below the approved families | Applied (process and image dumps → memory; other leaves routed by source/acquisition; the reintroduced theft/authentication keyword leaf was separated into credential wording, token shape, field access and serialization, account paths, and a credential-theft composite; a later reintroduced 2FA literal moved to credential wording) |
| obj `evasion/process/injection` (mechanics only) | mb `process/inject/<mechanism>`, payload execution, or a supporting profile | Rules showing concealment stay | Applied (APC and section-map execution moved to payload injection, in-process image mapping moved to its sink, version-proxy evidence to DLL masquerade, and kernel and atom/APC combinations split by supported evidence; all 129 rules from hollowing/process, hollowing/runtime and hollowing/source moved to payload process-inject/hollowing/{process,runtime,source}; explicit JavaScript, Go Unix, source-level, Go native, ROR13, encrypted-export and TEA shellcode activation moved to payload/memory-branch/shellcode; shellcode exploit payloads divided by browser carrier, syscall command and privilege behavior, parasitic replacement, PE-loader behavior, and Wasm; generic shellcode wording moved to payload vocabulary; Python host names and API co-occurrence without an invocation moved to process-injection profiles at suspicious criticality; API-name, path and loader markers were moved by evidence; the legacy injection tree and live rule references are absent) |
| obj `lateral-movement/social-engineering/spam` | obj `impact/spam` | An impact | Applied |
| obj `lateral-movement/delivery` | The remote operation, execution, propagation, or update-abuse subject | By required behavior and evidence | Applied (no YAML rules or live references remain; WMI, GPO, update-service and remote-execution indicators moved by claim. WSUS and SCCM abuse moved to supply-chain update-service; neutral WMI, PsExec and quiet remote-process observations moved to process creation. SMB credential spraying, self-copy and protocol/path evidence were separated during the neighboring review.) |
| obj `exfiltration/stealer/{network-config,process-list}` | obj `stealer/system-info/{network,process}` | Same source | Applied (legacy directories absent; target branches populated) |
| obj `exfiltration/stealer/{surveillance,phish}` | obj `stealer/<item>` or the supported neutral/local-acquisition observation | Purpose and method are not stolen item types | Item review applied |
| obj `exfiltration/sensitive-data` (retire) | `collection` or `credential-access` (no send), `stealer/<item>` (chain), `side-channel` (leaking oracle), mb `data/serialize` or metadata (partial evidence) | By evidenced result | Applied (browser, automation and source rules reviewed; CSS oracles → side-channel; partial observations → their subjects; no legacy YAML rules or live references remain) |
| obj `supply-chain/{install-hook,recon-exfil,credential-theft}` (retired) | Credential access, exfiltration, discovery or execution by required result; preserve installation-trust context as evidence | A trigger alone is not an objective; misuse of installation trust is | Applied (install-hook/scripts retired; generic registry clues separated from package configuration; synthetic QNX package and Java runtime/profile clusters removed; package-manager retired: alias, hook, source-name, beacon, opkg, RouterOS and path observations moved by behavior without unsupported platform or intent claims; hook-only review separated webhook, package download, manifest and defacement evidence; unofficial SDK descriptions no longer imply a typosquat or empty export; Python .pth Bun sidecar execution moved to package-triggered execution, with its Bun release, sidecar path and call-text clues separated by subject; Bun bootstrap retired: npm release references, executable lookup, sidecar names, module imports and setup-script declarations separated by subject, with runtime provisioning and package-triggered execution moved to their behaviors; remote-config retired: YAML-write clues and obfuscated postinstall module loading moved to their respective behaviors; library retired: import-time PATH and encrypted-evaluation clues, Ruby process launch and installer evidence moved by subject; init and shortcut retired: initializer download clues, shortcut modification and package-triggered shortcut creation separated by behavior; agent retired: agent permission staging, configuration writes and documented thread clues moved by subject; database and system-path retired: MongoDB write and system-bin symlink clues moved to their behaviors; credential retired: credential access, exfiltration, URL and environment observations, and account-seeding clues separated by subject; account creation split by application, device, cloud and system, and a bcrypt salt prefix no longer claims a known password; remote-binary retired: generic staging evidence moved to its subjects, install-time execution to package triggers, registry redirection to package-manager abuse and historical host clues to dependency source; the release-installer exception now requires digest-source comparison clues; setup retired: encoded execution, socket dispatch, HTTP, file collection, MSI argument and Run-key clues moved by behavior; product-specific Clawdbot and Cloudrouter update instructions moved to their tool identities; Bun and Git-hook dropper leaves retired: dependency setup, package entrypoints and repository-triggered remote shell clues moved by behavior; AST dropper leaf retired: module imports, file moves, Git staging and source-name observations moved by subject; Windows-target, WSL and token-loader clues moved to package-triggered execution and network module loading; Windows-loader leaf retired: path, HTTP route, XOR, staging and hidden Python execution clues separated by subject; skill-agent retired: generic skill installation, workflow and template-script clues moved to their behaviors; archive-wide global-scope text no longer suppresses postinstall skill evidence; Rust build and Python setup native staging clues moved by subject; npm native-loader install-command, addon-loading and archive executable clues moved by subject, co-occurrence no longer claims a native launch, and a redundant remote-shell composite requiring an unrelated Node script was removed; native-loader retired: package-triggered execution, credential-store clues, rootkit hiding, insecure staging and Tor references moved to their subjects; the generic Tor reference and credential-store clues no longer claim a hostile implant, and a script-count gate no longer pretends to prove native code; hook-setup batch ML names and ordinary Python command moved to neutral profiles and process evidence, with fake-setup claims removed; cleartext archive, elevation, host exfiltration and Python retrieval clues moved by subject; PyPI setup path, command, package, environment, prompt and decoding observations moved to their subjects; ordinary progress text and Python-named download domains no longer claim deception, and test paths no longer suppress COMPUTERNAME or encoded-array evidence; PyPI setup persistence, dependency installation, shortcut, execution and staging composites moved by behavior; generic COM shortcut and executable suffix clues no longer claim browser-extension deployment or an extension mismatch; scanner-label context no longer suppresses Python input-library installation evidence; hook-setup retired: encoded PowerShell, install-triggered execution, privilege checks, dependency setup and path or network clues moved by subject; generic directory creation, webhook references and shell-init paths no longer claim payload delivery or persistence; obfuscation dropper leaf retired: XOR and arithmetic decoding, computed imports, self-deletion, obfuscated HTTP and remote-file opening moved by behavior; Solana fragments and install-like names no longer claim a dead-drop loader, and scanner or test-file context no longer suppresses the affected decoder evidence; runtime download, Node stdin, proxy, warning suppression, package checks and network-evaluation clues moved by subject; generic stdin, proxy and header references no longer claim a beacon or code execution, and test paths no longer suppress fetch/decrypt evidence; runtime retired: masked registry installs, encoded execution, process launch and cache staging moved by subject; rtcli command text no longer claims a hidden launch, and unrelated API options no longer identify rtcli; custom setup leaf retired: environment checks, credential and host exfiltration, webhook posts and request/process clues moved by subject; duplicate hostname and unreachable HTTP matchers removed; GitHub PATH, Composer and native download branches moved by behavior, while uppercase module archives with Hermit no longer imply an attack; shell dropper leaf retired: Termux downloads, heredoc and encoded-header clues, filesystem tests, system paths and sidecar execution moved by subject; generic paths and encoded prefixes no longer claim a bot or payload, and unnecessary size filters and scanner or installer exclusions were removed; the install-hook/dropper tree has no YAML or live references; the final MSBuild install-hook rules moved alongside NuGet hostname exfiltration, retiring the install-hook tree; all three legacy trees have no YAML rules or live YAML references) |
| obj `supply-chain/metadata-anomaly` (retire) | Package and patch metadata, destructive behavior, or masquerade by claim | Package irregularities alone do not establish a supply-chain compromise | Applied (the legacy directory and its live YAML references are absent) |
| obj `anti-static/obfuscation/{binary-metrics,code-metrics,tools,multi-layer}` | meta `binary` or `file`, `well-known/`, or a named concealment | Measurements and identities are not concealment | Applied (function-size and digit-heavy XOR line observations moved to file profiles; VS Code and QuickLook markers moved to their subjects; function and identifier populations, text distributions, generated-code and runtime references, PHP array, Unicode and image observations, long-line execution profiles, and Lua/JavaScript source and evaluation evidence, shell source and execution clues, and native immediate arithmetic moved to their subjects; unreferenced recognized-context components retired; code-metrics is empty; MinGW, import/export, sparse-import, section-name, overlay, complexity and selected binary-shape observations moved to binary profiles, with section and symbol names split by subject; binary-metrics is empty after routing layout, signature, API-resolution and packing evidence by claim; XOR/Base64 wording, PHP and Java source profiles, shell encoding and reconstruction, Ruby decode/evaluation, a remote-script objective, macOS shell/section profiles and HTML constructor execution moved by evidence; Python escaped-name and reflection clues, XOR techniques, marshal reconstruction and decoded-evaluation chains moved by evidence and operation; JavaScript shard/decoder and SVG clues, plus PowerShell transformed-evaluation, assembly activation, injection and construction profiles, moved by evidence and operation; VBScript fragments, encoded references, layered concealment and execution or evidence profiles moved by their claims, retiring multi-layer; tools is absent with no live YAML references) |
| meta `file/encoded`; `lang/encoded` | meta `file/encoding`; `lang/encoding` | Rename, then group by encoding scheme or measured shape | Applied; orphaned impossible XOR/Base64 co-occurrence composite removed |
| meta whole-file byte-entropy rules under `image/*` | meta `file/entropy` | Decoded-image measurements stay | Applied (no whole-file byte-entropy rules remain; decoded-image measurements stay under `image`) |
| meta `file/{string,literal}/*` | The subject each string evidences; context-only predicates held pending validated representation | No definitions remain; reintroduction is rejected | Applied (batches 047–080; the process-name leaf moved to named product and OS identities, generic service-name references and updater filename observations; an adjacent updater name rule joined the same updater-path sibling; device strings split into industrial and generic vocabulary, a keyword-cluster profile, USB identity and VirtualBox references, with physical and action vocabulary separated from the crowded content-word leaf; account labels and record-field co-occurrences moved to naming and field-presence subjects; artifact strings split into license, lexical and member-reference observations without asserting a Vagrant identity; file strings split into document and credential suffixes, names, paths, vocabulary, file-read context and .NET identity, with document and filetype-list evidence also separated from the crowded extension leaf; telemetry and security strings split into vocabulary, system fields, supporting profiles, logging symbols and YARA-X references; browser and macOS settings names moved to identity, vendor, path and text subjects, preserving broad Internet Explorer exclusions; activation-tool identity and its existing exception moved to well-known, with generic KMS, Safe Mode and Defender text separated by subject; Unix star references moved to the tool and netstat usage/source references to neutral tool evidence; remaining utility names, filename facts and token-count context moved by subject, retiring the application-name leaf; container, graphics, credential, attribution, hashed-record, string-count and upgrade-text leaves split by their observed subjects; all remaining file/literal and charset rules moved to alphabet, hex, syntax, numeric-array, terminology and observed-text subjects; the final identity strings moved by subject and both closed legacy trees are absent) |
| meta `lang/source/literal/value/*` | `lang/source/literal/{string,integer,hex,array}`, the evidenced subject, or `well-known/` | Review matcher and provenance before choosing a type or identity | Applied (generic string shapes, constructor-path, config-metacharacter and touch-point strings, ambiguous single-word literals, C# Path/CRLF, generic Go/protocol and appendChild/src/forward strings, and six hex observations moved; comma-delimited numeric text → text-shape; Git hook-name fragments → VCS path references, compiled-model and injection-related wording → natural phrasing, CAFEBABE text → hex; Testing Library scope text → package-reference component, with a bounded package-specifier observation outside recursive identity exclusions; Python bytecode reader-name and registry-route fragments moved to their subjects; quoted host terms → system-info field-name references; Android action strings → literal/string; model and port-scan vocabulary → natural-language vocabulary; exact git literal → tool-reference profile; encoded method names → `lang/encoding/base64`; datetime call → `lang/source/syntax/call/invocation`; shortcut glob → `fs/path/glob`; quoted code, generic tokens and shell tilde literal → `lang/source/literal/string`, bare numeric and versioned archive text → `file/profile/text-shape`, Python marshal name records → `binary/code/bytecode`; quoted wallet RPC fragments → component literals, with unbound fragment/selector/rotation combinations → notable cryptography profiles; task literal, quoted labels and unbound filename/status text → their literal or text-shape subjects; package and module references → import metadata, Codex name text → source naming, HTTP references → their metadata subjects; remaining encoding, wording, syntax, module-reference and text-shape observations moved by claim; no legacy YAML rules or live YAML references remain) |
| meta `file/data-blob/*` | The specific measured property or behavior-supported subject | No residual `data-blob` bucket; split entropy, region, signature, name, and string observations | Applied (14 rules moved to entropy, byte-prefix, filename, path, string-population and text-shape homes; no legacy YAML rules or live YAML references remain) |
| meta `file/policy/*` | `permission`, `hardening`, `package`, or document/format-specific property | No generic policy bucket; preserve declared-versus-effective scope | Applied (research-canary disclosure wording → natural-language phrasing ([inventory](docs/taxonomy-audit/taxonomy/research-canary/migration.json)); C initializer shape → source syntax ([inventory](docs/taxonomy-audit/taxonomy/c-initializer/migration.json)); mobile-link setting names → source naming; Google-services filenames and symbols → path and source naming, with co-occurrence → mobile-config profile; Android manifest, build plugin and field names → their subjects, with unbound combinations → mobile-config profile; mobile branding and white-label names → paths, source naming, package keywords and product identity, with co-occurrence → mobile-config profile; Xcode project, scheme, symbol and command references → their subjects, with co-occurrence → mobile-config profile and the former broad suppressors narrowed to a named tool context; AppArmor include directive → file format; AWS and Socket scanner field text → config syntax; Socket config basename/schema reference → tool-reference profile; Windows policy exception → the suppressed objective; systemd path, ExecStart fields and unit layout → path, service unit fields and service format respectively; uppercase config/key token shapes → file text-shape; agent tool wildcard syntax and settings path → call arguments and agent-config path, with unbound co-occurrence → agent-config profile; security-document wording and defense contexts → documentation policy, structured guardrail response → text shape, with the former directory-wide exception narrowed to defense contexts and a structured block response; agent approval policy wording → documentation policy, block message → diagnostic, safety-setting text → text-shape; no legacy YAML or live YAML references remain) |
| meta `file/function/*` | Source declaration/name; population profile; `binary` anatomy | A name does not prove invocation or behavior | Applied (selected source declarations and function names moved, including Java sendRequest, Go IsDLL, shell callable identities, managed method-name text, JVM callback names, Java method names and signature text, Go probe names and decrypt-named declarations; Go-style strings in compiled files → binary name text; function populations → `lang/source/function`; AST node counts → `lang/source/shape`; JVM method-reference counts → `binary/symbols/count`; JavaScript decrypt-named symbol → source naming, Ruby audit text → declaration syntax, document function-like text → text-shape; Java method symbols → function naming, Python bytecode name → bytecode metadata, binary helper text → binary name text, and VBA/getuid declaration-like text → text-shape; PHP function-length metric → function-population, parsed-call count → syntax-tree, and unbound transform, locator and spoof-name text → text-shape; remaining function-name and symbol observations → source naming; no legacy YAML rules or live YAML references remain) |
| meta `file/{arithmetic,padding}/*` | Parsed operator population, actual arithmetic operation, observed filler span, or a measured text-shape profile | Separate source-shape measurements from operation claims | Applied (`file/arithmetic` retired; digit and whitespace ratios and line shapes moved; leading whitespace moved to `file/profile/text-shape`; the uncontextualized `PADDINGXXPADDING` token moved to `file/profile/token-shape`, without claiming an observed filler span) |
| meta `package/tooling`, `hardening/missing` | `build/*`, `well-known/*`, `package/<subject>`; the mitigation's own subject | Grab-bag and judgment names | Applied (`hardening/missing` held four unreferenced aliases of ELF linking facts; those facts remain under `binary/linking/runtime`; Netris and HAL evidence moved to `well-known/`; no legacy tooling rules or live YAML references remain) |
| meta `binary/{installer,framework,vendor,signing,license,toolchain}` | `well-known/`, `vendor`, `signed`, `binary/provenance`, `lang/compiler` | Identity is not a format property | Applied (the Free Software Foundation name reference → `vendor/string`; Python Software Foundation, GitHub and Digital River names moved to vendor string observations after reviewing 57 legacy vendor-directory downgrade consumers; those unverified names no longer trigger those directory-wide downgrades; the remaining Microsoft version claims, Windows product names and verified-system contexts were separated by subject; 57 legacy vendor-directory downgrade uses were reviewed and removed or narrowed to verified Microsoft platform signing, and the legacy vendor directory was retired; Microsoft filenames, certificate-name text, Security Essentials references and Sync Center identities moved to their subjects; the Sync Center identity no longer independently claims malicious behavior; madExcept, API-set description, product-reference and publisher-certificate facts were separated from generic Windows vendor wrappers; service reconfiguration now requires signature verification, and compatibility names no longer suppress export observations; the Apple vendor wrapper was retired after reviewing its directory-wide consumers: bundle identifiers, framework references, project banners and platform signatures remain available independently rather than broadly downgrading unrelated behaviors; Adobe company strings and version claims moved to vendor observations; the former installer wrapper no longer treats a company claim as installer identity or suppresses Flash infector rules, and the broad company-field downgrade wrapper was retired; Halide and Hexagon exports moved to their named runtimes; a three-marker Hexagon provenance profile no longer claims a Halide simulator based on generic toolchain evidence; NVIDIA NVAPI claims and Qualcomm XBL markers moved to product subjects, while CUDA section names, CDSP tree strings and ADSP filenames remain observations; firmware markers no longer suppress factual complexity measurements; Bitdefender, Wine and ReactOS markers moved to their products; Bitdefender resource names no longer suppress measurements or service behavior, and Wine/ReactOS resource-memory exclusions now require the corresponding API exports; CPUID, HWiNFO and WebView2 product references moved to their named products; an incomplete CPUID catalogue comparison and Realtek/Intel name cooccurrence no longer assert brand confusion, and WebView2 filenames no longer suppress unrelated behavioral profiles; Realtek audio and RealPlayer resource identities moved to their named products, with generic company and updater text separated; the identity-only profiles no longer claim masquerade or Magistr infection; a COM registration export and an absent signature no longer alone claim Realtek masquerade, while the hardcoded-mutex and persistence consumers remain; the broad firmware and embedded-toolchain vendor wrapper was retired: distinct firmware and compiler observations remain at their subjects instead of triggering directory-wide downgrades; ARM firmware symbols are matched as symbols, and the writable-code rule uses the corroborated firmware profile; EDG and GCC frontend identities, SHC generated-runtime evidence and embedded compiler markers were separated from the crowded native compiler directory; a BPF header-byte shape → binary header identity, with a generic fixture-path suppression removed; Xcode field-name text → build-toolchain references, and its former directory-wide suppression → parsed embedded-plist keys; signer-verification profiles → signature metadata, with unsupported overlay timing removed; binary/signing retired by separating CodeDirectory identifier claims, CodeResources structure, plist resource references and icon paths; installer custom-action and reference leaves retired: MSI project-command and INF command templates moved to process creation, INF entrypoint names to package-manager references, and MSI file-table and library text to package metadata; WiX Burn, ALZip and FreeArc SFX indicators moved to their tool identities, with existing archive downgrades preserved through an evidence aggregator; WixSharp MSI contents, action-name references and installer profiles separated by subject, and VSTO and ClickOnce bootstrapper strings and their combined profile moved to installation evidence without asserting a Visual Studio identity; installer/builder retired after Advanced Installer markers moved to product identity, generic helper filenames to filename/MSI observations, and updater and installer-context clues to installation profiles; unsubstantiated forced-update and stager descriptions corrected; installer/plugin retired by separating INetC and Tauri markers, export names, NSIS path and filename evidence, and installer profiles; four impossible database sentinels and their unreachable Cheat Space composite removed; MSI component, property, wrapper and data-name observations moved to installation, office-property and package-file subjects; unsupported persistence, anti-tamper and disabled-control claims corrected; the database-wide downgrade retained its prior evidence during migration; installer/database retired by separating MSI content and script labels, cabinet bytes, product references, execution commands, path observations and installer profiles; incorrect script-execution and payload claims reduced to the evidence, and the extension-only downgrade removed; installer/runtime and embedded-payloads retired: mutex names, resource labels, manifest references, setup-tool identity and managed custom-action clues separated by subject; an embedded executable count corrected to include script streams, and an unsupported Elex family/decoy claim moved to a neutral installer profile; Install4j and IzPack indicators moved to product identities and IExpress directive references to installation evidence; the IzPack manifest matcher corrected and a generic filename-only installer exclusion removed; Inno data and password markers moved to runtime identity while generic encryption-name clues moved to cipher evidence; generic encryption names were removed from the installer suppression context; NSIS product markers moved to tool identity; generic DLL and CRC-option names moved to partial evidence and excluded from installer-wide suppression, as were generic IExpress option names; installer/script retired by separating Inno loader identity, generic ZLB bytes, version-field observations and unrecognized resource-prefix evidence; generic bytes and unknown prefixes no longer trigger installer-wide suppression; crowded PE version-field presence facts split into their own sibling; InstallAware and QSetup SFX evidence moved to product identity; a certificate-table-only SFX profile renamed to avoid claiming a verified signature and removed from broad installer downgrades; installer/sfx retired by separating IExpress/Wextract product identity from generic CABINET, FDI and Advpack references; overlapping exact and substring manifest markers merged so one occurrence cannot count twice; embedded WinRAR module names moved to product references and generic setup, silent, overwrite and destination names to their respective operation evidence; generic embedded content no longer triggers installer-wide downgrade; WinRAR PE self-extractor identity separated from generic dialog, script and overlay evidence; broad archive downgrades now use named self-extractor identities, including verified contexts when available; related installer profiles grouped under one parent to keep the profile level navigable; binary/framework retired: .NET host PDB paths and version claims separated from corroborated runtime and multi-PE profiles; weak host/bundle exclusions removed from AMSI, wallpaper, token-privilege and process-hollowing findings; managed attributes and constructor-name evidence moved to their subjects; .NET reference context now requires corroborated CoreLib evidence or a signed reference-attribute observation instead of a basename alone; CLR entrypoint, metadata and managed-assembly evidence moved to the managed-language subject; over-escaped namespace fallback patterns corrected; VB6 runtime evidence moved to language runtime metadata, and the application profile now requires evidence independent of its runtime DLL reference; Node native-addon registration moved to module behavior; generic register-name shapes require Node ABI corroboration, and Node identity no longer suppresses explicit preload shell chains; MFC, ATL and WTL class references moved to their named libraries, with generic CDialog text separated; the redundant ATL-or-WTL wrapper was removed; Qt runtime name and compatibility-shim API references moved to their subjects; resource language-name labels no longer imply the resource is localized or provide framework-wide downgrade context; generic native-image PDB suffixes separated from System.Diagnostics.Process library references, preventing a generic suffix from claiming that library; .NET distribution artifacts grouped to divide a crowded runtime directory; UPX version bytes and packer text separated from UPX-named executable context; three unreachable downgrade sentinels and version-only exclusions from packed-file detections removed; Java launcher symbols and JSmooth references moved to their runtime and tool identities; generic Java paths and localhost URLs separated, and proxy and export claims reduced to observed symbols; Flutter desktop and embedder references moved to their UI framework; broad framework downgrades use corroborated Flutter context and a low-entropy layout no longer excludes a single DLL-name reference; Unity graphics references moved to the Unity runtime context, and an impossible Electron compatibility sentinel and its ineffective exclusions removed; Windows BITS and Media Player name references moved out of binary/framework, with framework-wide downgrade consumers updated and a .NET detection narrowed to .NET evidence; installer/family retired: Huawei-specific uninstall guide text separated from a generic uninstall namespace; NSIS and certificate combinations no longer claim KanKan or verified authorship; the installer-context aggregator is described as evidence rather than a benign verdict; system product identities grouped by mobile and desktop subject to keep the parent navigable; Steam and Tencent product references moved to their products, while Tencent certificate chain names moved to signature metadata without claiming verified authorship and no longer alone trigger installer suppression; Qt Installer Framework, InstallShield and Squirrel product markers separated from generic source and NuGet archive filenames, which no longer independently trigger installer suppression; Inno/Delphi and crypto-support profiles moved to product context; their import hash is a generic binary observation and no longer alone triggers installer suppression; YingInstall markers moved to product identity; Netman product and company version fields separated, and YingInstall wrapper detection now requires a YingInstall-specific marker; Smart Install Maker name and NSIS header bytes moved to their product references, with the NSIS bytes no longer labeled suspicious; Free IP Switcher and RIP Tweaks version claims moved to their named products; the Eusing company field is separate vendor evidence and no longer triggers the broad installer context; unsupported installer and signer attribution was removed; Embala banner identity moved to its tool identity while generic Lua error text moved to uninstall evidence and no longer triggers broad installer suppression; an installer-product context catalog preserves reviewed product references; installer/archive retired after separating 7-Zip identities from generic compression and uninstaller-name clues; self-extractor downgrades now require named product profiles, and overlapping 7ZSfxMod and overlay clues no longer count themselves twice; missing nested-signature sentinels replaced with XML key observations that do not claim signature verification; Microsoft CD bootstrap → Windows utility identity with verified platform signature; binary `license` and `toolchain` have no remaining YAML rules or live YAML references; all six legacy branches have no YAML rules or live YAML references) |
| `well-known/malware/supply-chain` | The family's defining role | Delivery does not choose identity | Applied (S1ngularity, Homebrew impersonation campaign markers, the TeamPCP Nx bootstrap and the bmrxntfj wallet-stealer cluster → `malware/stealer`; Shai-Hulud → `malware/worm`; the campaign-listed Pafer pickle loader, Mangorbit evil-twin extension and Graphalgo Go trojan modules → their respective `malware/trojan` families; Melcuratts and GlassWorm loader indicators → `malware/dropper`; unbound campaign references at notable; generic Homebrew payload text and Charpup filename, archive-path and function-name observations → metadata; a single proc-macro1 release checksum → dependency-specific typosquat evidence; the legacy directory and live references are absent) |

Remove a legacy home's whitelist entry only after its last rule moves.

**Why the targets changed:**

| Change | What it fixes |
|---|---|
| Split C-runtime memory by operation; separate free and resize from alloc | Releasing memory is no longer filed as allocation, or by runtime. |
| Consolidate memory mappings and local network resources | One resource, one home, whatever the OS API or backing store. |
| Retire source-language, backend and synonymous launch branches | Equivalent observations stop getting different homes by implementation. |
| Separate crypto operations from primitive presence; add `metaprogramming/reflection` | An unknown implementation or algorithm no longer forces an unsupported claim. |
| Explicit broad transform operations and work scheduling | Unknown algorithms and worker reuse get homes without guessed methods or thread creation. |
| Move payload activation to `execution`; keep control surfaces in C2 | A payload handoff no longer implies a command channel. |
| Admission before payload routing; neutral `process/deploy` | Ordinary updaters stay neutral; preparation gains no execution claim. |
| Install and build context as referenced facts; supply-chain only for trust violations | Credential theft and export keep one home across lifecycle phases. |
| Keep clear names and variable depth | Effort goes to meaning, not uniformity. Wholesale resource-first renames, larger-cap exemptions and a fixed depth ceiling were rejected ([NEW_TAXONOMY_CHANGES.md](NEW_TAXONOMY_CHANGES.md)). |

### Open checkpoints

Resolve each in the migration manifest before moving the affected rules.

| Checkpoint | Required resolution |
|---|---|
| Capacity for broad leaves | The forward maximum is 80 rules; review touched leaves at 72 and split by a durable distinction before they approach the cap; any category-specific exception requires a complete relevance audit and explicit user approval. At the cap, divide and reorganize the category and its neighborhood into durable, precise subdivisions with room to grow, while auditing all rules, parents and siblings. Document the population and consumers, place broad observations accurately, and do not invent a sibling or `other` bucket to satisfy the count. |
| Level-3 branches | Name the children, their single axis, precedence and an incomplete-evidence example before migrating. |
| Broad staging profiles | Staging rules that fit no operation need a defined home; neither dropping the claim nor calling it activation is acceptable. |
| Cross-cutting discovery | Generate an algorithm/source/mechanism index from recorded facets, so an "AES" view finds both presence and operation rules. No engine change. |

### Migration guardrails

- For every move into generic syntax, naming, literals or profiles, record why
  the required evidence supports no more meaningful behavior, objective or
  subject. Review operands, API semantics, targets and configuration effects.
  Record matcher improvements separately when weak detection prevents the
  intended inference; relocation alone does not resolve that weakness.
- A branch contract states the subject, the children's question, admission and
  exclusion criteria, and an example with a neighboring counterexample.
- Two independent placement passes agree on the branch's examples, nearest
  alternatives and broadest observations; disagreement fixes the contract, not
  the sample.
- Every new or relocated leaf has a positive fixture and a near miss for its
  distinguishing claim. Test the required claim, not artificial exclusivity;
  include a both-claims case where overlap is intended. Test exceptions for the
  exact suppression they perform.
- Acceptance: every old rule accounted for; references resolve; placement-only
  moves preserve matching; fixtures and mapping reviews recorded; intentional
  coverage changes evidenced separately; `make validate` passes.

## Reference

### Trait IDs

```
directory/path::trait-name
└─────┬──────┘  └────┬────┘
  directory      local ID
```

The directory path is the ID prefix; filenames never are. `trait-name` resolves
in the same directory; `micro-behaviors/communications/http` matches every trait
in that subtree except `exception` composites;
`micro-behaviors/communications/http/client::curl-download` matches one trait.

```yaml
# objectives/command-and-control/reverse-shell/fd-redirect/combos.yaml
composite_rules:
  - id: reverse-shell
    desc: "Reverse shell pattern"
    crit: hostile
    all:
      - id: micro-behaviors/communications/socket/create
      - id: micro-behaviors/process/fd/dup
      - id: micro-behaviors/process/create/shell
```

### MBC and ATT&CK identifiers

- ATT&CK techniques `T1234`, sub-techniques `T1234.001`; MBC behaviors `B0001`,
  micro-behaviors `C0015`, enhanced ATT&CK techniques `E1234`.
- Assign each ID from the rule's required evidence, not its directory, filename
  or neighbors. A detached install-hook launch is not B0024; a chat send is not
  B0020; product masquerade is not B0039. Prefer the parent ATT&CK technique
  when the evidence does not support a sub-technique.
- Use a file-level mapping default only when every rule in the file proves the
  behavior. `mbc:` is scalar; never write a placeholder `none`. Record further
  justified IDs in the migration review index.
- Distinct evasion and escalation claims keep distinct rules even when they
  share injection mechanics.
- Review against the local MBC catalog
  ([summary](../src/mbc-markdown/mbc_summary.md),
  [overview](../src/mbc-markdown/README.md),
  [mapping guidance](../src/mbc-markdown/yfaq/README.md)), and record its
  revision in the migration manifest.
