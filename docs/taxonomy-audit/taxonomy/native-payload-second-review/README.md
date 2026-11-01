# Native payload: embedded, command and editor review

Twelve rules moved out of legacy native-payload staging, reducing that
location from 73 to 61 direct rules:

- Four Go/Rust embedded-ELF and autostart/module-name combinations moved to
  embedded-binary profiles. The Go persistence-like profile is suspicious;
  service and autostart references alone do not establish a persistence
  operation. The Gogra consumer was redirected.
- The Mach-O Base64/overlay/shell-API combination moved to an overlay profile.
  The native shell write/chmod/cleanup combination moved to file-write context;
  neither proves that the embedded data was launched.
- The editor activation rule and its tree-sitter flow moved intact to the
  fetch-and-spawn execution sink. The tree-sitter matcher binds the response,
  writer and launched path; its VS Code supply-chain consumer was redirected.
- The Brass Audio filename-shaped path moved to a file-path subject. The
  malformed OOXML/Base64 PE signature combination moved to an embedded-binary
  profile: it does not require PE execution. Two unsigned GUI/API/entropy
  combinations moved to PE API profiles; their conditions do not establish a
  fake interface or a downloader.

Original predicates, explicit scopes, confidence and exclusions were
preserved apart from three removed size gates. The Go embedded-ELF profile no
longer requires a file of at least 1 MB; that increases the possible matches
of its Gogra consumer. Its underlying ELF-header atoms still have a 50 MiB
maximum, and its Base64 ELF alternative has a 1 GiB maximum. Both GUI profiles
no longer impose a 128 KiB maximum. One still depends on an entropy trait with
32 KiB minimum and 16 MiB maximum. No full composite fixture was constructed
for these size changes; the rule structures were checked before and after.
