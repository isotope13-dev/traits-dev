# Property-list mislabeled-bad review — 2026-11-04

Reviewed all 40 snapshot entries with both scanners and resource inspection. Hopper confirmed 37 good and 3 inconclusive. Most entries are localized UI strings, application metadata, code-signature manifests, interface archives or .NET resources containing ordinary images and UI values. Some came from hostile projects, but those individual resource files do not themselves establish malicious behavior.

`8f16cbef1e44` contains a Parallels icon path and its SHA-1 and SHA-256 hashes. The former hostile AMOS rule inferred malware from that icon alone. It is now a notable code-signature metadata observation; both scanners agree. This does not assert that an application containing the icon is safe.

`c61c14fffdde` refers to external byte-array resources that were unavailable in the snapshot. `ea088c39c9fb` is opaque high-entropy data despite its resource filename. `b0b1ba136f20` contains a password-protected archive that could not be inspected with the locally available passwords. These remain inconclusive. Serialized resource entries examined in `0d1b38e87729` and `6a346f29f8b1` identify Windows Forms state and drawing-point types respectively.

Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks. No engine features were added.
