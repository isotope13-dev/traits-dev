# Dropper interpreter-stdin activation

`raw-ip-fallback-shell-dropper` requires three linked observations: a downloader
fallback chain, a raw-IP endpoint, and `curl` output piped directly to a shell.
The payload source is consumed through the new shell interpreter's stdin, so its
canonical dropper home is `objectives/command-and-control/dropper/interpreter-stdin`.
It does not stage and launch a file, and it does not establish a persistent
reverse shell. The downloader fallback remains a neutral HTTP capability that
the objective references.

The rule moved from `dropper/delivery/execute-download` with its matcher,
platform/file-type scope, confidence, criticality and ATT&CK/MBC metadata
unchanged. Soft validation passes **1,837/1,837 fixtures**. The source leaf drops
from 294 to 293 rules; strict validation remains at 59 issues, including 165
over-cap directories.
