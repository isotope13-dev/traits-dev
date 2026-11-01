# Self-extracting and signed NSIS staging retirement

Eleven rules moved from the legacy `self-extracting` and `signed-nsis-bundle`
staging directories, which are now removed. Configured launches from opaque
self-extracting bundles now live under `execution/payload/file-exec/spawn/sfx`;
this groups the launch behavior instead of the carrier's signing status. The
Microsoft-signed NSIS combination with remote-process memory and thread APIs
moved to process injection. These rules retain their previous match conditions,
confidence and hostile or suspicious severity.

The 7-Zip overlay and API combination, the signed embedded-PE overlay, and the
NSIS embedded-PE/system-reference combination moved to installer or embedded
binary profiles. Their descriptions no longer infer a signed loader, sideloading
or RunOnce persistence from generic API, DLL-name or registry-path references.
The latter profile is suspicious rather than hostile. Exact family consumers
were updated.

The hosts-file sinkhole rule used an ancestor reference to all legacy droppers.
It now also accepts the moved traits: the new SFX execution directory and the
existing process-injection directory cover their full groups, while explicit
references retain the three profile alternatives. This preserves the moved
members of the former alternative set. `TAXONOMY.md` documents the SFX launch
sink. Parsed comparisons verified all eleven rules' match legs and constraints.
