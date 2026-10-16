Mirai-derived native bot review
==============================

All three specimens are **MALICIOUS**, based on executable propagation and
process-killing paths. Reputation and ensemble scores were not used as proof.
These are stripped, statically linked Linux/uClibc builds of the same bot;
they are not dependency archives or ordinary administration utilities.

| SHA-256 prefix | Architecture | Main | Telnet loader | Native process scanner | RC4 configuration transform |
|---|---|---|---|---|---|
| d5862fa98e68 | ARM, little endian | 0x11c78 | 0x14128 | 0x11400 | 0x164a4 |
| f47f2abebfcc | PowerPC, big endian | 0x1000aab4 | 0x1000d344 | 0x1000a1e4 | 0x1000f7e8 |
| 05fc0e8dc8e4 | MIPS O32, big endian | 0x40c3a8 | 0x40f6d8 | 0x40b7b4 | 0x412918 |

Static evidence
---------------

`atomscan --no-update --mode slow --follow=none <sample>` and
`cleave facts <sample>` were run for each specimen. Rizin disassembly was used
to follow initialization, credential construction, connection states, remote
command sends, packet framing and process termination. No specimen ran.

* The loader populates default username/password pairs, including root with
  xc3511 and Zte521. It generates target addresses, connects to Telnet port
  23, handles login failures and shell prompts, and sends credentials and
  shell commands through the target's socket. In ARM, dictionary construction
  is at 0x14328 onward; port 23 is placed in the connection at 0x14604.
* Authenticated shells receive BusyBox probes, writable-directory tests,
  wget/TFTP/FTP/curl script delivery and a DLR payload stage. The staged
  executable is chmodded and launched. ARM 0x14a90–0x14aa0 sends the actual
  chmod/execute command through send(), rather than merely displaying it.
* The bot transmits seven hex-escaped shell fragments using BusyBox echo -ne,
  reconstructing a process-killer script for the remote host. ARM
  0x14e64–0x14e98 sends the echo prefix and fragment selected from the table.
  Rejoining and decoding those fragments in every specimen yields the same
  script: enumerate /proc/*, inspect /proc/$pid/exe, test the `(deleted)`
  suffix, and issue `kill -9 "$pid"`. The native scanner also enumerates
  processes and inspects executable links, with filters for download tools,
  login and deleted images, before its kill path.
* The configuration initializer implements RC4 KSA and PRGA with XOR swaps.
  Reproducing its exact swaps (including the same-index behavior) recovers
  `bigr.dyn`, `lkol.dyn`, `The Peoples Bank of China.`, and
  `TSource Engine Query`. The encrypted records and 256-byte key are identical
  across all three builds. The ARM key is at file offset 0x1a2bd; the
  PowerPC and MIPS copies are at 0x18b94 and 0x1e250. These values are analysis
  evidence, not required signature strings or evidence of observed contact.
* ARM 0x1048c resolves the configured domain; 0x10c0c opens the control
  connection. 0x12608 receives framed data and XORs payload bytes with a
  cycling four-byte state; 0x10e78 dispatches task messages. The attack parser
  at 0x828c extracts duration, vector, targets and options; 0x8190 forks a
  timed attack worker and calls its registered vector. The registered UDP
  vector at 0x8a7c constructs IP/UDP packets and repeatedly calls sendto at
  0x912c. Thus the recovered query is consistent with implemented flood
  functionality, not evidence that a game client is the program's purpose.

Rule decisions
--------------

Retain credential-associated propagation and Mirai-family identification.
Add a separate hostile finding for the deleted-image killer carried by that
stager. The escaped filter/kill observation remains notable when isolated;
maintenance scripts can have that behavior. Add notable RC4 transforms for
the three instruction sets and hex-escape decoding context. The signatures
contain no endpoint, key, branding, hash, exact size or staged filename.

Correct three misleading findings:

* `GET/dlr.` is a payload-search fingerprint used by the scanner, not a
  complete malformed HTTP request. Retain the family fingerprint under an
  accurate name and require a protocol version for malformed requests.
* `/config/` is one of the loader's filesystem staging-directory candidates.
  Require HTTP route-registration syntax before claiming a config/user route.
* `KERN_SECURELEVEL` is passed to getenv at ARM main 0x11c8c–0x11cb4, then
  used as an optional identifier. A macro spelling alone establishes no BSD
  kernel operation. Retire that unsupported atom; retain the actual
  `kern.securelevel` sysctl-name observation.

Verification
------------

Run `python3 testdata/taxonomy/mirai-native-review/check.py --cleave cleave`.
The 18 controls use generated, non-executable relocatable ELF containers and
source snippets. They cover all three RC4 loops and missing-XOR near misses,
changed script variable names and escape case, incomplete/distant filter and
kill evidence, maintenance without credentials, decoder-prefix-only data,
fingerprint versus HTTP request, and filesystem paths versus registered
routes. They assert that maintenance and ordinary strings do not activate
the new hostile finding. No fixture executes the embedded instructions or
shell text.

Final rescans show three hostile traits per specimen: credential propagation,
Mirai loader identity and the deleted-image killer. Each has its correct
notable RC4 transform and escape-decoding context. The three unsupported
behavior claims no longer fire.
