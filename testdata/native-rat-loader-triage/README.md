# Native RAT and staged-DLL triage

All three submitted files were analyzed with `atomscan`, `cleave facts`, rizin,
PE structure inspection and offline Unicorn emulation. No sample was launched
as an operating-system process and no outbound connection was made.

- **91fc174fa776**: x86 HTTP RAT with Microsoft Word VERSIONINFO claims.
  The binary validates a checksummed command header, dispatches commands
  1000–1019, connects command execution to anonymous pipes, and constructs a
  delayed `cmd /c ping ... & del` command targeting its own image. These are
  the two retained hostile behaviors. Drive enumeration and Office claims
  do not establish Elex or WannaCry; no ransomware behavior was found.
- **27b7d8489dc5**: damaged UPX wrapper containing a Gh0st-derived RAT profile
  and x86/x64 Hidden-derived drivers at file offsets `0x38f10` and `0x48558`.
  The original compressed stream cannot be unpacked successfully. The drivers
  register filesystem minifilters and implement removal of hidden entries
  from directory-query results. Their shared Hid_State/Hid_StealthMode
  configuration does not establish CoolClient. The RAT's SAM path format,
  GetMP credential command and HTTP-like response now require mapped sections.
  Whole-file signatures previously attributed a driver to Gh0st using bytes
  in its overlay; those duplicate signatures are replaced by this profile.
- **a9829fde5d7d**: native x64 obfuscated DLL stager claiming `claque.exe`.
  At `0x140008251` and `0x14000826b`, separate custom-decoder calls recover
  the DLL headers and section data. At `0x14000b89d` and `0x140008fc7`, code
  restores erased MZ/PE signatures, then reconstructs a memory image and
  resolves its imports. The recovered `build.dll` exports DllMain and spawns
  a worker. Offline emulation of that worker exposes host/hardware/locale
  queries, hashing, compression and an XOR-masked host-inventory POST to `/`,
  with fallback hosts uefarafara.mom, uefarafara.forum and uefarafara.rest.
  This supports a malicious staged loader/host profiler; browser credential
  theft and the supplied cosmical2049.com attribution were not established.
  The outer file retains two suspicious concealment traits rather than
  unsupported hostile CLR/resource claims. Its CLR strings and debugger API
  references occur in runtime code; the large resource is an icon, not a DLL.

## Focused controls

`verify.py` constructs inert PE controls and scans them without executing them:

```
python3 testdata/native-rat-loader-triage/verify.py /path/to/scratch/controls
```

Ordinary runtime names, incomplete hide logs, shared driver configuration,
DJB2-like ciphertext substrings, signature bytes in data, and incomplete or
unmapped-overlay Gh0st markers must produce no hostile findings. The complete
Gh0st marker cluster in a mapped section must retain its family finding.

The existing HTTP RAT and self-delete composites score 9.9 precision. The
revised Hidden concealment composite scores 9.6 and the section-scoped Gh0st
profile scores 7.4, exceeding the required 3.5 authoring floor.
