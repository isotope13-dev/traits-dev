# Staging shape review

The legacy `compressed`, `image-map`, and `public-folder` staging leaves were
retired, and the macOS archive execution rule moved from `zip-stage` to shell
download and execution. Other rules in `zip-stage` remain for review.

- The GeTaOEP banner is a tool reference, so it moved to the existing OEP
  finder catalog. Its original broad substring and whole-file scope are
  preserved; cleave has an exact-ID exception for that reference because its
  meaning does not depend on binary size or section.
- Public-folder matches describe path-shaped text, not proof of a generated
  name or a dropped file. The full executable path is now a notable path
  observation, and the incomplete path fragment remains a component.
- The PowerShell gzip rules were moved to encoding profiles. Their predicates
  detect co-occurring compression, path text and byte values, not an actual
  write or header overwrite. Ordinary `.bin` combinations are notable; the
  RTF combinations remain suspicious leads. Names, descriptions and ATT&CK
  labels were corrected without narrowing the predicates.
  The synthetic EXE-to-`.bin` fixtures are notable; the `.rtf` fixtures are
  suspicious. The fixture named `rtf-stomp.ps1` contains the header bytes as
  text but does not overwrite the output header.
- The macOS rule retains its bounded fetch, extraction, chmod and launch
  evidence under shell download execution. To make room, the crowded shell
  directory was split: 43 existing fetch-and-execute rules and the macOS rule
  now occupy `command/fetch`, with exact references retargeted. Other
  shell execution rules remain in the parent for subsequent review.
