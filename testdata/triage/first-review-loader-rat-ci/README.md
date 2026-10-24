First reasoned review: XWorm client, PowerShell crypter, and vulnerable CI

The SHA-256 identities are recorded in review.json. Original samples were
scanned with atomscan (slow, no update, no followed references) and cleave
facts. Static reconstruction used Python AES/XOR decoding, token-resolved
CIL disassembly with dnfile/dncil, and rizin x86 disassembly. Nothing in the
samples was executed and no configured endpoint was contacted.

The 48 KiB PE is a symbol-obfuscated Visual Basic XWorm V3.0 client. Its
reachable handlers and installation code establish malicious behavior.
New CIL shape observations add distinct screen-response, self-removal and
shutdown coverage. Wildcard call operands are not independently resolved by
the matchers: their descriptions say references/construction, and hostile
consumers additionally require the independently established backdoor.

The workflow exposes a secret to a local action after external-head
checkout. Neither the local action nor any theft payload is supplied.
Treating this configuration as proof of credential theft was unsupported.
The complete old match is retained as a suspicious CI configuration
property under metadata/build/ci/gate. The two permission variants have the
same evidentiary limit and retain their properties there too. The local
secret atom's matcher is unchanged; its name/description now accurately
state proximity rather than asserting an action type or same-input flow.
Its exact consumers were updated. Ancestor credential selectors were
audited; the broad env/secrets theft consumer is scoped to scripts and
cannot consume a github-actions property. No attack detector was suppressed.
The prior unguarded-workflow fixture is moved from hostile to benign with
the suspicious risk required and hostile findings forbidden.

The PowerShell executes AES-decrypted source, reconstructs a masked managed
hollowing launcher, and repeatedly installs a native image into a suspended
Framework host. Existing hostile traits cover these distinct stages. Add a
neutral process-query/loop/delay co-occurrence observation; it does not
claim persistence across reboot, network beaconing, or a bound relaunch.
The protected native payload's downstream application identity remains
unresolved and is not used for the verdict.

Run the focused controls from the repository root:

    TMPDIR=<scratch> python3 testdata/triage/first-review-loader-rat-ci/check.py

Controls include the real client, byte-asserted CIL mutations, unrelated
managed binaries, gated and ungated workflows, permission variants, real
credential exfiltration, and ordinary process polling. Mutation files are
static probes, not runnable benign software. Existing managed task/screen
and PowerShell native-host controls are also run. Before/after scans compare
all decoded children, not just the outer files. No archive members exist in
these three original samples; PowerShell decoding yields three children.
