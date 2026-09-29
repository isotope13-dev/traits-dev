# Telegram profile exfiltration follows the source

The composite `telegram-system-profile-exfil` matched Node host/user profile
collection sent through Telegram, but was filed under the transport
`exfiltration/messaging/telegram`. Its npm preinstall wrapper lived separately
under `supply-chain/recon-exfil/install-hook`. `TAXONOMY.md` specifies that a
complete source-plus-send chain belongs under `exfiltration/stealer/<source>`;
Telegram is the channel, and the npm lifecycle is context.

Both composites now live in
[`objectives/exfiltration/stealer/system-info/profile/telegram.yaml`](../../objectives/exfiltration/stealer/system-info/profile/telegram.yaml).
The canonical rule still requires the same Telegram send and host/user query
evidence. The archive-scope npm rule still requires that canonical result and
`preinstall-runs-node-local-script`. Their descriptions, criticality,
confidence, mappings, scope, and effective platform/file-type defaults are
preserved. The `telegram-hardcoded-bot-config`, `npm-sysinfo-http`, and
`node-collect-exfil` consumers now reference the canonical source ID; both
existing suppression terms on the latter two rules remain present.

The supply-chain leaf falls **195 → 194** and the source leaf rises **84 → 86**,
below the 100-rule cap. The live package checks confirm the distinction:
JavaScript host/user data sent to Telegram matches the source rule; an npm
`.tgz` with a preinstall script that runs that file matches the package rule;
the same payload in a package without a preinstall hook does not match the
package rule.
