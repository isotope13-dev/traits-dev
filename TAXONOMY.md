# cleave Taxonomy

The taxonomy's primary purpose is a **precise, defensible catalog of malware
behaviors and characteristics**, aspiring to Carl Linnaeus's classification rigor:
each observation has one reasonable home, each child refines its parent, and
similar categories have documented boundaries. The catalog is informed by
[MBC (Malware Behavior Catalog)](https://github.com/MBCProject/mbc-markdown).

## Purpose and design commitments

Behaviors describe capabilities, mechanisms, and supported attacker objectives;
characteristics describe properties such as structure, provenance, and identity.
Both are first-class subjects. A characteristic need not be recast as a technique
to earn a place. Neutral capabilities and properties belong in the catalog too;
their presence alone does not imply malice.
The Linnaean analogy is a standard of classification rigor, not a requirement for
fixed ranks, uniform depth, or a single classification for an entire sample.
ML features are a downstream use of this classification. Taxonomic meaning takes
priority over the current model's feature layout.

The practical standard is reproducible classification: two authors reading a
matcher and the directory contracts should independently choose the same home
without knowing the sample, implementation language, or consuming composite.
This catalogs observations, not mutually exclusive classes of specimens: one
sample can exhibit many behaviors and characteristics, each classified separately.
The catalog describes what a program can probably do, using the available
evidence. Runtime execution is not an admission requirement. Distinctive
strings, API references, paths, constants, and embedded implementations can all
support a capability inference. Classify the probable capability at the
specificity the evidence supports; express the evidence and uncertainty in
the rule's description, matcher, scope, and confidence.
The directory names the inferred capability; the rule description names the
observed evidence. For example, an interface-name reference can indicate
probable network-interface interaction without identifying whether the program
enumerates, configures, or monitors interfaces. Keep that rule in the interface
capability leaf until its evidence supports a more specific operation.

- **One defensible home per observation.** Classify what the matcher establishes.
  Each child narrows its parent; siblings answer the same classification question.
  Behavioral branches refine capabilities or techniques; characteristic branches
  refine properties or identities. Neither needs artificial technique labels.
  Document admission criteria and tie-breaking rules wherever categories overlap.
  For competing directories, state what each admits, what it excludes, and the
  evidence that decides between them; include a boundary example when needed.
- **Strictly leaf-only.** Atomic and composite rules live only in leaves. Parents
  organize categories; references reuse evidence without copying rules between levels.
- **Consolidate duplicate observations.** Identical matcher bodies are candidates
  for merging, not reasons for parallel taxonomy branches. Compare effective scope
  and conditions before merging; preserve distinct observations when those differ.
- **Classify the behavior or characteristic, not its implementation.** Language,
  file type, and library backend normally belong in filenames and rule scope;
  equivalent observations share a directory across source and compiled forms.
  Embedded library evidence follows
  its supported technique; independent artifact identity belongs in `well-known/`.
  Distinguish a program's technique from the analyzer's evidence: manipulating an
  AST is a technique; using an AST matcher to recognize a socket call is not.
  Keep hierarchy labels platform-, language-, and filetype-neutral when the
  behavior is shared. A platform name is appropriate when it is part of the
  technique itself (for example, `systemd` persistence); it is not a generic
  implementation partition. Linux namespace operations therefore belong in
  the `namespace` technique leaf with Linux scope on the applicable rules, not
  beneath a `namespace/linux/` directory.
- **Keep claims within the evidence.** A reference, dependency, or embedded
  implementation can support a useful characteristic or capability without
  proving execution, data flow, or malicious intent. Names, descriptions, and
  placement must preserve that distinction.
- **Prefer breadth when equally precise.** Retain depth for real subtechniques.
  Counts and depth warnings prompt review; they never justify invented distinctions,
  generic overflow buckets, or merging meaningfully different behaviors.
- **Preserve detection deliberately.** Update consumers when consolidating or moving
  rules, test both positive and benign cases, and document intentional coverage changes.
  A misleading classification is not repaired by lowering criticality.

Treat directory boundaries as an authoring contract: if two homes remain equally
reasonable, clarify their admission criteria or revise the partition before
adding the rule. Apply the [placement procedure and directory budgets](#directory-budgets-and-placement-contracts)
below; counts are constraints and review signals, not definitions of behaviors.

## Tiers

| Tier | Purpose | Criticality Range | MBC Equivalent |
|------|---------|-------------------|----------------|
| **Capabilities** (`micro-behaviors/`) | Probable capabilities inferred from evidence — what code *can probably do* | component → baseline → notable → suspicious | [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
| **Objectives** (`objectives/`) | Attacker goals — why code *likely wants* to do something | component → baseline → notable → suspicious → hostile | [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions) |
| **Known Entities** (`well-known/`) | Specific well-known malware, unwanted software, and tool/app/library signatures | component → baseline → notable → suspicious → hostile | [Corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) |
| **Metadata** (`metadata/`) | Neutral file-structure properties — what a file *is* | component → baseline → notable → suspicious (rare) | — |

**`metadata/` reaches `notable` when the fact identifies something rather than merely measuring it.** The tier is neutral about *intent*, not about *significance*: a file-structure property that establishes provenance — a signer, a toolchain or compiler, a declared import, a referenced library or runtime — is precisely what the `notable` definition below calls "program identity, and signing information", and an analyst wants it surfaced in a version diff. (This is a criticality rule, not a placement licence: a fingerprint saying a file *is* a named piece of software still belongs in `well-known/` — see [Metadata (`metadata/`)](#metadata-metadata).) Reserve `baseline` for properties that are near-universal **within the trait's own `for:` scope** (`USER32.dll` in a Windows GUI PE, `BSJB` in a .NET assembly); a property that most files of that type do not have is not baseline. `hostile` remains the real tier prohibition — `objectives/` and `well-known/` only.

Organize atomic traits by what they detect, not by what composite they serve — atomics and the composites that reference them often live in completely different directories. See [Matcher Defines Identity](#matcher-defines-identity) for the full rule and the placement-over-criticality guidance.

Traits rarely seen in legitimate software that have well-defined objectives belong in `objectives/` rather than `micro-behaviors/`.

## Criticality

| Level | Meaning | Tier Constraints |
|-------|---------|-----------------|
| **exception** | Benign-context composite: a known-good pattern assembled from `notable` traits that, when it matches, suppresses or downgrades a host detection. Referenced only from `unless:`/`downgrade:`. Assembly-only — never emitted to JSON, the CLI, the web UI, or differential analysis. See [Exception composites](#exception-composites-crit-exception). | Composites only; any tier |
| **component** | Evidence too weak or incomplete to express a clear standalone observation (e.g., the string fragment `&cc=` or one half of a protocol marker). Reserve this for fragments that only acquire meaning when combined with other evidence. Being referenced by a composite does **not** make a trait a component. | Any tier |
| **baseline** | Common functionality; doesn't indicate program purpose (e.g., `mmap`, `stdio`, `read`). Always present in JSON, the web UI, and differential analysis. | Any tier |
| **notable** | Expresses a clear behavior, purpose, or identity that could interest a security engineer during differential analysis (e.g., `socket`, HTTP requests, network-library imports, `exec`, `eval`). If an appeared/disappeared atomic finding would help an analyst understand what changed, it should be at least notable—even when the behavior is benign. This includes communications, code execution, crypto, encoding/decoding, privilege operations, sensitive file access, registry access, persistence, program identity, and signing information. | Any tier |
| **suspicious** | Rarely legitimate; indicates possible malicious intent. | `micro-behaviors/`, `objectives/`, `well-known/`, `metadata/` (rare) |
| **hostile** | Clear attack pattern; no legitimate use. Requires precision >= 3.5 as an authoring bar; runtime precision checks are advisory (see [RULES.md](RULES.md#criticality-levels)). | `objectives/`, `well-known/` only — **never** `micro-behaviors/` |

> **Visibility caveat — `component`/`baseline` are not hidden from users.** The CLI may de-emphasize or omit them (historically `component` was filtered unless a referencing composite fired; that is no longer guaranteed), but the JSON output, the web interface, and version-to-version differential analysis all surface them. Demoting a trait therefore does **not** make a false positive disappear — a user still sees it, mislabeled — and rules are equally important to get right at every criticality level. Lower criticality only when the lower tier is genuinely correct (a true composite fragment or universal-baseline capability). Fix a real false positive properly: tighten the matcher, add an `unless:`/`not:` exclusion, or relocate the trait (see [Matcher Defines Identity](#matcher-defines-identity)).

### Prefer strong atomic traits

Atomic traits should, whenever possible, be strong enough to communicate a precise and useful fact on their own. `component` is a last resort for evidence that cannot honestly support such a fact—not a default for the leaves of a composite.

- **Composite membership does not determine criticality.** A complete API call, import, command, protocol operation, path access, or product identity remains `notable` when it independently tells an analyst something useful, even if a composite also references it.
- **Use the standalone-description test.** Imagine the atomic finding appearing by itself in a version diff. If its matcher supports a clear description that a security engineer could use to understand or investigate the change, it is not a component. If the only honest description is “fragment,” “marker,” “part of,” or an otherwise incomplete clue, `component` may be correct.
- **Distinguish `baseline` from `component`.** A baseline trait expresses a clear but nearly universal behavior (`read`, `stdio`, `mmap`). A component does not yet express a clear behavior at all. Do not use `component` merely because a behavior is common.
- **Strengthen weak atoms before accepting components.** Prefer a structured matcher, call argument, anchored token, tighter context, proximity constraint, or a canonical matcher that captures equivalent syntax. The goal is fewer, stronger atomics—not many weak fragments assembled mechanically.
- **Never demote to manage duplicate output.** If an atomic and composite finding overlap, consolidate equivalent matchers, choose a canonical trait, update references, or improve presentation. Do not lower an independently meaningful atomic capability to `component` just because it participates in a composite.

Examples: `urllib.request.urlopen()`, a socket connection, an HTTP-client import, `execve`, AES use, or a registry write are independently meaningful and therefore notable. A bare `&cc=` fragment, one word from a multi-token family signature, or one half of an encoded marker may correctly be a component.

### Exception composites (`crit: exception`)

`exception` is a special, **composite-only** criticality for a *benign-context suppressor*: a known-good pattern that, when it matches, suppresses or downgrades another detection through that detection's `unless:`/`downgrade:` clause. It is the sanctioned home for "this combination looks alarming but is a recognized benign program or toolchain" rules — the kind that otherwise drift into `objectives/` or `well-known/malware/`, where a benign suppressor does not belong. A rule whose id or description reads as benign suppression — `benign`, a `<thing>-context` name (`fp-context`, `safety-context`, `panos-context`, …), a `-fp` / `-soft-fp` / `-known-fp` or `-exceptions` id, `false-positive`, or allow/whitelisting — sitting in `objectives/` or `well-known/malware/` is almost certainly misorganized; make it a `crit: exception` composite instead (or, if it really detects something, rename it for what its matcher finds).

The contract (each is enforced at load time):

- **Composites only.** An atomic trait may not be `crit: exception`.
- **Referenced only from `unless:`/`downgrade:`.** An exception is never positive evidence — referencing one from `all:`/`any:`/atomic `if:` is an error.
- **Must be referenced.** An exception no rule reaches is dead weight and is rejected.
- **Members must be `notable`.** Its `all:`/`any:` legs must each resolve to a `notable` trait — or another `exception` (an exception may compose nested benign patterns). A benign assertion is assembled from "defines program purpose" facts, not baseline noise, component fragments, or `suspicious`/`hostile` legs.
- **Named traits only.** Every condition must be a trait reference; inline matchers (`text`, `symbol`, `raw`, …) are rejected, since they carry no criticality and would bypass the `notable`-member rule.
- **May live anywhere**, because it is named and located by what it suppresses rather than by tier.

**Directory-reference safety — the reason this class exists.** A bare directory reference (`objectives/foo`) in an `all:`/`any:` clause silently *excludes* any exception beneath it, so you can fold an entire `objectives/` directory in as positive evidence without ever inheriting a suppressor by accident. Exceptions are reached only by an exact `dir::id` reference — the form `unless:`/`downgrade:` use — with one carve-out: inside another exception composite, a directory reference *does* include the exceptions beneath it, so an exception may deliberately assemble a directory of benign patterns.

## ML Feature Extraction

The ML pipeline extracts features from **trait-path prefixes + criticality**, not individual trait IDs alone. The current Collimator path-presence/max-criticality extractor keeps the first three path segments **including** the tier (`objectives/evasion/kernel-hide`), so it guarantees only two taxonomy levels below that tier as direct path features. Full paths can also appear in higher-order features when present in the trained vocabulary, but a deep path is not guaranteed its own unary feature. Treat the visible-prefix limit as an implementation detail that may change with a model update, not as a reason to erase a real technique distinction. This means:

- **Directory structure is the feature space.** A trait at `objectives/evasion/kernel-hide/rootkit/linux.yaml` with `crit: suspicious` currently generates direct path features through `objectives/evasion/kernel-hide:suspicious`; the deeper `rootkit` distinction is not a guaranteed unary feature. The directory hierarchy directly shapes what the model learns.
- **Criticality is the signal strength.** Two traits in the same directory but at different criticality levels produce different features. A `suspicious` rootkit trait and a `component` rootkit trait are distinct signals.
- **Path-prefix visibility is bounded.** The current direct path feature uses the tier plus its first two descendants. Deeper directory names remain important for human placement and can occur in higher-order features, but they are not guaranteed an independent direct feature until the model's path limit changes.

### Design implications for trait authors

- **Group detections by their shared behavior or characteristic.** Consistent categories also support feature aggregation; rule count alone establishes neither taxonomic validity nor ML signal quality.
- **Don't create single-trait subdirectories** when the trait fits an existing directory. Browser-specific evidence for the same credential-access technique belongs in that technique's leaf, with browser-specific filenames. A distinct technique may justify a small leaf; document its boundary rather than merging it merely to increase the count.
- **Use technique-based directories.** Directory names should describe the behavior or method being detected, not the implementation language, platform, ecosystem, file type, malware family, or sample source. Put implementation details in filenames when they help readability, unless the technique itself is platform-specific.
- **Prefer concise, meaningful names.** Short directory names are easier to scan and produce cleaner ML features: use `exec`, `poll`, `proxy`, `shell`, `reflect`, or `stage` when they are clear in context. Do not shorten names so far that humans lose the technique meaning.
- **Avoid marker buckets.** Do not use `marker/` or `markers/` as directory names; name the behavior or technique being indicated instead.
- **Every subdirectory must add precision over the path that leads to it.** A child directory has to answer "the parent's concept, but *which kind / how / in what form?*" — if it merely restates the parent (a synonym) or means "everything else here," it earns no place in the tree. Test: read the full path left-to-right; each segment should narrow the set further. `process/create/shell/invoke/` fails — *invoking* a shell **is** *creating* a shell process, so `invoke` is a synonym for `create`, not a refinement; in practice it had become the catch-all bucket (everything that wasn't one of the precise siblings `batch/`, `encoded/`, `injection/`, `interactive/`…), which is why it bloated past the size cap. Contrast its siblings, which each genuinely refine "create a shell" (*via a batch file*, *with an encoded command*, *by injection*). A segment that you can't finish the sentence "…the parent, specifically the **___** kind" for is either a synonym (drop it / merge up) or a grab-bag (split it into the precise techniques it actually contains). Verb-vs-verb synonyms (`create`/`invoke`/`spawn`/`exec`/`run`) are the most common offenders.
- **A bare `any:` composite shares its legs' criticality.** A composite that is nothing but an `any:` list — no `all:`/`unless:`/`not:`/`downgrade:`/`needs:`/size/scope, and a `for:`/`platforms:` identical to its legs — fires exactly where its legs fire, on whichever one matched. Ranking it above them makes the reported tier depend on which leg happened to hit, so the same evidence in the same file surfaces at two different levels. Either raise the legs to the composite's `crit:`, or add the filtering that earns the higher tier (`needs: 2`, a second `all:` leg, a size band). This bites most often on library-identity rules: if each marker independently identifies the library, every marker is `notable` and so is the roll-up — put the criticality once, in `defaults:`.

- **Criticality assignment affects ML directly.** A trait bumped from `notable` to `suspicious` changes which feature it contributes to. Assign criticality based on the trait's actual detection confidence, not to manipulate features.
- **Never name a directory for a verdict.** `legitimate/`, `benign/`, `known-good/`,
  `safe/`, `trusted/`, `whitelist/` and friends are rejected: a directory names what
  its traits *search for*, whether the answer is alarming is `crit:`, and a
  benign-context suppressor belongs in the directory for the thing it detects.
  `os/service/legitimate/` held `uv publish` markers and `curl | sh` installer
  shapes -- neither a service nor a judgment a reader could act on; they now sit in
  `os/package-manager/publish/` and `os/package-manager/installer-script/`.

- **Keep meaningful distinctions visible when practical.** The current direct path feature ends after two taxonomy levels below the tier. Thus `micro-behaviors/fs/path/sensitive/private-key/` and its siblings share the direct prefix `micro-behaviors/fs/path`; the model cannot distinguish private-key paths from other paths through that feature alone. A more exact taxonomy might use `fs/path/private-key/`, `fs/path/password-store/`, and `fs/path/cookie/`, with ownership in filenames such as `ssh.yaml` or `browser.yaml`; those leaves still share the current direct prefix. Likewise, `objectives/anti-static/obfuscation/string/encoding/` and `.../string/fragmentation/` share the direct prefix `objectives/anti-static/obfuscation`; their distinct leaves are not guaranteed unary features. Consider a broader sibling layout such as `anti-static/obfuscation/string-encoding/` and `.../string-fragmentation/` if it preserves one clear home per matcher.
- **Prefer breadth over depth when precision is unchanged.** Put distinct, equally specific techniques in sibling directories rather than stacking another level under a broad bucket. Keep a deeper child when it expresses a genuine subtechnique and flattening it would merge claims that need different destinations. Directory depth is not itself evidence of misorganization; a validator may flag sparse sibling cohorts for review, but it must not demand a shallower path when that would make placement ambiguous or less exact.

## Core Principles

### Single-Trait Rule

Unlike MBC, which allows one behavior to map to multiple objectives (e.g., Process Injection is both Defense Evasion and Privilege Escalation), cleave allows exactly **one trait per behavior**. Place it at the most specific location the evidence supports. Composite rules in other directories can reference the single trait to express multi-objective interpretations.

The same logic extends to matchers: define each one once. If two traits would search for the same thing, make a single canonical atom and reference it rather than copy the pattern — duplicate matchers drift out of sync, double-count evidence, and split one signal across two ML features. Unique matchers keep the trait set slim.

### Matcher Defines Identity

**A trait's matcher is its identity. Its name, description, and directory must describe what the matcher actually searches for — not the intent of a composite that references it, and not the worst case it might contribute to.** Organize atomic traits by what they detect, not by what composite they serve. This applies at **every** criticality, `component` and `baseline` included.

A trait fails this rule when its name, description, or location claims an intent its matcher does not capture. Example: a regex that merely reads `$_SERVER['HTTP_REFERER']`, named `http-referer-to-reflection` ("HTTP Referer used in function execution") and filed under `objectives/command-and-control/backdoor/webshell/obf-dispatch/`. The matcher detects only *"reads the Referer request header"* — a neutral capability present in countless benign plugins — so the trait is both **mislabeled** (the name asserts reflective dispatch the regex never checks) and **misplaced** (a neutral read does not belong in a webshell objective directory). The reflective-dispatch intent lives in the *other* legs of the composite (the dynamic-call atoms); this atom only contributes "the referer was read."

**The fix is to relocate and rename the trait to match its matcher** (here, a `micro-behaviors/communications/http/...` capability such as "reads the Referer request header"), then have the webshell composite reference it cross-directory. **Lowering the criticality is never the fix.** Demoting to `component` does not make the false positive disappear — per the [Criticality](#criticality) visibility caveat, the JSON output, web UI, and differential analysis still surface it (and the CLI may too), now mislabeled as a webshell building block and keyed to the wrong `directory-path + criticality` ML feature. Reserve `component`/`baseline` for traits that are *already* accurately named and located for what they detect and genuinely have no standalone meaning.

When a generic capability false-positives because it sits in the wrong tier, fix the placement. Generic capabilities such as process execution, interpreter invocation, network clients, registry manipulation, file writes to sensitive locations, and persistence surfaces belong where those behaviors are described — usually under `micro-behaviors/` — and should stay `notable` or higher when they are analyst-relevant. Notable in terms of what would be interesting to a security engineer for triage: such as who, what, when, where of a program (even if benign). Objective traits should compose those capabilities with intent-specific evidence rather than bury generic atomics as mislabeled `component` rules.

### Names an attacker or a collector chose

**A trait may match a filename. A conviction may not depend on one that the attacker or the collector picked.** Matching a name is not the problem; resting a `suspicious`/`hostile` verdict on a name that costs nothing to change is. Three cases, and only the first can carry weight:

- **The format mandates it.** `SKILL.md`, `package.json`, `AUTOEXEC.BAT`, `MANIFEST.MF`. The attacker has no choice: a malicious agent skill that omits `SKILL.md` is not a skill, and a boot script that is not named `AUTOEXEC.BAT` does not run at boot. These are properties of the platform, so requiring one in `all:` is correct — and they belong in `metadata/`, `micro-behaviors/` or `well-known/app/` as format facts at `notable`, which is where a conviction composite then references them.
- **The attacker chose it.** A dropped `motivate.bat`, a `_runtime.js` sidecar, a campaign token, a C2 hostname, a chosen function name. Real evidence about *this* sample, and worth stating — but the next build renames it for free, so it corroborates in `any:` and never gates in `all:`. This is the rule the supply-chain audit already states for matchers: chosen local identifiers must not become identity signatures.
- **A collector chose it.** The name of the outer artifact being scanned — `Win32.Volk.7z`, `2026-03-27-telnyx-v4.87.2.zip`, `telnyx-4.87.2.tgz`. Nobody in the attack picked it; it was assigned when the specimen was fetched or filed, and it changes on re-collection. It carries no attack information at any criticality.

The distinction is container versus member, not file extension. A member inside an archive is named by the attacker or by the format; the container itself is named by whoever downloaded it. A literal ending in an archive extension is the static approximation of "this can only ever match the container", which is what a validator can check at author time.

**A conviction needs at least one content-derived required leg.** Names, sizes, and metrics describe what a file *is called*, *weighs*, and *counts* — never what it does. A rule assembled entirely from those is a file hash in behavioural clothing: `size_min` and `size_max` both 1917, an exact `.tgz` basename, and `strings.count` exactly 13 convict one artifact and nothing else, including the next build of the same malware. State the behavior, then let the name corroborate it.

### Tier Dependencies

| Tier | Can Reference | Rationale |
|------|--------------|-----------|
| `micro-behaviors/` | `micro-behaviors/`, `metadata/`, `well-known/{app,dual-use,game,lib,tool}/` for false-positive exclusions only | Capabilities must not depend on objectives or malware families |
| `objectives/` | `micro-behaviors/`, `objectives/`, `metadata/`, `well-known/{app,dual-use,game,lib,tool}/` (positive evidence allowed); never `well-known/malware/` | Objectives build on capabilities and other objectives. Legitimate-software identifiers are fine as positive evidence — the relationship runs `well-known/malware/ → objectives/`, not the reverse |
| `well-known/` | all tiers | Signatures can reference anything |
| `metadata/` | `metadata/`, `well-known/{app,dual-use,game,lib,tool}/` for benign context only | Informational properties must not depend on behavior or objectives |

**Capabilities must not reference objectives.** Capabilities are observable mechanics; objectives infer intent. If a `micro-behaviors/` rule needs an `objectives/` trait, either move the objective to `micro-behaviors/` (if it's actually a capability), refactor the dependency away, or move the whole rule to `objectives/` (if it's actually inferring intent).

**Capabilities must not use `crit: hostile`.** Hostile requires intent inference, which belongs in `objectives/`. Maximum capability criticality is `suspicious`; validation rejects hostile capabilities.

**Neutral capabilities belong in `micro-behaviors/`, not `objectives/`.** A trait that detects a single API call, syscall, or keyword (fork, crontab, SetFileAttributes, getenv) is a capability — it belongs in `micro-behaviors/` regardless of which objective composite references it. Composites reference traits across directories. Component traits (`crit: component`) may appear in `objectives/` only when they are attack-context-specific fragments with no meaning outside that context (e.g., Nemucod string pieces, default credential lists, supply-chain URL patterns).

For example, a Swift `Data(base64Encoded:)` reference belongs to
`micro-behaviors/data/decode/base64` even when an anti-static composite uses it;
the `/bin/sh`, `-c` argument pair belongs to
`micro-behaviors/process/create/shell/command-string`. The objective composite
retains only the intent that the combined evidence supports.

### Directory Layout Convention

Paths classify observations from general to specific; they do not require fixed
ranks or uniform depth. Behavioral paths commonly follow
`TIER/CATEGORY/BEHAVIOR/METHOD/platform.yaml`; characteristic and identity paths
instead refine the property or entity being identified. Omit levels that add no
meaning. Implementation-specific filenames do not create taxonomy categories.
Regardless of path shape, rules belong strictly in leaves.

- **`objectives/`**: `objectives/OBJECTIVE/BEHAVIOR/METHOD/` with technique-based directories and per-platform or per-ecosystem YAML files. Add sub-method directories when a method has many variants (e.g., string obfuscation techniques). Avoid platform, language, ecosystem, file-type, and family names as directories unless they are the technique being detected.
- **`micro-behaviors/`**: `micro-behaviors/CATEGORY/BEHAVIOR/METHOD/` (e.g., `crypto/symmetric/aes/ruby.yaml`, not `crypto/symmetric/aes.yaml`). If no specific method applies, group by syscall, protocol, or logical grouping. Composite traits may reference directory names to match related rules.
- **`well-known/malware/` and `well-known/unwanted/`**: Organize by recognized family or named entity, not by a generic behavior, delivery method, or bundle of traits. Malware may retain a broad class before its family (`well-known/malware/backdoor/bpfdoor/`); unwanted software normally uses the family directly (`well-known/unwanted/gameograf/`). Do not use generic buckets such as `newtab-wallpaper-adware/` or `vpn-leadgen/`. **"Recognized" means recognized by name outside this repository** — a family a working security engineer would already know (Shai-Hulud, event-stream, XZ Utils), not merely a package that once carried an advisory. That bar is high on purpose, so these directories stay small: an obscure typosquat, a tea.xyz reward-campaign stub, or a single withdrawn npm release is an *instance* of a technique, not a family, and naming a directory after it buys a signature that matches one package and nothing else. Detect those through the technique instead — a registry-pollution, dependency-substitution, or install-hook rule under `objectives/` convicts the next hundred of them too. A family directory earns its place only when the campaign has a name people use and traits that generalize across its members. Put generic unwanted or abusive behavior under the best-fitting `objectives/` hierarchy, then let each named family rule reference that objective. If no objective fits, add a behavior-based objective or document the taxonomy gap rather than filing intent-bearing behavior under `micro-behaviors/`.
- **Directory names** should be short, readable, and semantically useful. Prefer `exec` over `command-execution`, `poll` over `polling-command`, and `reflect` over `reflective-loader` when the parent path supplies enough context. Keep longer names when the shorter form would be ambiguous. A directory segment must name a SUBJECT — the thing the traits beneath it are about. Three kinds of word fail that and are rejected by the validator:

  - **Catch-alls** (`core/`, `common/`, `general/`, `misc/`, `other/`) mean "everything else", so they never make you answer what a trait is about — which is the same question that reveals whether it belongs in the tier at all. Split by the behavior each child actually detects.
  - **Judgments** (`anomaly/`, `quality/`, `suspicious/`, `notable/`) assert a verdict instead of naming a subject. The fact belongs with the thing it describes, and *how unusual it is* belongs in `crit:` — which already carries exactly that, at the level the ML pipeline reads. `metadata/binary/anomaly/provenance::pe-zero-timestamp` is `baseline` and `…::pe-far-future-timestamp` is `notable`: the degree is already expressed, so the directory is restating it and spending a visible level to do so.
  - **Forms** (`metrics/`, `threshold/`, `scoring/`, `pattern/`, `indicators/`) describe the shape of the rule rather than its subject. Everything in `metadata/` is measured; put the count with the part it counts and let the threshold live in the trait name (`few-basic-blocks`, not `metrics/threshold/`).

Adjectives fail for the same reason as judgments: `sparse/`, `dense/`, `structural/` partition by value, not by subject, so they separate facts that belong together (`few-basic-blocks` from the other code measurements) and spend the last ML-visible level saying nothing.

**Implementation containers** (`library`, `lib`, `stdlib`, `framework`, `wrapper`,
`runtime`, `provider`) are also unsuitable when they merely partition the same
technique by backend. This is a placement rule, not a global validator word ban:
those words can name a real resource, interface or artifact class. Apply the
[implementation substitution test](#implementations-and-library-fingerprints)
and its counterexamples before removing a level.

**The matcher’s input form is not the taxonomy subject.** A rule does not
belong under `source/`, `javascript/`, `python/`, `pe/` or another language or
file-type branch merely because it matches source text, syntax, bytecode, or a
particular artifact type. Put equivalent behavior in one language-neutral
directory and express supported languages, platforms and file types with the
rule’s `for:` and `platforms:` scope. Classify source-level evidence by what it
establishes: an operation/API by its capability, a hostile code technique by
its objective, and a structural property of the analyzed code by its metadata
subject. Code techniques such as AST inspection/transformation and runtime
reflection belong under `metaprogramming/<technique>` regardless of whether
evidence is source text or compiled code. `micro-behaviors/data/source/` is a
historical mixed namespace, not a claim that source code is a kind of runtime
data or a valid new placement; do not add rules there. Migrate each existing
rule to its semantic subject rather than recreating `source/` as a taxonomy
axis.

### Directory budgets and placement contracts

**Placement procedure:** State the observation the matcher actually supports;
choose its tier; find the existing subject; then choose the most specific
leaf justified by that observation. Check its nearest competing leaf before
adding a rule. Implementation language, evidence surface, and the objective
that consumes an atom do not choose its home.

**Keep directories strictly leaf-only.** Broad observations do not justify
putting YAML beside subdirectories. We previously tried mixed nodes: similar
rules accumulated at both parent and child levels, creating duplicate homes.
This applies to atomic traits and composites alike: a parent cannot retain
umbrella composites, aliases, or broad matchers after gaining rule-bearing
children. Parent paths remain available for directory references; they group
descendant rules without owning another copy of those rules.
When a matcher cannot choose among children, resolve its actual claim:

- A shared operation with an unspecified algorithm belongs with that operation,
  such as cipher initialization; it must not be assigned an algorithm it does
  not establish. The operation needs one canonical home shared by all callers.
- A dependency declaration or attribution belongs with that metadata subject;
  it does not establish every capability of the named library.
- A matcher with independently meaningful alternatives should be reviewed as
  separate canonical observations, with consumers updated to preserve the
  original alternatives. Do not copy the whole matcher into each destination.
- An opaque fingerprint that really establishes only a broad capability needs
  a coherent leaf partition for that capability before migration. Record an
  unresolved placement issue until that partition is defensible. Do not use a
  parent-level rule, `general`, `other`, or a false subtechnique to hide the gap.

A proposed split must account for **all** existing rules, including broad
observations, before any are moved. If its children cannot do so without
overlap or overstated claims, revise the split. The 100-rule cap is not evidence
that a more specific observation exists.

`make validate` enforces **one inclusive cap of 100 rules per directory**:
atomic `traits` plus `composite_rules`, across every YAML file in that directory.
There is no separate atomic cap and no directory exemption. All criticalities,
including `exception`, consume the budget. Descendant directories have their own
budgets; filenames do not create new namespaces or budgets.

`make validate` emits a **soft, non-blocking depth warning above five directory
levels below the tier**, across all four tiers. Count neither the tier itself
nor the YAML filename: `objectives/a/b/c/d/e/rules.yaml` is depth five and does
not warn; `objectives/a/b/c/d/e/f/rules.yaml` is depth six and does. A warning
requests review, not mandatory flattening, and does not change the exit status.
There is no hard physical depth limit.
Use the shortest hierarchy that gives each matcher one clear semantic home.
Prefer breadth over depth when sibling techniques remain equally exact; retain
a deeper level when flattening would merge distinct techniques or make
placement ambiguous. The current ML extractor gives direct path features only
through two descendants below the tier, so deeper leaves may not contribute a
separate direct feature. That is a model-visibility limitation to weigh, not a
reason to sacrifice taxonomy precision. Within the behavioral tiers, below
the first category level, the validator reports a parent for review when it
has at least two child subtrees and all those subtrees together contain fewer
than 35 rules. This may suggest room to express equally precise sibling
categories more broadly. Single-child parents do not trigger this advisory;
internal directories still contain no rules. It does not reject a path solely
because it is deep.

Sibling names sharing a spelling stem also prompt non-blocking review. A stem
match is not proof of synonymous subjects: account identity and process
accounting are distinct. Document admissions and exclusions; merge only when
the observations genuinely overlap. This does not create a directory exemption.

Platform breadth is likewise a review heuristic: four or more platform
declarations produce a non-blocking scope advisory, uniformly across tiers.
Check that the matcher supports each platform; a format-defined metadata fact
can legitimately hold across operating systems. Do not drop supported coverage,
duplicate matchers by OS, or move a rule into a different subject just to reduce
the count. Invalid platform declarations remain errors. This advisory does not
relax the 100-rule cap or the strictly leaf-only policy.

Before splitting a directory, audit its siblings and likely destinations. Route
misplaced atoms to their existing homes and consolidate equivalent rules first.
Every proposed parent needs a placement contract containing:

1. The one question answered by its children and the evidence required to enter it.
2. Each child's positive definition, exclusions, and nearest competing sibling.
3. A deterministic precedence rule when one matcher contains several facets.
4. At least one placement example and counterexample, with a canonical destination.

A child must be a proper refinement of its parent. Remove synonymous or empty
grouping levels. Expand breadth for different mechanisms, resources, or effects
when doing so preserves exact placement; do not split by alternate verbs,
languages, APIs, or rule forms.
Keep the existing 150-child fan-out cap: broad identity catalogs should split by
a stable function, with an explicit primary-function tiebreaker.

Separate independent facts into canonical atoms and reference them from composites.
Do not duplicate a whole objective under every carrier, trigger, or ecosystem.
A composite lives with its most specific required behavioral result; optional
corroboration does not choose its directory. A rule that needs several children
but proves no narrower result needs an explicitly defined joint behavior, not a
`misc/`, `combined/`, or `behavioral/` overflow bucket.

The [behavioral directory contracts](#behavioral-directory-contracts)
are the placement guide. The [directory audit and migration plan](docs/taxonomy-audit/PLAN.md)
records violations and the work needed to bring existing rules into that guide.
Existing IDs continue to resolve until a migration updates their consumers;
their presence does not make a conflicting directory an equally valid home.
Destinations marked **planned** need a coordinated rule/reference migration and
any applicable validator-whitelist update before use. Do not create duplicate
matchers or compatibility aliases to straddle old and new homes.

### Directory & Evolution Guidelines

- **Leaf-Node Policy**: A directory level cannot contain both YAML files and subdirectories. An internal directory may have just one child; a child that adds meaning remains useful even when no other subtype is represented. Single-child count is an audit statistic, not a validation warning. When flattening a genuinely redundant level, remove the obsolete directory as well as moving its YAML, and update references. A valid leaf need not be extended to level three merely for uniform depth.
- **Intent-Based Categorization**:
  - **`objectives/`**: Reserved for unwanted, improper, or malicious behavior that requires intent inference. Any generic finding suggesting unwanted behavior, malice, or abuse must be categorized under an `objectives/` hierarchy.
  - **`micro-behaviors/`**: Reserved for strictly neutral, atomic observations. If an id, description, or matcher interpretation hints that the observed behavior is unwanted, promotional, deceptive, abusive, or malicious, it is not neutral and should move to `objectives/`; keep only the underlying factual mechanic here.
- **Platform/Language Neutrality**: Directories must NOT be named after programming languages (e.g., `python/`) or platforms (e.g., `windows/`). These are used as suffixes in YAML filenames (e.g., `dropper_python.yaml`). This ensures the ML pipeline can perform cross-language and cross-platform technique correlation.
- **Matcher Neutrality**: File a rule by the operation it observes, regardless
  of whether a text search, symbol fact, or AST query detects it. `ast/` is a
  valid subject only when the program itself constructs, traverses, or
  transforms an abstract syntax tree. A Ruby AST matcher for `Base64.decode64`
  belongs with Base64 decoding; one for `File.rename` belongs with file rename.
  Stream binary/text mode changes belong in `fs/file/io-mode`; permission-bit
  changes belong in `fs/chmod`, even if both APIs call their argument a mode.

## Decision Framework

### Tier Selection

```
Specific malware, unwanted software, dual-use product, app, library, game, or tool signature; well known enough that at least 1 in 1000 developers or security engineers would recognize it?
  → well-known/

Attacker intent inferred from capability combinations?
  → objectives/

Evidence of a probable capability, without an attacker-intent claim?
  → micro-behaviors/
     Rarely legitimate?     → suspicious
     Useful in differential analysis? → notable
     Universal baseline?      → baseline

Neutral file property (not behavioral)?
  → metadata/
```

### Text, Content, and Metadata Boundaries

The matcher type does not decide tier placement. A `type: text`, `string_literal`, `raw`, or `encoded` matcher still belongs where the thing it detects belongs:

- **Classify the inferred capability, not the certainty or evidence format.** A distinctive interface name such as `veth` or `docker0` supports probable network-interface interaction and belongs in `micro-behaviors/network/interface/`, alongside relevant API references, paths, and calls. This is a capability clue, not proof of runtime activity or attacker intent. Describe a reference as a reference; require operation-specific evidence to label it enumeration or configuration. Reconnaissance intent belongs in `objectives/discovery/network/` only when combined evidence supports that inference. String evidence does not need a separate metadata home, `reference/` layer, or `probable/` branch. Ordinary ambiguous words still need context before they support a useful capability inference.
- Terms go where the represented concept belongs, not under a text bucket. A credential word belongs in `objectives/credential-access/theft/keywords/`; HTTP verbs belong in `micro-behaviors/communications/http/keywords/`; help and usage strings belong in `micro-behaviors/ui/help/` because they represent the ability to expose a user-facing help surface.
- Terms that represent attacker intent or impact go under `objectives/`. Infection terms such as "infected", "virus", or ELF infection context belong with `objectives/impact/infect/`; hostile traits stay in `objectives/` or `well-known/`.
- Specific product, malware-family, tool, library, app, or game identities go under `well-known/`, not a generic keyword bucket. Embedded implementation evidence follows the [technique-first contract](#implementations-and-library-fingerprints); a dependency declaration remains metadata.
- Metadata is only for neutral structural facts about what a file or package is: manifest fields, declared permissions, file magic, dimensions, counts, layout, package quality, or other non-behavioral shape. Suspicious metadata can be used as evidence in an objective composite, but "metadata anomaly" is not itself a supply-chain attack kind.
- Generated-code and build-output properties belong under their specific `metadata/build/` subject; fingerprints identifying the analyzed tool or library artifact belong in `well-known/`; package properties belong under the corresponding `metadata/package/` subject. Embedded library code belongs with its supported capability. Do not put all benign tooling in a package bucket. Assemble benign-context suppressors as `crit: exception` composites according to the exception contract, and reference them from `unless:` or `downgrade:`.
- `micro-behaviors/data/` is for operations on data: encoding, decoding, compression, serialization, parsing, archive handling, string manipulation, buffers, databases, embedded payload/resource handling, source-level data mechanics, and control-flow patterns over data. It is not for data merely being present.
- Do not create generic content buckets such as `data/text/`, `text/`, `lexicon/`, `vocabulary/`, `words/`, or `strings/` as dumping grounds. Split terms by the concept they represent, and let composites reference those atoms across directories.

### Evasion Boundaries

Three objective categories cover evasion, following MBC's distinction between analysis evasion and detection evasion:

| Category | Target | MBC Definition | Examples |
|----------|--------|---------------|----------|
| `anti-analysis/` | Automated analysis environments | *"Prevent, obstruct, or evade behavioral analysis — for example, analysis done using a sandbox or debugger."* (OB0001) | IsDebuggerPresent, VM detection, sandbox fingerprinting, emulator checks |
| `anti-static/` | Static analysis of the file at rest | *"Prevent or hinder static analysis. Simple static analysis identifies features such as embedded strings, header information, or file metadata. More involved static analysis involves disassembly."* (OB0002) | Code obfuscation, packing, control-flow flattening, code virtualization |
| `evasion/` | Users, admins, deployed security products | *"Enable malware to evade detection."* (OB0006) | Rootkits, masquerading, AMSI bypass, log clearing, process injection, self-deletion |

**Tiebreaker:** When a technique spans categories, ask what it *primarily* defeats:
- Fools a sandbox, debugger, emulator, or VM? → `anti-analysis/`
- Resists disassembly, decompilation, or string extraction? → `anti-static/`
- Hides from users, admins, or AV/EDR in production? → `evasion/`

### Process creation

`micro-behaviors/process/create/<mechanism>/` is the feature `process/create/<mechanism>`. The model keeps that third segment and no further one, so the segment has to be the mechanism. A directory under `launch/`, `shell/`, or `exec/` does not gain a new meaning by existing; the model still reads the parent.

Each sibling has to name a different fact. Finish "this matcher creates an execution context by ___." If an existing sibling already finishes that sentence, the trait belongs there and the language or API spelling goes in the filename. A synonym of the parent or of a sibling does not get a path. Verb piles (`launch` / `invoke` / `spawn` / `exec` / `run`) are the usual way this fails.

Stop at the first row that describes the matcher:

| The matcher shows | Directory |
|---|---|
| A thread inside the current process | `thread` |
| A clone of the current process | `fork` |
| A new shell parsing command text (`sh -c`, `cmd /c`, `shell=True`, a pipeline, `bash "$f"`) | `shell` |
| A new interpreter process handed source text (`node -e`, `python -c`) | `eval` |
| A library object standing for the child (`Popen`, `NSTask`, `ProcessBuilder`) | `subprocess` |
| The desktop opener choosing the handler (`ShellExecute`, `open`, `NSWorkspace`) | `shellexec` |
| An API directly starting an image from an argument vector or executable command line (`execve`, `CreateProcess`, `posix_spawn`, `WinExec`, `WshShell.Run`) | `exec` |
| Only an executable name, launch flag, agent permission, or import, without a creation mechanism | The corresponding path/configuration/import observation; not a second process-creation mechanism |

The table describes canonical ownership, not a claim that all existing leaves
already comply. `launch`, `direct`, `spawn`, `execv`, and `spawnv` must be reconciled
by these tests. The executable being launched does not override the mechanism.
A `Popen(..., shell=True)` matcher belongs in `shell`; a matcher for `Popen`
without that argument belongs in `subprocess`. An API's optional capabilities
are not evidence that a particular invocation uses them.

For Windows Script Host, `WshShell.Run` with an executable path is a direct
program-start clue under `exec`; an explicit `%COMSPEC% /c` argument is a
shell-command clue under `shell`. A bare `wscript.exe` or `cscript.exe` name
is an executable-name reference, and `WScript.Shell` alone is a COM-object
reference. The Microsoft [WSH process guidance](https://learn.microsoft.com/en-us/archive/msdn-magazine/2002/may/scripting-windows-script-host-5-6-boasts-windows-xp-integration-security-new-object-model#spawned-processes)
shows the explicit `%COMSPEC%` handoff. Existing `shell/wsh` and
`shell/script-host` are overlapping legacy sources, not alternative homes for
new WSH Run rules; migrate their rules by these tests and preserve consumers.

Below `shell`, choose a consistent command-form question: interactive session,
command text, script file, or pipeline. Shell encoding/injection facts can be
referenced without creating another home for the same invocation. Existing
`batch`, `encoded`, `injection`, and language/wrapper branches need that sibling
review; their existence is not proof that they partition the parent correctly.
`shell/` itself holds no YAML while it has children, and its descendants still
share the feature `process/create/shell`. A child whose claim merely repeats
the parent's claim is not a useful split.

`launch/workspace` fails that test. Opening a bundle through NSWorkspace is the desktop opener, which is `shellexec`, and the extra segment would still be read as `launch`.

### Placement Tiebreaker

When a behavior could serve multiple objectives, place the single trait where evidence points most specifically. Composites in other objectives reference it.

| Scenario | Placement | Rationale |
|----------|-----------|-----------|
| Process injection, no further context | `evasion/process/injection/` | Stealth is the most common use; privesc/lateral composites reference it |
| Staged payload acquisition plus activation | `command-and-control/dropper/` | Repository convention; choose the required activation mechanism from the directory guide. This does not by itself establish an ongoing C2 channel. |
| Environment-variable access vs path reference | A call that reads an environment variable belongs in `micro-behaviors/os/env/read/`, even when the selected variable names a path such as TEMP. A literal or constructed temporary path without an environment-read operation belongs in `micro-behaviors/fs/path/temp/`. |
| Keylogging capability detected | `collection/keylog/` | General capture; credential-access composites reference it when combined with specific store targeting |
| Rootkit hides files/processes | `evasion/kernel-hide/` | Hides from users/admins, not from sandboxes |
| Masquerades as system binary | `evasion/masquerade/` | Deceives users/admins, not analysis tools |
| Port scanning / network recon | `discovery/network/scan/` | Gaining knowledge, not propagating |
| Brute-forcing remote services (SSH, IoT) | `lateral-movement/brute-force/` | Malware brute-forcing is about spreading to new hosts |
| Local password cracking (hashcat, john) | `credential-access/` | Cracking local hashes, not spreading |
| Killing rival malware processes | `impact/degrade/` | Destructive impact, not propagation |
| WMI process execution | `execution/` | Execution; lateral only when combined with network evidence |
| Killing AV/EDR processes | `impact/degrade/edr/` | Aggression ("I'll stop you"), not stealth; evasion/anti-av/ is for bypass |
| Bypassing AMSI or using indirect syscalls | `evasion/anti-av/` | Stealth ("don't see me"), not aggressive termination |
| Defender exclusion vs AMSI bypass vs delayed injection | `evasion/anti-av/platform/defender/` requires a Defender product exclusion or protection change; `evasion/anti-av/amsi/` requires tampering with the AMSI scanning interface; `evasion/process/injection/` requires cross-process execution transfer. | The target mechanism decides placement. AMSI is not a Defender-specific subtechnique, and delaying an injection does not by itself show AV tampering. Reference the other mechanisms from a composite only when its own objective is established. |
| Disabling/flushing firewall rules | `impact/degrade/firewall/` | Degrading system capability, not hiding |
| Hidden files in system directories | `evasion/file-hiding/` | Concealment from users/admins; a hidden file doesn't survive reboots better |
| `fork` + `setsid` without a durable activation change | `micro-behaviors/process/daemonize/` | Detachment alone does not establish restart after reboot. A durable service/boot registration belongs in persistence. |
| Reads Chrome Login Data SQLite | `credential-access/browser/` | Targets a specific credential store |
| Reads a cookie-store data field (`CookiesData`, etc.) | `micro-behaviors/communications/http/cookies/` | Neutral cookie-store field access; credential-access/exfil composites reference it |
| Extracts saved Wi-Fi profile keys | `credential-access/wifi/` | Targets a specific credential store |
| Reads `AWS_SECRET_ACCESS_KEY` from env | `credential-access/env/secrets/` | Targets a specific secret |
| Reads `os.environ` generically | `micro-behaviors/os/env/` | Neutral capability, no credential targeting |
| Generic keystroke capture | `collection/keylog/` | General capture; credential-access composites reference it |
| Chrome passwords + HTTP POST to attacker | `exfiltration/stealer/browser/` | Source + transport = exfiltration; the source names the directory |
| Chrome passwords read, never sent | `credential-access/browser/` | No transport leg — not a stealer |
| "admin" or "root" keyword | Concept-specific keyword directory, usually `objectives/discovery/account/keywords/` or a narrower objective when context supports it | Account/user concept, not credential access and not generic text |
| CLI `--help` / `Usage:` text | `micro-behaviors/ui/help/` | Help text is a user-interface behavior, not file metadata |
| Infection vocabulary | `objectives/impact/infect/` | The terms represent an impact objective, not generic content |
| File property with no behavioral implication | `metadata/` | Structural fact, not behavior |
| File property indicating deceptive intent | `evasion/masquerade/` | Deception is behavioral |

## Behavioral directory contracts

**Count depth after the tier:** in `objectives/command-and-control/reverse-shell/pty`,
`command-and-control` is level 1, `reverse-shell` is level 2, and `pty` is level 3.
This section defines ownership at those levels. Deeper levels may refine
the claim, but may not change its subject or rescue a misplaced parent. Depths
above five receive the soft review warning described in the directory budgets;
this documentation scope is not a three-level validation cap.

Read every path as an admission test: **the tier's kind of observation, about
this subject, narrowed by this behavior or mechanism**. The tables below and
the annotated tier trees define subjects; boundary tables settle collisions.
`<subject>`, `<mechanism>`, and `<entity>` denote the explicitly defined kind of
child, not literal directory names or permission to invent a catch-all.

| Tier | Level 1 answers | Level 2 answers | Level 3 answers |
|---|---|---|---|
| `micro-behaviors` | Which resource or capability domain? | Which operation, resource family, or protocol? | Which required mechanism or defined subtype of that operation? |
| `objectives` | Which unwanted result or adversary objective? | Which behavior establishes it? | Which required mechanism, target resource, or source distinguishes that behavior? |
| `metadata` | Which artifact subject? | Which part, property family, or declared field? | Which property of that same subject? |
| `well-known` | Which entity class? | Which primary function/family class, or direct entity where that tier uses one? | Which named entity, or a genuine component of an entity already named at level 2? |

At each parent choose **one** child question, not a mixture of these alternatives.
For example, `exfiltration/stealer` chooses the stolen source, while
`communications/http` chooses the HTTP operation or protocol surface. Language,
platform, file type, API spelling, evidence source, and optional corroboration
do not create parallel homes for the same claim. Put implementation variants in
filenames and independent facts in referenced traits.

For a new rule, write its supported claim before choosing a path. For a composite,
use the result established by required evidence. An optional `any` alternative
does not establish its own narrower subtype; a rule accepting several sources
is not a multi-source sweep unless it requires the sweep. If two destinations
still pass, add a deciding example and counterexample here **before** adding
the rule or directory. Do not decide by spare capacity or the location of the
sample that motivated it.

### Stealer source axis

`exfiltration/stealer/<source>` answers one question: **what information or
resource is transferred out?** It does not classify the search strategy, the
transport, the API, the implementation language, or the malware's purpose.
Keep a rule at the broadest source leaf that its required evidence supports;
make a narrower child only when it names a stable kind of stolen data and
changes the claim an analyst can make. A file path or API mention alone is not
proof of transfer, and a transport leg alone is not proof of a sensitive
source.

| Evidence establishes | Destination | Boundary |
|---|---|---|
| Browser credential, cookie, history, or extension-store contents leave | `stealer/browser` | Reading without a send leg is `credential-access/browser`; a browser API alone is a capability. |
| A named credential or secret source leaves | Its matching leaf, such as `credential`, `dev-secret`, `env`, `keychain`, `ssh`, `token`, or `wallet` | Choose the source actually required by the matcher, not an optional alternative. |
| File contents leave, with no more specific data class | `stealer/file` | A recursive search is an acquisition method; enumeration without transfer is `collection/file-targeting`. |
| Host/account/device identifiers leave | `stealer/system-info/identity` | Hostname, username, account name, machine ID, or a stable hardware identifier. |
| OS, runtime, or execution-environment facts leave | `stealer/system-info/platform` | This is about the reported host's platform, not the classifier's platform restriction. |
| Running-process inventory leaves | `stealer/system-info/process` | Process enumeration without a send leg is discovery. |
| Installed-software or package inventory leaves | `stealer/system-info/software` | A package name or dependency list is not automatically software inventory. |
| Interfaces, routes, addresses, or network configuration leave | `stealer/system-info/network` | Merely mentioning an interface supports a probable network capability or discovery claim, not theft. |
| A host report requires fields from multiple `system-info` classes, or explicitly leaves the reported host-data class open across multiple classes, with no one class defining the claim | `stealer/system-info/profile` | A generic “profile” label or one host field alone do not qualify. If one source class is required and sufficient, use that class. Alternatives spanning classes are profile, not `multi-source`. |
| A host marker accompanies a required remote command-dispatch channel | `command-and-control/backdoor/dispatch/<channel>` | The required operator task and execution define the rule; host/platform markers are supporting context. Use `stealer/system-info/<source>` only when the matcher requires probable host-data transmission rather than merely correlating host clues with tasking. |
| Two or more independent stolen source classes are each required | `stealer/multi-source` | `all` evidence must require each class. An `any` list of alternative sources is not multi-source theft. |

Use the same source-first rule for tricky neighboring names. `sweep` describes
how candidates are searched, so it is not a source leaf: transferred files go
to `file`, while an untransferred sweep stays under collection or discovery.
`surveillance` describes purpose, so classify transferred screen, camera,
audio, input, or message data by that source; monitoring without transfer stays
under collection. `phish` describes acquisition, so classify the stolen
credential or user input. A network channel, resolver, endpoint, or encoding
does not change the source. These legacy names admit no new rules and must be
emptied by source-by-source review; do not move a rule until its required
evidence supports the destination and its existing consumers are checked. The
legacy-candidate dispositions are tracked in
[`docs/taxonomy-audit/STEALER-SOURCE-PLAN.md`](docs/taxonomy-audit/STEALER-SOURCE-PLAN.md).

For example, a trait requiring both host identity and interface inventory in
one outbound report belongs in `system-info/profile`; a trait requiring only a
hostname and username belongs in `system-info/identity`. A rule accepting
either a process inventory or installed-software inventory also belongs in
`system-info/profile`: it leaves the specific host-data class open, but does
not require both datasets. If both browser
cookies and wallet data are independently required, use `multi-source`; if a
matcher accepts either one, use the broader source claim or split the rule.
The implementation language, OS, file format, and transport belong in the
filename, `for`, or referenced component traits, never in a parallel source
directory.

### Ledger operations and wallet evidence

A blockchain implementation is not a cryptographic primitive. Classify each
observation by its supported operation; a client can legitimately expose many
of these capabilities without becoming a separately identified SDK artifact.
Strings and API references can support probable capability just as calls can;
the description states which evidence was observed.

| Home | Admission and tie-break |
|---|---|
| `data/transaction/construct` | Populate transaction outputs, build instructions/messages, or estimate a transaction fee. A message-type reference belongs here even without submission. |
| `data/transaction/authorize` | Grant or describe another party's spending/transfer authority: token allowance, permit fields, delegated transfer authorization. This narrower authority claim takes precedence over ordinary construction. A maximum integer alone is not an allowance. |
| `data/transaction/sign` | Sign a required financial transaction or payment mandate. A signature over arbitrary messages/typed data, or an OR accepting those, belongs in `crypto/asymmetric/signature`. |
| `data/transaction/submit` | Submit/broadcast a transaction, extrinsic or financial order. A composite requiring construction/signing plus submission follows submission; local preparation alone does not. |
| `data/transaction/query` | Read or interpret transaction-record fields/results, including recipient-byte decoding. Live account balances and contract state are client operations, not transaction-record parsing. |
| `communications/blockchain/client` | Ledger-client operations such as balance, contract and state queries; existing chain-specific RPC composites remain here. Offline keys, a brand, a provider import or endpoint alone does not establish client use. |
| `communications/http/url/rpc` | Ledger explorer/RPC endpoint references without a required operation. An ordinary price-feed URL belongs in `url/endpoint`, not here. |
| `communications/http/services/payment` | HTTP payment-gating interfaces, payment headers, resource servers and payment-payload validation. Transaction-specific cryptographic signing follows `data/transaction/sign`; a generic privacy wrapper alone is insufficient. |
| `crypto/asymmetric/key` | Private-key/keypair loading, generation, reconstruction or derived public keys/accounts, regardless of wallet or implementation. Do not describe every factory as derivation or every wallet constructor as a private-key import. |
| `ui/controls/wallet` | Wallet connection, recovery-phrase, signing and reward/balance interface text. Prompts do not themselves establish key acquisition, signing or reward submission. |

**Capability is not a library exemption.** Do not use a whole blockchain,
wallet or crypto capability directory as proof that a file is a benign library.
The word `wallet`, a public RPC URL, key parsing, or an ordinary transaction API
may occur in malware. Exclusions must name the actual alternative explanation
and have evidence for it. Review consumers when moving these observations:
retaining every old capability as an identity exclusion perpetuates false
negatives; widening to a whole destination creates new ones. Identity evidence
must identify the analyzed artifact; it is not synonymous with embedded use.

### Mnemonic key material and recovery interfaces

`crypto/mnemonic` owns mnemonic representations of cryptographic seed material:
wordlists, phrase construction/generation, phrase validation, and distinctive
phrase identifiers or implementation references. It is not a library layer or
a synonym for key derivation. A wordlist can encode entropy without running a
KDF; a mnemonic can exist without a blockchain connection. BIP-39 explicitly
separates [mnemonic generation from seed derivation](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki#generating-the-mnemonic). Preserve these
observations across source, scripts and binaries in the same leaf.

- Producing/loading a private key, a wallet keypair, or a hierarchical key path
  belongs in `crypto/asymmetric/key`. A phrase-specific operation follows
  `crypto/mnemonic`; an OR accepting either phrases or keypairs uses the broader
  key-material claim and must not be described as phrase-only generation.
- PBKDF2 calls/parameters follow `crypto/kdf`; a bare `self.wordlist` member
  follows `data/collection/wordlist`, because it could be an ordinary dictionary.
  A composite tying that wordlist to mnemonic and PBKDF2 evidence can support
  mnemonic implementation presence without identifying an independent library.
- Recovery UI labels, seed-word entry grids, textareas and invalid-phrase text
  belong in `ui/controls/wallet` when wallet/seed-phrase context is supported.
  Phrase assembly itself follows `crypto/mnemonic`. A UI prompt does not imply
  capture for an attacker; acquisition/export composites must supply that context.
- Bitcoin WIF is a private-key representation (`crypto/asymmetric/key`), not a
  mnemonic. Ethereum UTC keystore names are wallet file locators (`fs/path/wallet`).
  Neither alone is theft. Secret-source consumers may reference their precise
  observations without putting neutral atoms back in an objective tier.
- Seed-phrase words are content clues, not file metadata. A bare `seed` function
  name, maximum integer, or unqualified address variable does not establish a
  mnemonic or a blockchain technique. Do not fill this leaf with those remnants.

### Implementations and library fingerprints

**Classify implementation fingerprints by the supported technique whenever
possible.** Static linking, dynamic linking, vendoring, a runtime helper and a
handwritten implementation are evidence/implementation differences; they do not
create separate AES, HTTP, archive, string or process-creation techniques.
Keep language and backend in the filename, trait name and description.

| What the matcher establishes | Placement and description |
|---|---|
| Embedded AES tables or an AES-specific implementation signature | `micro-behaviors/crypto/symmetric/aes`, refined by the actual mechanism where needed; describe “contains an AES implementation,” not “encrypts files.” |
| A native crypto-provider reference without a supported specific algorithm or payload purpose | `micro-behaviors/crypto/native/`; describe the API reference or co-occurrence as evidence of probable crypto capability, not as proof that a fallback ran, a payload was encrypted, or a named algorithm was used. A declared dependency alone is metadata; a fingerprint of the analyzed library itself is `well-known/lib/`. |
| A generic cipher construction name or API reference with no proven algorithm or key type | `micro-behaviors/crypto/cipher/`; keep it separate from `symmetric` and `asymmetric` until evidence supports one. A bare `Cipher` name is a weak clue, not proof of encryption or payload decryption. |
| Embedded zlib inflate implementation or its specific API | `micro-behaviors/data/decompress/zlib`; do not claim compression or execution when only decompression capability is supported. |
| A library-specific HTTP request or string operation | The corresponding HTTP/string operation, alongside other implementations of that operation. |
| A fingerprint supporting a known capability group but no narrower operation | That capability group's documented observation, if a valid home exists. Do not invent an algorithm or create `library`, `wrapper`, or `implementation` as a remainder bucket. Factor broad roll-ups into their supported canonical observations. |
| Only a dependency declaration, upstream attribution, runtime requirement or linkage fact, without evidence of an implementation's presence | Its metadata subject. A provider name alone must not establish AES, RSA, TLS or another specific operation. An implementation-specific signature that does establish embedded code instead follows its supported capability above. |
| The independently identified library/package/source artifact itself | `well-known/lib/<function>/<entity>`, with evidence of that artifact identity. A separately analyzed library member of an archive can qualify; a marker in its enclosing application does not make the application that library. |

`well-known` is not the default destination for all embedded implementation
markers. Some existing rules already mix artifact identity and embedded-code
presence; migrate those by their claims rather than treating the mix as the
contract. Do not change a broad identity exclusion into an exclusion for every
file using the corresponding technique: a malicious program can contain
ordinary AES, HTTP and compression implementations. Preserve specific benign
context through reviewed named `exception` composites where warranted.

**Test a suspected implementation layer:** replace the library/backend with a
different implementation while preserving the observed operation. If the
directory would change solely because of that replacement, the level is not a
subtechnique. `crypto/library`, `http/lib`, `aes/runtime-library`,
`string/library`, and `process/create/stdlib` fail this test and are closed to
new implementation-based splits. Renaming `library` to `framework`, `provider`,
`wrapper` or `runtime` does not fix it. `crypto/library/blockchain` also mixes
domains: cryptographic primitives stay in crypto; ledger RPC, transaction data
handling and wallet interfaces follow their supported communication/data/key
operations. Do not just promote the entire contents to `crypto/blockchain`.

The word itself is not globally forbidden. `fs/path/library` can mean a path to
shared-library files; `os/env/runtime` means runtime configuration variables;
`os/security/auth/provider` can mean an authentication-provider interface.
These name the observed resource or mechanism. Likewise `well-known/lib` names
an entity class. Check the parent-child claim, not a universal word blacklist.
Even a valid subject needs cleanup: `/Library/Caches` is a cache, not a library
binary merely because an ancestor directory is named `Library`.

The [implementation-layer audit](docs/taxonomy-audit/IMPLEMENTATION-LAYERS.md)
records current source directories, concrete destinations and reference risks.

### Capability domain ownership

These contracts apply to every child of the named level-1 directory, including
children omitted from the illustrative trees. A familiar API or library name
does not override the operation its matcher actually observes.

| Level-1 directory | Admission and child question | Boundary |
|---|---|---|
| `browser-extension` | Extension-host operations that have no technology-neutral equivalent: action, lifecycle, management, tabs. Children identify that host surface. | Storage, messaging, HTTP, scheduling, and injection use their capability homes. Manifest authority uses `metadata/permission`. Engine-emitted host/permission IDs are covered below. |
| `communications` | Exchanging data, addressing peers, or manipulating a communication protocol. Level 2 names the protocol or transport facility; level 3 names its operation/surface. | Local interface inspection or configuration is `network/interface`; passive file format facts are metadata; attacker control or theft needs an objective claim. |
| `crypto` | Cryptographic primitives, keys, derivation, hashes, and certificate operations. Children refine primitive family then algorithm/operation. | Encoding is `data/encode` or `decode`; randomness is `os/random`; certificate contents are `metadata/signed`; named-library identity is `well-known/lib`. |
| `data` | Transforming, interpreting, organizing, or operating on data. Children identify an operation and its algorithm/format/mechanism. | Mere data presence is metadata. Source location, language, or intended consumer is not a second transform. |
| `dylib` | Native shared-library loading, enumeration and loader lookup. Children identify the loader operation. | Language module loading is `os/module`; manual address resolution is `os/api-resolution`; a named API goes with its function. `dylib/library` is a legacy mixture: dependency facts use metadata, embedded capabilities use their techniques, independent library identities use well-known/lib. |
| `fs` | Filesystem objects, paths and operations. Children identify the resource or operation, then its mechanism or resource subtype. | File contents are classified by what they establish; a sensitive path literal does not prove theft. Raw hardware interaction is `hardware`. |
| `hardware` | Direct device access, input/output, capture, or control. Children name the device family then operation. | Querying host properties is `os/sysinfo`; manipulating windows/widgets is `ui`; ongoing surveillance needs collection evidence. |
| `mem` | Address-space allocation, access, protection, mapping and management. Children name the memory operation then its mechanism. | Cross-process execution transfer is not established by allocation/write alone. Compression remains `data` even when performed in memory. |
| `network` | Local network interfaces and their identity, address, and state. Children name the network resource or operation. | Protocol exchange and peer communication belong in `communications`; a probable interface capability clue alone does not establish discovery intent, which belongs in `objectives/discovery/network/`. |
| `os` | Operating-system facilities with no more specific resource home: registry, services, accounts, authority, environment, kernel, packages. Children name the facility then operation. | File/process/network operations retain their specific homes even when accessed through an OS API. |
| `process` | Execution contexts, lifecycle, control, identity, arguments and I/O. Children name the operation then its mechanism. | Permissions use `os/privilege`; runtime identity is `well-known/lib`; durable activation is persistence. |
| `time` | Reading time, waiting, measuring elapsed time, or arranging callbacks. Children distinguish query, sleep, timing and scheduling. | OS task/service registration is `os/autorun` or `os/service`; an analysis-evasion gate needs an objective composite. |
| `ui` | Presenting information or managing user-interface elements. Children name the UI surface then operation. | Display hardware/capture is `hardware/display`; deceptive interaction requires an objective; a help string is a UI observation, not a program identity. |

### Communications: operation before implementation

Use a specific protocol operation before a lower transport when that operation
is required. A generic `connect` is a socket fact; a complete HTTP request does
not acquire a second home merely because it uses a socket underneath.

| Competing directories | Deciding evidence and canonical home |
|---|---|
| `socket/{create,bind,listen,connect,send,receive}` vs `socket/{tcp,udp}` | An explicit operation wins. Transport-only APIs/constants without an operation use the transport subject. `dial`, `wrapper-connect`, and `state-connect` are not independent connection operations. |
| `http/client`, `http/request`, verb leaves | Method-specific request → `http/{get,post,put,patch,delete,head,options}`; method-unspecified request/client use → `http/client`. `request` must not duplicate the latter. |
| `http/upload` vs `http/post` | A file/attachment transfer mechanism → `upload`; POST without that evidence → `post`. POST alone is not file upload or exfiltration. |
| `http/download` vs `http/get` | Retrieving a response as an artifact/file → `download`; GET alone → `get`. A downloader requires neither execution nor attacker control. |
| `http/download/fallback` | A conditional retry or ordered alternate downloader after failure/unavailability belongs in `download/fallback`. A multi-client marker without a matched order supports fallback capability, not proof a retry occurred. Neither fallback nor generic download establishes payload activation; a dropper must add staging-to-sink evidence. |
| `http/header`, `authorization-header`, `body`, `query` | Classify the particular field's meaning first: authentication → its auth subject; User-Agent → `user-agent`; cookies → `cookies`; otherwise use the HTTP surface. A raw header token does not prove a request or a login. |
| `http/oauth`, `device-code`, `token-auth`, `jwt`, `basic-auth`, `auth` | OAuth grant acquisition/refresh, including device authorization → `oauth`; presenting a bearer token → `token-auth`; JWT structure/processing → `jwt`; Basic credentials → `basic-auth`; `auth` only when the mechanism is not established. Mechanism-specific leaves take precedence. |
| `http/cookies`, `cookie-store`, `cookie-name` | HTTP cookie operations and protocol fields → `cookies`. A cookie-jar path → `fs/path/cookie`; credential/session extraction requires its own objective. Consolidate competing spellings by this distinction. |
| `http/services` vs a protocol operation | A named remote service endpoint without an operation → `services`; an operation tied to that endpoint → the operation's directory. A vendor CLI invocation is not automatically HTTP. |
| Cloud metadata endpoint vs cloud credential/path evidence | Provider-specific host and request-path clues → `http/services/<provider>/metadata`; a shared metadata address with no provider-specific path → `http/services/cloud`; provider request headers such as `Metadata-Flavor` or `X-aws-ec2-metadata-token` → `http/header/custom`. Environment-variable names → `os/env/cloud`; local credential/config paths → `fs/path/credential`; SDK import or query-call clues follow the named provider capability. These are content clues: they suggest probable capability, but do not prove a request, read, or credential access. |
| `communications/url` vs `http/url` or `http/query` | Generic URL construction/parsing/reference → `url/{construction,parse,reference}`; HTTP request parameter handling → `http/query`. Endpoint identity follows the service/resource it identifies. |
| `communications/transfer` vs a protocol operation | Protocol-neutral evidence of sending/uploading/transferring data → `transfer`; when the matcher identifies HTTP, FTP, messaging, DNS, or another protocol, use that protocol's operation. Language clues such as upload wording indicate a probable transfer capability, not proof that bytes left the process. |
| `http/url/github` vs a dropper sink | A raw GitHub URL or filename suffix, including `.png`, is neutral endpoint text and belongs under `http/url/github`; a suffix does not establish response bytes or steganography. Put a composite that requires a staged payload to be activated by an assembly/module loader under `dropper/module-load`, referencing the URL clue. |
| `communications/ip` vs `network/interface` vs `objectives/discovery/network` | Address syntax, literals, construction, or parsing → `communications/ip`. Local interface identity/address/state evidence, including a distinctive name, API reference, or query command → `micro-behaviors/network/interface`; this suggests capability and does not alone establish hostile reconnaissance. Active remote probing or a multi-signal network survey that supports an intent inference → `objectives/discovery/network`. |
| `dns/lookup`, `dns/txt`, `resolver`, `server` | Generic name-resolution APIs and operations without record-type-specific behavior → `lookup`; querying, parsing, or handling TXT records → `txt`; configure/select resolver infrastructure → `resolver`; receive/respond to DNS queries → `server`. TXT is already a lookup, so do not repeat `lookup` in the feature name. A DNS label/domain literal alone does not prove any of these operations. |
| `communications/ipc` vs network messaging | Local process/host bridges, pipes, shared-memory messaging and native-host channels → `ipc`; remote messaging protocols → `messaging` or the named protocol. IRC is a network protocol, not IPC merely because it transmits messages. |
| Native-host setup vs remote staging | Native messaging permission, an install callback, local storage writes and an install message remain separate neutral observations. A stored URL or comment about a helper does not prove a request, registration write or execution. Remote-command/staging objectives require the additional tasking, acquisition or execution relationship; missing helper code must not be supplied by inference. |
| `communications/mcp` vs agent configuration | MCP negotiation, tool/resource listing and invocation → `mcp`; a config field naming an MCP server is metadata. A tool exposing a shell references canonical process traits. |
| TLS under HTTP vs socket TLS | Generic TLS handshake, validation and encrypted transport belong with socket TLS (`socket/ssl` currently); an explicitly HTTP-only integration may refine HTTP. Duplicate TLS APIs do not belong in both `http/ssl` and `http/tls`. Certificate facts use metadata; certificate operations use crypto. |
| `proxy/{socks,tunnel,relay,reverse}` vs C2 | Required SOCKS protocol → `socks`; establishing an encapsulated channel → `tunnel`; forwarding over an existing channel → `relay`. Direction alone does not establish attacker control; combine it with the required mechanism, rather than duplicating a relay under `reverse`. |

Other protocol families (SSH, FTP, email, WebSocket, RPC, industrial protocols)
use their protocol-specific operation as the child: connection, authentication,
read/receive, write/send, server handling or configuration. A generic byte-copy
loop remains generic I/O unless protocol evidence is required. Product, SDK,
OS and language names are not alternative operation leaves.

### Data, files, memory, and code loading

| Competing directories | Deciding evidence and canonical home |
|---|---|
| `data/encode` vs `decode` vs `metadata/file/encoded` | Required direction of transformation chooses encode/decode; encoded material merely present is metadata. A library import supporting both directions is one capability observation, not two claims that both operations ran. |
| `data/{encode,decode}/<algorithm>` vs origin/spelling variants | Base64 remains `base64` whether the input is an HTTP body, environment value, native call or reflected method. Repeated decoding is a real refinement; `symbol-base64` and `request-base64` are not different algorithms. |
| Decoder matcher backends and API variants | Symbol/call facts, source text and compiled method names for the same decoder share its algorithm leaf. `decode/symbol-base64` is retired; preserve an old subtree consumer as named alternatives, not a reference to the broader destination. Equivalent API spellings can share a matcher when their scope and meaning agree. Review consumers that intentionally selected one variant before broadening them. A generic method name such as `DecodeString` does not identify Base64 without its package or receiver context. |
| Codec operations vs imports, alphabets and output | A decoder/encoder operation or direction-specific API reference belongs with that direction. Importing a module that provides both directions belongs in `metadata/import/package`; an alphabet constant belongs in `metadata/file/string/charset`. A generic file-write method belongs with file writes, even when its caller previously decoded data. Consumers may combine these observations, but an import, alphabet or write alone must not satisfy a decoding aggregate. |
| Arithmetic vs codecs, formatting and branching | Numeric calculations, shifts, masks and bitwise combinations → `data/arithmetic`; constructing a textual number representation → `data/format/string`; conditional execution → `data/control-flow/branch`. Generic shifts, binary formatting, or a nearby alphabet do not establish a codec or its direction. A hexadecimal literal in a condition does not by itself establish a threshold comparison. Arithmetic has the same home in source and compiled code; `data/source/arithmetic` is retired. |
| DOM construction, XML typing and codec direction | Generic DOM node creation, traversal and mutation → `data/collection/dom`; XML parser class/API references → `data/parse/xml`; XML node data types and typed-value properties → `data/format/xml`. Browser rendering or window interaction needs browser-specific evidence and belongs in UI. XML object serialization remains `data/serialize/xml`. `nodeTypedValue` is read/write and supports non-Base64 types: require a bound Base64 text-to-bytes sequence for decoding, or bytes-to-text sequence for encoding. An arbitrary element name such as `Base64Data` establishes neither XML nor a codec. |
| Generic DOM vs browser UI | Element/node construction, insertion/removal, selectors, XPath, tree walkers and node text/attribute operations belong in `data/collection/dom`, including when found in browser code. A variable named `document` or `node` does not establish a browser window or traversal relationship. UI placement requires an additional browser/window/page-specific subject, such as window visibility, user interaction, page rendering or active-tab access. A nearby walker and assignment are separate observations until their receiver/data flow is bound. Language and DOM implementation stay in scope/filenames. |
| Encoding families vs mixed transformation umbrellas | Base16 belongs with `decode/hex`, Base32 with `decode/base32`, ASCII85/Z85 with `decode/base85`, and standard/URL-safe Base64 with `decode/base64`. Joining decoded pieces belongs with string assembly. `decode/encoded` is retired: encoding, compression and object serialization are different subjects. Consumers needing alternatives across them should reference the named observations rather than invent a shared decoder category. |
| `data/compress` vs `decompress` vs `archive` | Reducing a byte stream → compress; expanding it → decompress; accessing or creating a member container → archive. ZIP member extraction is `archive/extract`; using raw deflate is the corresponding compression direction. |
| `data/serialize` vs `parse` vs `format` | Object ↔ representation codecs (JSON, YAML, protobuf, pickle) → `serialize/<format>`; lexical/grammar/query interpretation → `parse/<grammar-or-operation>`; specialized format handling without a more specific operation → `format/<format>`. File format identity alone is metadata. |
| JSON conversion vs computed calls or expression evaluation | `JSON.parse(Buffer.from(...))` is JSON deserialization; it implies Base64 only when the Buffer operation requires that encoding. A computed Buffer method-call chain belongs with dynamic dispatch until its method and encoding are established. `eval("(" + expression + ")")` is expression evaluation, not necessarily JSON conversion or safe code. Nearby encoding labels and unrelated `toString` calls do not establish a conversion chain. |
| `data/string`, `buffer`, `collection`, `control-flow`, historical `data/source` | String-value operation → string; byte/storage operation → buffer; collection/element operation → collection; execution-path construct → control-flow. Source code is the matcher’s evidence, not a subject: classify the analyzed program’s operation/technique it establishes. AST operations → `metaprogramming/ast`; runtime reflection → `metaprogramming/reflection`; code shape without an operation → `metadata/code`. Never choose a directory by source-vs-compiled representation or language; put those constraints in rule scope. |
| `metaprogramming/ast` vs `data/parse` | The analyzed program constructs, traverses, inspects or mutates a program AST → `metaprogramming/ast`; parsing data formats/grammars unrelated to program structure → `data/parse` or `data/format`. An AST used only by the analyzer to inspect a sample is evidence format, not a behavior to classify. JSON used to transport an AST does not by itself make the operation an AST technique. |
| Source parsing vs AST manipulation | A program that parses source into an AST uses `metaprogramming/ast`; classify parser tooling used only by an analyst as evidence, not behavior. Formatting or emitting generated code is `metaprogramming/generation`; a composite may require AST parse, output formatting and a file write to claim code generation. These homes are independent of whether the same technique appears in source code or compiled artifacts. |
| `metaprogramming/reflection` vs dynamic loading/evaluation | The analyzed program discovers types/members or invokes them reflectively → `metaprogramming/reflection`; loading a module or evaluating source/bytecode → the corresponding load/evaluation capability. A language-specific API matcher belongs in that neutral technique leaf with its language in `for:`. |
| `communications/http/direct-socket` vs `communications/http/client` vs `communications/socket` | Hand-built HTTP request/message over a directly connected socket → `http/direct-socket`; a platform or library HTTP client API → `http/client`; socket connect/listen/stream behavior without HTTP semantics → `communications/socket`. The protocol of the message determines the first placement even when the transport is a raw socket. A socket plus an HTTP token alone does not establish a shell or malicious command channel. |
| `communications/rpc` vs `data/transaction/query` | RPC method names, request batches, and remote-procedure transport → `communications/rpc`; interpreting fields or reconstructing values from a retrieved ledger transaction → `data/transaction/query`. A configured endpoint alone is URL/configuration evidence; it does not prove a request or transaction operation. |
| Blockchain-client behavior vs blockchain-related identifiers | A client behavior requires evidence of an operation against a blockchain interface: a chain-specific RPC request/query, a contract/log read, or a transaction operation tied to a ledger protocol. Put atomic observations with their operation (`communications/rpc`, `data/transaction/*`, `crypto`, or the relevant wallet/provider interface); place operation composites that establish client use under `communications/blockchain/client/`, where the directory feature aggregates them. A package import, SDK/library fingerprint, chain name, endpoint string, wallet-provider method vocabulary, or offline key derivation alone does not establish client behavior. A transaction signing primitive without chain-specific transaction context remains crypto; an endpoint without an operation remains URL/configuration. Malware objectives may reference precise client operations, but must add the malicious purpose (for example, retrieving C2 data or unauthorized transfers). |
| `communications/ip/literal` vs network objectives | A parsed or literal address, including RFC1918/private ranges, is neutral endpoint evidence → `ip/literal`; require connection direction, protocol, and the behavior carried over it before assigning C2 or hostile intent. Private-address identity alone is not a command channel. |
| Code-generation API vs code-generation library fingerprint | A call/construction that performs code or bytecode generation → `metaprogramming/generation`; a reference to a framework specialized for that technique may also live there, but must say “reference” and must not assert generation occurred. A scan of the library artifact itself uses its `well-known/lib` identity. |
| `data/db/<engine>` vs operation children | Engine-specific protocol/API without a specific operation uses the engine; a required query/delete/schema/backup operation uses that operation, with engine in the filename. A targeted credential table adds a separate objective claim. |
| SQL syntax vs schema operations | Catalog/table/column introspection → `data/db/schema/introspection`; table definitions and relational column declarations → `data/db/schema/relational`; stored functions, procedures, triggers and their language bindings → `data/db/schema/stored-code`. These operations keep the same home across SQL dialects and API spellings. A SELECT against a schema catalog is introspection; a SELECT against application records is data access. A column name alone does not prove a relational schema, and a password column plus assignment does not prove plaintext storage. Generic SQL syntax and command references remain in `data/db/sql` pending operation-specific migration; it is not an alternative home for established schema operations. |
| Database row mutation vs schema destruction | Deleting records or truncating table contents → `data/db/delete/row`; deleting a table/database/schema object → schema destruction, not row deletion. Inserting or assigning record values → `data/db/write/row`. A password-column declaration and SET assignment do not establish whether the value is plaintext or hashed. A generic static `truncate()` call belongs with method dispatch until a database receiver is established; a `clearAllLogs` symbol alone is telemetry naming, not proof of deletion. |
| SQL mutation placement | INSERT, UPDATE and REPLACE row-operation syntax → `data/db/write/row`; DELETE and TRUNCATE record-removal syntax → `data/db/delete/row`; DROP TABLE/VIEW/INDEX/DATABASE/SCHEMA syntax → `data/db/schema/delete`. These homes are independent of SQL dialect, source language and matcher backend. Deleting records preserves the storage object; dropping it destroys a schema object. Keep literal-only, clause-qualified and broad token predicates distinct when their supported claims or scope differ. |
| SQL context vs unrelated observations | Unrelated database evidence must not decide whether a command label or language construct exists. Command/status vocabulary → `metadata/file/string/command`; a comma expression → `data/control-flow/sequence`; delimiter removal through split/join → `data/string/replace`. None independently establishes remote control, concealment or payload execution. Intent-bearing consumers must require their own supporting operations rather than treating absence of SQL as malicious evidence. |
| Account vocabulary vs credentials, schemas and telemetry | User/account identifiers, names, email and membership/activity labels without a required operation → `metadata/file/string/account`; authentication-secret labels or token values → `metadata/file/string/credential`. A required object structure, parsed field, or value mapping belongs with the corresponding structured-data observation; a quoted label or label followed by a colon alone does not establish an object or assignment. Relational definitions require database syntax. Telemetry vocabulary requires a monitoring/analytics subject; an account label alone is not telemetry. A set of labels does not establish a shared record, key relationship, collection or transmission. |
| Object properties vs named vocabulary | Required member/subscript access → `data/property/access`, independent of language or representation; a generic `.get()` call without a resolved receiver → `data/control-flow/dispatch`. Object-definition/key syntax → `data/serialize/schema-object`; an exported module interface → `os/module/export`. Bare names follow their subject: account/contact labels → `metadata/file/string/account`, device-property labels → `metadata/file/string/device`, generic named code identifiers → `metadata/file/string/identity`. A member node alone need not prove a read rather than a write; descriptions must state the access the matcher actually establishes. `data/source/property/identity` is retired, not a second home for these observations. |
| Property operations and computed calls | Member lookup or access → `data/property/access`; assigning a property value → `data/property/assign`; defining a descriptor or accessor → `data/property/define`; enumerating keys or entries → `data/property/enumerate`. Invoking a selected member or constructor → `data/control-flow/dispatch`, whether selected directly, by brackets, or by a function result. A computed key does not prove decoding; arguments `0` and `false` do not prove a hidden process. Name the operation rather than retaining `source/property`, `computed` or `transition` as competing homes. Buffer allocation, loops, conditional expressions, array operations and module exports retain their own subjects even when exploit composites combine them. |
| Generic Run/argument syntax vs shell execution or obfuscation | A method named Run, indexed invocation, numeric/Boolean arguments, or arithmetic argument expressions → `data/control-flow/dispatch` until the receiver and operation establish a shell/process launch. The number 2 alone does not establish file overwrite. Addition in a subscript and WScript bracket access → `data/property/access`; ordinary indexing or host API access is not obfuscation. Functions choosing a method, argument or constructor do not establish decoding without a transformation. Exact objective consumers may combine these neutral observations with their own required evidence; broad shell/obfuscation references must not treat the neutral syntax itself as the claimed operation. |
| Collection shape and arithmetic vs encoding, reconstruction and timing evasion | Nested array literals → `data/collection/array`; nesting alone establishes no lookup, codec or obfuscation. Identifier subtraction and `+=` assignment → `data/arithmetic`; without operand types or bindings, neither proves date measurement nor string reconstruction. Date calls → `time/query`. Timing evasion requires evidence of an analysis-dependent timing decision. Nearby initialization, addition and eval establish co-occurrence only; they do not identify a malware family or prove a shared accumulator. |
| Function measurements vs runtime indirection or padding | Function counts, anonymity, constant-return counts and ratios → `metadata/file/function`; the subject measured chooses the directory, not a threshold or suspected obfuscator. Function-selected keys → `data/property/access`; a function call producing a key does not establish decoding. Computed invocation patterns → `data/control-flow/dispatch`; hex-shaped tokens do not prove numeric offsets when the matcher also accepts identifiers. Objective consumers must supply the evidence for concealment or padding. |
| Hexadecimal notation vs encoding and concealment | Numeric token text and incomplete bracket/number prefixes → `metadata/file/literal`; they do not establish a decoder, mixed radices, byte range, or an array literal. Binary operations between hexadecimal operands → `data/arithmetic`; indexing by a hex key or identifier-plus-hex expression → `data/property/access`, without asserting the receiver is an array. Actual representation conversion belongs with its codec operation. Concealment requires additional evidence beyond the radix spelling. Filename extensions belong in `metadata/file/extension/identity`, including when used as exclusions. |
| Indexed values, collection methods and lexical array-like shapes | Unbound indexed reads and bracket chains → `data/property/access`; assignment between indexed values → `data/property/assign`; addition between indexed values → `data/arithmetic` without claiming numeric or string types. Sort/fill method syntax → `data/collection/array`; join with a short string argument → `data/string/concat`, without assuming the argument is a delimiter. Byte-buffer construction and zero initialization → `data/buffer/alloc`; a random index calculation → `os/random/prng/stdlib` without claiming an element was accessed. Method-name strings and bracket/URL prefixes → `metadata/file/literal`; bracketed Base64-like strings → `metadata/file/encoded` without claiming a codec operation. `data/source/syntax/array` is retired; do not recreate a source-representation bucket. |
| Symbol repetition vs character conversion vs decoding | Repeated `indexOf` symbols → `metadata/file/naming`: a name count establishes neither a string receiver nor a decoder. Repeated `charCodeAt` near `String.fromCharCode` arguments → `micro-behaviors/data/string/conversion`. Decoding requires evidence of the representation being decoded; concealment requires additional context. |
| Structural profiles vs intent and generated provenance | A conjunction of long lines, opaque identifiers and missing comments describes line layout (`metadata/file/line`), not npm malware. Repeated character conversion with line/name constraints stays in `data/string/conversion`; it does not prove a decoder. Bare `Search.setIndex` text belongs in `metadata/file/literal`, unlike a format-specific generated-index signature in `metadata/build/generated`. Do not let a weak reference inherit the broad build exclusions. A disjunction of unrelated counts does not identify an obfuscator; a package having tests does not establish exfiltration. Retire unsupported aggregates rather than inventing a directory for their claims. |
| Binary string counts, compiler symbols and graphics declarations | Counts of extracted or high-entropy strings across a binary belong in `metadata/file/string/count`, including threshold-specific observations (one to five is not zero); they do not identify a section, an obfuscated blob or a trojanized backdoor. Compiler ABI/runtime symbol prefixes belong in `metadata/binary/symbols/compiler`. Import-kind graphics API declarations belong in `metadata/binary/symbols/imports`; graphics vocabulary, including library filename/path text, belongs in `metadata/file/string/graphics`. Neither proves a drawing operation or library loading. Embedded implementation fingerprints that actually establish a graphics technique remain behavioral evidence; broad library-name or symbol declarations must not acquire that stronger claim. |
| Graphics vocabulary, declarations and provider identity | Graphics API/backend/driver words and filename/path references → `metadata/file/string/graphics`, taking precedence over generic filename text in `file/string/file`; end-user product names remain `file/string/application-name`. Parsed imports → `metadata/binary/symbols/imports`; exported provider interfaces → `metadata/binary/symbols/exports`; declared SONAME and provider/interface conjunction → `metadata/binary/linking/runtime`. Mesa artifact identity requires corroborating provider and Mesa/DRI evidence in `well-known/`; words alone do not establish it. Actual drawing operations remain behavioral evidence. |
| WebAssembly declarations vs language attribution | Parsed export names belong in `metadata/binary/symbols/exports`, even when queried through a value array; arbitrary name text is not an export. An unspecified producer record belongs in `metadata/binary/provenance/build`. Corroborated compiled-language attribution can reference those facts from `metadata/lang/compiled`; one helper name or producer-record presence does not by itself establish a language. WASM is rule scope, not a new directory axis. |
| Account properties vs accounting vocabulary | `metadata/file/string/account` owns user/account identifiers and profile fields. `metadata/file/string/accounting` owns literal vocabulary for login-session and process-usage records, including accounting headers/configuration; it does not imply header inclusion, portability or file operations. Concrete accounting log paths belong in `micro-behaviors/fs/path/log/accounting`; destruction intent belongs in `objectives/evasion/indicator-removal/accounting`. A shared spelling stem does not make these subjects synonymous. |
| TLS operations vs vocabulary and generic I/O | Bare security labels such as `domain_intel` belong in `metadata/file/string/security`; they establish neither TLS use nor benign scanner identity. Generic NSPR read/write/send/receive references belong in `process/io/stream` when the matcher cannot distinguish backing or encryption. TLS classification requires TLS-specific evidence; context creation alone does not establish a connection, and warning suppression alone does not establish disabled verification. |
| TLS verification vs HTTP and sockets | `communications/tls/verify/disable` owns explicit peer-certificate/hostname verification-disable APIs and settings, including client-library forms. Ordinary context creation, custom trust callbacks, warning suppression and a selectable insecure-mode option do not belong there. HTTP requests own HTTP mechanics; socket creation/connect/accept own transport endpoints. An API backend does not give a TLS observation a second HTTP/socket home. The retired `http/ssl` leaf must not be recreated; remaining legacy TLS observations are audited by operation before moving. |
| TLS initialization vs connection and verification | `communications/tls/initialize` owns creating configuration or per-connection state and selecting the initial client method. Preserve object distinctions in trait names; SSL_new state is not TLS session resumption. Setup does not establish a connection, negotiate a handshake, or disable verification. Those operations need their own evidence; do not use an OR of constructors as a connection claim. |
| Diagnostic warnings vs TLS verification | Warning emission/filtering/suppression belongs in `os/telemetry/logging/warning`, even when the warning concerns an insecure request. A warning filter does not disable certificate or hostname checks and does not establish HTTP activity. Consumers requiring suppression must reference its exact atoms because the warning leaf also admits emission. |
| Argument-byte characteristics vs resolved API operations | Encoded register-load/call shapes without a bound callee belong in `metadata/binary/code/arguments`, with architecture in scope/filenames. Name the observed bytes, not inferred API semantics. An import elsewhere does not resolve the matched call; an operation-specific claim requires that target and its argument evidence. The metadata leaf does not guarantee instruction alignment or execution. |
| Binary packing vs DNS construction | Generic format-driven record serialization belongs in `data/serialize/binary`; known integer widths, byte order and length fields belong in `data/buffer/integer-codec`. A `struct.pack` format such as `!HHIH` or `!HBB` specifies a layout, not a DNS record identity. DNS consumers reference the canonical packing observation and supply the protocol evidence. Using an AST or symbol matcher does not create an `ast` technique. |
| Length framing and ASCII encoding vs DNS labels | A length expression belongs with integer framing; ASCII conversion belongs in `data/encode/charset`. Their co-occurrence does not establish DNS or exfiltration. A coherent dotted-label encoder must bind each label to its own length and encoded bytes. DNS wire construction remains a neutral capability; a transfer objective needs additional evidence. |
| Domain-like formatting vs DNS transfer | Formatting dotted fields and a domain-like suffix belongs in `data/string/concat`; it does not prove resolution or transmission. A nearby binary-packing operation does not supply that missing relationship. `objectives/exfiltration/dns/ast` is retired: matcher backends do not define behavioral categories. Actual AST manipulation belongs with its operation. |
| Domain variable names vs channel behavior | Assignment text using names such as `beacon_domain` belongs in `metadata/file/string/domain`; the author's vocabulary does not prove a beacon or transfer. HTTP URL construction belongs in `communications/http/url/build`. Independent hex conversion and a templated hostname do not establish that the encoded value is placed in the hostname; an objective must supply that relationship and its intent evidence. |
| Literal limits vs truncation | `metadata/file/string/limit` owns text naming a numeric bound, such as `max_length=63`, without evidence that the bound is applied. It does not own measured file/string sizes or actual truncation operations. A DNS-sized constant plus a variable-shaped curl URL does not establish label truncation or exfiltration. URL structure belongs in `communications/http/url/build`; an actual truncation belongs with the string operation. |
| Generic options vs service operations | `metadata/file/string/traversal` owns recursion/traversal option vocabulary without an operation; `metadata/file/string/limit` owns literal per-page counts without evidence of pagination. Neither `recursive=true` nor `per_page=20` identifies GitHub. A bare `/graphql` literal belongs in `communications/http/graphql`, independent of provider. Service-specific composites must add the service evidence explicitly; generic options must not inherit service-wide suppression or intent claims. |
| Service endpoint vs mutation | A shared collection path such as GitHub `/user/repos` establishes an endpoint reference, not listing or creation. Creation requires an explicit creation method/route or supported API call. A version header plus `auto_init` does not establish a request; unrelated method and path arguments to an unresolved helper do not establish its destination. Keep endpoint observations available without promoting them to mutations through an OR composite. |
| Contents endpoint vs write destination | A GitHub `/contents/` URL can support a read. A contents-write claim needs a write-specific API/route or a write call bound to that destination. A PUT to another host near a GitHub URL is not a GitHub write. Repository creation plus a contents URL does not establish publication, and even two supported operations do not prove their order, shared repository, or payload flow. |
| Value origin vs selected option | A literal contributing to an options object's history does not necessarily remain its selected value. Claims about a request method must account for duplicate keys, spreads, computed keys and intervening mutation. Value-origin evidence is not a substitute for that proof; unresolved options remain unresolved rather than inheriting the strongest historical value. |
| HTTP hostname transport vs DNS exfiltration | A bound value supplied in an HTTP request's hostname belongs in `micro-behaviors/communications/http/request/url`; the corresponding transfer objective belongs in `objectives/exfiltration/http/hostname`. Query parameters and bodies have their own HTTP channel categories. A hostname in a curl URL does not prove a DNS query occurred. Direct DNS label/query transport keeps its DNS home. Independent hex conversion and URL text are insufficient; bind the produced value to the requested hostname. |
| Function definitions vs invocation | A function defined with a familiar utility name is a naming/definition observation (`data/source/function/names`), not proof that the utility runs. A local `curl` definition can invalidate assumptions about a curl invocation. Reuse a shared definition guard where appropriate; duplicate-matcher checks must preserve the distinction between defining, calling and merely mentioning the same name. |
| Socket paths vs IPC and container operations | `micro-behaviors/fs/path/socket` owns filesystem socket endpoint references, including Docker daemon paths and encoded forms. It does not establish opening, connecting, listening, or controlling a container. Those operations require their own IPC/container evidence. Socket files are not device-node paths; protocol/address-family constants are not filesystem paths. A known Docker endpoint can still corroborate a container-reference claim, but cannot alone establish trusted container tooling for a suppression. |
| Port literals vs service and security properties | `metadata/file/string/network` owns port references and service vocabulary without network operations. Port 2375 does not establish Docker or unauthenticated access; port 2376 does not establish TLS. A literal pair remains one configuration observation, not a scan. Service-specific words may corroborate service context, while connection, protocol, authentication and probing claims each need their own evidence. |
| Privilege vocabulary vs container configuration | Generic `Privileged`/`privileged` fields, assignments and `--privileged` text belong in `metadata/file/string/security`. They do not identify Docker, Kubernetes or an SDK. Container-specific findings add the relevant configuration structure or command context. A Docker `HostConfig` privilege setting is configuration evidence, not proof of launch; an enabled CLI option must not accept `--privileged=false` or a longer option name. |
| Compiler ABI, library identity and exception flow | Compiler/runtime symbol prefixes remain in `metadata/binary/symbols/compiler` even when referenced by library or execution rules. They alone establish neither libc++/libstdc++ identity nor exception-based control flow. ABI plus a system-API reference and size/string-count filters belongs with `process/create/api-system`; exception obfuscation requires evidence of exception-based control transfer. Place a shared string-count predicate in `metadata/file/string/count`, retaining nonredundant size, entropy and scope gates in contextual composites. Do not duplicate a neutral count under a malware family. |
| Dot joins vs DNS labels or exfiltration | A dot join near named fields establishes string composition and co-occurrence → `data/string/concat`; it does not establish that those field values enter the joined string. DNS placement requires a DNS operation or protocol-specific construction. Exfiltration requires evidence of the transmitted data and destination; broad objective references must not inherit a neutral string helper as exfiltration evidence. |
| Metadata vocabulary vs section-specific binary facts | Whole-file vocabulary belongs with its meaning, independent of which binary section contains it. Section filters are required when the claim depends on that location; do not invent a section requirement to permit relocation. Missing filters on binary-only metadata produce a review advisory. Existing binary-fingerprint and hex-condition requirements remain separate. |
| `crypto/library/blockchain` vs transaction and protocol operations | Cipher/signature/hash primitives → crypto; constructing, signing, submitting or querying a financial ledger transaction → `data/transaction/{construct,sign,submit,query}`. Generic RPC/HTTP remains communications; provider endpoint identity is not a transaction. |
| `crypto/symmetric/xor` vs `data/{encode,decode}/xor` | A required keyed cipher construction → crypto; representation scrambling/descrambling → data. A bare XOR instruction cannot establish either construction. |
| `fs/path/<resource>` vs all file operations | Merely naming a location → path by resource kind. Required read/write/copy/etc. → that operation, referencing the path atom where useful. A path match never inherits the consuming composite's action. |
| Service-account resources vs container runtime | A defined bearer-token path belongs in `fs/path/token`; a deployment namespace file belongs in `fs/path/config/environment`; a public CA certificate location belongs in `fs/path/certificate`. The latter two are not credentials merely because their parent is named `secrets`. A mount-directory prefix identifies neither the child resource nor file access. Classify each matcher by the resource it actually identifies; a cross-resource OR must not claim token theft or reading. Kubernetes API/client evidence remains separate from filesystem references. The retired runtime `serviceaccount-files` aggregate must not be recreated. |
| Certificate paths vs public keys and signing metadata | `fs/path/certificate` admits locations identifying public certificates or trust bundles. SSH authorization/host-trust key files remain `fs/path/public-key`; private keys remain `fs/path/private-key`. An ambiguous `.pem` suffix alone identifies neither certificate nor private key. Certificate loading/verification is an operation; the analyzed artifact's signing chain is `metadata/signed/certificate`. A referenced CA file does not identify that artifact's signer. |
| Generic secret directories vs specific credential resources | A conventional secret-store directory such as `/run/secrets` belongs in `fs/path/credential` when the matcher identifies no particular child resource. It does not establish a bearer token, private key, configuration file, or the actual contents of the mount. A defined child resource uses its specific category, including public certificates and deployment configuration. Generic directory and child matches may overlap; they are not independent credential categories. Container-runtime identity and filesystem access require additional evidence. |
| Kubernetes directory prefixes vs package imports | `/var/run/secrets/kubernetes` prefix text identifies a conventional secret-store location → `fs/path/credential`; it does not require a service-account child or identify a client library. Package-import evidence can identify a Kubernetes dependency, but does not prove invocation or runtime execution. Keep path and import observations separate even when both are useful workload context. Prefix matchers must be described as prefixes, not exact directories or individual files. |
| Kubernetes API/configuration references vs Linux namespaces | Kubernetes API route text belongs in `communications/http/services/kubernetes`; it does not establish an HTTP request or identify a client library. The `KUBECONFIG` name belongs in `os/env/config`, without implying a value read or credential contents. Linux namespace flags, joining and creation belong in `os/container/namespace`; Kubernetes resource scoping does not make its API paths Linux namespace operations. Do not recreate the retired `kubernetes-comp` identity OR. |
| Environment configuration names vs access | A variable name or configuration marker is a reference, not a read. Consumers claiming environment access must require `os/env/read` or a more specific access observation, not the entire `os/env` ancestor. Even access plus nearby secret names does not prove that all named values were read or transmitted. |
| Token files vs token-issuance APIs | A service-account filesystem token location → `fs/path/token`; a TokenRequest API route is protocol/API evidence, not a token-file path. Resource names shared between an API and a file do not justify merging their categories. Standard and variable-mount token paths share the same filesystem leaf; their overlapping matches are not independent resources for cardinality claims. |
| Resource paths vs contextual weighting | A rule in `fs/path/<resource>` must establish a location of that resource. Tool identities, runtime context and benign-use weighting do not qualify, even as `component` composites: parent-directory consumers would inherit them as path evidence. Keep a single consumer's context directly in its `unless`/`downgrade` clause; reusable benign suppressors follow the exception contract. `needs` over directory references can count multiple matching rules in one directory, not distinct categories or resources. For a category-pair claim, require both category predicates explicitly. Cross-category pairs belong in `fs/path/credential`; ordinary app-data paths do not establish credentials. |
| Filename/member text vs file reads | Text such as `/ "token").read_text` belongs in `metadata/file/string/file`: it does not require a call, a resolved path, or bearer-token contents. A filename alone cannot identify Kubernetes or another service. Structured read operations belong in `fs/read`; read evidence bound to a selected target refines `fs/read/file/target`. Neither a method reference nor a comment should acquire operation semantics through a directory roll-up. |
| `fs/path/{password-store,cookie,private-key,public-key,token,secret-config,config}` | Choose the identified resource in that order of specificity, not its application owner: saved-login DB, cookie jar, private key, authorization/host-trust key, token file, secret-bearing config, then ordinary config. A file's defined role, not a generic credential word, determines the choice. |
| `fs/path/{personal,app-data,cache,font,library,log,metadata-store,system,temp}` | Classify the kind of resource named by the path, not the spelling of an ancestor directory. Browser history is personal; a profile or application-support/group-container path is app-data; cache is cache; an installed font path is font; `/lib` and `.dylib` references are shared-library paths; `/Library/Logs` is log; `.DS_Store` is a directory-metadata store; OSRecovery is a system path; temporary locations are temp. Thus `/Library/Caches` goes to cache and `/Library/OSRecovery` to system even though both contain the segment `Library`. |
| `fs/path` vs `fs/path-ops` | A path identifies a resource → `path/<resource>`; code joins, normalizes, parses or matches pathnames → `path-ops/{join,normalize,parse,match}`. Migrate `path/{construct,basename,check}` by operation; resource references stay in path. `Path.Combine` is join; `Path.GetDirectoryName` is parse/extract-parent. A bare method-name token is only an API fingerprint, not proof the method was called or that the surrounding behavior is malicious. Traversing the filesystem is directory/traverse, not pathname manipulation. |
| `fs/read`, `write`, `delete` vs `file/*` and `shell-ops` | Explicit content read/write/deletion uses the dedicated operation parent; create/open/copy/move/rename/stat use the corresponding `fs/file` operation. Shell/API spelling does not create another home. Reconcile `file/read-write` per actual evidence; keep a joint claim only if both operations are required. |
| `fs/directory`, `enumerate`, `traversal`, `search` | Listing one directory → `directory/readdir`; recursive descent without a narrower target-selection claim → `directory/traverse`; filename/content predicates, globs, search options, and indexed searches → `search`; drive/device inventory → `enumerate` by resource. A filename or extension predicate selects files, not a resource class to enumerate. `fs/enumerate/extension` is retired into `fs/search`. When search also descends recursively, the required name/content predicate selects `search`; recursion alone selects `traverse`. Directory deletion → `delete/directory`, rather than also directory/rmdir. |
| `fs/temp`, `fs/path/temp` | Creating a temporary object → `temp/{file,directory}`; a temporary location reference → `path/temp`. Tool-builder identity (PyInstaller, etc.) does not define a temporary-file operation. |
| `fs/memory/mmap`, `mem/alloc/map`, `mem/anonymous`, `mem/create` | Required file-backed mapping → `fs/memory/mmap`; anonymous address-space mapping → `mem/alloc/map`; anonymous file descriptor → `mem/anonymous/create`; shared memory/image-section object → `mem/create` by object. Generic `mmap` without backing evidence must not assert a specific backing. |
| `mem/alloc`, `protect`, `read` vs execution/injection | Allocation, permission change or remote memory access alone stays neutral. Injection needs a target process and execution transfer; same-process payload execution is not cross-process injection. RWX permissions alone do not establish hostile intent. |
| `dylib/load`, `os/module/load`, `process/interpreter/eval` | Native loader mapping a library → dylib; language module/import mechanism → os/module; evaluating source in the current interpreter → interpreter/eval. Spawning an interpreter is process/create. Retire duplicate `module/{require,dynamic-load}` spellings by mechanism. |
| `dylib/lookup` vs `os/api-resolution` | Ordinary exported-symbol lookup → dylib/lookup; manually walking tables or reconstructing API addresses → os/api-resolution by mechanism. Concealing import identity is a separate anti-static claim, not every `GetProcAddress`. |

### OS facilities and process boundaries

Apply the ordered [process-creation table](#process-creation) for
`process/create/<mechanism>`. At the same visible depth:

| Competing directories | Deciding evidence and canonical home |
|---|---|
| `process/create/fork` vs `process/fork/clone` | Creating a clone of the process is `create/fork`; reconcile the duplicate branch. A thread in shared address space is `create/thread`. |
| `process/exit`, `terminate`, `control` | Ending the current process → exit; terminating another → terminate; other process control → its operation. A signal API without the terminating signal is not process termination. |
| `process/identity`, `info`, `enumerate`, `pid` | Current process identity → identity; process attributes → info; listing processes → enumerate; PID-file lifecycle → pid. A PID value is not a PID file. |
| `process/thread`, `threading`, `sync`, `mem/sync` | Thread creation → create/thread; thread lifecycle/attributes → thread; locks/events/join → process/sync; memory visibility/cache synchronization → mem/sync. Language/platform does not choose among them. |
| `process/fd`, `io`, `communications/ipc` | Descriptor operations and standard-stream attachment → fd; copying/pumping data between streams → io; creating or addressing the pipe/channel itself → IPC. A reverse shell references these observations and adds outbound shell-I/O coupling. |
| `os/env` topics vs operations | Named variable meaning wins when required: CI-issued secret → `ci-credentials`, other secret name → `secret-name`, ordinary provider/runtime config → its topic. Variable-unspecified read/enumeration/modify/dump uses the operation leaf. Merge `check`/`gate` by value-test semantics. Never classify a secret as ordinary provider config solely by vendor prefix. |
| `os/registry/{read,write,delete,keys,hive}` vs `access`/`manipulate` | Required value read/write/delete wins; key/hive references alone use keys/hive. Split residual generic access by open/enumerate/watch/create semantics during migration. A Run-key write with durable activation is a persistence composite, not every registry write. |
| `os/service` operations vs `user-session`/`config` | Required create/start/stop/delete/query/configure/dispatch operation wins. A service definition field without an action remains a field/configuration fact. User versus system service scope is evidence, not a duplicate operation branch. |
| `os/autorun`, `time/schedule`, persistence | OS-managed task/autorun definition or registration → autorun; in-process timer/callback → time/schedule; durable unwanted reactivation → persistence by the trigger contract below. Task XML alone is not malicious installation. |
| `os/sysinfo`, `hardware`, discovery | Query hostname/OS/hardware properties → sysinfo; operate a device → hardware; required reconnaissance collection/target selection → discovery. A single vendor literal proves neither probing nor reconnaissance. |
| `os/privilege`, `security`, privilege escalation | Authority/token queries or ordinary changes → privilege/security; crossing to greater authority through abuse → privilege-escalation. `sudo` text or a requested-admin manifest alone is not that crossing. |
| `hardware/input`, `display`, collection | Device/event/capture API alone → hardware; required logging or surveillance behavior → collection. An empty error handler or arbitrary screen API is not screenshot theft. |

Within `process/fd`, use `query` for obtaining or inspecting a descriptor,
`control` for changing its flags, `close` for closing it, `dup` for duplicating
a descriptor, and `stdio` for attaching or configuring standard input/output/error.
When a matcher requires a duplication API, `dup` owns that atom even if its
argument is a standard descriptor; a composite that describes the resulting
standard-stream attachment belongs in `stdio`. A bare `fileno()` is a query,
not socket evidence. A connected descriptor or fixed remote address alone does
not establish a shell or hostile intent. Language and file type stay in scopes
and filenames.

For stream observations, a `Stdin` assignment belongs in `process/fd/stdio`;
an arbitrary `inputStream` property or input/output worker belongs in
`process/io/stream`. Variable names such as `conn`, `sock`, and `process` do
not establish object types. Starting two stream workers does not establish
opposite transfer directions. A reverse-shell composite must add the actual
connection, shell process, and required I/O coupling evidence.

A named runtime variable such as `BASH_ENV` belongs in `os/env/runtime`, even
when a CI attack consumes it. Require CI-specific evidence before using
`os/env/cicd`. A `Zone.Identifier` string belongs in `fs/path/stream`;
modification/removal evidence is needed before claiming MOTW removal. A binary
export count belongs in `metadata/binary/symbols/count`, regardless of which
capability or objective uses that count as an exclusion or downgrade.

A manifest dependency remains `metadata/package/dependencies/manifest/identity`
when a fixture or known-library composite consumes it. A Preact dependency
alone establishes neither a test fixture nor an executed import. The fixture
composite must add its own private-package, path or other contextual evidence;
do not place the declaration in the fixture directory and then use that
directory to suppress the same declaration elsewhere.

For archive members, distinguish the **name** from the member's **contents**.
Patterns over `archive.members[*].path` that merely suggest a key, certificate
or credential file belong in `metadata/package/files/name`. Describe the name
or suffix; do not assert that the file contains a private key. Fixture or
credential-use composites must add their own contextual/content evidence.
The former `metadata/package/files/credentials` leaf contained only such name
patterns and is retired; do not recreate it as a second home for them.

Use `metadata/package/files/archive-member` for member structure, including
rooted paths and traversal counts; use `files/name` for lexical naming
conventions. A parent-directory segment must come from a parsed member path
or traversal metric, not arbitrary `..` bytes in compressed content. An archive
basename's suffix belongs in `metadata/file/extension/package`; the parser's
reported format belongs in `metadata/file/format/structured`. Parser-error
counts belong in `metadata/file/archive` and do not alone establish fatal
corruption or tampering. Contextual diagnostics reference these shared facts.

Parsed archive properties also belong in metadata: encrypted-member counts,
duplicate-member counts, and member-path separators describe the container
being analyzed. `micro-behaviors/data/archive/` is for code that can create,
list, read, extract, or otherwise manipulate archives. A parser finding about
the sample's archive is not evidence that the program itself performs that
operation.

When an archive is a recognized package format, classify package-specific
member facts under that package's `metadata/package/files/` subject. For
example, APK resource paths, DEX member names, and nested APK assets belong in
`mobile-package/`; generic archive-member layout facts stay in
`metadata/package/files/archive-member`. These member facts describe package
contents or structure even when their names are suspicious. A probable staging,
loading, or harassment claim belongs in the corresponding capability or
objective only when a composite adds evidence for that claim; those rules
consume the package facts rather than redefining them.

DOS internal-table query evidence belongs in `micro-behaviors/os/msdos/internal`.
An `AH=52h` load followed by an interrupt sequence is a neutral query indicator;
an `AH=52h` load before an unknown near call is only a component. Infection or
antivirus-tampering composites add their own directory-entry, write, hook or
target evidence. The query alone must not carry either objective label.

### Objective ownership and level-three questions

Every row requires evidence for the unwanted result. Neutral APIs, labels and
format facts remain canonical observations in their own tiers. A consuming
composite does not pull its atoms into this tree.

| Level-1 directory | Admission and level-2/3 question | Nearest competing home |
|---|---|---|
| `anti-analysis` | Detect, gate or interfere with a behavioral-analysis environment. Behavior names the target/probe class; method names the required probe or interference. | Ordinary platform detection is a capability; static representation concealment is anti-static; bypass of deployed controls is evasion. |
| `anti-static` | Conceal or frustrate recovery of code/data from the artifact. Behavior names packing, obfuscation or polyglot abuse; method names the required concealment. | Neutral encoding/compression/metrics are not concealment by themselves. |
| `collection` | Acquire or stage target information without a required transmission leg. Behavior names the information/capture source; method names how it is captured. | Credential stores → credential-access; reconnaissance inventory → discovery; source plus send → exfiltration. |
| `command-and-control` | Attacker communication, remote tasking/access, activation, or the repository's payload-delivery behavior. Level 2 names that result; level 3 names its required mechanism. | Neutral networking is communications; theft is exfiltration; spreading to another system is lateral movement. |
| `credential-access` | Acquire, intercept, crack, or abuse access to authentication material or a specifically targeted secret store. Method refines the store or extraction/interaction mechanism. | A store path alone is a neutral reference; transport creates an exfiltration claim; payment manipulation is impact. |
| `discovery` | Reconnaissance of systems, accounts, software, network or cloud resources. Children identify the surveyed resource then probe/enumeration mechanism. | A neutral query alone remains a capability. Secret retrieval is credential access even if a discovery API returns it. |
| `evasion` | Conceal activity or bypass deployed detection/access controls. Children name the affected control or hiding behavior, then mechanism. | Terminating/degrading defenders → impact; defeating analysis environments → anti-analysis; code concealment → anti-static. |
| `execution` | Obtain unwanted code execution by an exploit, deceptive invocation, or abuse of a trusted execution surface. Level 3 names the required primitive. | Generic execution APIs remain process capabilities; a staged-payload chain uses dropper; remote command dispatch uses C2. |
| `exfiltration` | Transfer target data out through an unauthorized or attacker-directed path. Complete chains use `stealer/<source>`; transport-abuse-only claims use their channel. | Gathering without sending is collection/credential access/discovery. HTTP POST or an endpoint alone is not theft. |
| `impact` | Damage, disrupt, extort, manipulate or hijack systems, data or resources. Behavior names the effect; method refines its mechanism or target. | Hiding a change is evasion; a normal deletion or encryption API remains a capability. |
| `lateral-movement` | Establish access to or propagate onto another system. Behavior names access/propagation mechanism; method refines it. | Local execution/collection does not become lateral because a network library is present. Scanning alone is discovery. |
| `persistence` | Create durable reactivation or retained access beyond the current execution. Level 2 chooses the activation/access boundary; level 3 names the mechanism. | Detachment, hiding and long-running loops alone do not establish durability. |
| `privilege-escalation` | Gain authority beyond the starting principal through a required abuse mechanism. Children name the elevation primitive then affected boundary. | Ordinary authorized elevation APIs are capabilities; injection without higher authority is not privilege escalation. |
| `supply-chain` | Abuse component selection, provenance, publication, build/update trust, or the correspondence between a distributed component and its claims. Children identify that trust violation. | A package is a carrier; generic theft, execution and persistence retain their own result directories. |

Within `impact/cryptojacking/miner`, command-line flags that select a pool,
algorithm, worker count or injection mode belong in `config`, including a
composite of those flags. `runtime` requires evidence of a miner's operating
loop, worker, launch or execution context; a fetch/extract/exec profile with
XMRig and pool evidence belongs there only when its description does not claim
an unproven downloaded-file handoff. A pool endpoint alone belongs in `pool`.

When several outcomes are required, keep their canonical composites and place
the chain by its distinguishing result: source plus send → exfiltration;
cross-host installation → lateral movement; higher-authority execution →
privilege escalation; durable reactivation → persistence. A payload reaching an
execution sink → dropper unless a more specific required outcome establishes
one of those results. Unrelated outcomes need separate composites, not arbitrary
placement by the first leg. An objective-specific violation of package trust
may reference a theft/dropper composite without duplicating its entire claim.

### Remote access, reverse shells, and droppers

At `objectives/command-and-control`, classify the **required result** first:

| Level-2 directory | Admission | Exclusion / routing |
|---|---|---|
| `reverse-shell` | Outbound connection explicitly coupled to a shell session's input/output. | A listening/accepting shell → `backdoor/bind-shell`; HTTP-polled task execution or independent command requests → `remote-command`; socket and shell symbols without their relationship are insufficient. |
| `reverse-shell/stream-bridge` vs `dropper/delivery/pipe` | An interactive remote socket bridged to shell input/output → `reverse-shell/stream-bridge`. Downloaded content piped into a local shell without a remote interactive session → `dropper/delivery/pipe`. Both may use a shell, but only the first carries an operator session. |
| `backdoor/bind-shell` vs `backdoor/dispatch` | A listener that connects an accepted client to a shell → `bind-shell`. | Use `dispatch/<mechanism>` when the handler receives independent tasks and chooses an operation/command; remote access to a shell does not create a second dispatch classification. |
| `remote-command` | Receive attacker-directed tasks and dispatch operations or return command results. Repeated HTTP retrieval and dispatch → `remote-command/http-poll`; a single received task dispatch → `remote-command/dispatch`. An outbound HTTP client retrieving tasks → `backdoor/tasking/http`. | A persistent connected shell uses reverse-shell; an HTTP server route that accepts an operator request and executes its body → `backdoor/webshell/exec`. A single HTTP request is not polling. |
| `remote-command/dispatch` admission | Required evidence must connect received task data to an operation, interpreter, or command execution. A response written back over the channel strengthens the dispatch chain. | Socket plus process execution, or output written to a socket without received task execution, does not establish remote command dispatch. A persistent shell whose standard streams are wired to a connection uses `reverse-shell/<mechanism>`. |
| `backdoor` | An unauthorized access/control surface, such as a bind listener, webshell or authentication bypass. | Generic task dispatch uses remote-command; durable installation adds a persistence claim; binary/script/native-source are not access mechanisms. |
| Modular RAT profile vs capability cluster | Classify as `backdoor/rat/<mechanism>` only when the rule establishes a remote administration or tasking surface, not merely plugin-loading and socket APIs. | A pipe-delimited host string, socket connect, 32-byte array, nearby library load and VM check support separate neutral capability and anti-analysis findings. They do not establish encrypted command transport or an operator-controlled RAT. |
| `beacon` | Repeated attacker check-in or heartbeat, without a narrower required tasking result. | An ordinary timer or telemetry endpoint is not a beacon; an actual dispatched task belongs with its tasking result. |
| `botnet` | Fleet membership/coordination or distributed operator tasking. | A network-device platform or DDoS action alone is not botnet coordination. |
| `channel` | A communication mechanism proven to carry attacker control, without a narrower access/dispatch claim. | Generic transport APIs are capabilities. Choose protocol/mechanism over vendor identity. |
| `dns` | DNS-mediated task retrieval, attacker check-in, or command-channel tunneling; `dga` for algorithmic rendezvous naming. | Stolen values follow `exfiltration/stealer/<source>` when the source is established, otherwise `exfiltration/dns/<mechanism>` only when unauthorized transfer is supported. A DoH provider endpoint or media type alone belongs in `micro-behaviors/communications/dns/doh`; a generic DNS lookup is a capability. |
| `infrastructure` | An endpoint, configuration or rendezvous construction with a demonstrated C2 role. | Ordinary hosting/service endpoints and chosen labels alone do not establish C2. |
| `trigger` | An attacker activation condition: packet knock, message/content gate or local artifact gate. | Ordinary lifecycle/timer facts are capabilities/metadata; `activation` merely restates trigger. |
| `dropper` | Required acquisition/staging of a payload linked to its activation. | An installer identity, download, encoded blob or execution API alone does not establish this chain. |
| HTTP retrieval vs dropper activation | A `DownloadString` call, URL, or cleartext HTTP reference belongs under `micro-behaviors/communications/http/` unless the rule also links the retrieved content to an activation sink. Require that link before classifying `dropper`; source evaluation routes to `dropper/script-eval`, a launched staged file to `dropper/file-exec`, and in-memory transfer to the supported injection/image-map sink. | A download alone establishes a probable network capability, not payload execution, command dispatch, or C2. |
| HTTP/write/activation co-occurrence without a handoff | Classify the composite by its required operation: response or script-path writing → neutral HTTP download/write or filesystem write; `importlib` module loading → neutral module load; subprocess or variable-path interpreter launch → neutral process creation. Describe the nearby HTTP and file clues as context. | A `urlopen().read()`, writable script path, `spec_from_file_location(...).exec_module()`, or response write beside a child interpreter does not prove the same bytes or path reach that sink. Use the corresponding dropper sink only when the matcher binds the source or stage to it. |
| HTML object `codebase` vs saved executable | An `<object codebase="...exe">` attribute is an HTML-format reference; a UNC EXE string is executable-path evidence; `ADODB.Stream` alone is a COM ProgID reference. | Co-occurrence with `SaveToFile` does not show that the saved path is the `codebase` target. Classify a complete staged-file activation by its linked file-handler sink only when the rule establishes that handoff. |
| HTA host, media markup, and payload sink | `<hta:application>` identifies the HTA carrier; a media element referencing a file is HTML-document structure; off-screen/minimized windows follow hidden execution. Dynamic `eval` or a script-host launch follows its actual execution mechanism. | A media element alone does not prove a decoy lure. A gzip write to `tempZip`, a nearby `Run tempBat`, or WebClient bytes beside `Assembly.Load` does not establish the downloaded/decoded content as the launched payload. Require the value or path handoff before classifying a dropper. |
| Desktop-entry download, autostart, and document guise | A linked download-to-launch chain follows the dropper activation sink. A rule that additionally requires XDG autostart belongs under `persistence/login/xdg`; one that requires a deceptive document icon/name belongs under `evasion/masquerade/document`, referencing the delivery finding. | `wget -O /tmp`, chmod/pipe command text, `Type=Application`, `Exec=`, and `Terminal=false` are neutral command or format evidence on their own. They do not create another `dropper/execution/launcher` technique. |
| Editor extension installation vs dropper | A durable editor extension installation belongs under `persistence/system/editor-extension`; a bare `--install-extension` operation is a neutral package-manager capability. A source-to-installed-package handoff may refine the persistence profile with download evidence. | An HTTPS call, VSIX clue and force-install CLI in one file do not necessarily bind the fetched VSIX to the CLI argument. The editor or programming language is rule scope, not a `dropper/execution/ide-extension` branch. |
| Temp path, file write, and launch | An EXE/DLL/temp-data path is filesystem-path evidence; `curl -o` or WebClient use follows the downloader; `SaveToFile` follows stream writing; a `rundll32` invocation follows its named execution mechanism. | A download method beside a temp EXE path and a shell name does not prove that path was downloaded or executed. A batch download to `ProgramData` paired with a run from `Temp` names different paths and cannot be treated as one staged-file handoff. |
| DNS TXT stage vs DNS command channel | A TXT response assembled into a local executable and linked to its launch follows the dropper file-execution sink; TXT records carrying operator commands or replies follow `dns`. | TXT lookup, chunk decoding and a nearby spawn do not by themselves prove either a command channel or a staged-file handoff. Do not use `dns/tunneling` as a home for every encoded TXT response. |
| Document auto-open vs dropper | An auto-open trigger with a process or interpreter call, but no acquired payload linked to that call, follows `objectives/execution/trigger/document` or the specific interpreter mechanism when that is the primary claim. | A macro, decoded command, hidden window or `CreateProcess` API name alone does not make a dropper. |
| API resolution vs loader | Manual export walking or API-hash resolution, including a small DLL with sparse imports, follows `anti-static/obfuscation/native-api-hash` when hash-based; an ordinary resolver follows its API-resolution capability. | Sparse strings, a DLL shape or selected file/memory API hashes do not establish DLL sideloading or staged-code activation. |
| Archive extraction and shortcut launch vs dropper | `hh -decompile` follows CHM extraction, and a LNK invocation follows LNK execution. A staged CHM-to-shortcut dropper needs the downloaded archive, extracted shortcut and launched target linked by path or data. | `curl`, `hh -decompile` and `.lnk` in one file, even in order, do not prove they refer to the same artifact. |
| Archive download, extraction, and TEMP launch | An archive-extraction command is a neutral `data/archive/extract` capability; HTTP file transfer follows the downloader; a TEMP script or executable launch follows process creation. A required Run-key write follows `persistence/login/startup/registry`. | Proximity among download, extraction, and launch supports context, not an archive-payload dropper claim. Require a path or data relationship from the downloaded archive to an extracted member and from that member to the launch target before using a dropper activation leaf. Keep a hidden-window option as concealment context, not evidence of the handoff. |

Reverse-shell level-3 placement uses the **first required mechanism** below.
All rows still require the admission test above. Direction, transport and
encoding do not replace that evidence.

| Level-3 child | Required mechanism | Competing legacy paths |
|---|---|---|
| `dev-tcp` | Shell pseudo-device opens the connection and redirects shell I/O. | `/dev/tcp` sending HTTP alone goes to neutral communications. |
| `netcat` | Netcat (including compatible `nc`/`ncat` forms) connects to a remote endpoint and directly owns the shell relay. Require connect-mode endpoint evidence; a local listener is `backdoor/bind-shell`. | A netcat banner, import, or command invocation without shell-I/O coupling is a neutral capability under `micro-behaviors/communications/socket/netcat/`; it does not enter this objective. Other utilities need their own child only when evidence and volume justify one. |
| `pty` | A pseudoterminal explicitly carries the connected session. | PTY allocation alone remains `process/tty/pty`. |
| `fd-redirect` | Socket installed as inherited standard descriptors for the shell process. | The former `dup/` and `syscall/` objective leaves are retired. Syscall choice is evidence for descriptor redirection, not a second objective. Stream copy/pump loops belong in `stream-bridge`. |
| `stream-bridge` | Explicit read/write/copy operations bridge a socket and persistent child-process streams. | Socket and shell co-occurrence is insufficient; per-command result loops use remote-command. |

Choose one primary leaf using this precedence when a rule proves more than one
mechanism: `dev-tcp` → `netcat` → `pty` → `fd-redirect` →
`stream-bridge`. This names the most specific required relay mechanism and
prevents duplicate copies of one detection in several leaves. A rule that
proves only socket plus shell co-occurrence does not qualify for any of them;
strengthen its evidence or route it to the actual command-dispatch behavior.
Encoding style and syscall/API spelling do not override this choice.
An encoded-command option belongs with command-invocation flags; window-style
arguments belong with hidden process launch. A TCPClient name inside Base64 is
a TCP facility reference, not a reverse shell. Classify decoded payloads by the
behavior they establish, and distinguish containing such a payload from proving
that a launcher executes it. Do not combine decoding, a shell invocation and a
network type name into a relay verdict without the transfer mechanism.
`reverse-shell/encoded` is retired: encoding is a representation, not a relay
mechanism. Shell-option labels belong with neutral security vocabulary under
`metadata/file/string/security`; decoded import text belongs with import
metadata. Neither proves that the named behavior executes.
Nearby decoding and process execution do not establish that decoded bytes become
code, even inside a package. Separate encoded strings must not be joined into
an invented relay; retain their independently supported capability observations.
Computed calls, an obfuscator-style function name, or a sparse import table do
not supply missing network or relay evidence. In native code, cmd.exe strings,
pipe APIs and Winsock imports still need evidence linking the channel to child
I/O. The same applies to CLR type/method names: `TcpClient`, redirected standard
streams, `HandleCmd`, or reverse-shell terminology do not prove a relay. A
command-handler identifier belongs with neutral dispatch observations; consumers
must establish remote execution through additional behavioral evidence. Where
source relations are available, bind the network stream and child process to
both directions of transfer rather than joining unrelated helpers in the file.
Locale and window-station queries do not establish a C2 activation gate
without the relevant conditional behavior. When an aggregate adds only an
unsupported verdict to existing canonical observations, retire the aggregate;
do not preserve it under a vague obfuscation or generic-behavior directory.
For a stream relay, require input delivery and a return path; a networking
call, shell reference, and generic `.pipe()` call are insufficient. An
explicit `telnet | shell | telnet` pipeline or a Telnet/shell cycle through
one FIFO belongs in `stream-bridge`, not `pty`: require the shell's pipeline
position and, for FIFO cycles, the same created path at both ends. A filter
such as `sed` between Telnet commands is not a shell. FIFO creation near a
Telnet command is not a relay, and service/tunnel/cron strings do not establish
a persistent shell without the corresponding activation behavior. An
input/output pipe pair must use the same peer and child identifiers; separate
file-backed stdin/stdout pipes cannot borrow an unrelated network connection.
The neutral paired-pipe observation belongs in `process/fd/stdio`, regardless
of whether its matcher uses text, call facts, or an AST query. Identifier
agreement is not proof of the peer's network type or immunity to reassignment;
the objective still requires connection and shell evidence. An extension or
install-hook wrapper references the canonical relay rather than
repeating weaker stream tests. Archive co-occurrence proves that the package
contains the relay and trigger declaration, not that the trigger invokes it.
An environment reference such as `IS_CHILD` belongs in `os/env/config`; its
name alone proves neither a guard nor a detached-child restart.
`netcat/` is the technique directory for a shell relay owned by netcat; it is
not a generic home for every observation mentioning the utility. Keep direct
shell execution (such as `nc -e /bin/sh`) and FIFO/pipeline relay forms together
while the directory remains comfortably within the 100-rule cap. If growth makes
the directory crowded, split only by the relay invocation form, such as
`netcat/direct-exec/` and `netcat/fifo/`. Each child must require that form and
exclude its sibling's form. Keep language and file type in rule scope/filenames;
they do not define netcat subtechniques. A utility invocation without evidence
that netcat carries the shell session stays in the neutral socket capability
taxonomy, even if an objective composite later references it.

**Netcat versus descriptor redirection:** a rule requiring netcat's invocation
semantics belongs in `netcat`, even if the invocation also redirects descriptors.
A utility-independent socket-to-stdio observation belongs in its neutral fd
capability; a utility-independent shell-relay composite belongs in `fd-redirect`.
Reference that shared evidence from the netcat rule rather than copying its
matcher into both objective leaves.

`socket-exec/` and `stdio/` are retired reverse-shell catch-alls, not placement
destinations. Standard I/O names a resource shared by several relay mechanisms;
it does not distinguish descriptor inheritance from stream pumping. When
migrating their rules, classify the required shell-I/O mechanism: a PTY carrying
the session → `pty`; socket descriptors inherited by the shell → `fd-redirect`;
explicit socket/child-stream copying → `stream-bridge`; netcat owning the relay
→ `netcat`; shell pseudo-device redirection → `dev-tcp`. A loop that receives
independent commands and dispatches them belongs in `remote-command/dispatch`,
even when the transport is a socket. Socket and shell evidence without one of
these relationships does not establish a reverse shell and must be tightened,
reclassified by its actual behavior, or removed if it has no valid claim.

An accepted connection feeding shell descriptors belongs in `backdoor/bind-shell`;
an outbound connection feeding them belongs in `reverse-shell/fd-redirect`.
Bind/listen/accept and connect are distinct admission evidence, not interchangeable
alternatives in a rule claiming an outbound shell.

`encoded` does not define an alternative shell bridge. `http-poll` does not
establish a shell session without the required I/O relationship. Retire those
parallel classifications when migrating their rules; `syscall` is already retired.

Dropper level-3 children classify the **required activation sink**. The legacy
`delivery`, `staging`, `execution`, and `behavior` partitions are being
reconciled into these canonical homes. Pick one sink and reference source,
concealment and trigger facts; do not duplicate a complete chain under its
carrier or encoding.

`dropper/execution/loader` has no separate admission test: a loader is a
program role that can activate code through several different mechanisms.
`execution` is a phase, not an activation technique. Treat all children of
this legacy partition as audit sources, not as destinations for new rules.
Classify each rule by the sink its matcher requires. A loader-shaped name,
import or event hook without evidence that staged code reaches a sink does
not establish a dropper. Keep its supported observation in the neutral
capability tier, or place a complete non-dropper composite under the actual
objective it supports.

Script, HTA, WSH, MSI and package format identify a carrier or host, not the
payload sink. A command that invokes `mshta` on a remote URL supports script
interpreter execution; it does not by itself establish a separately staged
dropper payload. An MSI containing `New-ScheduledTaskAction` supports a
scheduled-task observation, while an MSI Run-key write supports persistence.
The container may be useful as a scope or corroborating leg, but the required
result owns the rule. Likewise, a quoted Ruby library name is only a string
literal unless the matcher requires an actual import or load expression;
do not report bare names as module loading or infer dropper execution from
them.

A distinctive builder path plus a binary-layout profile may identify a named
malware wrapper without proving what that wrapper executes. Put the path
fingerprint and its family composite under `well-known/malware/`, and reusable
section measurements under `metadata/binary/section/`; another family can
reference the shared wrapper when its own corroboration is required. A bare
COM ProgID prefix is an automation reference, not a reconstructed token array,
HTTP client or dropper by itself. If two consumers need the same matcher with
different file-size bounds, keep one neutral observation and put the narrower
bound on the consumer that requires it. Do not invent a section or size bound
for a family string without evidence merely to satisfy validation.
The same rule applies to stack-built string fragments in native code: bytes
constructing `%appdat`, `http://`, a filename or `%s:Zone` are path, URL and
stream-name evidence, respectively. Their adjacent code bytes or an API-name
reference do not prove that a URL is downloaded, a Mark-of-the-Web stream is
removed, or the downloaded file is launched. A distinctive code-stub signature
can identify a family only after the family attribution is supported; generic
fragments remain neutral facts that the family rule can reference.

For example, `BeaconPrintf` and related Beacon Object File host API names
belong in `micro-behaviors/process/interpreter/bof`: they indicate BOF host
compatibility, not acquisition or activation of a staged BOF. The generic
COFF `__imp_` import-pointer prefix belongs in
`micro-behaviors/os/linker/import-symbol`, even when it helps corroborate a
BOF host. Only a composite linking staged BOF material to execution belongs
under the appropriate dropper activation sink.

When no activation sink is established and a staging observation remains in
the legacy `staging/` branch, use the technique the matcher actually requires:

| Required evidence | Placement | Boundary |
|---|---|---|
| Archive membership or archive-contained payload/lure, with no required encryption clue | `dropper/staging/archive/` | A disk image merely contained in an archive stays here; require mounting or execution from that image before using `staging/image-disk/`. |
| Encrypted content used as the defining staging mechanism | `dropper/staging/encrypted/` | A password-protected archive belongs here when the archive's encrypted-member/header evidence is required. If encryption is optional and the archive or nested disk image is the actual technique, use `staging/archive/`. |
| Reconstructed or decoded embedded payload, with no activation sink established | `dropper/staging/encoded/` | Require evidence of payload reconstruction, not merely an encoding API or encoded string. Once a sink is shown, classify the full chain by that activation sink. |
| Executable carrier is a small stub with a dominant appended payload | `dropper/staging/stub/` | Require the stub-and-overlay shape, not just any embedded PE or a process-launch name. A shell or URLMon clue without a link to the appended bytes does not make this a file-exec chain. |
| Payload is embedded in a non-resource carrier without the stub-and-overlay shape | `dropper/staging/embedded/` | Require evidence that the embedded material is used as a stage; a bare embedded-PE fact stays in `metadata/binary/layout/embedded` or `micro-behaviors/data/embedded`. Resource-table extraction belongs in `staging/resource` when its staging relation is supported. |
| Payload is extracted from an executable resource table without a proven activation sink | `dropper/staging/resource/` | Require resource access and extraction/staging evidence. A resource API or a large `.rsrc` section alone stays neutral; once the extracted content is linked to an activation sink, choose that sink instead. |
| Mounted virtual disk used to activate a contained executable or shortcut | `dropper/staging/image-disk/` | Requires mount/activation evidence; archive membership alone does not qualify. |

The evidence-source format (archive metadata, strings, or API references) does
not create another taxonomy branch. The rule description should say whether
the observed evidence indicates an encrypted archive, archive membership, or
disk-image activation, and must not claim a launch or decryption sink that the
matcher does not connect.

| Activation child | Required payload activation |
|---|---|
| `process-inject` | Transfer execution of the staged payload into another process. |
| `image-map` | Map/relocate a native image for execution in the current process. |
| `module-load` | Load staged code through a runtime module/assembly loader. |
| `script-eval` | Evaluate staged source in the running interpreter. |
| `interpreter-stdin` | Feed staged source through a new interpreter's stdin. |
| `file-exec` | Launch a staged file through a process or file-handler mechanism. |

A WebAssembly host (`new Go()` plus `WebAssembly.instantiate`) is a neutral
interpreter/module capability under `micro-behaviors/process/interpreter/wasm`.
A long or generated-looking `.wasm` filename, a sidecar `require`, or an empty
Promise catch adds context but does not connect that named asset to the bytes
passed to `instantiate`. Use `dropper/module-load` only when acquisition or
staging of the WASM payload is linked to that activation call. JavaScript as
the host language and `.wasm` as the payload format do not select separate
dropper children.

`file-exec` is strictly a parent; its rule-bearing leaves refine the activation
mechanism. `file-exec/command` requires a shell or command interpreter to
evaluate command text that launches the staged file (`system()` with a shell
command, or a shell script invoking a local payload). `file-exec/spawn` requires
a process-creation API or structured process invocation to launch the staged
file directly (`Start-Process`, `ProcessBuilder`, `execve`). `file-exec/installer`
requires handing a staged package to an installer transaction (for example,
`msiexec`). If a chain invokes an installer to activate its package, classify
that rule under `installer`, even though the installer itself is a process.
Use `command` when shell parsing is required and `spawn` when the target path is
passed directly to a process-creation mechanism. A mere installer reference
without package-install evidence does not qualify for `installer`. Do not put
rules directly in the `file-exec` parent.

Installer evidence follows the observation it actually establishes. An SFX
`RunProgram` command selects a process target under
`micro-behaviors/process/create/installer`; its `InstallPath` directive selects
an archive extraction destination under
`micro-behaviors/data/archive/extract/destination`; `Progress="no"` configures a
user-interface control under `micro-behaviors/ui/controls/progress`. A large,
high-entropy installer overlay is a binary layout or packing observation, not
evidence that the overlay was launched. Self-issued signatures and fabricated
product claims belong under certificate or identity masquerade. The historical
`dropper/execution/installer` carrier leaf is only a migration source: a rule
belongs in `dropper/file-exec/installer` only when the staged package is linked
to the installer invocation. These contracts apply equally to NSIS, Inno Setup,
MSI, 7-Zip SFX and other installer formats.

Bare host-profile field-name pairs belong under
`micro-behaviors/data/format/host-profile`, even if
a known sample serializes them as JSON. Use `data/format/json` when the matcher
requires JSON syntax or a parsed JSON structure; a regex that only sees
`machine_name` near `windows_user` does not establish the encoding. A composite
that requires those fields and an HTTP POST can then describe transmission of
a host profile under `objectives/exfiltration/stealer/system-info/profile`.

A .NET `AppDomain.AssemblyResolve` handler that resolves a staged assembly is
`module-load`. A host process-creation API marker alongside that handler does
not turn the rule into `file-exec` unless the matcher requires launching the
staged file through that process API.

For example, a password-protected 7z rule that requires stdout extraction,
payload validation, a temporary executable path, and `Start-Process` belongs in
`file-exec/spawn`: encryption and archive format describe the source, while the
direct child-process launch is the defining sink. If the encrypted archive is
identified without a linked activation sink, keep it in `staging/encrypted`.

Require evidence of cross-process execution transfer for `process-inject`;
executable memory or thread creation in the current process alone does not
establish injection. `image-map` requires evidence that a native image is
mapped or relocated for execution in the current process. Decrypting into
executable memory without either specific sink remains memory staging until
the matcher supports a narrower activation claim.

A file-level co-occurrence of HTTP retrieval, response materialization, and an
interpreter launch does not by itself link the retrieved bytes to the launched
interpreter. Keep that useful observation under the interpreter capability,
describe it as co-occurrence, and reserve a dropper execution classification
for evidence that connects the staged payload to its activation sink. A broad
proximity window may support a lead, but it must not turn unrelated paths in a
large source file into a download-and-execute claim.

Likewise, renaming a file to an executable suffix alongside a shell invocation
supports a rename-and-command-execution observation. It is a dropper only when
the matcher connects the renamed staged file to the launched command. An
`extconf.rb` build hook or outer package is trigger and carrier context; if
command execution is the required result, classify that composite with
execution and reference the hook or package fact.

Within `objectives/command-and-control/dropper/delivery/`, use `urlmon/` for
download-and-execute rules whose specific transfer technique is URLMon
(`URLDownloadToFile` and related URLMon paths), `wininet/` for WinINet, and
`winhttp/` for WinHTTP. These API names are valid technique labels even though
they are Windows-specific: the child states the transfer mechanism, while the
parent states the malware behavior. The APIs are separate categories because
they are distinct transfer interfaces; do not merge them as synonyms. Keep
rules that combine multiple transfer methods or do not identify one of these
APIs in the general `execute-download/` leaf. Do not create language- or
filetype-based children.

Use `hidden-stage/` for dropper rules whose distinguishing technique is
concealing the staged payload in a hidden or writable scratch surface and
arming or launching it. Prefer an API-specific transfer leaf (`urlmon/`,
`wininet/`, or `winhttp/`) when the rule's defining technique is that transfer
API; use `hidden-stage/` for format-neutral hidden-path staging without a
narrower transfer mechanism. A hidden window alone is process-creation
evidence, not a hidden-file stage.

The same boundary applies to PowerShell: a hidden-window option, an
`Invoke-WebRequest` call, and a nearby `Start-Process` indicate concealed
execution and network-request capabilities, but do not establish that the
response supplies the launched process. Keep this as a neutral hidden-process
capability co-occurrence. Classify a confirmed downloaded MSI under
`dropper/file-exec/installer` only when the rule also connects the retrieved
path to the installer invocation.

The same remote encrypted assembly therefore has one chain home, `module-load`;
its encryption, network transport and install hook are referenced observations.
The neutral loader and any concealment objective retain their own canonical IDs.
Likewise, decrypting a staged file and activating it through dynamic `require`
is `module-load`; decrypt-and-eval chains use `script-eval`, and ciphertext with
no established sink remains in the appropriate staging leaf.

`new Function`/`eval` of decrypted source is `script-eval`; `Module._compile`
is `module-load`. A local write/chmod/spawn chain is `file-exec` only when the
bounded evidence supports a likely relation between the stage and the launch.
A PowerShell `AppDomain.Load` or .NET `Assembly.Load` of staged bytes is also
`module-load`, even when the resulting code stays resident in memory. Reserve
`staging/memory` for executable-memory staging that does not establish a more
specific activation sink. Memory residency alone does not choose that leaf.
A standalone interpreter-evaluation capability stays under
`micro-behaviors/process/interpreter/eval/`; only a completed staged-source
chain moves to the dropper sink leaf. A generator/source fragment that indicates
JavaScript `eval` is therefore a language-specific eval observation, not by
itself proof of encrypted staging or a dropper.
The same applies to a Java resource getter beside `ScriptEngine.eval` when
the rule does not bind the resource stream to the eval argument. An obfuscated
class name plus engine setup belongs with class-name obfuscation; a WSH
`GetObject` variable call beside a split URL scheme belongs with string
fragmentation until the reconstructed moniker is tied to that call.

Remote scriptlet execution through `regsvr32` (`/i:` plus `scrobj`) belongs in
`execution/lolbin/regsvr32`, where the named proxy-execution technique and its
Squiblydoo refinement share one leaf. It is not `dropper/file-exec`: the
activation is the LOLBin's scriptlet mechanism, not launch of a staged file.
Generic `regsvr32` invocation remains a process-launch capability; a complete
staged-file chain belongs under its actual activation sink.

A remote MSI URL combined with `msiexec` installation belongs in
`dropper/file-exec`: the installer is the file-handler activation sink.
`msiexec` invocation or an MSI identity without remote staging and installation
evidence does not establish that dropper chain.

### Analysis evasion, concealment, and disruption boundaries

| Competing paths | Evidence that decides |
|---|---|
| `anti-analysis/{debugger-detect,sandbox-detect,vm-detect,emulator-detect,tool-detect}` | The required target probe chooses the behavior: debugger status/interference; sandbox execution artifacts; virtualization interfaces; emulation artifacts; analyst-tool detection. A VM artifact is not automatically a sandbox. Composite analysis gating references the actual probe. |
| `anti-analysis/{environment-detect,fingerprinting,geofencing,timing}` | Environmental condition not covered by a specific target; host-bound identity; geographic/locale gate; or timing interference respectively. Generic system information and sleep remain capabilities. |
| `anti-analysis/self-modify` vs `anti-static/obfuscation` | Modification reacting to live analysis → anti-analysis; representation mutation concealing code → anti-static. Ordinary memory permissions prove neither. |
| `anti-static/obfuscation/{imports,reflection,name-mangling}` | Concealed API/import identity → imports; concealed dynamic dispatch → reflection; altered identifier names → name-mangling. A normal dynamic lookup is a capability. |
| `anti-static/obfuscation/{string,encoding,payload}` | Concealed string values → string; encoding used as the required concealment itself → encoding; concealed executable stage as a unit → payload. Neutral decode/decrypt remains a capability. |
| `anti-static/obfuscation/{syntax,control-flow,instruction}` | Source-form concealment without changing path structure → syntax; obscured branches/dispatch → control-flow; instruction-level junk/substitution → instruction. File language is not the axis. |
| `anti-static/pack` vs `obfuscation/payload` vs metadata | Packed executable reconstruction/unpacking → pack; concealed payload without packer structure → payload; high entropy or section shape alone → metadata for that part. Named packer identity → well-known. |
| `evasion/anti-av` vs `impact/degrade` | Bypass/interposition/exclusion of observation → anti-av; terminate, disable or damage the defender → degrade by affected system. Generic security-product discovery belongs in discovery. |
| `evasion/kernel-hide` vs user-space hooks | Kernel-mediated concealment alone qualifies for kernel-hide. User-space interposition uses the applicable process/hijack concealment mechanism; `kernel-hide/userspace` is a migration conflict. |
| `evasion/{masquerade,decoy,file-hiding}` | Falsified identity → masquerade by identity surface; diversionary content → decoy; concealment of a file's visibility/location → file-hiding. A hidden-file attribute alone remains neutral. |
| `evasion/{indicator-removal,self-delete}` | Removing records/artifacts of activity → indicator-removal; removing the running program's own artifact → self-delete. Application-log type does not duplicate the same removal mechanism under another sibling. |
| `impact/{destroy,wipe,ransom,degrade,dos,infect}` | Content destruction → destroy; overwrite/erase storage → wipe; coercive encryption/extortion → ransom; disable a capability → degrade; availability exhaustion → dos; insert replicating code into a host → infect. Read/write/encrypt APIs alone establish none of these outcomes. A generic “sending crash” report string plus a socket or connect API does not establish availability exhaustion. |

### Collection, credentials, discovery, and theft

Classify **what is acquired**, then whether the rule requires it to leave.
An endpoint plus unrelated sensitive tokens is not a demonstrated source-to-send
chain. A path/API atom retains its neutral home even when every current consumer
is a stealer.

| Required source/result | Canonical ownership and disambiguation |
|---|---|
| Saved login, authentication cookie/token, key or credential store | Extraction/access objective under `credential-access/<store>`; a literal field/path or general store API remains neutral. Browser history/content is collection, not credential access. |
| Keyboard, clipboard, screenshot, microphone/camera capture | Collection by captured source when logging/surveillance is established. Generic UI/device calls remain capabilities. Capturing an explicitly credential input can refine credential-access/capture. |
| Mailbox/message content vs account secrets | `collection/email-harvest` or messaging for content; credential-access for authentication material. An audit event stating access occurred is not itself a harvesting implementation. |
| Host, account, software, process, network or cloud reconnaissance | Discovery by surveyed resource. `discovery/host` owns installed software/security/browser applications; system owns machine/hardware/OS profile; process owns running-process inventory; network owns interfaces/peers/probes; account owns principals; cloud owns provider resources. Reconcile duplicate host/process/system branches accordingly. |
| Host-information query near an endpoint vs exported host data | A WMI/OS query plus an IP/URL clue without a send operation remains `discovery/system/profile`; even a literal `/exfil` path in class strings is endpoint evidence, not a transfer leg. Require upload/send evidence before assigning `exfiltration/stealer/system-info/<source>`. |
| Specific source plus its transmission | `exfiltration/stealer/<source>`; the source wins over HTTP/DNS/webhook transport, package carrier, and install/build trigger. |
| Required theft of independent datasets plus transmission | `exfiltration/stealer/multi-source`, replacing the audited portion of legacy `sweep`. Browser cookies plus wallet secrets qualify; browser identity plus a separately required network/geo profile also qualifies. Several observations about one host do not: network address and geo fields together are still one network-profile dataset. An OR over sources or an optional second source does not qualify. |
| Exfiltration channel abuse without a narrower established source | `exfiltration/<transport>` by required transport mechanism; it still needs theft/unauthorized-transfer evidence. Neither HTTP POST nor an OAST domain alone meets admission. |
| Local hash/password recovery vs remote guessing | `credential-access/cracking` for local recovery; `lateral-movement/brute-force` for attempts to gain remote access. Service/protocol identity alone is not guessing. |
| Deceptive credential prompt vs its completed export | `credential-access/phishing` for deception/relay; `exfiltration/stealer/input` for captured-input export. The former `stealer/phish` rules have been reconciled: local capture and archiving are not export. Reference acquisition evidence rather than duplicating its matcher. |

For `stealer/<source>`, use the identified store before a broad storage medium:
wallet → wallet; browser-owned saved logins/cookies → browser; OS secret store
→ keychain; SSH material → ssh; cloud-provider stores → cloud; developer
credential files → dev-secret; process environment → env; app session tokens
not covered by those stores → token; other documents → file. Source-required
capture, mailbox, host profile, account DB, and appliance configuration use
their source children. Network inventory follows the host-report contract
below. A specific store beats `file`, `input`, or `system-info`; accompanying
host context does not turn one stolen dataset into multi-source theft.

#### Stealer directories classify the acquired information

The primary question is **what information is probably acquired and sent?**
Transport, acquisition method, breadth of search, and implementation language
do not compete with that source axis. Host identity accompanying wallet theft
does not make a second theft objective: the wallet remains the defining source.
Likewise, browser fingerprint fields describe a client profile; they are not
the same source as browser passwords, cookies, or browsing records.

Keep the source axis separate from the acquisition-method axis. A broad file
sweep describes how a program searches, not what data leaves; it cannot be a
peer of `browser`, `wallet`, or `system-info`. Put the search behavior under
`collection/file-targeting` (or the narrower acquisition behavior it actually
supports), then classify any required outbound chain by its data source. Use
`multi-source` only when the matcher requires independent source classes. The
legacy `stealer/sweep` directory admits no new rules and is not a fallback for
an unclear source. Its former Android permission/WebView combination and
raw-IP/header combination were retired from the stealer tier because neither
required a data-read plus outbound-transfer chain. Their independent capability
signals remain available in their proper homes. Protocol-neutral upload/send
wording belongs under `micro-behaviors/communications/transfer`; a source
specific export composite must additionally require a sensitive-data clue and
bind the source, transfer, and destination evidence by proximity where possible.

`system-info` owns exported host/client reports: identity, OS/runtime,
hardware, installed software, running processes, and network inventory.
Hostname, username, MAC/IP addresses, OS details, and process lists may be
parts of one report. They do not become independent stolen datasets merely
because their evidence comes from different APIs or discovery directories.
Account names in an inventory belong here; an authentication database or
password hashes belong in `account-db`. Network survey data belongs here;
Wi-Fi passwords belong with credentials, and a stolen appliance configuration
file belongs in `appliance-config`.

Split `system-info` by the kind of reported information, not by the API,
language, operating system, or way it was collected. `identity`, `platform`,
`software`, `process`, and `network` are narrower source domains. `profile` is
for a host/client report that requires multiple such domains or leaves the
reported domain open across them; it is not a synonym for “many indicators,”
“broad sweep,” or “unknown data.” When one domain is necessary and sufficient,
use that domain even if the rule also mentions ancillary host fields.

The implemented subdivision has the following placement contracts. Rules live
only in the populated children; `system-info` itself contains no rules or
aliases. Hardware is a reserved source contract, not an empty directory: the
audited matchers did not require a hardware-only export. Map every rule,
including helper atoms, before any future split.

| `system-info` child | Defining information; boundary |
|---|---|
| `identity` | Host/account/device identifiers or fingerprints. A hardware serial or MAC used to identify a victim is identity; hardware capacity and interface configuration are not. |
| `platform` | OS, kernel, runtime, release, architecture, and execution environment. The surveyed platform is data, never a hierarchy keyed by OS or language. |
| `hardware` (reserved) | CPU, memory, storage capacity, and physical-device inventory. Stable victim identifiers go to identity. Materialize this leaf only when a matcher requires that source. |
| `software` | Installed packages, applications, services, and versions. Running instances go to process; OS/runtime version goes to platform. |
| `process` | Running-process inventory and its execution attributes. A process inventory sent by itself belongs here; a report that requires process data together with identity, platform, software, or network data belongs in `profile`. Replaces the corresponding `process-list` rules. |
| `network` | Interfaces, addresses, routes, neighbors, connectivity, and network survey results. Replaces inventory from `network-config`; exclude secrets and whole appliance configurations. |
| `profile` | A host/client report whose required source spans, or cannot be confined to, one of the specific information domains above. Examples: a multi-domain schema, a profiling bundle, or alternatives among host-inventory domains. Every alternative must still establish host-information evidence; an endpoint or User-Agent alone does not. |

Use the most specific established source; ancillary identifiers do not displace
it. Use `profile` when reporting the host is the defining result and the whole
matcher does not require one narrower information domain. This is the common
source shared by host-inventory alternatives, not a miscellaneous leaf for an
unknown source. An OR over unrelated theft targets (for example, wallet keys
or screenshots) is not a host profile and still needs matcher/source review.
A distinctive interface-name reference alone remains a capability clue at
`micro-behaviors/network/interface`; a reconnaissance combination belongs in
discovery, and a probable report export belongs in stealer. These are evidence
thresholds for classification, not demands for proof of runtime activity.

`multi-source` requires independently meaningful target datasets (for example,
browser credentials and wallet keys), each required by the matcher. Count
source classes, not matched traits: `needs: 2` can be satisfied by two indicators
of the same source, and directory references can match several traits. Two
browser stores still belong in browser. Shared host context, optional sources,
and OR alternatives cannot establish multi-source theft. Do not rename all of
`sweep` wholesale; its nonconforming rules need individual destinations.

`credential` owns probable export of authentication material or authentication
stores when the whole matcher leaves the store open. For example, an export
requiring either an SSH-key bundle or browser login databases belongs here;
one requiring both belongs in `multi-source`, and one requiring browser logins
alone belongs in `browser`. Multiple browser indicators cannot be counted as
multiple sources. Apply the specific-store rule first, then independently
required sources, then this common authentication-data category. It is not a
home for arbitrary OR alternatives: mailbox content, screenshots, documents,
and host reports do not become credentials through association with a stealer.
An unknown payload still follows its established transfer mechanism.

`keychain` requires a credential-store source (for example, Keychain, keyring,
Vault or Protected Storage) and probable outbound transfer. A DPAPI unprotect
call identifies a protection mechanism, not the store that supplied the data;
with an export context but no required store it follows `credential`. Likewise,
keychain-or-Discord, keychain-or-cloud and keychain-or-browser alternatives
follow `credential`, not `keychain` or `multi-source`. Two independently required
stores without transfer evidence belong in `credential-access/theft/multi-store`;
acquisition must not be classified as export merely because its consumer exports.
A keychain query beside an output-field label is a keychain capability clue;
network context must come from the consuming export classifier. Named account
or application credential targeting follows the established credential-access
source category (for example, GameCenter in gaming), even when Keychain supplies
its access method. Password prompts paired with a login-keychain path belong in
keychain credential access; the path alone does not establish a completed read.

Defanged IPv4 notation belongs in `communications/ip/parse`. Its matcher must
validate octet syntax after accounting for delimiters such as `[.]` or `(.)`;
a validator that accepts only dotted-decimal text cannot validate that form.
Defanging does not establish public routability or malicious intent. Private
and loopback addresses still have the same notation capability; a consuming
objective must supply its own behavioral context.

Browser credential access separates the protection/access mechanism from
neutral store locators. `credential-access/browser/app-bound` owns recovery or
bypass of App-Bound Encryption and its technique-specific fragments, across
browser brands. `browser/devtools` owns browser debugging interfaces used for
cookie/session acquisition or enabling access to that interface. Ordinary DPAPI
recovery remains in `browser/dpapi`; classic Chromium store/decryption workflows
remain in `browser/chromium`. A required App-Bound protection leg takes precedence
over the underlying DPAPI, injection, or browser-brand detail. Generic injection,
DPAPI and DevTools APIs retain their neutral capability homes. Explicit collector
report/key-dump output follows `browser/loot`, including a recovered App-Bound
key filename; the output filename does not establish how the key was recovered.

Browser-location clues follow `micro-behaviors/fs/path` even when they support
credential-access consumers. `cookie` owns cookie database/jar locations;
`password-store` owns login/password/key-store locations and named credential
service locators; `application/browser` owns profile roots, configuration,
history/local-storage locations, and alternatives spanning browser store types.
For example, a pattern accepting either Login Data or Cookies beneath a browser
profile follows `application/browser`, while a required Login Data filename
follows `password-store`. A `_copy.db` filename does not require copying, and
a nearby profile/store name does not require a read. Name these as references
unless the matcher also requires the operation. Executable/process basenames
follow `application/executable`; serialized password/cookie field syntax follows
`data/serialize/schema-object`; cookie getter/setter methods follow HTTP cookies.
KWallet/libsecret wallet, service and schema references follow the keyring
capability. Neither a brand set nor a JSON field alone establishes a collector.

Browser ownership is a source boundary, not an implementation environment.
`stealer/browser` admits probable export of browser-owned cookies, saved
credentials, storage state, and browsing records. An extension that sends a
screenshot follows `screen`; independently required browser data plus a
screenshot follows `multi-source`. Alternatives between browser passwords and
wallet, mail-client, or cloud credentials follow `credential`, unless one
narrower source is required. Protected Storage passwords without a browser
target follow `keychain`: a generic name/password report format does not
establish browser ownership. Local acquisition stays in credential-access or
collection; cookie APIs, analytics labels, and JSON construction stay neutral.

Browser-export admission requires evidence for both the browser dataset and its
probable transmission. Library co-occurrence, ad-hoc signing plus an HTTP client,
or a browser-store name plus a wallet brand do not supply that relationship.
These remain useful capability observations. A specialized cookie-reader module
belongs with HTTP cookie handling; an HTTP cookie-jar module belongs in
`communications/http/cookie-store`. Neither is a temporary-file technique merely
because a bundler can package it. A TLS write API reference belongs in
`communications/socket/ssl`; the browser-export composite supplies the cookie
target and session context. Explicit browser export takes precedence over its
local acquisition category; reference the acquisition rule from the exporter.

Disambiguate overloaded terms by the resource, not the spelling. PyInstaller's
archive "cookie" is a custom archive footer, so its read diagnostic belongs in
`data/archive/custom`, not HTTP cookies or browser credentials. Generic bundled
modules do not identify a bundler; archive-specific diagnostics may still be
referenced explicitly by consumers needing that context. When an exporter moves,
check whether its required acquisition rule already preserves an old directory
consumer before adding redundant alternatives. Also check `needs` counts,
exclusions and spatial conditions; simple existence equivalence is not a proof
for those cases.

HTTP export uses the required source before the channel: appliance configuration,
account stores, environment data, images, and generic local files follow their
`stealer/<source>` homes even when archived, encoded, or sent through several
protocols. Without a required narrower source, `http/archive` owns export
patterns requiring archive packaging or an archive payload; `http/encrypted`
owns payload cryptography with HTTP export context. Archive takes precedence
when both are required. `http/encoded` owns non-cryptographic encodings and
obfuscated HTTP representations; TLS alone does not make an encrypted-payload
rule. `http/upload` retains upload-specific objective patterns lacking those
required refinements. An optional archive, cipher, or source does not choose
the narrower directory. These are placement tests, not automatic justification
for an objective's criticality or confidence.

Neutral POST methods, request-body options, socket sends, route literals,
FormData fields, and MIME types retain their corresponding HTTP/socket
capabilities. In particular, `image/ppm` does not establish a screenshot, and
`Transfer-Encoding: chunked` does not establish Base64 encoding or application
data fragmentation. Archive creation and Base64 conversion stay with their
local operations. A consumer can infer export from these observations without
moving or copying them into the objective tier.

`micro-behaviors/crypto/hybrid` owns evidence combining symmetric payload
cryptography and asymmetric key wrapping, including envelope/algorithm-pair
references. `library` is not an intervening mechanism. Standalone signing,
generic provider APIs, and individual algorithms do not qualify merely because
a hybrid composite consumes them. `data/serialize/bittorrent` owns creation of
BitTorrent metainfo, including tracker/web-seed configuration and archive
publication. Existing metainfo fields and format references remain in
`data/format/bittorrent`; a torrent creator is not inherently a data thief.

For transport-only evidence, `exfiltration/http/header` owns attack-specific
HTTP-header channels and their vocabulary. A required `X-Exfil-Data` label with
optional browser or DNS context is neither browser-specific nor necessarily
DNS. Ordinary header access stays under HTTP capabilities. Header, query, and
body are different carriers; a known required stolen source takes precedence
over all three.

HTTP client observations do not become theft because a credential composite
consumes them. An OR over POST, upload, or curl mechanisms belongs with request
clients and retains that meaning in every consumer. Within request capabilities,
use the required facet first: JSON encoding → `request/json`, body construction
or transmission → `request/body`, method selection → `request/verb`, and bearer
authorization → `authorization-header`. General client calls and mixed client
mechanisms stay in `request/client`. A nearby label such as `vsent` does not
change a request observation into theft; the objective must add source evidence.
The duplicate `http/body` branch is retired: outbound body observations use
`request/body`, and no-CORS request mode uses `request/configuration`. Request
JSON remains a more specific facet than an unspecified body. Do not reopen the
old branch as another home for the same operations.

Browsing history and navigation records follow the same source rule as browser
cookies: local observation belongs in collection, while probable remote export
belongs in `stealer/browser`. A mere HTTP client accompanying local history
collection does not establish a reporting channel. Navigation-record fields and
page/referrer reads remain neutral capabilities. Do not count a recognized
cookie library or generic bundle marker as browser-theft evidence.

Local-storage evidence must require a storage interface; encryption, decryption,
or key import alone is not local storage. URL serialization and a URL near a
request-body field are distinct observations. Export composites can accept
either as corroborating record construction, but must independently require
the observed browser source and a transfer channel. Do not create a mixed
"upload payload" alias that turns either neutral observation into an objective.

Mail has three separate subjects: message content, authentication material, and
addresses/contacts. Mailbox-message collection belongs in `collection/email-harvest`;
remote export of message content belongs in `stealer/message`. Exported mail
account passwords or SMTP credentials belong in `stealer/credential`, unless
another established secret-store source is required. A mail client or email
transport does not make its payload message content. Browser session clues used
for mailbox reconnaissance follow mail collection, not browser-data export.

Under `micro-behaviors/communications/email`, `address` owns address recognition,
extraction, normalization and address-handling references; `mime` owns message
headers/content and attachments; `auth` owns authentication evidence; `queue`
owns message queuing. `access` owns mailbox client, enumeration and reading
interfaces (IMAP, MAPI, Exchange/EWS and webmail application endpoints). `send`
requires sending evidence: an Exchange client, folder query or attachment
constructor alone does not meet it. Provider authentication and request-parameter
references follow the named service when they identify that service rather than
email data handling. Collection composites combine these capabilities with their
source and acquisition context; generic capabilities do not become objectives
through their consumers.

A `MailItemsAccessed`/Bind audit record describes a recorded event and follows
`os/telemetry/logging/event`; it is not itself a harvesting implementation.
API/client GUID fields without that event context follow structured record
fields in `data/serialize/schema-object`. Names/descriptions must say whether
they recognize a record, a method reference, a path, or a probable workflow.
Address-book registry keys stay under registry keys, mailstore paths under
personal-data paths, and writing an address list to the clipboard is clipboard
output. None alone establishes harvesting or remote export.

TLS certificate-verification callback setters/customization belong in
`communications/tls/verify/callback`, regardless of the client using them.
`verify/disable` requires evidence that verification is disabled or bypassed;
installing a callback does not establish that. Keep the distinction even when
the sibling cohort is small: it prevents a meaningful security overclaim.

Structured-record declarations and access operations are different observations.
`data/serialize/schema-object` describes named fields or field combinations in
records. Reading a named key with a mapping lookup belongs in
`data/collection/map`; branching on a decoded response belongs in
`data/control-flow/branch`. A helper name does not establish an object schema:
cookie-access helpers follow cookies, a share-link constructor follows URL
construction, and an unstructured status label follows telemetry vocabulary.

`screen` owns probable export of displayed content: desktop/window/tab images,
screen streams, and text derived from displayed content (for example, OCR).
The acquired information decides placement, so a captured browser tab belongs
here rather than with browser-owned stores. Host identifiers accompanying a
screen report do not create an independent dataset. Local capture with
collection context belongs in `collection/screenshot`; capture APIs
alone remain capabilities. Neither a timer nor a streaming representation
changes the source; screen streaming with remote delivery belongs in `screen`.

`image` owns probable export of image data when the matcher leaves its origin
open. Bitmap copying, pixel readback, and image encoding do not themselves
distinguish screen pixels from an off-screen image. Prefer `screen` when the
whole matcher supports that source; use `image` for unspecified visual content,
and a camera source when acquisition specifically identifies camera recordings.
This is an information-source distinction, not a PNG/JPEG/filetype partition.
Known image content takes precedence over generic `file`; independently
required image and process-dump datasets belong in `multi-source`.

`audio` owns exported sound, including microphone recordings and audio whose
origin remains unspecified. An MP3 encoder does not identify a microphone.
`camera` owns exported camera imagery or camera streams. `audiovisual` owns a
recording whose source selection permits audio, camera video, or a combined
recording without requiring one narrower source. Use the narrower source when
the whole matcher identifies it. Screen-specific acquisition still goes to
`screen`; camera and microphone tracks within one recording do not by themselves
establish independent stolen datasets. Separately required screen/camera streams
or keyboard/screen acquisitions can establish `multi-source`. HTTP response
streams and public relays deliver data just as uploads do.

Local acquisition follows the same subjects: `collection/audio`,
`collection/camera`, `collection/screenshot`, or `collection/multi-source` for
independently required datasets. Optional sources, activity-control commands,
and unrelated graphics APIs do not establish multiple acquired datasets.
An input-injection channel follows remote control; redundant startup mechanisms
follow persistence even if a screenshot capability supplies optional context.

For keyboard evidence, distinguish observing input from generating it. Hooks,
listeners, polling APIs, and their implementation references belong with those
keyboard capabilities unless the whole matcher supports collection intent.
Logging or staging captured keystrokes belongs in `collection/keylog` by its
acquisition mechanism; exporting them belongs in `stealer/input`. Synthesized
keystrokes, including System Events `key down` commands, belong in
`hardware/input/keyboard/simulate`. An automation-service name without a keyboard
operation remains general automation. Filenames, event-field labels, and a
generic send method cannot independently establish that keystrokes were acquired.

Within `collection/keylog`, `hook` owns interception through a keyboard hook or
listener, `polling` owns repeated key-state queries, `device` owns direct input
device/HID acquisition, and `terminal` owns terminal-input collection. When a
keyboard hook invokes state queries, interception remains the acquisition
mechanism. `capture` is the legacy remainder, not an alternative home for a
known mechanism. A combined key-recording/store signature whose acquisition
mechanism remains unspecified can stay there pending the remainder's audit;
database/table names alone remain neutral keyboard labels. Independently
required clipboard or screen acquisition moves
the whole collection composite to `collection/multi-source`; sending acquired
keys moves it to `stealer/input`, regardless of the transport.

Direct input-event device reading, including evdev, uses `keylog/device`;
`evdev` is not a second home for that mechanism. Keyboard notifier interception
with recording/exposure context uses `keylog/hook`, including kernel callbacks.
The callback API, header, event-code gate, buffer copy, and character-device
creation are independent capabilities. Their execution context does not turn
them into collection by itself.

`collection/touch` owns collection of touch positions/gestures with collection
context, such as a remotely tasked agent. Raw coordinate reading/decoding alone
is an input-device capability. Touch positions are not typed characters: a
keyboard interpretation needs mapping or other keyboard evidence. Input export
still follows `stealer/input`, whether its source is keys, form values, or touch.

CSS field-value selectors paired with conditional remote resource requests,
and their corresponding character-log receiving service, belong in
`stealer/input`. A selector with a local or unspecified image URL remains a
styling capability. Parameterized log/focus routes, indexed buffers, stylesheet
paths, and password-field attribute updates do not independently establish
collection. They keep their route, data-access, path, or form-input homes.

The neutral capabilities have narrower contracts:

| Directory under `micro-behaviors/` | Admission and tie-break |
|---|---|
| `ui/window/hook` | Generic window-hook installation, chaining, removal, and lifecycle. `SetWindowsHookEx` without a keyboard hook type does not select keyboard interception. |
| `hardware/input/keyboard/hook` | Keyboard-specific hook interfaces, key grabs, or hook types. Generic window hooks remain under windows even when a keylogger consumes them. |
| `hardware/input/keyboard/listener` | Keyboard events, event codes, and subscriptions without a narrower interception mechanism. A KeyPress handler need not be global. |
| `hardware/input/keyboard/poll` | Queries of key state and virtual-key polling loops. |
| `hardware/input/keyboard/layout` | Key-code translation and keyboard layouts, including conversion to characters. |
| `hardware/input/keyboard/label` | Keyboard/keylogger names, key-name tables, and declared or placeholder keyboard functionality. Descriptions must distinguish declarations from implemented collection. |
| `hardware/input/keyboard/simulate`, `hardware/input/mouse/simulate` | Generation of input of the named kind. `synthesis` is not a separate technique. |
| `hardware/input/event` | General input event interfaces, state, payloads, and handling, including libraries and composites spanning keyboard and mouse. Use the keyboard or mouse child only when the matcher identifies that narrower subject. |
| `hardware/input/device` | Input-device inventory, paths, and device references. A path or filename filter alone does not establish a keyboard event read. |
| `hardware/input/mouse/position` | Pointer coordinates and pointer-information queries; a generic mouse-state name does not identify position. |
| `ui/window/probe`, `ui/window/enumerate` | Window-class references and identification belong in probe; window title/text queries belong in enumerate. A class-name set containing general GUI windows is not specifically a browser/WebView capability. |

Generic compiler execution, formatted headings, log filename templates, temporary
paths, thread creation, and writable file modes keep their corresponding
capability homes. Their use by a keylogger does not change their subject.
Content referring to a filename remains a path observation; matching the
analyzed artifact's own basename is file metadata.

Browser observation and telemetry follow the same evidence-role distinction.
Tab/navigation listeners and URL extraction are browser capabilities; JSON
serialization is not upload, and a request-body fragment is not a completed
request. Local storage, cookie lifetime, and uninstall-URL registration remain
their respective capabilities. Collection requires source/retention context;
export follows the acquired source even when its transport is an analytics SDK.
An SDK name or endpoint alone does not establish that sensitive data is sent.

Within neutral telemetry, `os/telemetry/logging/event` owns named event/status
vocabulary and combinations of those labels. A failure/success event name is
evidence of an instrumentation interest, not proof that its named operation
occurred. `os/telemetry/activity` owns activity-report fields and combinations
of fields/events describing what is monitored. `logging/analytics` owns analytics
interfaces, property bags, identity configuration, and forwarding context;
`communications/http/telemetry` owns telemetry endpoints and request mechanics.
Use the more specific protocol operation when required. A bare path-field name
stays with path references, and a generic chat-send label stays with messaging;
neither becomes telemetry merely because a reporting composite consumes it.

An empty allowlist and an unsuccessful array lookup do not establish a return,
disabled collection, or a kill switch. File those observations with array
operations until an execution-control matcher supplies the claimed consequence.
Browser executable filenames are application-path references; they do not
establish process enumeration, browser history access, or the analyzed file's
own identity.

Wallet evidence follows its required subject, not the desktop/mobile packaging
of the application. Use these boundaries before placing a wallet-related rule:

| Required observation | Home and boundary |
|---|---|
| Wallet database, keystore, vault or data-directory location | `micro-behaviors/fs/path/wallet`; constructing or mentioning the location does not establish a read. A roll-up of locations remains a location observation. |
| Installed application bundle location | `micro-behaviors/fs/path/application/bundle`; `/Applications/Trezor Suite.app` locates an application, not its secret store. |
| Named application or package reference, including an OR with its store location | `micro-behaviors/os/application/target`; the whole matcher must require a store location to qualify for the wallet-path leaf. A product string does not identify the analyzed artifact as that product. |
| Wallet-specific recovery/connection interface | `micro-behaviors/ui/controls/wallet`; an unqualified “SECRET PHRASE” label instead belongs in `ui/dialog/prompt`. |
| DPAPI reference or Telegram-send member/channel name | The protection or messaging capability respectively. A wallet consumer does not give these generic observations a wallet source. |
| Probable wallet-secret acquisition without export | `objectives/credential-access/wallet/<mechanism>`; a path or application name alone remains neutral. The legacy `desktop` leaf is being reconciled, not an admission rule based on packaging. |
| Required seed-phrase source and probable export | `objectives/exfiltration/stealer/wallet`, including seed-entry forms. An alternative allowing a generic private key or unqualified secret phrase follows `stealer/credential` unless other required evidence establishes a wallet source. |

Credential-entry interfaces belong in `micro-behaviors/ui/controls/credential`
when their required subject is private-key or other authentication-material entry
and a wallet source is optional. This includes entry/recovery labels, verification
controller symbols, input surfaces, and page-level combinations. Wallet-specific
phrase/connection interfaces remain in `ui/controls/wallet`; an OR accepting a
generic private key follows the broader credential interface. Generic secret
wording without a required authentication-material type remains in
`ui/dialog/prompt`. None of these interfaces alone establishes deception or theft.

Application names, repeated brand references, named provider objects, and brand
catalogs belong in `os/application/target`, including wallet brands. A reference
to TronLink or an injected Phantom provider does not identify the analyzed file
as that independent artifact. Such words must not activate blanket known-app or
known-library exclusions merely because they previously occupied `well-known`.

A termination command or force-kill near an application path belongs with
`process/terminate/command`. A required named wallet application path supports
wallet context; an unqualified `/Applications/` path alone does not.
A composite combining concealed UI, termination, and wallet context may infer
process interference in `objectives/impact/degrade/process`; it must not claim
file replacement or credential access without that evidence. A wallet-associated
LaunchAgent label belongs with `os/service/launchagent`. Labels, recovery UI,
RunAtLoad text and LaunchAgents paths alone do not require spoofing, installation,
or export. Do not add a hostile wrapper to turn those clues into such claims.

File-search vocabulary and operations share `micro-behaviors/fs/search` when
their subject is selecting files. A wildcard literal supports a possible target;
a find-option fragment supports a search interface. Descriptions must distinguish
those clues from a matched command or traversal call. Language, source versus
binary, and target extension do not create competing hierarchy layers. The shared
`fs/search::recursive-file-discovery` selector combines traversal evidence with
the relocated application-bundle search. It is incomplete discovery evidence for
consumers, not a second definition of a search operation or proof of acquisition.
Keep such cross-mechanism combinations explicit; do not copy the underlying
matcher into both operation directories. Interpreting
configuration contents follows `data/config/load`, even when a parser method
names a file; finding that file follows `fs/search`.

A file-search plus transfer classifier follows `stealer/wallet` only when every
source alternative requires wallet evidence. An OR permitting generic `id.json`
search evidence follows `stealer/file`. Neither filename selection alone nor an
extra wrapper around a filename filter establishes theft. Preserve the selection
observation and require acquisition/transfer context in its consumers.

Directory consumers must retain useful source clues explicitly after relocation.
A wallet-source selector can reuse named application/store observations, but must
not inherit generic messaging, protection or prompt observations merely because
they once lived beside wallet rules. Such selectors express incomplete source
evidence; the consuming objective supplies acquisition or transfer context.
Counts of clues or repeated mentions do not prove multiple stores, reads, sends,
or repeated harvesting. An invalid-seed message beside one export is not evidence
of a second harvest.

Wallet address extraction interfaces belong in `data/parse/wallet` when they
identify parsing/extraction of wallet information without requiring secret
material. Public addresses are not private keys. Browser profile/path discovery
method references belong with browser application paths; reporting method
references belong with telemetry or URL construction. Named implementation
methods can support these capability inferences without establishing that the
program is a blockchain client or that it steals credentials.

When a composite claims several distinct named methods, use separate atoms and
an `any`/`needs` threshold. A regex occurrence count can be satisfied by repeated
copies of one alternative; it does not establish method diversity. A wildcard
method-name count likewise must not be described as a count of distinct wallet
providers unless distinctness is actually enforced.

Neutral `hardware/input/media` owns acquisition interfaces that leave audio
versus video open, such as `getUserMedia`, and mixed webcam/microphone controls.
`data/stream/record` owns stream recording and emitted recording chunks, including
synthetic streams; MediaRecorder alone does not identify a display, camera, or
microphone source. Named screen/webcam stream routes support their respective
capabilities. A generic stream handler belongs in `process/io/stream`, an HTTP
route definition in `communications/http/server/route`, and tunnel bootstrap or
numeric server selectors in `communications/proxy/tunnel`. A selector's meaning
must come from other evidence, not a source-specific trait name.

These boundaries classify probable capabilities, not proven execution. A
distinctive capture name, API reference, or image artifact can support an
inference when read with the other required evidence. Descriptions must not
claim a narrower source than the matcher supports. Generic raster operations
belong in `ui/graphics/draw`, image construction/readback in `ui/graphics/image`,
encoding in `data/encode/image`, display geometry in `hardware/display/state`,
and window bounds in `ui/window/region`. Window enumeration or device-context
access without pixel capture stays with windows. Image-path observations remain
in `fs/path/media`; explicit capture consumers may reference them. Source code
versus compiled form never creates a separate `native-capture` technique.

`file` owns exported files or staged file bundles when their content is not
confined to a more specific source. A search over sensitive filename extensions
does not establish every possible source those extensions could represent.
Pure targeting belongs in `collection/file-targeting`; credential acquisition
without export belongs in `credential-access`. Permission bundles belong in
the permission capability, and references to history or credential-config paths
remain path capabilities. Query fields naming collection stages belong with
the transfer protocol unless the matcher independently requires source evidence.
Within file targeting, `filter` owns selection by filename/extension patterns;
`identity-set` owns combinations identifying targeted files or stores, including
combinations that reuse filters. A group of target indicators is not an export
or a claim that every matched indicator represents another dataset.

Review threshold composites by evidence role as well as matcher identity.
Putting endpoints and source indicators in the same `any` list can satisfy a
theft claim using only endpoints, or using only local source paths. Require each
necessary role separately. Identical-body validation cannot detect this error:
two different endpoint matchers may still supply the same semantic role.

The former `phish` leaf classified an acquisition method; its exporting rules
now live in `input`, while local capture and archive staging have their own
objective homes. Legacy `surveillance` still classifies a purpose and overlaps
captured input. Its two Go input-export rules have moved to `input`; audit the
remaining rules by exported data (audio, video, message) before splitting.
Audited screen and image exports now use the source contracts above; local
capture and neutral graphics operations no longer acquire export meaning from
their former placement. Unresolved mixed-source or control-channel matchers
remain a review backlog, not an admission contract for new surveillance rules.
Keep phishing-method evidence under credential-access and reference it from the
source-specific export. See the [stealer migration plan](docs/taxonomy-audit/STEALER-SOURCE-PLAN.md)
for rule dispositions and ordering.

HTTP evidence uses the same whole-matcher distinction. `http/user-agent`
owns that header's values, reading/setting/testing it, and pools of those values.
`http/fingerprint` owns client-hint/fetch-metadata fields and profiles spanning
several HTTP fields. Selecting a browser's TLS/HTTP transport impersonation
profile belongs in `http/tls`; it does not merely set a User-Agent. Credential
provider modes and assumed-role records belong in `os/security/auth/cloud`,
even when found beside a user-agent in an audit record. None of these neutral
capabilities alone establishes export of host information.

`http/upload` owns file/data upload operations and their recognizable invocation
patterns. A content-type header alone belongs in `http/header/content-type`;
other named headers belong in their header category. `http/form` owns form and
multipart construction, fields, attachment descriptions, and form submission.
A filename suffix without form context belongs in `fs/path/extension`.
Constructing a Blob with a gzip media type belongs in `data/buffer/alloc`:
the label does not establish compression or transmission. Yarn bundle identity
belongs in `well-known/tool/packaging/yarn`, even if an upload rule once used it.

Endpoint paths such as `/collect` and `/exfil` belong in
`http/url/endpoint` when no source or unauthorized-transfer condition is required.
A request method or client marker can qualify endpoint evidence without turning
it into an exfiltration objective. Required stolen-source evidence follows the
stealer source contracts; otherwise an actual theft/transfer inference is needed
for `exfiltration/http/collect`. Password/secret assignments remain authentication
capabilities, not collection or export by themselves. An IP upload destination
whose alternatives include bare IP and IP:port values belongs in `ip/endpoint`;
`http/url/external-ip` specifically requires an HTTP URL form.

Broad directory consumers inherit these boundaries. Do not preserve a former
upload vote from a relocated header, suffix, package identity, or form-field
fragment merely to retain a score. Preserve explicit references and test actual
transfer controls; repair any lost legitimate inference using the evidence the
consumer actually needs. Identical bodies with different effective scopes or
suppression conditions require a coverage-aware merge, not automatic deletion.

RouterOS query literals follow the resource queried, just like other APIs:
interfaces → `network/interface`; routes → `os/network/route`; firewall
configuration → `os/firewall/query`; wireless configuration →
`hardware/wireless/network`. The hierarchy does not acquire a RouterOS layer.
`os/firewall/probe` means checking availability of firewall tooling, not reading
its rules. A host-profile accessor spanning identity, hardware, software, or
health goes in `os/sysinfo/profile`; configured services/tools go in
`os/sysinfo/config`. Multi-resource network status queries go in
`os/network/status`. Coordinated reconnaissance remains an objective assembled
from those capabilities; `discovery/network/enumeration` owns the network-only
query combinations, while `discovery/system/profile` owns broader host surveys.

An object-field matcher belongs in `data/serialize/schema-object`. JSON Pointer
token escaping (`~` → `~0`, `/` → `~1`) belongs in `data/encode/json-pointer`:
it transforms a path token rather than recognizing an object schema.

### Persistence: the activation boundary, not the file location

The former “firmware / OS boot / user login” wording is too narrow for permanent
event subscriptions, application hooks and retained account access. Use these
ordered level-2 contracts, then name the activation/access mechanism at level 3.

| Level 2 | Admission and level-3 examples | Exclusion |
|---|---|---|
| `firmware` | Durable activation below the OS: boot records, firmware/NVRAM changes. | An ordinary firmware query/update API is a capability. |
| `access` **planned** | Retain authentication/authorization through accounts, keys, tokens or grants; code execution is not required for the persistence claim. | Account enumeration and ordinary credential reads are not retained access. Reconcile login/account and login/ssh here. |
| `login` | Activation requires a login/session-start event: Run keys, startup-folder items, Winlogon, XDG autostart, login shell profiles. | HKLM vs HKCU and “runs as this user” do not decide the trigger. A Run key remains login even under HKLM. |
| `application` **planned** | Activation requires an application/runtime/project event: plugin load, interpreter startup/import, editor or repository hooks. | A hook declaration alone is metadata; session-start shell profile activation remains login. |
| `system` | Durable OS-managed activation independent of a required user-login or application event: services, boot scripts, cron/timers, permanent WMI events. | `fork`/`setsid` and a process surviving its parent do not establish reactivation. A user-owned timer is not necessarily login-triggered. |

Within `login`, registry Run keys go to `registry`, filesystem startup entries
to `startup`, Winlogon changes to `winlogon`, and shell startup configuration to
`shell`; do not repeat registry under startup. Within `system`, service-manager
registration uses `service`, not a parallel `systemd` sibling; WMI subscriptions
use `wmi`, not service. Platform, privilege and file location are matcher scope.

### Supply-chain trust and generic outcomes

Package scope is necessary for many supply-chain rules but is **not sufficient**:
the rule must establish a component/distribution trust violation, not merely
run inside a package. Read its claim with the package name removed; if it still
only says “steals credentials” or “runs a downloaded payload,” that result owns
the composite and the lifecycle context is a referenced fact.

| Canonical behavior | Admission and level-3 distinction | Competing legacy branches |
|---|---|---|
| `supply-chain/impersonation` | Misrepresented name, provenance, functionality or contents in component selection/distribution. Required deception comparison chooses the child, not manifest/registry/archive carrier. | `manifest`, `registry`, wheel/sdist and package-metadata buckets are not deception techniques; ordinary name similarity is a metadata fact. |
| `supply-chain/trojanized` | Unauthorized substitution/modification of an otherwise legitimate component or trusted build/update input/output. Distinguish dependency substitution, build-pipeline modification, update substitution and configuration poisoning. | A wholly malicious loader is not proof that legitimate software was modified. Product identity alone is not proof of a trojanized copy. |
| `supply-chain/hidden-payload` | Concealment that specifically abuses package inspection, declared contents or a distribution trust boundary. Name the required concealment mechanism. | Generic encrypted/embedded code → anti-static; neutral layout/manifest facts → metadata; full activation chain → dropper. |
| Credential access or theft during install/build/import | Canonical credential-access or exfiltration source, referencing the lifecycle/build context. | Retire duplicated results in `supply-chain/credential-theft` and `recon-exfil`; a registry token remains a credential even outside installation. |
| Host-profile discovery or export during an install hook | Discovery-only command/field evidence → `discovery/system/profile`; a required host-profile source plus outbound transfer → `exfiltration/stealer/system-info/profile`. Keep the install-hook declaration as a referenced context leg. | The hook is a trigger, not the collected data or the transfer result. |
| Execution/persistence during a package lifecycle | Canonical execution/dropper/persistence outcome, referencing the hook fact and any separate trust-violation composite. | `install-hook` is not a second objective tree. Neutral declaration → `metadata/package/scripts/lifecycle`; actual package-manager operation → `micro-behaviors/os/package-manager`. |

For overlaps within supply-chain, required modification of an established
legitimate input/baseline wins (`trojanized`); otherwise required concealment
from package inspection wins (`hidden-payload`); otherwise required deceptive
selection/identity claims use `impersonation`. Dependency confusion through a
misleading registry identity is impersonation; rewriting a trusted dependency
configuration is trojanization. Each needs evidence of its particular trust
violation. Merely naming a dependency or containing encoded bytes is neither.
`hidden-payload/runtime` is a legacy holding area, not an admission category:
runtime phase alone does not describe concealment. Move full acquisition-to-
activation chains to `command-and-control/dropper/<sink>`, attacker tasking or
access to its command-and-control result, and required source-plus-transfer
chains to `exfiltration/stealer/<source>`. Keep a rule in `hidden-payload/`
only when its required evidence specifically establishes the package or
distribution concealment named by that leaf. Treat package lifecycle and
runtime identity as context unless they establish the trust violation.

### Metadata subject ownership

Use the property being asserted, not the matcher implementation. A parser can
expose a company name, an API or a credential; those facts keep their own meaning.
Conversely, a text matcher of a structured field remains a fact about that field.

| Level-1 subject | Level-2/3 ownership | Nearest competing home |
|---|---|---|
| `arch` | Artifact instruction-set/ABI target, refined by architecture family. | Compiler identity → lang; hardware queries → capabilities. Architecture is the subject here, not a platform split for an unrelated behavior. |
| `binary` | Anatomy: header, section, symbols, code, resource, linking, layout, debug. Level 3 is a property of that part: section entropy, header geometry, symbol count, layout overlay. | Whole-file size/format → file; compiler attribution → lang/compiler; signed identity → signed; named API/product → its capability/identity. |
| `build` | Build configuration and transformation: compiler invocation/config, bundling, minification, transpilation, scaffolding, packaging, CI. Children name transform or pipeline property, not software identity. | “Built with compiler X” → lang/compiler; “this file is compiler X” → well-known; an artifact's manifest field → package. |
| `document` | Parsed document subject and part: office macro/container, PDF action/form, RTF structure, HTML structure, OLE container. | Embedded code's behavior stays with its behavior; filename/magic alone → file. An OLE container fact does not prove an Office application identity. |
| `file` | Generic whole-file identity, extent and representation: format, extension, magic, size, encoding, text profile. | Specific parsed anatomy → binary/document/image; specific field/resource meaning takes precedence over generic string/catalog buckets. |
| `hardening` | Artifact policy/mitigation properties: sandbox declarations, executable-memory policy, build/layout mitigations. | Actual security API use is a capability; bypass is an objective. “Missing” is a value of a mitigation, not a parallel subject. |
| `image` | Image-specific pixel/channel/segment properties. | Generic image file identity → file; rendering/capture → hardware/UI; concealed payload intent → objective. |
| `font` **planned schema** | Font-specific container/table validity and layout relationships. | Generic font magic/extension → file; format-independent byte coverage → media. A claim requiring a font table identity stays font. |
| `media` **planned schema** | Cross-carrier container/byte-coverage properties shared by fonts, images, audio and video. | Pixel, glyph, codec or format-specific table relationships use their specialized subject. A carrier-specific parser alone does not change an otherwise identical generic coverage claim. |
| `import` | Artifact/code dependency reference, without claiming the artifact is that dependency. Static children distinguish builtin/package/framework reference; engine-generated language/module IDs retain their schema. | Manifest declarations → package/dependencies; import-table cardinality → binary/symbols; observed API → its capability; library identity → well-known. |
| `lang` | Source/artifact language, compiler attribution, runtime requirement, language version and encoding. Level 3 refines that same language property. | Transform output → build; shipped runtime/library identity → well-known; natural-language content alone belongs to its language property, not a data operation. |
| `package` | Declared package fields and package-member/project properties. Level 2 names the field/resource, level 3 its facet. | Registry reputation/history → registry; behavior of a lifecycle script → its capability/objective; named package identity is not any arbitrary dependency declaration. |
| `permission` | Declared authority, grant scope and activation rights. Level 2 names the protected surface; level 3 refines grant breadth/property. | API invocation → capability. A declared clipboard permission does not prove reading the clipboard. Ordinary extension identity/description is a package property. |
| `registry` | Package-registry publication record: release/package history, reach, ownership and listing claims. Registry provider goes in the filename; new subdivisions must name those properties. | This is not the Windows registry (`micro-behaviors/os/registry`). Bundled manifest facts remain package metadata; reputation is not an attack verdict. |
| `signed` | Signature/certificate/entitlement/trust facts. Under certificate choose the required role: `subject`, `issuer`, `signature`, or `security`; `issuer/name` is a certificate's claimed issuer name, `issuer/chain` is chain structure, and named verified issuer sets such as `issuer/microsoft` or `issuer/attestation` are exact chain-thumbprint identities. | Installing/verifying a certificate → crypto; vendor string without signature provenance → vendor/provenance; a timestamp authority or issuer does not establish the artifact's leaf signer. A Microsoft third-party attestation CA proves Microsoft attested to the signer, not that Microsoft authored the signed code. |
| `vendor` | OS/platform vendor provenance claims, refined by the claimed role or evidence surface. | Third-party product identity → well-known; certificate subject → signed/certificate; manifest vendor field → package/vendor. |

For certificate rules, classify by the certificate role/property the matcher
actually reads, using this precedence when one rule appears to fit several
labels:

| Matcher evidence | Canonical home | What it does not establish |
|---|---|---|
| Distinguished-name fields on the signing leaf certificate | `metadata/signed/certificate/subject` | Product identity or verified issuer identity. |
| Issuer distinguished-name text | `metadata/signed/certificate/issuer/name` | That the named authority issued the certificate; names are claims. |
| Exact verified-chain thumbprint for a Microsoft code-signing CA | `metadata/signed/certificate/issuer/microsoft` | Microsoft authorship when the CA is a third-party attestation authority. |
| Exact verified-chain thumbprint for a Microsoft third-party component CA | `metadata/signed/certificate/issuer/attestation` | Microsoft platform provenance; it establishes attestation of another signer. |
| Presence, length, or shape of verified chain entries | `metadata/signed/certificate/issuer/chain` | The identity of any authority in the chain. |
| Signature verification, digest integrity, or nested-signature state | `metadata/signed/certificate/signature` | Signer identity by itself. |
| EKU, key usage, or other certificate security constraints | `metadata/signed/certificate/security` | Whether the signature verifies. |

When a rule combines these facts, split independent observations into canonical
atoms and let the composite state the combined result. Do not place an issuer
name string under a verified-authority directory, or infer a product/platform
identity from certificate text alone.

`font` and `media` are documented schema namespaces without YAML directories in
this checkout. Their table definitions settle ownership before materialization;
the migration must also update the whitelist and any engine-emitted IDs.
Empty/example directories are not evidence of an existing rule home.

At `metadata/package`, the field wins over the file that contains it: `name`,
`author`, `description`, `license`, `repository`, `version`, `runtime`,
`entrypoint`, `scripts`, `dependencies`. Level-3 script children distinguish
automatic lifecycle, explicitly invoked build/development, and named command
entrypoints; the **trigger declaration**, not the script's eventual behavior,
chooses among them. Dependency children distinguish manifest, lockfile and
shipped archive facts; use the ordered facet rubric below for deeper refinements.

For package contents: `files` owns members/layout; `documentation` owns
documentation roles; `testing` owns harness/fixture/assertion roles; `integrity`
owns checksums/content agreement; `config` owns declared configuration. A test
fixture's role takes precedence over a generic member count/path. Plain README
presence is documentation, not package description. A checksum manifest is
integrity, not generic completeness. Language and ecosystem do not choose
between compiled/scripted testing buckets; reconcile those by test role.

Within documentation, `claims` owns statements about the package's promised
properties or purpose; `security-advisory` owns advisory references and removal
notices; `source` owns documentation filename/location observations. A claim
read specifically from the manifest's `description` field instead belongs in
`description/<subject>`, even if identical words could appear in a README.
A placeholder claim does not prove deception, and a removal notice does not
authenticate its author. Objective composites must supply those extra facts.
Prose matchers must admit their actual document types; inheriting a manifest-only
scope for README text makes a README composite ineffective.

For `permission/host`, grant breadth distinguishes **planned**
`all-origins`, `domain-pattern`, and `explicit-origin` children. A hostname
literal without a grant context is not permission evidence. Engine-emitted
`micro-behaviors/browser-extension/{host-access,permission}/<value>` IDs are a
separate existing producer schema; reference them where appropriate, and do not
copy their matchers into YAML or move their IDs without an engine/consumer migration.

### Known entities: one identity, one primary function

The entity's own fingerprint must pass the recognition and specificity bars
above. A generic API, a dependency name in another package, an embedded
implementation signature and a company signer are not interchangeable with
“this artifact is this product.” Embedded implementation evidence follows the
[technique-first contract](#implementations-and-library-fingerprints). Level-3 product
names inherit the admission contract of their function; they are not thousands
of new behavioral categories requiring separate copies of the behavior tree.

Choose the level-1 class in this order:

| Class | Admission and tie-breaker |
|---|---|
| `malware` | A recognized malicious family, with family-specific evidence. Choose its established defining behavior at level 2 and family at level 3. A legitimate product's name alone cannot establish a malicious variant. |
| `unwanted` | A recognized unwanted-software family whose distribution/operation itself earns that classification, without claiming all instances are hostile malware. Direct family children remain valid. |
| `lib` | The identified component is consumed as a library/framework/runtime. Function at level 2 wins over language, native/managed implementation or vendor. Its standalone developer executable may be a separate tool only if it is a distinct component with distinct evidence. |
| `dual-use` | A legitimate product whose primary purpose fits the specific access-control, credential recovery, executable packaging, remote administration, bulk transfer or tunneling class. These defined functions take precedence over generic app/tool categories. |
| `game` | Game/platform identity or a game-specific gameplay/mod component, with no narrower unwanted/malware determination. A general security exploitation framework is a tool, not a game because one target is a game. |
| `tool` | A professional developer, administrator or analyst utility: build/CLI, packaging, detection, forensics, reverse engineering or offensive testing. End-user applications and reusable libraries use their classes. |
| `app` | An end-user application, integrated service/suite or platform component not admitted by the preceding classes. Level 2 is its primary user-facing function. |

Resolve common level-2 collisions as follows:

| Competing function directories | Ownership |
|---|---|
| `lib/testing` vs `lib/development` | Test execution, assertions, mocks and fixtures → testing; compiler/build/lint/developer infrastructure → development. |
| `lib/format` vs `lib/data` vs `lib/media` | Representation parsing/serialization → format; query/storage/data-model operations → data; audio/video/image processing/codecs → media. A database client is not format merely because its wire format is parsed. |
| `lib/network` vs `lib/web` vs `lib/ui` | Protocol/transport client → network; server/application framework → web; visual/interactive component framework → ui. Being written in JavaScript does not make all three web frameworks. |
| `lib/cloud` vs `lib/vendor-sdk` | Cloud resource/control-plane SDK → cloud even for one provider; other single-vendor product/service SDK → vendor-sdk. Generic protocol support stays network. |
| `lib/platform` vs `lib/runtime` vs `lib/native` | OS/device integration → platform; language execution/FFI → runtime; fundamental native ABI/libc/allocator component → native. Compiled implementation alone does not choose native. |
| `lib/stdlib` vs any specific function | Language standard-library extension/polyfill → stdlib; a distinct domain (crypto, dates, network, etc.) keeps its domain. Small size is not a stdlib classification. |
| `app/development` vs `tool/development` | Integrated user-facing IDE/development application → app; standalone compiler/build/CLI utility → tool. A GUI alone does not turn an analyst debugger into an end-user app. |
| `app/security` vs `tool/detection`, `forensics`, `offensive`, `reverse-engineering` | Deployed/end-user protection product → app; analyst workflow → the specific tool function. A multifunction tool retains its documented primary function instead of receiving duplicate identity trees. |
| `app/infrastructure` vs `app/network` vs `tool/sysadmin` | Integrated deployment/control-plane service → infrastructure; ordinary network application/service → network; operator administration utility → tool/sysadmin, unless the narrower dual-use contract wins. |
| `malware/{downloader,dropper,stealer,backdoor,rat,botnet}` | Classify the recognized family's defining purpose, not every matched capability: remote payload acquisition, embedded/staged payload delivery, theft, access surface, broad remote administration, or fleet coordination. Reference its other behaviors. Delivery in a package alone does not create a second supply-chain family home. |

Before adding any entity, search all function buckets for its canonical name
and aliases. A multifunction entity already assigned to one class stays there
until a documented reclassification moves it and its references together.

### Worked placements and migration status

| Matcher establishes | Home through level 3 | Why a nearby home loses |
|---|---|---|
| A browser saved-login database path | `micro-behaviors/fs/path/password-store` | No read/extraction/send is required. |
| `Popen` with `shell=True` | `micro-behaviors/process/create/shell` | Shell parsing is more specific than the subprocess wrapper. |
| `eval(source)` in the current interpreter | `micro-behaviors/process/interpreter/eval` | No new interpreter process is created. |
| An install hook harvests process-environment secrets and sends them | `objectives/exfiltration/stealer/env` | Install time is referenced context, not another theft category. |
| A host/user profile is sent through Telegram during npm preinstall | `objectives/exfiltration/stealer/system-info/profile` | The profile is the source; Telegram and the package lifecycle are referenced transport/context. Use `exfiltration/messaging/telegram` when no narrower data source is established. |
| A downloaded file is staged and launched | Planned `objectives/command-and-control/dropper/file-exec` | Download method and carrier do not replace the activation sink. |
| A socket listener accepts a shell connection | `objectives/command-and-control/backdoor/bind-shell` | The connection is accepted rather than initiated as a reverse shell. |
| The certificate subject identifies a publisher | `metadata/signed/certificate` | It identifies the signing role, not every product or vendor string. |
| A package declares a named dependency | `metadata/package/dependencies` | This says what another package declares, not that the artifact is the dependency. |
| Bundler-generated module wrappers | `metadata/build/bundler` | Tool output is not the tool's own identity. |
| A bare `memcpy` symbol in a malware sample | `micro-behaviors/mem/c-runtime/functions` | Sample attribution supplies no family-specific matcher evidence. |

The larger trees below are an orientation map containing current and historical
paths; they are not an exemption from these contracts. A conflicting legacy
branch is migration debt, not an alternate authoring choice. Before moving a
cohort, map every rule to these contracts, calculate destination counts, and
rewrite exact and directory references together. Documentation records the
boundary; validation and fixture results verify the migration.

## Tier 1: Capabilities (`micro-behaviors/`)

Value-neutral observations about what code can do. High confidence from static analysis. Maps to MBC [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors): *"low-level, support many objectives and other behaviors, and aren't necessarily malicious."*

```
micro-behaviors/
├── browser-extension/     # Browser-extension (WebExtension) platform APIs
│   │                      #   Irreducibly extension-specific surfaces only — the
│   │                      #   browser is the host platform here, not an OS.
│   │                      #   Generic extension capabilities map to their technique
│   │                      #   homes instead (messaging → communications/ipc/message/,
│   │                      #   storage → data/db/web-storage/, alarms → time/schedule/,
│   │                      #   scripting → process/inject/, webRequest → process/hook/,
│   │                      #   cookies → communications/http/cookies/, downloads →
│   │                      #   communications/http/download/, native messaging →
│   │                      #   communications/ipc/native-host/, identity → os/security/,
│   │                      #   proxy → os/network/, debugger → process/attach/).
│   ├── host-access/       #   Granted origin authority (host_permissions /
│   │                      #     content-script matches). Engine-emitted, one
│   │                      #     dynamic trait per host: host-access/<host>::granted.
│   │                      #     The host is its own subdirectory (not a local id)
│   │                      #     so the UI shows each host and the ML pipeline keys
│   │                      #     a per-host feature; engine IDs use the canonical
│   │                      #     <dir>::<local> form, same as YAML. The grant covers
│   │                      #     DOM injection, cookie reads, privileged cross-origin
│   │                      #     requests, and traffic interception — not mere comms.
│   │   └── shopping/      #     Shopping and e-commerce host targeting
│   ├── permission/        #   Declared API permission, engine-emitted one per
│   │                      #     permission: permission/<perm>::declared (kebab-cased).
│   │                      #     Own subdir per permission (UI + ML). Risk/intent
│   │                      #     (overprivileged, dangerous combos) → YAML objectives.
│   ├── lifecycle/         #   Runtime lifecycle / identity / browser.* namespace
│   ├── tabs/              #   Tab create / query / update / navigate
│   ├── management/        #   Enumerate / enable / uninstall other extensions
│   └── action/            #   Toolbar action / popup surface
│
├── communications/        # Network communication              → MBC: Communication
│   │                      #   Organized by protocol. Neutral mechanics only.
│   │                      #   Port scanning → objectives/discovery/network/scan/.
│   │                      #   Tor hidden services → objectives/command-and-control/.
│   │                      #   DDoS amplification → objectives/impact/dos/.
│   │                      #   DNS tunneling → objectives/command-and-control/.
│   ├── socket/            #   Socket ops (TCP, UDP, raw, bind, listen)  C0001
│   ├── transfer/          #   Protocol-neutral data-transfer operations and clues
│   ├── tls/               #   Transport security, independent of application protocol
│   │   ├── initialize/    #     Prepare configuration or per-connection state
│   │   └── verify/        #     Peer certificate/hostname authentication
│   │       └── disable/   #       Explicit verification-disable APIs/settings
│   ├── http/              #   HTTP/HTTPS (client, server, download)     C0002
│   │   └── direct-socket/ #     Hand-built HTTP over connected sockets
│   ├── dns/               #   DNS (lookups, records, DoH, tools)        C0011
│   ├── email/             #   Email (SMTP, MAPI, MIME, NNTP)            C0012
│   ├── icmp/              #   ICMP (ping, traceroute)                   C0014
│   ├── ipc/               #   Local IPC (pipes, DDE, XPC, host bridges) C0003
│   │                      #   Legacy IRC entries must move to network protocol handling.
│   ├── rpc/               #   Remote procedure-call protocols
│   ├── mcp/               #   Model Context Protocol (stdio and HTTP)
│   ├── ftp/               #   FTP client/upload                         C0004
│   ├── ssh/               #   SSH client/connect
│   ├── ip/                #   IP addressing (parse, resolve, embedded)
│   ├── proxy/             #   Proxy/tunneling (SOCKS)
│   ├── url/               #   URL construction/parsing
│   ├── websocket/         #   WebSocket
│   ├── messaging/         #   Chat/bot platform send APIs (sendMessage, sendDocument)
│   │                      #     Platform-AGNOSTIC message-send verbs only — Slack,
│   │                      #     Discord, Teams, Telegram all share them. The platform
│   │                      #     HOST marker (api.telegram.org) belongs in
│   │                      #     http/services/<platform>/; exfil INTENT belongs in
│   │                      #     objectives/exfiltration/messaging/. Native-messaging
│   │                      #     IPC (browser host bridge) → ipc/native-host/, not here.
│   ├── async-io/          #   Async I/O (epoll, kqueue, io_uring, tokio)
│   ├── capture/           #   Packet capture (tcpdump, wireshark)
│   ├── benchmark/         #   Network performance testing
│   │                      #   --- ICS/OT protocols (neutral mechanics only) ---
│   │                      #   ICS port scanning → objectives/discovery/network/scan/.
│   │                      #   ICS sabotage/manipulation → objectives/impact/degrade/ics/.
│   │                      #   ICS environment discovery → objectives/discovery/system/.
│   ├── modbus/            #   Modbus industrial control protocol         (TCP 502)
│   ├── dnp3/              #   DNP3 SCADA/utility protocol                (TCP 20000)
│   ├── s7/                #   Siemens S7comm/ISO-TSAP                    (TCP 102)
│   ├── bacnet/            #   BACnet building/industrial automation      (UDP 47808)
│   ├── ethernet-ip/       #   EtherNet/IP + CIP industrial protocol     (TCP 44818)
│   ├── opcua/             #   OPC UA industrial interoperability         (TCP 4840)
│   └── profinet/          #   PROFINET industrial Ethernet               (RT/IRT)
│
├── crypto/                # Cryptographic operations            → MBC: Cryptography
│   │                      #   Cryptographic operations and key material.
│   │                      #   API hashing → objectives/anti-static/obfuscation/imports/.
│   │                      #   DPAPI credential decryption → objectives/credential-access/.
│   │                      #   PRNG → os/random/.
│   ├── symmetric/         #   Symmetric ciphers (AES, DES, XOR, RC4)   C0068
│   ├── asymmetric/        #   Asymmetric ciphers (RSA, ECC, Curve25519)
│   ├── cipher/            #   Generic cipher construction/API clues with no supported family
│   ├── hybrid/            #   Symmetric payload cryptography with asymmetric key wrapping
│   ├── hash/              #   Cryptographic hashes (SHA, MD5, Blake2b)  C0029
│   ├── kdf/               #   Key derivation functions                  C0028
│   ├── mnemonic/          #   Seed-phrase representations, wordlists and validation
│   ├── certificate/       #   Certificate ops (install, store, sign, verify)
│   ├── native/            #   Native crypto provider/API references without a narrower operation
│   └── library/           #   Legacy implementation partition; migrate by technique/group
│                          #   Embedded code → supported crypto capability; independent
│                          #   library artifact identity → well-known/lib/crypto/.
│                          #   Blockchain RPC/transaction operations are not crypto primitives.
│
├── metaprogramming/       # Code-as-code techniques; language and filetype neutral
│   ├── ast/               #   Program code inspects, traverses, builds, or transforms ASTs
│   ├── generation/        #   Generate or rewrite code/bytecode
│   └── reflection/        #   Program code discovers types/members or invokes them reflectively
│                          #   Source-vs-compiled and language belong in rule scope/files.
│                          #   Parsing source into a program AST belongs in ast;
│                          #   generating or formatting output code belongs in
│                          #   generation. Library references assert presence only.

├── data/                  # Data transformation                 → MBC: Data
│   │                      #   Neutral data operations only.
│   │                      #   Shellcode/exploit payloads → objectives/evasion/ or execution/.
│   │                      #   Token extraction → objectives/credential-access/.
│   │                      #   Obfuscator detection → objectives/anti-static/.
│   │                      #   CVE-specific patterns → objectives/execution/exploit/.
│   │                      #   Malware family markers → well-known/.
│   ├── arithmetic/        #   Numeric and bitwise operations, independent of representation
│   ├── encode/            #   Encoding (base64, hex, URL, XOR, rot13, custom)  C0026
│   ├── decode/            #   Decoding (base64, hex, buffer)                   C0053
│   ├── compress/          #   Compression (zip, gzip, zlib)                    C0024
│   │   ├── aplib/         #   aPLib compression
│   │   ├── brotli/         #   Brotli compression
│   │   ├── bzip2/          #   BZip2 compression
│   │   ├── gzip/           #   Gzip compression
│   │   ├── lz4/            #   LZ4 compression
│   │   ├── lzma/           #   LZMA/XZ compression
│   │   ├── combined/       #   Legacy mixed claims; classify required operation/algorithm
│   │   ├── stream/         #   Algorithm-neutral compression streams
│   │   ├── zip/            #   ZIP compression
│   │   ├── zlib/            #   zlib/deflate compression
│   │   └── zstd/            #   Zstandard compression
│   ├── decompress/        #   Decompression of encoded/compressed data
│   │   └── combined/       #   Legacy mixed claims; preserve distinct algorithm facts
│   ├── archive/           #   Archive operations (tar, zip extraction)
│   ├── serialize/         #   Serialization (JSON, YAML, pickle, protobuf)
│   ├── transaction/       #   Financial/ledger transaction data operations
│   │   ├── authorize/     #     Spender/transfer authority and permits
│   │   ├── construct/     #     Messages, outputs and fee preparation
│   │   ├── sign/          #     Transaction/payment-specific signing
│   │   ├── submit/        #     Broadcast transactions or financial orders
│   │   └── query/         #     Interpret retrieved transaction fields/results
│   ├── format/            #   Format handling not covered by a narrower operation
│   │                      #     File-level identification or header presence → metadata/file/format/
│   ├── embedded/          #   Embedded content/resource handling (certificates, EXIF, runtime)
│   ├── language/          #   Legacy: language presence → metadata/lang/natural/
│   ├── source/            #   CLOSED historical mixed namespace; classify by semantic subject
│   ├── string/            #   String length, search, comparison, conversion    C0019
│   ├── buffer/            #   Buffer operations (offset writes, reassembly)
│   ├── collection/        #   Operations over collections (arrays, mappings)
│   ├── property/          #   Object properties: access, assign, define, enumerate
│   │                      #     Computed invocation → control-flow/dispatch;
│   │                      #     property labels without operations → metadata
│   ├── db/                #   Database operations (SQL, Redis, MongoDB, etc.)
│   └── control-flow/      #   Control flow patterns (loops, error handling)
│   # NOTE: PRNG → os/random/. Config detection → metadata/config/.
│   # data/ is for data transformation and data-structure handling, not
│   # system queries, file metadata, data merely being present, or generic
│   # text/content buckets. Do not add data/text/; terms belong where the
│   # concept they represent belongs.
│   #
│   # NOTE — decoding/deserialization is a CAPABILITY, not file metadata.
│   #   Decoding an encoding (base64, hex, custom alphabet) or parsing a
│   #   particular format (pickle/marshal, an image/archive/document format)
│   #   is on the TAXONOMY notable bar — an analyst wants it surfaced in a
│   #   supply-chain diff. It belongs here (data/encode/, data/decode/,
│   #   data/serialize/, data/compress/, data/archive/, data/format/),
│   #   NOT in metadata/. An import alone does not establish the operation:
│   #   `import base64` supports both encoding and decoding and belongs with
│   #   import metadata, not arbitrarily under one direction. An embedded
│   #   alphabet is charset metadata. Keep these useful observations, but
│   #   require direction-specific evidence before reporting a transformation.
│   #   The engine also emits a neutral per-module import node under
│   #   metadata/import/<lang>/<module> for composites that need an
│   #   import fact without inferring the decode capability.
│
├── dylib/                 # Native shared-library loader operations
│   ├── enumerate/         #   Enumerate loaded native libraries
│   ├── load/              #   Load/map through the native library loader
│   ├── lookup/            #   Resolve an exported symbol through that loader
│   └── library/           #   Legacy mixed references/identities; migrate by actual claim
│                          #   Embedded APIs → their techniques; dependency facts → metadata.
│                          #   Language module loading → os/module/; see boundary table.
│
├── fs/                    # Filesystem access                   → MBC: File System
│   │                      #   Neutral file operations only.
│   │                      #   File infection → objectives/impact/infect/.
│   │                      #   Disk wiping → objectives/impact/wipe/.
│   │                      #   Hidden file creation → objectives/evasion/file-hiding/.
│   │                      #   Obfuscated paths → objectives/anti-static/obfuscation/.
│   ├── acl/               #   Access Control List manipulation (setfacl, getfacl, NTFS ACLs)
│   ├── attributes/        #   File attributes (chattr, xattr)
│   ├── chmod/             #   Permission mode modification and queries (chmod, umask)
│   ├── chown/             #   Ownership modification (chown, lchown, fchown, takeown)
│   ├── config/            #   Configuration file operations
│   ├── delete/            #   File deletion
│   ├── device/            #   Block/character device access
│   ├── directory/         #   Directory create/chdir/list/traverse; deletion → delete/directory
│   ├── disk/              #   Disk/partition operations
│   ├── enumerate/         #   Drive/device inventory; directory listing → directory/readdir
│   ├── file/              #   File create/open/copy/move/rename/stat; read/write/delete use dedicated homes
│   ├── link/              #   Hard/symbolic links
│   ├── lock/              #   File locking (flock)
│   ├── memory/            #   Memory-mapped I/O (mmap)
│   ├── path/              #   Path references and construction
│   │   ├── config/        #     Config paths (accounts, groups, sudoers)
│   │   ├── device/        #     Device paths (storage, terminal)
│   │   ├── private-key/   #     Private key material (SSH, TLS, keystores, DPAPI)
│   │   ├── public-key/    #     authorized_keys / known_hosts (access grant, not a secret)
│   │   ├── password-store/#     Password databases (browser logins, keychain, vaults)
│   │   ├── token/         #     OAuth / API / session token files
│   │   ├── secret-config/ #     Config that carries secrets (.env, .npmrc, kube/docker)
│   │   ├── wallet/        #     Cryptocurrency wallets and seed phrases
│   │   ├── cookie/        #     Cookie jars
│   │   ├── account-db/    #     System account databases (/etc/passwd, shadow, SAM)
│   │   ├── credential-filename/ # Filename itself marks it secret (auth.json, secrets.*)
│   │   ├── credential/    #     Cross-family umbrellas ("any credential path") + guards
│   │   ├── app-data/      #     Application data/profile dirs (bulk content, not a secret)
│   │   ├── personal/      #     Messages, notes, contacts, history -- not credentials
│   │   └── temp/          #     Temporary paths
│   ├── path-ops/          #   Pathname manipulation, distinct from path resources
│   │   ├── join/          #     Combines path components into a pathname
│   │   ├── normalize/     #     Canonicalizes separators, dot segments, or case
│   │   ├── parse/          #     Extracts parent, basename, extension, or components
│   │   └── match/          #     Tests a pathname against a pattern/predicate
│   ├── pipe/              #   Named pipes (FIFO)
│   ├── proc/              #   /proc filesystem access
│   ├── quota/             #   Filesystem quota operations
│   ├── read/              #   File reading (standalone)
│   ├── search/            #   File search/query tools (locate, mdfind, Spotlight)
│   ├── shell-ops/         #   Legacy spelling split; cp/mv/rm belong with their operations
│   ├── swap/              #   Swap operations
│   ├── sync/              #   Filesystem sync (fsync, fdatasync)
│   ├── temp/              #   Temporary file/directory creation
│   ├── traversal/         #   Legacy overlap; recursive descent → directory/traverse
│   ├── volume/            #   Volume mount/unmount
│   ├── watch/             #   File monitoring (inotify, fanotify, fswatch)
│   └── write/             #   File writing (standalone)
│
├── hardware/              # Hardware device I/O                 → MBC: Hardware
│   │                      #   Direct interaction with hardware devices.
│   │                      #   Querying system properties → os/sysinfo/.
│   │                      #   Neutral enumeration → os/sysinfo/; reconnaissance chains → discovery/.
│   │                      #   Clipboard (OS IPC) → os/clipboard/.
│   ├── block/             #   Block storage device access
│   ├── display/           #   Screen/graphics (capture APIs, DirectX)
│   ├── flash/             #   Flash memory devices (MTD, MMC)
│   ├── input/             #   Keyboard, mouse (capture, simulation)
│   ├── iokit/             #   macOS IOKit device framework
│   ├── smartcard/         #   Smart card reader access (WinSCard)
│   └── wireless/          #   Wireless network interfaces
│
├── mem/                   # Memory operations                   → MBC: Memory
│   ├── advise/            #   Memory advisory (madvise, posix_madvise)
│   ├── alloc/             #   Memory allocation (malloc, VirtualAlloc, PAGE_EXECUTE_*)
│   ├── anonymous/         #   Anonymous memory (memfd_create, /dev/shm)
│   ├── c-runtime/         #   C runtime memory functions (memcpy, memset)
│   ├── create/            #   Memory-backed file creation
│   ├── decompress/        #   Legacy: decompression remains data/decompress/ in memory too
│   ├── gc/                #   Garbage collection
│   ├── inline-asm/        #   Inline assembly detection
│   ├── lock/              #   Memory locking (VirtualLock, mlock)
│   ├── protect/           #   Memory protection changes (mprotect, VirtualProtect)
│   ├── query/             #   Memory queries (VirtualQuery)
│   ├── read/              #   Memory read (including cross-process ReadProcessMemory)
│   └── sync/              #   Memory visibility/cache synchronization; locks → process/sync
│   # NOTE: RWX allocation alone is a neutral memory observation. Payload
│   # execution, injection, unhooking and exploitation require their own
│   # objective evidence; a memory API does not establish those outcomes.
│
├── network/               # Network-resource capabilities
│   └── interface/         # Interface identity, address, and state; clues may
│                          # indicate probable interaction without proving an
│                          # enumeration or configuration operation
│
├── os/                    # OS integration                      → MBC: Operating System
│   │                      #   OS-specific APIs that don't fit other top-level categories.
│   │                      #   Process ops → process/. File ops → fs/. Timing → time/.
│   │                      #   Persistence composites (crontab, registry Run keys) →
│   │                      #   objectives/persistence/.
│   ├── api-resolution/    #   API resolution (GetProcAddress, hash-based)
│   ├── application/       #   Application identities used by OS facilities
│   │   └── target/        #     App/package IDs cited as the intended target
│   │                      #     (reference evidence; not installed-app discovery)
│   ├── autorun/           #   Autorun keyword/scheduled task patterns
│   ├── bpf/               #   BPF/eBPF operations
│   ├── callback/          #   OS callback mechanisms
│   ├── clipboard/         #   Clipboard (OS IPC), split by what the code
│   │   │                  #   does to it -- reading someone's clipboard and
│   │   │                  #   replacing it are different threats, and the
│   │   │                  #   feature stops at this level.
│   │   ├── read/          #     Pulls clipboard contents out          T1115
│   │   ├── write/         #     Puts contents in, clears, or replaces
│   │   │                  #     them (the clipper/hijack shape)
│   │   ├── monitor/       #     Watches for changes over time
│   │   └── reference/     #     Names the clipboard API without
│   │                      #     performing an operation
│   ├── com/               #   Windows COM/OLE
│   ├── compat/            #   OS compatibility layers
│   ├── console/           #   Console I/O (C0033)
│   ├── container/         #   Container runtime detection
│   ├── env/               #   Environment variables (C0034). Which variable
│   │   │                  #   is named is the discriminator, so the topic sits
│   │   │                  #   at this level -- it used to live under a `vars/`
│   │   │                  #   grouping word, where all 14 topics collapsed into
│   │   │                  #   the single feature `os/env/vars`.
│   │   ├── secret-name/   #     Secret-bearing variable references      T1552.001
│   │   ├── ai-provider/   #     AI SDK configuration variables
│   │   ├── package-manager/ #   npm/node ecosystem variables
│   │   ├── runtime/       #     Language/runtime tuning knobs (NODE_OPTIONS,
│   │   │                  #     OMP_NUM_THREADS, MallocStackLogging)
│   │   ├── ci-credentials/ #    CI-issued secrets
│   │   ├── cicd/          #     CI/CD runner variables
│   │   ├── cloud/         #     Cloud-provider variables
│   │   ├── system-info/   #     Host/system description variables
│   │   ├── user-info/     #     User identity variables
│   │   ├── user-paths/    #     Per-user path variables
│   │   ├── platform/      #     Platform/arch variables
│   │   ├── ssh/           #     SSH agent/auth variables
│   │   ├── editor/        #     EDITOR/VISUAL and friends
│   │   ├── pipeline/      #     Pipeline plumbing variables
│   │   ├── modify/        #     Setting, clearing or injecting a variable
│   │   │
│   │   │                  #   Use these operations only when no specific variable
│   │   │                  #   subject is required; the boundary table orders the facets:
│   │   ├── read/          #     Querying a variable (os.Getenv, System.getenv,
│   │   │                  #     process.env, getenv)
│   │   ├── enumeration/   #     Walking the whole environment
│   │   ├── block/         #     Windows environment-block APIs that allocate
│   │   │                  #     and release the block itself
│   │   ├── dump/          #     Dumping the environment wholesale
│   │   ├── config/        #     Env-driven configuration
│   │   └── check/         #     Guarding on a variable's value
│   ├── event/             #   OS event mechanisms
│   ├── exception/         #   Exception/error handling
│   ├── firewall/          #   Firewall tool references (iptables, nft, ufw, firewalld)
│   │                      #     Neutral: "code references a firewall tool" (notable)
│   │                      #     Destructive ops (flush, disable, policy change) →
│   │                      #     objectives/impact/degrade/firewall/
│   ├── group/             #   Group management
│   ├── kernel/            #   Kernel interaction (modules, devices, callbacks)
│   │   └── boot/          #     Boot configuration (bcdedit, Safe Mode, boot flags)
│   │                      #       Neutral: "changes how the machine next boots";
│   │                      #       EDR teardown / ransomware staging composites →
│   │                      #       objectives/impact/degrade/ and objectives/evasion/anti-av/
│   ├── linker/            #   Dynamic linker configuration
│   ├── message/           #   Message queues
│   ├── module/            #   Module loading
│   ├── msdos/             #   MS-DOS interrupt handling (vintage)
│   ├── network/           #   Network config and status
│   │   └── status/        #     Active network state queries (netstat, ss)
│   ├── package-manager/   #   Package management (apt, pip)
│   ├── pam/               #   PAM authentication
│   ├── privilege/         #   Privilege APIs (manifest, paths — neutral only)
│   ├── random/            #   Random number generation
│   ├── registry/          #   Windows registry (C0036)
│   ├── security/          #   OS security APIs (keychain, capabilities, auth)
│   │   ├── auth/          #     Authentication and authorization checks, including
│   │   │                  #       app-level ones (WordPress capability/nonce/session)
│   │   └── jailbreak/     #     Jailbreak/root artifact paths a program looks for.
│   │                      #       Neutral: banking and DRM apps check these too;
│   │                      #       evasion intent → objectives/anti-analysis/
│   │                      #       environment-detect/
│   ├── recovery/          #   OS recovery points (SRSetRestorePoint). Creating
│   │                      #     one is neutral; removing them is
│   │                      #     objectives/impact/degrade/system/recovery/.
│   ├── service/           #   System service management, split by the verb --
│   │   │                  #   the verb is the discriminator and the feature
│   │   │                  #   stops at this level, so each is a sibling rather
│   │   │                  #   than a child of control/.
│   │   ├── create/        #     Registering a new service
│   │   ├── start/         #     Starting or restarting one
│   │   ├── stop/          #     Stopping one
│   │   ├── delete/        #     Removing one
│   │   ├── configure/     #     Changing start type or config
│   │   ├── query/         #     Reading status or config
│   │   ├── dispatch/      #     A program acting AS a service (control
│   │   │                  #     dispatcher, status handler)
│   │   ├── control/       #     Generic service-manager interaction that
│   │   │                  #     names no particular verb (OpenSCManager,
│   │   │                  #     ControlService, bare systemctl/launchctl)
│   │   └── user-session/  #     Legacy scope bucket; operation wins over per-user scope
│   ├── signal/            #   Signal handling
│   ├── stdio/             #   Standard I/O operations
│   ├── syscall/           #   Direct syscall invocation
│   ├── sysinfo/           #   System information queries
│   │   ├── platform/      #     OS/arch detection (uname, sys.platform, GOOS)
│   │   ├── hostname/      #     Machine name (gethostname, hostname cmd)
│   │   ├── hardware/      #     Hardware info (DMI, SMBIOS, memory)
│   │   ├── disk/           #     Disk capacity and volume information
│   │   ├── directories/   #     System directory paths
│   │   ├── process/       #     Current process info (GetStartupInfo)
│   │   ├── config/        #     System config (sysconf, sysctl)
│   │   └── vmware/        #     VMware/ESXi paths, commands
│   ├── telemetry/         #   OS telemetry and instrumentation
│   ├── user/              #   User account management
│   ├── virtualization/    #   Hypervisors, virtual devices, VM snapshots
│   ├── wmi/               #   Windows WMI queries
│   └── wsh/               #   Windows Script Host
│
├── process/               # Process control                     → MBC: Process
│   │                      #   Privilege APIs → os/privilege/. Env vars → os/env/.
│   │                      #   Container runtime → os/container/.
│   ├── argument/          #   Command-line argument parsing
│   ├── attach/            #   Process attachment (ptrace, debug)
│   ├── control/           #   Process control signals
│   ├── create/            #   Process creation (spawn, exec)
│   ├── daemonize/         #   Daemon creation (setsid, double-fork)
│   ├── debug/             #   Debug operations
│   ├── enumerate/         #   Process listing
│   ├── exit/              #   Process self-exit
│   ├── fd/                #   File descriptor manipulation (dup2)
│   ├── fork/              #   Legacy duplicate of create/fork
│   ├── hook/              #   API/function hooking
│   ├── identity/          #   Process identity (getpid, getppid)
│   ├── info/              #   Process information queries
│   ├── inject/            #   Cross-process injection (DLL, thread, APC, atom-bombing)
│   ├── interpreter/       #   Code interpreters/runtimes
│   │   ├── eval/          #     Source evaluated inside the running interpreter.
│   │   │   │              #       No new process: that is process/create/eval.
│   │   │   │              #       Shell `eval`/`source "$x"` belongs here too; it
│   │   │   │              #       starts no new shell (`sh "$x"` does: create/shell).
│   │   │   │              #       Eval of fetched/received code is the objective
│   │   │   │              #       objectives/execution/interpreter/eval/remote/.
│   │   │   │              #       Children are below the ML-visible level and
│   │   │   │              #       split by mechanism; language goes in the filename.
│   │   │   ├── direct/    #       The eval builtin named at the call site
│   │   │   │              #         (eval, iex, Execute, instance_eval, loadstring)
│   │   │   ├── indirect/  #       Eval reached without naming it there
│   │   │   │              #         ((0,eval)(), window.eval, Set-Alias iex)
│   │   │   └── compile/   #       Source compiled into a callable, then invoked
│   │   │                  #         (Function, create_function, ScriptBlock::Create)
│   │   ├── vm/            #     Node.js VM module (createContext, runInContext)
│   │   ├── node/          #     Node.js internal bindings (process.binding)
│   │   └── gentee/        #     Gentee scripting runtime
│   ├── io/                #   Process I/O redirection
│   ├── lifecycle/         #   Process lifecycle management
│   ├── pid/               #   PID file operations
│   ├── resources/         #   Process resource management
│   ├── script/            #   Legacy carrier bucket; classify actual execution mechanism
│   ├── sync/              #   Process synchronization
│   ├── terminate/         #   Process termination (killing other processes)
│   ├── thread/            #   Thread lifecycle (Java)
│   ├── threading/         #   Legacy overlap; create/thread, thread lifecycle, or sync
│   ├── tls/               #   Thread-local storage
│   ├── tty/               #   TTY/PTY operations (terminal detection, pseudoterminals)
│   └── user/              #   Process user identity (whoami, getlogin, getpwuid)
│
├── ui/                    # User interface operations
│   ├── controls/          #   Widget/control operations, including progress display settings
│   ├── dialog/            #   Dialog boxes, message boxes, prompts
│   ├── framework/         #   Legacy backend split; widget/render operations use their subjects
│   ├── graphics/          #   GDI/drawing operations
│   ├── help/              #   Help/usage surfaces and documented CLI behavior
│   ├── menu/              #   Menu operations (popup, context)
│   ├── terminal/          #   Terminal/console UI (ANSI, ncurses)
│   ├── wallpaper/         #   Desktop wallpaper manipulation
│   └── window/            #   Window management (create, show, position)
│   # NOTE: Stealth UI behaviors (hiding Dock icon, hiding windows,
│   # excessive VScrollBar deception) belong in objectives/evasion/,
│   # not here. Micro-behaviors/ui is for NEUTRAL UI operations only.
│
└── time/                  # Timing operations
    ├── sleep/             #   Delays
    ├── schedule/          #   Scheduled execution
    └── timing/            #   Timers and timing measurements
```

## Tier 2: Objectives (`objectives/`)

Attacker goals inferred from capability combinations. Maps to MBC [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions). Implies *likely* intent — static analysis alone can't be 100% certain.

```
objectives/
├── anti-analysis/             # Evade behavioral analysis (OB0001)
│   │                          #   Sandboxes, debuggers, emulators, VMs
│   │                          #   "Don't analyze me" — targets analysts & analysis tools
│   ├── debugger-detect/       #   Debugger detection                      B0001
│   ├── sandbox-detect/        #   Sandbox detection                       B0007
│   ├── vm-detect/             #   Virtual machine detection               B0009
│   ├── emulator-detect/       #   Emulator detection                      B0004
│   ├── environment-detect/    #   Analysis environment detection          B0013
│   ├── timing/                #   Timing-based evasion / delays           B0025
│   ├── tool-detect/           #   Detect analyst tools (IDA, procmon)
│   ├── geofencing/            #   Geographic/locale conditional exec      B0025
│   ├── anti-tampering/        #   Detect analyst code patches
│   ├── self-modify/           #   Self-modification reacting to live analysis B0008
│   │                          #     Static concealment → anti-static; neutral writes → capabilities.
│   ├── self-terminate/        #   Crash/exit when analysis detected
│   ├── process-tree/          #   Break process lineage for sandbox evasion
│   ├── fingerprinting/        #   CPU/instruction environment detection
│   ├── browser-detect/        #   Browser sandbox detection
│
├── anti-static/               # Evade static analysis (OB0002)
│   │                          #   Disassembly, decompilation, string extraction
│   ├── obfuscation/           #   Obfuscated files/code          E1027 + B0032
│   │   │                      #   Organized by technique, not by language or file type.
│   │   │                      #   A string encryption rule works the same whether
│   │   │                      #   the target is a Python script or a PE binary.
│   │   ├── string/            #     String obfuscation (encrypt, split, concat)
│   │   ├── encoding/          #     Data encoding (base64, hex, xor, arithmetic)
│   │   ├── eval/              #     Dynamic execution (eval, exec, Function, WSH)
│   │   ├── control-flow/      #     Control-flow (flattening, VM dispatch, polymorphism)
│   │   ├── syntax/            #     Source syntax patterns (AST/raw; anti-tamper,
│   │   │                      #       dynamic property access, IIFE wrappers).
│   │   │                      #       vs string/: string/ detects string-value techniques;
│   │   │                      #       syntax/ detects source-level structural patterns.
│   │   │                      #       vs control-flow/: control-flow/ is about execution
│   │   │                      #       path manipulation; syntax/ is about language-specific
│   │   │                      #       constructs used to hide intent.
│   │   ├── instruction/       #     Instruction-level (junk/dead code)     B0032
│   │   ├── name-mangling/     #     Name mangling (var rename, exports, identifiers)
│   │   ├── imports/           #     Import concealment, API hashing
│   │   ├── reflection/        #     Dynamic dispatch (prototype, proxy, dlsym)
│   │   ├── payload/           #     Embedded/encrypted payloads
│   │   ├── document/          #     Document-specific (RTF, Office, LNK)
│   │   ├── steganography/     #     Data hiding (images, unicode)
│   │   ├── binary-metrics/    #     Legacy: neutral anatomy measurements → metadata/binary
│   │   ├── code-metrics/      #     Legacy: code measurements → metadata; concealment needs evidence
│   │   ├── tools/             #     Legacy: tool identity → well-known; output → its transform
│   │   ├── multi-layer/       #     Legacy: define required concealment, not a catch-all conjunction
│   │   └── anti-decompile/    #     Anti-disassembly tricks                B0012
│   ├── pack/                  #   Software packing                        F0001
│   └── polyglot/              #   Polyglot file format abuse
│
├── evasion/                   # Evade detection in production (OB0006)
│   │                          #   Users, admins, AV/EDR, forensics
│   │                          #   "Don't see me" — targets defenders & security tools
│   │                          #   Bypass/stealth only — aggressive termination of
│   │                          #   security products belongs in impact/degrade/edr/.
│   ├── anti-av/               #   AV/EDR bypass (stealth, not termination)
│   │   ├── amsi/              #     AMSI bypass
│   │   ├── blinding/          #     Kernel security module neutralization
│   │   ├── code-padding/      #     Benign code-mass padding (ML/heuristic dilution)
│   │   ├── edr-detect/        #     Legacy: reconnaissance → discovery/host/security
│   │   ├── gui-decoy/         #     Decoy GUI message-pump (no real GUI resources)
│   │   ├── import-pollution/  #     Import table pollution
│   │   ├── manifest-padding/  #     Fake AV dummy text in PE manifest
│   │   ├── platform/          #     Platform-specific bypass (exclusions, disables)
│   │   ├── syscall/           #     Direct/indirect syscalls (EDR bypass)
│   │   ├── tbav/              #     TBAV anti-heuristic ASM signature
│   │   └── tls-fingerprint/   #     TLS fingerprint manipulation
│   ├── decoy/                 #   Deceptive content (documents, fake errors, lures)
│   ├── file-hiding/           #   Hidden files/directories                E1564, F0005
│   ├── file-unlock/           #   Force-close file locks                  T1562
│   ├── fileless/              #   Avoid disk artifacts (memory-only staging)
│   ├── hijack-execution-flow/ #   Execution flow hijacking                F0015
│   ├── hosts-file/            #   Hosts file manipulation                 F0004
│   ├── indicator-removal/     #   Remove evidence of activity             T1070
│   │   ├── cleanup/           #     Artifact cleanup (scripts, marker files)
│   │   ├── history/           #     Shell history clearing                T1070.003
│   │   ├── logs/              #     Log clearing + audit sanitization     T1070.001
│   │   └── timestamps/        #     Timestomping                          T1070.006
│   ├── kernel-hide/           #   Kernel-level hiding (rootkit)           E1014
│   ├── masquerade/            #   File/process masquerading               T1036
│   ├── process/               #   Process-level evasion
│   │   ├── callstack-spoof/   #     Callstack spoofing
│   │   ├── hidden/            #     Hidden process/window execution       E1564
│   │   ├── hook/              #     API/XHR hooking
│   │   └── injection/         #     Process injection                     E1055
│   ├── quarantine-removal/    #   macOS Gatekeeper bypass                 B0047
│   ├── security-bypass/       #   Security restriction bypass (PHP, LLM policy boundaries)
│   │   └── llm/               #     Prompt-injection composites that bypass
│   │                          #     AI agent instruction hierarchy, tool-use
│   │                          #     controls, or safety policies. Neutral or
│   │                          #     standalone prompt text atoms stay in
│   │                          #     micro-behaviors/data/llm/.
│   ├── self-delete/           #   Self-deletion after execution           F0007
│   └── tcc-manipulation/      #   macOS TCC database manipulation
│
├── command-and-control/       # C2 communication (OB0004)
│   │                          #   "Communicate with compromised systems to control them"
│   │                          #   MBC: B0030 C2 Communication, B0031 DGA, E1105 Ingress Tool Transfer.
│   │                          #   NOT C2: DDoS → impact/dos/. Exfil → exfiltration/.
│   │                          #   Credential phishing → credential-access/. Competing malware → impact/.
│   ├── backdoor/              #   Unauthorized remote access surfaces        B0030
│   │   ├── bind-shell/        #     Listener accepts a connection into a shell
│   │   ├── auth-bypass/       #     Unauthorized bypass of the access check
│   │   ├── binary/            #     Legacy carrier split; classify access mechanism
│   │   ├── script/            #     Legacy carrier split; classify access mechanism
│   │   ├── daemon/            #     Legacy lifecycle context; durability is a separate claim
│   │   ├── stealth/           #     Legacy facet; reference the concealment behavior
│   │   ├── reflective-load/   #     Legacy loader mechanism; not access by itself
│   │   └── webshell/          #     Web-based backdoors (PHP, JSP, ASPX)
│   ├── beacon/                #   Periodic check-in / heartbeat              B0030
│   ├── botnet/                #   Bot network coordination                   B0030
│   ├── channel/               #   Communication channels (all protocols)     B0030
│   │   ├── covert/            #     Covert channels (ICMP, stego)
│   │   ├── http/              #     HTTP/HTTPS C2 protocol
│   │   ├── irc/               #     IRC-based C2
│   │   ├── messaging/         #     Discord, Slack, Telegram
│   │   ├── tor/               #     Tor hidden services
│   │   ├── tunnel/            #     Tunneling, proxy, SOCKS
│   │   └── websocket/         #     WebSocket C2
│   ├── dns/                   #   DNS-based C2 + DGA + tunneling             B0031
│   ├── dropper/               #   Payload staging linked to activation       E1105 + B0023
│   │   │                      #   Canonical activation homes; legacy migration in progress.
│   │   │                      #   Existing delivery/staging/execution/behavior branches
│   │   │                      #   are reconciled by activation sink, not retained as aliases.
│   │   ├── process-inject/    #     Execute staged payload in another process
│   │   ├── image-map/         #     Map native staged image in the current process
│   │   ├── module-load/       #     Runtime module/assembly activation
│   │   ├── script-eval/       #     Evaluate source in the current interpreter
│   │   ├── interpreter-stdin/ #     Source streamed to a new interpreter
│   │   └── file-exec/         #     Launch a staged file
│   │       └── spawn/         #       Write/copy it, then launch a child process
│   ├── infrastructure/        #   C2 infrastructure (domains, IPs, cloud)    B0030
│   │   ├── domain/            #     Domains, DGA, hosting
│   │   └── config/            #     C2 config patterns
│   ├── remote-command/        #   Command dispatch                           B0011
│   ├── reverse-shell/         #   Outbound connection coupled to shell I/O   B0030
│   │   ├── dev-tcp/           #     Shell pseudo-device connection/redirection
│   │   ├── netcat/            #     Netcat invocation owns the shell relay
│   │   ├── pty/               #     Pseudoterminal carries connected shell session
│   │   ├── fd-redirect/       #     Socket installed as inherited shell descriptors
│   │   └── stream-bridge/     #     Explicit socket/child-stream bridge
│   └── trigger/               #   Attacker activation gates, not ordinary lifecycle facts
│
├── collection/                # Information gathering (OB0003)
│   │                          #   "Identify and gather information, such as sensitive files"
│   │                          #   Generic capture mechanisms live here.
│   │                          #   Credential-specific stores → credential-access/.
│   │                          #   Financial data → credential-access/financial/.
│   ├── keylog/                #   Keystroke logging                       T1056.001
│   ├── clipboard/             #   Clipboard capture                       T1115
│   ├── audio/                 #   Local sound acquisition                 T1123
│   ├── camera/                #   Local camera acquisition                T1125
│   ├── multi-source/          #   Independently required acquired datasets; no export
│   ├── screenshot/            #   Screen capture                          T1113
│   ├── touch/                 #   Touch position/gesture collection
│   ├── archive/               #   Archive collected data                  T1560
│   ├── database/              #   Database enumeration/access             T1005
│   ├── email-harvest/         #   Mailbox/address collection              T1114
│   ├── file-copy/             #   File copying mechanisms                 T1005
│   ├── file-targeting/        #   File enumeration for targeting          T1083
│   ├── network/               #   Network packet/traffic capture          T1040
│   ├── messaging/             #   Messaging app data collection           T1005
│   ├── app-data/              #   Application-specific data (Notes, Stickies)
│   ├── monitor/               #   Monitoring/telemetry capture
│   ├── activity/              #   User activity tracking
│
├── credential-access/         # Credential theft (OB0005)
│   │                          #   "Obtain credential access" — targeting specific stores.
│   │                          #   Generic capture (keystrokes, clipboard) → collection/.
│   │                          #   Neutral env access (os.environ) → micro-behaviors/.
│   │                          #   Credential access + transport → exfiltration/stealer/.
│   │                          #   Account/user vocabulary alone → its account subject,
│   │                          #   not credential theft; API/path atoms → micro-behaviors/.
│   ├── api-harvest/           #   API key/token harvesting                T1528
│   ├── browser/               #   Browser credential stores              T1555.003
│   ├── capture/input/         #   Password prompt capture                 T1056
│   ├── clipboard/             #   Clipboard credential targeting
│   ├── cloud/token/           #   Cloud service tokens
│   ├── cracking/              #   Password cracking                       T1110
│   ├── credential-manager/    #   Windows Credential Manager              T1555.004
│   ├── dev-tools/             #   Developer tool credentials (JFrog)
│   ├── discord/token/         #   Discord token theft                     T1528
│   ├── dump/system/           #   OS credential dumping                   T1003
│   ├── email/                 #   Email client credentials
│   ├── env/                   #   Environment secrets                     T1552.001
│   │   ├── dotenv/            #     .env file access
│   │   ├── harvesting/        #     Env var harvesting
│   │   ├── secrets/           #     Secret access patterns (AWS_SECRET, etc.)
│   │   └── token/             #     Hardcoded tokens in env
│   ├── files/config/          #   Config file credentials                 T1552.001
│   ├── financial/             #   Financial data (credit cards)            T1005
│   ├── ftp/                   #   FTP client credentials
│   ├── gaming/                #   Gaming platform credentials (Steam)
│   ├── keychain/              #   macOS Keychain                          T1555.001
│   ├── messaging/             #   Messaging app credentials (Telegram)
│   ├── pam/intercept/         #   PAM interception                        T1556.003
│   ├── phishing/              #   Credential phishing                     T1566
│   ├── shell/history/         #   Shell history                           T1552.003
│   ├── ssh/key/               #   SSH key theft                           T1552.004
│   ├── theft/                 #   Credential theft composites
│   │   ├── multi-app/         #     Sweep across app SESSIONS (wallets, Discord, Steam)
│   │   └── multi-store/       #     Sweep across developer credential STORES (cloud
│   │                          #       configs, SSH keys, .env/.npmrc, browser DBs); the
│   │                          #       dev-workstation analogue of multi-app. A sweep
│   │                          #       that also SENDS → exfiltration/stealer/ by source.
│   ├── validation/            #   Credential validation
│   ├── vpn/config/            #   VPN config credentials
│   ├── wallet/                #   Crypto wallet access                    B0028
│   └── windows-registry/      #   Registry credential extraction
│
├── discovery/                 # Environment reconnaissance (OB0007)
│   │                          #   "Gain knowledge about the system and network"
│   │                          #   Rules must infer reconnaissance INTENT, not just
│   │                          #   observe a single system call. Single os.platform() →
│   │                          #   micro-behaviors/. Profiling multiple properties → here.
│   │                          #   Notebook-specific host/browser fingerprinting →
│   │                          #   fingerprint/notebook; generic host fields → fingerprint/info.
│   ├── system/                #   System information                      E1082
│   │   ├── fingerprint/       #     System/hardware/OS profiling
│   │   │   └── notebook/      #       Notebook-specific host/browser fingerprinting
│   │   ├── architecture/      #     CPU architecture discovery
│   │   ├── locale/            #     Language/region discovery
│   │   ├── hardware/          #     Hardware enumeration
│   │   └── device/            #     Device discovery
│   ├── network/               #   Network information                     T1016
│   │   ├── connections/       #     Active connections                     T1049
│   │   ├── enumeration/       #     Host enumeration                      T1018
│   │   ├── interface/         #     Interface listing
│   │   ├── scan/              #     Port/service scanning                 T1046
│   │   └── iot-devices/       #     IoT device discovery
│   ├── host/                  #   Host-specific discovery
│   │   ├── application/       #     Application discovery                 E1010
│   │   ├── browser/           #     Browser data locations
│   │   ├── geo/               #     Geolocation
│   │   ├── permissions/       #     Permission enumeration
│   │   ├── security/          #     Security software discovery           T1518.001
│   │   └── software/          #     Installed software                    T1518
│   ├── process/               #   Running-process discovery               T1057
│   │   ├── enumerate/         #     Inventory of running processes
│   │   └── window/            #     Window discovery                      E1010
│   ├── account/               #   Account/user discovery                  T1087, T1033
│   │   └── lookup/
│   └── cloud/                 #   Cloud instance metadata                 T1552.005
│       └── metadata/
│
├── execution/                 # Code execution (OB0009)
│   │                          #   "Execute code on a system to achieve a variety of goals"
│   │                          #   Neutral capabilities (openpty, GetModuleHandle, fork+setsid,
│   │                          #   Math.random) → micro-behaviors/. Evasive execution (reflective
│   │                          #   loading, fileless, shellcode) → evasion/. Privesc (sudo, GTFOBins)
│   │                          #   → privilege-escalation/. Remote commands → command-and-control/.
│   │                          #   Staged-payload activation → command-and-control/dropper/.
│   │                          #   Hook declarations → metadata/package/scripts/lifecycle/;
│   │                          #   composites using them live with their required result.
│   ├── activex/               #   COM/ActiveX execution                   E1569
│   ├── autoinstall/           #   Automatic dependency installation
│   ├── automation/            #   Compiled automation (AppleScript)        E1059
│   ├── compile/               #   Compile after delivery
│   ├── condition/             #   Conditional execution / guardrails       B0025
│   ├── exploit/               #   Exploitation for client execution        E1203
│   ├── interpreter/           #   Script/code interpreters                 E1059
│   ├── lnk/                   #   LNK-based execution                     E1204
│   ├── lolbin/                #   Living-off-the-land binaries             T1218
│   │   └── regsvr32/          #     Regsvr32 scriptlet execution / Squiblydoo
│   ├── lure/                  #   User execution via social engineering    E1204
│   ├── trigger/               #   Document exploitation triggers           E1203
│   └── wmi/                   #   WMI execution                            E1569
│
├── exfiltration/              # Data theft (OB0010)
│   │                          #   "Steal data from a system" — complete chains use SOURCE.
│   │                          #   Reading credential stores → credential-access/.
│   │                          #   Gathering/archiving data → collection/.
│   │                          #   Sending data to attacker → exfiltration/.
│   │                          #   Transport mechanism alone (HTTP POST) = micro-behavior.
│   │                          #   Transport + sensitive source = exfiltration objective.
│   ├── cloud/                 #   Cloud storage exfil (S3, GCS, Colab)     T1567
│   ├── dns/                   #   DNS-based exfil (subdomain encoding)     T1048
│   ├── ftp/                   #   FTP-based exfil
│   ├── http/                  #   HTTP/HTTPS exfil (POST, upload, paste)   T1041
│   ├── messaging/             #   Messaging platform abuse for exfil
│   │   ├── discord/           #     Discord webhooks
│   │   ├── slack/             #     Slack webhooks
│   │   └── telegram/          #     Telegram bot API
│   ├── oob/                   #   Out-of-band data collection services
│   │   └── shortener/         #     URL shortener abuse
│   ├── sensitive-data/        #   Legacy: no send → collection/credential-access; chain → stealer
│   ├── serialization/         #   Legacy: neutral serialization → data/serialize; chain → stealer
│   ├── side-channel/          #   Covert channels (DNS tunneling, stego)
│   └── stealer/               #   Complete steal-and-send chains           E1020
│       │                      #     The ONLY stealer home. There is no collection/stealer/
│       │                      #     or credential-access/theft/stealer/: gathering without
│       │                      #     sending is collection/, reading a store is
│       │                      #     credential-access/, and "stealer" means the data leaves.
│       │                      #     Named families → well-known/malware/stealer/.
│       │                      #     Contract for every rule under stealer/:
│       │                      #     - a composite with a sensitive-SOURCE leg AND a
│       │                      #       TRANSPORT leg (HTTP/upload, webhook, bot API,
│       │                      #       SMTP, FTP, socket, DNS). No transport → the source's
│       │                      #       credential-access/ or collection/ home; no narrower
│       │                      #       source → exfiltration/<transport>/ only if theft or
│       │                      #       unauthorized transfer is still established.
│       │                      #     - composites only, as far as possible: source atoms
│       │                      #       live in credential-access/, discovery/, collection/;
│       │                      #       neutral atoms in micro-behaviors/. An atom stays
│       │                      #       only when it has no meaning outside the chain.
│       │                      #     Children are named for WHAT is stolen (level 3 is the
│       │                      #     last ML-visible level); transport, language, platform
│       │                      #     and product go in the filename.
│       ├── account-db/        #     /etc/shadow, /etc/passwd, SAM, sudo logs
│       ├── appliance-config/  #     Router/firewall/appliance configs (RouterOS, NetScaler)
│       ├── audio/             #     Sound, including recordings with unspecified origin
│       ├── audiovisual/       #     Audio/video recording without a required narrower source
│       ├── browser/           #     Browser passwords, cookies, extension storage
│       ├── camera/            #     Camera imagery or streams
│       ├── cloud/             #     Cloud credentials (~/.aws, IMDS, kubeconfig)
│       ├── credential/        #     Authentication-store export with no required narrower store
│       ├── dev-secret/        #     .npmrc, .git-credentials, .env files, CI secrets
│       ├── env/               #     Process environment secrets
│       ├── file/              #     Documents, disk sweeps, removable media
│       ├── image/             #     Image data with unspecified acquisition origin
│       ├── input/             #     Keystrokes, form input, clipboard
│       ├── keychain/          #     OS secret stores (Keychain, DPAPI, libsecret)
│       ├── message/           #     SMS, mailboxes, chat history
│       ├── multi-source/      #     Required independent stolen datasets, not indicator counts
│       ├── screen/            #     Display/window/tab images, streams, or derived text
│       ├── ssh/               #     SSH keys and host files
│       ├── surveillance/      #     Legacy purpose axis: audit by input/screen/audio/video source
│       ├── sweep/             #     Legacy unresolved rules; no new admissions
│       ├── system-info/       #     Host/client reports; parent holds no rules
│       │   ├── identity/      #       Host, account, and stable device identifiers
│       │   ├── platform/      #       OS/runtime/execution-environment information
│       │   ├── software/      #       Installed software/package inventory
│       │   ├── process/       #       Running-process inventory
│       │   ├── network/       #       Interfaces, routes, connectivity, and network survey
│       │   └── profile/       #       Reports spanning or leaving open several host domains
│       ├── token/             #     App session tokens (Discord, Telegram, games)
│       └── wallet/            #     Crypto wallets and seed phrases
│
├── impact/                    # Destructive operations (OB0008)
│   │                          #   "Manipulate, interrupt, or destroy systems and data"
│   │                          #   Aggressive actions that damage, disrupt, or hijack resources.
│   │                          #   NOTE: evasion/ = stealth ("don't see me").
│   │                          #   impact/degrade/ = aggression ("I'll stop you").
│   │                          #   Killing AV processes is impact, not evasion. Bypassing AV
│   │                          #   (AMSI, indirect syscalls) is evasion.
│   ├── cryptojacking/         #   Resource hijacking / cryptomining        B0018
│   ├── crypto-manipulation/   #   Cryptocurrency manipulation (clipboard hijack) T1565.001
│   ├── deface/                #   Defacement                              T1491
│   ├── degrade/               #   System capability degradation
│   │   ├── edr/               #     EDR/AV termination (aggressive)       T1562.001
│   │   ├── firewall/          #     Firewall disable/flush                T1562.004
│   │   │                      #       Atoms (tool refs) in micro-behaviors/os/firewall/
│   │   ├── ics/               #     ICS/OT safety parameter manipulation  T0836
│   │   │                      #       Chemical dosing, pressure, valve overrides,
│   │   │                      #       turbine speed, safety interlock disable.
│   │   │                      #       Atoms (protocol refs) in micro-behaviors/communications/.
│   │   ├── rival-bot/         #     Competing malware termination
│   │   └── system/            #     Critical file/recovery deletion
│   ├── destroy/               #   Data destruction                        T1485
│   ├── dos/                   #   Denial of service                       B0033
│   ├── infect/                #   File infection (virus propagation)
│   ├── ransom/                #   Ransomware encryption + extortion       T1486
│   ├── services/stop/         #   Service stopping                        T1489
│   ├── system/                #   System impact (crash, shutdown, reboot)
│   ├── ui/manipulation/       #   User-visible interface manipulation
│   │   └── browser/           #     Unauthorized browser settings and search/homepage changes
│   └── wipe/disk/             #   Disk wiping                             T1561
│
├── lateral-movement/          # Propagation (OB0011)
│   │                          #   "Propagate or move through an environment"
│   │                          #   Active (direct access) or passive (malicious email).
│   │                          #   Everything here must involve spreading to new systems.
│   │                          #   Scanning/recon → discovery/. Local password cracking → credential-access/.
│   │                          #   Process injection → evasion/. Masquerading → evasion/masquerade/.
│   ├── brute-force/           #   Remote service credential spraying      T1110
│   │   ├── ssh/               #     SSH brute-force                       T1021.004
│   │   ├── iot/               #     IoT default credentials (Mirai-style)
│   │   ├── network/           #     Network service cracking
│   │   └── password/          #     Default credential lists (components)
│   ├── delivery/              #   Payload delivery to new targets         E1105
│   ├── exploit/               #   Remote exploitation for access
│   ├── infection/             #   File infection / virus propagation      T1554
│   ├── pass-the-hash/         #   Credential reuse for remote access      T1550.002
│   ├── smb/                   #   SMB share propagation                   T1021.002
│   ├── social-engineering/    #   Lures, spam (passive lateral)           B0020, B0021
│   ├── ssh/                   #   SSH lateral (connect, backdoor, deploy) T1021.004
│   ├── trojanize/             #   Software trojanization
│   ├── usb-worm/              #   USB drive propagation
│   └── worm/                  #   Self-propagating (email, SMB, IRC, P2P)
│   # Brute-force lives here (not credential-access/) because malware brute-forcing
│   # is almost always about spreading to remote services, not cracking local passwords.
│   # Local password cracking (hashcat, john) would be credential-access/.
│
├── persistence/               # Remain on system (OB0012)
│   │                          #   "Remain on a system regardless of system events"
│   │                          #   Organized by durable activation/access boundary, not
│   │                          #   file location or owner. See ordered persistence contract.
│   │                          #   NOTE: hiding/concealment belongs in evasion/, not here.
│   │                          #   Persistence requires reactivation or retained access.
│   ├── firmware/              #   Survives OS reinstall — below the OS
│   │   └── boot/record/      #     MBR/bootkit                           F0013, T1542
│   ├── access/                #   Planned: retained accounts, keys, tokens and grants
│   ├── application/           #   Planned: durable application/runtime/project activation
│   ├── system/                #   Durable OS-managed boot/timer/event activation
│   │   ├── cron/              #     System crontabs (/etc/crontab)        T1053.003
│   │   ├── daemon/init/       #     Legacy: fork+setsid alone is process/daemonize
│   │   ├── init/              #     SysV init.d, rc.local, chkconfig
│   │   ├── input-manager/     #     macOS InputManager                    T1547.015
│   │   ├── launchd/           #     macOS LaunchDaemons                   T1543.004
│   │   ├── registry/          #     OS activation settings; HKLM Run still uses login/registry
│   │   ├── service/install/   #     Windows SCM / systemd units           T1543.003
│   │   ├── systemd/           #     Legacy duplicate; service manager → service
│   │   └── wmi/subscription/  #     WMI event subscriptions               T1546.003
│   └── login/                 #   Runs at user login / session start
│       ├── account/create/    #     Legacy: retained principal → planned access
│       ├── ifeo/debugger/     #     Legacy: executable-start trigger → planned application
│       ├── registry/          #     HKCU Run keys, auto-launcher          F0012
│       ├── scheduled-task/    #     Login-triggered tasks only; OS timers → system
│       ├── self-install/      #     Self-copy + registry persistence
│       ├── shell/config/      #     .bashrc, .zshrc, .profile             T1546.004
│       ├── ssh/backdoor/      #     Legacy: durable authorized key → planned access
│       ├── startup/           #     Start Menu folder, shortcuts          T1547
│       ├── winlogon/userinit/ #     Winlogon Userinit key                 T1547.004
│       └── xdg/               #     XDG autostart entries
│
├── privilege-escalation/      # Obtain higher permissions (OB0013)
│   │                          #   Often overlaps with Persistence behaviors
│   ├── exploit/               #   Local exploitation                      T1068
│   │   └── kernel/            #     Kernel LPE (IDT, commit_creds)
│   ├── elevation-control/     #   Abuse elevation control                 T1548
│   │   ├── uac-bypass/        #     Windows UAC bypass                    T1548.002
│   │   ├── manifest/          #     Windows manifest elevation
│   │   ├── setuid/            #     Setuid abuse (Unix)                   T1548.001
│   │   ├── applescript/       #     AppleScript admin privs               T1548.004
│   │   └── security-framework/#     macOS Authorization APIs              T1548.004
│   ├── hijack-execution-flow/ #   Execution flow hijacking                F0015
│   │   ├── service/           #     Service binary path hijack
│   │   └── preload/           #     LD_PRELOAD into privileged procs
│   ├── kernel-modules/        #   Kernel modules & extensions             F0010
│   ├── modify-service/        #   Modify existing service                 F0011
│   ├── process-injection/     #   Injection into privileged procs         E1055
│   ├── install-certificate/   #   Root cert installation                  F0016
│   └── token-manipulation/    #   Token/privilege manipulation             T1134
│
├── supply-chain/                # Supply chain compromise (T1195)
│   │                            #   "Manipulate products or product delivery mechanisms
│   │                            #   prior to receipt by a final consumer for the purpose
│   │                            #   of data or system compromise."
│   │                            #   Organized by ATTACK TECHNIQUE, not ecosystem
│   │                            #   or evidence container. Ecosystem (npm, pypi,
│   │                            #   rubygems) usually belongs in filenames; use it
│   │                            #   as a directory only when the registry surface
│   │                            #   itself is the technique being modeled.
│   │                            #   Avoid vague buckets such as package/,
│   │                            #   manifest/, behavior/, metadata/, or more/:
│   │                            #   choose the move being made instead.
│   │                            #   Require component/distribution trust abuse. Merely
│   │                            #   restricting a rule to packages does not establish it.
│   │                            #   Generic behaviors stay in their existing objectives:
│   │                            #     Generic recon (whoami) → discovery/.
│   │                            #     Source + unauthorized send → exfiltration/stealer/.
│   │                            #     HTTP POST alone → micro-behaviors/communications/http/post/.
│   │                            #     Generic obfuscation → anti-static/obfuscation/.
│   │                            #     Generic credential reads → credential-access/.
│   │                            #   Supply-chain composites reference those atomics.
│   │                            #   Build/test facts → metadata; software identity → well-known;
│   │                            #   benign suppressors → crit: exception composites.
│   ├── install-hook/            #   Legacy trigger partition; close to new result copies
│   │                            #     Declaration → metadata/package/scripts/lifecycle.
│   │                            #     Invocation → package-manager capability.
│   │                            #     Theft/execution/persistence → required outcome.
│   ├── recon-exfil/             #   Legacy duplicate results; migrate by acquired source
│   │                            #     No send → discovery/collection/credential-access.
│   │                            #     Source + send → exfiltration/stealer/<source>.
│   │                            #     Lifecycle/registry/CI context is referenced evidence.
│   ├── credential-theft/        #   Legacy store duplication; migrate to credential-access
│   │                            #     Registry credentials remain secrets regardless of trigger.
│   ├── hidden-payload/          #   Concealed malicious code in packages     T1027
│   │                            #     Concealment abusing declared/shipped content or package
│   │                            #     inspection trust. Compilation/hex arrays alone are generic.
│   │                            #     Composites reference anti-static/ atomics.
│   │                            #     NOT general obfuscation (→ anti-static/obfuscation/).
│   │                            #     `runtime/` is legacy; do not classify by phase.
│   ├── impersonation/           #   Package identity deception               T1195.002
│   │                            #     Typosquatting, dependency confusion, deprecated-package
│   │                            #     hijack, function shadowing, name similarity.
│   │                            #     Suspicious metadata is not a supply-chain attack kind;
│   │                            #     use metadata/package facts as signals for an established
│   │                            #     deception comparison or other concrete trust violation.
│   └── trojanized/              #   Backdoored legitimate code               T1195.002
│                                #     Modifications to known-good libraries/frameworks.
│                                #     A wholly malicious package goes with its established
│                                #     behavior; it is not necessarily concealed or trojanized.
```

## Tier 3: Known Entities (`well-known/`)

Specific, broadly recognizable software identities, including malware families, unwanted software, dual-use products, applications, libraries, games, and professional tools. Malware categories align with [MBC/STIX 2.1 malware types](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html).

For libraries, identify the analyzed artifact itself. Embedded implementation
signatures belong with their supported techniques or capability groups under
the [implementation contract](#implementations-and-library-fingerprints).

Do not create general-purpose traits in `well-known/` that could match multiple families, even at a low criticality. Move general-purpose traits to a general-purpose location.

**Rules:**
- Each malware family appears in exactly **one** category — pick the primary behavior
- Categories describe **what the malware does**, not who made it or how it arrives
- Actor attribution (APT group, nation-state) belongs in trait descriptions, not directory names
- When a family has multiple capabilities (e.g., stealer + worm), pick the most distinctive
- `trojan/` is the catch-all — use only when no more specific type fits
- `dual-use/` is for legitimate named software whose abuse-relevant function warrants explicit analyst notice; group it by that function
- `unwanted/` is the umbrella for PUA, PUP, adware, and riskware families whose distribution or operation is itself unwanted; do not add a parallel `pua/` alias
- `tool/` is for professional developer, analyst, offensive-security, reverse-engineering, and administration tools that do not fit the narrower dual-use boundary
- Apply the ordered [known-entity contract](#known-entities-one-identity-one-primary-function) before choosing a function; never create parallel identity trees for the same entity

```
well-known/
├── app/                   # Specific legitimate applications and suites
│   ├── ai/                #   AI assistants, agents, and automation products
│   ├── browser/           #   Web browsers and browser runtimes
│   ├── browser-extension/ #   Browser extensions, grouped by product
│   ├── communication/     #   Mail, chat, messaging, and conferencing clients
│   ├── publishing/        #   CMS, publishing, and content-management products
│   ├── data/              #   Databases, dashboards, search, and analytics apps
│   ├── development/       #   User-facing IDEs and development applications
│   │                      #     Standalone build/CLI utilities → tool/development/.
│   ├── enterprise/        #   Enterprise management and business suites
│   ├── finance/           #   Wallet, trading, banking, and payment applications
│   ├── infrastructure/    #   Cloud, server, container, and deployment products
│   ├── media/             #   Audio, video, graphics, and creative applications
│   ├── network/           #   Ordinary network clients, services, and monitors
│   │                      #     Abuse-salient tunnels/proxies → dual-use/tunnel/.
│   ├── productivity/      #   Office, notes, documents, and personal productivity
│   ├── security/          #   End-user defensive and security products
│   │                      #     Analyst/pentest utilities → tool/{detection,offensive}/.
│   ├── storage/           #   Backup, synchronization, recovery, and storage apps
│   ├── system/            #   OS, desktop, runtime, and platform components
│   └── utility/           #   Cleaners, installers, disk, and system utilities
├── dual-use/              # Legitimate software with abuse-relevant capabilities
│   ├── access-control/    #   Licensing, activation, and privilege-control utilities
│   ├── credentials/       #   Password, hash, key, and product-key recovery
│   ├── tunnel/            #   Proxies, relays, and network tunnels
│   ├── packaging/         #   Packers and executable converters
│   ├── remote-admin/      #   Remote monitoring and administration products
│   └── transfer/          #   General-purpose bulk transfer and cloud-sync tools
├── game/                  # Game clients/platforms and game-specific tools
│   └── (steam, etc.)
├── lib/                   # Widely recognized libraries/frameworks/runtimes
│   ├── ai/                #   AI, machine-learning, and inference libraries
│   ├── cloud/             #   Cloud-provider and platform SDKs
│   ├── concurrency/       #   Async control flow, promises, queues, pooling
│   ├── crypto/            #   Cryptography, identity, and authentication libraries
│   ├── data/              #   Databases, dataframes, ORM, and storage clients
│   ├── datetime/          #   Date, time, calendar, and astronomical libraries
│   ├── development/       #   Compilers, testing, linting, and build libraries
│   ├── format/            #   Parsers, schemas, archives, and serialization
│   ├── media/             #   Audio, video, image, font, and codec libraries
│   ├── network/           #   Protocol, transport, and network client libraries
│   ├── observability/     #   Logging, error tracking, APM, and session replay
│   ├── platform/          #   OS, desktop, mobile, and platform integration
│   ├── runtime/           #   Language runtimes, engines, FFI, and bindings
│   ├── stdlib/            #   Standard-library extensions, polyfills, shims
│   ├── testing/           #   Test frameworks, assertion and fixture libraries
│   ├── native/            #   Native systems, libc, allocators, and kernel support
│   ├── ui/                #   UI components, editors, and frontend libraries
│   ├── vendor-sdk/        #   Single-vendor product and service SDKs
│   └── web/               #   Web and application frameworks
│                          #
│                          # `stdlib/` replaced `core/`, which was banned as a
│                          # catch-all. It is not "small utilities": the test is
│                          # that the library extends or polyfills the language's
│                          # OWN standard library -- collections (lodash), type
│                          # predicates (is-what), compat shims (six, es6-shim).
│                          # A library with a subject of its own goes to that
│                          # subject's category, never here.
│                          #
│                          # Cloud resource/control-plane SDKs belong in cloud/, even
│                          # for one provider. Other single-vendor product/service
│                          # SDKs use vendor-sdk/; generic protocols use network/.
│                          #
│                          # Every library sits in a FUNCTION bucket above. There is
│                          # no `core/`, `common/` or `misc/`: a catch-all never makes
│                          # you answer "what does this library do", which is the
│                          # question that also surfaces whether it belongs here at
│                          # all. If you cannot name the function, that is the signal
│                          # to stop, not to invent a bucket.
│                          #
│                          # ENTRY BAR — `well-known/` is for "specific, broadly
│                          # recognizable software identities". Before adding a
│                          # library, both must hold:
│                          #   1. an analyst would recognize the name unprompted, and
│                          #   2. it appears across many samples, so the rule earns
│                          #      its keep beyond the one file that prompted it.
│                          # A directory whose whole content is a package-name match
│                          # is an allowlist, not an identity. Two rules and a name is
│                          # the shape that gives it away.
│                          #
│                          # If a narrow package keeps false-positiving, the fix is
│                          # one of: tighten the matcher that fired (usually right),
│                          # or a `crit: exception` benign-context composite, which
│                          # may live anywhere and is the sanctioned home. Adding an
│                          # obscure package here to silence one sample trades a
│                          # false positive for a permanent maintenance burden and
│                          # teaches the model a name it will never see again.
├── malware/               # Malware family signatures
│   ├── backdoor/          #   Passive remote access — shell, tunnel, implant
│   │                      #     Waits for attacker commands. Simpler than a RAT.
│   │                      #     (BPFDoor, TinyShell, RustDoor)
│   ├── botnet/            #   Bot network member — C2-controlled fleet
│   │                      #     Part of coordinated infrastructure.
│   │                      #     (Mirai, Gafgyt, Mozi)
│   ├── downloader/        #   Fetches payload from remote URL
│   │                      #     No embedded payload — downloads at runtime.
│   │                      #     (SugarLoader)
│   ├── dropper/           #   Contains or stages another payload
│   │                      #     Embedded payload dropped to disk or loaded into memory.
│   │                      #     (Nemucod, Hadooken, TEARDROP)
│   ├── exploit/           #   Exploits a specific vulnerability (CVE, PoC)
│   │                      #     (Roblox game exploits, CVE-specific code)
│   ├── keylogger/         #   Primary function is keystroke capture
│   │                      #     (Backtrack, ChromePush)
│   ├── miner/             #   Cryptomining / resource hijacking
│   │                      #     MBC: resource-exploitation. A miner product identity alone
│   │                      #     does not establish a malicious family or unauthorized mining.
│   ├── ransomware/        #   Encrypts files and demands ransom
│   │                      #     (LockBit, Conti, Babuk)
│   ├── rat/               #   Full remote administration toolkit
│   │                      #     Superset of backdoor — file manager, screen viewer,
│   │                      #     keylogger, webcam, plugin system.
│   │                      #     Require malicious-family evidence; a legitimate remote
│   │                      #     administration/testing product is not malware by name alone.
│   ├── rootkit/           #   Kernel or userspace hiding + privilege escalation
│   │                      #     (eBPFKit, Reptile, Diamorphine)
│   ├── stealer/           #   Information stealer — credentials, tokens, wallets
│   │                      #     MBC: information-stealer. (AMOS, RedLine, Vidar)
│   ├── supply-chain/      #   Legacy class; package delivery alone does not choose identity
│   │                      #     Reconcile recognized families by defining behavior;
│   │                      #     retain one canonical family home and reference trust abuse.
│   ├── trojan/            #   Disguised as legitimate software
│   │                      #     Use only when no more specific type fits. The social
│   │                      #     engineering / disguise is the defining characteristic.
│   │                      #     (Emotet, DNSChanger)
│   ├── virus/             #   Self-replicating file infector
│   │                      #     Modifies other executables to include itself.
│   │                      #     (Rivanon, BlackHawk, Nicole)
│   ├── webshell/          #   Web-based backdoor (PHP/JSP/ASP shell)
│   │                      #     (Alfa, Ribel)
│   └── worm/              #   Self-propagating across networks
│                          #     Spreads without user interaction (email, SMB, SSH).
│                          #     (MyDoom, Conficker, Beagle)
│
├── unwanted/              # Potentially unwanted software and riskware families
│                          #   Umbrella for named PUA/PUP/adware/riskware entities
│                          #   whose distribution or operation is itself unwanted,
│                          #   but which are not clearly hostile malware.
│                          #   Do not use for ordinary legitimate dual-use products.
│                          #   (Computrace/rpcnetp, OfferCore)
│
└── tool/                  # Legitimate tools often abused
    ├── browser/           #   Browser components (Chromium sandbox, extensions)
    ├── development/       #   Standalone compiler/build/CLI tools; integrated IDEs → app/development
    ├── detection/         #   Security detection tools (cleave's own stng)
    ├── forensics/         #   Memory, disk, and incident-forensics tools
    ├── media/             #   Media acquisition/conversion (yt-dlp, gallery-dl)
    ├── packaging/         #   Package/version managers, installer builders
    ├── offensive/         #   Pentesting/red-team tools + game cheat frameworks
    ├── reverse-engineering/#  RE tools (IDA, OllyDbg, Scylla, LordPE)
    └── sysadmin/          #   Admin tools, system libraries, VCS
```

## Metadata (`metadata/`)

Properties of the artifact: its structure, format, provenance, declarations,
and measurements. Content may supply evidence for these properties, but
content is not automatically metadata. A distinctive string indicating a
probable capability belongs with that capability in `micro-behaviors/`.

**Rules:**
- Behavioral detection belongs in `micro-behaviors/` or `objectives/` according to the evidence, not here
- Tool/malware signatures belong in `well-known/`, not here
- Supply-chain attack indicators belong in `objectives/supply-chain/` (organized by technique, not ecosystem)
- OS/platform vendor traits go under `vendor/`
- Identities of the analyzed app, dual-use product, tool, game, or library/framework/runtime artifact go under `well-known/{app,dual-use,tool,game,lib}/`. Embedded implementation fingerprints belong with their supported capabilities; dependency declarations and attribution alone remain metadata.
- **Distinguish a tool's *output* from the tool's *identity*.** "This code was bundled/minified/transpiled" is a build-transform fact → `metadata/build/<function>/` (group by function: `bundler/`, `minifier/`, `transpiler/`). "This file *is* webpack / PuTTY / Wireshark" is a named-software fingerprint → `well-known/`. Putting a software identity in `metadata/` is the same *matcher-defines-identity* violation as mislabeling a generic capability.
- **Avoid grab-bag directories.** A directory must name one coherent concept that is meaningful as an ML path feature. If a dir accretes unrelated kinds of traits — e.g. the former `package/tooling/` held build-output (`webpack-bundled`), software identities (`tool-identity-putty`), *and* project-hygiene facts (`has-eslint-config`) all at once — the path feature becomes noise and analysts can't reason about it. Split each kind to its proper home (`build/`, `well-known/`, and the `package/` subdirectory for the subject) and delete the grab-bag. Vague names (`tooling`, `context`, `misc`, `helpers`) are a smell that this has happened.

  **Audit semantic content currently filed under `file/string`.** Do not send
  capability indicators here merely because they match strings or cannot prove
  execution. Existing semantic-content branches and their older placement rows
  are a migration backlog, not precedents for new rules. Reassess each matcher
  for its probable capability or characteristic; retain genuine artifact
  measurements such as extracted-string counts in metadata. A weak but useful
  capability indicator can remain with its capability at appropriate confidence.

  The former `metadata/library/` tree held ~1,030 rules across ~68 directories and mixed several different concepts: library fingerprints that duplicated `well-known/lib/`, plain capability markers wearing a library's directory name, named offensive tools, CI fingerprints, and vague structural leaves. That migration is complete: `metadata/library/` is now closed and empty. Because a directory reference is an ML path feature, each migrated matcher was placed according to what it actually finds; never recreate the old bucket or move a whole directory on the strength of its name.
- New top-level subdirectories require updating both TAXONOMY.md and `ALLOWED_METADATA` in `src/capabilities/validation/directory_whitelist.rs`
- **Depth:** Prefer breadth when precision is unchanged; depths above five below `metadata/` receive the same non-blocking review warning as other tiers. Current direct ML path features include only two levels below the tier; taxonomy depth and model visibility are separate concerns.
- **Max leaf size:** 100 rules per directory across all tiers, atomic traits and composite rules counted together (`policy/oversized-dir`); no directory exemptions
- **Max fan-out:** No directory should have more than 150 immediate subdirectories. Split by the parent's documented subject/function question; ecosystem or vendor grouping must not create a second home for the same claim.
- **Prefer technology-neutral subdirectory names.** Technology names belong in filenames, not directory names, unless the technology itself defines the subject. The 100-rule cap does not justify a language or platform split.
- **One level, one question.** Every child of a directory must answer the *same* question about its parent. A level that mixes axes gives some traits two valid homes at once, and the duplicate pair is then created by the taxonomy rather than by an author: it is not a mistake anyone can avoid.

  The test is to name the question out loud and check that every sibling answers it. `micro-behaviors/fs/path/` should answer *what does this path point at* — a credential, a cookie, a config file, a log, a cache. Siblings like `application/`, `package-manager/`, `os/` and `webserver/` answer a different question, *whose is it*, and siblings like `basename/`, `construct/` and `traversal/` answer a third, *what is being done with it*. With all three present, "an application's config file path" is a genuine member of `config/`, of `application/config/`, and arguably of `basename/` — which is exactly how `fs/path/config/app/` and `fs/path/application/config/` both came to exist, holding the same subject (`editor-extensions` on one side, `vscode` on the other).

  Pick the axis that distinguishes *behavior*, because that is what the directory feature feeds to the ML pipeline. Reading a credential path is a different act from reading a cache path, so the resource kind is the axis; Chrome's cookie path and Firefox's are the same act, so the owner is not. The losing axes move into the filename, exactly as platform and language already do: `config/app/vscode.yaml`, never `application/config/vscode.yaml`.

- **A trigger is not an objective.** Independent dimensions must not be multiplied into a path. A rule about a payload carries three facts that vary freely: what it *does* (fetch, stage, execute), what *sets it off* (an install hook, a git hook, a `.lnk`, a fake update), and where it *came from* (npm, PyPI, an RPM). Give each its own directory level and the tree has to enumerate every objective under every trigger.

  That happened under `objectives/supply-chain/install-hook/`: the trigger partition grew a second objective tree — `dropper/`, `credential/`, `config-write/`, `database/`, `registry/` — while `objectives/command-and-control/dropper/` independently grew `lifecycle/` and `package/`. The directory contracts now resolve that ambiguity: the required result owns the composite; the trigger is a referenced observation. Existing copies need coordinated migration.

  The behavior owns the directory, because that is the feature the ML pipeline reads. The channel is a filename, as for any other ecosystem. The trigger is a *referenced trait*: `metadata/package/scripts/lifecycle::install-hooks` is a fact about the package, and a composite that wants "install hook downloads and executes" names it as a leg rather than moving house to sit under it.

  The diagnostic: if a directory level names *when* or *how* something runs rather than *what is achieved*, every objective underneath it is a duplicate waiting to be written.



```
metadata/
├── arch/                  # CPU architecture (x86, ARM, MIPS, IoT)
├── binary/                # Binary internals (requires binary parsing).
│   │                      #
│   │                      #   ONE ORGANIZING AXIS: the anatomy of the format. Each child
│   │                      #   names a PART of the binary (header, sections, symbol
│   │                      #   tables, resources, …) and holds facts ABOUT that part.
│   │                      #
│   │                      #   The rule that settles every placement question here:
│   │                      #   **a directory holds facts about a part of the format,
│   │                      #   never facts about what the contents of that part MEAN.**
│   │                      #     "the import table has three entries"  → symbols/
│   │                      #     "it imports GetProcAddress"           → micro-behaviors/
│   │                      #     "its exports impersonate version.dll" → objectives/ (sideload)
│   │                      #     "those exports are libcurl's ABI"     → well-known/lib/
│   │                      #
│   │                      #   Two axes that are NOT directories here, because they are
│   │                      #   things a trait SAYS rather than parts of the artifact:
│   │                      #     - measurement ("metrics") — every fact here is measured;
│   │                      #       put the count with the part it counts and let the
│   │                      #       threshold live in the trait name.
│   │                      #     - judgment ("anomaly") — malformedness is a fact about
│   │                      #       the part; `crit:` carries how unusual it is.
│   │                      #   Adjectives (`sparse/`, `dense/`, `threshold/`, `structural/`)
│   │                      #   fail the precision test above: they partition by value, not
│   │                      #   by subject, and spend the last ML-visible level on nothing.
│   ├── header/            #   Machine, characteristics, timestamps, entry point,
│   │                      #     malformed/contradictory header fields
│   ├── section/           #   Sections: names, count, size, entropy, permissions,
│   │                      #     alignment, sparsity. Section *content* patterns are
│   │                      #     behavior → objectives/, or capability → micro-behaviors/
│   ├── symbols/           #   Shape of the import/export/symbol tables: counts, ordinal-
│   │                      #     only imports, stripped tables, export-name statistics.
│   │                      #     A NAMED api/symbol is a capability → micro-behaviors/
│   ├── code/              #   The code itself: basic blocks, functions, complexity,
│   │                      #     code size and density
│   ├── instruction/       #   Instruction-level patterns (indirect calls, CPUID)
│   ├── resource/          #   Embedded resources
│   ├── linking/           #   Dynamic dependencies, RPATH/RUNPATH, delay-load
│   ├── debug/             #   Debug directories and symbol files (PDB, DWARF)
│   ├── layout/            #   Whole-file structure: overlay, embedded payloads, bundles
│   └── provenance/        #   Build-origin records, source-tree/VCS identifiers
│                          #     Inferred language/compiler attribution → lang/compiler/
│   #
│   # Routed OUT of metadata/binary/, because identity is not a format property:
│   #   installer/  → well-known/  (Inno Setup, NSIS, WiX, InstallShield, 7-Zip SFX
│   #                 are named products; the *fact* that a file is self-extracting
│   #                 is layout/)
│   #   framework/  → well-known/lib/ for the runtime's identity; keep only the
│   #                 format-level consequence (e.g. "PE carries a CLR header")
│   #   vendor/     → metadata/vendor/ (already the sanctioned home for OS/platform
│   #                 vendors) or well-known/ for products
│   #   signing/    → metadata/signed/   license/ → provenance/   toolchain/ → lang/compiler/
├── build/                 # How an artifact was BUILT or TRANSFORMED — never *who* the
│   │                      #   tool is. Group by transform FUNCTION, not by specific tool:
│   │                      #   the directory is an ML feature, so `bundler/` is one dense
│   │                      #   signal across webpack/rollup/esbuild/parcel/vite, and the
│   │                      #   specific tool is the trait NAME (`esbuild-bundled`). The
│   │                      #   tool's IDENTITY as named software (e.g. "this binary IS
│   │                      #   webpack/PuTTY") belongs in well-known/, never here.
│   ├── bundler/           #   Module bundlers (webpack, rollup, esbuild, parcel, vite)
│   ├── minifier/          #   Minifier / uglifier output patterns
│   ├── transpiler/        #   Source-to-source transforms (babel, typescript, swc)
│   ├── autotools/         #   GNU build family (autoconf, automake, libtool)
│   ├── scaffold/          #   Project/code generators and templating
│   ├── ci/                #   CI/CD pipeline fingerprints (github-actions, jenkins)
│   └── ...                #   cmake, cargo, docker, conda, ecosystem
├── document/              # Document internals (requires document parsing)
│   ├── chm/               #   Compiled HTML Help (ITSF/ITSP/PMGL)
│   ├── html/              #   HTML structure
│   ├── office/            #   Office documents
│   │   ├── macro/         #     VBA, embedded macros
│   │   └── markup/        #     OOXML, ActiveMime structure
│   ├── ole/               #   OLE compound documents
│   ├── pdf/               #   PDF structure
│   └── rtf/               #   RTF analysis
├── file/                  # File-level observables (no deep parsing required)
│   ├── catalog/           #   File/catalog identity and generated registries
│   ├── encoded/           #   Encoded content presence (base64)
│   ├── extension/         #   File extension classification
│   ├── format/            #   Text/data format identification (JSON, makefile)
│   ├── invisible-unicode/ #   Invisible Unicode text properties
│   ├── magic/             #   Magic byte signatures
│   │                      #   (no metrics/ — a measurement is not a subject; file text
│   │                      #    shape belongs with profile/, entropy with the thing measured)
│   ├── policy/            #   Policy/config text identities
│   ├── profile/           #   Text profile and wrapper shapes
│   └── string/            #   String measurements; semantic-content branches await audit
├── font/                  # Font container structure (sfnt/WOFF/WOFF2/EOT)
│   ├── container/         #   Format identity and header/table-directory validity
│   └── layout/            #   Byte coverage: gaps, trailing data, oversized tables
│                          #   File identity remains under file/{magic,extension};
│                          #   masquerade/stowaway INTENT lives in objectives/
├── hardening/             # Security hardening features (sandbox, seccomp, pledge)
├── image/                 # Image-specific neutral measurements
│                          #   (no metrics/ — pixel and channel statistics belong with the
│                          #    image property they measure)
│                          #   File identity remains under file/{magic,extension}
├── media/                 # Media-container structure, shared across carriers
│   ├── container/         #   Container identity and structural consistency
│   └── layout/            #   Byte coverage: holes, trailing data, what fills them
│                          #   Covers fonts, images, audio and video alike;
│                          #   masquerade/stowaway INTENT lives in objectives/
├── import/                # Dependencies/imports (auto-generated)
│   ├── python/ npm/ ruby/ java/ go/ rust/ c/
│   └── macho/ elf/ pe/   #   Binary format imports
├── lang/                  # Language, compiler, encoding detection
│   ├── compiled/          #   Compiled language detection (assembly, C, Go, Rust)
│   ├── compiler/          #   Compiler identification
│   │   ├── managed/       #     Managed runtimes (.NET, Delphi)
│   │   ├── native/        #     Native toolchains (GCC, Clang, MSVC, MinGW)
│   │   └── systems/       #     Systems language compilers (Go, Rust)
│   ├── embedded/          #   Embedded language detection
│   ├── encoded/           #   Encoded strings (unicode, wide)
│   ├── generated/         #   Emitted by a code generator, not hand-written
│   ├── javascript-features/ # JavaScript language features
│   ├── scripted/          #   Scripted language detection (VBScript, Lua, Perl)
│   ├── source/            #   Which language a source file is written in
│   ├── upstream/          #   Part of a recognized upstream tree (Wine, ReactOS, Linux)
│   └── ...                #   go-build, linking, optimization, security, shebang, version
├── library/               # CLOSED historical namespace; migration completed, do not recreate.
│   │                      #   Do not classify by implementation container. Independent
│   │                      #   artifact identity → well-known/lib/; embedded code → its
│   │                      #   supported capability; declarations → their metadata subject.
│   │                      #   Migrate existing entries by what each matcher finds:
│   │                      #     library/framework/runtime identity → well-known/lib/<function>/
│   │                      #     a neutral capability (screenshot, download, symbol lookup)
│   │                      #       → micro-behaviors/<category>/
│   │                      #     intent-bearing behaviour → objectives/
│   │                      #     build/transform output (bundled, minified) → metadata/build/
│   │                      #   Historical IDs must not be revived as aliases.
├── package/               # Package ecosystem metadata and project-hygiene facts
│   ├── config/            #   Configuration file detection
│   ├── contributors/      #   Contributor metadata
│   ├── dependencies/      #   Dependency analysis, split by where the fact was read:
│   │                      #     manifest/ (declared), lockfile/ (resolved), archive/ (shipped)
│   │   └── manifest/      #     Facets are ordered; see "Choosing a dependency-manifest facet":
│   │                      #     identity/ name-form/ source/ range/ reconciliation/ presence/ count/
│   ├── documentation/     #   Documentation presence
│   ├── error-handling/    #   Error handling patterns
│   ├── files/             #   File counts and types
│   ├── keywords/          #   Package keywords
│   ├── license/           #   License detection
│   ├── logging/           #   Logging patterns
│   ├── maintainers/       #   Maintainer counts
│   ├── manager/           #   Package-manager fingerprints (homebrew, composer) — the
│   │                      #     distribution tool, distinct from the build transform (build/)
│   ├── name/              #   Manifest name field  (each manifest field is its own
│   ├── description/       #   Manifest description field   leaf, at the ML-visible
│   ├── repository/        #   Manifest repository field    level -- there is no
│   ├── author/            #   Manifest author field        `manifest/` container:
│   ├── entrypoint/        #   Declared entry point         keywords/, license/,
│   ├── runtime/           #   Declared runtime/engines     scripts/ and dependencies/
│   ├── ...                #   homepage, version, vendor,   are manifest fields too,
│   │                      #     publishing, workspace, …   so the level separated
│   │                      #     nothing while spending the last visible segment.
│   │                      #   Package metadata that is NOT a manifest field is read from
│   │                      #     the package's contents or layout instead: files/,
│   │                      #     documentation/, testing/, integrity/, scaffold/.
│   │                      #   (no metrics/ — a measurement is not a subject)
│   │                      #   (no quality/ — a judgment, not a subject: whose quality, by
│   │                      #    what standard? Its contents belong with the field or subject
│   │                      #    they describe — manifest-field completeness -> the actual field,
│   │                      #    version values -> versioning/, checksum manifests ->
│   │                      #    integrity/, logging -> logging/, error handling ->
│   │                      #    error-handling/ — and its benign-context suppressors are not
│   │                      #    metadata at all: named software -> well-known/, the
│   │                      #    suppressor itself -> a `crit: exception` composite)
│   ├── scripts/           #   Package scripts
│   ├── testing/           #   Testing detection
│   │   ├── compiled/      #     Legacy language partition; classify test role
│   │   ├── harness/       #     Runtime-specific test harnesses
│   │   ├── presence/      #     Test presence indicators
│   │   └── scripted/      #     Legacy language partition; classify test role
│   └── versioning/        #   Version detection
│       # NO `tooling/` — it was a grab-bag mixing build-output (→ build/),
│       # software identities (→ well-known/), and properties of unrelated subjects.
│       # There is no quality/ destination; use the actual subject above.
├── permission/            # Declared permission and extension authority metadata
│   │                      #   Neutral facts about what authority a manifest grants or
│   │                      #   what declared API surface is available. Actual API use
│   │                      #   belongs with capabilities. Provider/ecosystem belongs
│   │                      #   in filenames (browser.yaml, vscode.yaml), not dirs.
│   │                      #   Abuse chains using these facts belong in objectives/.
│   ├── activation/        #   Auto-activation and extension lifecycle triggers
│   ├── active-tab/        #   Browser activeTab authority
│   ├── alarm/             #   Timers/alarms extension authority
│   ├── bookmark/          #   Bookmark access authority
│   ├── capture/           #   Screen, tab, media, and display capture authority
│   ├── clipboard/         #   Clipboard read/write authority
│   ├── cookie/            #   Cookie read/write/watch authority
│   ├── debugger/          #   Browser/debugger attachment authority
│   ├── dom/               #   Page DOM script/style injection authority
│   ├── download/          #   Download API authority
│   ├── extension-api/     #   Generic extension host API context markers
│   ├── extension-id/      #   Extension identifier lists/maps
│   ├── history/           #   Browser history/top-sites authority
│   ├── host/              #   Host/origin authority patterns and broad host access
│   ├── identity/          #   OAuth/identity permission declarations
│   ├── management/        #   Extension-management authority
│   ├── manifest/          #   Extension manifest structure and manifest-only fields
│   ├── network/           #   Request interception/filtering/modification authority
│   ├── offscreen/         #   Offscreen document authority
│   ├── runtime/           #   Declared runtime authority/context; callback use → capabilities
│   ├── storage/           #   Extension storage authority
│   ├── telemetry/         #   Extension telemetry/event reporting authority
│   ├── uri/               #   URI handler and OAuth callback authority
│   └── workspace/         #   Workspace/file access authority
├── signed/                # Code signatures, certificates, entitlements
│   ├── certificate/       #   Certificate chain string patterns
│   ├── entitlements/      #   Code entitlements (macOS/iOS, Android)
│   ├── platform/          #   Platform-signed binary composites (auto-generated)
│   ├── trust-level/       #   Signing trust level (ad-hoc, developer, platform, app store)
│   └── (auto-generated: platform::apple, developer::*, adhoc::unsigned)
└── vendor/                # OS/platform vendor identification only
    └── (per-vendor subdirs: apple, microsoft, netbsd, fsf, etc.)
```

### Metadata boundary rubric

When placing a new metadata trait, use this tiebreaker table. Each row names the two most likely categories and the deciding question:

| Category A | Category B | Deciding question |
|-----------|-----------|-------------------|
| `binary/` | `file/` | Is the claim about executable/object-file anatomy? → `binary/`. Is it about whole-file format, extension, magic or size? → `file/`. The parser used is supporting evidence, not the placement rule. |
| `binary/` | `document/` | Is the subject executable/object-file anatomy? → `binary/`. Document/container structure (OLE, OOXML, PDF objects)? → `document/`. Behavior or identity inferred from either keeps its own tier. |
| `binary/` | `lang/` | Is it about the binary's structure (sections, imports, metrics)? → `binary/`. Is it about what language/compiler produced it? → `lang/` |
| `binary/<part>/` | `crit:` | Both a neutral measurement and a malformation are facts about the same part of the format, so both live with that part (`header/`, `section/`, `code/`, `symbols/`). How unusual the value is goes in `crit:` — `baseline` for a zero timestamp, `notable` for a far-future one — not in a `metrics/` vs `anomaly/` directory choice |
| `document/` | `file/` | Document internal objects/relationships → `document/`; whole-file format identity → `file/`. OLE/OOXML/PDF magic alone does not assert an internal relationship. |
| `build/` | `lang/` | Is it about build orchestration (cmake, docker, CI/CD)? → `build/`. Is it about the language toolchain (gcc, rustc, delphi)? → `lang/` |
| `metadata/build/` | `well-known/` | Is it the **output/shape a tool left in the file** (this code was *bundled*, *minified*, *transpiled*)? → `metadata/build/<function>`. Is it the **named tool/software being identified** (this *is* PuTTY / Wireshark / the webpack package)? → `well-known/{app,dual-use,tool,lib}/`. The transform is a metadata fact; the identity is a fingerprint. A named-software fingerprint in `metadata/` is the "matcher defines identity" violation. |
| `metadata/build/` | `metadata/package/` | Is it evidence of a build/transform tool's output (bundled, minified, autotools-generated)? → `build/`. Is it a project-hygiene fact? → the `metadata/package/` subdirectory for that subject (`documentation/`, `testing/`, `config/`, `logging/`, `error-handling/`) — there is no `quality/` bucket |
| `package/` | `well-known/lib/` | Package fields, scripts, testing or a dependency declaration → `package/`. Identity of the analyzed library/framework/runtime artifact → `well-known/lib/`. Embedded implementation evidence → its supported capability, not an artifact identity. `metadata/library/` is closed. |
| `package/` | `permission/` | Ordinary package fields/members → `package/`. Declared authority (permissions, host grants, OAuth scopes, content-script scope) → `permission/`. Invoking an API is a capability; mentioning its permission is not invocation. |
| `dependencies/manifest/<facet>/` | each other | See [Choosing a dependency-manifest facet](#choosing-a-dependency-manifest-facet) — the facets overlap on purpose (every declaration has a name, a source and a version), so they are ordered and the first match wins |
| `signed/` | `vendor/` | Is it about the cryptographic signature chain or entitlements? → `signed/`. Is it identifying an OS/platform vendor by strings/resources/patterns? → `vendor/` |
| `vendor/` | `well-known/app/`, `well-known/dual-use/`, or `well-known/tool/` | Is it an OS/platform vendor or system userland marker (Apple, Microsoft, NetBSD, GNU/FSF)? → `vendor/`. Is it a specific well-known application or suite? → `well-known/app/`. Is its legitimate abuse-relevant function the reason analysts need the identity? → `well-known/dual-use/`. Is it a professional analyst/admin/developer tool? → `well-known/tool/` |
| `vendor/` | `well-known/lib/` | Platform vendor that produced the file → `vendor/`. Identified third-party library/framework/runtime artifact → `well-known/lib/`. An embedded implementation fingerprint follows its technique; a vendor/library mention alone does not identify the whole file. |
| Interface indicators | artifact metadata | Distinctive interface names, paths, API references, and calls all support the capability in `micro-behaviors/network/interface/`. Their evidence strength affects confidence and the specificity of the description; it does not create another home under metadata. |
| `network/interface` | `hardware/wireless/network` | Generic adapters, interface addresses/status, and virtual or bridge interfaces belong in `network/interface`. Wi-Fi/Bluetooth radio discovery, wireless association, saved WLAN profiles, and wireless-specific client APIs belong in `hardware/wireless/network`; the wireless subject takes precedence even when an API enumerates adapters. Strings, library references, imports, and calls share the same technique home. Reading a saved WLAN profile alone is a neutral capability; credential access requires evidence for the secret-access inference. |
| `network/interface` | `os/network/route` | Adapter identity, address, and status queries or changes belong in `interface`. Reading, creating, deleting, or changing destination-to-next-hop routing entries belongs in `route`, whether evidence is a command or an OS API. A route lookup that also selects an interface remains route evidence; a separate adapter query remains interface evidence. |
| `os/network/route` | `os/network/neighbors` | IP destination-to-next-hop routes belong in `route`. Local IP-to-link neighbor mappings, ARP tables, and neighbor-cache queries or flushes belong in `neighbors`. A cache flush is neighbor-table management, not route-table modification. |
| `os/network/route` | `os/sysinfo/network` | A route-table operation or route selection belongs in `os/network/route`. A composite that characterizes the host by combining network configuration with adapter, wireless, or other host facts belongs in `os/sysinfo/network`. A queried domain-join status is host identity → `os/sysinfo/hostname`; querying directory contents or objects belongs in `os/security/directory-service`. |
| `network/interface` | `os/network/share` | Network adapters and their addresses belong in `interface`. Enumerating or mapping remote shares and drives belongs in `share`, even when the evidence comes from a shell command. |
| `network/interface` | `os/network/tunnel` | Generic adapter inventory, addresses, bridge and virtual-Ethernet references belong with interfaces. TUN/TAP packet endpoints, WinTun adapters, VPN-service builders and application selection, and configured tunnel interfaces belong in `os/network/tunnel`. These indicate probable tunnel-interface capability across operating systems; they do not require proof of live traffic or a particular implementation language. |
| `os/application/target` | `network/interface` | A package identifier cited as the application a program may select or target belongs in `os/application/target`, even when a VPN or another network feature consumes it. This records a reference to an app identity; it does not prove the app is installed or that an operation occurred. Interface-name references and adapter APIs belong in `network/interface`, because their probable capability concerns network interfaces. A package-manager API that queries, installs, or manages apps belongs under `os/package-manager/` instead. |
| Cloud credential and service clues | `metadata/file/string` vs the supported capability | Strings embedded in a file are content, not file metadata. Use the service, header, environment, path, or authentication-source home named in the communications tie-break above. Credential-access objectives combine these neutral capability clues with evidence that supports an intent inference. |
| `os/network/tunnel` | `communications/proxy/tunnel` | The OS tunnel branch owns virtual packet interfaces and their configuration. The proxy branch owns application/session forwarding, such as a public-service tunnel or a WebSocket-to-TCP bridge. A `/dev/net/tun` path or WinTun library reference follows the OS capability; a stream-forwarding API follows the proxy mechanism. Consumers may combine them without copying the atoms. |
| WLAN capability clues | independent provider identity | Library-name references and a `wlanapi.dll` basename can support probable wireless API capability in `micro-behaviors/hardware/wireless/network`. A stronger fingerprint identifying the independent provider artifact belongs in `well-known/lib/`. A filename alone must not gain verified-provider semantics or newly activate broad known-library suppressors merely through relocation. |

### Choosing a dependency-manifest facet

`metadata/package/dependencies/` first splits by **where the dependency fact was
read from** — `manifest/` (declared by the author), `lockfile/` (resolved by the
installer), `archive/` (present in the built artifact). Read the path as a
sentence: *a package's dependencies, as declared in its manifest, specifically
the …*

Under `manifest/`, one dependency entry satisfies several facets at once —
`"@img/sharp-linux-x64": "^0.33"` has an identity, a name shape, a source and a
version range. **The facets are therefore ordered, and the first one that
describes what the matcher actually reads wins.** Ask the questions in order:

1. **`identity/` — *which* package?** The matcher names one specific package
   (`lodash`, `axum`, `child_process`). Test: rename the trait after the package
   and nothing is lost. A trait that would stop working if the package were
   renamed belongs here.
2. **`name-form/` — what does the *name* look like?** The matcher reads the name
   as a pattern, not as a particular package: a `-linux-x64` platform triple, a
   `.js` suffix, a `lint`/`build` word. Test: it would match a package that does
   not exist yet.
3. **`source/` — where does it *resolve from*?** The matcher reads the
   right-hand side as a location: a protocol (`git+ssh:`, `file:`, `workspace:`,
   `catalog:`, `link:`, `portal:`, `github:`), a URL, a local path.
4. **`range/` — *which version*?** The matcher reads the same right-hand side as
   a version specifier: `*`, `latest`, `^1.2`. `source/` and `range/` both read
   that field; the split is **where to fetch** versus **which release**.
   `"pkg": "*"` is `range/`, `"pkg": "github:o/r"` is `source/`.
5. **`reconciliation/` — declared versus actually *used*?** The only facet
   allowed to read beyond the manifest: it compares the declaration against the
   imports in the shipped code. Everything phantom/unused-dependency lives here.
6. **`presence/` — is the field *there at all*?** Omitted, present, or an empty
   object. No entry is examined. `npm-no-dependencies-field` is presence.
7. **`count/` — *how many*?** The field is populated and the claim is
   cardinality. `npm-dependency-fanout` is count, not presence.

Two consequences worth stating, because both were live mistakes before the
split:

- **`identity/` is not `name-form/`.** One names a package; the other names a
  shape. `npm-dep-lodash` and `optional-native-linux-dep-name` look alike as
  trait ids and are not the same kind of fact.
- **A facet is not an ecosystem.** npm, Cargo and Gradle declarations of the
  same kind share a facet and are separated by *filename*
  (`identity/cargo.yaml`, `identity/npm.yaml`), per the technology-neutral
  directory rule above.


## Reference

### Trait ID Format

```
directory/path::trait-name
└─────┬──────┘  └────┬────┘
  directory      local ID
```

**Reference patterns:**
- `trait-name` — same directory (local)
- `micro-behaviors/communications/http` — any trait in directory
- `micro-behaviors/communications/http::curl-download` — exact match

### Composite Rules

Capabilities combine into objectives via composite rules:

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

### Example Classifications

| Code Pattern | Tier | Path | Criticality |
|--------------|------|------|-------------|
| `socket()` call | Capability | `micro-behaviors/communications/socket/create` | notable |
| `eval()` call | Capability | `micro-behaviors/process/interpreter/eval/direct` | notable |
| Process hollowing | Capability | `micro-behaviors/process/hollow` | suspicious |
| Screenshot API | Capability | `micro-behaviors/hardware/display/screenshot` | notable |
| Screenshot + timer + upload | Objective | `objectives/exfiltration/stealer/screen` | suspicious |
| Reverse shell pattern | Objective | `objectives/command-and-control/reverse-shell` | hostile |
| Cobalt Strike beacon | Known | `well-known/malware/rat/cobalt-strike` | hostile |

### MBC Identifiers

- **ATT&CK Techniques**: `T1234` or `T1234.001` (sub-technique)
- **MBC Behaviors**: `B0001` (behavior), `C0015` (micro-behavior)
- **MBC Enhanced**: `E1234` (ATT&CK technique with MBC enhancements)
