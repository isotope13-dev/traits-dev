# Codec direction controls

The C fixtures are inert matcher controls. Rebuild the ELF fixture with the
command and verify its source/output hashes in `fixture-build.json`:

```sh
cc -Os -s -Wl,--build-id=none -o testdata/taxonomy/codec-directions/zstd-decoder.elf testdata/taxonomy/codec-directions/zstd-decoder.c
```

`cases.json` checks LZMA decoder versus encoder evidence and the binary-only
scope of the Go Zstandard decoder rule.
