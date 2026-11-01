# Embedded-source sink review

Thirty embedded-source rules moved out of the legacy dropper directory. Marked
file-range evaluation, transformed-code execution, remote constructed code,
and hidden file-backed execution now use their respective payload sinks.
Ruby DATA-section evaluation and a zlib/Base64/eval pattern are capabilities;
Base64 with unsafe YAML loading is suspicious parsing evidence, not proof of an
exploit. The Code Verification/XOR rule no longer attributes a family that its
conditions do not identify.

The existing hosts-file and plugin dropper ancestor consumers retain the moved
alternatives. The transformed execution leaf was also reviewed: eight rules
that specifically require blockchain-derived source now use the existing
blockchain category. The adjacent obfuscated-eval and hidden-child rule stays
in transformed execution because it does not require blockchain evidence.
Its explicit consumers were updated without broadening directory selectors.

The final review divided the transformed neighborhood by activation behavior
before adding the remaining JavaScript and PowerShell execution rules.

The final 33 embedded JavaScript and PowerShell rules have now moved. The
transformed-execution neighborhood is divided by shell, child interpreter,
constructed code and direct evaluation. The generic encoded-stage file's
30 KB upper limit was removed; its 8 KB minimum and distinctive content and
evaluation conditions remain.

A `data-base-title` marker does not establish a URL or fetch, an eval alias
assignment does not establish that the alias was called, and registry writes
beside AppDomain and Base64 references do not establish an assembly load.
Those observations and their weak composites now state their evidence and use
notable or suspicious severity. A rotation counter is no longer named RC4,
and scheduled-task arguments are not described as an established key.
The two dropper ancestor consumers retain the migrated alternatives.

The former 30 KB maximum contradicted a required long-line observation whose
minimum was 32,768 bytes. The long-line observation now measures the stated
line property without a whole-file size range, and its general Base64-cluster
building block has no maximum. The intentionally compact profile retains its
30 KB maximum; its conditions can now actually match. A synthetic 21 KB
JavaScript file matched the line, cluster and compact-profile observations.
The long-line consumers were reviewed: their hostile findings also require
independent decoder/evaluation or hidden WMI/ActiveX evidence. Files outside
the previous size range can now supply the baseline line observation.
