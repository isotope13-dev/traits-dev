# Standalone runtime review

Nineteen non-Deno rules moved out of the legacy standalone-runtime leaf.
Fetching a runtime and launching it in a temporary directory uses the network
spawn sink; a Composer Run-key and Node HTTP combination uses registry-script
persistence. Fragmented Node distribution text, dependency names and unbound
Python release/spawn/hex clues describe their evidence. `get-pip.py` text is a
name reference, not proof of a download. A WSH hidden command beside Python
runtime names is suspicious evidence, not proof of a staged runtime.

The hosts-file dropper ancestor consumer retains these alternatives; its existing
process-artifact selector covers the corresponding moved profile. Four existing
Node rules requiring network fetch moved from generic runtime-spawn to the
network-fetch spawn sibling before adding a new runtime-spawn rule.

The AppData, environment-read and runtime-platform leaves contained 82, 93
and 79 rules. Their rules are now grouped by app-data subject, environment
read type, and runtime observation respectively. Existing directory selectors
remain at the parent and continue to include the split leaves. An existing Go
exfiltration move-preservation check was updated and passes.

The 36 Deno-specific rules also moved out of the standalone leaf. Direct
operations go to their corresponding capabilities; encoded text goes to
encoding evidence; and combinations retain only the intent their evidence
supports. A remote module-loading chain with a host profile remains an execution
objective. The hosts-file consumer retains the moved alternatives.

The crowded HTTP-path (91), HTTP API-path (93), browser application-path (83),
CI environment (80), and environment-enumeration (75) leaves were split by
subject or operation. Enumeration keeps its original engine-allowlisted file
path; reporting and procfs observations are sibling leaves, and the three
existing enumeration consumers explicitly include them. Hostname observations
and process-identity queries were also split. A Go process-ID query was moved
out of hostname; selectors of those parent directories now reflect that
correction. The new Deno hostname, environment-read, and OS-version queries
also participate in existing selectors of those subjects.
