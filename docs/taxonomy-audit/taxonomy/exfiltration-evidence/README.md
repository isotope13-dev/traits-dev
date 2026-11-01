# Exfiltration evidence migration

Six rules moved from `objectives/exfiltration/sensitive-data/source` by what
they actually establish:

- Two CSS character-oracle composites remain hostile and move to
  `objectives/exfiltration/side-channel`: a character sweep plus a remote
  resource request supports the export objective.
- Two `EXFIL` framing strings move to `micro-behaviors/data/serialize/envelope`.
  One mentions a file, while the other contains a value and length; neither
  alone establishes a socket transfer or a credential. The frame used by a
  credential-transfer composite is a component. The unreferenced file-labelled
  frame is a notable text observation. Their unsupported ATT&CK labels are
  removed.
- A C# signature-shaped string and a Go identifier string move to
  `metadata/lang/source/naming/function/{signature,communication}`. The names
  explicitly say “exfiltrate”, so they are notable text observations; they do
  not establish a call, transfer or platform attribution. Their inherited scope
  and confidence remain unchanged.

The one exact consumer of the credential frame was retargeted. Three other
rules refer broadly to `objectives/exfiltration`: the four name and frame
observations no longer satisfy those broad references on their own. That is an
intentional precision change; the CSS transfers remain in the objective subtree.
No directory reference to the retired source leaf was found.

[moves.json](moves.json) preserves original rules and maps their IDs. Run
`uv run docs/taxonomy-audit/taxonomy/exfiltration-evidence/check-moves.py`
to compare matchers, scope, confidence, criticality, and both physical and
namespace populations. Other sensitive-data rules remain to be reviewed and
migrated.

`make validate` passed all 13,920 classified fixtures for the initial six-rule
batch. A focused `cleave test-rules` check also matched both the relocated frame
 and its credential-transfer composite on `cases/credential-transfer.c`. On
 `cases/frame-only.c`, the frame matched and the transfer composite did not. The
 fixture source is analyzed statically and is not executed.

## Go and file-neighborhood review

The former `source/go.yaml` held an encrypted paste-service transfer, a
credential-file/socket transfer, an ordinary DNS-and-environment co-occurrence,
and an unreferenced generic OR of more specific findings. The transfer rules
moved to `http/paste-service` and `stealer/credential`. The DNS/environment
profile moved to `metadata/file/profile/network` at baseline: its former size,
signature and path suppressions and exfiltration annotations were removed so
those generic observations do not imply transfer. Its old file-scoped legs
were Go-only DNS and Lua-only `_ENV`, so they could not match together and the
Lua leg was not OS-environment access. The replacement uses Go OS-environment
access and is scoped to Go. The redundant OR was removed.
[go-moves.json](go-moves.json) records the original definitions; run
`uv run docs/taxonomy-audit/taxonomy/exfiltration-evidence/check-go.py`.
The Go DNS/environment fixture matched the repaired profile, while the
DNS-only control did not. These fixture files are analyzed, never executed.

The `stealer/file` leaf had 88 rules. Its review moved 18 rules by subject:
credential-bearing files, configuration, account inventories, activity history,
documents, credential validation and instruction coercion. The file leaf now
has 69 rules. A supposed source-code upload only required a file open and an
encode/decode request; it became a neutral network profile. A credential-target
and authentication composite did not require a transfer and moved to
credential validation at suspicious. A log-forwarding instruction moved to
LLM egress evasion rather than claiming completed export.

Two synthetic QNX composites and their three now-unused atoms were removed:
`FILE=%s/%s` does not identify a home listing, and a formatted `HOST`/UID string
plus a host lookup and send call does not establish the claimed host-profile
transfer. The existing broad file-directory consumer was reviewed: it retains
its threshold and the moved transfer evidence, while excluding those unsupported
claims and the two non-transfer observations. See
[file-reorganization.json](file-reorganization.json) and run
`uv run docs/taxonomy-audit/taxonomy/exfiltration-evidence/check-file-reorganization.py`.

After the Go and file-neighborhood changes, `make validate` passed all 13,920
classified fixtures. The subsequent [host-profile review](../host-profile-neighborhood/README.md)
reorganized the 90-rule profile leaf alongside its identity and account siblings.
