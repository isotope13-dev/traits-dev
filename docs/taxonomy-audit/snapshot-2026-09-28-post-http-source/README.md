# Shared-tree snapshot after socket-to-process boundary review

Generated 2026-09-28 from base revision
`a5d07653229f5482466ac164b221e884d781a849`, including uncommitted/concurrent work.
The established snapshot directory name is retained.

The [wallet-UI audit](../WALLET-UI-BOUNDARIES.md) records **44 moves, one merge,
and two unsupported hostile wrapper retirements**. Desktop-wallet falls from
24 to 17, objective mnemonic from 41 to 33, and blockchain-library from 63 to 56.
The [socket-relay audit](../WEBSHELL-REQUEST-FD-REDIRECT.md) moves the ASP.NET
reverse-shell chain and its socket/process evidence to reverse-shell descriptor
redirection and neutral socket creation. The [wallet-keyring audit](../SENSITIVE-DATA-WALLET-KEYRING.md)
moves seven source-specific export rules into `stealer/wallet`.

Across **20,672 YAML files** and **118,817 rules** (79,336 atomic and 39,481
composite), there are **144 oversized directories**, **16,076 rules in them**,
and **3,836 excess rules**. No cap exemption exists. Atomic overlap review contains
**102 groups / 229 rules touching violators**, with **431 groups globally**.
No rule directory is deeper than five. Sparse sibling review uses 35 and does
not flag a single child alone.

The [wallet-UI verification record](../wallet-ui-verification.json) protects 541
original definitions. **127 focused assertions** pass across 37 files. All
**1,842 corpus fixtures** pass in the controlled snapshot with current taxonomy
overlays, including the added benign path control. No corpus files or fixtures
are excluded. Live strict validation reports **98 issues**, including the 144
cap violations. The full migration remains unfinished.
