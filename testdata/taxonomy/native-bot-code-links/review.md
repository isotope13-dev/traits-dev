# Native bot code-link review

Reviewed SHA-256 prefixes: `2a12baea80ed`, `0bc6c9f8f46e`,
`78889cf81d4d`. All three are MALICIOUS based on code, independently of ML
scores, collection filenames, sandbox scores, or family signatures.

## StormAttack loaders: 2a12baea80ed and 78889cf81d4d

Both retain the same loader implementation and select installation mode 3.
The entry point reaches `0x401cb0`; mode 3 calls `0x401900` and the shell
cleanup at `0x401390`. The first routine creates a GUID-named Active Setup
component under HKLM, writes StubPath (`0x401a26` / `0x401a4b`), reads its
own image, patches the copied buffer, writes it, and launches the copy.
Cleanup obtains the current module path and COMSPEC and constructs `/c del`.

Other retained branches extract resource 101, replace LanmanServer's
ServiceDLL (`0x401260`), and allocate/write a DLL path in a child process,
resolve LoadLibraryA, and pass it to CreateRemoteThread (`0x401150`).
These are code capabilities, not proof that each branch runs in this build.

`2a12baea80ed` contains a 39,936-byte DLL resource (SHA-256
`0df2765cead245e3a89f9fafbbe5eb42ec7d41386a6c6dc235827539171335fd`).
Its Storm banners and command-report format corroborate the loader identity.
`78889cf81d4d` has an empty resource tree despite a large resource section.
Both have altered layouts and retained file-offset patch constants, so
successful installation/payload execution is not established by this review.
Existing traits correctly describe the retained malicious code; no changes
were needed for these two targets.

## Avzhan worm/bot: 0bc6c9f8f46e

The PE entry is `0x4093bf`, reaching startup `0x408640`. It has no executable
section flags, but retains the program in writable `.data`, and DEP is not
requested. Static decoding was performed without executing the sample.

* `0x407aa6` receives socket tasks and dispatches the received buffer.
  Branches download/run programs and invoke `system("shutdown -r -t 0 -f")`
  at `0x407f02`. The remote task path, not the shutdown string alone,
  establishes hostile control.
* `0x406bed` resolves WNetAddConnection2A, tries IPC$ credentials, copies its
  own image through administrative shares, builds a remote AT command from
  the successful destination, and invokes WinExec (`0x406eaf`).
* `0x407190` stages the image in a recycle-bin-shaped directory;
  `0x4070fc` writes executable AutoRun open/explore directives. A drive
  traversal worker invokes these routines.
* `0x408572` enumerates PROCESSENTRY32 records, compares the caller's name
  against the image name, and passes the selected PID to OpenProcess and
  its handle to TerminateProcess. Startup and its loop both pass KSafeTray,
  KSWebShield and kislive names to this helper. Rising and Qihoo names also
  occur in checks: their mere presence did not establish termination.
* `0x404ab0` XORs a fixed buffer in place with byte 1. `0x404ad0` invokes
  that decoder and writes the same buffer. The decoded PE is a Windows
  screensaver, not evidence of an encrypted malicious payload by itself.

The original `native-worm-av-process-kill` required only administrative-share,
AutoRun and AV-name text. Retired that unsupported claim. The replacement
requires a name-to-helper call link, name-comparison/termination code and
correct OpenProcess/TerminateProcess IAT slots. Its hostile composite also
requires the socket-task dispatcher and the forced-reboot call code.

## Placement and consumer audit

* Administrative-share and IPC$ templates moved unchanged to
  `micro-behaviors/fs/path/reference`; the sole exact consumer was updated.
  No ancestor directory selectors consume the moved worm atoms.
* Unused Rising/Qihoo name atoms were consolidated into existing neutral
  product references. Rising now includes ravmond as well as ravmon; these
  two existing product atoms retain DLL scope from the retired atoms.
* XOR-masked DOS/PE header presence moved unchanged to
  `metadata/binary/layout/embedded`; it does not establish a decoding action.
  All three exact consumers were updated. The sole ancestor selector is
  `compression-lib-embedded-binary`, scoped to ELF; the moved PE/DLL-only
  matcher cannot affect that consumer.
* The shutdown command text trait was renamed to reflect its binary as well
  as source scope, with both exact consumers updated.

## Focused controls

Actual Cleave/YARA evaluation of the new rules on the reviewed PE and byte
mutations, without executing any specimens:

| Control | AV helper | XOR decoder |
|---|---:|---:|
| Unmodified bytes under a different filename | yes | yes |
| Redirect one of the two security calls | yes | yes |
| Redirect both security calls to another helper | no | yes |
| Replace one of the two security-name arguments | yes | yes |
| Replace both security-name arguments | no | yes |
| Point termination call at OpenProcess's IAT slot | no | yes |
| Remove process-name comparison | no | yes |
| Change XOR read-buffer address | yes | no |
| Change XOR write-buffer address | yes | no |
| Change XOR key | yes | no |
| Remove the encoded PE header | yes | no |

The remaining real call must continue matching when only its twin is changed.
The encoded-header relocation retains its matcher; passive header presence
remains notable even when a decoder link is broken.
