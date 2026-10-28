# cleave Taxonomy

Where a trait goes, and why. Apply it mechanically: two authors — human or
model — reading the same matcher should choose the same directory without
knowing the sample, its reputation, its language, or the composite that
consumes it.

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

1. **Catalog observations, not specimens.** A sample yields many findings, each
   placed separately. Its reputation, its family, where its other rules live
   and spare directory capacity never choose a home.
2. **The matcher is the identity.** Name, description and directory describe
   what the matcher finds, not the consuming composite's intent
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
6. **Claim no more than the evidence.** A string, API reference, path or
   constant alone is a reference, not a capability. Bounded operation context
   or a validated structural pattern can support a *probable* capability;
   proof of execution is not required. The directory names the inferred
   capability; the description names the evidence. Never infer an algorithm,
   data flow, target or purpose the matcher lacks.
7. **Implementation is scope.** Language, platform, file type, backend, API
   spelling and matcher type go in `for:`, `platforms:`, the filename and the
   trait ID, not in directories — unless the platform *is* the technique
   (systemd, `LD_PRELOAD`, Winlogon).
8. **Shortest precise path.** Split only for a real distinction, never for
   symmetry, rule count or ML feature depth. Prefer breadth when siblings are
   equally exact.
9. **Criticality never fixes placement.** Fix a misleading classification by
   moving, renaming or tightening the rule, never by demoting it.
10. **Preserve detection.** Moves keep matchers and effective scope; detection
    fixes are separate, tested and recorded.

## Placement procedure

1. **Write the claim** the matcher supports in one sentence. For a composite,
   that is what its *required* evidence establishes.
2. **Choose the tier** ([Tiers](#tiers)).
3. **Choose level 1:** facility, objective, artifact subject or entity class.
4. **Apply the branch's boundary and ordered tests.** Required results beat
   incidental context.
5. **Stop at the most specific home the evidence supports.** Evidence lacking
   the algorithm, mechanism or subtype stays in the broad operation leaf
   (`crypto/encrypt`, `crypto/cipher`).
6. **Check the nearest competing leaf.** If both fit, add a deciding example and
   counterexample here first.

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
- **Co-occurrence is not data flow.** Unless the rule binds source to sink
  (same value, path or handle), describe it as co-occurrence.
- **One result per composite.** Split unrelated results; keep a joint rule only
  when the relationship is the observation. There is no `misc/`, `combined/` or
  `behavioral/` overflow.

## Tiers

| Tier | Holds | Does not claim | MBC analogue |
|---|---|---|---|
| `micro-behaviors/` | Probable capabilities, simple or compound | Malicious intent or observed execution | [Micro-behaviors](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
| `objectives/` | Attack claims that required evidence supports | That every constituent operation is malicious | [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions) |
| `metadata/` | Artifact structure, format, declarations, provenance, measurements | That declared behavior runs, or that provenance identifies a product | — |
| `well-known/` | Identity of recognized software or malware families | That a shared capability or dependency identifies the artifact | [Corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) |

**Choose in this order:**

1. The matcher shows the artifact *is* a specific, recognized product or
   malware family → `well-known/`.
2. Required evidence supports an attacker goal, unauthorized result or abuse
   mechanism → `objectives/`. One structured matcher can qualify (an AMSI
   patch); being common in malware cannot.
3. A probable capability with no attack claim → `micro-behaviors/`.
4. A property of the artifact → `metadata/`.

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
neutral capability stays neutral. An atom belongs in `objectives/` only if its
matcher alone establishes an attack claim, or it is a `component` fragment
meaningless outside that attack (Nemucod string pieces, default-credential
lists). RULES.md is stricter; see [open checkpoints](#open-checkpoints).

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

`component` and `baseline` are **not hidden**: JSON output, the web UI and
diffs show them. A demoted false positive stays visible, mislabeled, under the
wrong ML feature.

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

**A trait's name, description and directory must say what its matcher finds**,
at every criticality.

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
meaning. General validation does not enforce leaf-only placement; review the moved
parent and its descendants explicitly against this contract.

| Validator check | Limit |
|---|---|
| Rules per directory | **100** traits plus composites is the default maximum, summed over its YAML files and criticalities. A category-specific exception requires a complete relevance audit and explicit approval; filenames create no budgets. |
| Subdirectories | Hard error above 150 immediate subdirectories. Split broad catalogs by a stable function with a tiebreaker. |
| Depth | Soft warning beyond five levels below the tier (`objectives/a/b/c/d/e/f/x.yaml` warns). Soft warnings fail `make validate`; `cleave validate --soft` only reports them. |
| Sparse siblings | Soft warning when a parent has ten or more child directories averaging eight or fewer rules per child. Reports child count, total rules, and average rules per child; strict validation fails until the parent is reviewed. |
| Sibling stems | Soft warning on shared stems. A shared stem is not synonymy (account identity ≠ process accounting); document the boundary or merge. |
| Platforms | Soft warning at four or more. `platforms: [all]` only in `ALL_PLATFORM_DIRECTORY_ALLOWLIST` (same file). |

`platforms: [all]` is allowed only where a fact means the same on every OS:
`metadata/package/description/disclosure`,
`metadata/package/documentation/{claims,security-advisory,source}`,
`metadata/registry`, `metadata/filename`, `metadata/path`,
`metadata/file/profile/{test-indications,source-indications}` and
`micro-behaviors/communications/url/host` and
`objectives/supply-chain/security-hold`. Security-holding status is independent
of the target OS; its policy classifier does not assert code portability.
Naming properties record the scanned
filename or naming measurements; OS-specific path rules still require their
own explicit platform scopes. Test-indication profiles combine metadata and
directory observations; each child retains its OS/type gate, and the profile
asserts neither testing purpose nor software portability. Even there it
must be justified. Source-indication profiles are transparent ORs of named
source syntax, naming and declaration observations; their children retain all
OS/type gates, and the profile asserts neither execution nor benign intent.
An AUR package targets Linux, and source code alone does not
prove portability.

**Size prompts a semantic review; it never chooses a partition.** The 100-rule
maximum applies by default; category-specific exceptions require a complete
relevance audit and explicit user approval. Start with the parent and its
peers: identify the question at that level, move misplaced rules, and consolidate
equivalent matchers after comparing effective scope and conditions. Remove a
redundant level when it merely restates its parent or names the evidence carrier.
Only add children for distinctions the required evidence supports. Capacity,
language, backend, rule form and an `other` bucket never choose a home. A
complete placement of broad and narrow observations is required before moving.
Historical larger-budget reviews remain audit evidence, not active waivers.

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
not predicates or criticalities. Review every consumer when a directory moves:
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
| `process` | Execution contexts: creation, lifecycle, coordination, descriptors, interpreters, attach/hook/inject. | Privilege (`os/privilege`); durable activation (`objectives/persistence`). |
| `dylib` | Native library loading, unloading, enumeration, symbol lookup. | Language modules (`os/module`); manual API resolution (`os/api-resolution`). |
| `metaprogramming` | The program inspecting, generating or transforming program structure: `ast`, `generation`, `reflection/{inspect/{class,member},resolve,invoke}` *(legacy: `process/interpreter/reflection`)*. `generation` includes turning supplied source or an AST into an executable representation without requiring its invocation; reflection inspection reads class/type or member metadata, resolution finds members, and invocation calls a resolved member. | Running compiled/generated code (`process/interpreter/eval/constructed`); launching a compiler process (`process/create`); loading, defining or activating executable classes (`process/interpreter/runtime`); an AST the *analyzer* uses to match. |
| `os` | Host services without a more specific facility: registry, services, environment, accounts, privilege, security controls, kernel, packages, autorun, sysinfo, telemetry, clipboard, console. | File, process and network operations, even through an OS API. |
| `time` | Clocks, waits, elapsed time, in-process scheduling. | OS task registration (`os/autorun`, `os/service`); evasion gates (objectives). |
| `ui` | Presentation and interaction. | Display hardware or capture (`hardware/display`); deception (objectives); framework identity (`well-known/lib/ui`). |
| `browser-extension` | Extension-host surfaces with no neutral home: `action`, `lifecycle`, `management`, `tabs`; engine-emitted `host-access/<host>` and `permission/<perm>`. | Storage, messaging, HTTP, scheduling and injection keep their usual homes; manifest authority is `metadata/permission`. |

### Communications and local networking

| Home | Admission and boundary |
|---|---|
| `communications/<protocol>/<operation>` | DNS, FTP, TFTP, SSH, TLS, WebSocket, RPC, gRPC, email, messaging, IRC, MCP, ICS protocols (`modbus`, `dnp3`, `s7`, `bacnet`, `ethernet-ip`, `opcua`, `profinet`). Children are operations (connect, authenticate, send, receive, serve, configure). A vendor, SDK or client library is not a protocol. |
| `communications/http/{client,server}` | Method-unspecified client use; server-side handling. No `request` leaf duplicating `client`. |
| `communications/http/url/path` | HTTP URL path references, including literal API routes such as `/_api/...` or `/api/v2/chat/`. A route reference alone establishes neither a request, SDK identity, nor endpoint operation. |
| `communications/http/{get,post,put,patch,delete,head,options}` | A required method. |
| `communications/http/{download,upload}` | A response saved as an artifact (ordered retries in `download/fallback`); a file or attachment sent. GET alone is `get` and POST alone `post`; neither is upload, exfiltration or execution. |
| `communications/http/{header,cookies,auth,redirect,response,form}` | Classify a header by meaning: authentication → its auth leaf (`oauth` incl. device code, `token-auth`, `jwt`, `basic-auth`; `auth` when unknown), `user-agent`, `cookies`; otherwise `header`. A cookie-jar path is `fs/path/cookie`. |
| `communications/http/services/<provider>` | A named service endpoint with no operation; an operation goes to its own leaf. Cloud metadata: provider host or path → `services/<provider>/metadata`; headers such as `Metadata-Flavor` → `header/custom`. |
| `communications/socket/{create,connect,bind,listen,accept,send,receive,close,configure}` | Lifecycle and I/O. An operation beats a transport-only fact (`tcp`, `udp`); `dial`, `wrapper-connect` and `state-connect` are not operations. Hand-built HTTP over a socket is `http/direct-socket`. |
| `communications/tls/{initialize,verify}` | TLS apart from the application protocol: setup; peer verification (`verify/callback`; `verify/disable` only for explicit disabling). Setup is not a connection; a callback or suppressed warning does not disable verification. |
| `communications/ip/{literal,parse,construct}` | Address syntax, including private ranges and defanged notation. Address text proves no connection. |
| `communications/url/{parse,construction,host,scheme,path,query,user-info}` | Generic URL structure and endpoints. `http/url` facts that are generic URL syntax may live in sibling facets such as `http-path`, `http-query`, `http-scheme`, `http-encoded`, or in the construction facet's `http` and `url-fragment-http` children; HTTP endpoint, API-route and request-specific facts remain in `http/url`. Under `host`, `name` is for hostname identity or syntax independent of a callback role (domain references, suffixes, dynamic-DNS names, IDN form); `label` records the spelling or shape of individual hostname labels; `oob` is for recognized out-of-band callback services and callback-specific host patterns. When a host is known for its callback role, use `oob`, not `name`. Endpoint recognition alone does not establish contact, exfiltration, or hostile intent; behavior with an established transfer belongs under `objectives/exfiltration/oob`. `user-info` records the authority text before `@`, including hostname-shaped credentials; the destination hostname after `@` belongs under `host`. Neither establishes authentication or contact. Request parameters are `http/query`. A Wayback URL targets the archive, not its inner path. |
| `communications/ipc/<mechanism>` | Local channels: pipes, named pipes, Unix sockets, D-Bus, XPC, Binder, native-messaging hosts. Descriptor duplication is `process/fd`; shared-memory allocation is `mem`. IRC is a network protocol: `communications/irc` (*legacy: `ipc/irc`*). |
| `communications/messaging` | Send verbs shared across chat platforms. The platform's host is `http/services/<platform>`. |
| `communications/{proxy,capture,transfer,benchmark,flood}` | Relays (`proxy/socks` for SOCKS, `tunnel` to build an encapsulated channel, `relay` to forward over one), packet capture, protocol-neutral send wording, throughput tests, repeated sends. Attack traffic is an impact claim. |
| `network/interface` | Interface identity, address, configuration or state, including a distinctive name (`veth`, `docker0`) and MAC addresses. Wi-Fi and Bluetooth radios and WLAN profiles → `hardware/wireless`. |
| `network/{connections,route,neighbors,dns,forward,qos,tunnel,status,share}` *(legacy: `os/network/*`)* | Connection inventory, routes, ARP caches, resolver configuration, forwarding, traffic policy, OS tunnel interfaces (TUN/TAP, WinTun), connectivity, share mapping. DNS wire traffic stays `communications/dns`; application-level forwarding is `communications/proxy/tunnel`. |

`communications/http/request/{body,credentials}` is a legacy branch (see "No `request` leaf duplicating `client`"), and both are classified by **the item that enters the request**, in the `stealer` item vocabulary. `request/body/<item>`: `construction` (how a body is attached, naming no item), `credential`, `command-output`, `application-state` (keychains, wallets, browser stores, activity records), `file`, `environment` and `injection` (a body carrying shell-control or traversal syntax). `request/credentials/<origin>` answers *where does the credential come from?*: `file`, `environment`, `ci-credential` (matches `os/env/ci-credentials`), `literal` (embedded in code or a URL), `application-state`, and `unspecified-origin` for a generic secret-flow candidate that names none. An exception composite lives beside the rules it suppresses, not under the item it happens to mention.

Don't duplicate WebSocket under HTTP, or a client library under each HTTP verb.
A port literal is not a service, scan or authentication state.

Protocol configuration follows the configured facility, not its INI/JSON
carrier. `communications/irc/configure` admits a recognized IRC server-setting
structure containing a server and port; describe it as a declared endpoint,
not a connection. A custom variable named `%flserv` or `%flport` alone does not
establish that structure or role. Parsing a configuration file is a separate
data operation; recognizing its section syntax is format metadata. File-path
references keep their `fs/path` homes even inside protocol configuration.
The reviewed IRC children are `command` (protocol-command vocabulary or
construction) and `configure` (declared connection settings). Command text
does not establish endpoint settings, and endpoint settings do not establish
a command being sent.

`communications/http/client/initialize` records construction or opening of an
HTTP client or connection object without a required request method. An
`HttpURLConnection` cast beside `openConnection()` belongs here; a bound POST
method belongs in `http/post`, and an arbitrary `openConnection()` without an
HTTP receiver does not establish this subject. Opening the object does not
prove network transmission. Library spelling belongs in the ID and scope.

### Cryptography

**Operation beats presence.** An AES encryption call is `encrypt`; an AES
implementation signature (tables, S-box) is AES presence — two observations,
not one matcher copied. A direction-specific constructor goes with its
direction but claims initialization, not transformed bytes; imports and
constructors alone never map to MBC Encrypt Data.

| Home | Admission and boundary |
|---|---|
| `crypto/symmetric/<algorithm>`, `asymmetric/<algorithm>`, `hybrid` | Primitive or implementation presence with no narrower operation ("contains AES", not "encrypts files"). Refinements such as `aes/initialize` (non-directional constructor), `aes/ctr` and `aes/decrypt` stay until the operation leaves absorb them. `hybrid` is symmetric payload crypto plus asymmetric key wrapping. |
| `crypto/{encrypt,decrypt,sign,verify}` *(legacy: algorithm leaves such as `symmetric/aes/decrypt`, `asymmetric/{encrypt,signature}`)* | The operation, whether or not the algorithm is known. |
| `crypto/asymmetric/signature` | Public-key signature support with no required direction or named primitive. A known direction goes to `sign` or `verify`; a named primitive without a required operation stays in its presence home. Excludes MACs, key formats and the file’s own signature. |
| `crypto/cipher` | Cipher capability with no named algorithm or direction (a bare `Cipher`, Go GCM block-size errors). Record any known family in the rule. |
| `crypto/hash/{digest,hmac}` | Cryptographic digest or MAC, including implementation presence; CryptoAPI hashing is `digest`. `digest/<algorithm>` (`md5`, `sha1`, `sha2`, `sha3`, `blake`) holds rules whose matcher names the algorithm, whatever the language; `digest/unnamed-algorithm` holds evidence that names none (`createHash(alg)`, `ComputeHash`). A digest compared against an embedded value is `os/security/auth/digest-comparison`. Mining markers are not hashing: Stratum and proof-of-work references are `communications/blockchain/mining`. Noncryptographic checksums → `data/checksum` *(legacy: `crypto/hash/{crc32,fnv}`)*. |
| `crypto/kdf` | Key derivation, whether or not the algorithm is known (PBKDF2 parameters, salt). |
| `crypto/key/{generate,import,export,exchange,representation}` *(legacy: `asymmetric/key`, `asymmetric/ecdh`)* | Key lifecycle and representation. Bitcoin WIF is a key representation, not a mnemonic. |
| `crypto/certificate` | Parsing, validating, installing and storing certificates. The file's own signature is `metadata/signed`. |
| `crypto/provider` *(legacy: `crypto/native`, `crypto/library/{provider,cng,cryptoapi}`)* | Provider acquisition and release with no narrower operation; `CryptHashData` is hashing. No remainder bucket. |
| `crypto/mnemonic` | Seed-phrase wordlists, generation and validation. Not a KDF (BIP-39 separates them). A bare `self.wordlist` is `data/collection`. |

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
chain RPC → `communications/blockchain/client`; RPC endpoints with no operation
→ `communications/http/url/rpc`; wallet UI → `ui/controls/wallet`; wallet files
→ `fs/path/wallet`. Signing arbitrary messages is `crypto/sign`
*(legacy: `crypto/asymmetric/signature`)*.
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
| `data/{parse,serialize,format}/<format>` | Parsing input; object ↔ representation (JSON, YAML, protobuf, pickle; general record fields in `serialize/schema-object`, credential-shaped records in `serialize/schema-credential`); formatting (`format/string` for number text, `format/credentials` for token shapes). Format identity alone is metadata. |
| `data/archive/{create,extract,list,modify}` | Code that manipulates archives. A rule binding a member to its extracted file is `extract`, though it also writes. |
| `data/{string,buffer,collection,property}/<operation>` | Operations on strings, byte buffers, collections (DOM trees in `collection/dom`) and object members (`property/{access,assign,define,enumerate}`), classified by receiver and operation, not method name. |
| `data/{arithmetic,checksum,reassembly,transaction}` | Numeric and bitwise operations; noncryptographic integrity checks; reassembly; ledger transactions. |
| `data/db/<operation>`, `data/config/<operation>` | Database operations, engine in the filename: rows (`write/row` for INSERT, UPDATE, REPLACE; `delete/row` for DELETE, TRUNCATE) and schema (`schema/{introspection,relational,stored-code,delete}`, `DROP` being `delete`); `sql` holds legacy generic syntax. Configuration reads and writes; a configuration file path is `fs/path`. |
| `data/control-flow/{branch,loop,dispatch,error-handling,assert,return,sequence}` | Execution-path constructs. A method named `Run`, an indexed invocation or a computed call is `dispatch` until its receiver shows a launch. `dispatch` answers *how is the callee selected?*: `named` (a fixed name such as `Run` or `Create`), `computed` (a runtime expression: bracket access, a variable function, an indexed callback), `selector` (a `switch` or lookup on a command or decision value) and `indirect` (a machine-level pointer or register call). The first row that fits wins; a call through a computed name that is also a known launcher stays `computed` until its receiver shows a launch. |
| `data/{stream,embedded,llm}/<operation>` | Streams and recording; embedded resources; model inference and tool calls. Prompt text that overrides policy is `objectives/evasion/security-bypass/llm`. |

`data/source` is retired: its rules split by evidence form. Syntax manipulation goes
to `metaprogramming`, execution constructs to `data/control-flow`, artifact and
language facts to `metadata`. A function *defined* with a utility's name is not
a call to it.

`data/encoding/xor` records direction-neutral XOR scrambling structure. A
state-update/byte-XOR/store sequence fits even when the same loop can encode
and decode. A bare XOR instruction does not establish scrambling. Required
reconstruction context can establish decoding in a consuming rule; the atom
must not acquire a direction from its consumer.

### Files, memory and hardware

| Home | Admission and boundary |
|---|---|
| `fs/file/{create,open,close,move,rename,stat,io-mode}`; `fs/file/copy/{call,command,source-destination}` | File-object operations. Copy separates function calls, command syntax, and rules requiring source/destination context. Text/binary mode is `io-mode`; permission bits are `fs/chmod`; share and disposition flags are `open`. |
| `fs/read`, `fs/write`, `fs/delete/{file,directory}` | Content I/O; deletion by what is removed. A sensitive filename creates no second home. |
| `fs/directory/{create,readdir,traverse}`, `fs/search` | Create; list one directory; recurse; select by name, extension or content. `readdir/{native,command,language}` separates enumeration interfaces, shell commands and language forms. `search/{command,name,content,sensitive-file}` separates the selection predicate. A required predicate makes it `search` even when recursive. `fs/enumerate` is drive and device inventory only. |
| `fs/path/<resource>` | A location, classified by **what it points at**, not its owner or an ancestor's name (`/Library/Caches` is `cache`). For secrets, the first that fits: `password-store`, `cookie`, `private-key`, `public-key` (authorized_keys, known_hosts), `token`, `secret-config`, `config`; a generic secret directory (`/run/secrets`) or cross-family union is `credential`. Others: `wallet`, `account-db`, `certificate`, `app-data`, `personal`, `cache`, `font`, `library`, `log`, `metadata-store`, `system`, `temp`, `socket`, `stream`, `extension`, `application/{bundle,browser,executable}`. A path never proves access. |
| `fs/path-ops` | Pathname manipulation: join, normalize, parse and match remain distinct trait IDs (`Path.Combine`, `realpath`, `GetDirectoryName`). |
| `fs/{acl,attributes,chmod,chown,link,lock,sync,watch,quota}` | Permissions, attributes, ownership, links (`hardlink`, `symlink`, `junction`), file locks (not `.lock` names), sync, change monitoring, quotas. |
| `fs/temp/{file,directory}`, `fs/volume`, `fs/disk/{partition,raw}` | Creating temporary objects (a temp *location* is `fs/path/temp`); mounts; partitions and raw disk. Disk inventory is `os/sysinfo/disk`. |
| `fs/swap/{on,off}` | Activating or disabling swap. Storage-header initialization (`mkswap`) belongs in `fs/volume/format`; raw zeroing remains `fs/disk/raw` until required evidence establishes formatting. |
| `mem/{alloc,free,resize,copy,fill,compare}` | Allocate, release (`HeapFree`), resize (`HeapReAlloc`), copy, fill, compare. |
| `mem/{map,unmap}`, `mem/create`, `mem/anonymous/create` | Mappings (`mremap` is `map`, not proof of a size change); shared and image-section objects; anonymous file descriptors (`memfd_create` proves no execution from it). |
| `mem/{read,write,protect,query,advise,lock,gc,sync}` | Access (local, remote or physical, when established), permissions, inspection, advice, pinning, GC, cache visibility. RWX alone is neutral; writing to another process transfers no execution. |
| `mem/combined` | Composites needing one alternative across memory operations. |
| `mem/{heap-spray,stack-pivot,overflow}` | The required spray layout, stack redirection or out-of-bounds write; allocation, stack access or an unsafe API alone is not enough (MBC C0006, C0009, C0010). |
| `hardware/{input,display,block,flash,gpu,wireless,smartcard,serial,iokit}/<operation>` | Device I/O and control. Input: `event`, `device`, keyboard `hook`/`listener`/`poll`/`layout`/`simulate`, mouse `position`/`simulate`, and `media` for audio-or-video interfaces (`getUserMedia`). A generic window hook is `ui/window/hook`. |

### Process, OS, time and UI

| Home | Admission and boundary |
|---|---|
| `process/create/<mechanism>` | Creating an execution context; see [process creation](#process-creation). |
| `process/thread/{lifecycle,enumerate,group,priority,config,terminate}`, `process/fiber/<operation>` | Thread or fiber management apart from creation; a fiber is not a thread. |
| `process/sync/{mutex,semaphore,event,critical-section,join}` | Coordination between execution contexts; memory visibility is `mem/sync`. |
| `process/work/{queue,pool,task}` *(legacy: `process/threading/queue`)* | Queue and pool management; task submission, completion, waiting, cancellation and future/result access (`QueueUserWorkItem`, `dispatch_async`). These do not establish thread creation. Joining a thread is `process/sync/join`; timer callbacks are `time/schedule`. |
| `process/{identity,info,enumerate,argument,resources,pid}` | Current identity; attributes (`info/name` for a process-name literal); listing; arguments; limits; PID files (a PID value is not one). |
| `process/{exit,terminate,control,daemonize}` | Ending this process (`exit/handler` for exit callbacks); killing another (a signal API without the kill signal is not); other state changes; detaching (`fork`+`setsid`). |
| `process/lifecycle/<operation>` | Lifecycle; a guard blocking a second instance (mutex, PID file, lock) is `single-instance` (MBC B0024), while a mutex alone is `process/sync/mutex`. |
| `process/debug/tool-markers` | References to debugging or tracing tooling, including executable names and paths. A reference proves neither a running debugger, a tool-owned artifact, nor an anti-analysis check; those require independent operation and target evidence. |
| `process/fd/{query,control,close,dup,stdio}` | Descriptor operations, including child standard-stream configuration, redirection, and descriptor duplication. Creating an IPC pipe is `communications/ipc`. |
| `process/io/stream/<operation>` | Reading, writing, piping, or relaying stream data, including paired relays between a peer stream and child stdin/stdout. This is the data-movement operation; stdio configuration and descriptor setup or duplication remain under `process/fd`. |
| `process/tty/<operation>` | Terminal interaction and PTYs. |
| `process/interpreter/<operation>` | In-process execution: `eval/{direct,indirect,constructed,source}` plus `bof` (Beacon Object File host APIs), `wasm`, and `vm`. `eval` executes supplied code in an existing interpreter. Launching an interpreter is `process/create`; compilation without required invocation is `metaprogramming/generation`; language identity is metadata. |
| `process/{attach,debug,hook,inject}/<mechanism>` | Attaching, debugging, intercepting and transferring execution, with no established attacker purpose. |
| `process/deploy/<sink>` | Neutral acquisition- or staging-to-activation chains (an updater fetching and launching its image), by the [payload sinks](#payload-activation-and-staging). |
| `dylib/{load,unload,lookup,enumerate}` | Native loader operations. Language modules are `os/module`; export walking or API hashing is `os/api-resolution`; hiding import identity is an anti-static claim. |
| `os/registry/<operation>` | A value read, write or delete beats key or hive references (`keys`, `hive`). Value-name and value-type references belong in `value-name` and `value-type`; they prove neither access nor activation. Only a Run-key write with durable activation is persistence. |
| `os/service/<operation>` | `create`, `start`, `stop`, `delete`, `configure`, `query`, `dispatch` (running as a service), `control` (no verb). A definition field alone is configuration; user or system scope is evidence, not a branch. |
| `os/env/<subject>`, `os/env/<operation>` | The first required meaning wins: CI-issued credential (`ci-credentials`) → other credential (`secret-name`, e.g. `AWS_SECRET_ACCESS_KEY`) → interpreter or loader configuration (`runtime`: `BASH_ENV`, `NODE_OPTIONS`) → filesystem location (`path`; *legacy: `user-paths`*) → CI job metadata (`cicd`) → user identity (`user-info`) → service configuration (`provider`). Otherwise use the operation: `read`, `enumerate` (*legacy: `enumeration`, `dump`*), `write` (*legacy: `modify`*), `test` (*legacy: `check`, `gate`*). A name is a reference, not a read; reading a secret is not theft. |
| `os/{user,group,privilege,security}/<operation>` | Principals and authority; security controls (`security/auth`, `security/jailbreak`). Crossing to higher authority is an objective. |
| `os/kernel/<facility>`, `os/{syscall,bpf,container,virtualization}` | Kernel facilities (`kernel/driver` for driver installation and loading, MBC C0037/C0023, not ordinary service creation; *legacy: `os/service/driver`*); direct syscalls; BPF; namespaces (`container/namespace`) and container runtimes; hypervisors. |
| `os/module/load`; `os/{api-resolution,linker}` | Language-module loading; manual API resolution; dynamic-linker configuration (`linker/{audit,env,load-path,symbol-version}`). Ruby `require` caches a module; `Kernel.load` evaluates the source file on each call. Native libraries belong under `dylib`. |
| `os/autorun`, `os/package-manager`, `os/sysinfo/<property>`, `os/random`, `os/telemetry` | OS task and autorun registration (malicious durability is persistence); package operations, including package-manager configuration under `os/package-manager/config`; host properties (`hostname`, `platform`, `hardware`, `disk`, `locale`, `profile`); randomness; logging and analytics. |
| `os/{clipboard,console,event,signal,exception,message,com,wmi}` | Host facilities. Clipboard by operation: `read`, `write`, `monitor`. COM or WMI evidence with a known function goes to that function. |
| `os/application/shell-namespace` | Operating-system shell item namespace operations, including virtual items as well as filesystem objects. PIDL manipulation belongs here; resolving a concrete filesystem path belongs in `fs/path`, and an icon drawing operation in `ui/graphics/icon`. A single shell-item API is an observation, not proof of filesystem mutation. |
| `os/application/target/<function>` | An app or package cited as the program's target (wallet brands, `SpringBoard`); neither discovery nor the file's identity. Children classify the referenced product's function, not the reference's spelling or encoding. |
| `time/{query,sleep,timing,schedule}` | Read time; wait; measure elapsed time (`timing/check`); schedule in-process callbacks (`schedule/timeout` for alarms). |
| `ui/{controls,dialog,graphics,help,menu,terminal,wallpaper,window}` | Credential-entry controls (`controls/credential`), wallet UI (`controls/wallet`), drag-and-drop interaction (`controls/drag-drop`), prompts (`dialog/prompt`), `--help` text (`help`), window hooks, enumeration and notifications. Deceptive hiding is evasion. |

`os/application/target` asks **what function does the referenced software serve?**
All children record references, not installation, use, discovery, or ownership.
Use the narrowest function required by every passing alternative:

| Child | Admission and boundary |
|---|---|
| `wallet` | Wallet products, their stores, registered wallet-extension IDs, or catalogs confined to wallets. Wallets take precedence over the broader financial-services class; a bare exchange/payment-service name is `finance`. |
| `finance` | Exchanges, payment services and DeFi protocols without required wallet identity. Stripe fits; a MetaMask extension ID is `wallet`. |
| `browser` | Browser products and browser toolbars. Brave fits; a required Brave Wallet extension ID is `wallet`, and a media-player ActiveX control is `media`. |
| `security` | Defender, bot-defense and CAPTCHA products. A named security product fits; a rival malware/campaign name is `malware`. |
| `agent` | Named AI-agent products and agent packages. Hermes and OpenClaw fit; a generic word such as "agent" does not identify a product. |
| `system` | Platform application stores, platform services and desktop-shell components. Finder and Play Services fit; a browser name is `browser`. |
| `network` | Communication clients, VPN clients and remote-session applications. Discord, OpenVPN and LiveDesk fit; a server implementation is `server`. |
| `cloud` | Cloud-platform and infrastructure-provider names. GCP fits; a named bot-defense product is `security`. |
| `server` | Named application/web-server implementations. Tomcat and nginx fit; an HTTP method or generic server API is a protocol capability. |
| `media` | Media-player products and their controls. RealPlayer fits; BaiduBar is `browser`. |
| `game` | Game products and their platform controls. Ourgame's GLWorld control fits; an ordinary media player is `media`. |
| `utility` | Standalone diagnostic or administration tools without a narrower required product class. CPU-Z and wmiexec fit; an app-store identifier is `system`. |
| `malware` | Rival malware or campaign names cited as targets. TeamPCP fits; this reference never identifies the analyzed file as that malware. |

The broadest current observations are multi-product references confined to one
function, such as wallet catalogs. A future observation spanning functions must
resolve its full population and a supported broad home before admission; it
must not be copied into several children. The placement inventory and unchanged
definition checks are recorded in
`taxonomy-migration/batches/stranded-target-functions/`.

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
resource belongs in `naming/resource`. These are vocabulary observations,
not proof that the named operation ran.

`process/interpreter/eval/` answers one question: **how does supplied code begin
executing inside an existing interpreter?** Admission requires execution, not a
compiler name, source-shaped string, constructor reference, or code object that
is merely produced. Its children are:

| Child | Definition and boundary | Example | Counterexample |
|---|---|---|---|
| `direct` | A recognized evaluator consumes source, a form or an expression directly. Input provenance stays in the trait name. | `eval(decoded)`; Python `exec(code)`; shell `eval "$cmd"`. | `compile(source, ..., "exec")` produces a code object but does not run it. |
| `indirect` | The evaluator is reached through an alias, global/member lookup, callback, bridge or other computed dispatch. The matcher must still establish evaluator semantics. | `(0, eval)(code)`; passing `eval` as a promise callback. | Calling an arbitrary variable or computed member is `data/control-flow/dispatch`. |
| `constructed` | Required evidence both creates or obtains an executable unit and invokes that unit. | `new Function(body)()`; `exec(compile(source, ...))`; `ScriptBlock.Create(text).Invoke()`. | `new Function(body)`, `ScriptBlock.Create(text)` and Lua `load(text)` without invocation are `metaprogramming/generation`. |
| `source` | A file is evaluated in the current interpreter context rather than launched as a child. | shell `source file`; PowerShell `& "file.ps1"`. | Node `Module._compile` is `os/module/load`; `bash file` creates an interpreter process. |

Precedence is `source` for a required file, then `constructed` when creation and
invocation are both required, then `indirect` when dispatch obscures or reroutes
the evaluator, otherwise `direct`. A decoder, decryptor, HTTP response or object
field does not create another child: those facts qualify the input, not the
execution mechanism.

Within `metaprogramming/generation`, runtime compilation answers a different
question: **does the program turn supplied program text or structure into an
executable representation?** It includes Python `compile`, JavaScript
`Function`, PowerShell `ScriptBlock.Create`, expression-tree `Compile`, and
similar callable/code-object construction. It excludes execution-only APIs,
compiler/toolchain identity, external compiler process creation, module loading,
and quoted compiler wording. Generation is the existing broader operation—it
already includes JIT and C# compilation—and remains one leaf while the combined
catalog fits the default 100-rule budget and one-operation contract.

#### Process creation

`process/create/<mechanism>` is an ML feature; finish "creates an execution
context by ___". **The first matching row wins:**

| The matcher shows | Directory |
|---|---|
| A thread in the current process | `thread` |
| A fiber | `fiber` |
| A clone of the current process | `fork` |
| A new shell parsing command text (`sh -c`, `cmd /c`, `shell=True`, a pipeline, `bash "$f"`, `%COMSPEC% /c`) | `shell` |
| A new interpreter handed source text (`node -e`, `python -c`) | `eval` |
| A Windows Script Host execution or script-moniker API | `process/interpreter/wsh` |
| A library object standing for the child (`Popen`, `NSTask`, `ProcessBuilder`) | `subprocess` |
| The desktop opener choosing the handler (`ShellExecute`, `open`, `NSWorkspace`) | `shellexec` |

`process/thread/{create,config,lifecycle,terminate,enumerate,priority,runtime}`
records one thread operation per child. Synchronization remains under
`process/sync`; scheduled work remains under `process/work`.
| An API starting an image from an argument vector or command line (`execve`, `CreateProcess`, `posix_spawn`, `WinExec`, `WshShell.Run` with an executable path) | `exec` |
| Only an executable name, launch flag, permission or import | Its path, configuration or import observation, not process creation |

An explicit shell argument beats the wrapper. An API's optional features are no
evidence that this call uses them, and the launched executable does not change
the mechanism. Under `shell`, pick one command-form axis (interactive session,
command text, script file, pipeline).

`process/inject/remote-thread` records remote-thread APIs and their accompanying
remote-memory preparation. It does not require a DLL payload: allocation,
writing and `CreateRemoteThread` references fit; allocating and writing without
an execution-transfer API do not. `process/inject/dll` needs DLL-loading
evidence. Neither an API profile nor a JVM interface declaration proves that a
particular buffer became the thread's entry point. Imported method references
and declarations remain distinct evidence.

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
| `collection` | `keylog`, `clipboard`, `screenshot`, `audio`, `camera`, `touch`, `messaging`, `email` *(legacy: `email-harvest`)*, `network`, `app-data`, `database`, `file-targeting`, `file-copy`, `archive`, `monitor`, `activity`, `multi-source` | Targeted acquisition or staging **without** a required send. Credentials → `credential-access`; reconnaissance → `discovery`; source plus send → `exfiltration`. `network` means captured traffic. |
| `credential-access` | By source: `browser`, `cloud`, `credential-manager`, `keychain`, `env`, `files`, `ssh`, `wallet`, `email`, `messaging`, `dev-tools`, `wifi`, `registry` *(legacy: `windows-registry`)*, `memory`; by acquisition: `capture`, `cracking`, `phishing`, `theft`, `validation` | Acquiring authentication material or a targeted secret store, by the [credential-source order](#objective-boundaries). Source-specific distinctions such as provider, smartcard, system and store live beneath their store family; validation and session reuse live beneath `validation`. |
| `discovery` | `account`, `host`, `system`, `network`, `process`, `cloud` | A reconnaissance survey, by surveyed resource: `host` = installed software, security products, browsers; `system` = machine, hardware, OS; `process` = running processes; `network` = interfaces, peers, probes, scans; `account` = principals; `cloud` = provider resources. One generic query stays a capability. |
| `command-and-control` | `channel/<transport>`, `beacon`, `remote-command/<dispatch>`, `backdoor/<access-surface>`, `reverse-shell/<io-coupling>`, `botnet`, `infrastructure`, `dns`, `trigger` | Attacker control, tasking, access or communication. Payload delivery is [execution](#payload-activation-and-staging); a protocol name is not C2. |
| `execution` | `payload/<sink>` *(legacy: `command-and-control/dropper/<sink>`)*, `staging/<operation>` *(legacy: `command-and-control/dropper/staging/<carrier>`)*, `exploit`, `interpreter`, `lolbin`, `lure`, `trigger`, `database`, `activex`, `automation`, `compile`, `lnk`, `wmi`, `autoinstall` | Unwanted execution through an exploit, deceptive invocation, trusted execution surface or admitted payload chain. Generic execution APIs stay in `process`. `database` is database-hosted execution (CLR procedures, `xp_cmdshell`, OLE Automation). |
| `exfiltration` | `stealer/<item>`; transport-only: `http`, `dns`, `ftp`, `cloud`, `messaging`, `llm`, `oob`, `side-channel` | Unauthorized transfer. An acquisition-to-send chain is classified by its stolen item and beats transport; a transport child needs an established theft claim whose item kind is not established. A POST, an endpoint or ordinary model inference is not exfiltration. Header, query and body are distinct HTTP carriers. |
| `evasion` | `anti-av/<control>`, `security-bypass/<control>`, `masquerade/<deception>`, `decoy`, `file-hiding`, `kernel-hide`, `indicator-removal/<record>`, `self-delete`, `process/<concealment>`, `fileless`, `hijack-execution-flow`, `hosts-file`, `quarantine-removal`, `tcc-manipulation`, `file-unlock` | Hiding activity from users, admins or deployed security products, or bypassing their controls. |
| `impact` | `destroy/<resource>`, `wipe`, `ransom`, `dos`, `degrade/<target>`, `infect/<host-artifact>`, `crypto-manipulation`, `cryptojacking`, `deface`, `services`, `system`, `ui`, `spam` *(legacy: `lateral-movement/social-engineering/spam`)* | Destruction, disruption, extortion, unauthorized modification or resource abuse. Ordinary deletion or encryption is neutral; spam needs unsolicited-message abuse, not volume. |
| `lateral-movement` | `exploit/<remote-surface>`, `brute-force/<service>`, `pass-the-hash`, `smb/<mechanism>`, `ssh`, `worm`, `usb-worm`, `delivery/<mechanism>`, `social-engineering` | Reaching or spreading to **another** system. A mechanism-specific exploit or credential reuse beats a generic protocol home. Scanning is discovery; local cracking is `credential-access/cracking`; infecting local files is `impact/infect`. Delivery subcategories require evidence of remote propagation; neutral WMI or process execution stays under `execution` or `micro-behaviors`. |
| `persistence` | `login/<surface>`, `system/<surface>`, `firmware/<surface>` | Durable, unwanted reactivation, [by trigger](#persistence-follows-the-trigger). |
| `privilege-escalation` | `exploit/<boundary>`, `elevation-control/<bypass>`, `token-manipulation`, `hijack-execution-flow/<surface>`, `modify-service`, `kernel-modules`, `install-certificate`, `process-injection` | A required crossing to greater authority. A privileged API, requested permission, `sudo` text or injection alone is not one. |
| `supply-chain` | `impersonation/<deception>`, `trojanized/<trusted-input>`, `hidden-payload/<inspection-evasion>`, `security-hold` | Abuse of component selection, distribution, or build and update trust; [package scope is not enough](#supply-chain-trust). `security-hold` is the explicit classification-policy exception below. |

### Objective boundaries

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
| `dns` | DNS tasking, check-in or tunneling; DGA. | A DoH endpoint or lookup (`micro-behaviors/communications/dns`). |
| `infrastructure` | Endpoints or rendezvous with a demonstrated C2 role. | Ordinary hosting and chosen labels. |
| `trigger` | Attacker activation conditions: packet knock, content gate, local artifact gate. | Ordinary lifecycle or timer facts. |

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

### Payload activation and staging

A payload chain needs **acquisition or staging linked to activation**, plus
admission. Admitted chains go in `execution/payload/<sink>`; the same chain in
an ordinary updater goes in `micro-behaviors/process/deploy/<sink>`. Choose
**one** sink; reference source, concealment and trigger facts.

| Sink | Required activation |
|---|---|
| `process-inject` | Execution moved into another process (`hollow`, `remote-thread`, `thread-hijack`). |
| `image-map` | A native image mapped for execution in this process. |
| `module-load` | Staged code loaded by a module or assembly loader (`Assembly.Load`, `AppDomain.AssemblyResolve`, `Module._compile`, dynamic `require`, WASM instantiation of staged bytes). |
| `script-eval` | Staged source evaluated by an interpreter (`eval`, `new Function`, `iex`, or explicit inline evaluation such as `node -e`). The child-process launch is supporting evidence; no staged executable file is implied. |
| `interpreter-stdin` | Staged source piped to a new interpreter. |
| `file-exec` | A staged file launched via `command` (a shell parses the launch), `spawn` (a process API launches the path) or `installer` (an installer transaction such as `msiexec`). |

`file-exec` is split by launch mechanism: `command/*` (a shell or script host parses the launch), `spawn/*` (a process API launches the path; `native` for compiled images, `runtime` for language runtimes), `detached` (hidden or background launch), `installer/*` (an installer transaction; `package` rules read the installer file, `invocation` rules read whatever launches it) and `shellcode`. Each matcher and description must retain the launch mechanism.

`image-map` and `interpreter-stdin` are not in the target sink set
([open checkpoint](#open-checkpoints)).

**The link is the claim.** A download, URL, encoded blob, execution API,
installer identity or loader-like name alone is not a payload chain: bind the
bytes or path to the sink, or keep the parts as neutral capabilities. Script,
HTA, WSH, MSI and package formats are carriers, not sinks. `regsvr32 /i:` with
`scrobj` is `execution/lolbin/regsvr32`. An auto-open document trigger with a
process call but no linked payload is `execution/trigger`.

**Staging without activation** needs executable-payload preparation plus
admission. Partition by operation, in precedence order: `reconstruct`
(synthesis or decoding) → `extract` (an embedded or container member) →
`acquire` (external fetch) → `store` (placement), as
`execution/staging/<operation>`. The carrier (archive, encrypted blob, stub,
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

| Required exported item | Home beneath `stealer` |
|---|---|
| Authentication material whose exported form is unknown, or alternatives spanning values and whole authentication records | `credential` |
| Selected secret values whose kind is unknown, or alternatives spanning secret kinds | `credential/value` |
| A selected password, protected password/verifier field or pre-shared authentication password | `credential/value/password` |
| A selected bearer, API, OAuth or application session token | `credential/value/token` |
| A selected cryptographic secret/private key | `credential/value/key` |
| A mnemonic, seed phrase or recovery secret | `credential/value/recovery-secret` |
| A stored authentication database, cache, keyring or credential-record set exported as a record/container | `credential/record` |
| Configuration files or settings, without a required extracted secret type | `configuration` |
| A broad process-environment snapshot, or environment values without a required credential type | `configuration/environment` |
| Application storage/profile state with its content type left open | `application-state` |
| Cookie state, without assuming every cookie authenticates a session | `application-state/cookie` |
| Browsing/history/activity records | `activity` |
| Captured input values, keystroke/touch records or clipboard content without narrower semantic content | `input` |
| Media content: static images, sound or ordered visual streams, with modality in the trait ID and description | `media` |
| Payment-card and associated billing data | `financial/payment-card` |
| Messages, mailboxes, SMS | `message` |
| A database dump or row set without a narrower required semantic item | `database` |
| Files whose contents have no narrower required item class | `file` |
| Host report: identifiers / OS and runtime / installed software / running processes / network inventory | `system-info/{identity,platform,software,process,network}` |
| Host report spanning or leaving open several of those | `system-info/profile` |
| Workspace/repository metadata report | `system-info/workspace-profile` |
| Two or more independent item families, **each required** | `multi-item` |
| Theft established, but alternatives or untyped content proves no narrower item family | `stealer` itself |

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
scope. Retained access without reactivation (created accounts, authorized SSH
keys, now in `login/{account,ssh}`) is an [open checkpoint](#open-checkpoints).

### Supply-chain trust

**Security-hold classification policy.** `security-hold` classifies a recognized
security-held package as `hostile`, including an inert npm replacement or a
vendored copy. This is an explicit exception to the usual requirement for
artifact evidence of an attack. The finding describes security-holding status,
not payload execution. An npm manifest must carry both `0.0.1-security` and the
canonical npm security-holder repository in that same manifest; an authoritative
registry record may instead supply its security-hold flag or holder description.
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

| Level 1 | Level 2 (level 3 refines it) | Boundary |
|---|---|---|
| `arch` | Instruction-set or ABI target, by family | Parsed target fields (ELF `e_machine`); a word such as `mips64` in `.rodata` identifies nothing. Header-field validity is `binary/header`. |
| `binary` | `header`, `section`, `symbols`, `code`, `instruction`, `resource`, `linking`, `layout`, `debug`, `provenance`; a property of that part | **Facts about a part, never what it means:** "three imports" → `symbols`; "imports `GetProcAddress`" → a capability; "exports impersonate `version.dll`" → an objective; "exports are libcurl's ABI" → `well-known/lib`. A part's measurement and malformation share its directory; `crit:` says how unusual. |
| `build` | `bundler`, `minifier`, `transpiler`, `generated`, `ci`, `config`, `manifest`, `artifact`, `reproducible`, `vcs`, … by transform or pipeline function | What a tool left in the file (bundled, minified, transpiled), grouped by function; the tool goes in the trait name (`esbuild-bundled`). "This file *is* webpack" is `well-known/`; compiler attribution is `lang/compiler`. |
| `document` | `pdf`, `office`, `rtf`, `html`, `ole`, `chm`; a parsed part or property | Structure, not the behavior of embedded code. Magic alone is `file`. |
| `filename` | `identity`, `name-form`: own basename and stem | A property of the scanned name, without parent-directory context. An embedded or referenced name belongs to its own subject. |
| `path` | Own scanned location and directory relationships | Parent components, source-tree location and multi-component paths. A path mentioned in code is `micro-behaviors/fs/path`; an archive table entry is `archive/member/path`. |
| `archive` | Container facets and member fields (below) | Properties of the scanned container or its recorded entries; code operating on archives is a capability. |
| `file` | `format`, `magic`, `extension`, `size`, `encoding` (*legacy: `encoded`*), `entropy`, `profile`, `line`, `catalog`, `comment`, `function`, `import`, `padding`; remaining whole-file properties | This legacy umbrella grants no default home: a specific subject beats a generic text bucket. `file/string` and `file/literal` are **closed**: move each rule to the subject it evidences. A context-only literal has no standalone behavior home; retain its placement hold until a supported contract or validated consumer representation exists. The validator rejects new IDs in both namespaces; existing IDs are grandfathered during migration. See the [validator enforcement record](taxonomy-migration/research/document-authority/literal-validator-enforcement.md). |
| `hardening` | `build`, `layout`, `memory`, `mitigation`, `sandbox` | Absence is a value of a mitigation, not a "missing" subject. Using a security API is a capability; bypassing one, an objective. |
| `image` | `pixel`, `segment`, `trailing`: decoded-image measurements, segment totals, trailing layout | Whole-file byte entropy is `file/entropy`. A metric name proves no color channel or end marker. Rendering and capture are capabilities. |
| `font`, `media` | *Reserved:* font table and container validity; cross-carrier byte coverage | Whitelisted; create with the first supported rule. |
| `import` | `builtin`, `module` (source-local named modules), `package`, `framework`; engine-emitted `<lang>/<module>` nodes | A dependency reference, not library identity or proof of use. `import base64` supports both directions, so it is an import fact, not `data/decode`. |
| `lang` | `source`, `compiled`, `scripted`, `compiler`, `runtime`, `version`, `encoding` (*legacy: `encoded`*), `natural`, `locale`, `generated`, `upstream` | "Built with compiler X" is here; "this file *is* compiler X" is `well-known/`. Code transformation is `build`; runtime reflection is `metaprogramming`. Engine-emitted `metadata/lang/embedded::<language>` marks detected source inside a containing file; it does not say that source ran. |
| `package` | A manifest field or package role (below) | Properties of the distributed component, not its runtime behavior. |
| `permission` | Declared authority by protected surface (`host`, `clipboard`, `storage`, `network`, …); grant scope and manifest-level profiles combining declared authority or target scope | A hostname without grant context is not a permission; a grant or target profile does not prove API use, injection, interception or theft. Invoking an API is a capability. |
| `registry` | Package-registry publication records: release history, reach, custody, listing claims | Not the Windows registry (`micro-behaviors/os/registry`). Reputation is not a verdict. |
| `signed` | `certificate`, `entitlements`, `platform`, `script`, `trust-level` | A signer name is neither product identity nor proof of a valid chain. |
| `vendor` | OS or platform vendor provenance (Apple, Microsoft, NetBSD, GNU) | Certificate fields are `signed`; manifest vendor fields are `package`; third-party products are `well-known/`. |

`metadata/file/encoding` is split by observable transform family: `base64`,
`hex`, `xor`, `url`, `escape`, and `compression`; `container` records an
encoding or armor represented by a format wrapper, and `shape` records
encoding-like structure without a supported scheme claim. `metadata/lang/encoding`
uses `base64`, `hex`, `xor`, `url`, `unicode-escape`, `wide`, and `shape` for
the same distinctions in source representation. These children describe the
observed representation; they do not assert a decoder call, concealment, or
execution.

Text shaped like `require('../common')` or `function test()` does not alone
establish a package test-harness role. The rule combining those alternative
source forms belongs in `metadata/lang/source/shape`; a single call form belongs
in `metadata/lang/source/syntax/call`, outside broad `metadata/package/testing`
selectors. An actual module-loading call belongs
under `micro-behaviors/os/module`; a corroborated test-harness role belongs
under `metadata/package/testing`. Preserve explicit consumers when relocating
weak source context rather than granting every test exclusion that context.
`metadata/file/system-info/field-name` records file-content references to
system-information field names, including words in compiled artifacts. A name
alone does not establish source code, a structured record, or information
collection; a required source construct belongs in `metadata/lang/source`.

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

**Source syntax.** `metadata/lang/source/syntax` asks **which grammatical construct is present?**
Its children require the construct's source form; a text or literal matcher
may observe embedded code, examples or comments. These observations establish
neither execution nor the capability suggested by an identifier. Language,
API and parser remain scope and filenames, not children.

| Child | Required property | Boundary and deciding example |
|---|---|---|
| `assignment/{name,member,call,value}` | Assignment syntax, grouped by the required target or, when no target is required, the assigned value. | Use `member` for member or indexed targets, `call` for call-shaped targets, `name` when a target name is required without a more specific target form, and `value` when the target is unconstrained. A required `const`, function or type declaration goes to `source/declaration`; a mapping entry goes to `key-value`. |
| `call` | A call-shaped expression, its arguments, or bounded relationships between calls. | `fetch(a.url, b.options)`, `send({...})`, and an end handler near `eval(` fit. A bare `EventDispatcher` name goes to `source/naming`; parentheses must be required for a call claim. |
| `command` | Command words, options, operands or pipelines in command text or an argument list. | `git log --patch` and `install -D` fit. A parenthesized method invocation goes to `call`; a bare cmdlet name goes to `source/naming`. |
| `directive` | Source-processing directives, event annotations or named language sections. | ASP.NET `<%@ Page ... %>`, MIDL `cpp_quote`, `@event timer.action`, and YARA `strings:` fit. A type or rule declaration introducing a name goes to `source/declaration`; an ordinary mapping key goes to `key-value`. |
| `key-value` | A named key/value entry or markup attribute, including the value's source form. | `"command": "..."`, `pattern: /.../`, and an HTML `href="...?q=..."` fit. `obj.command` goes to `member`; assignment to a standalone variable goes to `assignment`. |
| `member` | A qualified name, member selection, subscripted member, or template field reference. | `Net::HTTP`, `exports.KNOWN_C2_DOMAINS`, `obj['a' + 'b']`, and `{{.Field}}` fit. If invocation parentheses are required, use `call`; a field's initializer belongs in `key-value`. |
| `operator` | An operator or cast relates expressions or a value and a type. | A function-pointer cast and a comparison against an epoch constant fit. A function-pointer declaration belongs in `source/declaration`; a large numeric call argument belongs in `call`. |
| `type-expression` | A source expression naming a type, with no required value being cast. | PowerShell `[char[]]` fits; a required `-as [type]` cast belongs in `operator`. |

**Choose by the required relationship, then its operands.** A declaration
introducing a binding or type goes to `source/declaration`; an assignment
without that declaration evidence stays in `syntax/assignment`. A field entry
beats an incidental member name in its value. For expressions, required
assignment beats a nested call, a call/argument relationship beats incidental
member access, and a cast/comparison beats its operand's spelling. A shell
command's words and options belong together in `command`, even when serialized
as an argument array. An API name alone never acquires call semantics.

Within `lang/natural`, `vocabulary` describes words or token sets; `phrasing`
describes multiword clauses and their stated relationships, such as an action
paired with omission of review. A clause alone does not establish an agent
directive or prove that its described action ran.

Use the existing neighboring subjects when no single syntax construct is the
claim: `source/naming` for identifier vocabulary and function-name populations,
`source/literal` for array values or the contents and line shape of literals,
and `source/origin` for a source layer's carrier or extraction provenance.
`source/shape` holds source-context profiles spanning constructs, declarations
or source-file evidence: the Delphi/YARA source signatures, Haxe basename or
package declaration, frontend member-or-hook literal profile, scanner schema
exception, source-catalog label and encoding-related source profile. A single
assignment does not become a whole-source profile because it is counted.

The [source syntax move inventory](docs/taxonomy-audit/taxonomy/source-syntax-placement/migration.json)
places all 101 former direct rules. The audit found no identical effective
definitions to consolidate. Matchers, defaults, scope, criticality and explicit
dependencies are preserved. The two PHP-panel directory exclusions use the
shared `source/shape::source-syntax-known-benign-context` profile to retain
their original observation set, including relocated observations. Its PHP scope
matches those consumers; it follows the existing named exclusion-group
convention and retains `component` criticality for source context alone.

Raw signed-entitlement keys are emitted as runtime facts under
`metadata/entitlement/<category>::<key>`. The rules in
`metadata/signed/entitlements` interpret those facts into named properties;
the raw entitlement IDs are engine output, not duplicate YAML declarations.

`metadata/file/format/console-font` holds console-font format signatures and
fragment-manifest structure. A matched header prefix alone does not establish
whole-file validity. The reserved `metadata/font` home is for font-table or
cross-carrier properties, not a duplicate format identity.

**`metadata/file/profile` holds static, file-scoped measurements and
relationships.** A profile must state one stable, testable claim, the relation
among its evidence, and its file scope. It needs benign controls and near
misses. It does not establish runtime behavior, malware or product identity,
intent, or benign purpose. Same-file co-occurrence alone is not a profile, and
this directory is not a fallback for evidence without a defensible claim. This
contract is reviewed through rule review and focused fixtures; general Cleave
validation does not establish that a profile's semantics are sound.

**Archive boundaries follow the observed property.** Member names and member
table observations belong in `archive`, even when the name is a hash,
lure, extension or signing-file label. The scanned file's own basename belongs
in `filename`; an extension-only observation belongs in `file/extension`.
Parsed container-kind declarations (cabinet, Phar) belong in `file/format`,
signature bytes in `file/magic`, and bytes specifically in a PE resource in
`binary/resource`. Phar signature presence and scheme belong in
`signed/trust-level`; they establish neither signature validity nor a trusted
publisher. A member called `BNDLTOOL.RSA` remains a member-name observation.

The live profile children have distinct jobs: `field-presence` records whether
a parsed field exists; `function-population`, `identifier-population`,
`operator-population`, `string-population`, and `token-population` measure
defined populations. Operator populations count parsed source operators; they
do not establish execution or a purpose for those operators.
The remaining children are:
`installer-layout` records file and sidecar relationships; `markup` records
parsed markup or document-content patterns; `structured` records an explicit
relationship among structured fields; `source-indications` and
`test-indications` record source or test-context clues, not execution;
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
source escape syntax belongs in `metadata/lang/encoded/unicode-escape`, and an
isolated escape does not establish table or non-prose context. `file/catalog/service`
records service-name references and embedded
service configuration markers; a name mention does not establish service use,
while a provisioning composite must include the relevant configuration and
behavior evidence. `file/catalog/identity` describes reference catalogs found
inside the analyzed file; it does not identify the analyzed file as a product,
which belongs in `well-known/`. `file/comment` records parsed comment spans and file-shape metrics;
comment text is not executable code or a verified claim. `file/function` holds
source declarations and names; names do not prove calls. Function-population
metrics belong in `file/profile/function-population`; binary method anatomy
belongs in `binary`. `file/import` records parser-reported import counts;
named module references belong in `metadata/import`, and neither proves use.
`file/padding` requires an observed filler span, not a whitespace ratio.
`file/arithmetic` is retired: parsed operator populations belong in
`file/profile/operator-population`; actual arithmetic operations belong in
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
remain in `syntax/call/arguments`. A bare `dumps(metrics)` beside a JSON-looking
filename does not establish JSON serialization. Counts of recovered string
candidates belong in `file/profile/string-population`, not a source-literal
catalog.

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

1. `identity` — the manifest declares one specific package (`lodash`); renaming
   the name changes the trait. This records the declaration, not proof that the
   artifact implements that package.
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
| Leaf signer distinguished-name fields | `signed/certificate/subject` | Product identity |
| Issuer distinguished-name text | `signed/certificate/issuer/name` | That the named authority issued it |
| Exact verified-chain thumbprint of a Microsoft code-signing CA | `signed/certificate/issuer/microsoft` | Microsoft authorship when the CA attests third parties |
| Exact thumbprint of a Microsoft third-party component CA | `signed/certificate/issuer/attestation` | Microsoft platform provenance |
| Presence, length or shape of chain entries | `signed/certificate/issuer/chain` | Any authority's identity |
| Verification, digest integrity, nested signatures | `signed/certificate/signature` | Signer identity |
| EKU, key usage, other constraints | `signed/certificate/security` | That the signature verifies |

**Script-signature markers** belong in `signed/script`. A `SIG` begin/end
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
| `signed` vs `vendor` | Signature chain or entitlements → `signed`; vendor identified by strings or resources → `vendor`. |

Engine-emitted IDs (imports, permissions, signers, browser-extension host
grants) keep their producer schema. Reference them; never shadow them with YAML
copies or move them without an engine change.

## Known entities: `well-known/`

An identity catalog, not a second behavior tree: a directory here says the
analyzed artifact **is** that named thing. Depth is usually
class/function/entity; skip the function level when it adds nothing.

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
rules still require a meaningful size bound.

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
plan.

### Migration map

*Staged*: a reviewed batch in `taxonomy-migration/batches/`, not yet applied.
*Partial*: some rules moved. *Open*: no batch.

| Legacy home | Target home | How rules move | Status |
|---|---|---|---|
| mb `os/network/{forward,neighbors,qos,route}` | mb `network/<same>` | Same subject | Applied |
| mb `os/network/{connections,dns,share,status,tunnel}` | mb `network/<same>` | Same subject | Applied |
| mb `os/network/mac_address`; `webextension` | mb `network/interface`; mb `communications/proxy/config` | MAC addresses are interface identity; WebExtension rules configure browser proxies | Applied |
| mb `communications/ipc/irc` | mb `communications/irc/{command,handler}` | IRC is a network protocol | Applied |
| mb `communications/http/url/*` (generic URL facts) | mb `communications/url/<facet>` | Generic syntax to URL facets; HTTP endpoint, API-route and request facts stay | Partial (construction, path, query, scheme, encoded, host/domain/port/TLD, fragment, external-IP and navigation batches moved; API-specific and transport-specific leaves remain) |
| mb `crypto/symmetric/<alg>/{decrypt,…}`, `crypto/asymmetric/{encrypt,signature}` | mb `crypto/{encrypt,decrypt,sign,verify}` | Operations move; presence stays | encrypt and decrypt staged (B086, B087); sign and verify open |
| mb `crypto/native`, `crypto/library/{provider,cng,cryptoapi}` | mb `crypto/provider` | Operations go to their own leaves | Applied (provider and CryptoAPI rules moved) |
| mb `crypto/library/*` (other children) | Primitive family, operation, `data/transaction`, `communications/blockchain`, `crypto/key` | By claim | Partial (blockchain moved; other library buckets remain) |
| mb `crypto/asymmetric/{key,ecdh}` | mb `crypto/key/{generate,import,export,exchange,representation}` | By key operation | Partial (ecdh → exchange; Apple key-generation and representation-export imports → their operations; wallet and library name references → source naming; other key evidence remains) |
| mb `crypto/hash/{crc32,fnv}` | mb `data/checksum` | Noncryptographic | Applied |
| mb `data/source/*` | mb `metaprogramming/*`, `data/control-flow/*`, `data/property/*`; meta `*` | By claim | Applied (source syntax and naming, metadata, reflection, control flow and property operations routed by claim; no YAML rules or live YAML references remain under `data/source`) |
| mb `data/encoded` | meta `file/encoding` or mb `data/decode/<scheme>` | Presence vs operation | Applied |
| mb `data/decode/{request,reflection,environment,native}-base64` | mb `data/decode/base64` | Origin is not an algorithm | Applied |
| mb `fs/shell-ops` | mb `fs/{read,write,delete/*,file/*}`, `ui`, `os/application/shell-namespace`, or meta `binary/symbols` | By evidenced subject; an unspecified Shell32 file operation is a symbol reference | Applied (all 42 rules and references moved; the legacy directory has no YAML; see [migration inventory](docs/taxonomy-audit/taxonomy/shell-subjects/migration.json)) |
| mb `fs/traversal`; `fs/enumerate` (non-inventory) | mb `fs/directory/traverse`; `fs/directory/readdir`, `fs/search` | Inventory stays in `fs/enumerate` | Applied (traversal, directory listing, and permission search moved; volume/device inventory remains) |
| mb `fs/directory/mkdir` | mb `fs/directory/create` | Rename | Applied |
| mb `fs/memory/mmap`, `mem/alloc/map` | mb `mem/map` | Any backing | Applied |
| mb `mem/c-runtime/functions`, `mem/alloc/{executable,heap,managed,…}` | mb `mem/{alloc,free,resize,copy,fill,compare}` | By operation; allocator only when established | Partial (C-runtime allocation → `alloc/heap`; PowerShell `Marshal.Copy` → `copy`; remaining allocator buckets need claim review) |
| mb `mem/decompress` | mb `data/decompress/<algorithm>` | A data transform | Applied (no rules remain under `mem/decompress`; algorithm rules are in `data/decompress`) |
| mb `process/threading/*` | mb `process/{thread,sync,work}`; IPC to `communications/ipc` | `queue` → `work`; locks → `sync`; thread creation/concurrency → `thread` | Applied |
| mb `process/fork` | mb `process/create/fork` | Duplicate | Applied |
| mb `process/user` | mb `process/identity` or `os/user` | Current process vs principal administration | Partial (user queries moved to `process/identity/query`) |
| mb `process/create/{launch,direct,spawn,execv,spawnv,stdlib,wrapper,…}` | mb `process/create/<mechanism>` | [Process creation](#process-creation) | Open |
| mb `process/interpreter/reflection` | mb `metaprogramming/reflection` | Code as code | Applied |
| mb `process/script` | The actual execution mechanism (`process/interpreter/wsh` for WSH) | A carrier is not a mechanism | Applied |
| mb `os/env/{enumeration,dump}`, `modify`, `{check,gate}`, `user-paths` | mb `os/env/{enumerate,write,test,path}` | Other topic leaves move to the subject they require | Partial (mapped operation categories applied) |
| mb `os/service/driver` | mb `os/kernel/driver` | Drivers are not services | Applied |
| mb `dylib/library`, `ui/framework` | meta, a capability, or `well-known/lib`, by claim | Implementation containers | Partial (`usb_init` export → `metadata/binary/symbols/exports`; libm imports → `metadata/binary/symbols/imports`; other library observations remain) |
| obj `command-and-control/dropper/{process-inject,image-map,module-load,script-eval,interpreter-stdin,file-exec}` | obj `execution/payload/<sink>` (admitted) or mb `process/deploy/<sink>` (neutral) | By sink; admission picks the tier | Partial (`file-exec` applied: 639 rules in `command/{batch,script-host-download,script-host-embedded,shell}`, `detached`, `installer/{package,invocation}`, `shellcode`, `spawn/{native,runtime}`; the legacy directory is removed; other sinks open) |
| obj `command-and-control/dropper/staging/*`, `staging-xor`, `staged-loader` | obj `execution/staging/{reconstruct,extract,acquire,store}` | By operation | Open |
| obj `command-and-control/dropper/*` (`delivery`, `execution`, `behavior` and the rest) | A payload sink, staging operation, C2 result or neutral capability | By claim | Open |
| obj `collection/email-harvest` | obj `collection/email` | Rename | Applied (legacy directory and references are absent) |
| obj `credential-access/windows-registry` | obj `credential-access/registry` | Rename | Applied |
| obj `credential-access/{dump,theft,validation}` | obj `credential-access/<source or acquisition>` (`memory`, `files`, `credential-manager`, `capture`, `validation`, …) | Dump is not memory; source and acquisition distinguish below the approved families | Applied (process and image dumps → memory; other leaves routed by source/acquisition) |
| obj `evasion/process/injection` (mechanics only) | mb `process/inject/<mechanism>` | Rules showing concealment stay | Open |
| obj `lateral-movement/social-engineering/spam` | obj `impact/spam` | An impact | Applied |
| obj `lateral-movement/delivery` | `delivery/{remote-execution,wmi,gpo,update-service}`; `smb/admin-share` | By the remote mechanism and required effect | Partial (these mechanism-specific batches moved; multi-stage/multi-method remain under review) |
| obj `exfiltration/stealer/{network-config,process-list}` | obj `stealer/system-info/{network,process}` | Same source | Applied (legacy directories absent; target branches populated) |
| obj `exfiltration/stealer/{surveillance,phish}` | obj `stealer/<item>` or the supported neutral/local-acquisition observation | Purpose and method are not stolen item types | Item review applied |
| obj `exfiltration/{sensitive-data,serialization}` | `collection` or `credential-access` (no send), `stealer/<item>` (chain), mb `data/serialize` (neutral) | By required send | Open |
| obj `supply-chain/{install-hook,recon-exfil,credential-theft,metadata-anomaly}` | The required result's home, hook referenced | A trigger is not an objective | Open |
| obj `anti-static/obfuscation/{binary-metrics,code-metrics,tools,multi-layer}` | meta `binary` or `file`, `well-known/`, or a named concealment | Measurements and identities are not concealment | Open |
| meta `file/encoded`; `lang/encoded` | meta `file/encoding`; `lang/encoding` | Rename, then group by encoding scheme or measured shape | Applied; orphaned impossible XOR/Base64 co-occurrence composite removed |
| meta whole-file byte-entropy rules under `image/*` | meta `file/entropy` | Decoded-image measurements stay | Applied (no whole-file byte-entropy rules remain; decoded-image measurements stay under `image`) |
| meta `file/{string,literal}/*` | The subject each string evidences; context-only predicates held pending validated representation | No new IDs; exact existing IDs remain grandfathered until migrated | Partial (batches 047–080) |
| meta `lang/source/literal/value/*` | `lang/source/literal/{string,integer,hex,array}`, the evidenced subject, or `well-known/` | Review matcher and provenance before choosing a type or identity | Partial (generic string shapes and a hex value moved; encoded method names → `lang/encoding/base64`; datetime call → `lang/source/syntax/call/invocation`; remaining observations need individual review) |
| meta `file/data-blob/*` | The specific measured property or behavior-supported subject | No residual `data-blob` bucket; split entropy, region, signature, name, and string observations | Applied (14 rules moved to entropy, byte-prefix, filename, path, string-population and text-shape homes; no legacy YAML rules or live YAML references remain) |
| meta `file/policy/*` | `permission`, `hardening`, `package`, or document/format-specific property | No generic policy bucket; preserve declared-versus-effective scope | Open |
| meta `file/function/*` | Source declaration/name; population profile; `binary` anatomy | A name does not prove invocation or behavior | Partial (selected source declarations and function names moved; remaining observations need matcher and scope review) |
| meta `file/{arithmetic,padding}/*` | Parsed operator population, actual arithmetic operation, observed filler span, or a measured text-shape profile | Separate source-shape measurements from operation claims | Partial (`file/arithmetic` retired; digit and whitespace ratios and line shapes moved; leading whitespace moved to `file/profile/text-shape`; the uncontextualized text token under `padding` remains for review) |
| meta `package/tooling`, `hardening/missing` | `build/*`, `well-known/*`, `package/<subject>`; the mitigation's own subject | Grab-bag and judgment names | Applied (`hardening/missing` held four unreferenced aliases of ELF linking facts; those facts remain under `binary/linking/runtime`; Netris and HAL evidence moved to `well-known/`; no legacy tooling rules or live YAML references remain) |
| meta `binary/{installer,framework,vendor,signing,license,toolchain}` | `well-known/`, `vendor`, `signed`, `binary/provenance`, `lang/compiler` | Identity is not a format property | Open |
| `well-known/malware/supply-chain` | The family's defining role | Delivery does not choose identity | Open |

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
| Capacity for broad leaves | The default maximum is 100 rules; any category-specific exception requires a complete relevance audit and explicit user approval. Review parent and peer subjects, document the complete population and consumers, and resolve every broad observation before moving. Remove redundant levels and misplaced or duplicate rules before proposing refinements; do not invent a sibling or `other` bucket to satisfy the count. |
| Level-3 branches | Name the children, their single axis, precedence and an incomplete-evidence example before migrating. |
| Payload sinks | Decide `image-map` and `interpreter-stdin` before moving them. |
| Broad staging profiles | Staging rules that fit no operation need a defined home; neither dropping the claim nor calling it activation is acceptable. |
| Retained access | Choose a home for created accounts and authorized SSH keys, now in `persistence/login/{account,ssh}`. |
| C2 `dns` and `trigger` | The target layout folds DNS control into `channel/<transport>` and admitted activation guards into `execution/trigger`; keep both leaves until a disposition is recorded. |
| Cross-cutting discovery | Generate an algorithm/source/mechanism index from recorded facets, so an "AES" view finds both presence and operation rules. No engine change. |

### Migration guardrails

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
