Version-drift triage evidence (2026-10-07)

All three submitted packages are BENIGN. Earlier releases were downloaded
without executing their installers or package code.

WEDOS Protection & Cache Performance (wgpwpp) 2.2.2 versus 2.2.1:
https://downloads.wordpress.org/plugin/wgpwpp.2.2.1.zip
SHA256 188d26060bf6c680590d9f0beaa55ef3d73a20c2d89a97f8e8c41bb331e04994
Cache/Engine.php already wrote the MU-plugin cache runner in 2.2.1.
The new runner rejects error responses and refreshes old local templates;
it does not acquire remote PHP or introduce a request-driven command sink.
Snapshot.php is new: it measures the local site, captures and parses its
TLS certificate without verification, counts admins and pending updates,
and stores bounded daily health records. Only the public homepage URL is
sent to the vendor performance endpoint. The new vulnerability feed is
SHA256-checked data, matched against the local inventory, not executed.
The UI and vendor CDN changes use the established vendor infrastructure.
This build enables vendor CDN by default despite comments/readme claiming
otherwise; that inconsistency is not evidence of an attacker payload.
TLS options remain notable capabilities; a generic PHP option does not
establish an evasion objective. MU-path/write proximity is now described
literally, with its backdoor consumers retaining attack-specific legs.
Generic file_put_contents no longer claims event-triggered execution or
remote transfer through its ATT&CK tags.

Orchestra Tennant 0.3.1 versus 0.3.0:
https://proxy.golang.org/github.com/realkasparov/orchestra-tennant/@v/v0.3.0.zip
SHA256 76f61940698ab82e3aa975190f0614b73052a5f2a45d5acbd01eef0d0cbfb9a4
Only release workflow, README, main.go, service.go, install.sh and new
update.go change. The installer implementation is unchanged; its comment
and README URL move from raw main to the project's release asset.
The new explicit update command downloads its platform archive and
checksums.txt from that same GitHub repository, verifies SHA256 before
extracting a regular binary file, atomically replaces its executable,
and restarts its installed user service. Skills are unchanged.
An archive-wide skill-plus-README-pipeline join incorrectly attributed
ordinary README install documentation to agent skills. The replacement
requires both observations in the same file and reports a neutral capability.

Wolfi libudev 261.3-r4 versus 261.3-r3:
https://packages.wolfi.dev/os/x86_64/libudev-261.3-r3.apk
SHA256 d83cb7a4f8aafec206cde573d375f52426b2cdfbb5d905fe19e1a3ca8853d351
Both packages use the same systemd v261.3 source commit.
The melange diff adds bootctl-status-random-seed.patch and refreshes build
dependencies/package provenance. Rizin section comparison shows byte-identical
.text, .rodata, .init_array and .dynsym; imports, symbols and extracted
string sets are identical. Disassembly of detect_vm_cpuid and
 detect_vm_dmi_vendor confirms normal systemd CPUID/DMI classification.
These tables already exist in r3; no new anti-analysis code was added.
The VM vendor composite now uses the existing systemd-native-library
exception, which includes libudev, rather than only libsystemd's basename.

Controls:
cache-mu-write.php: notable path/write proximity, no backdoor conviction.
mu-command-backdoor.php: hostile MU-plugin webshell consumer still matches.
SKILL.md and skill-installer.zip: same-file pipeline documentation matches.
unrelated-readme-installer.zip: skill without pipeline plus unrelated README
pipeline must not match the agent-skill pipeline documentation composite.

Final atomscan scans of all three submitted archives report zero suspicious
and zero hostile YAML findings, while retaining their notable capabilities.
