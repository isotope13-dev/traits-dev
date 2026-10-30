# Parked pixel-payload fixtures

These 33 PNG carriers embed scripts, archives, JSON, URLs, and one ELF image in
their pixel planes (LSB and higher-bit masks, several channel orders and bit
orders, 8- and 16-bit lanes). Detecting them requires reconstructing candidate
pixel layouts from decoded pixels — an engine capability that no released
`cleave` build has yet.

They were generated with `scripts/fixture-builders/make-png-stego-controls.py`
(`stegano-sequential.png` and `stegano-prime.png` are real `stegano-lsb` 3.0.0
CLI carriers, independently confirmed with zsteg) and committed together with
the native pixel detector that recognizes them:

- `filefacts-png-native.patch` — bounded pixel-layout reconstruction in
  filefacts, emitting `png.pixel_payloads` values.
- `cleave-layer-registry.patch` — registers the new encoded-layer names.

Both patches are preserved in `../improve/native/`, along with the 37/37
regression run (`native-pixel-regressions.json`), corpus results
(`native-final-corpus.jsonl`), and the audit trail. Until an engine carrying
that work ships, the pixel-payload traits below load but cannot fire, so these
fixtures cannot grade `suspicious`/`hostile` and are parked here instead of
under `testdata/`:

- `metadata/image/pixel/payloads.yaml` (`png.pixel_payloads` value rules)
- `objectives/anti-static/obfuscation/steganography/image/pixel-payloads.yaml`
  (`png-pixel-*` atoms and the `png-pixel-executable` composite)

The four clean controls remain in
`testdata/baseline/generated/taxonomy/png-pixel-stego/` and must stay
`baseline` once reconstruction ships.

## Restoring

When a `cleave` build with pixel reconstruction is deployed, move every file
here back to its originating directory — everything except `elf-image.png.xz`
belongs under `testdata/suspicious/generated/taxonomy/png-pixel-stego/`;
`elf-image.png.xz` belongs under `testdata/hostile/generated/taxonomy/png-pixel-stego/`
— and run `make validate`. `scripts/review/test-png-pixel-stego.py` regenerates
the synthetic subset from source if a fixture is missing.
