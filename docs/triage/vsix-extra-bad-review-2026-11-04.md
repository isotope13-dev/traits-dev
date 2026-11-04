# Additional VSIX bad-label review, 2026-11-04

This tracks the 100-file snapshot under
`/var/tmp/triage-vsix-20261104/mislabeled-bad/`. The snapshot paths do not
necessarily reflect current Hopper labels. Unlisted files remain unreviewed.

## Reviewed and recorded good

- `f75d45128a4e`: Sunset Gradient Theme. The startup entry point provides a
  welcome webview and theme selection, and the remaining JavaScript is a syntax
  highlighting demo. The archive scan reported no suspicious or hostile
  findings. Full validation passed and Hopper moved the sample to good.
- `1d260f4b4bb7`: Claude Commit 1.0.1. The extension gets a Git diff on user
  command, encodes the prompt for a local Claude CLI invocation, and populates
  the commit message. It passes `--dangerously-skip-permissions`, surfaced as a
  notable finding; the scan reported no suspicious or hostile findings. Full
  validation passed and Hopper moved this exact archive to good.
- `8d27165d7e69`: unofficial Claude Code Simplified Chinese translation.
  Its startup code locates the installed Claude extension, backs up and
  rewrites its webview and settings using bundled or user-configured text
  replacement rules, and exposes restore and reload commands. The included
  rules were checked for embedded code and network destinations; their regex
  replacements translate interface text. Atomscan reports no suspicious or
  hostile findings. Full validation passed and Hopper moved it to good.
- `72daf8f53460` and `874488c00ec9`: Dev Session Canvas Notifier 0.22.0
  and 0.24.1. Their bundles post desktop notifications through platform
  utilities and use random, expiring, single-use callback tokens to trigger
  restricted focus actions. The newer build adds localization. Their stated
  companion dependency returned `no_release` to Atomscan's follow operation;
  that outcome does not establish marketplace removal or a malicious
  dependency. Corrected the metadata finding and the dependent pack finding
  to describe unresolved references without claiming a takedown or payload.
  Rescans report no suspicious or hostile findings. Full validation passed,
  and Hopper moved both archives to good.

## Under review: altered Claude Commit archives

`cde571278c81` has the same publisher, name and version as `1d260f4b4bb7`,
but its entry point appends an immediately invoked function after the source
map directive. That code reads or creates a home-directory identifier and
silently POSTs it with platform and package metadata to an external service.
Its activation remains command-driven. The original entry point matches the
rest of this bundle byte for byte. The attribution and purpose of the added
reporting code are unresolved; do not treat the unchanged marketplace identity
as proof of authenticity or as proof of malicious intent.

`aaf9ae014190` includes the same appended reporting pattern, changes publisher
`juanlb` to `juajnnlb`, keeps the upstream repository and name, and enables
startup activation. Added a suspicious composite requiring those independent
observations; it does not claim credential theft or command-and-control.
Cleave matches the altered archive and not the original; controls restoring
the original publisher, removing startup activation, changing the repository,
or removing the appended code each clear the finding. Final endpoint rulings
for both altered archives remain pending further evidence.

Atomscan also matches the new composite on the lookalike. An earlier full
validation encountered a concurrent XPI fixture change; the subsequent
`make validate` run passed (`/tmp/vsix-e7-validate.log`).

## Encrypted Claude Code npm archive

`e7a10d27f537` is an encrypted ZIP, not a standalone VSIX. Its npm manifest
claims Anthropic authorship and the upstream Claude Code homepage under the
different `@chatgptclaudeclub` scope. Its command starts the bundled CLI with
an escaped, preloaded interceptor. Static decoding shows the interceptor
substitutes reads of Claude credential files, can configure a proxy obtained
from the service, and can act on heartbeat instructions to redirect models or
terminate. The client gathers hardware identifiers and posts the collected
inventory during device registration to the third-party service. It parses
message streams for usage counts; the reviewed initialization does not set the
optional endpoint for uploading entire captured requests and responses. Do not
claim it uploads conversation contents without further evidence.

Added a suspicious package identity composite requiring the official author
string, official homepage and Claude command with an unofficial package name.
The original manifest matches; changing each of the three claims or restoring
the official npm name clears the finding. The initial archive scan reports a
hostile hardware-enrollment finding and several obfuscation findings. The
manifest finding also appears in Atomscan, and `make validate` passed. The
package's full review and final disposition remain open.

## GitHub session identity-rewrite proof of concept

`5cae06a432da` is an executable credential-access demonstration, not a benign
hello-world extension. Its startup code patches `JSON.stringify` to replace
its extension identity with GitHub's pull-request extension identity, silently
requests an existing GitHub session with repository and workflow scopes, shows
the token, and uses it to list repositories. It displays a message describing
the potential for unauthorized repository access. Its explicit proof-of-concept
character does not make the implemented credential-access attempt benign.

Added a hostile composite for identity rewriting, silent session acquisition,
an access-token reference and a bearer-authenticated GitHub API clue. Both
scanners match the original; controls removing the rewrite, silent option, or
bearer header do not. An existing suspicious fixture implements the same
exploit and was moved to the hostile fixture set. Full validation and Hopper
recording completed: `make validate` passed and Hopper confirmed the existing
bad label (no-op).

## Boardwalk Plus startup downloader

`1a55c6fa904d` activates on every VS Code window. Before registering its
Kanban-board command, it downloads an external JavaScript file into a temporary
path and invokes it with Windows Script Host. On non-Windows platforms the
specified host is a temporary `cscript.exe` path, so successful execution is
not assumed there. This executable remote-stage behavior is unrelated to the
advertised board. The exact remote payload was not fetched or executed.

Atomscan reports `vscode-activation-http-jscript-stage` as hostile and also
reports the component HTTP download, file write, and script-host observations.
The one hostile finding describes the single observed chain; multiplying it
into overlapping hostile findings would duplicate the same behavior. The
endpoint ruling is bad; full validation passed and Hopper confirmed the
existing bad label (no-op).
