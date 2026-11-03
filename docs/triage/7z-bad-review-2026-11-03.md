# 7z snapshot review — 2026-11-03

Review covers all 40 snapshot archives: 36 bad and four good. The decisions below were recorded in Hopper after current scanner checks and uncached validation. All 40 archives listed successfully and 64 members were extracted for static analysis with the standard `infected` password. Both current scanners were run on each archive and on individual extracted members; the complete local manifests and reports are under `/var/tmp/triage-7z-*`. Archive filenames and member names are leads, not proof of behavior.

The previous `encrypted-labeled-virus-archive` family of findings made a hostile claim from encryption and a malware-like member name alone. Its descriptions and criticalities were corrected, and a regression test checks harmless encrypted content with both an unknown and a known password. Full uncached validation passed afterward.

Individual members of `14c4e2527085` and `88336e8ad650` implement source propagation and Word/Outlook macro propagation, respectively. Several DOS members have behavior-based infection or raw-disk-write detections, and disassembly confirms matching INT 21h or INT 13h operations in sampled members. Each archive was reviewed in the entries below.

`72190f0add02` contains code that reads and writes raw sectors, including code consistent with a boot-sector infection. The former generic raw disk and boot-sector wiper rules inferred wiping from sector operations and exit alone; those observations now live under `micro-behaviors/os/msdos/disk` with neutral descriptions and criticalities. A signature-specific Copier detection remains. Regression tests cover generic sector writes, copies, and boot-sector writes. Disassembly and both current scanners now confirm the boot-infection behavior. Other initially unrecognized members were examined directly; `97ccd70fedea` retains the decoding limitation described below.

- `14c4e25270851349391637f2f7d6eadaeb7a575249d84d7fa1c5cfc4f70c1412` — **bad** — 1C report code extracts its own source, finds unmarked reports, and inserts the source into them.

- `88336e8ad650a509f23a720344d1f996e0eb69af92bef0d5c96bb7cdc53645c2` — **bad** — Word macro copies itself between document and template, lowers macro security, and mails the active document through Outlook.

- `78c2341527f1c11f3cd5041eecff890e4e5536c94027515f16715fc63d2c6008` — **bad** — VBScript repeatedly displays a modal message box in an unconditional loop.

- `04dc51c01a1c3e8b25a2cdd31298424c09186ef4847eaab95695d172774d808c` — **bad** — DOS code searches executable files, writes altered content, and restores timestamps; disassembly corroborates the infection-oriented findings.

- `3bb6aadf7915f5738d17d5da71ece0e4906e5569cb58aafd84107cc1fd614ad3` — **bad** — DOS code installs an interrupt handler and alters file contents; disassembly corroborates the reported resident infection behavior.

- `51598fcada0aa7de8f3b243ee01945dc178f6dac3fb109ffc42587bef4af85d6` — **bad** — DOS code searches files, appends a body, patches the entry, and restores timestamps; disassembly corroborates the findings.

- `853f32759138e1994fbd0b24fa64c37bc7ffec38825991af6fde73c85da5a6b0` — **bad** — A ten-byte wrapper contains a valid PE DLL. Its process-hiding export maps physical memory and modifies linked process-list pointers; both scanners now recover the PE and report the combined evidence.

- `afd78605ae9666f57684514674135a274945c1f2bb0f87a80e8ca9916c8da4db` — **bad** — DOS program enumerates files, opens them for writing, appends its body and patches entries; disassembly confirms the infection operations.

- `b66d62f8a402bfb48df6d7631e5e322acefbc826fe78d87c61f7cfd7985af4b6` — **bad** — DOS program searches executables, opens and modifies them, and preserves timestamps; disassembly confirms the infection operations.

- `b96022c60596639ed2556bf8d77cdf7d7244f33fbb37cd27fba8e86182d2e719` — **bad** — DOS program searches executable files and writes infection-related changes; disassembly confirms file search, read and seek operations.

- `d938e45c456586d2a1f71d8409e92dcaabcfe25a26e6002cddf8034ad588d2b1` — **bad** — DOS program enumerates executables and modifies their contents while preserving timestamps; disassembly confirms the reported operations.

- `802d3bb97033b542e26ba7d1c9498ea47f04b0680efb20aae4cfa61b4702c3a2` — **bad** — Archive contains multiple DOS file infectors; disassembly shows file search, body writes and entry redirection.

- `2dc0459585032a3a1a480e137f4727f0958a31737ddb64a6e81ad9cc7db1e1a1` — **bad** — DOS code searches executables, reads and replaces a three-byte entry, then writes a program-sized body; the late-file sequence is now detected by both scanners.

The embedded-PE gap found in `853f32759138` was repaired in Cleave: validated PE/ELF content in bounded unknown binary carriers is analyzed as a child, including when the unknown carrier is an archive member. Unit tests exercise valid and malformed wrappers and the default archive path. The decoded DLL's physical-memory reference, process-hiding export, and related API evidence now produce a behavior-specific finding; PE fixture tests cover missing components. Both rebuilt scanners recovered the actual DLL and reported the finding.

- `40bcd5c97aaa0100ec4e1abb8043c1969a967a8c397f71dc772ace2ecbd9bd8a` — **bad** — Go agent binary contains compiled routine names for C2, reverse shell, shellcode injection and persistence; build metadata and the broader symbol set corroborate a dedicated post-exploitation agent.

- `178a47486e0ec9d5114953f985137afd17caae325601132987ec0155bbf1495e` — **bad** — DOS program searches executables, redirects their entry points and appends its code; disassembly confirms the reported infection operations.

## Obfuscated script follow-up

For `97ccd70fedea`, static reconstruction of the outer permutation, dictionary expansion, and nested literal permutations was performed without executing the script. The reconstructed source and literal table show an HTTP POST/response command loop, a branch that evaluates a received command, file-write-and-run branches, and persistence through a Run key and a scheduled task. The reconstructed artifacts are in `/var/tmp/triage-js-decoded-stage.js`, `/var/tmp/triage-js-decoded-layer2.js`, `/var/tmp/triage-js-expanded.js`, and `/var/tmp/triage-js-table.json`; they may contain an endpoint and should be handled as sensitive sample data.

The initial archive scan flagged obfuscation but did not recover these behaviors. The literal-only permutation decoder initially recognized a different set of shuffle and dictionary constants.

Cleave now recognizes this alternate outer permutation and dictionary recipe, plus the nested literal-only shuffle. Both rebuilt scanners expose the same additional decoded JavaScript layer (`83d4c15d4654`) from the original archive. The implementation checks complete normalized decoder bodies, accepts only bounded literals, and does not execute JavaScript. The literal configuration table remains unresolved in that layer. A hostile variant finding now combines two fragments of the verified shuffled configuration with string-shuffle and variable-eval observations; its description identifies the configuration and obfuscation rather than asserting the hidden command behavior was automatically recovered. Both scanners report it on the original archive, and negative tests cover each fragment, shuffle, eval, and generic obfuscation. Static reconstruction demonstrates a dedicated command-and-control agent; the artifact is **bad**, and Hopper confirmed its existing label after uncached validation. Automatic resolution of the configuration table remains a coverage gap.

Further disassembly of `72190f0add02` shows a resident INT 13h handler, boot-sector checks, and writes through the saved disk interrupt. The existing `dos-int13-hook-writer` composite combines an interrupt-vector swap and a generic DOS file-write signature; it does not prove their execution order or, by itself, establish boot-sector infection. The generic combination was moved to neutral behavior evidence; a separate detection now requires zero-segment vector exchange, a boot-buffer patch, and sector-write code. Positive and negative tests and uncached validation pass.

- `72190f0add0275634b4d8eda77d1a89b879fdded5b43013a5ff68ab94bd842e7` — **bad** — Resident DOS boot infector hooks INT 13h, checks and patches boot buffers, and writes sectors through the saved disk handler.

## Commodore archive follow-up

`0436536a4239` contains two encrypted members. The common sample password
extracts a 518-byte Commodore 64 program and a 772-byte LyNX archive. The
LyNX member contains an exact copy of the program starting at offset 254.

The program's BASIC entry and four separate machine-code sequences at `$080b`,
`$081c`, `$08e4`, and `$0913` match the independently documented disassembly
of a 1541-drive-resident file infector. The loader sends drive memory-write
commands and starts the uploaded drive code; the corresponding drive routines
read and change disk-directory data. See the [annotated Commodore virus
analysis](https://codebase.c64.org/doku.php?id=base%3Aviruslist). This is a
malicious executable, not a conclusion based solely on the collector filename.
Initial local disassembly is saved at
`/var/tmp/triage-commodore-043-disasm.txt`.

File identification now recognizes a self-consistent C64 BASIC `SYS` entry
and routes it to generic binary analysis. The dedicated Commodore platform
prevents these observations from being labeled Unix or Windows. A hostile
finding requires the BASIC entry, serial upload loop, drive sector job,
directory-track setup, directory-entry redirection, and marker update; it
describes matching code, not observed execution. Both rebuilt scanners report
that finding for the original archive and its extracted program. Focused
positive and negative tests and uncached validation pass. Hopper confirmed the
existing **bad** label for
`0436536a42393f76abf84df793ac67effef5525e475aa63169f6cc37bef64272`.

- `e649374d3d0cc70e5d3120602498a54020c2232337c238ff415418e54da94b15` — **bad** — DOS code searches files, reads the original three-byte entry, writes a body, rewrites the entry, and restores the timestamp. Both scanners report the more specific append-and-entry-patch pattern, validation passes, and Hopper confirmed the existing bad label.

Review of this sample and `ccca72742a29` exposed three findings that labeled
unbound combinations of DOS search, file I/O, timestamp, and interrupt-vector
operations as hostile infection. Those combinations are now filed as
suspicious behavior evidence, and their descriptions state the observed call
sequences. New hostile findings
require ordered entry-patch or executable-header-write sequences together with
additional search/timestamp or EXEC-hook evidence. Focused tests check missing
components and generic call combinations.

- `ccca72742a293e9495a54e9fa2820ac671170c8bb13d38024401e440bdc6db66` — **bad** — This MZ-format DOS executable installs an INT 21h EXEC hook and includes a body write and executable-header rewrite. File identification now preserves structurally valid DOS MZ files for generic binary analysis instead of routing them to a PE-only parser; extended PE and NE signatures retain their existing types. Both scanners detect the specific EXEC-hook and rewrite pattern in normal archive scans, focused tests and uncached validation pass, and Hopper confirmed the existing bad label.

- `181daa8176ddb3f2588c09efa1a871ff61c45d2059ece9b331799e7403fdb0ab` — **bad** — The DOS program copies and replaces the INT 21h vector, intercepts EXEC, reads four bytes from a target, and uses shared seek/write routines to append code and replace the entry. Both scanners report the combined EXEC-hook, read/check, and shared-call pattern. Focused tests cover missing components and relocated operands; validation passes and Hopper confirmed the existing bad label.

- `225ffa6374f46eced295890b48b461836c65bc708bba80b114e8cbeca9b31da7` — **bad** — The DOS program redirects interrupt handlers, reads and rewrites the original three-byte entry, and writes a body using private interrupts. It also requests VSAFE/VWATCH removal and contains adjacent `SCAN` comparisons and delete-call setup. Both scanners report the entry-write code and two separate security-tool-related findings. Negative tests cover missing behavior, scanner-name bytes, delete setup, and removal request; validation passes and Hopper confirmed the existing bad label.

- `1ee1ac5c3f25a49eb47f8431aff3531f03d16c7e0f139d0aca3351c5a2596635` — **good** — The encrypted DOS program reconstructs a resident screen-effect program that hooks keyboard and timer vectors, draws a bouncing character, and supports keyboard controls. Static review found no boot-sector or file-infection operations. A bounded decoder now exposes the reconstructed layer without execution; its hash matches an independent reconstruction. Both scanners report the XOR loop, vector handling, resident behavior, and BIOS character-write bytes with no suspicious or hostile findings. Decoder unit and integration tests and uncached validation pass. Hopper moved the archive from bad to good.

- `820ce8beb6a53a31c4816ee831d8a2fd2d6c2ca0ccb86e9cd43d2ffd154d1923` — **bad** — The encrypted DOS program enumerates files, constructs a jump from saved entry bytes, writes a three-byte prefix, and writes a body. Static reconstruction of its forward word-XOR loop matches the scanners' recovered layer byte for byte. Both scanners report a finding requiring the ordered jump/prefix-write code, file-search, EOF-seek, and timestamp sequences; focused tests cover missing components, a loose-call negative, and an alternate DOS open spelling. Validation passes and Hopper confirmed the existing bad label.

During this review, a prior hostile finding combined an isolated E9-byte store
and a generic write-service observation, without connecting the stored byte to
the write. That loose combination now reports only suspicious behavior, and
the single E9 store is described as byte-level metadata. The more specific
finding above does not assert that separate operand pointers are proven equal.
The previously reviewed PingPong screen-effect simulator remains free of
suspicious or hostile findings in both scanner runs.

- `9549235769386a408965932b2235c8bee0b1ed9aef468fdc6d96d44e60f30937` — **bad** — The DOS program saves and replaces the INT 21h vector, reads and checks an executable header, writes its image, resets the DOS system file table cursor, rewrites the header, and restores the timestamp. Both scanners report the specific combined static-code pattern in normal archive scans. Focused tests cover missing components, changed header size, cursor reset, and relocated operands; full uncached validation passes. Hopper confirmed the existing bad label.

- `e228423ffb44b7d3222e587e1d08fab327f924ffb94484226d00bf380b3a7b77` — **bad** — The IBM VM/CMS REXX program displays a greeting, reads NAMES and NETLOG records, and issues EXEC send commands to the resulting contacts. A conservative CMS source recognizer makes this previously unidentified archive member available to normal scans. Both rebuilt scanners report the contact/log-based EXEC distribution pattern; the finding does not assert delivery, recipient execution, or that the sent filename is the currently running file. File-identification and pattern tests cover comments, binary data, missing components, different filenames, and line boundaries. Full uncached validation passes, and Hopper confirmed the existing bad label.

- `44ed806837666cb9b5730764b2796345028b558c28eb816ef078a1c03ccb3a1d` — **bad** — The dedicated ABAP virus proof of concept selects reports, reads its own and another report's source, and inserts source lines into an in-memory table. The `INSERT REPORT` statement that would write the modified program is commented out, so the artifact does not establish a repository write as supplied. SAP documents both [first-column comment syntax](https://help.sap.com/docs/abap-cloud/abap-keyword/comment-line) and [INSERT REPORT](https://help.sap.com/docs/SUPPORT_CONTENT/abap/3353523713.html). A conservative ABAP report recognizer makes the previously skipped member available in normal scans. Both scanners report the combination with a distinct commented-writer description; the individual source-text observations do not bind their operands to one another. Tests cover the active and commented forms, renamed tables, missing stages, and file identification; full uncached validation passes. Hopper confirmed the existing bad label.

- `7dc6ad83a8f158fc70f328f823138c7a53f0279341ed35f127a40207f2a105a3` — **good** — This Windows NE executable's ordinal imports cover window handling, timers, drawing, resources, and sound. Static inspection of its short code segment found DOS version and exit interrupts, no disk interrupt, and no file-write or network API imports. The analysis used [Wine's NE relocation reader](https://github.com/wine-mirror/wine/blob/master/tools/winedump/ne.c) and its [Win16 USER ordinal definitions](https://github.com/wine-mirror/wine/blob/master/dlls/user.exe16/user.exe16.spec), alongside KERNEL and GDI definitions; these static observations do not claim execution. The archive's `not-virus_BadJoke` member label was incorrectly categorized under virus identity. It is now a neutral archive-name observation, with a regression case that keeps genuine virus-label handling separate. Both scanners report no suspicious or hostile traits, full uncached validation passes, and Hopper moved the archive to good.

- `b6fdbc3b743e1ccd902747bcb5316db152c00928a95f424a766be9d42fcb8337` — **good** — This Windows NE program imports graphics, window, timer, memory, and runtime APIs. Unlike the previous sample it also imports KERNEL's general DOS-call interface; all five relocation sites were traced to version checking, getting and setting interrupt 0, process exit, and restoring interrupt 0. The code contains no disk interrupt, and its resolved imports contain no network or file-write API. The static mapping used [Wine's NE relocation implementation](https://github.com/wine-mirror/wine/blob/master/tools/winedump/ne.c) and [Win16 KERNEL ordinals](https://github.com/wine-mirror/wine/blob/master/dlls/krnl386.exe16/krnl386.exe16.spec). Both scanners report no suspicious or hostile traits after the BadJoke label correction; validation passes and Hopper moved it to good. No code was executed during review.

The scanners now extract NE import references from bounded relocation tables,
including named imports and Win16 ordinals. Common Windows ordinals are named;
unknown ordinals and ordinals from non-Windows NE targets remain numeric.
Both scanners recover 37 and 47 distinct imports respectively from these two
samples, matching an independent relocation-table check, and report neutral
timer and drawing observations plus a sound import in the first sample.
Neither gained suspicious or hostile findings. Unit tests cover unknown and
named imports, non-Windows targets, malformed tables, and the normal parsing
pipeline; full uncached validation passes. Import names do not establish that
the APIs ran, and the Win16 ordinal-name table is intentionally incomplete.

- `c69a71a1dd36e5d217f59d9c67f6d7a1098a9cff2690929b56cdb08fc4588e6c` — **bad** — The Win16 program copies its executable to a fixed path, writes that path (preceded by spaces) to the `windows` profile's `run` entry, overwrites clipboard text, repeatedly opens a text file, sends a misleading critical-error report to the printer, and requests Windows exit. These are static observations, not a claim that the code was executed or that the profile value succeeds on every Windows version. Win16 KERNEL, USER, and SHELL ordinal names were checked against Wine's [KERNEL](https://github.com/wine-mirror/wine/blob/master/dlls/krnl386.exe16/krnl386.exe16.spec), [USER](https://github.com/wine-mirror/wine/blob/master/dlls/user.exe16/user.exe16.spec), and [SHELL](https://github.com/wine-mirror/wine/blob/master/dlls/shell.dll16/shell.dll16.spec) specifications. Both scanners report the profile-run write and a hostile finding for the same call's executable path hidden behind 278 spaces. The rules bind the section, key and padded path arguments to the KERNEL relocation rather than combining unrelated strings with an import. Clipboard, launch, and Windows-exit imports remain separate observations; imports alone do not establish execution. Synthetic tests cover shifted segments, changed arguments, relocation offsets, ordinal and library changes, short padding, relative paths, and non-executable targets. Full uncached validation passes, and Hopper confirmed the existing bad label.

- `eb8dbc580ffc24110ce8d15694c9e3fcf91ddf42eb330a3fcbe6b740d1be09c3` — **bad** — The Z80 source scans TR-DOS directory entries for BASIC files, adjusts an entry's length, uses the saved restart return address to copy code into a disk buffer, and writes sectors. This is a static source review; it does not claim the program ran. The [contemporary TR-DOS programming guide](https://zxpress.ru/en/ezines/faultless/03/working-with-tr-dos-at-machine-code-level-entry-points-to-subroutines-sector-read-and-write) describes the disk-service entry point. Both scanners now report a hostile combination of BASIC-entry selection, length adjustment, saved-register copying, and sector read/write source patterns. The separate patterns do not prove operand identity, and the composite description avoids claiming it. Synthetic tests cover each missing observation, commented-out code, case changes, and CRLF input; the ZX Spectrum platform alias test and full uncached validation pass. Hopper confirmed the existing bad label.

- `45acd774877474217b3f42400b363c28fbba8774e71b478e7f2c22cd3abe991c` — **bad** — The unencrypted archive contains eight serialized Sign of Misery scripts, eight corresponding rendered command listings, and one informational text file. The listings describe enabling Task Manager, registry-editor, and shell restrictions, copying executables into Windows directories, referencing Run keys, and setting a recovery/payment notice. The serialized scripts contain matching policy-value records and notices. The listings are descriptions of the script commands; neither their presence nor a static scan establishes that a command ran. A narrow content recognizer now routes the previously skipped serialized scripts to generic binary analysis, including when renamed, without labeling every script malicious. Both scanners report the lockout/payment combination in all eight serialized scripts and all eight listings. Cleave also analyzed the informational text in the archive; Atomscan's archive output omitted it, so it was scanned separately and had no suspicious or hostile findings. Existing source-dump descriptions that only required policy-name mentions were corrected to describe mentions. Focused tests cover file identification, changed policy records, disabled values, missing notice terms, and missing listing components. The policy observations are distinct byte or source-text clues; their individual operands are not all bound across separate records. The Russian payment-notice clues are limited to their observed legacy encoding and wording. Full uncached validation passes, and Hopper confirmed the existing bad label.

- `7b41fd536533c7f37be62897581d15f91422c9feb2e75da670e31f511def2ca2` — **bad** — The archive pairs a DOS MZ executable with documentation for a virus-construction toolkit. The executable independently retains nearby fragments of the builder's banner and credits, a VCL-specific compiler option, and a logic-bomb symbol, as well as a HackStop protector marker. These correlated fragments support the builder identity without relying on the collector's filename; they do not establish execution or demonstrate every capability claimed by the manual. A bounded attempt to reconstruct the inner compression layer did not yield a trustworthy unpacked program; interrupts were blocked during emulation, and the recovered program was not run. [Deark's static PKLITE module](https://github.com/jsummers/deark/blob/master/modules/pklite.c) did not recognize the outer protection layer. Both scanners now report the builder identity and the neutral protector marker, while the documentation alone has no suspicious or hostile finding. Generic DOS interrupt-byte descriptions were corrected to describe the observed bytes rather than claim that calls occurred. The identity signature is based on partial compressed literals and may miss other compression variants. Synthetic tests cover missing fragments, unrelated protector markers, and invalid headers; full uncached validation passes. Hopper confirmed the existing bad label.

- `96292c372562b51850cd5d5b7c52b0aa2ebdb0b1f7486f9344e12f2257400150` — **bad** — This stripped 16-bit Unix a.out initially jumps from the program text into code in its initialized-data region. Static PDP-11 disassembly shows that code reading directory-sized records, opening candidate files for read/write, checking the `0407` executable magic, adjusting executable-header sizes, writing its own code at the end of a file, and rewriting the header. The Unix [seek system-call documentation](https://www.typewritten.org/Manual/Bell/UNIX/32V/man2/lseek.html) and the [PDP-11 disassembler](https://github.com/caldwell/pdp11dasm) informed the interpretation; the program was not executed. A bounded a.out recognizer now routes consistent relocation-stripped `0407` images to generic analysis without inferring an architecture from the shared header. Both scanners detect the graft: the rule binds the initial jump into initialized data to nearby PDP-11 header-adjustment, end-seek/write, and start-seek/write instruction patterns. It is a specific instruction-pattern detector, not a general PDP-11 disassembler or proof that a program ran. Identification and synthetic rule tests cover truncated headers, changed entry targets, non-data targets, and missing write stages; full uncached validation passes. Hopper confirmed the existing bad label.

- `a2a6d5acf30d0e5f41c47200316f1c062a521e39b7a50dd21ae6b09feaff3ced` — **bad** — A bounded static reconstruction of the DOS COM program's word-wise subtract, XOR, and rotate loop reveals code that redirects DOS services through INT 1, finds `.COM` files, overwrites them from the program image, and restores attributes and timestamps. The new decoder's output matches an independently reconstructed image byte for byte. A behavior rule binds the find path to the overwrite subroutine and interrupt-vector redirection. Both rebuilt scanners report that finding on the original archive and decoded child; focused decoder and rule negatives and uncached validation pass. Hopper confirmed the existing bad label.

- `c8e3975f373187fd17eb831674e253c9b060b6f204c629a69bb20b17f988b0c3` — **bad** — Several archive members repeatedly write one buffer to successive BIOS sectors on four distinct drives, and another repeatedly writes zeros to successive CMOS indices. The archive also includes a screen-effect-only helper; the hostile verdict rests on the actual disk and CMOS code. Both scanners detect the destructive loops in the original archive. Negative tests cover changed buffers, drive or sector relationships, loop branches, write calls and CMOS values, and uncached validation passes. Hopper confirmed the existing bad label.


- `3a6645737b22f980fd65efd6cd3eb284fd2af7d6dddec564e14a20b74d19957e` — **bad** — The 1,024-byte Apple II boot member matches every byte of an independently extracted [StarFighter II boot image](https://retrocomputing.stackexchange.com/questions/32316/extract-virus-bootsectors-from-spy-format-elite). Its altered boot code includes 65816 mode and vector manipulation. A signature requiring separate boot, native-mode and vector-hook spans identifies this exact known code without asserting execution. ProDOS boot structure now routes to generic analysis; both scanners detect the original archive, signature boundary tests and uncached validation pass, and Hopper confirmed bad.

- `572e692fd8126c81eabd803e670f340979655eca2cfe1ecdc40bd446d58cf715` — **good** — The member matches all 3,328 bytes of `Defanged.Virus` from the [Apple.Rx antivirus distribution](https://www.applefritter.com/content/how-do-i-run-program-i-cant-do-it); the accompanying documentation calls it a non-harmful demonstration. Static 6502 review finds ProDOS `$CA` file reads, not writes. A neutral rule binds its read buffer and recognizes its ProDOS context; both scanners report no suspicious or hostile findings, boundary tests and uncached validation pass, and Hopper moved it to good. The archive name alone was misleading.

- `dc90564b68e1df9f3b4eaff4d88cb9b49a3e44a1d698b0e2375c71eca3d9c54c` — **bad** — A bounded subtraction loop reconstructs a DOS program that enumerates executables, patches entry bytes, appends a body, and restores timestamps. Its next XOR stage has a zero key in this specimen. The reconstructed bytes match an independent static reconstruction; both scanners recover them from the original archive and report the file-infector finding. Decoder boundary tests and uncached validation pass, and Hopper confirmed bad.

- `ecb66ce42a3f1feba3c1c9c0704565d58a3739125edb2120b80bdb9b2b5b3beb` — **bad** — A bounded byte-XOR loop reconstructs a DOS program that patches COM/EXE entries, writes its body, and preserves timestamps. Its decoded bytes match an independent reconstruction, and both scanners detect the existing parasitic-infector rule on the original archive and decoded child. Decoder boundary tests and uncached validation pass, and Hopper confirmed bad.
