# Staging stub review

The eight rules under `staging/stub` were reviewed and moved by evidence. Their
match conditions, scopes and confidence were retained; unsupported attack
labels and claims were removed.

- The Back Orifice installer wording is a notable product reference in
  `well-known/malware/backdoor/back-orifice`. The fixed-offset `fseek` source
  and the `fileNumber` comparison or relative-seek alternative are components.
  Neither atom alone establishes self-extraction or a second payload.
- Self-read plus offset-seek references is notable under
  `micro-behaviors/fs/read/self`; its consumer that also requires hidden and
  detached process indicators is suspicious under hidden process execution.
  Corresponding combinations requiring the Back Orifice reference remain in
  that family's catalog, so generic behavior does not depend on malware
  identity. All 128 combinations of the original evidence legs were checked
  for equivalent composite matching. Neither branch claims the observed
  operations are bound to one payload.
- WinRAR SFX plus numbered executable part names is a notable archive profile.
  Two unsigned overlay profiles with a temporary executable path or a loader
  name are notable, not proof of a write or a watchdog. The existing
  `metadata/file/profile/overlay-api` directory was renamed `overlay` to house
  both API and path correlations with a common subject.
