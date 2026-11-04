# Static-library filetype mislabeled-bad review — 2026-11-04

The snapshot contains 40 files: 25 bad, 2 good and 13 inconclusive. Most are legacy executables or other data with `.a` names rather than static libraries.

`4cd2399424e9`, `435fead38758`, `26dccd740c04`, `553a5ce58384` and `067f7f320dd9` are DOS executable infections; both scanners already identify their encrypted body, host-file modification or resident execution-hook behavior. `b9cf1e71ec95` installs an INT 21h handler, searches files with FCB services and writes FCB records. A new finding combines the handler, host-restoration trampoline and FCB search/write instructions. Both scanners match; changing the FCB write service clears the control. These six are bad.

`cc6fc4302b01` is an encoded ASP command shell already identified by both scanners. `11d526b14b26` is an MHTML document embedding a Base64 PE and an executable object codebase with XOR-obfuscated VBScript. The extracted executable was UPX-packed; unpacking and scanning did not establish its behavior, so the finding rests on the combined MHTML construction. Both scanners match the original, and changing the MHTML codebase scheme clears the control. Both are bad.

`8f1e9817c614` is an email with a ZIP attachment containing a PE named with a misleading `.txt`, a long run of spaces and a `.pif` extension. A new finding detects the padded document disguise on the actual PE. Both scanners match the extracted ZIP and clear a control with an ordinary `.pif` name. The original email was not traversed to the embedded ZIP by the initial scanner runs, so detection requires extraction. It is bad as a disguised executable delivery.

`3b4c7f289e63` is a conventional libsodium import library with cryptographic import symbols. Both scanners found no hostile traits, and its archive members and symbols were reviewed; it is good.

`3a66d492d145` installs an INT 21h execution hook and writes an in-memory COM image; `20a0eb2cb50d` seeks through a host file, appends a body and rewrites its three-byte entry; `e51070dca23e` installs a resident handler, updates files and copies saved host bytes back to the COM entry; `898b8686cb81` restores its host entry and installs a resident FCB-search handler. All four are bad. New findings combine those instruction patterns with existing service facts. Both scanners match each original, and controls changing the relevant write or restoration operation clear each respective finding. The findings combine static file-level evidence and do not prove a specific runtime path was taken.

`4fb45946cb8a` combines BIOS sector writes, a resident interrupt handler, forced read/write file handles and directory-size concealment. It is bad. A new composite matches both scanners; changing the sector-write instruction to a read clears the control.

`9ae925f9b205` is an LLVM/MinGW toolchain archive with 6,310 entries and approximately 398 MiB uncompressed. Atomscan reported no hostile traits across 5,665 extracted entries, while the cleave run timed out after 150 seconds. The size and incomplete scan prevent a full embedded-payload review, so it is inconclusive; Hopper records that via the purgatory compatibility target.

`c6237ffd02b5` installs an execution handler, performs read/seek/write and timestamp operations, and writes a 24-byte file prefix after seeking to the beginning. It is bad. Both scanners match the new combined finding, and changing the prefix-write length clears the control. The finding does not independently parse the rewritten header.

`1eaa9ba37249` is a boot-sector image that reduces reported BIOS memory and combines a resident INT 21h execution handler with disk-sector and file-write instructions. It is bad. A new finding combines these facts and the boot signature; both scanners match, and changing the memory reduction to an increase clears the control.

`089261bdb3ce` restores three saved bytes to the COM entry, searches for files, opens them for update and writes them. Its initial jump wraps within the 16-bit segment to the appended code. It is bad. Both scanners match a new combined finding, and changing the three-byte restore length clears the control.

`7ab58407a5e6` transfers control to appended DOS code, restores four bytes at the COM entry and searches, opens, reads and writes executable-compatible files. It is bad. Both scanners match a new combined finding; changing the restore destination clears the control.

`a2da326f2c11` contains a dense DOS code region and a bootstrap that sets the processor trap flag and installs an interrupt vector; it also contains a VSAFE/VWATCH removal request. It is bad as hostile obfuscation with security-tool evasion. Both scanners match the new composite; changing the trap-flag bit clears the control. The protected body was not fully decoded.

`a5787bfb0c5b` jumps into an additive decoder whose key evolves by multiplication. Static decoding exposes DOS host-entry restoration and self-appending file-infection behavior, which both scanners flag in the recovered stage. The original is bad as hostile obfuscation; both scanners match the new decoder finding, and changing the key-update operation clears the control.

`c7a8f6cd8601` starts with a near jump into a tail arithmetic-noise loop, while a 4 KiB region of the body has 7.73-bit entropy. It is bad as hostile obfuscation. Both scanners match the new finding, and changing the loop clears the control. The protected body was not decoded, so no specific payload behavior is asserted.

`6fac38b6846b` is a Symbian release-6 installer. Static parsing of its file records shows that installation runs an embedded application and also installs a recognizer; the application contains its own package and recognizer paths alongside Bluetooth and OBEX imports. It is bad based on that combined staging behavior. Both scanners match the new finding, and changing the Bluetooth import clears the control. The finding combines file-level facts; it does not prove a Bluetooth transfer occurred. The temporary extraction followed the [SIS file-format description](https://thoukydides.github.io/riscos-psifs/sis.html).

Full validation passed after the changes; no engine features were added.

`22831f14b45b` is a DOS wrapper that copies itself and builds a VBScript from hex-encoded DEBUG input. Static decoding shows Outlook address-book enumeration, attachment of the copied executable and message sending. It is bad. A new finding combines the wrapper's self-copy and DEBUG staging with encoded address enumeration, attachment and send operations. Both scanners match; changing the encoded attachment operation clears the new finding.

`93bdcf2a7921` jumps into a noisy word-addition decoder. Static decoding reveals host-entry restoration, an execution hook and file opening, seeking and writing. It is bad as hostile obfuscation and executable infection. Both scanners match the decoder finding; changing its memory-add operation clears the new finding. The original decoder finding establishes the obfuscation, while the infection behavior was confirmed from the decoded stage.

`f371ef7f0536` copies a stage while XOR-decoding it. Static decoding reveals an INT 21h execution hook, resident installation and file open, seek and write operations. It is bad as hostile obfuscation and executable infection. Both scanners match a new finding combining the copy decoder, resident probe and host-return trampoline; changing the XOR key clears the finding.

`edd18673bdc3` is a 4 KiB standalone Word table stream with a macro project name and formatting metadata, but no document container or executable macro body. It is inert in its own right and is good; the project name alone does not establish behavior.

The following are inconclusive after static inspection, with the specific limits noted. Hopper records these using its purgatory compatibility target:

- `21b5214739bd` is a DOS boot-security program with password prompts and disk operations. The inspected code and strings do not establish whether its modifications are malicious or are the advertised boot protection.
- `953e19e88ff4` is a Symbian installer that runs an application and installs a recognizer referring to it. Its E32 application uses a compression format that the available extraction attempts did not recover, leaving its behavior unresolved.
- `5f149d8e1390`, `b5cda3de3a5f` and `65fc45f965db` are Symbian/Psion binaries or resources. Paths and strings identify app data and, in one case, mail resources, but the code or resource semantics needed to determine their effects were not recovered.
- `db08d14d8999` contains two EPOC images, Bluetooth/OBEX imports, recognizer paths and media-looking filenames. Those facts merit investigation but do not by themselves establish whether it sends disguised executable copies or how its recognizer is installed.
- `dd8849eebd64` is a PowerPC PEF executable; `e6907c8c71f7`, `9e35527939d3` and `91847a6e3c33` are classic Mac resource forks. Resource maps and strings were inspected, but their executable resources were not sufficiently decoded to establish behavior.
- `144da99b060c` is compiled or packed OBASIC content whose program logic was not recovered. `dab69083e650` is a compressed Windows Help document whose embedded help macros could not be extracted with the available tools.
