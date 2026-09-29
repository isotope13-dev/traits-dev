# Swift beacon-format and path clues leave encrypted payload taxonomy

## Findings and placement

`swift-dns-checkin-labels` matched only the quoted words `status`, `checkin`,
and `heartbeat`; it contained no DNS API, resolver, or network operation. It
now lives as `swift-checkin-state-label-set` under
`objectives/command-and-control/beacon/format`, where the matcher describes a
probable beacon-format clue without asserting DNS transport.

The only higher-order consumer combined that field set with a hidden temporary
path and an SSH authorized-key path. It moved from
`anti-static/obfuscation/payload/encrypted` to the same beacon-format leaf as
`swift-beacon-format-with-sensitive-paths`. Its three evidence legs and
hostile criticality/confidence are preserved; its inherited mappings now match
the beacon-format subject (`T1071`, `B0030`). The name records co-occurring
evidence rather than claiming DNS or a completed file transfer.

`swift-hidden-system-logs-stage` matched only the literal `/tmp/.system_logs`.
It now lives as `swift-hidden-system-logs-path-reference` in
`micro-behaviors/fs/path/temp`. The path matcher, Swift/Unix scope, suspicious
criticality and confidence are unchanged; the new description does not assert
that a write or staging operation occurred. The two remaining source-command
composites that use this path clue now reference its neutral capability ID.

## Verification and remaining review

A synthetic Swift sample containing the three required clues matched both the
relocated path atom and beacon composite. The existing source-command rule
conditions were retained where they remain in that file. The anti-static
encrypted-payload leaf loses three definitions; no rule was deleted.

The remaining `swift-staged-account-copy` and `swift-staged-ssh-session`
composites still need source-to-sink review: their current names claim file
copy/staging, while the available rules combine path clues with a URL-session
marker and do not directly connect the named files to reads or writes. This is
an explicit follow-up, not evidence that the files were staged.
