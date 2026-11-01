# Encoded carrier evidence review

Sixteen rules from the JavaScript, JCL, Windows DLL and batch legacy carrier files moved to evidence or behavior categories. Their predicates, scopes, confidence values and suppressions are unchanged.

- A JavaScript `unescape` prefix and separate file-output stream do not establish that a PE is written. Fragmented `String` text and a separate `eval` do not establish that the fragment is evaluated. These are suspicious file-write and evaluation profiles. A separate WSH/WMI execution combination retains its execution objective.
- JCL `EXEC` of a SOCK-prefixed member and adjacent DD declarations are observations of the named syntax. The combination with a hex deck and TSO references is suspicious, without claiming a network stager.
- A `rundll32` export and a small DLL with dynamic-loading API names are binary and loading observations. ROT1, XOR and a `desktop.ini` reference indicate obfuscation clues, not a demonstrated sidecar loader. The 64 KiB maximum remains on the small-DLL profile because it defines the profile's size claim.
- A GitLab executable URL combined with a temporary path and batch substring syntax does not establish a download or execution. A Rouki obfuscator label or author reference is a component under the named tool, because the author link alone is not proof the tool is present. Its dependent combination with Japanese text and substring syntax is a suspicious profile, not a hostile loader.

The metadata and component classifications avoid asserting capabilities or family identities from names alone. Unsupported inherited attack metadata was removed from observations.
