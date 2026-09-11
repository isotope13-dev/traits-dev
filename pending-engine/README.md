# Traits parked pending engine support

Everything under this directory loads cleanly as YAML but references engine
features that the installed cleave (2.10.0) does not provide, so `cleave
validate` rejects the whole trait tree while they are in place:

- **`metadata/font/`, `objectives/.../payload/font/`** — written against a
  `font` file type and `font.*` facts (`font.problems`, `font.tables`,
  `font.trailing_bytes`, `font.printable_ratio`, ...). This build has no such
  file type: it classifies `.ttf`/`.otf`/`.woff`/`.woff2` as `Unknown` and
  emits no `font.*` values.
- **`metadata/media/`, `objectives/.../payload/media/`** — `metadata/media` is
  not a registered `metadata/` subdirectory in this build, and the layout
  traits read `media.trailing_bytes`, `media.gap_bytes` and
  `media.stowaway_entropy`, none of which exist.
- **`objectives/impact/infect/binary/{note-cavity,graft}/`** — the ELF
  note-cavity and Mach-O segment-graft infection composites. Their legs read
  `elf.executable_segment_count`, `elf.entry_in_nonstandard_section`,
  `elf.uncovered_note_count`, `elf.build_id_uncovered`,
  `macho.executable_segment_count` and `macho.entry_in_nonstandard_section`.
  The engine computes `elf.wx_segment_count`, `elf.note_count`,
  `elf.has_build_id` and `elf.entry`, but not these.

Nothing here was capable of matching on this engine — a rule keyed on a file
type that is never assigned, or on a metric that is never computed, is inert —
so parking them changes no verdict. Restore them (and the trait ids excised
from `metadata/binary/anomaly/format/{elf,macho}.yaml`, from
`objectives/evasion/masquerade/extension-mismatch/{font,image}.yaml`, and from
`objectives/supply-chain/hidden-payload/font-asset/traits.yaml`) once cleave
ships the font/media analyzers and the ELF/Mach-O graft metrics.
