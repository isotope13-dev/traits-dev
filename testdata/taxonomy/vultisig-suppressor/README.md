# Vultisig package-name suppressor regression

The published `@vultisig/sdk` npm tarball at version 10.1.0 is pinned here as a benign wallet-SDK control (SHA-256 `ac318411e19c1fc20394ee307e6e651693939eb618a9f848d54c180e4f99527a`). Its bundle contains normal wallet transaction RPC methods and cryptocurrency address patterns. Those capabilities alone must not produce a wallet-drainer finding.

The three JavaScript controls are synthetic hostile behavior samples derived from an existing hostile fixture. Each changes a transaction destination and intercepts a browser wallet provider. Two also carry copied Vultisig text; a counterfeit npm archive declares the exact package name. The behavior findings must survive those copied identifiers. The counterfeit also verifies that package identity is still recorded as metadata, without acting as a suppression.

The old directory-level exception hid behavior findings anywhere under a package path containing the Vultisig name. The test checks that copied names and repository URLs do not hide hostile behavior, while ordinary RPC and address support in the official SDK do not, by themselves, imply a browser wallet drainer, address hijacker, or transaction rewrite. The archive is inspected statically; no package code is executed.
