# Command and SSH observation corrections

Placement review by supported observation: a call passing a cmd member belongs
in process/create/shell/bridge; a key filename set belongs in fs/path/private-key;
Join-Path of USERPROFILE and .ssh belongs in fs/path/secret-config because the
directory also holds configuration and public keys. Neither path nor names prove
credential theft. A second review by neighboring boundaries reached the same
homes: these are not remote tasking or credential-acquisition observations.

Mapping:
- objectives/command-and-control/remote-command/tasking::json-cmd-field-exec-chain
  replaced by micro-behaviors/process/create/shell/bridge::js-cmd-member-exec-call.
  Intent inference now remains in the existing HTTPS polling composite, which
  separately requires JSON parsing. The replacement matches an actual call
  argument, not a JSON parse followed by unrelated comments and a declaration.
- objectives/credential-access/ssh/key::powershell-ssh-key-name-set moved to
  micro-behaviors/fs/path/private-key with unchanged matcher and Windows scope.
- objectives/credential-access/ssh/key::powershell-userprofile-ssh-dir moved to
  micro-behaviors/fs/path/secret-config with unchanged matcher, scope and exclusions.
  Both moved observations are notable and omit unsupported attack/collection tags.

Exact references and ancestor selectors were reviewed. Only the local tasking
and key-harvest composites referenced these old atoms. Existing objective parent
selectors intentionally lose the neutral atoms; capability selectors gain them.

Controls: command-member.js matches the command atom; version-launcher.js does
not. key-read.ps1 matches both SSH atoms and the harvest composite;
key-name-policy.ps1 matches the name set but neither directory nor harvest.
The three reviewed archives and fetched dependencies emit zero suspicious or
hostile traits after these edits (782, 53 and 83 analyzed units respectively).
