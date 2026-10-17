Packed multipart file exfiltration with a per-build marker
============================================================

`packed-multipart-file-exfil-with-build-marker` convicts a PE that performs
a libcurl multipart upload of a file[] field while carrying a per-build
UNIQUE mutation slot in packed UPX data, corroborated by a hardcoded
cleartext endpoint or a UPX overlay executable. Legitimate uploaders lack
the packed build-marker pairing, so the endpoint only corroborates in
`any:` while the upload machinery plus the marker gate in `all:`.

Run `python3 testdata/packed-multipart-build-marker-exfil/verify.py
<scratch-directory>`. The positive must report the hostile; dropping the
marker, the file[] field, or every corroborating endpoint must not.
