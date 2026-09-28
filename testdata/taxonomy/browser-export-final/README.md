# Browser export and capability boundaries

These synthetic controls are scanned, never executed. Run:

```sh
python3 scripts/check-browser-export-routing.py
```

The runner uses temporary copies outside the fixture tree so path-based fixture
suppression does not hide results. Twelve files cover three browser exports and
their local-only counterparts, TLS without cookies, cookie-reader/cookie-jar
modules, a custom archive diagnostic, and two formerly hostile false positives.
The module and archive marker fixtures use multiline text because the retained
`text exact` matchers require a complete trimmed source line. They do not test
arbitrary string-literal matching or broaden the original Python/bytecode scope.

The runner checks 31 rule findings and two full-scan assertions that the Notes
client and store/wallet names emit no browser-export verdict. The original
hostile wrappers matched both controls before retirement; useful primitives
still match afterward. The ObjC controls include actual Objective-C declarations
so content-based file-type detection chooses the intended scope.

`adhoc-notes-client.macho` is an inert arm64 Mach-O used to exercise the original
binary-only signature/libcurl rule. Its source is retained in `src/`. Rebuild it
without running it:

```sh
clang -target arm64-apple-macos11 -c src/adhoc-notes-client.c -o /tmp/adhoc-notes-client.o
ld64.lld -arch arm64 -platform_version macos 11.0 11.0 -e _main \
  -undefined dynamic_lookup -adhoc_codesign /tmp/adhoc-notes-client.o \
  -o adhoc-notes-client.macho
```

The custom archive diagnostic's meaning is documented by
[PyInstaller's archive reader](https://github.com/pyinstaller/pyinstaller/blob/develop/bootloader/src/pyi_archive.c).
It reads an `ARCHIVE_COOKIE` structure; it is unrelated to HTTP session storage.
