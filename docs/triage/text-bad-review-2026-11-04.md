# Text filetype mislabeled-bad review — 2026-11-04

The 40-file snapshot contains 37 good, 2 bad and 1 inconclusive artifact, including archives.

The following 18 standalone artifacts are good; both scanners reported no hostile findings, and cleave reported no suspicious findings. Their parent project labels do not change the content of these supporting files:

- `0672f5f53afc`, `372a87bf6fb1` and `2a04189fc727` are inert parser or serialization test data.
- `1de4a867b436` is an export definition; `be9c476cebc8` is a resource-layout fragment; `4333b3e3100d` is test-runner configuration; and `a92e0349d7dd` is an error log.
- `96e42aa71c9d`, `a59b58cb7875`, `9a3b7cffd2cb` and `bb1881990585` are stylesheets; `b8054a1bd2d9` is a website-mirroring readme.
- `34180abed081`, `237e0b4b08a4`, `15f72541d1a0`, `76ab82fe34e6` and `144cde79fad8` are license texts.
- `6f87cfffbcf2` is a standalone list of common SNMP community strings. It contains no attack implementation.

The following 19 are good standalone artifacts. Both scanners found no hostile traits, and cleave found no suspicious traits:

- `912e985f25d8` and `0bea1dad34e0` are database schema migrations; `980063341bde` is a SQLite export-symbol list.
- `26254574e469`, `8732a4a2c5b6`, `eec54c0b009e`, `8f71eea78edb`, `b4ab4e65ec55`, `791f46b5c4fb`, `ba7821f705dc`, `049201f884fd`, `20c8dce89189`, `a1b4b997ac3a` and `8af0489791a5` are CSS or LESS stylesheets. The one CSS import points to a local stylesheet.
- `608a12b80fc7`, `585caa9dff6b` and `7b566194ad95` are documentation; `6cbca35a999b` is a font license; and `4d701c15112a` is an adjective list.

`779f015d33bf` is an HTML template with repeated keyword placeholders and a scraped-content placeholder. Both scanners report suspicious doorway-template findings. Its rendering system and actual use are absent, so it is inconclusive; Hopper records this through purgatory.

`59237eb64414` is an encrypted ZIP containing an npm package whose JavaScript collects host details and `/etc/passwd` and `/etc/shadow` contents, then posts them to an external Oastify endpoint. It is bad as an executable host-findings exfiltration PoC. `05b638d65351` is a source RPM containing a PCP regression test that plants a symlink and invokes the privileged target against it; it is bad as an executable symlink-exploit PoC. Both scanners already report hostile findings for each archive. The tests and sample provenance do not neutralize the implemented attack behavior.
