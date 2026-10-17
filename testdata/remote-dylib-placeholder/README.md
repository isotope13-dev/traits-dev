# Documentation-domain dylib URLs are fixtures, not payloads

`source-remote-dylib-url` (suspicious) fired on the risset package-manager
test suite shipped inside the libcsound sdist: its manifest-parsing test
references `https://example.com/old.dylib`. RFC 2606 placeholder hosts
(`example.com`/`.org`/`.net`) are non-routable, so no staged payload lives
there; the trait now excludes them with a `not:` clause.

Run `python3 testdata/remote-dylib-placeholder/check.py
<scratch-directory>`:

- `fixture-placeholder-negative.py`: `example.com` `.so`/`.dylib` manifest
  entries. Must report nothing.
- `fixture-remote-positive.py`: dylib URL on a real remote host. Must
  still report the suspicious trait.
