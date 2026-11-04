# IPA mislabeled-bad review — 2026-11-03

The sole entry, `c86826bcbede`, is a password-encrypted ZIP containing three IPA archives. It remains bad: the Coinbase Wallet bundle contains a Lending framework with wallet-unlock and account-monitoring behavior and transaction manipulation. Both scanners retain hostile findings for the archive and that framework. The collection's documented archive password allowed offline inspection; no sample was executed.

The MetaMask IPA's 20 MB JavaScript bundle had a separate hostile wallet-file-exfiltration finding based on unrelated file reads, encryption, wallet vocabulary, IPFS references, and POST-related code spread across the bundle. The composite now requires its evidence within 8192 bytes. Both scanners clear the bundle, while a compact proof of concept that reads a wallet mnemonic, encrypts it, and POSTs it still receives the hostile finding. This correction does not determine whether the rest of the IPA is benign.

Full validation passed and Hopper confirmed the bad label.
