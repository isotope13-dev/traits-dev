# Python response-evaluation review

Thirty rules moved out of the last legacy response-evaluation subtree. Network
execution and decoded network execution use the corresponding payload sinks;
JSON-supplied PowerShell commands use command dispatch; ordinary HTTP response
evaluation remains a capability. Source names, JSON field access, URL
construction, and unbound reflection clues live with their evidence. The
Connexion schema-resolver path is a notable library identity clue, not proof of
malicious code.

A Python exec near shell command output has no required network input and is
classified as suspicious input evaluation. Unsafe YAML deserialization of a
network response is a suspicious capability rather than proof of an exploit;
HTTP next to an unsafe loader is a separate co-occurrence profile. A 120 KB
whole-file limit was removed from the `module_code = ...read().decode()`
observation. Its exact naming and read/decode syntax still apply; its hostile
consumer additionally requires urllib, an exec call, a module path and other
context. A padded Python sample over 120 KB matches the revised observation.

The hosts-file and plugin dropper ancestor consumers retain their migrated
alternatives. Their existing URL-construction directory selector already covers
the relocated API-code path observation.

The operation-reference and script-evaluation leaves had 71 and 72 rules.
Seven binary beacon-name string observations moved to binary-string profiles;
seven decoded-source observations were separated into encoded-network,
text-shape and process-evaluation profiles. Existing exact consumers were
updated. These moves leave 64 and 65 rules in the original leaves, respectively.
