# Native PE review

All judgments below follow offline byte inspection and Rizin disassembly.
No specimen was executed and no executable or account-service endpoint was
fetched. These inputs contain no fetched package dependency.

| SHA-256 | Identification | Judgment |
| --- | --- | --- |
| a4ac34614c1111141447076608905cd124ce2235a88c448877d2b4cebabf446f | Eupdate Helper 4.0.1.0, yztcsn | BENIGN |
| 80732ccbf0a7e541fed2bbca748e6b8011c57c538f8a19e6aad81bef835af00c | StormAttack dropper with embedded DDoS DLL | MALICIOUS |
| f9adb5918487d90c4d812852f1799147368b458291a7e760bd28cd6ad28ba996 | Eupdate Helper 4.0.1.0, yztcsn | BENIGN |

## Eupdate Helper

The two files have identical code, imports and resources over file offsets
0x400..0x21bff. Differences lie in unused DOS-header bytes and the appended
hash-rotation pad. The same behavior analysis therefore applies to both.

- At VA 0x412964 the updater fetches an info.txt manifest, parses version:
  and downurl:, and compares the remote version with its local version.
  MessageBoxW at 0x412c6e explicitly asks in Chinese whether to update the
  ESET virus-database update tool. The comparison at 0x412c77 requires
  IDYES (6); the other branch reaches the declined-update path at 0x412f54.
  The affirmative path downloads its replacement, checks MZ at 0x412dea,
  renames the existing executable using MoveFileExW, launches the new copy
  and opens its explanation page. Weak transport/authenticity checks are
  present, but there is no captured malicious replacement or hidden launch.
- The relay listens on port 8000 and authenticates to upstream ESET update
  infrastructure using accounts obtained from a remote list. At 0x4146c7
  a suffix comparison deliberately returns 404 for .signed requests;
  0x417c40 filters [SERVERS], [LINKS] and [HOSTS] manifest sections. Neither
  path patches the client's verification nor demonstrates malicious update
  substitution. Retain the neutral filtering/HTTP observations.
- The configuration decoder at 0x416bb0 implements
  `out[i] = in[i] XOR key XOR ((31*i+7) & 255)`. Its four callers in
  0x415c80 decode `encrypt`, `type`, `/id.html`, and `id.1yz.me`;
  port 4046 is appended to the HTTPS account-list URL. These are account
  acquisition parameters, not local credential theft or executable staging.
- At 0x415a8e..0x415af0 the program writes its own quoted path under HKLM
  Run. Its elevation path uses ShellExecuteW with runas, invoking normal
  UAC consent. At 0x413108 onward, bind failure leads to TCP-table lookup
  and termination of the conflicting port owner, rather than a security
  process kill list. Existing notable autorun and termination traits remain.
- At 0x4127e4 the program opens its own image, seeks to EOF and appends
  4..11 bytes. The standby copy/relaunch flow is at 0x415800 and scheduled
  handoff at 0x4171c4. This is unusual hash rotation; keep its existing
  suspicious trait. It establishes no malicious payload or hostile purpose.

Retire the seven updater convictions: hash rotation, unsigned status, HTTP
updates, an external IP, Run registration and mirror filtering do not prove
trojanization or an unwanted downloader. Remove the identity downgrades that
referenced a retired conviction. No new product or endpoint exception is used.
Final sample coverage is zero hostile and one suspicious trait each.

## StormAttack

The outer PE contains a DLL at file offset 0x8060. Do not infer Elex, Remcos
or WannaCry from the collector filename. Family identification comes from
STORMSERVER.DLL, Storm Ser DLL and the recovered DDoS/task-dispatch code.

- The resource extraction routine at VA 0x402460 writes the embedded DLL.
  0x401150 allocates a buffer in a child process, writes a DLL path, resolves
  LoadLibraryA and passes its result and the remote buffer to
  CreateRemoteThread at 0x40123d. Other branches attempt service, registry
  and copied-image installation.
- Many configuration strings and several instruction spans have been
  overwritten with random ASCII. Some installation/launch paths can fail:
  for example, the module name supplied to GetModuleHandleA at 0x401213 is
  corrupted. This does not establish successful service persistence.
  Remove the generic ServiceDll/resource/API-co-occurrence conviction and
  its name-gated StormAttack fallback: their matchers do not bind a DLL to
  service registration or prove a hijacked service. Existing capability
  observations remain; these removals do not change the malicious judgment.
- DLL entry 0x1000741a reaches initialization at 0x10007176, which starts
  a reconnect worker at 0x10006922. The connector at 0x10006974 creates an
  outbound socket and sends a host report. Its dispatcher receives up to
  1320 bytes at 0x10006b45, copies the record and branches on its first dword.
  Operation 1 dispatches attack modes; operation 2 sets the stop flag.
  Mode 12 at 0x10006e0d passes the record's target, port, duration and
  worker-count fields to the attack launcher at 0x10002552. Additional
  operations include message display and download/process-launch attempts.
- The preserved worker at 0x1000228e creates WSASocketA(AF_INET, SOCK_RAW,
  IPPROTO_UDP), enables IP_HDRINCL, builds a destination and repeatedly
  sends twelve datagrams at 0x10002353..0x10002380 until stopped. The packet
  builder at 0x10002389 constructs packet/header bytes. Other workers also
  implement repeated sends. This is concrete attack functionality.
- The DLL configuration decoder uses XOR 0x2c then XOR 2, followed by a
  helper that subtracts 0x64 and XORs 0x12. The supplied configuration
  decodes to invalid endpoint text; no working C2 or successful network
  attack is claimed. The file still contains the hostile attack code.

Add a notable bounded receive/copy/opcode-dispatch signature, with addresses
and branch displacements wildcarded. Combine it with the existing raw-UDP
attack and corroborating family identity to recognize the packet-tasked
StormAttack variant. Required code evidence prevents names alone from
convicting. Final coverage has two hostile traits in the embedded DLL.
The outer PE also retains an accurate notable section-overlap observation;
intent is established by the packer/loader composites that combine it with
additional evidence.

Move the former tiny-overlay-loader composite into PE section metadata.
The DLL has substantial native code in .data; small size and a writable
entry section establish neither a tiny stub nor packing. The padding metric
includes unmapped gaps and cannot establish an appended payload.

## Verification

Run atomscan and cleave facts on all three original paths. Final atomscan
invocation used `--no-update --follow=none -f json`; its YAML findings confirm
the counts above independently of the ML classifications. Disassembly used
Rizin function analysis, cross-references and explicit disassembly after
clearing string metadata in the non-executable DLL data section.

`check.py` generates controls only in the supplied scratch directory. It checks
the two updaters and an identity/IP rename, removes the raw-socket protocol,
burst count and copied-record signature independently, removes family version
corroboration, and checks three inert writable-entry PE controls plus a
read-only-entry near miss. These test
rule dependencies; mutated malware controls are not benign verdicts.

Two pre-existing Python JSON bytecode hex matchers prevented all initial
atomscan runs from loading traits. Flatten their nested alternations without
changing the accepted marshal records. This is an engine-compatible syntax
repair, separate from the sample behavior changes.
