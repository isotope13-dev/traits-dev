# BMP mislabeled-good review, 2026-11-04

Twenty-nine ordinary bitmap files have consistent declared lengths and no
suspicious or hostile findings in their fresh local slow scans. Endpoint
ruling: good. Validation passed, and Hopper confirmed the labels (no-ops).

`29b225ac2cb3` is a bitmap followed by an x86 XOR decoder and encrypted
payload. Static decoding recovers shellcode that enumerates files and drives,
names backup and security services, contains shadow-copy deletion and
storage-resizing commands, and embeds a ProLock ransom note. Its endpoint
ruling is bad for the embedded
ransomware functionality. Two new hostile findings on the original carrier
report the decoder and the XOR-encoded deletion command in separate taxonomy
directories. Removing the decoder or both copies of the encoded command
respectively prevents the corresponding finding. Validation passed, Hopper
moved it to bad, and its hash-verified snapshot was placed in
`/tmp/triage/misplaced-bad`.

`4dc2a8dbaa89` is a valid bitmap whose pixel channel reconstructs an entire
.NET DLL. The recovered DLL uses an encoded resource and reflection, but the
encrypted inner resource has not been decoded and its ultimate behavior is
unknown. The original image reports the pixel-channel PE observation. Endpoint
ruling: inconclusive, pending the inner payload's behavior.

`5e26b56703ee` begins with bitmap-like bytes and contains an `INICIO`/`FIM`
frame; reversing and Base64-decoding the frame recovers a packed Windows PE.
The recovered program has no conclusive malicious findings and its unpacked
behavior is unknown. A new suspicious observation reports the framed reversed
PE and rejects a control with the opening marker removed. Endpoint ruling:
inconclusive, pending analysis of the packed program. Hopper moved both
inconclusive samples and hash-verified snapshots were placed in
`/tmp/triage/misplaced-inconclusive`.

`2360f9a86889` is a PocketSphinx binary model definition. Its `BMDF` magic
resembles a bitmap header, but its embedded format description and model data
identify it as a speech model. The explicit file scan reports an unknown type
and no suspicious or hostile findings; this scanner cannot attach a format
trait to unknown file types. Endpoint ruling: good; validation passed and
Hopper confirmed the label (no-op).

`33b6bc3fc345` is CanisPack launcher source, and `bc41ea522ca4` is NZBGet
source. Both fresh local scans have no suspicious or hostile findings after
review. The latter's functional test starts a server and, when the optional
`--hold` flag is set, sleeps before cleanup. A long-sleep/process proximity
observation was relocated from anti-analysis to a neutral capability, since
the original rule did not establish execution order or intent. The source
matches the new observation and a control without the long sleep does not.
Their endpoint rulings are good; validation passed and Hopper confirmed both
labels (no-ops).

`0b583c309444` contains Jagged Alliance 2 Stracciatella game source and
bundled runtime libraries; `2485aa8a965a` contains VSCodium build source.
Their local slow scans report no suspicious or hostile findings. Endpoint
rulings: good; validation passed and Hopper confirmed both labels (no-ops).

`9307e1ffad00` is Telegram iOS source and `3671165bd52f` is LAMMPS source.
Their scans covered 15,175 and 5,300 reported components respectively and
contained no suspicious or hostile traits. Endpoint rulings: good;
validation passed and Hopper confirmed both labels.

`b49c16fb565b` is a MariaDB source RPM. An integration test clears its own
ColumnStore logs while resetting test services; this was previously reported
as system-log evidence removal. The general log-path truncation is now a
neutral observation, while direct system authentication or audit log
truncation remains suspicious and is retained by a positive control. Its
password-administration script copies `/etc/shadow` before updating root's
password hash, so the shadow-copy observation remains as the archive's one
justified suspicious finding. The full rescan covered 38,803 components and
reported no hostile traits. Endpoint ruling: good; validation passed and
Hopper confirmed the label.
