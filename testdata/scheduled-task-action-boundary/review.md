# Ouro CLI version drift review

Verdict: **BENIGN** — `@ouro.bot/cli` 0.1.0-alpha.936, SHA-256
`c043fa2bbc6413ead04ada7a021e10e276eb668dcfaa87a49f8957b38f1d410b`.

This is a Node.js AI agent CLI and daemon with messaging integrations,
terminal-agent supervision, a mailbox UI, and an operator-run Unraid deployment.
The tarball has no install/preinstall/postinstall hook. Its `prepack` hook
builds and verifies release assets before publication.

## Decisive version evidence

Fetched the npm registry tarballs for alpha.935 (immediate predecessor) and
alpha.850 (before the flagged documentation). Verified both registry SHA-1
checksums; the alpha.936 tarball also agrees with its registry checksum.

* alpha.935 SHA-256: `0e58e4ea5f91f67224bd2beb8fcf3a4f882b7a7b3ffefcca5a98d356104ad935`.
* alpha.850 SHA-256: `309d58f8f4ddad5b6c2251defdb7e0a92b436712363533a83993d26ebcb1b0ce`.

The alpha.935 → alpha.936 content diff leaves `deploy/unraid/README.txt`,
`sanctuary-butler-upgrade.mjs`, and `sanctuary-authority-root-lifecycle.js`
byte-identical. Package manifest and shrinkwrap change only the package version;
dependencies and lifecycle scripts do not change. Added code provides Shepherd
local-owner commands, bounded supervision replicas, custody reconciliation and
offline archive recovery. The UI bundle changes implement that supervision view.
The JavaScript uses ordinary TypeScript CommonJS output and a minified UI bundle.

The alpha.850 → alpha.936 README diff adds operator trust-directory instructions.
The old regex matches these exact spans on line 11 of the new README:

```
/trust /mnt/user/appdata/ouro-butler/trust/sanctuary` (this also makes /mnt/user/appdata
/trust/sanctuary:/etc/ouro/trust/sanctuary -v /mnt/user/appdata
```

Neither is a Windows task action. They belong to `install -d` and Docker bind
mount instructions. Alpha.850 has neither regex match; alpha.935 already has both.
Thus the immediate predecessor also demonstrates that the queue's alert is not
new executable behavior in alpha.936.

## Execution paths checked

`ouro-entry.js` dispatches argv through the CLI parser/executor. Shepherd
administration is reached only through explicit Shepherd commands and resolves
an existing local owner. Mutations check revisions and request IDs. The new
maintenance command verifies fresh disabled/stopped daemon state and retired
terminal inventory before copying a local SQLite custody ledger into a private
archive, retaining replay barriers and an interruption-recovery marker. Its
SQLite `exec` calls execute database statements, not shell commands.

Terminal observations come from configured cmux/Herdr hosts. The publisher
projects bounded summaries into a mode-0600 local JSON replica. The mailbox GET
route reads that replica with ownership, mode, size, no-follow and inode checks;
it does not add a remote administration route. Mandates persist to private
local files. These effects fit the existing agent-supervision purpose.

The unchanged Unraid upgrade entrypoint requires explicit operator invocation
and root, checks the selected Docker image, stages/verifies package pins,
recreates the resident, and installs its documented supervisor/watchdog.
The root lifecycle validates requests, image identity and root custody before
starting the Telegram authority gateway. Its Telegram getMe request validates
the configured bot token with Telegram. Process execution, ownership/mode
changes, network access and cryptography are expected deployment capabilities;
no hostile source-to-send chain or concealed execution was established.

## Detection change

Require horizontal whitespace after `/tr`, preserving its Windows task-flag
meaning while excluding `/trust`, `/trigger` and `/truncate` path/text prefixes.
Keep the existing behavior home and severity; this fixes the matcher rather
than suppressing this package by identity. Fixtures cover TEMP, APPDATA,
AppData, escaped AppData and Local/Programs paths, Unix bind mounts, prefix near misses and
a line break that must not supply a task argument.

The README also contains an inline PHP `rename($temporary, $outputPath)` call.
The pre-existing generic dollar-variable matcher described this as Perl.
Renamed it to `rename-dollar-variable-paths`, removed the unsupported language
claim, and updated its two exact consumers without changing matcher or scope.
Perl, embedded PHP, and prose controls cover this naming correction.

Base64 review: the large literal in `twilio-phone.js` contains an
ID3/MP3 silence asset used by the Twilio stream-failure playback buffer.
The complete Base64 quartets decode to 1,368 bytes; one dangling data character
prevents strict whole-literal decoding. This is an audio fallback, with no
code-evaluation sink. JWT payload decoding in `auth-flow.js` parses Base64 JSON claims.
Neither decoded value is passed to an evaluator or process launcher.

Validation: all 11 focused positive/negative fixtures passed using local traits.
The final atomscan archive rescan completed successfully with the task false
positive absent. The full local-rule report had no suspicious or hostile
findings; the final README report retains five accurate notable observations.

Judgment marker / commit-body line:
`Ouro CLI alpha.936: bound /TR flag; label generic rename accurately`
