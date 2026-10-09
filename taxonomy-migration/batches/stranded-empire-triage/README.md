# Stranded Empire, Metasploit and DAVTest member triage

All 91 listed members were judged individually MALICIOUS: 55 Empire members,
34 Metasploit members and two DAVTest webshells. Each is executable attack code
or an archive containing executable attack payloads. None of the listed members
is inert documentation or an ordinary vendored library. The three parent
archives retain their confirmed MALICIOUS labels independently of these decisions.

[member-results.json](member-results.json) records each actual extracted path,
verified SHA-256, identification, marker note and final hostile/suspicious IDs.
Each member has 2–4 distinct hostile traits across its analysis tree. Markers
were written beside all 91 extracted files and the three original archives;
their notes are reproduced verbatim in the commit body. Extraction removed the
displayed `data/` prefix. The listed `data.tar.gz` is the mettle gem's nested
payload archive, identified by its exact requested digest, rather than the
Debian package's outer data archive. Both fetched Ruby modules also match the
requested digests.

## Behavior review

Every member received an atomscan report and cleave facts extraction. Source
review followed operative code, not just names or comment descriptions. Empire
members implement credential and ticket recovery, password spraying, process
and token injection, privilege exploits, UAC registry hijacking, remote command
execution, interception, keylogging, persistence or ransomware. Agent templates
implement encrypted tasking, command execution and result transport. The C
launcher executes an encoded PowerShell agent. The test Mimikatz copy contains
the same operational reflective loader and credential-theft payload; its test
directory does not make that payload inert.

Embedded PE payloads were decoded without execution. CLR metadata and IL review
confirmed that renamed Rubeus code harvests and caches tickets, roasts Kerberos
credentials and forges tickets. SharpSecDump retrieves remote registry hives,
parses SAM/LSA records and decrypts account secrets. Other embedded assemblies
implement credential prompts, browser-secret access, key/audio capture, spooler
coercion and token abuse. PowerShell wrappers invoke those assemblies.

All 30 GoAhead compressed shared objects were decompressed and inspected.
Bundled C source and rizin disassembly/imports corroborate constructor-based
`LD_PRELOAD` execution, fork, reverse connect or bind/listen/accept, socket
redirection to standard descriptors and shell execution. Mettle archive review
located actual multi-platform agent binaries, C2 transport and TLV task handlers;
hostile findings belong to those payloads, not ordinary bundled support files.
The Next.js module leaks server-action key material and builds an executable
Flight gadget; the SonicWall module chains SSRF, CouchDB/Erlang command execution
and an authenticated privileged command-injection path. DAVTest's ASP/PHP
members directly execute request-controlled shell commands. Binwalk was not
installed; Python archive/encoding parsers, rizin and CLR IL inspection supplied
the deeper analysis instead. No sample was executed.

## Trait corrections and migration

Bare Winlogon, CSRSS and Services names now live under process information;
remote-thread APIs co-occurring with those names are notable injection
capabilities. Those observations alone establish neither masquerading nor
privilege escalation. The redundant ntdll/RtlAdjustPrivilege escalation composite
was removed; the canonical notable API trait remains. Policy names co-occurring
with registry-write APIs now have accurately named notable micro-behaviors.
They do not establish that a disabling value is written to the named policy.

[consumer-audit.json](consumer-audit.json) records every affected identity,
exact cross-namespace reference and ancestor directory consumer. All affected
consumers use the new canonical identities; no compatibility aliases remain.
Unmoved source composites retain their behavior. Type/platform gates and
specific exclusions were preserved. Signed/vendor severity downgrades were
removed from the neutral observations because signatures do not negate an API
or name reference. The broad impact consumers were reviewed: neutral policy
co-occurrences should neither establish impact nor suppress a malware identity.
Unsupported masquerade/escalation mappings were removed from the moved atoms.

Rubeus identification now also supports renamed builds through two distinctive
help passages, while existing attack composites still require ticket-abuse or
roasting evidence. New managed registry-secret composites require the relevant
SAM/LSA subpath, parser, decryption or remote-dump helper and explicit secret
report heading. Their supporting observations reside in registry or crypto
micro-behaviors; credential theft claims reside in credential-access/registry.
This separates offline hive recovery from live process-memory dumping. These
traits use behavior and corroborated tool identity, never specimen hashes or
the renamed assembly namespaces.

## Verification

The final scan covered all 91 members and verified their hashes, marker notes
and 2–4 hostile traits. Four benign source controls in
`testdata/stranded-empire-controls` check names alone, policy documentation,
unrelated registry writes and registry-path reporting: each has zero hostile
findings and at most one suspicious finding. Their expected rule matches and
nonmatches are reproducible with that directory's `check.py`.

A genuine benign CLR executable also produced no new managed-secret findings.
Byte-preserving near misses removed the SAM decryption helper or remote LSA
dump helper: only the corresponding hostile claim disappeared. Removing actual
roasting method names and hash-output prefixes retained Rubeus identity and
ticket detection while removing the roasting claim. Positive rule precision
was 6.8/6.4 for SAM/LSA and 6.8/7.1 for Rubeus ticket/roasting objectives.
The preliminary validator passed its fixture suites. The stricter final
validation identified a directory cap and description-length issue; the two
new hive subpaths were grouped with the offline-hive helpers after checking
that existing registry-key atoms do not duplicate these exact paths, and the
description was shortened. Final repository validation is required; these finite checks do not prove universal absence of
false positives.
