# Install-hook environment-secret source routing

The matcher file `env-secret.yaml` was under
`objectives/supply-chain/recon-exfil/install-hook`. Its three composites
identify an install hook that reads process-environment secrets and transmits
them. `TAXONOMY.md` already gives this exact behavior the canonical home
`objectives/exfiltration/stealer/env`; installation is contextual evidence,
not the behavior's taxonomy axis.

The file moved to
[`objectives/exfiltration/stealer/env/install-hook-env-secret.yaml`](../../objectives/exfiltration/stealer/env/install-hook-env-secret.yaml)
without changing any bytes. Its SHA-256 remains
`cbb0d9122c34ab13a2436a740fea3a2301d187e9ca1da09f331c86ea001528d2`.
The three composite IDs are local to the file; a repository-wide search found
no external references requiring edits.

The move preserves the three source-plus-transmission chains and their full
install-hook context. It does not imply that every package-install signal
belongs under exfiltration: a result whose defining behavior is package
deception, hidden payload delivery, or execution still follows that behavior's
documented supply-chain or dropper home.

The leaf counts changed from 198 to 195 in
`supply-chain/recon-exfil/install-hook`, and from 61 to 64 in
`exfiltration/stealer/env`. Both remain within the single inclusive 100-rule
cap at the destination; the source remains oversized and needs a broader
source-by-source audit. The inventory immediately after this move recorded 79 violating
directories and 2,026 excess rules; the later TCC source reclassification is
recorded separately in [its audit](TCC-APPLE-SECRET-MANIPULATION.md).

The prebuilt engine's soft validation after the move still reports three
unrelated benign paths from `pyaigis-top10.tar.xz` against
`anti-static/obfuscation/payload/encoded::shell-eval-base64-decode`. A fresh
`make validate` remains blocked during compilation because the checked-out
`stng` crate does not expose `decode_xor_fat_macho`; this move therefore has no
fresh-source full-corpus parity claim.

The adjacent `objectives/supply-chain/credential-theft/env` directory remains
legacy taxonomy debt: `TAXONOMY.md` directs install/build/import credential
theft to the canonical credential-access or exfiltration source and says to
retire duplicated outcomes there. It contains environment-access rules and
two package-context composites that require a separate coordinated audit.
