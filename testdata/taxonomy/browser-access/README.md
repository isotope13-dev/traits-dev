These fixtures are scanned, never executed. The controls distinguish browser
locations and serialized fields from collection, and exercise App-Bound and
DevTools consumer routing plus valid/invalid defanged IPv4 notation.

`schema-only.exe` contains three JSON field fragments. Its source is retained
in `src/schema-only.c`; the original rules apply to PE files, so a C source
fixture would not exercise them. Rebuild with:

```sh
clang --target=x86_64-pc-windows-msvc -fuse-ld=lld -nostdlib \
  -Wl,/entry:main -Wl,/subsystem:console -Wl,/nodefaultlib \
  testdata/taxonomy/browser-access/src/schema-only.c \
  -o testdata/taxonomy/browser-access/schema-only.exe
```

Run `python3 scripts/check-browser-access-routing.py` to check all controls.
