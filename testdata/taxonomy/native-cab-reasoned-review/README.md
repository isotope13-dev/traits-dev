# Native executables and WinFsp cabinet review

The three supplied artifacts were inspected with `atomscan`, `cleave facts`,
Rizin disassembly, PE parsing, and MSI table/cabinet extraction. No specimen was
executed. Addresses below are virtual addresses at the original image base.

## Judgments and code evidence

**6324dc81194a… — BENIGN: WinFsp 2023, version 2.0.23075.**

The complete SHA-256 exactly matches the publisher's
[WinFsp 2023 release](https://github.com/winfsp/winfsp/releases/tag/v2.0).
`osslsigncode verify` reports matching MSI signature digests, Navimatics LLC as
the signer, a March 16, 2023 timestamp, and successful signature verification.
This is corroboration for the inspected bytes, not an identity-string allowlist.

The MSI Property and ServiceInstall tables identify the version, SDK and
architecture-specific WinFsp.Launcher service. CustomAction records dispatch
InstanceID, ServiceRunning and deferred InstallJunctions/RemoveFiles actions.
The native custom-action DLL checks argument/path lengths; its InstallSymlinks
implementation at 0x10001460 reaches CreateSymbolicLinkW or the junction helper
at 0x100017d0. RemoveFiles at 0x100016e0 removes the specified installation
links/files. Rollback actions reverse these operations. The cabinet contains
the filesystem drivers, native and managed libraries, SDK source/headers and
example filesystems. These effects agree with a filesystem platform installer.
The cabinet is benign when inspected outside the MSI as well.

**a14c291a61fc… — MALICIOUS: damaged StormAttack DLL-injector installer.**

The CRT entry at 0x402674 reaches the configuration dispatch at 0x401cb0.
Configuration value 3 at 0x404120 selects the Active Setup installation branch.
The routine at 0x401900 creates an Installed Components key, writes the copied
image path as REG_EXPAND_SZ StubPath (0x401a4b), reads its own image with CRT
I/O, changes the copied configuration and writes/relaunches it. Other branches
extract the DLL through 0x402460 and write it via 0x4023c0. At 0x401260, code
deletes and replaces LanmanServer's ServiceDLL with a System32 DLL path.

At 0x401150, the loader chooses Internet Explorer, Notepad or Calculator,
creates the process, allocates/writes its DLL path into that process, resolves
LoadLibraryA and passes the resolved address and remote buffer to
CreateRemoteThread (0x40123d). Cleanup at 0x401390 obtains its own short path,
constructs COMSPEC `/c del … > nul`, and starts/resumes the cleanup process.
StormAttack's paired server/welcome banners corroborate family identity.
The hijacking and covert installation/injection code tip the judgment; ordinary
DLL-loading capability or the collector's filename would not.

The resource section is entirely zero, some code bytes are damaged and the IAT
contains resolved-address remnants. A usable embedded DLL, successful startup,
working DDoS payload or ransomware execution cannot be established from this
artifact. The retained hostile rules appropriately describe installer/injector
code, not demonstrated execution or encryption of victim files.

**e14b9d4567c6… — MALICIOUS: damaged Office-disguised HTTP RAT.**

The HTTP initialization code at 0x4057f0 loads WinINet/URLMon and resolves its
request/read APIs. The request routine at 0x40558c constructs POST and sends
binary records; 0x4037cb receives the HTTP response, checks status 200, reads
the response and validates its three-word checksum. The dispatcher at 0x4039b6
uses the received field at +0x10 to select commands 1000–1019. Command 1018
passes the received text at +0x20 to 0x403466. That routine creates a pipe,
sets the child's stdout/stderr to its write handle and calls CreateProcessW;
the response path packages the captured output for the next HTTP request.
Other handlers enumerate/manipulate files and processes or request shutdown.

The record codec at 0x405942 compresses data then XOR-copies bytes with 0x42;
0x4059a6 applies the same XOR before decompression. XOR is reversible scrambling,
not evidence of a cryptographic cipher. API names and shell command text are
partly assembled with stack stores. At 0x40317d, the program obtains its own
filename, formats the stack-built `cmd /c ping 127.0.0.1 -n 1&del "%s"`, and
passes it to WinExec. Its version resource claims Microsoft Word/Office despite
the remote-tasking code. No legitimate deployment context was supplied; the
covert command channel, destructive control and disguise establish the verdict.
Damaged instruction regions and incomplete runtime configuration prevent a
claim that this exact file successfully contacted a particular server.

## Trait changes and coverage

Seven CAB objective composites were retired: extensionless-crowd,
tiny-extensionless, extensionless-dropper, dotnet-exe-dropper, exe-entry-stub,
minimal-load-dropper and stub-exe-dropper. Their required evidence is ordinary
archive shape, CLR attribution, import counts or dynamic-loader APIs. Several
also described a sole member without requiring one. None establishes unwanted
extraction/activation or attacker control. Existing archive, CLR, import-count
and export-lookup traits preserve the supported observations. No product-name
exception or dependent-only exclusion was introduced.

Five firing Office references moved from sideloading/masquerading to
`micro-behaviors/fs/path/library` (DLL names) and `metadata/binary/debug`
(PDB path/name text). They describe references, including overlay references,
without asserting loaded modules, CodeView ownership or embedded executables.
Explicit consumers now reference the new IDs. The old objective directory has
no whole-directory YAML consumers; its remaining explicit consumers retain
their original matcher evidence. The username API moved from hostname to
`os/user/lookup` with its effective scope and explicit consumers preserved.
Whole-hostname selectors intentionally no longer include username lookup;
source hostname consumers retain all hostname evidence.

The constant-byte XOR-copy loop moved from `data/decode/xor` to
`data/encoding/xor`: the same loop is used on both inbound and outbound data.
The matcher now excludes a zero key and includes the count-up copy variant
found in the same codec. There are no explicit or directory YAML consumers of
the removed decode ID. Both native samples retain at least two independently
supported hostile findings; WinFsp and the isolated cabinet have zero hostile
or suspicious findings after the edits.

`check.py` builds inert PE/CAB controls into a supplied output directory and
checks emitted findings. Controls cover reference-only files, name/import
distinctions, both XOR loops with three different nonzero keys, zero-key and
wrong-store/branch/section near misses, extensionless cabinets and ordinary
managed/import-lookup executable cabinets. Run it from this checkout with:

```sh
python3 testdata/taxonomy/native-cab-reasoned-review/check.py /absolute/scratch/controls
```
