# Second review: be23e6, b73ffee, 57515e

## Identity and behavior

* be23e60ee6e1e62ed73d92746c7d344f54c2d7920a65464a5c03e05d6acce451:
  Mozilla XPI, Trus-Web3 WALLEТ 1.0.1. The final name character is Cyrillic.
  Manifest has an empty permission list and claims no data collection. The
  popup nevertheless makes ordinary web fetch requests. React and Ethers
  occupy most of the bundle and explain the cryptographic/RPC capabilities.
  The application checks one fixed Ethereum address's balance at Infura;
  positive balance enables its recovery UI, otherwise a blockchain dashboard
  provides cover. Seed words pass BIP39 validation, are joined and forwarded
  to Hi -> nu. Private keys pass network-specific syntax checks and go through
  ru -> nu. nu puts btoa(secret) in an event object's properties, serializes
  that object into an authenticated POST to api.segment.io/v1/track, and both
  paths show an import error. This is secret theft, not wallet analytics.
  ZIP CRCs pass; the alternate popup loads the same script. MALICIOUS.

* b73ffee54be102a0292739404232a589f16bb256026066e9b9cefe81170670b5:
  UTF-16LE Windows JScript source fragment. Instantiates FileSystemObject and
  WScript.Shell; the complete prefix would copy the current script to Public
  Downloads once. A helper strips an arbitrary non-ASCII delimiter. The last
  statement is an unterminated string, ending after the first emoji of the
  delimiter; JavaScript parsing reports an ERROR. There is no launch/eval sink.
  Deinterleaving the surviving Base64 chunks and decoding complete quartets
  yields a partial PowerShell-shaped string containing a split HTTPS URL.
  Neither the missing rest nor a decoder/sink is part of this specimen.
  The fragment's obfuscation is suspicious, but claiming infection or payload
  execution from its prefix was unsupported. BENIGN as supplied.

* 57515eece02d05b1eb7d39f479c1515c1ace2e2c6580e8d2aea67f34fdf55e23:
  Python SMTP/STARTTLS command-shell implementation. callback(host, port=25)
  repeatedly connects out, reads SMTP banners, sends EHLO and STARTTLS, and
  wraps the socket with a default certificate-verifying TLS context. Received
  bytes are decoded and passed directly to subprocess.check_output(...,
  shell=True); stdout returns over the same socket. Disconnects are followed
  by a random 600–699 second pause. It sends no mail and defines, but does not
  invoke, callback. MALICIOUS command-execution capability; no claim of an
  automatically started connection, disabled verification or email theft.

## Detection changes and placement review

* Self-path plus copy API is neutral filesystem evidence, not script infection.
  Moved the observation and its helper to fs/file/copy. No propagation claim.
* Non-ASCII delimiter removal conceals strings, not a steganographic carrier.
  Moved it to anti-static/obfuscation/string/conceal. The contextual WSH
  composite now requires actual dynamic evaluation and is suspicious.
* A WScript global reference identifies the runtime, not process creation.
* Tuple-address connects and sends of output-named variables are neutral
  socket capabilities. Updated their objective consumers to the new homes.
* SMTP STARTTLS control requires established command tasking or a native TLS
  command shell; ordinary mail upgrades remain neutral.
* btoa object fields belong to Base64 encoding, not an analytics service.
  Wallet exfiltration additionally requires a serialized fetch body, POST
  method and joined-word forwarding/error path in the same file, preventing archive-wide unrelated evidence pooling.
* Ethereum lookup method literals are neutral RPC observations, not C2
  infrastructure. Generic ledger method names require Solana-specific context
  before claiming Solana. Maximum uint256 is a numeric constant, not approval.
* Generic mismatch diagnostics do not establish a downloaded file or abort.
* bitGet is a bit utility, not Bitget. Commas in mnemonic arrays do not declare
  PAN fields. BIP39 wordlist words do not establish a Portuguese phishing lure.
* Whole-source URL/unicode decoding can preserve plain URLs unchanged. The
  encoded-HTTP observation now selects base-encoded/XOR blob decodes and makes
  no concealment claim from neutral encoding alone.

All moves retain exact consumer references. Severity/coverage corrections are
intentional changes stated above, separate from placement-only moves. New files
use existing leaves. Positive and near-miss controls are scanned from
scratch/acquit-controls to avoid test-path suppression. The supplied originals
are scanned with atomscan and cleave; raw cleave facts were read for all three.

Controls are retained in `acquit-controls/`. To reproduce without filename-based
suppression, copy them into a directory without a test-path component and scan
that directory with `cleave --traits-dir . --format json`. Self-copy, encoding-only,
ledger-methods and wallet-analytics must have no hostile detections. Generic
ledger-methods must not have Solana, Bitget or PAN findings; solana-context must
retain the Solana method observations. Delimiter-eval must retain concealment
observations, without a hostile conviction from WSH object creation alone.

Final detections: XPI has two distinct hostile traits (phishing and wallet-secret
export with the import-error path); the JS fragment has no hostile and one suspicious
trait; SMTP shell has two hostile traits plus its suspicious SMTP carrier. The
eight control files pass the stated assertions. Initial hostile precision scores
were 8.9/8.2 for SMTP and 8.4 for wallet export, above the 3.5 authoring floor.

The separate import-error composite is consolidated into the wallet-export
rule, which now requires that path itself, avoiding a redundant hostile trait.

Native SMTP/STARTTLS and ordinary mail-upgrade controls also cover the carrier
rule: native remote shell must match; ordinary SMTP upgrade must not.
