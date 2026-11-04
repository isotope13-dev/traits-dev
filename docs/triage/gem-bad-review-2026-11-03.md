# Ruby gem mislabeled-bad review — 2026-11-03

The 21 gems were unpacked and inspected without executing their contents, and both scanners ran with caching disabled.

Eight `monolith-twirp` packages (`8a58b4f5657c`, `dcfe7e70e0a9`, `1226d19faa8b`, `ffeb028cbf5c`, `98d06ad625e1`, `394e0b506860`, `736c568b3de8`, and `2418b1fd029d`) remain bad. Their Ruby code encodes hostname, user, and CI information into DNS queries to an external endpoint. The existing `encoded-label-dns-host-exfil` finding is hostile in both scanners. `f5327dcef86c` also remains bad: its install and runtime code collects sensitive environment values and credential files and posts them to a configurable endpoint; existing hostile findings cover that behavior.

`96252afcb9c8`, `dd21fcaa8076`, `eff3f7dc1210`, `955316946080`, `beeab6f2ab6c`, `80ec6aa08070`, `ee79a9071f3f`, and `cde81eb32a1a` remain bad. Their scripts collect remote responses, encode or package the results, and use embedded registry credentials to publish the data or store it in webhook URLs. Several use YARD configuration to load the code during documentation processing. `80ec6aa08070` additionally packages the working directory and runtime details. New combined RubyGems upload and webhook findings flag these behaviors in both scanners; controls that remove the credential, Base64 encoding, or working-directory collection clear the corresponding findings.

`1a42d09e1837` and `3d3963d5bc6a` are inert placeholder gems and were moved to good; the former contains only a comment, with no executables or extensions. The name-based placeholder rules were lowered from hostile to suspicious, and their descriptions no longer claim that a name alone proves an attack. This leaves one suspicious finding on the first placeholder while preserving hostile DNS findings on the separately implemented exfiltration packages. `a21b12819877` and `d9a7dad1899c` are a query-language library and an authentication integration, respectively, and were moved to good.

Full validation passed after the changes. The review yielded 17 bad and 4 good.
