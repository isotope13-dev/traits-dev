# cleave taxonomy

## Philosophy

Classify the observation. One specimen can show a decoder, a network client, and
a theft. Each finding gets the same home it would get in another specimen. The
file's reputation supplies no evidence to its matchers.

Give each observation one home. Define its matcher once. A capability shared by
several objectives retains its name wherever it is cited. A single definition
prevents duplicate counts and gives the next author a rule to reuse.

Each rank asks one question. Every child inherits its parent's meaning and adds
a distinction the evidence can support. Under a file path, ask what the path
points to. Under credential acquisition, ask where the secret came from. Under
theft, ask what left. A browser password can answer all three questions in three
different findings.

Prefer the shortest path that preserves the claim. A change of language,
library, platform, or matcher should leave the path alone when the operation
stays the same. Give a platform its own rank when it supplies the mechanism, as
Winlogon does. Put incidental differences in scope, filenames, or local IDs.

Two authors given the same required evidence should reach the same leaf. When
they disagree, find the fact that would decide the case. Put that fact in the
branch description. If neither author can name one, reconsider the division.

## Placement procedure

1. Write one sentence saying what must match. Identify the operation, its
   object, and any purpose the evidence distinguishes.
2. Choose the kingdom below. Read the nearest competing branch as well as the
   apparent destination.
3. Descend while each distinction holds for every way the rule can match.
   Uncertainty about purpose still leaves a known operation. Uncertainty about
   the algorithm still leaves a known transformation.
4. Find a rule-bearing leaf for that claim. Look for an existing matcher before
   adding one. A directory selector can name a whole branch.
5. Read the proposed path and description together. An analyst should be able to
   tell what was observed, what was inferred, and what remains open.

### Kingdoms

Start with what the required evidence tells you about the scanned artifact.

| Kingdom | Claim | Example |
| --- | --- | --- |
| `well-known` | Identity of a widely known project's own file. | libcrypto. |
| `objectives` | A plausible attack purpose. | A ransom demand. |
| `micro-behaviors` | A capability or a clue to one. | A crypto dependency. |
| `metadata` | A property with no behavioral implication. | ELF class. |

An incomplete observation keeps its subject. A distinctive Startup HTA path
assignment can be evidence of startup persistence. Describe the assignment.
Installation and activation each require further evidence. A generic path
assignment has only the meaning its operands supply.

### Matcher defines identity

Read the matcher before the name. A Referer-header read in a webshell is an HTTP
observation. A call that decodes Base64 and assigns the result to a member is a
decoding observation. An indexed XOR establishes a bit operation. A cipher or a
decoding loop requires evidence of that additional structure.

Static evidence can support a probable purpose. A description should say whether
the rule finds a name, a declaration, a configured action, a call, or a
relationship between operations. An import can identify an interface. A code
example quoted in a manual can contain the same spelling as a call.

Set criticality from the observation's significance in its scope. Set confidence
from confidence in the match. Repair a faulty claim by changing the matcher,
description, or placement. [Rule fields](RULES.md#a-rule-file)

A complete fact can be near-universal in its scope (`baseline`) or worth seeing
in a version diff (`notable`). A fragment may be a `component`. Use `suspicious`
for evidence of evasion or abuse with plausible benign use. Known entities admit
no baseline. Reserve `hostile` for objectives and known entities.

### Composites and references

Place a composite by the result its required legs support. A transport, trigger,
or encoding can contribute evidence from its own branch.

- Check every passing combination. A condition the rule can bypass cannot
  establish a subtype.
- Count independent roles. Two endpoints can satisfy a threshold of two while
  supplying no source. A directory selector can count both an atom and a
  composite built from it.
- State the relationship the matcher establishes. A credential query,
  decryption, and a webhook can support a stealer inference. A claim that the
  webhook carried the query result needs evidence connecting them. Proximity to
  one leg of a composite says little about its other legs.
- Give unrelated results separate rules. Keep a joint rule when their
  relationship is itself the observation.

Capabilities may cite capabilities and metadata. Use known apps, tools, dual-use
products, games, or libraries in a capability only to exclude a false positive.
Objectives can also cite other objectives and use those known entities as
evidence. Family detections may depend on objectives. Keep malware-family
identity out of capability and objective predicates.

Metadata may cite metadata and use a known benign entity as context.
Known-entity rules may cite any kingdom. Each identity rule must still
distinguish its entity on every passing path.

An informative operation stays informative inside a composite. A filename chosen
by a collector supplies no evidence of attack. A format-mandated name can be
required. A campaign filename can corroborate a content-based conviction. Name
an exception composite for the benign condition it recognizes. A path
containing `testdata` alone cannot establish that the artifact is a test.
[Exclusions and downgrades](RULES.md#exclusions-and-downgrades)

Assign MBC and ATT&CK IDs from the evidence required by the rule. Use a
file-level mapping only when every rule in the file earns it. For example, a
staging rule can support an ingress-transfer mapping before any payload
activation. A neutral send-mail operation and spam have different mappings.

## Map

Kingdom headings link to the tree. A path starts at the kingdom root unless it
names another kingdom. Each path names a subject. Inspect its children to find a
leaf. Braces list sibling directories under the printed prefix.

- [Capabilities](#micro-behaviors) include
  [protocols](#protocol-and-request-keys),
  [data](#transformations-and-representations),
  [resources](#resource-and-operation-keys), [processes](#execution-contexts),
  and [host services](#host-surfaces).
- [Objectives](#objectives) include [acquisition](#acquisition-keys),
  [export](#export-keys), and [activation](#activation-and-control-keys).
- [Artifact properties](#artifact-property-keys) and
  [entity classes](#entity-classes-and-functions) have their own keys.

### [Micro-behaviors](micro-behaviors/)

Choose the facility that owns the operation. An OS API can act on a file, a
process, or a socket. Its vendor and implementation language settle none of
those choices.

#### Communications and network

- [communications](micro-behaviors/communications/) covers exchanges with peers.
  Start with the protocol or channel, then the operation. DNS traffic belongs
  here. [network](micro-behaviors/network/) covers local interfaces, routes,
  neighbors, resolver settings, and forwarding.
- In `communications/socket`, classify by operation. Binding, listening, and
  accepting a connection each have a distinct home. An endpoint alone identifies
  an address. Client setup and completed contact are different observations.
- In `communications/http`, prefer the required transfer or service action.
  Downloading a file is more specific than a GET. Reading an incoming header
  differs from constructing an outgoing request. With only a header, use its
  role. With only a required method, use the method.
- In `communications/url`, distinguish a URL's construction, components, and
  opening. A GitHub URL belongs under `communications/url/external/github`. A
  GitHub API operation belongs under `communications/http/services/github`. A
  filename suffix in the URL says nothing about the response bytes.
- SSH configuration, key use, and connection are distinct. TLS setup and
  disabling certificate checks are distinct. Sending email is a capability.
  Evidence of unsolicited-message abuse can support `objectives/impact/spam`.
- Messaging, IPC, and proxying follow the channel and operation. Creating a pipe
  is IPC. Duplicating a file descriptor belongs under `process/fd`. A
  callback-shaped hostname alone establishes neither tasking nor theft.

##### Protocol and request keys

Within `communications/http`, choose the field, request, transfer, or service
the matcher requires. These distinctions apply equally to CLI and SDK calls.

- `oauth` requires grant or protocol evidence. A `refresh_token` field alone
  fits `token-auth`. Use `basic-auth` for Basic credentials, `jwt` for JWT
  structure, and `authorization-header` for constructing that header.
- `header/{referer,host,forwarded}` distinguishes the field read.
  `header/{content-length,transfer-encoding}` describes message framing.
  `head-request` records the HTTP method.
- `curl/{command,body,binding}` separates command invocation, body arguments,
  and the library interface. A curl command alone leaves download open.
- `request/query` requires an outgoing request. Under `request/body`, use
  `construction` for assembly, or `credential`, `environment`, `file`, or
  `command-output` when the content is required. A body under construction can
  be identified before any bytes are sent.
- `services/entra-directory` covers directory users, roles, and principals.
  Other Graph resources belong with their service. A bare Graph host gives no
  evidence of an operation on a user. `services/github` likewise needs a service
  interface or operation beyond the spelling of a URL.

Under `communications/url`, `host` identifies the host, `resource-path` the
resource addressed, and `query` the parameters. Query children include
`command`, `credential`, `prompt`, `profile`, and `structure`. A generic
parameter name establishes structure. A required operation on its value can
justify a narrower subject. `construction/query` describes building a query.

Use `communications/ssh/{configure,keys,connect,transfer}` for settings, key
use, connection, or transfer. Under `communications/tls/verify`, a callback
belongs in `callback` unless its behavior establishes `disable`. Classify a
SOCKS interface under `communications/proxy` and local forwarding policy under
`network/forward`. Protocol families such as `communications/{dns,smb,irc}` or
`communications/{modbus,dnp3,s7}` use the same operation test.

#### Crypto and data

- A manifest dependency on OpenSSL or an import of libcrypto belongs under
  `micro-behaviors/crypto`. When only the provider is known, use
  `crypto/provider/library` and describe the dependency. A particular cipher,
  operation, or attack purpose needs its own evidence.
- [crypto](micro-behaviors/crypto/) groups cryptographic operations, primitives,
  and key handling. Prefer the operation when the rule requires encryption,
  decryption, signing, verification, derivation, or hashing. A recognizable
  implementation with no direction can establish a primitive. A key reference
  can identify the kind of material involved.
- Keep the supported stage. An encryptor constructor belongs under
  `crypto/encrypt/initialize`. A call that transforms data belongs under
  `crypto/encrypt/transform`. An API name alone belongs under `reference`.
  Changing libraries preserves the operation. The artifact's own signature
  belongs under `metadata/signature`.
- [data](micro-behaviors/data/) covers representation, transformation, storage,
  and control flow. Parsing takes a representation to objects. Serialization
  goes the other way. Choose encode, decode, compress, or decompress when
  direction is required. A bidirectional codec and an encoding merely present in
  a file have different homes.
- For Base64, inspect `data/decode/base64` for the required kind of decode. A
  Base64 module import indicates a codec with direction unresolved. Indexed
  arithmetic, an XOR transformation, and a keyed cipher each require their own
  distinguishing evidence.
- File contents, database records, configuration, and streams keep their
  resource when it matters. A database read that selects a column is more
  specific than a generic query. Use `process/stdio` for identified standard
  streams and `data/stream` for generic stream operations.
- A conditional belongs with control flow. A probe directed at a sandbox can
  support anti-analysis. An execution trigger requires evidence of what
  activates the behavior. A routine availability check establishes a guard.

##### Transformations and representations

- Under `crypto/symmetric/aes`, distinguish a constant table, initialization,
  mode selection, and transformation. A call that establishes encryption or
  decryption takes the corresponding direction. A constructor can establish
  direction before it transforms bytes.
- `crypto/hash/{digest,hmac,proof-of-work}` separates a digest, a keyed MAC, and
  work against a target. `data/checksum` covers noncryptographic checks. A
  signature interface can admit either signing or verification. A method called
  `sign` alone may also admit HMAC.
- `crypto/key/{generate,derive,exchange,import,export,recover}` follows the
  key's lifecycle. `crypto/kdf` requires a key derivation function. Deriving a
  public key or an address from existing material belongs in `key/derive` under
  `crypto`.
- `data/transaction/{construct,authorize,sign,submit,query}` follows a ledger
  transaction. Wallet paths belong in `fs/path/credential/wallet`, wallet
  controls in `ui/controls/wallet`, RPC in `communications/blockchain`.
- Use `data/bitwise/xor-forms` for indexed, scalar, or stateful XOR. A
  reversible representation can support `data/encoding/xor`. A required
  direction narrows that to `data/{encode,decode}/xor`. A keyed cipher belongs
  in `crypto/symmetric/xor`.
- `data/{parse,serialize}/yaml` separates loading from emitting YAML.
  `data/archive/{create,extract,list,modify}` follows the operation on the
  container. `data/db/read/{column,key-value,records}` distinguishes a
  projection, keyed lookup, and record retrieval. Schema inspection belongs
  under `data/db/schema`.
- In `data/control-flow` distinguish a branch, dispatch, loop, and error
  handler. In `loop`, choose an unconditional loop first, then a counted loop,
  collection iteration, or another conditional loop. Preserve a selection or
  dispatch mechanism when the matcher requires it.

#### Files, memory, and hardware

- [fs](micro-behaviors/fs/) owns file and directory operations. Distinguish a
  path reference, opening the resource, reading it, changing it, and executing
  it. A `Zone.Identifier` stream name is a path fact. Removal requires a change.
- Under `fs/path`, classify the referenced resource. A file that holds a
  secret is a credential, not configuration, and goes under `credential/`. A
  public key, a CA certificate, and a product's non-secret settings stay
  outside it. A path under a system root can still identify an application
  cache. A scanned file's own location belongs under `metadata/path`.
- Directory listing reads one directory. Traversal descends. Search requires a
  selection criterion. Creating a temporary file differs from mentioning a
  temporary directory.
- [mem](micro-behaviors/mem/) owns allocation, mapping, copying, protection, and
  release. A bare `memcpy` belongs under `mem/copy` in any specimen. Executable
  permissions describe a memory state. Control transfer into another process
  supplies the additional distinction for injection.
- [hardware](micro-behaviors/hardware/) owns device I/O and control, including
  keyboard input, display capture, radios, and block devices. A host inventory
  is `os/sysinfo`. Rendering a page is UI. Recording keystrokes for collection
  adds a purpose beyond receiving keyboard events.

##### Resource and operation keys

- `fs/path` asks what the path identifies. For a credential, take the first
  home under `credential/` that fits. A rule naming several kinds or services
  together is `collection`. Key material is `private-key`, even for a service:
  `~/.ssh/id_rsa` is `private-key`, not `ssh`. Then `wallet`, including a
  wallet keystore, `password-store`, `cookie`, and `account-db` for OS account
  databases such as `shadow`, SAM, and NTDS. Other SSH artefacts are `ssh`. A
  credential file of a named service goes to that service: `cloud`,
  `container`, `registry` (`.netrc` included), `vcs`, `ai-agent`, `database`,
  or `application` for other named apps and servers. A file recognized only by
  a generic name, such as `credentials.txt`, `token.txt`, or `.env`, is
  `generic-basename`. If the rule needs more than the name, it belongs
  elsewhere. A challenge flag is `challenge-flag`, not a credential.
  `system/{root,runtime,state,driver}` separates a
  system root, installed runtime, state, and driver under `fs/path`. `temp`
  covers the temporary location and `temporary-artifact` a named file there.
  Recognizing a path leaves the kind of access open.
- `fs/directory/{create,readdir,traverse}` covers creation, one listing, and
  recursion. `fs/search` adds a selection test. `fs/path-ops` acts on the
  pathname itself. `fs/file/copy` can distinguish a call, a command, or evidence
  binding the source and destination.
- `mem/alloc/{heap,virtual,unified}` follows the kind of memory obtained.
  `mem/{map,unmap,resize,free}` tracks mapping and lifetime. `mem/protect`
  changes permissions. Fileless storage created by `memfd_create` belongs in
  `mem/anonymous/create`. A later execution claim needs a transfer of control.
- `hardware/input/keyboard` separates hooks, polling, layout, and synthesized
  input. `hardware/display/screenshot` distinguishes a display capture from a
  window capture. Displayed page content belongs under `ui/graphics`.

#### Processes and code

- [process](micro-behaviors/process/) owns execution contexts, their lifecycle,
  descriptors, coordination, and interpreters. Choose the result when a command
  invokes another facility. A command that reads repository history is revision
  control even when a subprocess runs it.
- Unresolved clone flags belong in `os/syscall/clone`. A bare `execve`
  symbol is a reference to replacement. Describe how the rule recognizes it.
- Windows Script Host has a home under `process/interpreter/wsh`. Handing source
  text to a child interpreter belongs under
  `process/deploy/interpreter-command`. Dispatching a URL by scheme belongs
  under `communications/url/open`. A desktop opener with an unresolved target
  belongs under `os/handler/open`.
- Generating code without invoking it belongs in `metaprogramming/generation`.
  In-process hosting belongs under `process/interpreter/runtime`.
- [metaprogramming](micro-behaviors/metaprogramming/) covers inspection,
  generation, and transformation of program structure. Reflection can inspect,
  resolve, or invoke a member. An AST used by cleave is a matcher implementation
  detail.
- [dylib](micro-behaviors/dylib/) covers native library loading, unloading,
  lookup, and enumeration. Loading a language module belongs under `os/module`.
- [revision-control](micro-behaviors/revision-control/) owns repository history,
  changes, references, and publication. A forge SDK dependency can indicate
  access to the forge API. Claim a repository read or write when the matcher
  identifies that action.

##### Execution contexts

Under `process`, first ask what starts or changes. A thread, fiber, child
process, and replacement image have distinct destinations.

- `thread/create` starts a local thread. `fiber` concerns a fiber. `create/fork`
  clones the process. `replace` covers exec-family replacement.
- `create/shell` requires shell interpretation. `create/path-execution` covers a
  shell launching an explicit executable path. `create/variable` selects the
  child executable dynamically. `create/shell/variable-command` leaves shell
  builtins possible.
- `create/subprocess/{configure,launch,capture}` follows the child object. A
  prepared start-info object supports configuration. Capturing child output
  selects `capture` over a generic launch. `create/exec` covers process creation
  APIs. `create/cmdlet` covers a process-starting cmdlet.
- `interpreter/eval` separates a required file (`source`), code built and
  invoked (`constructed`), hidden dispatch (`indirect`), Python builtins
  (`python-builtins`), and direct evaluation (`direct`). Decoding alone
  establishes no evaluation. `deploy/interpreter-stdin` requires a handoff to an
  interpreter's input.
- `stdio/{configure,read,write,relay}` requires an identified standard stream.
  `fd` owns descriptor operations and `tty` terminal operations. `sync` owns
  synchronization. A mutex proves single-instance behavior only when used to
  enforce it.
- `hook` and `inject` describe mechanisms. Choose a separate objective for a
  required result such as gaining authority. Preserve the neutral mechanism for
  other consumers.

Under `metaprogramming/reflection`, `inspect` reads class or member details,
`resolve` finds a member, and `invoke` calls it. `dylib/lookup` resolves a
native symbol. `os/module/load/{name,path,memory,class}` follows the loader's
input. `revision-control/git/{read,write,transfer,configure}` follows the
repository operation even when a shell supplies the interface.

#### Host and user interfaces

- [os](micro-behaviors/os/) owns host services without a more specific facility.
  Choose the affected resource, such as a service, account, privilege, or
  registry key.
- Under `os/registry`, a known purpose of the key narrows a read or write. Under
  `os/env`, use the variable's meaning before the access verb, including for
  writes. `BASH_ENV` and a `NODE_OPTIONS` preload setting are runtime
  configuration even inside a CI attack. A CI-issued secret and CI job metadata
  differ.
- [time](micro-behaviors/time/) owns clocks, waits, elapsed time, and in-process
  scheduling. Registering an OS task belongs with the scheduler. Unwanted
  reactivation through that task can support persistence.
- [ui](micro-behaviors/ui/) covers controls, windows, menus, help, and graphics.
  A web view is a presentation surface. Deception needs evidence of how the view
  is used.
- [browser-extension](micro-behaviors/browser-extension/) covers extension-host
  actions, tabs, management, and lifecycle. Messaging and HTTP retain their
  protocol homes. A manifest's grant of host access belongs under
  `metadata/permission`.

##### Host surfaces

- In `os/registry`, use the subject of a known key, such as `autostart`,
  `credential`, `policy`, or `service`. When the subject stays open, choose the
  operation. A Run key reference and a write configuring reactivation support
  different claims.
- In `os/env`, use `credential` for secret-bearing variable names or access.
  Refine by the supported subject: `ci`, `cloud`, `database`, `registry`, `vcs`,
  or `service`, or by a selected value's kind (`key`, `token`, `password`).
  Generic credential-name tests stay in `credential/secret`. A name reference
  does not establish a read or theft. Use `runtime` for loader configuration,
  `path` for a location, and `cicd` for job metadata. Other settings belong in
  `config`, refined by `application`, `service`, `package`, `cloud`, `database`,
  `locale`, `cluster`, `telemetry`, `redaction`, or `session` when known.
  Use `read`, `write`, `test`, or `enumerate` when only the operation is known.
  `read/current` accesses the current process environment; `read/process`
  selects another process's environment. `enumerate/entries` observes the
  environment table; `enumerate/filter` selects entries by a predicate.
  `output` covers environment rendering,
  serialization, and pipelines; `release` covers environment-block cleanup.
- Under `os/telemetry/logging/llm`, use `content` for prompt, response, or tool-content logging settings and capture, and `session` for agent-session, transcript, PTY recording, and activity telemetry.
- `os/autorun` distinguishes a task's action, principal, trigger, registration,
  and configuration. `os/service` covers service creation, start, stop, query,
  and dispatch. `os/kernel/driver` covers driver loading.
  `os/application/target` groups named target applications by their function.
  Mentioning a browser in a target list does not identify the scanned program.
- `time/{query,sleep,timing,schedule}` distinguishes reading a clock, waiting,
  testing elapsed time, and scheduling. An analysis-specific timing gate can
  indicate an objective.
- `ui/help/{command,interaction,account,message,navigation}` follows what the
  help explains. `browser-extension/{action,lifecycle,management,tabs}` covers
  extension-host surfaces. An extension that uses ordinary HTTP, storage, or
  messaging stays with the operation.

### [Objectives](objectives/)

Use an objective when the matched behavior can reasonably be read as serving a
particular attack purpose, even if a benign explanation remains. Name the fact
that suggests it. A program copying itself into a login startup folder can
suggest persistence. A file copy alone identifies a capability. State what was
observed and how it bears on the objective. Intent and successful execution may
both remain unknown.

#### Observation, acquisition, and export

- [discovery](objectives/discovery/) surveys an environment. Choose a branch by
  the resource surveyed, such as accounts, software, processes, network peers,
  or cloud resources. A single generic host query is a capability.
- [collection](objectives/collection/) gathers targeted material. Choose the
  source, such as input, clipboard, screenshot, audio, or selected files.
  Credential acquisition and export add distinctions of their own.
- [credential-access](objectives/credential-access/) acquires authentication
  material. Decide first whether the mechanism is phishing, cracking, or live
  interception. For stored secrets, choose the immediate source. Cloud
  credentials read from the environment belong with environment access. A
  password read from a browser database belongs with the browser even if a
  keychain key unlocks it.
- When a phishing page collects and then redirects, collection wins. A page
  that takes both a password and a one-time code belongs with MFA.
- [exfiltration](objectives/exfiltration/) requires evidence of acquisition or
  content and a send. Distinguish an inferred transfer from a demonstrated data
  binding. A route string, a POST, or a hunting query that describes theft
  supplies too little alone. Use a transport branch when the evidence
  distinguishes the carrier and leaves the item open.
- Under `exfiltration/stealer`, ask what item the rule requires to leave. A
  selected private key remains a key whether read from a file, environment, or
  keychain. A complete credential database is a record. A whole environment
  snapshot is configuration. A cookie becomes a session credential when the
  evidence identifies its authentication role.
- Alternatives spanning passwords and tokens establish a secret value of
  unresolved kind. Two required, independent item families can establish
  `multi-item`. A screenshot import beside a password exporter establishes only
  one export. Preserve the broad claim when dividing its branch. See
  [Leaves](#leaves).

A host profile sent by webhook during package install belongs under
`exfiltration/stealer/system-info/profile`. The webhook and install hook remain
supporting evidence.

##### Acquisition keys

- `discovery/{account,host,system,process,network,cloud}` follows the survey.
  `host` covers installed software and security products, `system` the machine
  and OS, `process` running programs.
- `collection/keylog/{hook,polling,device,terminal}` requires recording context.
  Use `collection/keylog/config` for settings that enable or schedule keylogging
  when the capture API is unspecified.
- Use `collection/file-targeting` for selecting files and
  `collection/file-copy/sensitive` for copies selected by sensitive roots or
  names. Generic file copying stays under `micro-behaviors/fs/file/copy`.
- `collection/file-targeting/font-api` requires a font-reading API targeting a
  non-font file. A system file requested through a font API meets the boundary.
  Ordinary font reads belong with the font API capability. Transfer and
  credential theft require additional evidence.
- In `credential-access`, distinguish `capture` of a live secret from `cracking`
  a verifier. For stored credentials, `keychain` includes OS key stores,
  `credential-manager` password blobs, `env` process variables, and `cloud` a
  cloud secrets service. Process memory belongs in `memory`, an offline SAM in
  `registry`. A known application database wins over its generic file or
  registry container.
- Under `credential-access/capture`, `api-hook` requires interception
  of a credential-handling API or method, including callbacks that copy its
  arguments and entry points that install the hook. Direct form reads, input
  prompts, accessibility reads, and touch reconstruction stay in `input`.
  A method name or credential marker alone does not establish interception.
- In `credential-access/phishing`, `landing` collects, `redirect` forwards, and
  `login-redirect` forwards to a tokenized login. Use `mfa` for one-time-code
  capture, `mfa-relay` for credential relay, `webview-wrapper` for a phishing
  app's embedded browser, and `link-deception` for a disguised destination.

##### Export keys

Read paths here relative to `exfiltration/stealer`. First identify the form that
leaves. Refine a selected secret by kind, a record by store, and a file by what
selected it.

- `credential/value/{password,token,session,key,recovery-secret}` covers
  selected values. `credential/value/ci-token` identifies a GitHub Actions
  token, `credential/value/ci` another CI secret.
- `credential/{browser-record,keyring-record,record}` covers whole stores or
  records. `credential/wallet/record` covers a serialized wallet record.
  `credential/file` requires selection of secret-bearing files. A chosen output
  filename supplies no evidence about their contents.
- `credential/value/environment` requires selected secret values from the
  environment. `credential/value/payload` requires credential fields in the
  exported data. A bulk environment snapshot is configuration.
- `credential/sweep` requires collection across credential sources or a
  search for credential material. `credential/archive` requires packaging the
  credentials. `credential/memory` requires process-memory material.
- `credential/wallet/key` requires wallet key material. A serialized wallet
  remains a record. Use `credential/value/key` when the matcher establishes a
  key without requiring a wallet.
- `configuration/environment` covers an environment snapshot. In
  `credential/environment`, `file-source` reads settings on disk,
  `current-process` reads this process, and `other-process` reads another. A
  selected private key still belongs with the exported key.
- `application-state/{browser-state,cookie,chat}` covers state whose content the
  rule does not narrow to a secret. `system-info` distinguishes host profiles,
  host-user pairs, hostnames, account inventories, and network or software
  inventories. `account-identity` covers an online identity.
- Under `system-info/host-user`, `callback` covers host or user information
  sent to a remote receiver. `query` requires that information in a URL query,
  `raw-socket` requires a direct raw socket, and `build-hook` requires the
  transfer to execute during a package build or installation hook, grouping the
  same build-time evidence across package ecosystems.
- `file`, `directory-listing`, `directory-tree`, `source-code`, and
  `command-output` describe distinct exported items. `media` covers sound,
  images, and visual streams. `financial/payment-card` requires card data. Theft
  of two private keys still selects one item family.

Under `configuration`, use `appliance` for device settings, `project` for
project files, `runtime` for application runtime settings, and `pipeline` for
CI definitions. Under `application-state`, `extension-storage` requires an
extension's persisted state and `webview-bridge` requires data from a hybrid
application bridge. `ui-text` covers exported text read from application UI
controls or accessibility trees; keyboard-event capture stays under `input`.
Browsing histories and navigation reports belong under `activity`.

A transport-specific query observation belongs under `exfiltration/http/query`
when the carrier is part of the claim. Its `file-content` child requires bytes
read from a file. A hostname sent in a query belongs in `host-profile`. Keep an
endpoint, a secret read, and a send as separate observations if their
relationship cannot support the proposed theft.

Under `exfiltration/http/agent`, distinguish `project-export` for files or
workspace data, `credential-usage-export` for credential or usage reporting,
`instruction` for agent context, and `service-relay` for a service-specific
relay whose payload is unresolved.

#### Activation, control, and reactivation

- [execution](objectives/execution/) covers attack-specific activation. A
  payload chain needs acquisition or staging and likely activation. File by
  the sink. Cite the transport, encoding, and trigger.
- Staging without activation belongs under `execution/staging` when its attack
  purpose is supported. Describe what is reconstructed, extracted, acquired, or
  stored. An updater performing the same neutral deployment belongs under
  `micro-behaviors/process/deploy`.
- Extraction decides when a fetched archive member is unpacked and launched.
  A runtime sidecar and an install hook can activate the same kind of file.
- A reusable operator request-to-command surface belongs under
  [command-and-control](objectives/command-and-control/). Distinguish tasking,
  beacons, channels, reverse shells, and backdoors by the control they provide.
  Activating one acquired payload establishes a different result.
- [persistence](objectives/persistence/) requires evidence directed at durable,
  unwanted reactivation. Choose the reactivation event, then the firmware,
  login, or system surface that implements it. The registry hive and script
  language are secondary. Describe an autorun reference as a reference.
- [lateral-movement](objectives/lateral-movement/) requires reaching another
  system. Remote installation, credential reuse, and exploitation differ. A scan
  surveys possible peers. A host parameter can designate the local machine.
- [privilege-escalation](objectives/privilege-escalation/) requires a crossing
  to greater authority. Identify the boundary and mechanism. Requested
  permissions, privileged API names, and process injection alone leave that
  crossing unestablished.

##### Activation and control keys

- `execution/payload` follows the sink. Use `process-inject` for execution in
  another process, `image-map` for a local image mapped for execution,
  `memory-branch` for local transfer into executable memory, `module-load` for a
  loaded module, `script-eval` for source evaluation, and `interpreter-stdin`
  for source passed to an interpreter by stdin.
- Under `execution/payload/interpreter-stdin/network`, `shell` covers fetched
  content passed through a shell pipeline or shell command. `interpreter`
  covers CLI pipelines that feed a language interpreter such as Node, Python,
  or Perl. `stream` covers application APIs that supply response data through
  an interpreter's stdin. Classify by the required transfer mechanism, not the
  programming language or package ecosystem. Calendar-triggered delivery stays
  under the sibling `calendar` branch.
- In `execution/payload/module-load`, prefer `network` for fetched input, then
  `embedded` for a resource, `transformed` for reconstructed input, and `input`
  when origin remains open. Loading a decoded network response still identifies
  the network source.
- Under `execution/payload/file-exec`, `command` requires shell-mediated launch,
  `spawn` a child-process API, `replace` image replacement, and `installer` an
  installer transaction. The `detached` children distinguish
  `archive-extraction`, `remote-download`, `install-hook`, `runtime-loader`, and
  `embedded-stage`. An encoded executable launched by a required preinstall hook
  belongs with the hook.
- `execution/staging/reconstruct` requires preparation of an executable stage.
  `acquire` covers acquisition, `http` HTTP-specific staging, `store` placement.
  `execution/interpreter/document/{macro,addin,command,pdf,xml}` names the
  activation surface. A document with an embedded URL alone has document and URL
  facts.
- `execution/exploit/conversion-parameters` requires a script API that lets
  caller-supplied conversion fields override the source and destination. An
  explicitly overridden destination distinguishes this from archive-member path
  traversal. Ordinary conversions and saves belong with their own operations.
- `privilege-escalation/exploit/maintenance-helper` requires command injection
  through a privileged maintenance helper. Routine maintenance inputs and
  standalone shell execution belong with their respective capabilities.
- Under `command-and-control/reverse-shell`, test for the required relay in
  this order. Use `dev-tcp`, `netcat`, `pty`, `fd-redirect`, then
  `stream-bridge`. Inherited descriptors and explicit copying between streams
  are different mechanisms.
- In `command-and-control/backdoor/webshell/request`, loading code wins over
  evaluation, which wins over OS command execution. Use `code-load`, `eval`, or
  `command` accordingly. With only the input surface, choose `query`, `body`,
  `form`, `header`, `cookie`, or `parameter`. In a tunnel, SOCKS framing wins
  over HTTP relay, which wins over a generic proxy.
- Under `persistence/login` choose `registry` for a Run key even in HKLM,
  `startup` for a startup item, `winlogon` for Winlogon, `xdg` for XDG
  autostart, and `shell` for a shell profile. Under `persistence/system` choose
  the service, driver, init, cron, WMI, editor, or Git surface. `service/loader`
  identifies a service loader such as an svchost DLL. A process that merely
  detaches belongs in `micro-behaviors/process/daemonize`.

#### Concealment, damage, and trust

- [anti-analysis](objectives/anti-analysis/) detects or interferes with
  analysis. Choose the environment probed or the check performed. A VM artifact
  can distinguish a VM probe. A sandbox score or an exit conditioned on that
  score has a different home.
- [anti-static](objectives/anti-static/) obstructs recovery of code or data. An
  unpacking mechanism or deliberate obfuscation can support the claim. High
  entropy is a measurement. A stock packer stub can identify how the artifact
  was built.
- [evasion](objectives/evasion/) covers bypass, blinding, concealment, or
  masquerade. An attempt to bypass an agent's approval gate differs from a user
  authorizing an action. Hiding activity from a defender differs from stopping
  its service.
- [impact](objectives/impact/) groups harmful effects such as disruption,
  destruction, secure erasure, extortion, infection, spam, and resource abuse.
  Stopping a defender belongs under `impact/degrade`. A wipe tied to a
  mount-derived device requires the selected device to be the write target.
  Ordinary cleanup can also delete.
- [supply-chain](objectives/supply-chain/) requires abuse of component
  selection, distribution, or build trust. A substituted legitimate input
  supports `trojanized`. Concealment tailored to package inspection supports
  `hidden-payload`. Deceptive naming or provenance supports `impersonation`. A
  package hook that steals credentials still has credential theft as its result.
- Under `supply-chain/impersonation/registry/publish`, use `listed` for exact
  threat-listed release coordinates, `campaign` for coordinated spam or
  reward-farming evidence, `custody` for registry ownership and removal
  history, `install-canary` for disclosed harmless install probes,
  `metadata-snapshot` for registry snapshot observations, `placeholder` for
  metadata-only packages, and `removed` when removal is paired with a retained
  hook. A name and affected version identify a listed release, not the
  package's behavior.
- `supply-chain/security-hold` records an explicit policy verdict on a held
  dependency, including an inert replacement. Require authoritative registry
  evidence or both npm version `0.0.1-security` and the canonical holder
  repository in the same manifest. Identify the affected dependency. Its
  declaring package can carry the finding without earning a hostile verdict
  on its code.

##### Objective boundaries

- `anti-analysis/sandbox-detect` distinguishes `hostname`, `score`, and
  `enforcement`. `anti-static/{pack,obfuscation,polyglot}` distinguishes
  unpacking that conceals code, deliberate transformation, and conflicting
  interpretations of one file.
- `evasion/security-bypass/llm` separates bypass of an approval gate
  (`approval`) from an instruction-priority override (`override`).
  `evasion/hijack-execution-flow` needs diversion. A greater-authority result
  can support `privilege-escalation/hijack-execution-flow`.
- In `impact`, distinguish `wipe` for secure erasure, `destroy` for destructive
  deletion, `ransom` for extortion, `dos` for exhaustion, and `infect` for
  insertion into a host file. `degrade/firewall` separates disabling the
  control, changing rules or policy, and stopping the service. Under
  `ui/manipulation/traffic`, `search-provider` takes search-result rewriting and
  `navigation` takes other redirects.
- Under `impact/crypto-manipulation/hijack-transfer`, `address` covers
  destination recognition, replacement, and routing, including changes through
  page, clipboard, request-body, or RPC-endpoint handling. `transaction` covers
  wallet transaction interfaces, signing authority, reward transactions, and
  signing relays. Use `address` when a matcher requires destination replacement.
  A wallet provider hook with unresolved destination belongs in `transaction`.
  Describe a provider request assignment as an interface observation.
- In `lateral-movement`, a required remote exploit, password guess, or hash
  reuse goes in `exploit`, `brute-force`, or `pass-the-hash` before a generic
  protocol branch. `privilege-escalation/token-manipulation` and
  `elevation-control` under the same objective distinguish two ways of crossing
  an authority boundary.
- Under `supply-chain/trojanized`, `build-pipeline` requires a compromised build
  and `ci-pipeline` the CI trust boundary. Under `trojanized/app`,
  `config-injection` covers application settings surfaces, while
  `build-config-injection` covers malicious behavior placed in JavaScript build
  configuration files. Under `hidden-payload` in
  `supply-chain`, choose `remote-loader`, `native-extension`, `encoding`, or
  `update-service` by the mechanism that defeats package inspection.

### [Metadata](metadata/)

Use metadata only when the matched fact itself gives no clue to a capability or
attack objective. File size, ELF class, and the number of imports describe the
artifact. A manifest can supply any kind of evidence. A dependency count is
metadata. A dependency on a crypto provider indicates crypto capability.

- [arch](metadata/arch/) records a parsed instruction-set or ABI target.
  [binary](metadata/binary/) records properties of headers, sections, symbols,
  instructions, linking, resources, layout, and provenance. Section entropy
  belongs with the section.
- [file](metadata/file/) covers whole-file format, magic, size, entropy, and
  representation. An encoded blob is a property. A decoder is a capability. A
  retained file profile needs one stated artifact property, a defined relation
  among its facts, and a benign control. Generic string and literal buckets are
  closed.
- [image](metadata/image/) measures decoded pixels, segments, and trailing
  layout. [document](metadata/document/) describes structured document parts.
  Code in a document keeps the subject its required behavior supports.
- [filename](metadata/filename/) describes the scanned basename.
  [path](metadata/path/) describes the scanned location.
  [archive](metadata/archive/) describes a container or an entry in its member
  table. A pathname mentioned in source belongs with the referenced resource.
- [import](metadata/import/) records import structure. Cleave also emits raw
  import facts here. An authored trait that uses one of those facts goes with
  the capability or objective it indicates. An exported ABI distinctive to the
  library's own binary can identify that shipped library.
- [lang](metadata/lang/) owns language, compiler, runtime, syntax, literals, and
  wording. Use source syntax or vocabulary when the observation establishes only
  a form or a word. Credential vocabulary can occur in a password setup guide.
- [build](metadata/build/) records marks of a build or transformation.
  [installer](metadata/installer/) records builder and plugin marks in an
  installer. A builder's own executable can earn a separate known-tool identity.
- [package](metadata/package/) records package properties such as version ranges
  and manifest structure. Interpret the contents of a field. A command in a
  lifecycle hook can identify an operation or suggest an attack objective.
- [registry](metadata/registry/) records package-registry facts such as release
  history or custody. Windows registry operations belong in
  `micro-behaviors/os`.
- [permission](metadata/permission/) describes declared authority.
  [hardening](metadata/hardening/) describes a mitigation or its absence. A
  permission grant alone establishes no access.
- [vendor](metadata/vendor/) records vendor provenance.
  [signature](metadata/signature/) distinguishes verification state, signer
  claims, certificate structure, and signed properties. A subject or issuer name
  read as text is a claim. Describe it as such. A verified chain can
  authenticate a signer. Third-party attestation still leaves the third party as
  the software's author. Use verified evidence when a signer identity is grounds
  for suppression.
- Under `signature/certificate/issuer`, an exact verified-chain thumbprint can
  identify a particular CA. A chain's presence or length identifies structure.
  Reading an issuer name as text belongs under `signature/claim`.
- Cleave emits raw entitlement keys under `metadata/entitlement`. YAML under
  `signature/entitlements` can interpret them. Reuse engine findings by ID.

#### Artifact property keys

- `filename/identity` holds a conventional basename or a closed set of names.
  `filename/name-form` permits an open spelling, version, or hash. Required
  parent components move the observation to `path`. In a container table use
  `archive/member/{filename,path,extension,size,time}` for the recorded field.
  Member order or arrangement belongs under `archive/layout`.
- `binary/{header,section,symbols,instruction,resource,linking,layout}` follows
  the measured part. `binary/resource/label` names a resource.
  `binary/layout/embedded` describes embedded layout. A compiler recorded in an
  artifact belongs under `lang/compiler`. A transformation evident in produced
  files belongs under `build/{bundler,packer,minifier,transpiler}`.
- `file/entropy` measures the whole byte sequence. `image/pixel` measures
  decoded image data. In `file/catalog`, distinguish detection rules
  (`pattern-rules`), threat records (`threat-pattern`), policy, network data,
  file types, packages, and vocabulary. Classify the catalog before a literal
  appearing inside one entry.
- Under `lang/source`, choose `syntax` for a grammatical relationship, `naming`
  for an identifier, and `literal` for a value. Within `syntax/assignment`, a
  member target, call on the right, assigned name, and assigned value have
  separate homes. `literal/fragment/{single,sequence}` distinguishes one
  fragment from a required sequence. A required call to a decoder still belongs
  with decoding.
- `package/name` records package identity fields. `package/description` records
  what the publisher says the package does. A claim in accompanying
  documentation belongs under `package/documentation/claims`. In
  `package/scripts`, `lifecycle` and `build` describe declared triggers, while
  `command` describes the command text.
- `package/dependencies` covers structural facets including `name-form`,
  `source`, `range`, `reconciliation`, `presence`, `count`, and `composition`. A
  version range, disagreement between two records, and size of the dependency
  set are different facts. A required crypto provider still identifies a
  capability even when a manifest supplies the evidence.
- Under `signature/claim`, choose `signer`, `subject`, `issuer`, or `id` for a
  signer-chosen name. Under `signature/certificate/issuer`, `microsoft` and
  `attestation` require the corresponding chain evidence, and `chain` measures
  chain structure. `signature/script` records signature markers in a script. A
  marker alone leaves verification open.

### [Well-known](well-known/)

Reserve this kingdom for software commonly recognized by engineers or security
analysts. For tools and libraries, ask which executable or library the project
ships and what identifies the scanned file as that artifact. Look up the
project's names and aliases before creating a home.

A distinctive export surface can identify OpenSSL's own libcrypto binary. An
application importing libcrypto has a crypto capability. A script that invokes
the OpenSSL CLI belongs with the operation its arguments indicate. A product
name in documentation identifies a mention. None of those consumer artifacts
earns the library's identity.

- [malware](well-known/malware/) holds recognized families. Choose one defining
  role per family, such as downloader, RAT, stealer, or worm. An actor or
  delivery channel belongs in the description. [unwanted](well-known/unwanted/)
  holds recognized adware, PUA, and riskware families.
- [lib](well-known/lib/) groups libraries, frameworks, and runtimes by function.
  A protocol client belongs with networking, a server framework with web, and a
  codec with media. A cloud control-plane SDK belongs with cloud even for one
  vendor.
- [dual-use](well-known/dual-use/) groups legitimate products whose ordinary
  purpose is relevant to abuse, including remote administration, tunneling, and
  transfer.
- [game](well-known/game/) includes game platforms and game-specific
  modifications.
- [tool](well-known/tool/) groups developer, administrator, and analyst
  utilities by function. A compiler CLI is a development tool. A C2 platform's
  operator console can identify the tool. An implant claim needs implant
  evidence.
- [app](well-known/app/) groups end-user applications and platform components.
  An IDE is a development app. Deployed protection and an analyst's forensics
  utility serve different users.

Test an identity rule on a shipped binary or library and on a client that uses
it. The client must miss. For a builder, also test a file it produced. Every
passing combination must distinguish the project's own artifact. Imports,
command lines, and build marks can survive in thousands of clients.

#### Entity classes and functions

- Under `malware`, use the family's defining role. Roles include `backdoor`,
  `botnet`, `downloader`, `dropper`, `exploit`, `keylogger`, `miner`,
  `ransomware`, `rat`, `rootkit`, `stealer`, `virus`, `webshell`, and `worm`.
  Use `trojan` when the evidence supports no narrower role. Give a family one
  canonical home even when it has several capabilities.
- Under `lib`, `format` parses or serializes, `data` queries or stores, and
  `media` processes media. `platform` integrates an OS or device, `runtime`
  supplies execution or FFI, and `native` supplies an ABI or allocator.
  `testing` owns assertions, mocks, and fixtures. `stdlib` extends a language's
  standard library. A small domain library still has a domain.
- `dual-use/{access-control,credentials,packaging,remote-admin,transfer,tunnel}`
  follows the shipped product's primary function. Under `tool/offensive`,
  `command-and-control` identifies operator software, `reconnaissance` names a
  discovery tool, and `web-assessment` names a web assessment tool.
- `app/development` holds an IDE, `tool/development` a compiler CLI.
  `app/security` covers deployed protection, `tool/detection` an analyst's
  scanner, and `tool/forensics` an examiner's utility. `app/infrastructure`
  administers deployments, `app/network` serves ordinary network users.

## Directory budgets and placement contracts

A directory in the tree may still hold legacy rules. Check its current
placement contract before copying a neighbor. For example, generic
`metadata/file/string` and `metadata/file/literal` are closed to new rules.
When a documented destination is still proposed, check validator admission
and the shape of the tree before moving definitions.

### Leaves

Put definitions in leaves. This applies to atoms, composites, and aliases in all
four kingdoms. A leaf may hold several trait YAML files. No descendant of a
directory holding trait YAML may also hold trait YAML. One rule-bearing
grandchild is enough to make its ancestor a branch.

A branch remains useful as a selector. The directory supplies the ID prefix. The
filename can distinguish languages within a rank. `directory::id` selects a
rule. A directory reference selects a set of rules. Ordinary positive directory
references skip exception composites.

Place the broadest observation before splitting a leaf. Name the evidence common
to its alternatives. If the matcher establishes a distinct common observation,
file it under that observation. If the proposed children leave no meaningful
home for the parent observation, revise the partition or keep the subject as a
single leaf. Copying a rule into each possible subtype counts it several times.

### Splits and names

Review a leaf at 72 rules. Keep new and reorganized leaves below 80 atoms and
composites combined, across all files and criticalities. Check both the source
directory and the ID namespace. A larger existing leaf is debt. An exception to
the population budget needs an audit and explicit approval.

Start at the common parent. Inspect its siblings for duplicates, misplaced
rules, and past overflow. A new child needs a stable distinction, a nearest
alternative, a deciding example, and a home for cases that fit neither. A small
subject can keep distinct operations in IDs and descriptions.

Choose a noun for a resource or a verb for an operation. Name resources in the
singular, such as `credential`, `token`, or `secret`. Use the same service
name wherever a branch splits by service: `os/env/secret/<service>` and
`fs/path/credential/<service>` share `cloud`, `vcs`, `registry`, `database`,
and `ssh`. Different names mean different evidence. An `os/env` `ai-provider`
key calls a model API, while an `fs/path` `ai-agent` store holds an agent
CLI's login. A name can carry its admission test, as `generic-basename` does.
Read the full path aloud. Remove a rank that repeats its parent. `misc`, `other`, `common`, and
`unspecified` name the difficulty of filing. `suspicious` names a judgment. `regex` names a
matcher. None tells the next author what evidence belongs there.

Directory prefixes and criticality feed downstream features. A duplicate matcher
can count one observation twice. Preserve real distinctions even when the
extractor reads only the kingdom and its next two ranks.

### Scope and validation

Set `for:` and `platforms:` from the matcher and its effective defaults. Use
`platforms: [all]` only in admitted directories for facts whose meaning holds
across operating systems. A manifest field can meet that test. An OS-specific
path retains its platform. Use reviewed broad scopes only for the directory and
platform set they cover.

At four or more effective platforms, check the reviewed platform sets. A move
preserves expanded file types as well as matchers. For example, the `source`
group excludes Ruby. A source-only replacement can silently lose a Ruby
detection. Recheck the matcher's file-type cap and the compatibility of
composite legs with their scope after a move.
[Targets](RULES.md#targets) and [scope and proximity](RULES.md#scope-and-proximity)

The authoring budget leaves room below cleave's 93-rule ceiling. Strict
validation also checks width, depth, names, and fragmentation. More than 150
immediate children triggers a width finding. Depth is counted below the kingdom
and reviewed past five ranks. In behavior and objective branches, ten or more
child subtrees averaging eight or fewer rules trigger review. A strict run fails
on these layout findings. Use the evidence in the rules to decide how to divide
the branch.

### Moving rules

1. Account for each old rule. Preserve its matcher, effective file types,
   platforms, and exclusions. Record any intended detection change separately.
2. Check exact references and directory selectors. An old selector may still
   resolve while losing a moved rule. A new selector may include extra members,
   broaden a suppression, or count a single fact twice. Search across the
   checkout, including suppressions and downgrades. If a move or retirement
   changes coverage of a matcher-qualified source path in Cleave's
   `BROAD_FILETYPE_ALLOWLIST`, coordinate the corresponding entry update
   or removal with the engine maintainer. Validation flags entries whose
   source path prefix no longer matches any loaded trait.
3. Test a positive and the nearest miss for the distinguishing claim. Where two
   claims may coexist, test both together. Label a fixture by what that file
   shows on its own. Use an archive fixture for a package-level claim and
   follow the [fixture layout and storage requirements](README.md#validation).
4. Compare the findings, scope, and selector membership before and after. Run
   `make validate` for standalone changes. A passing run checks the machinery.
   The branch description must still let another author place the next rule.
