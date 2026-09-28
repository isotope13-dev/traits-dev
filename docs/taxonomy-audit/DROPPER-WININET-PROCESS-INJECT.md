# WinINet process-injection audit

`wininet-download-process-hollowing-dropper` combines WinINet URL retrieval
with process enumeration, an embedded PE signature, thread-context query and
set references, and executable-allocation evidence. The required activation
sink is process injection, so the composite moved from the legacy generic
`delivery/execute-download` leaf to `dropper/process-inject`.

The matcher body, file scope, platforms, and criticality are unchanged. Search
found no exact-ID consumers to update. This migration records the likely sink;
it does not claim that a runtime download or injection was observed.

Soft validation passes **1,837/1,837 fixtures**. Strict validation still has
catalog-wide authoring and cap debt, including **165 over-cap directories**.
