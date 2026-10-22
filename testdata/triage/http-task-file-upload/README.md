HTTP tasking and file export
===========================

P7 DarkSword's published `download` handler reads a local file selected by
the C2 server and uploads it; its `exec` handler evaluates received JavaScript.
The article also describes on-device keychain JSON extraction and upload.

Sources:

- https://www.iverify.com/blog/blog-malvertising-coruna-darksword-iphone-exploits
- https://www.iverify.com/blog/darksword-variant-threat-research

The new capability matchers bind an HTTP response to a file-read path and
file contents to a fetch request body. The suspicious composite requires
both capabilities in one file. It does not prove those two operations use
the same file. The hostile composite additionally requires the existing
HTTP-response-to-eval provenance matcher. It detects the combined file
transfer and remote execution behavior without assigning a malware family.
Hostnames, staging filenames, command labels, and human language do not gate it.
JavaScript and TypeScript share these APIs across supported Unix and Windows
environments; this does not imply Python or native-binary coverage.

Run focused controls in the Cleave fixtures tree:

```sh
python3 testdata/triage/http-task-file-upload/check.py \
  --fixtures-dir /usr/local/var/cyclotron/cleave/tests/fixtures/http-task-file-upload
```

Cases cover renamed routes and Unicode identifiers, TypeScript, split reads,
JSON wrappers, ordinary file-transfer clients, local file uploads with remote
metadata, read-only clients, JSON forwarding, and commented examples. No
generated sample is executed. Four compiled native controls check the retained
HTTP upload symbol observation after consolidation.

The upload leaf was at 100 rules. Its two `http-upload-symbol-a/b` atoms and
their OR-only wrapper reported the same operation under three IDs. They are
consolidated into the retained `http-upload-symbol` ID with the union of the
original matchers and unchanged scope, severity, and confidence. There were
no external references to the removed atom IDs. The parent-selector consumer
in `dotnet-scout-pe.yaml` uses the upload directory as one alternative with
no cardinality threshold, so retaining the union preserves its admission.
