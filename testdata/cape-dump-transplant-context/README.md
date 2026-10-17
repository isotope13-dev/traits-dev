Transplanted-cert conclusions do not survive CAPE reconstruction
==================================================================

`cert-transplant-fake-upx-carrier` and `cert-transplant-file-walker-infector`
convict a dangling certificate directory paired with UPX section names or
with file-walker plus timestomp legs. A CAPE-reconstructed memory image
matches that shape innocently: the overlay certificate is never mapped into
memory so the cert directory dangles past the end of the dump, unpacked code
keeps UPX section names, and CAPE adds a synthetic `.CAPE` section. Both
composites exclude the CAPE-dump context (`cape-sandbox-dump-section`)
instead of convicting sandbox artifacts.

Run `python3 testdata/cape-dump-transplant-context/verify.py
<scratch-directory>`. The transplant-pattern positive must report both
hostiles; the same image with a `.CAPE` section must report neither.
