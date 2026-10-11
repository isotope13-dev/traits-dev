# ChroMapper Linux second review

Archive SHA256: f4c4f2199a8b4fed4c5cd296105232b5f8ef013ab51a0f402421613352e5ae5c.
Judgement: BENIGN, including UnityPlayer_s.debug, UnityPlayer.so, System.dll,
and mscorlib.dll. Main.dll implements the ChroMapper Beat Saber editor.

The launcher jumps directly to Unity PlayerMain. The Unity player and its
symbol-bearing companion have identical .text, .rodata and .data bytes.
The four preload shell convictions originated in a substring collision with
vrpn_FILE_CONNECTIONS_SHOULD_PRELOAD, not an LD_PRELOAD variable reference.
Main.dll IL loads local Plugins/*.dll, extracts beatmaps, and acquires Google's
Android platform-tools for Quest support. System and mscorlib have Mono
framework identities and define the networking, cryptography, file and
reflection APIs that the former loader profiles combined without data flow.

Corrections retain neutral API capabilities. Resource/crypto/write and
resource/resolver/write co-occurrences no longer claim extraction, dropping or
obfuscation. HTTP cache and DTLS heartbeat strings move to their protocols.
AssemblyResolve subscription API evidence moves to reflection. UTF-16 CLR
error text no longer counts as concealed reflection. Native integer tables,
PhysX PxTaskMgr, graphics "screen", managed System.dll and CLR TaskScheduler
no longer imply BPF, Task Manager, terminal type, NSIS or Windows autorun.

Focused controls: preload-positive.c must match linker/env::ld-preload;
preload-near-miss.c must not. taskmgr-positive.py must match
process/info/name::taskmgr-process; taskmgr-near-miss.py must not.
No sample filename or hash participates in the corrected detection predicates.

The BPF controls distinguish an ICMP identifier load followed by JEQ from
an unrelated integer table with the same isolated load-sized byte pattern.
Mono mscorlib resources are collation tables and mscorlib.xml; System resources
are notification sounds. TLS RC4-HMAC-MD5 strings are not Kerberos etype 23.
