# cleave Taxonomy

A taxonomy with three behavioral tiers and a metadata tier, following [MBC (Malware Behavior Catalog)](https://github.com/MBCProject/mbc-markdown) principles.

## Tiers

| Tier | Purpose | Criticality Range | MBC Equivalent |
|------|---------|-------------------|----------------|
| **Capabilities** (`micro-behaviors/`) | Observable mechanics — what code *can do* | component → baseline → notable → suspicious | [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
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

The ML pipeline extracts features from **subdirectory path + criticality**, not individual trait IDs. Each trait's directory path (up to 3 levels deep), combined with its criticality level, becomes a feature dimension. This means:

- **Directory structure is the feature space.** A trait at `objectives/evasion/kernel-hide/rootkit/linux.yaml` with `crit: suspicious` generates the feature `evasion/kernel-hide/rootkit:suspicious`. The directory hierarchy directly shapes what the model learns.
- **Criticality is the signal strength.** Two traits in the same directory but at different criticality levels produce different features. A `suspicious` rootkit trait and a `component` rootkit trait are distinct signals.
- **Depth matters.** The pipeline uses up to 3 directory levels. Features aggregate at the deepest available level, so `evasion/kernel-hide/rootkit` is more specific than `evasion/kernel-hide`, which is more specific than `evasion`.

### Design implications for trait authors

- **Group related detections under the same subdirectory** so they aggregate into a single, strong feature. A directory with 10+ traits produces a robust signal; a directory with 1-2 traits produces a weak one.
- **Don't create single-trait subdirectories** when the trait fits an existing directory. `credential-access/browser/` (11 traits) is a strong feature; adding `credential-access/opera/` with 1 trait creates a weak feature that should instead be a file within `credential-access/browser/`.
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

- **Name the level the model can see.** The feature keeps three directory levels after the tier, so the segment that carries the distinction has to sit at or above level 3. A tree like `fs/path/sensitive/private-key/` puts the real discriminator at level 4, where it is aggregated away: every child of `sensitive/` — SSH keys, cookies, `/etc/passwd`, an iMessage database — collapses into the single feature `fs/path/sensitive`, teaching the model that reading someone's notes and reading their private key are the same event. Promote the discriminating axis instead (`fs/path/private-key/`, `fs/path/password-store/`), and express the secondary axis — *whose* credential it is — in the **filename** (`ssh.yaml`, `browser.yaml`), which costs nothing because filenames are never part of trait IDs. A grouping word that only re-states its parent (`sensitive/credentials/`) fails the precision test above *and* spends the last visible level; drop it and let the type take that slot.
- **The 3-level depth limit** means `objectives/anti-static/obfuscation/string/encoding/` extracts as `anti-static/obfuscation/string` — the `encoding/` level is aggregated into `string/`. Plan directory depth accordingly, and avoid unnecessary intermediate directories (e.g., prefer `obfuscation/syntax/` over `obfuscation/source/syntax/`).

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

### Directory Layout Convention

All tiers follow: `TIER/CATEGORY/BEHAVIOR/METHOD/platform.yaml`

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
reflection belong under the same technique regardless of whether evidence is
source text or compiled code. `micro-behaviors/data/source/` is a historical
mixed namespace, not a claim that source code is a kind of runtime data or a
valid new placement; do not add rules there. Migrate each existing rule to its
semantic subject rather than recreating `source/` as a taxonomy axis.

### Directory budgets and placement contracts

`make validate` enforces **one inclusive cap of 85 rules per directory**:
atomic `traits` plus `composite_rules`, across every YAML file in that directory.
There is no separate atomic cap and no directory exemption. All criticalities,
including `exception`, consume the budget. Descendant directories have their own
budgets; filenames do not create new namespaces or budgets.

For `micro-behaviors/` and `objectives/`, the validator permits **2–5 directory
levels below the tier**, excluding the filename. A fifth level is available for
a real refinement; it is not a target. The documented ML aggregation remains
three levels below the tier. Raising the authoring depth does not change the
extractor or make levels four and five separate features.

Before splitting a directory, audit its siblings and likely destinations. Route
misplaced atoms to their existing homes and consolidate equivalent rules first.
Every proposed parent needs a placement contract containing:

1. The one question answered by its children and the evidence required to enter it.
2. Each child's positive definition, exclusions, and nearest competing sibling.
3. A deterministic precedence rule when one matcher contains several facets.
4. At least one placement example and counterexample, with a canonical destination.

A child must be a proper refinement of its parent. Remove synonymous or empty
grouping levels; promote meaningful children when that brings the distinguishing
subject into the first three levels. Expand breadth for different mechanisms,
resources, or effects, not for alternate verbs, languages, APIs, or rule forms.
Keep the existing 150-child fan-out cap: broad identity catalogs should split by
a stable function, with an explicit primary-function tiebreaker.

Separate independent facts into canonical atoms and reference them from composites.
Do not duplicate a whole objective under every carrier, trigger, or ecosystem.
A composite lives with its most specific required behavioral result; optional
corroboration does not choose its directory. A rule that needs several children
but proves no narrower result needs an explicitly defined joint behavior, not a
`misc/`, `combined/`, or `behavioral/` overflow bucket.

The [directory contracts through level three](#directory-contracts-through-level-three)
are the placement guide. The [85-rule audit and migration plan](docs/taxonomy-audit/PLAN.md)
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

## Decision Framework

### Tier Selection

```
Specific malware, unwanted software, dual-use product, app, library, game, or tool signature; well known enough that at least 1 in 1000 developers or security engineers would recognize it?
  → well-known/

Attacker intent inferred from capability combinations?
  → objectives/

Single observable mechanic, no intent inference?
  → micro-behaviors/
     Rarely legitimate?     → suspicious
     Useful in differential analysis? → notable
     Universal baseline?      → baseline

Neutral file property (not behavioral)?
  → metadata/
```

### Text, Content, and Metadata Boundaries

The matcher type does not decide tier placement. A `type: text`, `string_literal`, `raw`, or `encoded` matcher still belongs where the thing it detects belongs:

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
| An argument vector starting an image (`execve`, `CreateProcess`, `posix_spawn`) | `exec` |
| Only an executable name, launch flag, agent permission, or import, without a creation mechanism | The corresponding path/configuration/import observation; not a second process-creation mechanism |

The table describes canonical ownership, not a claim that all existing leaves
already comply. `launch`, `direct`, `spawn`, `execv`, and `spawnv` must be reconciled
by these tests. The executable being launched does not override the mechanism.
A `Popen(..., shell=True)` matcher belongs in `shell`; a matcher for `Popen`
without that argument belongs in `subprocess`. An API's optional capabilities
are not evidence that a particular invocation uses them.

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

## Directory contracts through level three

**Count depth after the tier:** in `objectives/command-and-control/reverse-shell/pty`,
`command-and-control` is level 1, `reverse-shell` is level 2, and `pty` is level 3.
This section defines ownership at those levels. Levels four and five may refine
the claim, but may not change its subject or rescue a misplaced parent. The
authoring limit remains five for behavioral tiers; this documentation scope is
not a new three-level validation cap.

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

### Implementations and library fingerprints

**Classify implementation fingerprints by the supported technique whenever
possible.** Static linking, dynamic linking, vendoring, a runtime helper and a
handwritten implementation are evidence/implementation differences; they do not
create separate AES, HTTP, archive, string or process-creation techniques.
Keep language and backend in the filename, trait name and description.

| What the matcher establishes | Placement and description |
|---|---|
| Embedded AES tables or an AES-specific implementation signature | `micro-behaviors/crypto/symmetric/aes`, refined by the actual mechanism where needed; describe “contains an AES implementation,” not “encrypts files.” |
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
| `communications` | Exchanging data, addressing peers, or manipulating a communication protocol. Level 2 names the protocol or transport facility; level 3 names its operation/surface. | Interface configuration is `os/network`; passive file format facts are metadata; attacker control or theft needs an objective claim. |
| `crypto` | Cryptographic primitives, keys, derivation, hashes, and certificate operations. Children refine primitive family then algorithm/operation. | Encoding is `data/encode` or `decode`; randomness is `os/random`; certificate contents are `metadata/signed`; named-library identity is `well-known/lib`. |
| `data` | Transforming, interpreting, organizing, or operating on data. Children identify an operation and its algorithm/format/mechanism. | Mere data presence is metadata. Source location, language, or intended consumer is not a second transform. |
| `dylib` | Native shared-library loading, enumeration and loader lookup. Children identify the loader operation. | Language module loading is `os/module`; manual address resolution is `os/api-resolution`; a named API goes with its function. `dylib/library` is a legacy mixture: dependency facts use metadata, embedded capabilities use their techniques, independent library identities use well-known/lib. |
| `fs` | Filesystem objects, paths and operations. Children identify the resource or operation, then its mechanism or resource subtype. | File contents are classified by what they establish; a sensitive path literal does not prove theft. Raw hardware interaction is `hardware`. |
| `hardware` | Direct device access, input/output, capture, or control. Children name the device family then operation. | Querying host properties is `os/sysinfo`; manipulating windows/widgets is `ui`; ongoing surveillance needs collection evidence. |
| `mem` | Address-space allocation, access, protection, mapping and management. Children name the memory operation then its mechanism. | Cross-process execution transfer is not established by allocation/write alone. Compression remains `data` even when performed in memory. |
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
| `http/header`, `authorization-header`, `body`, `query` | Classify the particular field's meaning first: authentication → its auth subject; User-Agent → `user-agent`; cookies → `cookies`; otherwise use the HTTP surface. A raw header token does not prove a request or a login. |
| `http/oauth`, `device-code`, `token-auth`, `jwt`, `basic-auth`, `auth` | OAuth grant acquisition/refresh, including device authorization → `oauth`; presenting a bearer token → `token-auth`; JWT structure/processing → `jwt`; Basic credentials → `basic-auth`; `auth` only when the mechanism is not established. Mechanism-specific leaves take precedence. |
| `http/cookies`, `cookie-store`, `cookie-name` | HTTP cookie operations and protocol fields → `cookies`. A cookie-jar path → `fs/path/cookie`; credential/session extraction requires its own objective. Consolidate competing spellings by this distinction. |
| `http/services` vs a protocol operation | A named remote service endpoint without an operation → `services`; an operation tied to that endpoint → the operation's directory. A vendor CLI invocation is not automatically HTTP. |
| `communications/url` vs `http/url` or `http/query` | Generic URL construction/parsing/reference → `url/{construction,parse,reference}`; HTTP request parameter handling → `http/query`. Endpoint identity follows the service/resource it identifies. |
| `communications/ip` vs `os/network` | Address syntax, literal, construction, or parsing → `ip`; local interface/route/address configuration or queries → `os/network`. Active remote probing is not merely address parsing. |
| `dns/lookup`, `resolver`, `server` | Resolve a name → `lookup`; configure/select resolver infrastructure → `resolver`; receive/respond to DNS queries → `server`. A DNS label/domain literal alone does not prove any of these operations. |
| `communications/ipc` vs network messaging | Local process/host bridges, pipes, shared-memory messaging and native-host channels → `ipc`; remote messaging protocols → `messaging` or the named protocol. IRC is a network protocol, not IPC merely because it transmits messages. |
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
| `data/compress` vs `decompress` vs `archive` | Reducing a byte stream → compress; expanding it → decompress; accessing or creating a member container → archive. ZIP member extraction is `archive/extract`; using raw deflate is the corresponding compression direction. |
| `data/serialize` vs `parse` vs `format` | Object ↔ representation codecs (JSON, YAML, protobuf, pickle) → `serialize/<format>`; lexical/grammar/query interpretation → `parse/<grammar-or-operation>`; specialized format handling without a more specific operation → `format/<format>`. File format identity alone is metadata. |
| `data/string`, `buffer`, `control-flow`, historical `data/source` | String-value operation → string; byte/storage operation → buffer; execution-path construct → control-flow. Source code is the matcher’s evidence, not a subject: classify the operation/technique it establishes. AST parsing, inspection or mutation → planned `code/ast`; runtime reflection → planned `code/reflection`; code shape without an operation → `metadata/code`. Never choose a directory by source-vs-compiled representation or language; put those constraints in rule scope. |
| `code/ast` vs `data/parse` | Parsing or traversing a program AST, or constructing/mutating that AST → `code/ast`; parsing data formats/grammars unrelated to program structure → `data/parse` or `data/format`. JSON used to transport an AST does not by itself make the operation an AST technique. |
| `code/reflection` vs dynamic loading/evaluation | Discovering types/members or invoking them reflectively → `code/reflection`; loading a module or evaluating source/bytecode → the corresponding load/evaluation capability. A language-specific API matcher belongs in that neutral technique leaf with its language in `for:`. |
| Code-generation API vs code-generation library fingerprint | A call/construction that performs code or bytecode generation → `code/generation`; a reference to a framework specialized for that technique may also live there, but must say “reference” and must not assert generation occurred. A scan of the library artifact itself uses its `well-known/lib` identity. |
| `data/db/<engine>` vs operation children | Engine-specific protocol/API without a specific operation uses the engine; a required query/delete/schema/backup operation uses that operation, with engine in the filename. A targeted credential table adds a separate objective claim. |
| `crypto/library/blockchain` vs transaction and protocol operations | Cipher/signature/hash primitives → crypto; constructing, signing, submitting or querying a financial ledger transaction → planned `data/transaction/{construct,sign,submit,query}`. Generic RPC/HTTP remains communications; provider endpoint identity is not a transaction. |
| `crypto/symmetric/xor` vs `data/{encode,decode}/xor` | A required keyed cipher construction → crypto; representation scrambling/descrambling → data. A bare XOR instruction cannot establish either construction. |
| `fs/path/<resource>` vs all file operations | Merely naming a location → path by resource kind. Required read/write/copy/etc. → that operation, referencing the path atom where useful. A path match never inherits the consuming composite's action. |
| `fs/path/{password-store,cookie,private-key,public-key,token,secret-config,config}` | Choose the identified resource in that order of specificity, not its application owner: saved-login DB, cookie jar, private key, authorization/host-trust key, token file, secret-bearing config, then ordinary config. A file's defined role, not a generic credential word, determines the choice. |
| `fs/path/{personal,app-data,cache,font,library,log,metadata-store,system,temp}` | Classify the kind of resource named by the path, not the spelling of an ancestor directory. Browser history is personal; a profile or application-support/group-container path is app-data; cache is cache; an installed font path is font; `/lib` and `.dylib` references are shared-library paths; `/Library/Logs` is log; `.DS_Store` is a directory-metadata store; OSRecovery is a system path; temporary locations are temp. Thus `/Library/Caches` goes to cache and `/Library/OSRecovery` to system even though both contain the segment `Library`. |
| `fs/path` vs `fs/path-ops` | A path identifies a resource → `path/<resource>`; code joins, normalizes, parses or matches pathnames → `path-ops/{join,normalize,parse,match}`. Migrate `path/{construct,basename,check}` by operation; resource references stay in path. `Path.Combine` is join; `Path.GetDirectoryName` is parse/extract-parent. A bare method-name token is only an API fingerprint, not proof the method was called or that the surrounding behavior is malicious. Traversing the filesystem is directory/traverse, not pathname manipulation. |
| `fs/read`, `write`, `delete` vs `file/*` and `shell-ops` | Explicit content read/write/deletion uses the dedicated operation parent; create/open/copy/move/rename/stat use the corresponding `fs/file` operation. Shell/API spelling does not create another home. Reconcile `file/read-write` per actual evidence; keep a joint claim only if both operations are required. |
| `fs/directory`, `enumerate`, `traversal`, `search` | Listing one directory → `directory/readdir`; recursive descent → `directory/traverse`; indexed/predicate search → `search`; drive/device inventory → `enumerate` by resource. Directory deletion → `delete/directory`, rather than also directory/rmdir. A file extension being searched is not a traversal mechanism. |
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
| `process/fd`, `io`, `communications/ipc` | Descriptor duplication/control → fd; routing child streams → io; the pipe/channel itself → IPC. A reverse shell references these observations and adds outbound shell-I/O coupling. |
| `os/env` topics vs operations | Named variable meaning wins when required: CI-issued secret → `ci-credentials`, other secret name → `secret-name`, ordinary provider/runtime config → its topic. Variable-unspecified read/enumeration/modify/dump uses the operation leaf. Merge `check`/`gate` by value-test semantics. Never classify a secret as ordinary provider config solely by vendor prefix. |
| `os/registry/{read,write,delete,keys,hive}` vs `access`/`manipulate` | Required value read/write/delete wins; key/hive references alone use keys/hive. Split residual generic access by open/enumerate/watch/create semantics during migration. A Run-key write with durable activation is a persistence composite, not every registry write. |
| `os/service` operations vs `user-session`/`config` | Required create/start/stop/delete/query/configure/dispatch operation wins. A service definition field without an action remains a field/configuration fact. User versus system service scope is evidence, not a duplicate operation branch. |
| `os/autorun`, `time/schedule`, persistence | OS-managed task/autorun definition or registration → autorun; in-process timer/callback → time/schedule; durable unwanted reactivation → persistence by the trigger contract below. Task XML alone is not malicious installation. |
| `os/sysinfo`, `hardware`, discovery | Query hostname/OS/hardware properties → sysinfo; operate a device → hardware; required reconnaissance collection/target selection → discovery. A single vendor literal proves neither probing nor reconnaissance. |
| `os/privilege`, `security`, privilege escalation | Authority/token queries or ordinary changes → privilege/security; crossing to greater authority through abuse → privilege-escalation. `sudo` text or a requested-admin manifest alone is not that crossing. |
| `hardware/input`, `display`, collection | Device/event/capture API alone → hardware; required logging or surveillance behavior → collection. An empty error handler or arbitrary screen API is not screenshot theft. |

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
| `reverse-shell` | Outbound connection explicitly coupled to a shell session's input/output. | A listening/accepting shell → `backdoor/bind-shell`; individual command requests → `remote-command`; socket and shell symbols without their relationship are insufficient. |
| `backdoor/bind-shell` vs `backdoor/dispatch` | A listener that connects an accepted client to a shell → `bind-shell`. | Use `dispatch/<mechanism>` when the handler receives independent tasks and chooses an operation/command; remote access to a shell does not create a second dispatch classification. |
| `remote-command` | Receive attacker-directed tasks and dispatch operations or return command results. | A persistent connected shell uses reverse-shell; an HTTP server endpoint exposing command execution uses backdoor/webshell. Polling/HTTP/socket are channel facts, not parallel copies of dispatch. |
| `backdoor` | An unauthorized access/control surface, such as a bind listener, webshell or authentication bypass. | Generic task dispatch uses remote-command; durable installation adds a persistence claim; binary/script/native-source are not access mechanisms. |
| `beacon` | Repeated attacker check-in or heartbeat, without a narrower required tasking result. | An ordinary timer or telemetry endpoint is not a beacon; an actual dispatched task belongs with its tasking result. |
| `botnet` | Fleet membership/coordination or distributed operator tasking. | A network-device platform or DDoS action alone is not botnet coordination. |
| `channel` | A communication mechanism proven to carry attacker control, without a narrower access/dispatch claim. | Generic transport APIs are capabilities. Choose protocol/mechanism over vendor identity. |
| `dns` | DNS-mediated control retrieval or command-channel tunneling; `dga` for algorithmic rendezvous naming. | DNS carrying stolen values belongs in exfiltration; generic lookup is a capability. |
| `infrastructure` | An endpoint, configuration or rendezvous construction with a demonstrated C2 role. | Ordinary hosting/service endpoints and chosen labels alone do not establish C2. |
| `trigger` | An attacker activation condition: packet knock, message/content gate or local artifact gate. | Ordinary lifecycle/timer facts are capabilities/metadata; `activation` merely restates trigger. |
| `dropper` | Required acquisition/staging of a payload linked to its activation. | An installer identity, download, encoded blob or execution API alone does not establish this chain. |

Reverse-shell level-3 placement uses the **first required mechanism** below.
All rows still require the admission test above. Direction, transport and
encoding do not replace that evidence.

| Level-3 child | Required mechanism | Competing legacy paths |
|---|---|---|
| `dev-tcp` | Shell pseudo-device opens the connection and redirects shell I/O. | `/dev/tcp` sending HTTP alone goes to neutral communications. |
| `utility-relay` **planned** | External network utility owns the shell relay. | Extend/rename `netcat`; a utility banner alone is identity/capability. |
| `pty` | A pseudoterminal explicitly carries the connected session. | PTY allocation alone remains `process/tty/pty`. |
| `fd-redirect` **planned** | Socket installed as inherited standard descriptors. | Consolidate `dup` and the applicable `stdio` rules. |
| `stream-bridge` **planned** | Explicit read/write/copy loop joins socket and persistent child streams. | Redistribute `socket-exec`; per-command result loops use remote-command. |

`encoded` and `syscall` do not define alternative shell bridges. `http-poll`
does not establish a shell session without the required I/O relationship.
Retire those parallel classifications when migrating their rules.

Dropper level-3 children are **planned replacements** for the overlapping
`delivery`, `staging`, `execution`, and `behavior` partitions. Pick the first
required activation sink; reference source, concealment and trigger facts.

| Planned child | Required payload activation |
|---|---|
| `process-inject` | Transfer execution of the staged payload into another process. |
| `image-map` | Map/relocate a native image for execution in the current process. |
| `module-load` | Load staged code through a runtime module/assembly loader. |
| `script-eval` | Evaluate staged source in the running interpreter. |
| `interpreter-stdin` | Feed staged source through a new interpreter's stdin. |
| `file-exec` | Launch a staged file through a process or file-handler mechanism. |

The same remote encrypted assembly therefore has one chain home, `module-load`;
its encryption, network transport and install hook are referenced observations.
The neutral loader and any concealment objective retain their own canonical IDs.

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
| `impact/{destroy,wipe,ransom,degrade,dos,infect}` | Content destruction → destroy; overwrite/erase storage → wipe; coercive encryption/extortion → ransom; disable a capability → degrade; availability exhaustion → dos; insert replicating code into a host → infect. Read/write/encrypt APIs alone establish none of these outcomes. |

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
| Specific source plus its transmission | `exfiltration/stealer/<source>`; the source wins over HTTP/DNS/webhook transport, package carrier, and install/build trigger. |
| Required multi-source sweep plus transmission | `exfiltration/stealer/sweep`. An OR over alternate sources is not a required sweep. Optional second sources do not move a browser stealer here. |
| Exfiltration channel abuse without a narrower established source | `exfiltration/<transport>` by required transport mechanism; it still needs theft/unauthorized-transfer evidence. Neither HTTP POST nor an OAST domain alone meets admission. |
| Local hash/password recovery vs remote guessing | `credential-access/cracking` for local recovery; `lateral-movement/brute-force` for attempts to gain remote access. Service/protocol identity alone is not guessing. |
| Deceptive credential prompt vs its completed export | `credential-access/phishing` for the deception/relay; `exfiltration/stealer/phish` for captured-input-plus-send. The latter references the former, not a duplicate phishing matcher. |

For `stealer/<source>`, use the identified store before a broad storage medium:
wallet → wallet; browser-owned saved logins/cookies → browser; OS secret store
→ keychain; SSH material → ssh; cloud-provider stores → cloud; developer
credential files → dev-secret; process environment → env; app session tokens
not covered by those stores → token; other documents → file. Source-required
capture, mailbox, host profile, account DB, appliance config and network config
use the correspondingly named existing children. A specific source beats
`file`, `input`, or `system-info`; a mandatory joint profile/sweep must say so.

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
| Execution/persistence during a package lifecycle | Canonical execution/dropper/persistence outcome, referencing the hook fact and any separate trust-violation composite. | `install-hook` is not a second objective tree. Neutral declaration → `metadata/package/scripts/lifecycle`; actual package-manager operation → `micro-behaviors/os/package-manager`. |

For overlaps within supply-chain, required modification of an established
legitimate input/baseline wins (`trojanized`); otherwise required concealment
from package inspection wins (`hidden-payload`); otherwise required deceptive
selection/identity claims use `impersonation`. Dependency confusion through a
misleading registry identity is impersonation; rewriting a trusted dependency
configuration is trojanization. Each needs evidence of its particular trust
violation. Merely naming a dependency or containing encoded bytes is neither.

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
| `signed` | Signature/certificate/entitlement/trust facts. Under certificate choose the required role: planned `subject`, existing `issuer`, planned `timestamp` or `revocation`, then `signature` or `security` properties. Redistribute the mixed `identity` leaf by those roles. | Installing/verifying a certificate → crypto; vendor string without signature provenance → vendor/provenance; a timestamp authority or issuer does not establish the artifact's leaf signer. |
| `vendor` | OS/platform vendor provenance claims, refined by the claimed role or evidence surface. | Third-party product identity → well-known; certificate subject → signed/certificate; manifest vendor field → package/vendor. |

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
rewrite exact and directory references together. No YAML has moved merely
because this guide documents a better boundary.

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
│   ├── http/              #   HTTP/HTTPS (client, server, download)     C0002
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
│   │                      #   Neutral crypto primitives only.
│   │                      #   API hashing → objectives/anti-static/obfuscation/imports/.
│   │                      #   DPAPI credential decryption → objectives/credential-access/.
│   │                      #   PRNG → os/random/.
│   ├── symmetric/         #   Symmetric ciphers (AES, DES, XOR, RC4)   C0068
│   ├── asymmetric/        #   Asymmetric ciphers (RSA, ECC, Curve25519)
│   ├── hash/              #   Cryptographic hashes (SHA, MD5, Blake2b)  C0029
│   ├── kdf/               #   Key derivation functions                  C0028
│   ├── certificate/       #   Certificate ops (install, store, sign, verify)
│   └── library/           #   Legacy implementation partition; migrate by technique/group
│                          #   Embedded code → supported crypto capability; independent
│                          #   library artifact identity → well-known/lib/crypto/.
│                          #   Blockchain RPC/transaction operations are not crypto primitives.
│
├── code/                  # Code operations/techniques, language and filetype neutral
│   ├── ast/               #   Parse, inspect, traverse, build, or transform ASTs
│   ├── generation/        #   Generate or rewrite code/bytecode; technique-specific
│   └── reflection/        #   Runtime type/member discovery or reflective invocation
│                          #   Source-vs-compiled and language belong in rule scope/files.
│                          #   Add this branch with its validator whitelist and first
│                          #   audited migration; do not use it as a generic code bucket.

├── data/                  # Data transformation                 → MBC: Data
│   │                      #   Neutral data operations only.
│   │                      #   Shellcode/exploit payloads → objectives/evasion/ or execution/.
│   │                      #   Token extraction → objectives/credential-access/.
│   │                      #   Obfuscator detection → objectives/anti-static/.
│   │                      #   CVE-specific patterns → objectives/execution/exploit/.
│   │                      #   Malware family markers → well-known/.
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
│   ├── format/            #   Format handling not covered by a narrower operation
│   │                      #     File-level identification or header presence → metadata/file/format/
│   ├── embedded/          #   Embedded content/resource handling (certificates, EXIF, runtime)
│   ├── language/          #   Legacy: language presence → metadata/lang/natural/
│   ├── source/            #   CLOSED historical mixed namespace; classify by semantic subject
│   ├── string/            #   String length, search, comparison, conversion    C0019
│   ├── buffer/            #   Buffer operations (offset writes, reassembly)
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
│   #   NOT in metadata/. This includes the
│   #   neutral act of IMPORTING such a module (e.g. Python `import base64`
│   #   → data/encode/base64::import-base64, `import pickle` →
│   #   data/serialize/unsafe/python::import-pickle): the import is a
│   #   capability observation, kept at notable. metadata/ only records what a file IS
│   #   (e.g. "contains base64-looking strings"), never that code decodes.
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
├── os/                    # OS integration                      → MBC: Operating System
│   │                      #   OS-specific APIs that don't fit other top-level categories.
│   │                      #   Process ops → process/. File ops → fs/. Timing → time/.
│   │                      #   Persistence composites (crontab, registry Run keys) →
│   │                      #   objectives/persistence/.
│   ├── api-resolution/    #   API resolution (GetProcAddress, hash-based)
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
│   ├── network/           #   Network config (interfaces, status)
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
│   ├── controls/          #   Widget/control operations
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
│   │   │                      #   Planned canonical children; migration required.
│   │   │                      #   Existing delivery/staging/execution/behavior branches
│   │   │                      #   are reconciled by activation sink, not retained as aliases.
│   │   ├── process-inject/    #     Execute staged payload in another process
│   │   ├── image-map/         #     Map native staged image in the current process
│   │   ├── module-load/       #     Runtime module/assembly activation
│   │   ├── script-eval/       #     Evaluate source in the current interpreter
│   │   ├── interpreter-stdin/ #     Source streamed to a new interpreter
│   │   └── file-exec/         #     Launch a staged file
│   ├── infrastructure/        #   C2 infrastructure (domains, IPs, cloud)    B0030
│   │   ├── domain/            #     Domains, DGA, hosting
│   │   └── config/            #     C2 config patterns
│   ├── remote-command/        #   Command dispatch                           B0011
│   ├── reverse-shell/         #   Outbound connection coupled to shell I/O   B0030
│   │   ├── dev-tcp/           #     Shell pseudo-device connection/redirection
│   │   ├── utility-relay/     #     Planned: network utility owns relay (netcat successor)
│   │   ├── pty/               #     Pseudoterminal carries connected shell session
│   │   ├── fd-redirect/       #     Planned: inherited descriptor redirection (dup/stdio)
│   │   └── stream-bridge/     #     Planned: explicit socket/child-stream bridge
│   └── trigger/               #   Attacker activation gates, not ordinary lifecycle facts
│
├── collection/                # Information gathering (OB0003)
│   │                          #   "Identify and gather information, such as sensitive files"
│   │                          #   Generic capture mechanisms live here.
│   │                          #   Credential-specific stores → credential-access/.
│   │                          #   Financial data → credential-access/financial/.
│   ├── keylog/                #   Keystroke logging                       T1056.001
│   ├── clipboard/             #   Clipboard capture                       T1115
│   ├── screenshot/            #   Screen capture                          T1113
│   ├── archive/               #   Archive collected data                  T1560
│   ├── database/              #   Database enumeration/access             T1005
│   ├── email-harvest/         #   Email address harvesting                T1114
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
│   │                          #       that also SENDS → exfiltration/stealer/sweep/.
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
│   ├── system/                #   System information                      E1082
│   │   ├── fingerprint/       #     System/hardware/OS profiling
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
│   ├── process/               #   Process enumeration                     T1057
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
│       ├── browser/           #     Browser passwords, cookies, extension storage
│       ├── cloud/             #     Cloud credentials (~/.aws, IMDS, kubeconfig)
│       ├── dev-secret/        #     .npmrc, .git-credentials, .env files, CI secrets
│       ├── env/               #     Process environment secrets
│       ├── file/              #     Documents, disk sweeps, removable media
│       ├── input/             #     Keystrokes, form input, clipboard
│       ├── keychain/          #     OS secret stores (Keychain, DPAPI, libsecret)
│       ├── message/           #     SMS, mailboxes, chat history
│       ├── network-config/    #     Interfaces, routes, ARP, Wi-Fi profiles
│       ├── phish/             #     Credentials typed into a phishing form
│       ├── process-list/      #     Running-process inventory
│       ├── ssh/               #     SSH keys and host files
│       ├── surveillance/      #     Screenshots, camera, microphone
│       ├── sweep/             #     One stealer harvesting many of the above
│       ├── system-info/       #     Host profile (hostname, user, OS, hardware)
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
│   ├── ui/manipulation/       #   Screen locker / UI lockout
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

File-level properties with no behavioral implication. Describes *what a file is*, not *what it does*.

**Rules:**
- Behavioral detection belongs in `micro-behaviors/` or `objectives/` according to the evidence, not here
- Tool/malware signatures belong in `well-known/`, not here
- Supply-chain attack indicators belong in `objectives/supply-chain/` (organized by technique, not ecosystem)
- OS/platform vendor traits go under `vendor/`
- Identities of the analyzed app, dual-use product, tool, game, or library/framework/runtime artifact go under `well-known/{app,dual-use,tool,game,lib}/`. Embedded implementation fingerprints belong with their supported capabilities; dependency declarations and attribution alone remain metadata.
- **Distinguish a tool's *output* from the tool's *identity*.** "This code was bundled/minified/transpiled" is a build-transform fact → `metadata/build/<function>/` (group by function: `bundler/`, `minifier/`, `transpiler/`). "This file *is* webpack / PuTTY / Wireshark" is a named-software fingerprint → `well-known/`. Putting a software identity in `metadata/` is the same *matcher-defines-identity* violation as mislabeling a generic capability.
- **Avoid grab-bag directories.** A directory must name one coherent concept that is meaningful as an ML path feature. If a dir accretes unrelated kinds of traits — e.g. the former `package/tooling/` held build-output (`webpack-bundled`), software identities (`tool-identity-putty`), *and* project-hygiene facts (`has-eslint-config`) all at once — the path feature becomes noise and analysts can't reason about it. Split each kind to its proper home (`build/`, `well-known/`, and the `package/` subdirectory for the subject) and delete the grab-bag. Vague names (`tooling`, `context`, `misc`, `helpers`) are a smell that this has happened.

  The former `metadata/library/` tree held ~1,030 rules across ~68 directories and mixed several different concepts: library fingerprints that duplicated `well-known/lib/`, plain capability markers wearing a library's directory name, named offensive tools, CI fingerprints, and vague structural leaves. That migration is complete: `metadata/library/` is now closed and empty. Because a directory reference is an ML path feature, each migrated matcher was placed according to what it actually finds; never recreate the old bucket or move a whole directory on the strength of its name.
- New top-level subdirectories require updating both TAXONOMY.md and `ALLOWED_METADATA` in `src/capabilities/validation/directory_whitelist.rs`
- **Depth:** Prefer at most three levels below `metadata/` so the distinguishing subject remains ML-visible. This is a feature-design guideline, not the behavioral-tier validator's physical depth limit.
- **Max leaf size:** 85 rules per directory across all tiers, atomic traits and composite rules counted together (`policy/oversized-dir`); no directory exemptions
- **Max fan-out:** No directory should have more than 150 immediate subdirectories. Split by the parent's documented subject/function question; ecosystem or vendor grouping must not create a second home for the same claim.
- **Prefer technology-neutral subdirectory names.** Technology names belong in filenames, not directory names, unless the technology itself defines the subject. The 85-rule cap does not justify a language or platform split.
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
│   └── string/            #   Neutral string identities
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
# objectives/command-and-control/reverse-shell/combos.yaml
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
| Screenshot + timer + upload | Objective | `objectives/collection/screenshot` | suspicious |
| Reverse shell pattern | Objective | `objectives/command-and-control/reverse-shell` | hostile |
| Cobalt Strike beacon | Known | `well-known/malware/rat/cobalt-strike` | hostile |

### MBC Identifiers

- **ATT&CK Techniques**: `T1234` or `T1234.001` (sub-technique)
- **MBC Behaviors**: `B0001` (behavior), `C0015` (micro-behavior)
- **MBC Enhanced**: `E1234` (ATT&CK technique with MBC enhancements)
