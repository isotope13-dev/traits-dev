# Python source distribution mislabeled-bad review — 2026-11-04

The 40 distributions were reviewed: 38 are bad and two are good.

`153b9dd39b6c` runs an installation hook that collects hostname, user, working directory, network and operating-system information and posts it to a Slack webhook. `3e67b6d875ee` posts directory listings, including the SSH directory, from an installation hook. Both are bad even though the packages present themselves as tests or proofs of concept. New findings combine install-hook, collection and outbound-reporting evidence. Both scanners flag each source file and its containing distribution; controls removing the webhook or SSH-directory path clear the respective finding. Full validation passed.

`3bde197fb401` downloads a binary during setup, writes a mining-pool configuration, marks the binary executable and runs it. It is bad. A new finding combines the download, launch and mining-configuration evidence; both scanners flag the source and distribution, and removing the mining configuration identifier clears the control.

The following 25 distributions are bad: `02b1b1763e2e`, `04c067140a34`, `19c56ac64ea7`, `248a04e76b4c`, `257f7be74581`, `4b6a84aa5c04`, `4e00307e965f`, `634f07075e34`, `744d8db1633e`, `8131311dd9b9`, `832f2eb1f9cd`, `8c045dcea65a`, `8cf1a988ace5`, `90990057f335`, `9682526bb4e9`, `a511f5b64aab`, `af8d445eaf5f`, `c771ff164481`, `cc056e46c209`, `da51a8c82f99`, `df7995160051`, `dfb59f81fe7f`, `eaf3797dca36`, `fdfef30d13e2`, `ff2cbfec50bc`. Their obfuscated install scripts change browser shortcuts to load an extension; static decoding recovered the same clipboard-replacement script from each. That script repeatedly replaces cryptocurrency addresses on the clipboard. Both scanners already flag the clipboard substitution and shortcut manipulation in every distribution; Hopper confirmed all 25 bad.

`3117cf486f9b`, `9ed2bfbf78b6`, `b6e9315ad082`, and `f7f53ed8da60` contain installation hooks that send hostname and local IP information to Discord webhooks. They are bad, including when presented as tests; existing findings match in both scanners.

`8a2a65ecffc3`, `927f0dc2b47a`, and `99c380656fc3` gather hostname, user and working-directory details and attempt to report them over DNS and HTTP when imported. `c76465282acb` attempts to package and upload Telegram Desktop session data; `1ed85a114d64` installs a reverse shell; and `ab7a25461a74` contains a browser-credential and Discord-token stealer. All six are bad and both scanners already report hostile findings. These are static behavioral findings, not proof of successful delivery.

`bbbbd3c66882` is an incomplete source distribution with packaging metadata and documentation but no executable package code. `8e037ecac5a9` has a manually invoked callback test with fixed URL parameters, but no installation hook or host-data collection. Both are good based on the supplied contents. The old hostile finding for sparse metadata and a repeated-nine version was downgraded to notable because those facts do not establish malicious behavior; both scanners now report no hostile findings on the callback package.

Full validation passed after the final changes. One performance rejection was replayed from the validation cache; an uncached run and a subsequent normal run passed.
