# Browser authentication evidence

This is the first eight-rule batch from the legacy browser leaf. Its token
fields, cookie field, fetch-body text and combined transfer now live under the
subjects described in the [object-schema review](../object-schema-neighborhood/README.md).
The original rule inventory and rewritten consumers are in [moves.json](moves.json).
The other browser rules still require migration by their targets and behavior.

A focused static check matched the relocated token-field set and transfer
composite on `cases/auth-and-fetch.txt`. On `cases/auth-only.txt`, the field
set matched but the transfer composite did not. The fixtures are not executed.
