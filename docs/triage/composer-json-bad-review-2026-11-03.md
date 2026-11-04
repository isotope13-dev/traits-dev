# Composer.json mislabeled-bad review

The single manifest was inspected and scanned with Cleave and Atom, with reference following disabled. Both scanners report the existing hostile static finding; Atom nevertheless renders an overall BENIGN 33% verdict.

- `1ca7fc7757286efb2b9b7e91dd6e8cbfc0604babf7791e4564c8111ecc61e308` — **bad** — Its post-install hook silently downloads an executable from a release URL into a hidden temporary path, makes it executable and launches it in the background. The existing combined Composer dropper trait describes that behavior.
