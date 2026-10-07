# Stranded-member trait corrections

Run `python3 testdata/stranded-member-controls/check.py` from this checkout.
The checks analyze bytes only; they do not execute the specimens.

## Placement and matcher audit

- `rotational-xor-logic` becomes
  `micro-behaviors/data/codec::powershell-repeating-key-xor-expression`.
  Its matcher and PowerShell/Windows scope are unchanged. Severity changes
  separately from suspicious to notable: indexing a repeating key proves no
  bit rotation or concealment. Other rotational rules remain in place.
- `windir-value-assignment` becomes the notable registry observation
  `micro-behaviors/os/registry/access::powershell-windir-property-access`.
  Effective file/platform scope is preserved; the matcher now requires a
  Get/Set/New-ItemProperty cmdlet rather than an arbitrary -Name argument. The former
  `user-windir-environment-hijack` pair was redundant and is retired. Its
  SilentCleanup consumer directly requires the property access, Environment
  key, registry-write evidence and task path within 180 bytes. This deliberately
  tightens the former two-reference proximity gate; reads alone prove no hijack.
- Generic FLS cooccurrence moves from the injection objective into
  `micro-behaviors/process/tls/fiber`. Matchers, size/platform/file scope and
  exclusions are preserved. Severity changes separately to notable. FLS APIs
  do not prove scheduling, injection or evasion. The outer fiber-dispatch
  composite was redundant because its thread-creation leg already satisfied
  its process-creation leg; it is retired with its alias comment file.
- SMB command serialization moves into direction-neutral `data/codec` with
  unchanged matcher and scope. Remote SMB relay remains lateral movement;
  loopback reflection belongs in network-service privilege escalation.
  NBNS header serialization, ID assignments and sending are neutral
  observations. Two less-than-255 comparisons are a neutral numeric
  observation in data/arithmetic; the matcher does not claim loops or
  branching. The poisoning objective requires those bounds alongside both
  transaction-ID assignments, packet construction/transmission and local
  authentication reflection/service execution. No standalone loop rule or
  unrelated Java detector change is needed.
- Native empty-buffer structure belongs in `metadata/build/scaffold`, not
  malware identity. A raw-byte regex with a 10,000-byte minimum checks all 9,993 zeros following
  the seven-byte PAYLOAD marker. The Samba exception requires module identity
  and its root-user import as well as that empty buffer. Both the native and
  third-party shell detections use the same exception.
- Shared Inveigh challenge serialization does not identify InveighRelay;
  the third-party identity match is disabled. Capture and relay behaviors
  remain detected. The PHP upload-only third-party label is also disabled
  because it misdescribes the full command/database webshell.

Exact-reference and ancestor-selector searches were performed across all four
rule tiers. Removed IDs have no remaining consumers. The Empire injection
selector remains an injection selector and intentionally excludes neutral FLS
cooccurrence. No XOR rotational directory selector needs widening; retained
consumers reference specific rotation rules. The keys and loops leaves were at
their 100-rule caps. The new windir observation was refined to actual property
access and placed in access; its redundant pair was removed and
byte-bound comparisons were placed with numeric operations. No existing rules were moved merely to make room. The windir and
serialization consumers use their new qualified IDs. No ATT&CK/MBC mapping is
assigned to the neutral replacement observations. New objective precision
scores exceed the 3.5 authoring bar; local NTLM reflection scores 6.1.

A second placement review checked the supported claims independently of the
former directories: neutral API/codec/property observations require no attacker
intent; local reflection and credential-directed poisoning do. Existing
admitted leaves are reused and no engine taxonomy expansion is required.

## Controls

The minimal PE files contain only synthetic import tables: multiple FLS APIs
plus a thread-creation import, FLS alone, or thread creation alone. PowerShell
fixtures distinguish repeating-key from fixed XOR, a registry-property read
from a variable assignment or unrelated -Name argument, UTF-16 command
serialization from UTF-8, and remote relay from local reflection. A local
reflection case without forged-packet transmission does not satisfy the
poisoning objective.

The Samba controls preserve the analyzed x86 ELF loader. The empty control
retains the complete unpatched buffer. One negative control changes its marker;
another changes only its last buffer byte. Both must stop the exclusion,
proving that a zero prefix cannot hide a populated buffer. These controls are
never run.

The full member corpus was re-scanned: 89 malicious members have 2–4 hostile
traits each; the unpatched Samba member has zero hostile and zero suspicious
traits. Ordinary libraries elsewhere inside the payload gem are not
individually convicted by their containing archive. Member evidence and
judgments are recorded in the external triage report; each marker note is
preserved in the commit body.

Baseline arithmetic controls use `cleave test-rules`: the installed scan
renderer strips baseline findings that no firing composite consumes. The
attack controls additionally check the normal atomscan output. The bounds
controls distinguish two comparisons, one comparison, and the non-byte value
2550 so a numeric prefix cannot satisfy the observation.
