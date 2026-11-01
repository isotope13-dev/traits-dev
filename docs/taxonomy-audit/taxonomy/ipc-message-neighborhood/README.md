# Messaging and storage neighborhood

The IPC message leaf started at 90 rules. The review moved Kafka publication
to publish/subscribe messaging, Windows atom-table operations to collection
operations, relay action names to source naming, and origin comparisons to
origin-policy observations. Extension runtime messaging is now a distinct IPC
branch; a DOM payload field name, a response call, a window-source comparison
and a CustomEvent constructor were placed with the observations they actually
require. The source-field and event predicates alone do not establish a message
or a dispatch.

One legacy page-relay composite moved into extension messaging. Its underlying
message and DOM-field conditions remain required, but its inherited external
transfer annotations were removed because the composite describes local
message passing. Nearby Web Storage and extension-storage observations moved
out of the crowded generic database-access leaf into `data/db/web-storage`.
The moved Kafka descriptions distinguish producer type references and record
construction from demonstrated setup or sending.

[moves.json](moves.json) contains the original definitions, defaults and
consumer rewrites. Run `uv run docs/taxonomy-audit/taxonomy/ipc-message-neighborhood/check-moves.py`
to compare predicates, effective defaults and destination populations. Local
references in the old message directory were qualified after their targets
moved. There were no direct directory-reference consumers of the affected
leaves in the pre-move YAML inventory.

`make validate` passed: 1,927 hostile, 1,774 suspicious, 8,883 notable and
1,336 baseline fixtures. Earlier browser, object-schema and token move audits
also passed after the reference updates.
