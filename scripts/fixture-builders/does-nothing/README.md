# No-op fixture builders

These 17 small Python programs are editable sources for 33 retained format
controls under `testdata/<severity>/does-nothing/artifacts/`. They construct
minimal containers whose contents and boundaries are visible in source.
`make validate` scans the checked-in outputs; rebuilding them is a maintenance
action, not part of validation's hot path.

The builders use Python's standard library and accept an explicit destination.
Generate outside `testdata/`, inspect the result, then publish it with
`scripts/add-fixture`. Archive timestamps can differ between rebuilds; compare
member names and decoded member contents rather than archive hashes.

```bash
python3 scripts/fixture-builders/does-nothing/make_png.py /tmp/sample.png
scripts/add-fixture /tmp/sample.png testdata/baseline/does-nothing/artifacts/new-control.png
make validate
```

| Builder | Arguments | Retained outputs |
| --- | --- | --- |
| `make_png.py`, `make_jpg.py` | `DEST` | `sample.png`, `sample.jpg` |
| `make_docx.py`, `make_xlsx.py`, `make_pptx.py` | `DEST` | Corresponding Office containers |
| `make_odf.py` | `odt\|ods\|odp DEST` | Corresponding OpenDocument containers |
| `make_pdf.py`, `make_pickle.py`, `make_lnk.py` | `DEST` | `sample.pdf`, `sample.pkl`, targetless `sample.lnk` |
| `make_font.py` | `DEST.ttf` or `DEST.woff2` | Inert font structure controls |
| `make_asar.py`, `make_crate.py`, `make_deb.py`, `make_gem.py`, `make_crx.py` | `DEST` | Corresponding package containers |
| `make_tar_pkg.py` | `alpine\|freebsd DEST` | `sample-alpine.apk`, `sample.pkg` |
| `make_zip_bundle.py` | `KIND DEST [PAYLOAD]` | `jar`, `war`, `ear`, `xpi`, `epub`, `nupkg`, `vsix`, `whl`, `egg`, `conda`, `aar`, `apk`, `ipa` |

The ZIP builder's AAR input is the retained `sample.class`. APK and IPA inputs
are XZ-compressed platform executables; the existing APK and IPA contain those
same no-op executables as `lib/x86/libsample.so` and
`Payload/Sample.app/Sample`. Extract and XZ-compress those bytes when rebuilding
without a cross compiler. Never execute an archive member to regenerate it.
The tar builder also supports `arch`; XZ/Zstandard or other outer packaging is
separate from its tar construction.

Retain a builder only while an output it can construct remains a fixture.
During the October 2026 migration, all 17 builders ran successfully and 33
outputs matched their retained counterparts after ignoring container timestamps.
