# Parsed archive facts belong in metadata

Five rules in `micro-behaviors/data/archive/member/traits.yaml` matched facts
reported by the archive parser: text-like member names, backslash separators,
duplicate member names, and encrypted-member counts. None described an
operation the analyzed program performs. The member-path facts now live in
`metadata/package/files/archive-member/payload-member.yaml`; duplicate and
encrypted-member counts live in `metadata/file/archive/archive.yaml`.

The matcher bodies, effective format and platform scopes, confidence, and
criticality are preserved. All consumers now reference the canonical metadata
IDs, including dropper and evasion composites. `TAXONOMY.md` distinguishes
parsed properties of the sample archive from code that uses archive APIs.

Soft validation passes **1,837/1,837 fixtures**. Strict validation remains at
the established **60 catalog-wide issues**, including **164 over-cap
directories**. No fixtures changed; this is a taxonomy relocation only.
