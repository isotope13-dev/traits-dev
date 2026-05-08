# cleave Taxonomy

A three-tier taxonomy following [MBC (Malware Behavior Catalog)](https://github.com/MBCProject/mbc-markdown) principles.

## Tiers

| Tier | Purpose | Criticality Range | MBC Equivalent |
|------|---------|-------------------|----------------|
| **Capabilities** (`micro-behaviors/`) | Observable mechanics — what code *can do* | component → baseline → notable → suspicious | [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
| **Objectives** (`objectives/`) | Attacker goals — why code *likely wants* to do something | component → baseline → notable → suspicious → hostile | [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions) |
| **Known Entities** (`well-known/`) | Specific malware families and tool signatures | component → baseline → suspicious → hostile | [Corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) |
| **Metadata** (`metadata/`) | Neutral file-structure properties — what a file *is* | component → baseline (occasionally suspicious) | — |

NOTE: atomic traits should be organized based on what they detect, not on what composite they serve. atomics and composites are often in completely different directories.

Traits rarely seen in legitimate software that have well-defined objectives should go within objectives rather than micro-behaviors.

## Criticality

| Level | Meaning | Tier Constraints |
|-------|---------|-----------------|
| **component** | Building block for composites; no standalone signal (e.g., string fragment `&cc=`). Filtered from terminal output unless a referencing composite fires. Always in JSON for ML. | Any tier |
| **baseline** | Common functionality; doesn't indicate program purpose (e.g., `mmap`, `stdio`, `read`). Always in output for ML. | Any tier |
| **notable** | Defines program purpose (e.g., `socket`, `exec`, `eval`). Capabilities that matter for differential analysis of supply-chain changes — i.e., anything an analyst would want to see "appeared" or "disappeared" between two versions — should be notable or higher: communications (HTTP, sockets, DNS, IPC), code execution (interpreters, eval, dynamic loaders), encryption methods (AES, RSA, ChaCha, KEM), encoding/decoding methods (base64, hex, custom alphabets), privilege escalation (sudo, setuid, capabilities), file access (read/write/delete on sensitive paths), registry access (Windows registry r/w), and persistence (cron, systemd, autoruns, launch agents). | `micro-behaviors/`, `objectives/`, `well-known/` |
| **suspicious** | Rarely legitimate; indicates possible malicious intent. | `micro-behaviors/`, `objectives/`, `well-known/`, `metadata/` (rare) |
| **hostile** | Clear attack pattern; no legitimate use. Requires precision >= 3.5. | `objectives/`, `well-known/` only — **never** `micro-behaviors/` |

## ML Feature Extraction

The ML pipeline extracts features from **subdirectory path + criticality**, not individual trait IDs. Each trait's directory path (up to 3 levels deep) combined with its criticality level becomes a feature dimension. This means:

- **Directory structure is the feature space.** A trait at `objectives/evasion/kernel-hide/rootkit/linux.yaml` with `crit: suspicious` generates the feature `evasion/kernel-hide/rootkit:suspicious`. The directory hierarchy directly shapes what the model learns.
- **Criticality is the signal strength.** Two traits in the same directory but at different criticality levels produce different features. A `suspicious` rootkit trait and a `component` rootkit trait are distinct signals.
- **Depth matters.** The pipeline uses up to 3 directory levels. Features aggregate at the deepest available level, so `evasion/kernel-hide/rootkit` is more specific than `evasion/kernel-hide`, which is more specific than `evasion`.

### Design implications for trait authors

- **Group related detections under the same subdirectory** so they aggregate into a single, strong feature. A directory with 10+ traits produces a robust signal; a directory with 1-2 traits produces a weak one.
- **Don't create single-trait subdirectories** when the trait fits an existing directory. `credential-access/browser/` (11 traits) is a strong feature; adding `credential-access/opera/` with 1 trait creates a weak feature that should instead be a file within `credential-access/browser/`.
- **Use technique-based directories.** Directory names should describe the behavior or method being detected, not the implementation language, platform, ecosystem, file type, malware family, or sample source. Use implementation details in filenames when they help readability, unless the technique itself is platform-specific.
- **Prefer concise, meaningful names.** Short directory names are easier to scan and produce cleaner ML features: use `exec`, `poll`, `proxy`, `shell`, `reflect`, or `stage` when they are clear in context. Do not shorten names so far that humans lose the technique meaning.
- **Avoid marker buckets.** Do not use `marker/` or `markers/` as directory names; name the behavior or technique being indicated instead.
- **Criticality assignment affects ML directly.** A trait bumped from `notable` to `suspicious` changes which feature it contributes to. Assign criticality based on the trait's actual detection confidence, not to manipulate features.
- **The 3-level depth limit** means `objectives/anti-static/obfuscation/string/encoding/` extracts as `anti-static/obfuscation/string` — the `encoding/` level is aggregated into `string/`. Plan directory depth accordingly. Avoid unnecessary intermediate directories (e.g., prefer `obfuscation/syntax/` over `obfuscation/source/syntax/`).

## Core Principles

### Single-Trait Rule

Unlike MBC, which allows one behavior to map to multiple objectives (e.g., Process Injection is both Defense Evasion and Privilege Escalation), cleave allows exactly **one trait per behavior**. Place it at the most specific location the evidence supports. Composite rules in other directories can reference the single trait to express multi-objective interpretations.

### Tier Dependencies

| Tier | Can Reference | Rationale |
|------|--------------|-----------|
| `micro-behaviors/` | `micro-behaviors/`, `metadata/`, `well-known/tool/`, `well-known/app/`, `well-known/lib/`, `well-known/game/` for false-positive exclusions only | Capabilities must not depend on objectives or malware families |
| `objectives/` | `micro-behaviors/`, `objectives/`, `metadata/`, `well-known/{tool,app,lib,game}/` (positive evidence allowed); never `well-known/malware/` | Objectives build on capabilities and other objectives. Legitimate-software identifiers are fine as positive evidence — the relationship runs `well-known/malware/ → objectives/`, not the reverse |
| `well-known/` | all tiers | Signatures can reference anything |
| `metadata/` | `metadata/`, `well-known/tool/`, `well-known/app/`, `well-known/lib/`, `well-known/game/` for benign context only | Informational properties must not depend on behavior or objectives |

**Capabilities must not reference objectives.** Capabilities are observable mechanics; objectives infer intent. If a `micro-behaviors/` rule needs an `objectives/` trait, either move the objective to `micro-behaviors/` (if it's actually a capability), refactor the dependency away, or move the whole rule to `objectives/` (if it's actually inferring intent).

**Capabilities must not use `crit: hostile`.** Hostile requires intent inference, which belongs in `objectives/`. Maximum capability criticality is `suspicious`. Validation rejects hostile capabilities.

**Neutral capabilities belong in `micro-behaviors/`, not `objectives/`.** A trait that detects a single API call, syscall, or keyword (fork, crontab, SetFileAttributes, getenv) is a capability — it belongs in `micro-behaviors/` regardless of which objective composite references it. Composites reference traits across directories. Component traits (`crit: component`) may appear in `objectives/` only when they are attack-context-specific fragments that have no meaning outside that context (e.g., Nemucod string pieces, default credential lists, supply-chain URL patterns).

### Directory Layout Convention

All tiers follow: `TIER/CATEGORY/BEHAVIOR/METHOD/platform.yaml`

- **`objectives/`**: `objectives/OBJECTIVE/BEHAVIOR/METHOD/` with technique-based directories and per-platform or per-ecosystem YAML files. Add sub-method directories when a method has many variants (e.g., string obfuscation techniques). Avoid platform, language, ecosystem, file-type, and family names as directories unless they are the technique being detected.
- **`micro-behaviors/`**: `micro-behaviors/CATEGORY/BEHAVIOR/METHOD/` (e.g., `crypto/symmetric/aes/ruby.yaml`, not `crypto/symmetric/aes.yaml`). If no specific method applies, group by syscall, protocol, or logical grouping. Directory names may be referenced by composite traits to match related rules.
- **Directory names** should be short, readable, and semantically useful. Prefer `exec` over `command-execution`, `poll` over `polling-command`, and `reflect` over `reflective-loader` when the parent path supplies enough context. Keep longer names when the shorter form would be ambiguous.

## Decision Framework

### Tier Selection

```
Specific malware family or tool signature?
  → well-known/

Attacker intent inferred from capability combinations?
  → objectives/

Single observable mechanic, no intent inference?
  → micro-behaviors/
     Rarely legitimate?     → suspicious
     Defines program purpose? → notable
     Universal baseline?      → baseline

Neutral file property (not behavioral)?
  → metadata/
```

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

### Placement Tiebreaker

When a behavior could serve multiple objectives, place the single trait where evidence points most specifically. Composites in other objectives reference it.

| Scenario | Placement | Rationale |
|----------|-----------|-----------|
| Process injection, no further context | `evasion/process/injection/` | Stealth is the most common use; privesc/lateral composites reference it |
| Dropper (any payload delivery) | `command-and-control/dropper/` | All droppers are C2 — organized by kill-chain: delivery/, staging/, execution/, behavior/ |
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
| Daemon fork+setsid persisting across reboot | `persistence/system/daemon/` | Restarting after reboot is persistence |
| Reads Chrome Login Data SQLite | `credential-access/browser/` | Targets a specific credential store |
| Reads `AWS_SECRET_ACCESS_KEY` from env | `credential-access/env/secrets/` | Targets a specific secret |
| Reads `os.environ` generically | `micro-behaviors/os/env/` | Neutral capability, no credential targeting |
| Generic keystroke capture | `collection/keylog/` | General capture; credential-access composites reference it |
| Chrome passwords + HTTP POST to attacker | `exfiltration/stealer/credential/` | Source + transport = exfiltration |
| "admin" or "root" keyword | `micro-behaviors/data/text/keywords/` | Neutral string, not credential access |
| File property with no behavioral implication | `metadata/` | Structural fact, not behavior |
| File property indicating deceptive intent | `evasion/masquerade/` | Deception is behavioral |

## Tier 1: Capabilities (`micro-behaviors/`)

Value-neutral observations about what code can do. High confidence from static analysis. Maps to MBC [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors): *"low-level, support many objectives and other behaviors, and aren't necessarily malicious."*

```
micro-behaviors/
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
│   ├── ipc/               #   IPC (pipes, DDE, XPC, WCF, IRC)          C0003
│   ├── ftp/               #   FTP client/upload                         C0004
│   ├── ssh/               #   SSH client/connect
│   ├── ip/                #   IP addressing (parse, resolve, embedded)
│   ├── proxy/             #   Proxy/tunneling (SOCKS)
│   ├── url/               #   URL construction/parsing
│   ├── websocket/         #   WebSocket
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
│   └── library/           #   Crypto library/framework detection        C0059
│
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
│   ├── archive/           #   Archive operations (tar, zip extraction)
│   ├── serialize/         #   Serialization (JSON, YAML, pickle, protobuf)
│   ├── format/            #   Format patterns in content (MZ header, PDF, HTML)
│   │                      #     File-level format identification → metadata/format/
│   ├── embedded/          #   Embedded content (certificates, EXIF, runtime)
│   ├── text/              #   Text/string analysis (keywords, patterns)
│   ├── source/            #   Source code patterns (syntax, quality, identifiers)
│   ├── string/            #   String operations (library, conversion)          C0019
│   ├── buffer/            #   Buffer operations (offset writes, reassembly)
│   ├── db/                #   Database operations (SQL, Redis, MongoDB, etc.)
│   └── control-flow/      #   Control flow patterns (loops, error handling)
│   # NOTE: PRNG → os/random/. Config detection → metadata/config/.
│   # data/ is for data transformation, not system queries or file metadata.
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
│   ├── directory/         #   Directory operations (create, list, traverse, delete)
│   ├── disk/              #   Disk/partition operations
│   ├── enumerate/         #   File/directory/drive enumeration
│   ├── file/              #   File operations (read, write, copy, move, delete, stat)
│   ├── link/              #   Hard/symbolic links
│   ├── lock/              #   File locking (flock)
│   ├── memory/            #   Memory-mapped I/O (mmap)
│   ├── path/              #   Path references and construction
│   │   ├── config/        #     Config paths (accounts, groups, sudoers)
│   │   ├── device/        #     Device paths (storage, terminal)
│   │   ├── sensitive/     #     Sensitive paths (SSH keys, wallets, credentials)
│   │   └── temp/          #     Temporary paths
│   ├── pipe/              #   Named pipes (FIFO)
│   ├── proc/              #   /proc filesystem access
│   ├── quota/             #   Filesystem quota operations
│   ├── read/              #   File reading (standalone)
│   ├── search/            #   File search/query tools (locate, mdfind, Spotlight)
│   ├── shell-ops/         #   Shell file operations (cp, mv, rm)
│   ├── swap/              #   Swap operations
│   ├── sync/              #   Filesystem sync (fsync, fdatasync)
│   ├── temp/              #   Temporary file/directory creation
│   ├── traversal/         #   Directory/drive traversal
│   ├── volume/            #   Volume mount/unmount
│   ├── watch/             #   File monitoring (inotify, fanotify, fswatch)
│   └── write/             #   File writing (standalone)
│
├── hardware/              # Hardware device I/O                 → MBC: Hardware
│   │                      #   Direct interaction with hardware devices.
│   │                      #   Querying system properties → os/sysinfo/.
│   │                      #   Hardware enumeration libraries → objectives/discovery/.
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
│   ├── decompress/        #   Native decompression in memory
│   ├── gc/                #   Garbage collection
│   ├── inline-asm/        #   Inline assembly detection
│   ├── lock/              #   Memory locking (VirtualLock, mlock)
│   ├── protect/           #   Memory protection changes (mprotect, VirtualProtect)
│   ├── query/             #   Memory queries (VirtualQuery)
│   ├── read/              #   Memory read (including cross-process ReadProcessMemory)
│   └── sync/              #   Synchronization primitives (mutex, semaphore)
│   # NOTE: RWX allocation, reflective loading, shellcode execution,
│   # ntdll unhooking, and UAF exploits → objectives/ (evasion or execution).
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
│   ├── clipboard/         #   Clipboard access (OS IPC)
│   ├── com/               #   Windows COM/OLE
│   ├── compat/            #   OS compatibility layers
│   ├── console/           #   Console I/O (C0033)
│   ├── container/         #   Container runtime detection
│   ├── env/               #   Environment variables (C0034)
│   ├── event/             #   OS event mechanisms
│   ├── exception/         #   Exception/error handling
│   ├── firewall/          #   Firewall tool references (iptables, nft, ufw, firewalld)
│   │                      #     Neutral: "code references a firewall tool" (notable)
│   │                      #     Destructive ops (flush, disable, policy change) →
│   │                      #     objectives/impact/degrade/firewall/
│   ├── group/             #   Group management
│   ├── kernel/            #   Kernel interaction (modules, devices, callbacks)
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
│   ├── service/           #   System service management
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
│   ├── fork/              #   POSIX fork/clone
│   ├── hook/              #   API/function hooking
│   ├── identity/          #   Process identity (getpid, getppid)
│   ├── info/              #   Process information queries
│   ├── inject/            #   Cross-process injection (DLL, thread, APC, atom-bombing)
│   ├── interpreter/       #   Code interpreters/runtimes
│   │   ├── vm/            #     Node.js VM module (createContext, runInContext)
│   │   ├── node/          #     Node.js internal bindings (process.binding)
│   │   └── gentee/        #     Gentee scripting runtime
│   ├── io/                #   Process I/O redirection
│   ├── lifecycle/         #   Process lifecycle management
│   ├── pid/               #   PID file operations
│   ├── resources/         #   Process resource management
│   ├── script/            #   Script execution
│   ├── sync/              #   Process synchronization
│   ├── terminate/         #   Process termination (killing other processes)
│   ├── thread/            #   Thread lifecycle (Java)
│   ├── threading/         #   Threading primitives (Windows sync)
│   ├── tls/               #   Thread-local storage
│   ├── tty/               #   TTY/PTY operations (terminal detection, pseudoterminals)
│   └── user/              #   Process user identity (whoami, getlogin, getpwuid)
│
├── ui/                    # User interface operations
│   ├── controls/          #   Widget/control operations
│   ├── dialog/            #   Dialog boxes, message boxes, prompts
│   ├── framework/         #   UI framework usage (tkinter, WinForms)
│   ├── graphics/          #   GDI/drawing operations
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
│   ├── self-modify/           #   Runtime self-modification               B0008
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
│   │   ├── binary-metrics/    #     Binary structural anomalies
│   │   ├── code-metrics/      #     Source code anomalies (metrics-driven)
│   │   ├── tools/             #     Known obfuscators (js-obfuscator, garble)
│   │   ├── multi-layer/       #     Multiple techniques combined
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
│   │   ├── edr-detect/        #     Security product enumeration           B0013
│   │   ├── heuristic/         #     Heuristic evasion (TBAV)
│   │   ├── import-pollution/  #     Import table pollution
│   │   ├── platform/          #     Platform-specific bypass (exclusions, disables)
│   │   ├── syscall/           #     Direct/indirect syscalls (EDR bypass)
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
│   │                          #     micro-behaviors/data/text/llm/.
│   ├── self-delete/           #   Self-deletion after execution           F0007
│   └── tcc-manipulation/      #   macOS TCC database manipulation
│
├── command-and-control/       # C2 communication (OB0004)
│   │                          #   "Communicate with compromised systems to control them"
│   │                          #   MBC: B0030 C2 Communication, B0031 DGA, E1105 Ingress Tool Transfer.
│   │                          #   NOT C2: DDoS → impact/dos/. Exfil → exfiltration/.
│   │                          #   Credential phishing → credential-access/. Competing malware → impact/.
│   ├── backdoor/              #   Persistent remote access (all types)       B0030
│   │   ├── binary/            #     Compiled backdoors (PE, ELF, Mach-O)
│   │   ├── script/            #     Script-based backdoors (+ RAT scripts)
│   │   ├── daemon/            #     Daemon/service backdoors
│   │   ├── stealth/           #     Stealthy backdoor techniques
│   │   ├── reflective-load/   #     Reflective loading patterns
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
│   ├── dropper/               #   Payload delivery & execution               E1105 + B0023
│   │   ├── delivery/          #     Transport (HTTP, FTP, GitHub, document)
│   │   ├── staging/           #     Payload prep (embedded, encrypted, memory)
│   │   ├── execution/         #     How payload runs (script, loader, eval)
│   │   └── behavior/          #     Multi-step behavioral composites
│   ├── infrastructure/        #   C2 infrastructure (domains, IPs, cloud)    B0030
│   │   ├── domain/            #     Domains, DGA, hosting
│   │   └── config/            #     C2 config patterns
│   ├── remote-command/        #   Command dispatch                           B0011
│   ├── reverse-shell/         #   Reverse shell patterns                     B0030
│   └── trigger/               #   Activation triggers
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
│   ├── stealer/               #   Multi-step stealer behavior composites  T1119
│   ├── activity/              #   User activity tracking
│
├── credential-access/         # Credential theft (OB0005)
│   │                          #   "Obtain credential access" — targeting specific stores.
│   │                          #   Generic capture (keystrokes, clipboard) → collection/.
│   │                          #   Neutral env access (os.environ) → micro-behaviors/.
│   │                          #   Credential access + transport → exfiltration/stealer/.
│   │                          #   Neutral keywords ("admin", "root") → micro-behaviors/.
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
│   │                          #   Droppers → command-and-control/dropper/ (all droppers are C2).
│   │                          #   Install hooks (setup.py cmdclass) → micro-behaviors/build/setup/;
│   │                          #   composites using them live in supply-chain/.
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
│   │                          #   "Steal data from a system" — focuses on TRANSPORT.
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
│   ├── sensitive-data/        #   Sensitive file targeting before transport
│   ├── serialization/         #   Data serialization for transport
│   ├── side-channel/          #   Covert channels (DNS tunneling, stego)
│   └── stealer/               #   Complete steal-and-send chains           E1020
│       ├── credential/        #     Credential access + transport
│       ├── file/              #     File theft + transport
│       └── system-info/       #     System profiling + transport
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
│   │                          #   Organized by trigger event: firmware (survives OS reinstall),
│   │                          #   system (OS boot), or login (user session start).
│   │                          #   NOTE: hiding/concealment belongs in evasion/, not here.
│   │                          #   Persistence is about *restarting*, not *hiding*.
│   ├── firmware/              #   Survives OS reinstall — below the OS
│   │   └── boot/record/      #     MBR/bootkit                           F0013, T1542
│   ├── system/                #   Runs at OS boot, no user login needed
│   │   ├── cron/              #     System crontabs (/etc/crontab)        T1053.003
│   │   ├── daemon/init/       #     Unix daemon patterns (fork+setsid)    T1543
│   │   ├── init/              #     SysV init.d, rc.local, chkconfig
│   │   ├── input-manager/     #     macOS InputManager                    T1547.015
│   │   ├── launchd/           #     macOS LaunchDaemons                   T1543.004
│   │   ├── registry/          #     HKLM registry keys                    E1112
│   │   ├── service/install/   #     Windows SCM / systemd units           T1543.003
│   │   ├── systemd/           #     systemd service files                 T1543.002
│   │   └── wmi/subscription/  #     WMI event subscriptions               T1546.003
│   └── login/                 #   Runs at user login / session start
│       ├── account/create/    #     Backdoor user accounts                T1136.001
│       ├── ifeo/debugger/     #     IFEO registry hijack                  T1546.012
│       ├── registry/          #     HKCU Run keys, auto-launcher          F0012
│       ├── scheduled-task/    #     Windows Task Scheduler
│       ├── self-install/      #     Self-copy + registry persistence
│       ├── shell/config/      #     .bashrc, .zshrc, .profile             T1546.004
│       ├── ssh/backdoor/      #     authorized_keys injection             T1098.004
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
│   │                            #   Organized by ATTACK TECHNIQUE, not ecosystem.
│   │                            #   Ecosystem (npm, pypi, rubygems) = filename, never directory.
│   │                            #   A trait belongs here only if it is supply-chain-specific —
│   │                            #   it would never fire outside a package/extension context.
│   │                            #   Generic behaviors stay in their existing objectives:
│   │                            #     Generic recon (whoami) → discovery/.
│   │                            #     Generic exfil (HTTP POST) → exfiltration/.
│   │                            #     Generic obfuscation → anti-static/obfuscation/.
│   │                            #     Generic credential reads → credential-access/.
│   │                            #   Supply-chain composites reference those atomics.
│   │                            #   Neutral FP-context (bundler/framework/test detection)
│   │                            #   belongs in metadata/ tier, not here.
│   ├── install-hook/            #   Install-time code execution              T1195.002
│   │                            #     Code that runs as side-effect of package installation.
│   │                            #     NOT runtime code. NOT manually invoked build scripts.
│   ├── recon-exfil/             #   Package-install-triggered recon + exfil  T1082, T1041
│   │                            #     Gathering host/env info and exfiltrating from package
│   │                            #     lifecycle contexts (postinstall scripts, OAST callbacks,
│   │                            #     CI/CD secrets exfil from lifecycle hooks).
│   │                            #     NOT generic recon (→ discovery/).
│   │                            #     NOT generic exfil (→ exfiltration/).
│   ├── credential-theft/        #   Stealing package-manager credentials     T1552
│   │                            #     Targeting package-ecosystem credential stores (.npmrc,
│   │                            #     pip.conf, gem credentials, registry tokens).
│   │                            #     NOT generic credential access (→ credential-access/).
│   ├── hidden-payload/          #   Concealed malicious code in packages     T1027
│   │                            #     Package-specific concealment — unicode steg in manifests,
│   │                            #     bytenode compilation, hex arrays in install scripts.
│   │                            #     Composites reference anti-static/ atomics.
│   │                            #     NOT general obfuscation (→ anti-static/obfuscation/).
│   ├── metadata-anomaly/        #   Suspicious package metadata patterns     T1195.002
│   │                            #     Anomalies in manifests, registry data, version schemes,
│   │                            #     author fields, extension manifests. Signals the package
│   │                            #     is suspicious before looking at code.
│   │                            #     NOT neutral metadata (→ metadata/ tier).
│   ├── impersonation/           #   Package identity deception               T1195.002
│   │                            #     Typosquatting, dependency confusion, deprecated-package
│   │                            #     hijack, function shadowing, name similarity.
│   └── trojanized/              #   Backdoored legitimate code               T1195.002
│                                #     Modifications to known-good libraries/frameworks.
│                                #     NOT wholly malicious packages (→ hidden-payload/).
```

## Tier 3: Known Entities (`well-known/`)

Specific malware families and tool signatures. Similar to MBC's [malware corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) but structured as detection rules. Categories align with [MBC/STIX 2.1 malware types](https://docs.oasis-open.org/cti/stix/v2.1/os/stix-v2.1-os.html).

Do not create general-purpose traits in well-known/ that would possibly match multiple families, even if they are at a low criticality. Move general-purpose traits to a general-purpose location.

**Rules:**
- Each malware family appears in exactly **one** category — pick the primary behavior
- Categories describe **what the malware does**, not who made it or how it arrives
- Actor attribution (APT group, nation-state) belongs in trait descriptions, not directory names
- When a family has multiple capabilities (e.g., stealer + worm), pick the most distinctive
- `trojan/` is the catch-all — use only when no more specific type fits

```
well-known/
├── app/                   # Specific legitimate applications and suites
│   └── (adobe, bitdefender, defender, vendor drivers, etc.)
├── game/                  # Game clients/platforms and game-specific tools
│   └── (steam, etc.)
├── lib/                   # Specific embedded libraries/frameworks/runtimes
│   └── (openssl, zlib, ffmpeg, psutil, sharpshell, etc.)
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
│   │                      #     MBC: resource-exploitation. (XMRig, Kinsing)
│   ├── ransomware/        #   Encrypts files and demands ransom
│   │                      #     (LockBit, Conti, Babuk)
│   ├── rat/               #   Full remote administration toolkit
│   │                      #     Superset of backdoor — file manager, screen viewer,
│   │                      #     keylogger, webcam, plugin system.
│   │                      #     (Cobalt Strike, Sliver, Pupy)
│   ├── rootkit/           #   Kernel or userspace hiding + privilege escalation
│   │                      #     (eBPFKit, Reptile, Diamorphine)
│   ├── stealer/           #   Information stealer — credentials, tokens, wallets
│   │                      #     MBC: information-stealer. (AMOS, RedLine, Vidar)
│   ├── supply-chain/      #   Malicious package, extension, or update
│   │                      #     Delivery context matters for ML — a malicious npm
│   │                      #     package looks different from a standalone binary.
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
└── tool/                  # Legitimate tools often abused
    ├── browser/           #   Browser components (Chromium sandbox, extensions)
    ├── development/       #   IDEs and developer tools (JetBrains)
    ├── detection/         #   Security detection tools (cleave's own stng)
    ├── dual-use/          #   Dual-use utilities (licensing, converters)
    ├── offensive/         #   Pentesting/red-team tools + game cheat frameworks
    ├── reverse-engineering/#  RE tools (IDA, OllyDbg, Scylla, LordPE)
    └── sysadmin/          #   Admin tools, system libraries, VCS
```

## Metadata (`metadata/`)

File-level properties with no behavioral implication. Describes *what a file is*, not *what it does*.

**Rules:**
- Behavioral detection belongs in `objectives/`, not here
- Tool/malware signatures belong in `well-known/`, not here
- Supply-chain attack indicators belong in `objectives/supply-chain/` (organized by technique, not ecosystem)
- OS/platform vendor traits go under `vendor/`
- Specific apps, tools, games, and library/framework/runtime fingerprints go under `well-known/{app,tool,game,lib}/`, not `metadata/`
- New top-level subdirectories require updating both TAXONOMY.md and `ALLOWED_METADATA` in `src/capabilities/validation/directory_whitelist.rs`
- **Max depth:** 3 levels within `metadata/` (ML pipeline limit)
- **Max leaf size:** No leaf directory should exceed 80 traits
- **Prefer technology-neutral subdirectory names.** Technology names belong in filenames, not directory names, unless needed to stay under the 80-trait limit at depth 3.

```
metadata/
├── arch/                  # CPU architecture (x86, ARM, MIPS, IoT)
├── binary/                # Binary internals (requires binary parsing)
│   ├── anomaly/           #   Structural violations (format, timestamp, layout)
│   ├── debug/             #   Debug symbols (PDB, DWARF)
│   ├── framework/         #   Runtime/framework detection (.NET, Java, VB6, MFC)
│   ├── installer/         #   Installer framework detection
│   │   ├── database/      #     Database-based (MSI, WiX)
│   │   ├── script/        #     Script-based (NSIS, Inno Setup)
│   │   └── sfx/           #     Self-extracting (7zip, WinRAR, IExpress)
│   ├── instruction/       #   Instruction-level patterns (indirect calls, CPUID)
│   ├── layout/            #   File-level structure (overlay, embedded, bundles)
│   ├── linking/           #   Runtime linking and dynamic resolution
│   ├── metrics/           #   Structural measurements (import/export/function
│   │                      #     counts, entropy, ratios, size thresholds)
│   ├── resource/          #   Embedded resource analysis
│   ├── section/           #   Section analysis
│   │   ├── content/       #     Section content patterns
│   │   ├── metrics/       #     Section entropy, ratios, custom names
│   │   └── names/         #     Section name detection
│   └── symbols/           #   Import/export symbol analysis
├── build/                 # Build systems, CI/CD (cmake, cargo, docker, jenkins)
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
│   ├── encoded/           #   Encoded content presence (base64)
│   ├── extension/         #   File extension classification
│   ├── magic/             #   Magic byte signatures
│   └── text/              #   Text/data format identification (JSON, makefile)
├── hardening/             # Security hardening features (sandbox, seccomp, pledge)
├── import/                # Dependencies/imports (auto-generated)
│   ├── python/ npm/ ruby/ java/ go/ rust/ c/
│   └── macho/ elf/ pe/   #   Binary format imports
├── lang/                  # Language, compiler, encoding detection
│   ├── compiled/          #   Compiled language detection (assembly, C, Go, Rust)
│   ├── compiler/          #   Compiler identification
│   │   ├── managed/       #     Managed runtimes (.NET, Delphi)
│   │   ├── native/        #     Native toolchains (GCC, Clang, MSVC, MinGW)
│   │   └── systems/       #     Systems language compilers (Go, Rust)
│   ├── encoded/           #   Encoded strings (unicode, wide)
│   ├── javascript-features/ # JavaScript language features
│   ├── scripted/          #   Scripted language detection (VBScript, Lua, Perl)
│   └── ...                #   go-build, linking, optimization, security, shebang, source, version
├── library/               # Legacy neutral library/framework context
│   ├── data/              #   Data/infrastructure libraries
│   ├── runtime/           #   Runtime/framework libraries
│   └── (neutral package/library context; known-library fingerprints → well-known/lib/)
├── package/               # Package ecosystem metadata & project quality
│   ├── chrome-extension/  #   Extension manifest analysis
│   ├── config/            #   Configuration file detection
│   ├── contributors/      #   Contributor metadata
│   ├── dependencies/      #   Dependency analysis
│   ├── documentation/     #   Documentation presence
│   ├── error-handling/    #   Error handling patterns
│   ├── fields/            #   Package field analysis
│   ├── files/             #   File counts and types
│   ├── help/              #   Help/usage interface
│   ├── keywords/          #   Package keywords
│   ├── license/           #   License detection
│   ├── logging/           #   Logging patterns
│   ├── maintainers/       #   Maintainer counts
│   ├── metrics/           #   Code metrics
│   ├── quality/           #   Quality signals
│   ├── scripts/           #   Package scripts
│   ├── testing/           #   Testing detection
│   │   ├── compiled/      #     Compiled-language frameworks
│   │   ├── harness/       #     Runtime-specific test harnesses
│   │   ├── presence/      #     Test presence indicators
│   │   └── scripted/      #     Scripted-language frameworks
│   ├── tooling/           #   Package tooling
│   └── versioning/        #   Version detection
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
| `binary/` | `file/` | Does it require parsing binary headers (PE/ELF/Mach-O)? → `binary/`. Observable from filename/magic/size alone? → `file/` |
| `binary/` | `document/` | Does it require a binary parser? → `binary/`. Does it require a document parser (OLE, OOXML, PDF objects)? → `document/` |
| `binary/` | `lang/` | Is it about the binary's structure (sections, imports, metrics)? → `binary/`. Is it about what language/compiler produced it? → `lang/` |
| `binary/metrics/` | `binary/anomaly/` | Is the measurement neutral (could be normal)? → `metrics/`. Does it inherently indicate malformation or tampering? → `anomaly/` |
| `document/` | `file/` | Does it require parsing document internals (OLE streams, OOXML parts, PDF objects)? → `document/`. Observable from header/extension alone? → `file/` |
| `build/` | `lang/` | Is it about build orchestration (cmake, docker, CI/CD)? → `build/`. Is it about the language toolchain (gcc, rustc, delphi)? → `lang/` |
| `package/` | `library/` | Is it about ecosystem-level metadata (fields, scripts, quality, testing)? → `package/`. Is it neutral library context retained for metadata use? → `library/`. Is it identifying a specific library/framework/runtime? → `well-known/lib/` |
| `signed/` | `vendor/` | Is it about the cryptographic signature chain or entitlements? → `signed/`. Is it identifying an OS/platform vendor by strings/resources/patterns? → `vendor/` |
| `vendor/` | `well-known/app/` or `well-known/tool/` | Is it an OS/platform vendor or system userland marker (Apple, Microsoft, NetBSD, GNU/FSF)? → `vendor/`. Is it a specific application or suite? → `well-known/app/`. Is it a utility or analyst/admin/developer tool? → `well-known/tool/` |
| `vendor/` | `well-known/lib/` | Is it identifying the platform vendor that produced the file? → `vendor/`. Is it an embedded third-party library/framework/runtime fingerprint (OpenSSL, zlib, FFmpeg, psutil, SharpShell)? → `well-known/lib/` |

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
| `eval()` call | Capability | `micro-behaviors/process/create/eval/dynamic` | notable |
| Process hollowing | Capability | `micro-behaviors/process/hollow` | suspicious |
| Screenshot API | Capability | `micro-behaviors/hardware/display/screenshot` | notable |
| Screenshot + timer + upload | Objective | `objectives/collection/screenshot` | suspicious |
| Reverse shell pattern | Objective | `objectives/command-and-control/reverse-shell` | hostile |
| Cobalt Strike beacon | Known | `well-known/malware/rat/cobalt-strike` | hostile |

### MBC Identifiers

- **ATT&CK Techniques**: `T1234` or `T1234.001` (sub-technique)
- **MBC Behaviors**: `B0001` (behavior), `C0015` (micro-behavior)
- **MBC Enhanced**: `E1234` (ATT&CK technique with MBC enhancements)

See [MBC Identifiers](https://github.com/MBCProject/mbc-markdown#identifiers) for the full specification.
