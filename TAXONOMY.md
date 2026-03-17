# cleave Taxonomy

A three-tier taxonomy following [MBC (Malware Behavior Catalog)](https://github.com/MBCProject/mbc-markdown) principles.

## Tiers

| Tier | Purpose | Criticality Range | MBC Equivalent |
|------|---------|-------------------|----------------|
| **Capabilities** (`micro-behaviors/`) | Observable mechanics — what code *can do* | component → baseline → notable → suspicious | [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors) |
| **Objectives** (`objectives/`) | Attacker goals — why code *likely wants* to do something | component → baseline → notable → suspicious → hostile | [Objectives](https://github.com/MBCProject/mbc-markdown#malware-objective-descriptions) |
| **Known Entities** (`well-known/`) | Specific malware families and tool signatures | component → baseline → suspicious → hostile | [Corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) |
| **Metadata** (`metadata/`) | Neutral file-structure properties — what a file *is* | component → baseline (occasionally suspicious) | — |

## Criticality

| Level | Meaning | Tier Constraints |
|-------|---------|-----------------|
| **component** | Building block for composites; no standalone signal (e.g., string fragment `&cc=`). Filtered from terminal output unless a referencing composite fires. Always in JSON for ML. | Any tier |
| **baseline** | Common functionality; doesn't indicate program purpose (e.g., `mmap`, `stdio`, `read`). Always in output for ML. | Any tier |
| **notable** | Defines program purpose (e.g., `socket`, `exec`, `eval`). Communications and code execution should always be notable or higher. Used for human review and differential analysis of supply-chain changes. | `micro-behaviors/`, `objectives/`, `well-known/` |
| **suspicious** | Rarely legitimate; indicates possible malicious intent. | `micro-behaviors/`, `objectives/`, `well-known/`, `metadata/` (rare) |
| **hostile** | Clear attack pattern; no legitimate use. Requires precision >= 3.5. | `objectives/`, `well-known/` only — **never** `micro-behaviors/` |

## Core Principles

### Single-Trait Rule

Unlike MBC, which allows one behavior to map to multiple objectives (e.g., Process Injection is both Defense Evasion and Privilege Escalation), cleave allows exactly **one trait per behavior**. Place it at the most specific location the evidence supports. Composite rules in other directories can reference the single trait to express multi-objective interpretations.

### Tier Dependencies

| Tier | Can Reference | Rationale |
|------|--------------|-----------|
| `micro-behaviors/` | `micro-behaviors/`, `metadata/` | Capabilities must not depend on objectives |
| `objectives/` | `micro-behaviors/`, `objectives/`, `metadata/` | Objectives build on capabilities and other objectives |
| `well-known/` | all tiers | Signatures can reference anything |
| `metadata/` | `metadata/` | Informational properties reference only other metadata |

**Capabilities must not reference objectives.** Capabilities are observable mechanics; objectives infer intent. If a `micro-behaviors/` rule needs an `objectives/` trait, either move the objective to `micro-behaviors/` (if it's actually a capability), refactor the dependency away, or move the whole rule to `objectives/` (if it's actually inferring intent).

**Capabilities must not use `crit: hostile`.** Hostile requires intent inference, which belongs in `objectives/`. Maximum capability criticality is `suspicious`. Validation rejects hostile capabilities.

### Directory Layout Convention

All tiers follow: `TIER/CATEGORY/BEHAVIOR/METHOD/platform.yaml`

- **`objectives/`**: `objectives/OBJECTIVE/BEHAVIOR/METHOD/` with per-platform or per-ecosystem YAML files. Add sub-method directories when a method has many variants (e.g., string obfuscation techniques).
- **`micro-behaviors/`**: `micro-behaviors/CATEGORY/BEHAVIOR/METHOD/` (e.g., `crypto/symmetric/aes/ruby.yaml`, not `crypto/symmetric/aes.yaml`). If no specific method applies, group by syscall, protocol, or logical grouping. Directory names may be referenced by composite traits to match related rules.

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
| Dropper fetches payload from a URL | `command-and-control/dropper/` | C2 evidence present |
| Dropper unpacks embedded payload, no network | `execution/dropper/` | Pure local execution |
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
| File property with no behavioral implication | `metadata/` | Structural fact, not behavior |
| File property indicating deceptive intent | `evasion/masquerade/` | Deception is behavioral |

## Tier 1: Capabilities (`micro-behaviors/`)

Value-neutral observations about what code can do. High confidence from static analysis. Maps to MBC [Micro-objectives](https://github.com/MBCProject/mbc-markdown/tree/master/micro-behaviors): *"low-level, support many objectives and other behaviors, and aren't necessarily malicious."*

```
micro-behaviors/
├── communications/        # Network communication              → MBC: Communication
│   ├── socket/            #   Raw sockets (netcat, telnet)
│   ├── http/              #   HTTP client/server
│   ├── dns/               #   DNS (lookups, txt, reverse, DoH, tools)
│   ├── icmp/              #   ICMP (ping, traceroute)
│   ├── capture/           #   Packet capture (tcpdump, wireshark)
│   ├── benchmark/         #   Performance testing (iperf, speedtest)
│   ├── ipc/               #   Inter-process communication
│   └── proxy/             #   Proxy protocols (SOCKS, etc.)
│
├── crypto/                # Cryptographic operations            → MBC: Cryptography
│   ├── symmetric/         #   AES, DES, etc.
│   ├── asymmetric/        #   RSA, ECC, etc.
│   ├── hash/              #   SHA, MD5, etc.
│   └── xor/               #   XOR operations
│
├── data/                  # Data transformation                 → MBC: Data
│   ├── encode/            #   Encoding (base64, hex, custom)
│   ├── compress/          #   Compression (zip, gzip, etc.)
│   └── serialize/         #   Serialization (JSON, protobuf, pickle)
│
├── fs/                    # Filesystem access                   → MBC: File System
│   ├── read/              #   File reading
│   ├── write/             #   File writing
│   ├── delete/            #   File deletion
│   ├── enumerate/         #   Directory listing
│   ├── hide/              #   Hidden file manipulation (suspicious)
│   └── path/              #   Path references
│       ├── config/        #     Config paths (accounts, groups, sudoers)
│       └── device/        #     Device paths (storage, terminal)
│
├── hardware/              # Hardware interaction                → MBC: Hardware
│   ├── input/             #   Keyboard, mouse
│   ├── display/           #   Screenshot, screen access
│   ├── audio/             #   Microphone, speakers
│   └── usb/               #   USB devices
│
├── mem/                   # Memory operations                   → MBC: Memory
│   ├── alloc/             #   Allocation
│   ├── protect/           #   Protection changes
│   ├── map/               #   Memory mapping
│   └── inject/            #   Shellcode/code cave (same-process)
│
├── os/                    # OS integration                      → MBC: Operating System
│   ├── autorun/           #   System/user autorun configuration
│   │   ├── system/        #     Boot-time autorun (init, systemd, launchd)
│   │   ├── user/          #     Login-time autorun (startup folder, shell rc, pth)
│   │   ├── scheduled/     #     Timer-triggered (cron, at)
│   │   └── supervised/    #     Process managers (pm2, supervisord)
│   ├── registry/          #   Windows registry
│   │   └── autostart/     #     Run/RunOnce key detection (neutral)
│   ├── env/               #   Environment variables
│   ├── service/           #   System services
│   ├── user/              #   User management
│   ├── syscall/           #   Direct syscall invocation
│   ├── bpf/               #   BPF/eBPF operations
│   ├── info/              #   System queries (baseline)
│   ├── network/           #   Network config (interfaces, status)
│   └── firewall/          #   Firewall management (iptables, nft, ufw, firewalld)
│
├── process/               # Process control                     → MBC: Process
│   ├── create/            #   Process creation
│   ├── inject/            #   Cross-process injection (DLL, thread, APC, atom-bombing)
│   ├── terminate/         #   Process termination
│   ├── enumerate/         #   Process listing
│   ├── hollow/            #   Process hollowing
│   ├── hook/              #   API/function hooking
│   └── fd/                #   File descriptor manipulation (dup2)
│
└── time/                  # Timing operations
    ├── sleep/             #   Delays
    ├── schedule/          #   Scheduled execution
    └── timer/             #   Timers
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
│   └── browser-detect/        #   Browser sandbox detection
│
├── anti-static/               # Evade static analysis (OB0002)
│   │                          #   Disassembly, decompilation, string extraction
│   ├── obfuscation/           #   Obfuscated files/code          E1027 + B0032
│   │   ├── string/            #     String obfuscation (encrypt, split, concat)
│   │   ├── encoding/          #     Data encoding (base64, hex, xor)
│   │   ├── eval/              #     Dynamic execution (eval, exec, Function)
│   │   ├── control-flow/      #     Control-flow (flattening, opaque predicates)
│   │   ├── instruction/       #     Instruction-level (junk/dead code)     B0032
│   │   ├── identifier/        #     Name mangling (var rename, exports)
│   │   ├── imports/           #     Import concealment, API hashing
│   │   ├── payload/           #     Embedded/encrypted payloads
│   │   ├── document/          #     Document-specific (RTF, Office, LNK)
│   │   ├── steganography/     #     Data hiding (images, unicode)
│   │   ├── source/            #     Source-level obfuscation patterns
│   │   ├── binary-metrics/    #     Binary structural anomalies
│   │   ├── code-metrics/      #     Source code anomalies
│   │   ├── tools/             #     Known obfuscators (js-obfuscator, garble)
│   │   ├── multi-layer/       #     Multiple techniques combined
│   │   └── anti-decompile/    #     Anti-disassembly tricks                B0012
│   ├── pack/                  #   Software packing                        F0001
│   └── polyglot/              #   Polyglot file format abuse
│
├── evasion/                   # Evade detection in production (OB0006)
│   │                          #   Users, admins, AV/EDR, forensics
│   │                          #   "Don't see me" — targets defenders & security tools
│   ├── anti-av/               #   AV/EDR bypass (stealth, not termination)
│   │   ├── amsi/              #     AMSI bypass
│   │   ├── defender/          #     Windows Defender bypass
│   │   ├── heuristic/         #     Heuristic evasion (TBAV)
│   │   ├── syscall/           #     Direct/indirect syscalls (EDR bypass)
│   │   └── platform/          #     Platform-specific bypasses
│   ├── file-hiding/           #   Hidden files/directories                E1564, F0005
│   ├── kernel-hide/           #   Kernel-level hiding (rootkit)           E1014
│   ├── log-clear/             #   Log clearing                            T1070
│   ├── timestomp/             #   Timestamp modification                  T1070.006
│   ├── self-delete/           #   Self-deletion after execution           F0007
│   ├── evidence-removal/      #   Artifact cleanup
│   ├── masquerade/            #   File/process masquerading               T1036
│   ├── decoy/                 #   Decoy documents/files
│   ├── fileless/              #   Fileless execution (avoid disk artifacts)
│   ├── process/               #   Process manipulation
│   │   ├── injection/         #     Process injection                     E1055
│   │   └── hidden/            #     Hide processes/windows
│   └── hijack-execution-flow/ #   Execution flow hijacking                F0015
│
├── command-and-control/       # C2 communication (OB0004)
│   │                          #   "Communicate with compromised systems to control them"
│   ├── beacon/                #   Check-in patterns                       B0030
│   ├── channel/               #   Communication channels
│   │   └── covert/            #     Covert channels (ICMP, DNS tunneling)
│   ├── reverse-shell/         #   Reverse shell patterns
│   ├── backdoor/              #   Backdoor patterns
│   ├── dropper/               #   Payload delivery (two-stage)            B0023 + E1105
│   │   ├── encrypted/         #     Encrypted payload droppers
│   │   ├── http/              #     HTTP-based droppers
│   │   ├── loader/            #     Loader patterns
│   │   ├── method/            #     Dropper methods/techniques
│   │   ├── payload/           #     Payload execution
│   │   ├── script/            #     Script-based droppers
│   │   ├── fileless/          #     Fileless droppers
│   │   ├── install-time/      #     Install-time droppers
│   │   ├── silent-install/    #     Silent installer patterns
│   │   └── stager/            #     Multi-stage droppers
│   ├── implant/               #   Implant execution patterns
│   │   ├── eval/              #     Remote code execution via eval
│   │   ├── activex/           #     ActiveX-based implants
│   │   └── reflective-load/   #     Reflective loading
│   └── infrastructure/        #   C2 infrastructure
│       └── spoofing/          #     Infrastructure spoofing
│   # MBC splits droppers: Ingress Tool Transfer (E1105, C2) vs Install
│   # Additional Program (B0023, Execution). Droppers inherently fetch a
│   # payload, so they default here. Embedded payload execution without
│   # network activity (single-stage unpack-and-run) → execution/dropper/.
│
├── collection/                # Information gathering (OB0003)
│   │                          #   "Identify and gather information, such as sensitive files"
│   ├── keylog/                #   Keystroke logging                       T1056.001
│   ├── clipboard/             #   Clipboard capture                       T1115
│   ├── screenshot/            #   Screen capture                          T1113
│   └── audio/                 #   Audio capture                           T1123
│   # MBC lists capture behaviors (keylog, clipboard, screen) under both
│   # Collection AND Credential Access. Single-trait rule: general-purpose
│   # capture mechanisms live here. credential-access/ targets specific
│   # credential stores. Composites in credential-access/ reference these.
│
├── credential-access/         # Credential theft (OB0005)
│   │                          #   "Obtain credential access" — specific stores
│   ├── browser/               #   Browser credentials                     T1555.003
│   ├── system/                #   OS credentials                          T1003
│   ├── network/               #   Network credentials
│   └── cloud/                 #   Cloud service credentials
│
├── discovery/                 # Environment reconnaissance (OB0007)
│   │                          #   "Gain knowledge about the system and network"
│   ├── system/                #   System information                      T1082
│   ├── network/               #   Network information                     T1016
│   ├── user/                  #   User information                        T1033
│   └── software/              #   Installed software                      T1518
│
├── execution/                 # Code execution (OB0009)
│   │                          #   "Execute code on a system to achieve a variety of goals"
│   │                          #   Neutral capabilities (openpty, GetModuleHandle, fork+setsid,
│   │                          #   Math.random) → micro-behaviors/. Evasive execution (reflective
│   │                          #   loading, fileless, shellcode) → evasion/. Privesc (sudo, GTFOBins)
│   │                          #   → privilege-escalation/. Remote commands → command-and-control/.
│   │                          #   Install hooks (setup.py cmdclass) → micro-behaviors/build/setup/;
│   │                          #   composites using them live in lateral-movement/supply-chain/.
│   ├── activex/               #   COM/ActiveX execution                   E1569
│   ├── autoinstall/           #   Automatic dependency installation
│   ├── automation/            #   Compiled automation (AppleScript)        E1059
│   ├── compile/               #   Compile after delivery
│   ├── condition/             #   Conditional execution / guardrails       B0025
│   ├── dropper/               #   Embedded payload execution (single-stage) B0023
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
│   ├── social-engineering/    #   Lures, spam (passive lateral)           B0020, B0021
│   ├── ssh/                   #   SSH lateral (connect, backdoor, deploy) T1021.004
│   ├── supply-chain/          #   Supply chain compromise                 E1195
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
│   └── install-certificate/   #   Root cert installation                  F0016
```

## Tier 3: Known Entities (`well-known/`)

Specific malware families and tool signatures. Similar to MBC's [malware corpus](https://github.com/MBCProject/mbc-markdown/tree/master/xample-malware) but structured as detection rules.

```
well-known/
├── malware/               # Malware family signatures
│   ├── apt/               #   APT/nation-state groups
│   ├── backdoor/          ├── botnet/          ├── dropper/
│   ├── exploit/           ├── loader/          ├── miner/
│   ├── ransomware/        ├── rat/             ├── rootkit/
│   ├── stealer/           ├── trojan/          ├── virus/
│   └── worm/
│
└── tools/                 # Legitimate tools often abused
    ├── browser/           #   Browser components (Chromium sandbox)
    ├── offensive/         #   Pentesting tools (Cobalt Strike, Metasploit)
    ├── reverse-engineering/#  RE tools (IDA, OllyDbg, Scylla, LordPE)
    ├── sysadmin/          #   Admin tools (PsExec, WMI, winpty, disk utils)
    └── dual-use/          #   Dual-use utilities
```

## Metadata (`metadata/`)

File-level properties with no behavioral implication. Describes *what a file is*, not *what it does*.

**Rules:**
- Behavioral detection belongs in `objectives/`, not here
- Tool/malware signatures belong in `well-known/`, not here
- Supply-chain attack indicators belong in `objectives/lateral-movement/supply-chain/`
- Vendor-specific traits go under `vendor/`
- New top-level subdirectories require updating both TAXONOMY.md and `ALLOWED_METADATA` in `src/capabilities/validation/directory_whitelist.rs`

```
metadata/
├── analytics/             # Analytics tracking (UTM parameters)
├── arch/                  # Architecture (x86, x64, arm, arm64, MIPS)
├── archive/               # Archive structure
├── binary/                # Binary structure (sections, debug info)
├── builder/               # Build system detection (cmake, cargo, docker)
├── bundle/                # Bundle structure (macOS .app)
├── compiler/              # Compiler detection
├── config/                # Configuration file detection
├── dev/                   # Development context (testing frameworks)
├── encoded-payload/       # Encoded content detection (base64 presence)
├── entitlements/          # Code entitlements (macOS/iOS capabilities)
├── file/                  # File-level metadata (size)
├── format/                # File format detection (ELF, PE, Mach-O, PDF)
│   ├── anomaly/           #   Structural anomalies
│   ├── elf/  pe/          #   Format-specific traits
│   ├── archive/           #   Archive formats
│   ├── security-rule/     #   Security rule formats (YARA, Sigma)
│   └── ...
├── hardening/             # Security hardening (sandbox, seccomp, pledge)
│                          #   Can be used in downgrade: rules
├── import/                # Dependencies/imports (auto-generated, no YAML needed)
│   ├── python/ npm/ ruby/ java/ go/ rust/ c/
│   └── macho/ elf/ pe/   #   Binary format imports
├── lang/                  # Source language and encoding detection
├── library/               # Library/framework detection (react, vue, jquery)
├── quality/               # Code quality metrics
│   ├── chrome-extension/  #   Extension manifest keywords
│   ├── config/            #   Configuration quality
│   ├── contributors/      #   Contributor metadata
│   ├── dependencies/      #   Dependency counts
│   ├── documentation/     #   Documentation presence
│   ├── error-handling/    #   Error handling patterns
│   ├── files/             #   File counts and content types
│   ├── keywords/          #   Package keyword metadata
│   ├── license/           #   License detection
│   ├── logging/           #   Logging patterns
│   ├── maintainers/       #   Maintainer counts
│   ├── metrics/           #   Code metrics
│   ├── npm/               #   npm-specific quality signals
│   ├── package-info/      #   Package metadata (empty fields)
│   ├── testing/           #   Test presence
│   └── versioning/        #   Version resource detection (PE, semver)
├── signed/                # Code signature detection
│   ├── apple/             #   Apple signing (YAML-defined wrappers)
│   ├── certificate/       #   Certificate string patterns
│   ├── platform/          #   Platform signatures (auto-generated)
│   └── (auto-generated: platform::apple, developer::*, adhoc::unsigned)
└── vendor/                # Vendor identification
    ├── apple/  fsf/  jetbrains/  microsoft/
    └── openssl/  realtek/  valve/
```

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
