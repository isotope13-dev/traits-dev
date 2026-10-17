# buildhound-context fixtures

`vendor-member.js` carries BuildHound vendor markers plus the LaunchAgent +
Claude-config behavior shape: the identity composite fires and the
`launchd-agent-persistence-with-claude-config` suspicious composite stays
absent via the new `unless` leg.

`rogue-agent.js` carries the same behavior shape with no vendor markers.
Outside fixture directories it fires the suspicious composite (verified with
`cleave test-rules` against an identical copy in /tmp); under `testdata/`
the `source-runatload-key` leg is blinded by the
`test-fixture-directory-path` exclusion, so this case only pins the
identity's absence here.

`package.json` pins the manifest-name leg of the identity.
