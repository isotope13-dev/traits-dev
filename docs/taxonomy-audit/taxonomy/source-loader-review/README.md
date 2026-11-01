# Encrypted source staging review

- Source XOR/RC4 clues with allocation and protection API references are now
  a memory-operation profile. The rule does not establish that the XOR result
  is decrypted into executable memory or that it runs.
- RC4, PE-resource extraction and a driver, registry or thread-hijacking clue
  are a suspicious PE API profile. A new hostile thread-hijacking objective
  combines that profile with the actual thread-hijacking leg, preserving a
  behavior-specific finding for that stronger case. It is limited to the C
  and C# types supported by the hijacking rule.
- The forwarded-export consumer now belongs to memory-operation profiles.
  Export forwarding and the memory/XOR profile do not establish that a
  proxy DLL decrypts or runs a payload, so its hostile claim was removed.
- The HackSkills archive download/extraction documentation rule identifies
  a known offensive tool rather than establishing hostile delivery. It moved
  to `well-known/tool/offensive/yaklang-hack-skills` as notable. A 2 GiB
  maximum satisfies the well-known size policy; the existing documentation
  identity dependency has its own 5 MB maximum. Both can limit detection.

Original match predicates, explicit scopes, confidence and exclusions are
unchanged; the proxy dependency was redirected. Names, descriptions, severity
and unsupported attack annotations changed to reflect the evidence. The
original broad RC4/resource rule was not narrowed to the new injection rule.
