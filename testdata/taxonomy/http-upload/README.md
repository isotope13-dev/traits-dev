# HTTP transfer, source, and local capability controls

Synthetic examples are scanned, never executed. Run:

```sh
python3 scripts/check-http-upload-routing.py
```

The runner copies each file to a temporary location outside the fixture tree.
These controls assert individual taxonomy findings, not whole-file risk scores.

The cases distinguish local archive creation from archive upload, local hybrid
cryptography from encrypted HTTP export, form construction from image export,
MIME types from screenshot activity, and transfer-encoding headers from payload
encoding. Other controls cover neutral appliance paths/network commands, route
construction, schema fields, upload consent, and BitTorrent metainfo creation.

Three profiler controls exercise the actual rewritten consumer: browser and
wallet targeting plus a retained HTTP capability, the same sources without
transfer, and transfer without the wallet source. The local-only case includes
a credential-named mapping fragment that used to count as HTTP exfiltration.
These original controls use a wallet-extension identifier and a neutral
variable name. The subsequent [blockchain controls](../blockchain/README.md)
cover `wallet.dat` and generic wallet terminology after removal of the blanket
blockchain-library exclusion.

Hostnames use reserved example domains. No fixture should be run as a program.
