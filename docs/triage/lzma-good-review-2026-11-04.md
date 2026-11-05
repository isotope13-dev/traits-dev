# LZMA mislabeled-good review, 2026-11-04

`27ea24b6918c` and `fe595cfd83f1` are XZ test streams containing “Hello
World”; the first intentionally lacks its end marker and the decoder reports
unexpected end of input. `9a6481a4aa6a` contains the quick-brown-fox text,
and `1ff2a49d3d2c` contains a small tar with a README and license.

`9aef898229de` decompresses to 17 repeated blocks, each containing 1 KiB
of a sequential repeated ASCII letter followed by 2 KiB of high-entropy data.
This is inert patterned data with no identified executable format; the decoded
file is reported as unknown by the scanner. `41c7d5561662` is an MSYS core
package, `ec91baaa1863` is a Brew Alpine package, and `37869c383d0b` is the
Phonopy source package. Fresh local scans of all eight carriers and the
separately decoded small payloads reported no suspicious or hostile traits.
Endpoint rulings: good; validation passed and Hopper confirmed all eight.

The Airflow package also present in this pool has the same hash as the package
reviewed in `ani-good-review-2026-11-04.md`. The remaining oh-my-pi archive is
under review.
