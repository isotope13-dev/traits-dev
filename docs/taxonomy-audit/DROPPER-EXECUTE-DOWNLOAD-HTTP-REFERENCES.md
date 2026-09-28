# HTTP retrieval signals belong in communications

The `execute-download` audit found six PowerShell rules that described HTTP
retrieval rather than an acquired payload linked to activation. Three
composite findings combined WebClient/`DownloadString` indicators and a
cleartext URL, but did not require evaluation or launch. Two more rules
identified a WebClient executable URL and staging to a writable path without a
launch sink. Their former hostile or suspicious criticality therefore
asserted more than these matchers established.

The four rules moved as follows:

- `typename-webclient` → `micro-behaviors/communications/http/client/webclient/`
- `webclient-downloadstring-http`, `typename-downloadstring-http`, and
  `typename-webclient-downloadstring` →
  `micro-behaviors/communications/http/lib/invoke-webrequest/`
- `webclient-downloadfile-exe-url` and `webclient-downloadfile-exe` →
  `micro-behaviors/communications/http/download/webclient/`

All matcher predicates, platform scope, and confidence values were preserved.
The `webclient-downloadstring-http` scope drops its impossible `pe` type: its
required DownloadString and cleartext-URL legs support PowerShell and batch,
not PE files. All viable declared types remain. The three composite findings now have `notable`
criticality. The TypeName/URL-only description now records co-occurring
evidence without claiming a DownloadString operation. Exact consumers were
rewritten to canonical IDs. No fixture-specific suppression or exception was
added. The parent `dropper/delivery/execute-download` count falls from 225 to
219; further sink-based migration remains under audit.
