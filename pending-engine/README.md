# Traits parked pending engine support

Everything under this directory loads cleanly as YAML but references engine
features that the installed cleave (2.10.0) does not provide, so `cleave
validate` rejects the whole trait tree while they are in place:

- **`objectives/.../payload/font/`** — written against a `font` file type and
  `font.*` facts. This build has no such file type: it classifies
  `.ttf`/`.otf`/`.woff`/`.woff2` as `Unknown` and emits no `font.*` values.
  The font container/layout traits themselves now live in
  `metadata/file/format/media/font-{container,layout}.yaml` with `for:`
  retargeted from `font` to `data` so the tree loads; they remain inert for
  the same reason, and this carrier composite still references trait ids at
  their old `metadata/font/` path.
- **`objectives/.../payload/media/`** — the media container/layout traits have
  since been rehomed to `metadata/file/format/media/{container,layout}.yaml`
  with `for: [media]` and now load; this carrier composite still references
  them at their old `metadata/media/` path.
- ~~`objectives/impact/infect/binary/{note-cavity,graft}/`~~ — **restored.**
  The ELF/Mach-O anomaly atoms were rewritten to read `elf.entry_section` and
  YARA segment rules instead of the metrics this engine lacks, so the
  note-cavity and segment-graft composites load and are back in `objectives/`.

Nothing still parked here is capable of matching on this engine — a rule keyed
on a file type that is never assigned is inert — so parking it changes no
verdict. Both remaining files are carrier composites whose legs moved: they
need their `metadata/font/` and `metadata/media/` trait ids repointed at
`metadata/file/format/media/` before they can be restored, and the font one
additionally needs cleave to ship the sfnt/WOFF analyzer behind `font.*`.
