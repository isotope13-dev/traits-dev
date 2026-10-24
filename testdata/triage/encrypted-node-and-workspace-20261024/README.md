# Native mapper, encrypted Node RAT, and workspace review

The verdicts apply to the supplied bytes and available context. External names,
scanner scores and collection labels were leads, not evidence of functionality.
`scan-comparison.json` records the original paths, changes and classifier output.

| SHA-256 prefix | Identification | Verdict | Hostile before → after | Suspicious before → after | Classifier before → after |
|---|---|---|---|---|---|---|
| 13371592ef5c | Virtualized x64 remote PE mapper | MALICIOUS | 0 → 0 | 2 → 2 | benign → benign |
| ed263d7dbabb | AES-wrapped PowerShell installer for a Node RAT | MALICIOUS | 0 → 1 | 1 → 3 | benign → hostile |
| 69e7b37e2ebd | Minimal VS Code workspace | BENIGN | 0 → 0 | 0 → 0 | benign → benign |

Each original has one file unit and no archive members. The reconstructed PE
and manually decrypted JavaScript are analysis artifacts, not original archive
members. Original hashes were verified in the final scans. The model warns
that its v18 feature specification predates the engine's expected v21.
Probabilities alone were not interpreted as verdicts: a live native scan prints
`scan benign confidence=0.978`; the PowerShell route now reports class 2.

The native executable is an unsigned PE32+ GUI image with empty on-disk .text
and .data sections, renamed executable packed sections, malformed resource
metadata and a 48,195-byte high-entropy overlay. The overlay was independently
confirmed with pefile; Rizin's initial overlay=false indication was incomplete.
Rizin tracing follows entry RVA 0x7c4719 into the register-saving VM entry at
RVA 0x7d29ca. Unicorn emulation of the supplied bytes, with synthetic Windows
exports and API stubs, restored 105,220 nonzero .text bytes. No real Windows
API calls or network actions were performed by that emulation.

The unpacking path checks IsDebuggerPresent, CheckRemoteDebuggerPresent,
NtQueryInformationProcess class 0x1e and kernel debugger information; it calls
NtSetInformationThread with class 0x11 and checks code using a CRC transform.
The restored native path at RVA 0x3430 prepares SeDebugPrivilege, obtains a
resource, queries the remote switch configuration and invokes RVA 0x2fa0 with
the resource buffer. That routine obtains a helper process, allocates remote
memory, copies a 0x540-byte mapper from RVA 0x2d000 plus payload and parameters,
and calls the resolved NtCreateThreadEx pointer at RVA 0x33cf. The mapper
validates MZ, PE and AMD64 headers and walks image sections. The thread API
name is masked in original .rdata and reconstructed by XOR; its existing
reference and concealment detections remain accurate. Other calls retain
virtualized trampolines; the reconstructed image is not a complete original
payload recovery.

The configuration URL is
`https://rule.110route.com/api/index/getSwitch?barid=` followed by the embedded
identifier. Forager attempted the actual configured URL; it received HTTP 200
responses with only two bytes and recovered no useful configuration artifact.
The endpoint's name does not establish a RAT family or a malicious server.
The verdict is tipped by concealed resource mapping into a helper, remote
gating, privilege preparation, randomized staging and anti-analysis together,
with no verified publisher, installer, authorized management purpose or
operator context explaining them. Authorized protected management software
remains a possible alternative. IcedID and njRAT attribution is unproven.

The native hostile-coverage goal remains unmet. The original retains its two
supported suspicious concealment findings and every previous neutral finding.
The injection chain and anti-debug probes were investigated in restored code,
but their complete API/argument relationships are virtualized in the original.
No general static matcher for those relationships was established. Combining
the visible masked thread name, memory API table and packed layout would
support concealment, not three independent hostile actions. No such inflated
rules were added. The benign classifier result remains a miss.

The PowerShell script dynamically compiles a fragmented ShowWindow P/Invoke,
hides its own and successive parent windows until Explorer, checks for an
existing Node process, and uses a named global mutex. It downloads and expands
a configured Node v26.4.0 Windows archive if its local executable is absent.
It decrypts the embedded script using AES-256-CBC with the embedded key and IV,
writes it to USERPROFILE\\AppData\\Local\\Nodejs, then launches that same path
as a hidden Node child. Its separately decrypted argument is
`reservphotoinstay.one`; the decrypted mutex uses a global GUID name. These
values were recovered rather than inferred from the file's collection name.

The 370,125-byte JavaScript uses an RC4 string array, arithmetic constants and
a custom bytecode VM. Decoder-only execution in QuickJS recovered the string
array. The VM's binary reader was then used to parse both code-unit pools and
their encrypted constant pools. Stubbed execution of those routines confirmed:

- A TON account get_domain request supplies the authority for a `wss://.../w`
  connection. The account is configured in the program; the environment keys
  alone establish only configuration references.
- The handshake uses secp256k1 ECDH, HKDF-SHA256 and AES-256-CBC. The onMessage
  routine decodes and decrypts input, parses JSON and passes it to handleMessage.
- The dispatcher executes supplied JavaScript with `new Function(code)()`,
  invokes command execution with response callbacks, downloads and runs files,
  launches an FFI-enabled child for native payload handling, replaces its own
  script, and restarts. These are request-controlled effects, not merely method
  names resembling capabilities.
- A Run-key routine writes HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
  to start the same script through a detached hidden Node process. The stub
  trace records the constructed Set-ItemProperty command. Other routines
  collect OS, CPU, host, user, memory, MAC and Windows machine identifiers.

The stub environment supplied inert filesystem, process, crypto and network
objects; it did not contact the resolved C2, write a real Run key, execute a
received task or establish native payload success. The script has no supplied
legitimate product or operator authorization explaining its concealed remote
command interface and persistence. These behaviors tip MALICIOUS even though
its runtime download comes from nodejs.org.

The new original-file rule binds the written path to the child argument and
binds that same child's executable variable to a Node path assignment. It
also requires embedded Base64, a decryptor call, hidden child execution and
window hiding beside parent-PID access. Separate findings expose the staged
execution, concealment, REST output-file request and reordered/abbreviated
Add-Type member compilation. The hostile-count goal remains below three:
C2, Run-key persistence and native/CLR handling are encrypted inside the
original. The current facts extractor does not perform this AES decryption or
recover the VM's operation relationships. Manually decoded stages establish
the verdict but cannot make those plaintext behaviors match the ciphertext.

The decrypted JavaScript itself was scanned, including its automatically
extracted constant-string-table layer. Its main hostile/suspicious counts are
0/4 → 0/2; the derived layer is 0/3 → 0/1. Two environment-reference atoms were
misplaced under blockchain C2 and overstated as suspicious. They now live in
micro-behaviors/os/env/provider at notable, with unchanged patterns and scope;
their exact C2 consumer references were updated. The retained transport/control
composite still needs its other legs. A plain configuration control matches
the neutral atoms and does not trigger that composite. The decrypted script's
classifier remains benign (probability .973286 → .922851): this is another
coverage/classifier gap, not a reason to restore inaccurate intent signals.

The 60-byte workspace is valid JSON containing only folders:[{path:"."}] and
empty settings. It declares no task, command, URL, extension or dependency.
No companion project content was supplied, so this does not certify a project
that might elsewhere use this workspace. Collection from a malware-associated
project or a mislabeled repository artifact could explain its source label;
the record does not establish either explanation. The supplied file is BENIGN.
Its false Firefox omission finding came from testing absence of a Gecko field
without requiring Gecko settings. The corrected rule requires that context;
actual omitted-disclosure Firefox controls still match.

Other shared corrections retain supported observations: the duplicate
PowerShell Rijndael matcher was merged into its AES/Rijndael home; CryptoStream
read mode was moved to cipher capability and no longer claims AES decryption;
a PID-filtered WMI query is recorded as a process query instead of full process
enumeration. Unfiltered enumeration remains covered. Consumers were inspected
and updated, including the broad paste-exfiltration alternative. To keep two
full directories within their budgets, the unchanged fixed-length x86 copy
matcher was moved from encrypted-payload intent to memory copying, and the
unchanged AMSI/download/process co-occurrence composite was moved from payload
activation to AMSI evasion. Neither copy bytes nor unrelated API co-occurrence
establish the original placement's stronger claim. Focused controls retain
the AMSI attack and copy observation. No supported original attack finding was
lost; the PowerShell's three removed IDs are replaced by corrected facts.

Verification: `python3 testdata/triage/encrypted-node-and-workspace-20261024/check.py`
passes 26 fixture checks plus three Gecko truth checks. It includes three
existing service/cipher fixtures, variable renaming, mismatched paths and
runtimes, visible execution, absent parent hiding, read/write modes, filtered
and unfiltered queries, and AMSI positive/near-miss controls. The prior native
review's 18 controls also pass. A broader legacy registry runner encountered
an unrelated unchanged comment-syntax expectation; the relevant cipher/service
controls are explicitly included in the passing focused run. The final gate
is `make validate`.

Full scans, facts, AES plaintext, VM decoding scripts and pools, stub traces,
native disassembly, emulation script and reconstructed memory, and fetched
artifacts/provenance are under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/bad-analysis`.
