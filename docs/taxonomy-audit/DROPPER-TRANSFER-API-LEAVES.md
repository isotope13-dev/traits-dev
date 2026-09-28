# HTTP API dropper technique leaves

The 30 rules moved from the generic `dropper/delivery/execute-download/` leaf
identify one of three concrete Windows transfer APIs. Thirteen use WinINet,
eleven use URLMon, and six use WinHTTP. They live in sibling technique leaves under
`objectives/command-and-control/dropper/delivery/`:

- `wininet/` identifies download-and-execute patterns built on the WinINet API.
- `urlmon/` identifies patterns built on URLMon, including
  `URLDownloadToFile`.
- `winhttp/` identifies patterns built on WinHTTP.

Both children state a specific transfer technique under the broader malware
delivery behavior. They are peers, not language or filetype buckets, and remain
at depth five. The general `execute-download/` leaf remains for techniques that
do not fit either API-specific category.

The moved rules retain their matcher bodies, criticality, confidence, tags,
platform constraints, size bounds, suppressions, and each rule's effective file
type scope. Short references remain inside their technique group. Existing
external consumers now use canonical API-leaf references. See the mapping
ledger for the exact IDs.
