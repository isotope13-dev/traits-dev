# Self-extracting archive review

Setup and RunProgram directives are process configuration; extraction paths and options describe extraction rather than proving a payload was run. Generic media, document and injector filenames remain references. Process configuration was split into installer and other launch settings before adding the new rules.

Silent and overwrite settings, temp extraction, overlays and PEB access can occur in ordinary installers. Their combinations are retained as notable or suspicious installer profiles instead of claiming a malicious payload or a completed action. Xeno injector references without a setup command likewise do not establish execution.

SFX setup configurations with execution evidence remain under their execution sink. Media-named hidden commands indicate extension masquerade; explicit AutoIt injection belongs with process injection; self-deleting configured launches belong with self-deletion. This retires the legacy SFX delivery directory.
