# Gopkg manifest and DOS companion review

## Verdicts

* `3886ff578b67c3fca2528ec8836c4e05bdad04264b435e442ad652c2e4141893`:
  **BENIGN**, an 802-byte Go dep dependency manifest.
* `425fa61207275f076bd5e129d0e4622016564ff1f19d0e72be0d65874fc5a0d7`:
  **MALICIOUS**, a 67-byte DOS COM companion infector, collected as
  `Virus.DOS.Dikshev.Comp.67`. The collector's family name is not a detection.

## Manifest analysis

Every byte is ASCII TOML or a comment. Active declarations constrain
`github.com/golang/protobuf` to version `1.0.0` and `github.com/ttacon/builder`
to branch `master`. Pruning removes tests and unused packages from vendored
dependencies. There are no command hooks, code, alternate source overrides,
embedded payloads or encoded strings. The URLs and override examples in the
generated header are comments.

The referenced [dep documentation](https://golang.github.io/dep/docs/Gopkg.toml.html)
was fetched and checked. A version without an operator is a caret range;
`1.0.0` is not an exact revision pin. No lockfile accompanies this sample,
so its historical resolved dependency revisions cannot be recovered from it.

Fetched and inspected upstream source archives:

* [ttacon/builder master](https://github.com/ttacon/builder): the runtime is
  `insertablebuffer.go`. Construction wraps a byte slice; growth allocates and
  copies memory; insert operations shift bytes; ReadFrom and WriteTo use
  caller-supplied streams. Imports are bytes, errors, io and unicode/utf8.
  Test initialization creates alphabetic fixture bytes. No launch, network,
  credential access or hidden initialization path was found.
* [golang/protobuf v1.0.0](https://github.com/golang/protobuf/tree/v1.0.0):
  Marshal/Unmarshal perform wire-format serialization. Registration stores
  descriptors and types in maps; generated init functions register schemas.
  The generator reads a request from stdin and writes generated source in a
  response to stdout. Its gRPC plugin registers with the generator; it does
  not connect to a remote service.
* [golang/protobuf v1.5.4](https://github.com/golang/protobuf/tree/v1.5.4),
  the latest stable version returned in the Go module proxy's version list:
  serialization delegates to google.golang.org/protobuf. Gzipped descriptors
  are parsed and registered as schema data. The developer-only alias generator
  invokes `diff` to compare generated source and deletes its `.bak` output;
  this is explicit generator behavior, not a manifest hook or load-time launch.

The source's hostile label may have been inherited from a repository/archive
containing malicious Go code, or may be a collection error. This is an inference;
the isolated manifest provides neither its containing program's identity nor
evidence of hostile behavior. The new declaration trait is notable metadata,
with no suspicious or hostile findings warranted.

## DOS control-flow analysis

Rizin disassembly used x86 16-bit mode with COM origin 0100h. Offsets here
are file offsets, not memory addresses.

| Offset | Instruction/effect |
|---|---|
| 00h–0Bh | DX=013Ah selects `*.e*`; AH=4Eh, CX=0, INT 21h finds the first normal file. Carry set returns through the PSP's termination vector. |
| 0Ch–21h | SI=009Eh reads the default DTA filename. DI=0143h is scratch beyond the image. LODSB/STOSB copies the basename and dot; seeing a dot redirects SI to `com\0` at 013Fh. |
| 22h–2Bh | POP DX selects the new name. AH=5Bh, CX=0100h creates a new file; an existing COM causes a carry branch to the next search. The attribute value is an unsupported high bit, not a hidden/read-only setting. |
| 2Ch–35h | XCHG AX,BX selects the returned handle. AH=40h; DX=0043h; XCHG CX,DX makes CX=67 and DX=0100h. INT 21h writes the entire running image to the new COM file. |
| 36h–39h | AH=4Fh and a backward short jump reuse INT 21h for find-next, then repeat the filename rewrite and copy. |
| 3Ah–42h | Plain data: `*.e*\0com\0`. No decoder or encrypted payload. |

This replicates into same-basename COM files and causes DOS COMMAND.COM's
COM-before-EXE lookup to select the virus when a command is entered without
an extension. The EXE is not overwritten or subsequently executed. There is
no resident handler, explicit EXEC call, network behavior, crypto, timestamp
change or permission-change syscall. Handles remain open until termination,
so propagation can stop when the DOS handle limit is reached.

Independent Unicorn emulation hooked INT 21h into in-memory file stubs,
with no host filesystem operations. Three executions verified no-match exit,
two byte-identical 67-byte copies, and skipping an existing COM while still
copying to the next basename. The final RET reaches PSP INT 20h.

## Rule changes and controls

* Bind the DTA-copy loop's extension pointer to COM-NUL and require the full
  create-new interrupt. Preserve variable data locations and image lengths.
* Move self-image writing from file creation into file writing; bind its
  buffer to 0100h and constrain the count to an in-file span containing the code.
* Replace adjacent-mask/string co-occurrence with a find-first operation whose
  DX points to the mask. Move this observation to file search.
* Require creation, executable search and self-image writing for infection.
  Move the independent executable-name shadowing claim to masquerade.
* Restrict private-interrupt matching to straight-line register setup.
  The old arbitrary gap crossed INT 21h and decoded the bytes `EB CD 2A`
  (a jump displacement followed by mask data) as INT 2Ah.
* The write-handle directory was at its 100-rule limit. Its unrelated
  `nsfilemanager-create` atom was actually file creation. Move that atom to
  the existing file-create leaf, preserving its matcher and effective defaults;
  there are no exact-ID consumers. This corrects placement without increasing
  any directory budget or splitting a leaf.

Twelve focused controls passed: the original image, a relocated extension with
a changed image size, wrong extension pointer, wrong search pointer, excessive
write length, TXT instead of COM, a normal terminating COM, a true private INT,
INT 21h followed by branch/data bytes, active dep constraints under a different
filename, commented constraints, and an unrelated package table. The excessive
write-length control retains name shadowing but loses the self-copy claim.

`cleave test-rules` reports precision 4.9 for infection and 4.0 for shadowing.
Both exceed the hostile authoring floor independently of the verdict evidence.

## Engine limitation

Both original paths were scanned with atomscan and cleave facts, and rescanned
after edits. The original DOS sample is classified as `unknown` because its
collector-assigned extension is `.67`. The engine skips generic analysis for
that type, before YAML trait evaluation. Adding a filename detection would
neither fix that dispatch nor meet the taxonomy's evidence requirements.

A byte-identical scratch copy named `companion.com` is classified as `dos_com`.
It fires the infection and name-shadowing hostile traits across two objective
directories, plus accurate notable search/create/write observations. The false
private-interrupt trait no longer fires. The original `.67` remains undetected
by this engine dispatch; the MALICIOUS marker is based on disassembly and
emulation, not the scan. Resolving this remaining gap requires an engine-level
content-identification change, beyond YAML traits.
