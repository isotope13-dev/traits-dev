# Proposed taxonomy

Give every supported program observation one clear home. Cover ordinary software
as well as malware; prioritize malware-relevant coverage without making ordinary
capabilities imply an attack.

**Status:** design proposal, not the current directory whitelist. No rules are
moved by this document. Retain existing names where they express the right
subject. New homes require coordinated rule, reference, and validator updates.

Implementation has started with Unix mapping/unmapping and a 17-rule memory-operation batch.
See the [migration evidence](taxonomy-migration/README.md) and
[completion checklist](NEW_TAXONOMY_PLAN.md); other proposed destinations remain
subject to their contracts and migration gates.

**Depth:** count below the tier. `objectives/execution/payload/file-exec` is
three levels. This guide specifies domains, behaviors, and useful refinements
through that depth. It does not require uniform depth or prohibit deeper
techniques. Add a fourth-level contract only when it resolves a real ambiguity.

## Ranks

| Tier | Level one | Level two | Level three |
|---|---|---|---|
| `micro-behaviors` | Facility or resource | Subject or operation | Narrower operation or mechanism |
| `objectives` | Attacker objective | Behavior | Required source, target, trigger, or mechanism |
| `metadata` | Artifact subject | Property or part | Refinement of that property or part |
| `well-known` | Entity class | Function or named entity | Named entity or discriminating variant |

Each branch states the question its children answer. Existing resource-first
and operation-first paths may remain when their boundaries are clear; changing
their order alone does not improve classification. Deeper paths need the same
contract and a useful distinction, not automatic flattening.

## Principles

1. **Classify the observation.** Write what the matcher supports before choosing
   its home. A composite's consumer, the sample's reputation, and the author's
   original investigation do not determine placement.
2. **Make each step narrower.** A child must retain its parent's meaning. State
   the question a parent's children answer; define boundaries when answers overlap.
3. **Keep one canonical home.** Reuse observations by reference. Equivalent
   implementations share a home; different observations may coexist in one file.
4. **Separate mechanics, intent, properties, and identity.** A program can have
   many findings. Its reputation does not change where its ordinary operations go.
5. **Match the claim to the evidence.** References and embedded implementations
   can establish probable capabilities without proving execution. Describe that
   evidence honestly. Do not infer an algorithm, data flow, or purpose it lacks.
6. **Keep implementation in scope and filenames.** Language, backend, format,
   and platform do not partition a shared behavior. A mechanism such as systemd
   registration may be inherently platform-specific.
7. **Prefer the shortest precise path.** Split for a meaningful distinction, not
   for symmetry, rule count, or a model's feature-depth limit.
8. **Preserve detection deliberately.** Moves preserve matchers and effective
   defaults. Correct detection defects separately and record coverage changes.

Atomic and composite are rule forms, not taxonomic ranks. A compound neutral
capability remains neutral. A single structured matcher can establish a complete
attack behavior. Criticality, confidence, MBC mappings, and placement must each
fit the supported claim; none substitutes for the others.

## Choose the tier

| Tier | What belongs here | What membership does not claim |
|---|---|---|
| `micro-behaviors` | Probable program capabilities, simple or compound. | Malicious intent or observed runtime execution. |
| `objectives` | Behaviors with evidence of an attacker goal, unauthorized result, or abuse mechanism. | That every constituent API or operation is malicious. |
| `metadata` | Artifact properties, declarations, structure, and provenance. | That declared behavior executes or provenance establishes product identity. |
| `well-known` | Specific software, component, or malware-family identity. | That a generic dependency or shared capability identifies the whole artifact. |

An embedded AES implementation is a crypto capability. A manifest naming a
crypto dependency is metadata. A fingerprint identifying the analyzed library
itself is an entity identity. Encryption of a victim's files for extortion is an
objective. Keep these claims distinct even when one sample supports all four.

**Placement key:** state the required observation; choose its tier; choose the
facility, objective, property, or entity class; apply that branch's boundary rule;
stop at the most specific supported home. Required results take precedence over
incidental context. If two homes still fit, repair the boundary before migrating.
The local tests below resolve overlaps this general key cannot decide alone.

## Reading the hierarchy

Paths in the tables are relative to their tier. Comma-separated names denote
siblings; a slash denotes a child. `<protocol>`, `<format>`, `<resource>`,
`<mechanism>`, and `<entity>` are typed expansion points, never literal directory
names. An unqualified sibling inherits the preceding parent's path.

Keep established practitioner abbreviations such as `fs`, `mem`, `os`, `ipc`,
`db`, and protocol names. Spell out unfamiliar terms; do not rename clear paths
merely to standardize abbreviation.

- **Specified:** literal paths and their admission rules are intended destinations
  in this proposal, whether or not they exist today.
- **Illustrative:** angle-bracket expansions specify an axis, not approved leaf
  names. A branch contract must name its children and their admission tests before
  that branch can migrate. Until then, its proposed partition is reserved for
  design; an implementer cannot fill the placeholder with an improvised child.
- **Reserved:** documented subjects without a present migration requirement.
- **Open:** the explicit checkpoints below. Do not resolve them by guessing a
  destination, inventing specificity, or dropping a rule.

Rules live only in leaves. A parent with rule-bearing descendants owns no rules.
Before splitting a leaf, place **all** its observations, including broad ones.
If the evidence cannot choose a proposed child, revise the partition or keep a
separate, precisely named operation. Do not force specificity or create `other`.

**Broad observations:** keep an operation as a leaf when its evidence may omit
the algorithm, mechanism, or target subtype. Known detail remains in the rule's
claim, matcher, scope, and reviewed mappings; a directory need not encode every
fact. The broad leaf admits exactly that operation, not unrelated leftovers.
New children require a complete partition, including the least-specific accepted
observation. Size pressure does not waive this requirement.

The branch contract lists the broad leaf's required claim, exclusions, and
review facets, with unknown values explicit. Reject rules that require a
different operation; apply the documented precedence where claims overlap.
A known algorithm does not disqualify an encryption rule from crypto/encrypt.
Deduplicate synonymous observations only after comparing matchers and effective
scope; similar names alone do not establish equivalence.

## Capabilities: `micro-behaviors/`

An OS API keeps the more specific resource home: filesystem calls belong in
`fs`, memory calls in `mem`.

| Facility | Admits |
|---|---|
| `communications` | Endpoint exchange, protocols, channels, and address representation. |
| `network` | Local interfaces, routes, resolvers, connections, and shares. |
| `crypto` | Cryptographic primitives, operations, keys, and certificates. |
| `data` | Data transformation, storage, manipulation, and control-flow constructs. |
| `fs` | Files, directories, paths, and filesystem properties. |
| `mem` | Address spaces, memory objects, access, and permissions. |
| `hardware` | Device and peripheral I/O or control, regardless of API wrapper. |
| `process` | Execution contexts, lifecycle, coordination, descriptors, and interpreters. |
| `dylib` | Native shared-library loading and exported-symbol lookup. |
| `metaprogramming` | Inspection, generation, and transformation of program structure. |
| `os` | Named host services without a more specific facility home. |
| `time` | Clocks, waits, elapsed-time measurement, and in-process scheduling. |
| `ui` | Presentation and user interaction. |
| `browser-extension` | Extension-host surfaces without a shared capability home. |

### Communication and local networking

Keep the distinction between protocol exchange (`communications`) and management
of local network resources (`network`). Move local network operations out of the
competing `os/network` branch. A protocol name alone does not establish C2.

| Home, through level three | Admission and boundary |
|---|---|
| `communications/<protocol>/<operation>` | Protocol behavior: retain DNS, FTP, TFTP, SSH, TLS, WebSocket, RPC, gRPC, email, messaging, industrial protocols, and MCP where their semantics matter. A service vendor or client library is not a protocol. |
| `communications/email/send` | Sending email. Unsolicited-message abuse uses impact/spam; a send capability alone establishes neither spam nor phishing. |
| `communications/http/client`, `server` | Method-unspecified client request capability; server-side request handling. A specific verb uses its verb leaf. |
| `communications/http/{get,post,put,patch,delete,head,options}` | Required HTTP method. A required upload/download result takes precedence over an otherwise generic method claim. |
| `communications/http/{download,upload,header,cookies,auth,redirect,response}` | Required transfer direction or protocol surface. Header names/values stay with headers; a recognized authentication exchange stays with auth. Generic POST is not upload or exfiltration. |
| `communications/socket/{create,connect,bind,listen,accept,send,receive,close,configure}` | Socket lifecycle, connection, I/O, and options. Classify a recognized higher protocol by that protocol when the matcher requires it. |
| `communications/ip/{literal,parse,construct}` | IP address syntax and manipulation. Local interface state belongs in network; address text does not prove a connection. |
| `communications/url/{parse,construction,host,scheme,path,query}` | URL structure, construction, and endpoint references. Move generic URL observations here from HTTP-specific buckets; retain HTTP semantics under HTTP. |
| `communications/ipc/{pipe,shared-memory,message-queue,native-host}` | Local communication channels. Descriptor duplication belongs in process/fd; generic shared-memory allocation belongs in mem. |
| `communications/{proxy,capture,transfer,benchmark,flood}` | Required relay, traffic capture, transfer, measurement, or repeated-send capability. Refine by its actual mechanism; attack traffic requires an impact claim. |
| `network/interface` | Interface identity, address, configuration, or state. Retain this broad leaf while evidence cannot consistently separate operations. |
| `network/{connections,route,neighbors,dns,forward,qos,tunnel,status,share}` | Local connection inventory, routing, resolver configuration, forwarding, traffic policy, tunnel setup, connectivity state, and network-share management. Wire DNS exchanges remain communications/dns. |

Do not duplicate WebSocket beneath HTTP, or a client library beneath every HTTP
operation. An interface MAC address belongs with the interface; generic address
formatting belongs with protocol/address representation. The required subject
decides, not whether an OS API exposes it.

### Cryptography and data

Retain cryptographic families for evidence of a primitive's presence. Give
operations their own homes when the matcher establishes an operation. This
accommodates unknown algorithms without backend buckets or false specificity.

| Home, through level three | Admission and boundary |
|---|---|
| `crypto/symmetric/<algorithm>`, `asymmetric/<algorithm>`, `hybrid` | Named primitive/implementation presence when no narrower operation is established. AES tables support AES capability, not file encryption. Family-only cipher evidence uses crypto/cipher and records the supported family. |
| `crypto/{encrypt,decrypt,sign,verify}` | The named cryptographic operation, including algorithm-unspecified operations. Keep these as leaves until a complete, defensible refinement is available. |
| `crypto/hash/{digest,hmac}` | Digest or keyed message-authentication capability, including implementation presence. The description distinguishes presence from an operation. Algorithm is retained in the rule; noncryptographic checksums use data/checksum. |
| `crypto/kdf` | Key derivation, including unknown derivation algorithms. Reconcile current algorithm-, password-, file-, and provider-based children by the actual derivation claim before retaining a split. |
| `crypto/key/{generate,import,export,exchange,representation}` | Key lifecycle, agreement, or material representation. A recognized key format without an operation uses representation. Derivation uses crypto/kdf. |
| `crypto/certificate/{parse,validate,store}` | Working with certificates. Certificate properties in the analyzed artifact belong in metadata/signed. |
| `crypto/provider` | Probable provider capability, including provider acquisition/release. Retain one resource leaf so a provider reference is not forced into an unsupported lifecycle operation. |
| `crypto/cipher` | Cipher capability without a named algorithm or a supported direction. This includes a known symmetric/asymmetric family with unknown algorithm. Named primitive presence uses its family branch; encrypt/decrypt evidence uses that operation. |
| `crypto/mnemonic` | Seed-phrase generation, validation, or representation capability. Private-key formats are keys; wallet locations are filesystem paths. |
| `data/{encode,decode,compress,decompress}` | Directional transform branches. A rule belongs under the operation its matcher supports; retain a scheme/format child only when its matcher establishes that distinction. Keep language and library variants together. Parents with child leaves store no rules. Capacity and incoming-home checks are required before migration. |
| `data/codec` | Direction-neutral codec interfaces and family evidence. Keep scheme identity in each trait ID. Use one leaf while the set is small; add scheme or algorithm children only when they improve placement precision and do not create sparse siblings. Gzip and zlib both use DEFLATE, but their APIs remain distinguishable by ID. Direction-specific operations stay in `compress` or `decompress`. Excludes arbitrary strings/blobs and plain stream I/O. |
| `data/compression` | Compression-family composites that aggregate evidence across codec schemes and the `compress`/`decompress` directions. They report the family-level claim; directional behavior stays in its operation leaf, and scheme-specific codec evidence stays in its codec leaf. |
| `data/{parse,serialize,format}` | Parse structured input, emit structured data, or format scalar/text output. Format alone does not establish direction. These are operation leaves; no unknown-format rule is forced into a named format. |
| `data/archive/{create,extract,list,modify}` | Archive operations, with format in scope or a justified deeper refinement. Archive membership/layout is metadata. |
| `data/{string,buffer,collection,property}/<operation>` | Operations on text values, byte containers, collections, or object properties. Classify by receiver and operation, not method spelling alone. |
| `data/{arithmetic,checksum,reassembly,transaction}` | Numerical operations, noncryptographic integrity checks, reconstruction, and transaction semantics. Encryption and cryptographic hashes retain crypto homes. |
| `data/db/<operation>`, `config/<operation>` | Querying/modifying stored records or reading/writing program configuration. A literal configuration file path is fs/path. |
| `data/control-flow/{branch,loop,dispatch,error-handling,assert,return,sequence}` | Execution-path constructs. Retain the established control-flow home; source language and analyzer AST matching do not create subtypes. |
| `data/{stream,embedded,llm}/<operation>` | Stream processing, access/extraction of embedded data, or model inference/tool interactions. Stored blob shape is metadata; malicious prompt effects are objectives. |

**Placement precedence:** a supported operation owns the rule; primitive presence
owns a rule that only identifies the primitive. Thus an AES encryption call goes
to encrypt, while an AES implementation signature stays in symmetric/aes. These
are different observations, not two copies of the same matcher. CryptoAPI hashing
joins hash/digest; Python and native-backend names do not choose a second home.

Broad provider and cipher observations now have explicit homes. Provider APIs
that establish a narrower operation still move there: CryptHashData is hashing,
not provider management. No `crypto/native` or `crypto/library` remainder bucket.

**Discovery across homes:** record supported algorithm/family and operation as
facets in the migration manifest and generated review index. An AES view includes
both implementation-presence and encrypt/decrypt rules while keeping their claims
distinct. This is a derived navigation view, not new matcher fields, duplicate
rules, or an assumption that a directory prefix contains every AES observation.
Only record facets actually required by the rule; optional evidence is insufficient.

### Files, memory, and hardware

| Home, through level three | Admission and boundary |
|---|---|
| `fs/file/{create,open,close,copy,move,rename,stat,io-mode}` | File-object operations. Content read/write/delete use the established operation homes below. |
| `fs/read`, `fs/write`, `fs/delete/{file,directory}` | Content I/O stays in operation leaves; deletion divides by the removed resource. A sensitive filename does not create a second read/write home. Refine only after resolving broad operations and capacity. |
| `fs/directory/{create,readdir,traverse}`, `search/<predicate>` | Directory creation, listing, recursive walking, or selection by name/content. A required selection predicate owns a search even when it walks recursively. |
| `fs/path/<resource>`, `path-ops/{join,normalize,parse,match}` | Location/reference to a resource versus manipulation of a pathname. Path presence does not establish file access. |
| `fs/{acl,attributes,chmod,chown,link,lock,sync,watch,quota}` | Permissions, attributes, ownership, links, locking, synchronization, change monitoring, and limits. Refine only by a distinct operation or mechanism. |
| `fs/temp/{file,directory}`, `volume/<operation>`, `disk/<operation>` | Temporary-object creation and logical storage operations. Raw device I/O belongs in hardware. |
| `mem/{alloc,free,resize,copy,fill,compare}` | Allocate storage, release it, change its size, copy bytes, fill bytes, or compare byte regions. Compare returns equality/order; it does not transfer bytes. Split C-runtime buckets by operation. Preserve useful allocation refinements until their full population and broad-evidence home pass the capacity gate. |
| `mem/combined` | Memory-management composites spanning allocation, release, resize, or query evidence. Keep each atomic operation in its own home; group only when the consumer requires one alternative condition. |
| `mem/{map,unmap}` | Establish/change address-space mappings, or remove them. `mremap` follows mapping; its name alone does not prove a size change. Backing type is a refinement only when established; generic mmap does not establish one. Consolidate mapping observations from fs/memory/mmap and mem/alloc here. |
| `mem/create/{shared,image-section}`, `anonymous/create` | Memory objects and anonymous file descriptors. Creating a memfd does not establish execution from it. |
| `mem/{read,write}` | Memory-access leaves. Record local, remote-process, or physical address space when established; do not force unspecified access into one. Writing another process does not itself transfer execution to it. |
| `mem/{protect,query,advise,lock,gc}`, `sync/cache` | Memory permissions, inspection, advisory policy, pinning, collection, and visibility. Thread coordination belongs in process/sync. |
| `mem/{heap-spray,stack-pivot,overflow}` | Required spray layout, stack redirection, or out-of-bounds write mechanism. Generic allocation, stack manipulation, or an unsafe API alone is insufficient. Exploitation claims add their own evidence; the directory does not assign criticality. |
| `hardware/{input,display,block,flash,gpu,wireless,smartcard}/<operation>` | Device I/O, capture, and control. Host property queries use os/sysinfo; surveillance requires an objective. Driver/backend names do not replace the device or operation. |

Retain filesystem resource-path categories. Their meaning is useful even without
an access operation. Retire `fs/shell-ops` and `mem/c-runtime`: their contents move
by operation. Memory decompression goes to data/decompress.

**Archive versus file:** a rule binding an archive member to its extracted output
belongs in data/archive/extract, even when it also proves a file write. A separate
generic write observation stays in fs/write. Archive-library and write APIs that
merely co-occur do not establish extraction. Independent facts may have separate
rules; do not copy the complete extraction matcher into both homes.

### Execution facilities, metaprogramming, and OS services

| Home, through level three | Admission and boundary |
|---|---|
| `process/create/{thread,fiber,fork,shell,eval,subprocess,shellexec,exec}` | Create an execution context. Use the ordered mechanism test below. |
| `process/thread/{lifecycle,enumerate,group,priority,config,terminate}`, `fiber/{switch,convert,terminate}` | Thread/fiber management apart from creation. A fiber is not a thread. Merge the competing threading tree by its observations. |
| `process/sync/{mutex,semaphore,event,critical-section,join}` | Coordination between execution contexts. File-backed locking follows the lock claim; memory visibility remains mem/sync. |
| `process/work/{queue,pool,task}` | Execution scheduling by resource: queue/pool creation, configuration, inspection, and shutdown; task submission, completion, waiting, cancellation, and future/result access. Queues carrying messages use communications/ipc. |
| `process/{identity,info,enumerate,argument,resources,pid}` | Current identity, process properties, listing, arguments, resource controls, and PID-file lifecycle. A PID value is not a PID file. |
| `process/{exit,terminate,control,daemonize}` | Current-process exit, termination of another process, other state changes, and detachment. Detachment does not establish persistence. |
| `process/lifecycle/{initialize,shutdown,single-instance}` | Lifecycle operations and linked detection/prevention of a concurrent instance. Single-instance admits mutex, PID-file, lock, or equivalent guards; a mutex reference alone stays process/sync/mutex. Review broader lifecycle claims before splitting the existing branch. |
| `process/fd/{query,control,close,dup,stdio}`, `io/stream`, `tty/<operation>` | Descriptor operations, stream pumping, and terminal control. Pipe/channel creation belongs in communications/ipc. |
| `process/interpreter/{eval,compile,scripting}`, `script/<operation>` | In-process language execution and script handling. Launching an interpreter belongs in create; mere language identity is metadata/lang. |
| `process/{attach,debug,hook,inject}/<mechanism>` | Process attachment, debugging, interception, and execution transfer without an established attacker purpose. Objective composites add their own abuse evidence. |
| `process/deploy/{file-exec,module-load,script-eval,process-inject}` | Neutral compound acquisition/staging-to-activation claims, classified by required sink. Require the relationship between acquired/staged code and that sink; unrelated APIs do not establish deployment. |
| `dylib/{load,lookup,enumerate,unload}` | Native loader operations and exported-symbol lookup. Language modules belong in os/module; manual API-address reconstruction in os/api-resolution. |
| `metaprogramming/{ast,generation,reflection}` | Inspecting/transforming syntax trees, generating code, or inspecting/manipulating program structure at runtime. Replace data/source partitions by the actual operation. |
| `os/registry/{read,write,delete,open,enumerate,watch,keys,hive}` | Registry operations or key/hive references. References cannot be classified as reads/writes; durable reactivation is a separate persistence claim. |
| `os/service/{create,start,stop,delete,query,configure,dispatch}` | Service management. Definition fields alone remain configuration facts. |
| `os/env/{ci-credentials,secret-name,runtime,path,cicd,user-info,provider}` | Required variable meaning, in the ordered contract below. A reference alone does not establish reading its value; ordinary secret access does not establish theft. |
| `os/env/{read,enumerate,write,test}` | Environment operations without a required subject admitted above. A literal path without environment evidence stays fs/path. |
| `os/{user,group,privilege}/<operation>`, `os/security/<control>` | Principal/authority operations versus security controls. Each control contract defines its operations; an OS implementation is not another subject. |
| `os/kernel/<facility>`, `os/{syscall,bpf,container,virtualization}/<operation>` | Kernel facilities and execution isolation. Keep namespace operations in os/container/namespace; implementation platform does not choose a second home. |
| `os/kernel/driver` | Driver installation, loading, unloading, and management. Record the supported operation; distinguish it from ordinary service management. Refine only with a complete contract for driver references and operations. |
| `os/{module,api-resolution,linker}/<operation>` | Language modules, manual API resolution, and linking facilities. Normal exported-symbol lookup stays in dylib/lookup. |
| `os/autorun/<trigger>`, `os/package-manager/<operation>`, `os/sysinfo/<property>`, `os/random`, `os/telemetry/<facility>` | Respectively: OS-managed activation, package operations, host-property queries, randomness, and logging/tracing facilities. Timer callbacks belong in time/schedule. Each expansion uses only its named axis. |
| `os/{clipboard,console,event,signal,exception,message}/<operation>` | Host interaction and notification facilities. Mechanism-specific COM/WMI/PAM rules use their function when known; mechanism-only evidence may retain the named facility. |
| `time/{query,sleep,timing,schedule}/<operation>` | Read time, wait, measure elapsed time, or schedule an in-process callback. A timing gate for analysis evasion belongs in objectives. |
| `ui/{controls,dialog,graphics,help,menu,terminal,wallpaper,window}/<operation>` | Presentation and interaction. UI framework identity is well-known/lib; distinctive UI capability references can stay with the relevant surface. |
| `browser-extension/{action,lifecycle,management,tabs}` | Extension-host surfaces with no shared capability home. HTTP, storage, messaging, and scheduling retain their ordinary homes. |

**Process creation:** choose thread, fiber, or fork when established; otherwise shell
parsing, interpreter evaluation, desktop handler selection, a child-process
abstraction, or direct executable start. An explicit shell argument overrides a
generic subprocess API. Reconcile launch/spawn/direct/execv by this mechanism test.

**Work scheduling:** QueueUserWorkItem and dispatch_async submit tasks and belong
in process/work/task; they do not require creation of a thread. Queue/pool resource
management belongs in its respective leaf. Waiting for a task result is task
management; joining a thread is process/sync/join. A timer-triggered callback uses
time/schedule. A future fourth level may separate task operations only after the
broad task-interface observations have a defensible home.

**Environment subjects:** use the first required meaning established: CI-issued
credential (ci-credentials); another credential (secret-name); interpreter/loader
configuration (runtime); filesystem location (path); CI job/runner metadata
(cicd); current user identity/home metadata (user-info); service configuration
(provider). Thus AWS_SECRET_ACCESS_KEY uses secret-name, BASH_ENV uses runtime,
and HOME uses path. Execution during CI alone does not change the subject. If no
defined meaning is required, use the observed env operation; do not invent a
topic from an arbitrary variable name.

## Attacker behaviors: `objectives/`

Keep the established objective names. A neutral operation does not enter this
tier merely because malware uses it.

**Admission comes before placement.** Required evidence must support the attack
claim, not just the mechanics it uses. Static analysis may infer that claim; proof
of runtime execution is not required. Ordinary download-and-run, secret access,
or service registration alone does not establish abuse. State the distinguishing
target, deception, unauthorized action, or attack-specific relationship in the
rule's rationale. Reputation, optional clues, and two unrelated APIs cannot supply it.

| Objective | Level-two behaviors and level-three distinction | Boundary |
|---|---|---|
| `anti-analysis` | `debugger-detect`, `sandbox-detect`, `vm-detect`, `emulator-detect`, `tool-detect`, `environment-detect`, `timing`, `geofencing`, `anti-tampering`; refine by required probe/interference. | Analysis-targeted probing or gating; ordinary environment queries remain capabilities. |
| `anti-static` | `obfuscation/<concealment-mechanism>`, `pack/<unpacking-mechanism>`, `polyglot/<interpretation-conflict>`. | Obstructing recovery of code/data; encoding, compression, or high entropy alone is insufficient. |
| `collection` | `keylog`, `clipboard`, `screenshot`, `audio`, `camera`, `messaging`, `email`, `network`, `app-data`, `database`, `file-targeting`, `archive`, `monitor`; refine by acquisition/staging mechanism. | Targeted information capture without a required send. Credentials use credential-access; reconnaissance uses discovery; network here requires captured traffic, not a host inventory. |
| `credential-access` | `browser`, `cloud`, `credential-manager`, `keychain`, `env`, `memory`, `registry`, `files`, `ssh`, `wallet`, `email`, `messaging`, `dev-tools`, `wifi`; classify by required source using the ordered rule below. `capture`, `cracking`, `phishing` identify acquisition rather than stored-secret extraction. | Credential issuer/consumer does not override the actual store. A login form alone is not phishing. |
| `discovery` | `account`, `host`, `system`, `network`, `process`, `cloud`; refine by surveyed resource or probe. | Reconnaissance profile or targeted survey. A lone generic query need not infer reconnaissance. |
| `command-and-control` | `channel/<transport>`, `beacon/<check-in-mechanism>`, `remote-command/<dispatch-mechanism>`, `backdoor/<access-surface>`, `reverse-shell/<io-coupling>`, `botnet/<coordination>`, `infrastructure/<selection-mechanism>`. | Required attacker control, tasking, access, or communication. Payload deployment moves to execution. |
| `execution` | `payload/{file-exec,module-load,script-eval,process-inject}`, `staging/{acquire,reconstruct,extract,store}`, `exploit/<vulnerability-mechanism>`, `interpreter/<abuse-mechanism>`, `lolbin/<trusted-surface>`, `lure/<activation-mechanism>`, `trigger/<activation-mechanism>`. | After objective admission, a full payload chain follows its sink; preparatory executable handling without a sink follows its established staging operation. |
| `exfiltration` | `stealer/<data-source>` for linked source-to-send behavior; `http`, `dns`, `ftp`, `cloud`, `messaging`, `llm`, `oob`, `side-channel` for a specifically established exfiltration-channel technique. | Full source-to-send claim takes precedence over transport. LLM requires unauthorized disclosure through a model/tool interaction; ordinary inference is insufficient. Separate collection and networking without a supported relationship are insufficient. |
| `evasion` | `anti-av/<control>`, `security-bypass/<control>`, `masquerade/<deception>`, `file-hiding/<mechanism>`, `kernel-hide/<mechanism>`, `indicator-removal/<record>`, `process/<concealment-mechanism>`, `fileless/<mechanism>`. | Concealing activity or bypassing deployed controls. Neutral injection/hooking is a capability until an abuse result is supported. |
| `impact` | `destroy/<resource>`, `wipe/<erasure-mechanism>`, `ransom/<extortion-mechanism>`, `dos/<exhaustion-mechanism>`, `degrade/<target>`, `infect/<host-artifact>`, `crypto-manipulation/<target>`, `cryptojacking/<resource>`, `deface/<surface>`, `spam`. | Destruction, disruption, extortion, unauthorized modification, or resource abuse. Spam requires unsolicited-message abuse; volume alone is insufficient. Ordinary deletion/encryption remains neutral. |
| `lateral-movement` | `exploit/<remote-surface>`, `brute-force/<service>`, `pass-the-hash/<protocol>`, `smb/<access-mechanism>`, `ssh/<access-mechanism>`, `worm/<propagation-mechanism>`, `usb-worm/<activation-mechanism>`. | Access or propagation to another system. Mechanism-specific exploit/credential reuse wins over a generic protocol home. |
| `persistence` | `login/<activation-surface>`, `system/<activation-surface>`, `firmware/<firmware-surface>`. | Durable unwanted reactivation. Login means a user/session event; system means boot, service, task, application, or platform lifecycle; firmware means pre-OS activation. |
| `privilege-escalation` | `exploit/<boundary>`, `elevation-control/<bypass>`, `token-manipulation/<operation>`, `hijack-execution-flow/<surface>`, `modify-service/<abuse>`. | Required crossing to greater authority. A privileged API, requested permission, or injection alone is insufficient. |
| `supply-chain` | `impersonation/<selection-deception>`, `trojanized/<trusted-input>`, `hidden-payload/<inspection-evasion>`. | Abuse of component selection, distribution, or build/update trust. A package carrier or install-time result alone does not qualify. |

### Objective boundaries that decide placement

- **Credential source:** first classify a required deceptive capture as phishing,
  password/hash search as cracking, or live interception as capture. For stored
  extraction, use the immediate store: OS keychain, credential manager, environment,
  or cloud-hosted secret service. Otherwise use a required application/key-format
  store (browser, SSH, wallet, etc.); generic file extraction uses files. AWS keys
  stolen from environment variables use env, not cloud. A browser secret read
  through the OS keychain uses keychain; decrypting the browser's own password
  database with a keychain-derived key uses browser because that database is the
  required credential result. Required final source wins over supporting unlocks.
  Raw process-memory extraction uses memory; system credential material in
  registry keys or hives uses registry, including an offline SAM hive. A required
  application store takes precedence over its generic file/registry container.
- **Export uses the same source rule.** Complete unauthorized keychain-to-send
  chains use exfiltration/stealer/keychain even when a browser consumes the secret.
  Multiple required independent sources use stealer/multi-source; optional source
  clues never change ownership. Source unknown means no invented source category.
- **Full result before context.** Credential export during installation belongs
  in exfiltration/stealer by source, with install context referenced. A separate
  supply-chain rule must establish deception, substitution, or inspection evasion.
- **Activation before delivery detail.** Once objective admission is satisfied,
  an acquisition/staging-to-activation chain goes in execution/payload by sink.
  Its neutral counterpart uses micro-behaviors/process/deploy by the same sink.
  Language, transport, encryption, and carrier remain supporting facts.
- **Staging without activation:** require both an executable-payload preparation
  relationship and objective admission. Use reconstruct for synthesis/decoding,
  extract for recovering an existing embedded/container member, acquire for an
  external fetch, or store for placement alone, in that precedence order when
  one chain requires several. A later required activation selects payload instead.
  This is preparation for execution, not a claim that execution occurred. Ordinary
  executable extraction remains data/archive/extract or data/embedded; encoded
  bytes alone establish neither executable staging nor abuse. Broader claims that
  establish no staging operation remain an Open checkpoint, not guessed placements.
- **Control before an individual payload.** After objective admission, a reusable
  operator request-to-command surface is C2; one acquired payload being activated
  is execution/payload. Neutral remote administration retains capability findings.
  A program may support both observations without duplicating the same rule.
- **Mechanism before assumed intent.** Keep neutral hooking/injection canonical
  in capabilities; evasion, credential access, or escalation composites add the
  evidence for their own results. Do not assign stealth merely because it is common.
- **Target decides evasion.** Defeating behavioral analysis is anti-analysis;
  obstructing static recovery is anti-static; bypassing deployed controls is evasion.
  Stopping defenders is impact/degrade; obscuring their view is evasion/anti-av.
- **Persistence follows the trigger.** A login-triggered task belongs in login;
  a boot/interval task belongs in system. The registry is a storage mechanism,
  not evidence that every registration is login persistence.
- **Narrow effects beat broad effects.** Secure erasure uses wipe; extortion uses
  ransom; forced resource exhaustion uses dos. Generic destructive deletion uses
  destroy. File infection uses infect; propagation to another host uses lateral-movement.
- **Independent results remain independent.** A composite needs one stated result.
  Factor unrelated results into separate rules; retain a joint behavior only when
  their relationship is itself the supported observation. Optional corroboration
  cannot choose the home. Broad multi-result profiles need review, not an overflow leaf.

### MBC and ATT&CK correspondence

Use the local MBC [catalog summary](../src/mbc-markdown/mbc_summary.md) and linked
behavior definitions as the review baseline; record the catalog revision in
the migration manifest so later mapping changes remain traceable.

Review external mappings for every migrated objective leaf: record supported
behavior/technique IDs and their evidence, or explain the absence of a mapping
in its contract. A directory name does not prove every rule fits the same ID.
Never put a placeholder `none` into a rule's mapping field.

| Local objective | Catalog correspondence |
|---|---|
| `collection`, `credential-access`, `discovery`, `command-and-control`, `execution`, `exfiltration`, `impact`, `lateral-movement`, `persistence`, `privilege-escalation` | Corresponding MBC objectives and ATT&CK tactics. Individual mappings still require a matching behavior or technique definition. |
| `evasion` | MBC Defense Evasion; review the applicable ATT&CK technique. |
| `anti-analysis`, `anti-static` | MBC Anti-Behavioral Analysis and Anti-Static Analysis. No same-named ATT&CK tactics; individual techniques may map. |
| `supply-chain` | No matching MBC objective. ATT&CK Supply Chain Compromise (T1195) applies to supported compromise of the supply chain, not every package-carried attack. |

Local placement and catalog reporting need not use the same objective. External
tool transfer may map to MBC E1105 while living in execution/staging/acquire;
ordinary downloads do not automatically qualify. Installation of additional
code may map to B0023; not every payload evaluation or injection does.

Keep the current scalar `mbc:` schema. One MBC behavior ID can belong to multiple
MBC objectives; report those associations through the catalog mapping without
duplicating the rule. Record additional justified IDs in the migration review
index pending explicit schema support. Distinct evasion and escalation claims
retain distinct rules; shared injection mechanics do not make them duplicates.

## Artifact properties: `metadata/`

Classify the property or declaration. A parser's implementation and the file
carrying a field do not supersede that field's meaning.

| Level one | Level-two subjects; level-three refinement | Boundary |
|---|---|---|
| `arch` | Instruction-set/ABI family; target variant. | Target identity here; header-field validity under binary/header. |
| `binary` | `header`, `section`, `symbols`, `code`, `resource`, `linking`, `layout`, `debug`; property of that part. | Counts, entropy, overlays, and geometry. Named imports may establish capabilities; signatures use signed. |
| `build` | `config`, `manifest`, `artifact`, `generated`, `bundler`, `minifier`, `transpiler`, `package`, `ci`, `reproducible`, `vcs`; transformation/pipeline property. | Build declarations and output properties. Compiler attribution uses lang/compiler; identity of the compiler itself uses well-known. |
| `document` | `pdf`, `office`, `rtf`, `html`, `ole`, `chm`; parsed part/property. | Artifact structure, not the behavior of embedded code. |
| `file` | `format`, `magic`, `extension`, `size`, `encoding`, `naming`, `profile`, `literal`; whole-file property. | Specific subject meaning wins over a generic text/blob bucket. A format-defined field is more precise than its raw string representation. |
| `hardening` | `build`, `layout`, `memory`, `mitigation`, `sandbox`; policy/mitigation. | Absence is a value of a mitigation, not a separate missing category. Actual bypass belongs in objectives. |
| `image` | `pixel`, `segment`, `trailing`; image-specific geometry or layout. | Rendering/capture is a capability. Generic file identity remains file/format. |
| `font`, `media` (reserved) | Retain the existing planned schema: font table/container properties and cross-carrier media coverage properties. Materialize only for supported observations. | Font/pixel-specific properties keep their specific subject; generic file size/format remains file. |
| `import` | `builtin`, `package`, `framework`; referenced module/component. | Dependency reference, not library identity or proof of use. Manifest dependency declarations use package/dependencies. |
| `lang` | `source`, `compiler`, `runtime`, `version`, `encoding`, `natural`, `locale`; named language/toolchain property. | Code transformation belongs in build; runtime reflection belongs in metaprogramming. |
| `package` | Manifest field or package role; see below. | Properties of the distributed component, not its eventual runtime behavior. |
| `permission` | Granted/requested authority by resource (`host`, `network`, `storage`, `clipboard`, etc.); scope of that grant. | A hostname without grant context is not a permission. An API call is a capability. |
| `registry` | Publication, maintenance, adoption, custody, and listing facts. Retain the current leaf until a real partition is needed. | A registry claim is neither verified authorship nor proof of compromise. |
| `signed` | `certificate`, `entitlements`, `platform`, `trust-level`; certificate role, declared authority, or verification property. | A signer name is not product identity or proof of a valid chain. |
| `vendor` | `identity`, `os`, `string`; specifically supported provenance claim. | Certificate fields stay signed; package vendor fields stay package; product fingerprints stay well-known. |

`package` level two follows the field: `name`, `author`, `maintainers`, `vendor`,
`description`, `license`, `homepage`, `repository`, `version`, `runtime`,
`entrypoint`, `scripts`, `dependencies`, `ecosystem`, `manager`, `workspace`.
Non-field roles are `files`, `documentation`, `testing`, `integrity`, `config`,
and `publishing`. At level three:

- `scripts/{lifecycle,build,command}` distinguishes automatic hooks, build tasks,
  and named commands by their declared trigger.
- `dependencies/{manifest,lockfile,archive}` distinguishes declared, resolved,
  and shipped dependency facts.
- `documentation/{claims,security-advisory,source}` distinguishes asserted
  properties, advisory references, and documentation location/role.
- Other fields refine by their property; tests refine by harness/fixture/assertion
  role; integrity refines by checksum or content agreement. A quality judgment
  such as empty, suspicious, or incomplete is a value, not a new subject.

Do not create speculative format branches. Reserved subjects are contracts, not
empty directories to create; generic whole-file properties remain file.
Engine-emitted import/permission findings retain their producer schema until
engine and consumers can migrate together. Do not create shadow YAML rules.

## Known entities: `well-known/`

Retain the existing classes and clear function names. This is an identity catalog,
not another copy of the behavior tree. Typical depth is class/function/entity;
direct entity children remain valid where no useful function partition exists.

| Class | Level-two ownership | Level three |
|---|---|---|
| `malware` | Established defining role: backdoor, botnet, downloader, dropper, exploit, keylogger, miner, ransomware, rat, rootkit, stealer, trojan, virus, webshell, worm. | Recognized family. Distribution through a package does not create a second supply-chain family identity. |
| `unwanted` | Recognized unwanted-software family. | Distinct variant only when identity evidence supports it; otherwise stop at the family. |
| `lib` | Retain ai, cloud, concurrency, crypto, data, datetime, development, format, media, native, network, observability, platform, runtime, stdlib, testing, ui, vendor-sdk, web. | Identified library/framework/runtime artifact. |
| `dual-use` | Retain access-control, credentials, packaging, remote-admin, transfer, tunnel. | Legitimate product whose primary purpose fits that function. These specific classes precede app/tool. |
| `game` | Named game/platform, or an existing useful class such as mod, cheat, anti-cheat. | Named component where a class parent is used. Do not invent a grouping level to force uniform depth. |
| `tool` | Retain browser, detection, development, media, offensive, packaging, reverse-engineering, sysadmin. | Professional utility. Add a function only when it distinguishes a real analyst/developer/admin workflow. |
| `app` | Retain ai, browser, browser-extension, communication, data, development, enterprise, finance, infrastructure, media, network, productivity, publishing, security, storage, system, utility. | End-user application, service/suite, or platform component. |

Choose class in order: malware, unwanted, library, defined dual-use function,
game-specific identity, professional tool, end-user app. Within a class, choose
the documented primary function once. A database library belongs in data; a
representation parser in format; a cloud-control SDK in cloud; a general protocol
client in network. Implementation language is not a function.

Identity requires discriminating evidence. A family-specific Elex configuration
fingerprint belongs with Elex; generic WMI or HTTP evidence does not. A program
containing library code is not necessarily that library as an artifact. An entity
classification is not a blanket reason to suppress its behaviors.

## Placement exercise

These are worked classification examples, not executed detection tests. Paths
are relative to the indicated tier. Objective examples assume the stated abuse
is supported by required evidence; the program merely being malware is insufficient.

| Required observation | Proposed home | Nearest alternative and deciding fact |
|---|---|---|
| Embedded AES implementation; direction unknown | micro: `crypto/symmetric/aes` | Not encrypt: no direction established. |
| Symmetric cipher capability; algorithm and direction unknown | micro: `crypto/cipher` | Not an invented algorithm; retain symmetric as a supported facet. |
| AES encryption operation | micro: `crypto/encrypt` | Operation wins over primitive presence; retain AES in the algorithm view. |
| Encoding operation; no existing scheme child fits | micro: unresolved under B6 until its positive evidence supports an under-cap child. | Not codec: direction is established, but specificity alone does not define a taxonomy class. |
| A codec implementation; direction unknown | micro: `data/codec` | Not encode or decode without directional evidence. |
| Memory allocation; allocator mechanism unknown | micro: `mem/alloc` | Not heap or virtual without mechanism evidence. Capacity checkpoint applies. |
| Archive member bound to a written output file | micro: `data/archive/extract` | Extraction owns the full relationship; its generic write atom remains fs/write. |
| QueueUserWorkItem or dispatch_async submission | micro: `process/work/task` | Not thread creation: submission may reuse an existing worker. |
| Create/configure a work queue | micro: `process/work/queue` | Not task: the queue resource itself is the subject. |
| Ordinary updater downloads and launches the retrieved image | micro: `process/deploy/file-exec` | No attack claim solely from acquisition plus activation. |
| Deceptive installer deploys concealed attacker code, with both deception and the handoff required | objectives: `execution/payload/file-exec` | Objective admission and linked activation are both established. |
| Attack-specific loader reconstructs executable code for a later stage; activation unavailable | objectives: `execution/staging/reconstruct` | Preparation is supported; execution is not. An ordinary embedded blob would stay neutral. |
| Encoded bytes with no executable or abuse evidence | metadata: `file/encoding` | Content representation is neither decoding capability nor payload staging. |
| Application reads its configured AWS credential normally | micro: `os/env/secret-name` | Required credential-variable subject wins over generic read; no theft is inferred. |
| Required attack behavior harvests AWS secrets from environment variables | objectives: `credential-access/env` | Immediate source wins over cloud issuer. |
| Required attack behavior extracts a browser secret from an OS keychain item | objectives: `credential-access/keychain` | Immediate secret source wins over its browser consumer. |
| Required attack behavior decrypts a browser password database using a keychain-derived key | objectives: `credential-access/browser` | Browser database is the final credential source; the unlock key is supporting evidence. |
| Install hook exports keychain secrets without authorization | objectives: `exfiltration/stealer/keychain` | Source-to-send result wins over lifecycle context. |

Before migrating a branch, two independent placement passes should agree on its
examples, nearest alternatives, and broadest accepted observations. Disagreement
requires a contract correction, not an ad hoc exception for the sample. Turn the
relevant examples into migration checks using existing fixtures where possible.

Additional catalog coverage checks:

| Required observation | Home or boundary |
|---|---|
| Prevent a second instance after checking a mutex, PID file, or lock (B0024) | micro: `process/lifecycle/single-instance`; acquiring an unrelated mutex is the near miss. |
| Send email (B0020); abuse a victim to send spam (B0039) | micro: `communications/email/send`; objectives: `impact/spam` only with the abuse claim. Legitimate bulk mail is the near miss. |
| Remote access (B0022) | Attacker access may use C2/backdoor; ordinary remote administration stays neutral. Review MBC's Impact/Persistence associations separately from local placement. |
| Conditional execution (B0025) | Neutral branch/gate stays data/control-flow; analysis-targeted gating uses anti-analysis; an admitted attack activation guard uses execution/trigger. |
| Execution dependency (B0044) | Required runtime/library facts use metadata/lang/runtime or package/dependencies as appropriate. A dependency does not establish process creation or an environment check. |
| Driver installation/loading (C0037/C0023) | micro: `os/kernel/driver`; generic service creation without driver evidence is insufficient. |
| Heap spray, stack pivot, buffer overflow (C0006/C0009/C0010) | Corresponding mem operation; mere allocation, stack-pointer access, or unsafe API presence is insufficient. |
| Malicious configuration (B0047), registry modification (E1112) | Neutral configuration/write facts stay capabilities. An objective must require the supported bypass, reactivation, or disruption result. |
| Self/taskbar discovery | Neutral process identity or window enumeration remains a capability; an admitted reconnaissance claim uses discovery/process or discovery/system by surveyed subject. |

**Fixture status: pending.** These examples specify claims, not completed tests
or guaranteed mappings for every rule at the named home. Before a branch moves,
its manifest must name actual fixture paths, expected rule IDs/homes, neighboring
claims, and recorded check results. `make validate` alone does not run this
placement exercise or establish semantic agreement.

## Disposition of existing branches

Before migrating a branch, inventory every existing level-two directory and
deeper leaf into the migration manifest. Record retain, rename, merge, split,
retire, or open; then account for every old rule ID and its destination, rationale,
and reference updates. An open row names an owner and the decision needed.
Omission means unreviewed, not implicitly retained or deleted. Retiring a branch
never silently discards its findings. Existing deep leaves follow the same review.

These boundaries correct blanket moves proposed in the review; they are not a
complete migration manifest:

| Existing branch (relative to its tier) | Disposition by required observation |
|---|---|
| micro: `data/source` | Split: syntax manipulation to metaprogramming, execution constructs to data/control-flow, artifact/language facts to metadata. |
| micro: `communications/blockchain` | Preserve actual protocol/RPC behavior; endpoint text, a dependency, and library identity require separate claim review. |
| micro: `fs/enumerate` | Split by directory listing, predicate search, or volume inventory; not everything is readdir. |
| micro: `process/threading`, `process/user` | Threading splits among thread, sync, and work; current process identity stays process/identity, while principal administration uses os/user. |
| micro: `ui/framework` | Identity to well-known/lib; distinctive UI capabilities stay with their surface. |
| objectives: `command-and-control/dropper` | Linked activation to execution/payload; admitted preparation to execution/staging; actual control remains C2. Neutral claims use capabilities. Broad partial claims remain open until their contracts are defined. |
| objectives: `credential-access/dump`, `windows-registry`, `theft`, `validation` | Classify by actual source or acquisition. Dump is not synonymous with memory; registry is not generic files; forged authentication is not password cracking. Unresolved claims remain open. |
| objectives: `evasion/hijack-execution-flow`, `privilege-escalation/process-injection` | Preserve concealment versus increased-authority results. Neutral interception/injection has its capability home. Do not merge distinct results just because mechanics overlap. |
| objectives: `exfiltration/serialization`, `sensitive-data` | A required send relationship selects source/channel; encoding alone is a capability, and capture alone is collection or credential-access. |
| objectives: `lateral-movement/delivery` | Open: inspect remote execution, administrative shares, WMI, GPO, and update-service delivery by mechanism and result. The existing branch is not an email-delivery category. |
| objectives: `supply-chain/credential-theft`, `install-hook`, `recon-exfil` | Theft without send uses credential-access; required export uses exfiltration; activation uses execution; trust abuse remains supply-chain; neutral installation/reconnaissance facts retain their own homes. |

No destination inferred from an old directory name bypasses tier admission,
leaf-only storage, or the capacity gate.

## Open checkpoints

These are implementation/design dependencies, not permission to use old and new
homes interchangeably. Resolve each in the migration manifest before moving the
affected rules; other specified branches can proceed independently.

| Checkpoint | Required resolution |
|---|---|
| Broad operation leaves versus the 100-rule cap | Measure the proposed destination after relocations and semantic deduplication. The earlier inventory already has 423 encoding rules, 341 decoding rules, 108 allocation rules, 177 file-read rules, and 467 file-write rules in their respective subtrees. Flattening them unchanged would fail. Retain a split only with a complete partition that admits broad evidence; otherwise record a concrete size-policy decision for that leaf. This document grants no exemption and does not authorize bulk flattening. |
| Illustrative third-level branches | Specify actual children, their single classification axis, precedence, and an incomplete-evidence example. Do not treat angle-bracket placeholders as permission to choose a different axis for each child. |
| Existing branch dispositions | Complete the manifest for the affected branch, including deeper leaves and broad observations. Assign an owner to unresolved rows; no migration proceeds on an omitted or open destination. |
| Broad preparatory attack profiles | Inspect staging rules that cannot select acquire/reconstruct/extract/store. Identify the actual supported observation and define its home; neither dropping the claim nor calling it activated is acceptable. |
| Cross-cutting discovery | Generate the algorithm/source/mechanism review index from the manifest's supported facets; verify representative queries. No engine schema change or automatic inference of an absent facet is implied. |
| Rules and validator alignment | Reconcile RULES.md's blanket restriction on objective atomics with the evidence-based tier rule here; align path whitelists and generated-ID contracts during migration. New documentation does not silently override the running validator. |

## Guardrails and migration

A branch contract states its subject, its children's question, admission and
exclusion criteria, and a positive/neighboring counterexample. Write additional
contracts only where the tables leave a genuine ambiguity; avoid repeating them
for every implementation or named product.

Every new or relocated leaf needs a representative positive fixture and a near
miss for its distinguishing claim, recorded in the shared contract/manifest.
Reuse existing fixtures. A program can validly match two siblings: test the
required claim, not artificial mutual exclusion. Include a both-claims case
where overlap is intentional. For exception rules, verify the intended
suppression. These checks complement preservation checks over the existing corpus.

Keep the current 100-rule limit and structural checks during migration. Treat
size as a prompt to inspect coherence: relocate mistakes and consolidate
equivalent observations before splitting. A coherent oversized leaf is an
explicit design issue; this proposal grants no exemptions. A 20-rule mixture
still fails semantic review. Retain the existing breadth/depth review signals;
do not add levels merely to satisfy a count.

Preserve exact-reference and directory-reference meaning. Moving a subtree can
silently widen or narrow a composite, including exclusions. Update all consumers,
effective scopes/defaults, exception references, and external mappings together.
`crit: exception` remains an assembly-only benign-context rule, not a behavior
category; its naming and placement must explain the context it recognizes.

Migration acceptance: every old rule is accounted for; references resolve;
placement-only moves preserve matching; leaf fixtures and mapping reviews are
recorded; intentional coverage changes have separate evidence; no leaf exceeds
the 100-rule cap; `make validate` passes. The migration manifest, detailed
fourth-level contracts, fixture results, and historical decisions belong outside
this concise guide.

## Appendix: rationale and sources

### Changes with a reason

| Change | Clarity gained |
|---|---|
| Split C-runtime memory buckets by operation; separate free/resize from alloc. | Releasing memory stops being classified as allocation or by runtime. |
| Consolidate memory mappings and local network facilities. | One resource has one home despite different OS APIs or backing stores. |
| Retire source-language, library/backend, and synonymous launch branches. | Equivalent observations stop acquiring different homes by implementation. |
| Add reflection under metaprogramming; separate crypto operations from primitive presence. | Unknown implementation or algorithm no longer forces an unsupported claim. |
| Define broad transform operations and work scheduling explicitly. | Unknown algorithms and worker reuse have homes without guessed methods or thread creation. |
| Place payload activation in execution; retain actual control surfaces in C2. | A payload handoff no longer implies an attacker command channel. |
| Require objective admission before routing deployment; retain neutral chains and partial attack staging. | Ordinary updaters stay neutral, and preparatory evidence does not acquire an execution claim. |
| Keep install/build context as referenced evidence; reserve supply-chain for trust violations. | Credential theft and export retain the same home across execution phases. |
| Move family fingerprints into entity identities. | A reusable behavioral finding no longer depends on a named family. |
| Preserve clear tier/domain/function names and variable depth. | Migration effort goes toward meaning rather than cosmetic uniformity. |

### Design basis

This proposal applies the repository's existing placement contracts, with the
boundary corrections above. MBC's useful distinction is between objectives,
behaviors, and methods; behavior can be reported when intent or method is unknown.
Its guidance to decompose compound observations supports canonical reusable
findings. See the local MBC [overview](../src/mbc-markdown/README.md) and
[mapping guidance](../src/mbc-markdown/yfaq/README.md).

The design lenses are Pike's predictable composition and economy of choices,
Linnaean distinguishing definitions, and MBC's malware-analysis experience. They
are design tests, not claims that those authors reviewed or endorsed this proposal.
Background: [Pike, Simplicity Is Complicated](https://go.dev/talks/2015/simplicity-is-complicated.slide)
and [The Linnean Society, Naming Nature](https://www.linnean.org/research-collections/on-display/staircase/naming-nature).

### Review decisions

The [committee-style recommendations](NEW_TAXONOMY_CHANGES.md) informed this
revision. Adopted C1/C10's ranks and facility guide; adapted C2/C4's placement key
and naming guidance; strengthened C6/C7/C11/C12/C14's branch, accounting, and
fixture requirements; incorporated C8/C9's catalog coverage with claim and schema
corrections; moved rationale here per C15. Retained the local boundary tests.

C3's wholesale resource-first renames, C5's 300-rule exceptions, and C13's fixed
depth ceiling are not adopted. Renaming alone adds no meaning; file counts do
not establish post-migration rule capacity; depth alone does not establish a
bad partition. The 100-rule checkpoint remains unresolved until measured,
coherent destinations satisfy it. No list-valued MBC field, fabricated fixture
result, or unconditional move from C7 is authorized by this revision.
