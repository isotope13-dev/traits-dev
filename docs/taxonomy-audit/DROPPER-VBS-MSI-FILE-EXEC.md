# VBScript MSI chains use the installer sink

Three VBScript composites require an `msiexec` quiet-install operation. Two
also require download evidence; the RMM-specific rule composes the delayed
download/install chain with an RMM identity. These rules now live in
`dropper/file-exec/installer/`, where the installer transaction is the
activation sink. The two other rules in the old `vbs-msi.yaml` file do not
require that transaction and remain in the source leaf for separate review.

The three matcher bodies, file/platform scopes, criticalities, confidences,
proximity bounds, and tags are unchanged. The source defaults were copied to
the destination. The dependent RMM rule moved with its base rule, so its local
reference remains valid; no external exact-ID consumers exist.
`execute-download` falls from **213 to 210 rules**, while
`file-exec/installer` grows from **7 to 10**. See the
[mapping ledger](dropper-vbs-msi-file-exec-mapping.json).
