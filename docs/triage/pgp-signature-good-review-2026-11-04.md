# PGP signature mislabeled-good review, 2026-11-04

All 40 samples are OpenPGP signature artifacts. GnuPG packet inspection
successfully parsed them: 39 contain one binary-document signature packet and
`60bee61fd77b` contains two. This establishes their structure, not the
validity of the signatures or trust in their signers; the signed documents and
verification keys were not part of this review.

The local slow scans with reference following disabled report no suspicious or
hostile traits. Five samples have a notable candidate Base64 decoding
observation, without a hostile finding. Their endpoint ruling is good as
standalone signatures. All 40 hashes matched their local pool identifiers,
`make validate` passed, and Hopper confirmed all 40 good labels (no-ops).
