# Closing the legacy `stealer/sweep` leaf

The source taxonomy classifies what data probably leaves. A sweep is an
acquisition/search method, not a data source; the old leaf had no coherent
admission contract. Its final three entries are handled individually below.

| Former entry | Evidence and problem | Disposition |
|---|---|---|
| `android-webview-location-file-spyware` | Requests location, contacts, storage, and Internet permissions; combines a remote-content WebView and a Base64 class reference. It requires neither a location/contact/file read nor a transfer operation. | Retired from `stealer/`. Permission, WebView, and Base64 findings remain independently available in their capability homes. Existing Android spyware composites that require actual capture or messaging evidence remain intact. |
| `binary-exfil-to-ip` | Requires a raw-IP URL and libcurl custom-header behavior, plus any one of broad file-targeting, system-fingerprinting, or credential-validation directories. Header configuration does not establish upload direction, and optional directory context does not establish the data sent. | Retired from `stealer/`; direct-IP HTTP and libcurl findings remain available as channel/capability signals. Source-specific upload rules continue to classify actual read-plus-send chains. |
| `native-mcp-snapshot-upload-language` and its consumer | The original phrase matcher required generic upload/send/post wording near snapshot/export, with no sensitive source in the atom. Its composite separately required a Cloudflare tunnel and credential/token wording, but the source and transfer wording were unbound. | Moved the protocol-neutral wording clues to `micro-behaviors/communications/transfer` and combined their two word orders there. The credential composite requires that transfer clue, a Cloudflare tunnel, and either a credential-snapshot or token-capture clue within 128 bytes. |

The two unsupported hostile composites were removed rather than assigned new
objective labels: neither had evidence for a defensible destination. This
intentionally removes their overclaim while preserving the underlying
capability/channel observations. The native composite remains, with a
proximity-bound source, transfer, and tunnel combination; a generic upload
phrase or a credential phrase alone cannot satisfy it. The independent transfer
wording clue remains visible in its neutral capability home.

The focused regression script synthesizes a minimal ELF for five cases. A
credential snapshot/export phrase near upload plus a Cloudflare tunnel must
match the relevant transfer atom, transfer composite, and stealer composite.
The script also covers token capture, both phrase orders, a tunnel with no
transfer phrase, a transfer phrase with no sensitive source, and missing tunnel
context. Run it with:

```sh
python3 scripts/check-stealer-sweep-resolution.py --cleave ../cleave/target/debug/cleave
```

The `stealer/sweep` leaf now contains no YAML rules and receives no new rules.
Future broad file searches belong in `collection/file-targeting`; any resulting
export belongs under the specific data source, or `multi-source` only when
independent sources are required together.
