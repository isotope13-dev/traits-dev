# Native payload staging review

The legacy native-payload directory was reduced from 85 to 73 direct rules:

- ELF overlay/syscall/RC4 and embedded-header/entropy combinations moved to
  overlay and embedded-binary profiles. Entropy, an ELF header or RC4 code
  alone does not establish that an overlay is encrypted or executed. The
  dependent generic service-name rule also became an embedded-binary profile;
  its path and name references do not establish a trojanized service.
- The MIPS opaque-data, write and `execve` combination moved to the new
  `execution/payload/file-exec/replace` sink: `execve` replaces the current
  process image. The NativeAOT RunPE type/embedded-data pattern and the
  compressed relocation-entry hollowing pattern moved to process injection.
- JNI/shell/ELF-header and 7-Zip GUI/embedded-PE combinations moved to
  embedded-binary profiles. Batch EXE/DLL URLs with curl, temp and background
  command clues moved to staging acquisition.
- The writable-entry compressed-stage wrapper was redundant: its sole parent
  already requires the same writable-entry trait, with the same file types,
  platform, severity and confidence. No YAML references to the wrapper existed.

Eleven moved rules retain their matching conditions, explicit scopes,
confidence and exclusions. Names, severity and unsupported attack
annotations were corrected where the former labels overstated the evidence.
The existing process-inject directory has one positive directory-level consumer;
the moved injection rules now also satisfy that consumer.

The embedded ELF64 header trait's 1,000,000-byte maximum was removed. It was
an arbitrary whole-file limit on a fixed-length header signature and affected the
only two consumers. A synthetic ELF with an appended matching header was
recognized both below and above the former limit; that test covers the header
trait, not the full composites. Other legacy native-payload rules remain.
