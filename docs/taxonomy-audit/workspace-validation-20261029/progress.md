# Shared workspace validation, 2026-10-29

Status: incomplete. A source-matched isolated build of the current sibling Cleave source was used; the default sibling release executable was stale. The current validation log is `.triage-work/dmg-good-20261029/review/validate-rebuilt-final.log`.

The rebuilt validator recognizes the eight directories and file-type exemptions that the older binary rejected. The PHP INI and VBScript regexes were bounded; positive and negative controls were checked. The two patterns now cap quoted INI values and pre-Execute statement prefixes at 256 bytes, so exceptionally long cases need a future matcher design that preserves coverage without excessive regex state growth.

Validation still fails on 29 oversized directories. The validator lists the exact directories and counts in the log. The taxonomy requires a complete relevance and duplicate audit before meaningful reorganization; an exception additionally requires explicit approval. Do not raise the global budget or add blanket exemptions merely to pass validation. `TAXONOMY.md` had conflicting 85 and 100 rule limits; the table now agrees with `RULES.md`, the later taxonomy table, and the current validator at 100.
