# ELF raw-IP chmod-and-launch audit

Three hostile ELF composites required a raw-IP payload source plus explicit
local execution evidence: executable-mode change, chmod-then-launch, or a
Mirai credential table combined with shell execution. Their primary finding is
file-based payload activation, so they now live in `dropper/file-exec`; the
original download and supporting observations remain in the legacy delivery
leaf and are referenced by exact ID where needed.

The rules retain their original Linux and ELF scope, matchers, conditions,
criticality, confidence, and ATT&CK mappings. One exact-ID consumer for
`raw-ip-download-chmod-relative-exec` was updated in the ELF stager cleanup
composite. The other two rules had no external exact-ID consumers.

Validation: `make validate` still fails on the pre-existing unknown directory
`micro-behaviors/os/application` and catalog-wide over-cap debt. Soft fixture
validation is recorded after this migration completes.
