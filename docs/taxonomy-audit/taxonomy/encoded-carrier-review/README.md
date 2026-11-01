# Encoded carrier review

Fourteen rules from seven legacy encoded-carrier files were classified by their evidence. Match predicates, scopes, confidence values and references were preserved.

- PHP percent-u word runs, substring syntax and bin2hex combinations describe an encoding shape; none establishes shellcode, so the old hostile composites are notable encoding observations.
- A VB `4D5A` string and numeric array do not establish a PE payload. They are a component and a suspicious encoding profile respectively. The combination of a longer hex PE header, a two-character loop, file-write and run clues remains an execution objective.
- Go gzip decoding, file writing and a temporary-path command constructor are a suspicious file-write profile; the command constructor alone does not establish a launch. Lua dynamic loading with hex and shell clues, and PowerShell Base64, deflate and variable-name indexing, are suspicious encoding profiles rather than established execution.
- C# Base64 MZ-prefix writing and the combination with KDF and assembly-load references are file-write and module-loading profiles. The sandbox-gated encrypted-archive and hidden-launch combination remains an execution objective.

Criticality was lowered where the evidence fell short of the former hostile execution or shellcode claims. Unsupported technique annotations were removed from observational profiles. No exclusion or match-count thresholds were changed.
