# Shell file-activation placement

## Decision

`objectives/command-and-control/dropper/file-exec` is the canonical leaf for a
staged file that is downloaded, made executable, and launched. These shell
rules require download, permission change, and local/background execution
signals, so they belong with file activation rather than the oversized
delivery/download leaf.

## Migration

Moved thirty-five composites total from `dropper/delivery/execute-download` to
`dropper/file-exec`, preserving their matchers, scope, metadata, confidence,
exclusions, and IDs:

- `shell-download-chmod-local-exec`
- `busybox-download-chmod-local-exec`
- `busybox-download-chmod-temp-exec`
- `raw-ip-busybox-download-chmod-local-exec`
- `raw-ip-busybox-multiarch-dropper`
- `encrypted-variable-payload-detached-dropper`
- `raw-ip-temp-download-chmod-exec`
- `raw-ip-literal-download-chmod-local-exec`
- `raw-ip-system-path-download-chmod-detached`
- `raw-ip-curl-literal-download-chmod-local-exec`
- `raw-ip-loop-download-chmod-var-exec`
- `raw-ip-redirected-download-chmod-exec`
- `multi-protocol-raw-ip-script-dropper-cleanup`
- `raw-ip-shell-fetch-chmod-detach`
- `multiarch-variable-protocol-dropper`
- `raw-ip-download-chmod-local-exec`
- `raw-ip-multiarch-shell-payload`
- `self-deleting-download-chmod-exec`
- `self-deleting-multiarch-download-dropper`
- `raw-ip-loop-download-chmod-exec`
- `raw-ip-bulk-download-chmod-exec`
- `raw-ip-bulk-multiarch-download-exec`
- `raw-ip-redirected-multiarch-dropper`
- `busybox-redirected-multiarch-dropper`
- `busybox-raw-ip-bulk-multiarch-dropper`
- `raw-ip-curl-bulk-download-chmod-exec`
- `raw-ip-curl-bulk-multiarch-dropper`
- `raw-ip-bulk-self-deleting-dropper`
- `multiarch-download-execute-loop`
- `raw-ip-multiarch-dropper`
- `raw-ip-multiarch-wget-dropper`
- `adb-tagged-multiarch-dropper`
- `multiarch-protocol-literal-exec`
- `raw-ip-shell-self-deleting-dropper`
- `raw-ip-masqueraded-shell-dropper`

Internal consumers in the old shell file and the external anti-analysis, cleanup,
and self-delete consumers now use canonical paths. All fourteen rules retain
their platform-neutral shell scope, matchers, proximity limits, exclusions, and
activation evidence.

The old rule has precision 10.7, slightly above the engine's normal composite
range; this was already true before relocation. The migration changes its
directory feature only and does not weaken the 30-line proximity requirement.

## Verification

- Temporary downloader → `chmod` → local execution samples match generic and
  BusyBox composites; a BusyBox temp execution sample matches the background
  variant, and the raw-IP variant still matches its endpoint leg.
- A control with the generic three signals separated by more than 30 lines
  does not match; all atomic evidence remains visible.
- The full soft fixture gate passes after the move; strict validation still
  reports the existing catalog-wide cap and quality debt.
