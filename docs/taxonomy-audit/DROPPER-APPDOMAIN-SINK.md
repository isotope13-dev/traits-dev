# PowerShell AppDomain loaders use the module-load sink

Four composites under
`objectives/command-and-control/dropper/staging/memory/powershell.yaml`
require a PowerShell AppDomain assembly loader and method reflection, combined
with a remote source or related stage evidence. They identify staged managed
code being activated by a runtime module loader. AppDomain loading is the
specific sink; in-memory residency does not make `staging/memory` the better
home.

The file moved intact to
[`objectives/command-and-control/dropper/module-load/powershell-appdomain.yaml`](../../objectives/command-and-control/dropper/module-load/powershell-appdomain.yaml).
Its SHA-256 is unchanged at
`b022aeecfce0099044183cb8c413f4be2edbfb9f293178e30d6f6c3f87e5dd92`.
All four composites keep their matchers, settings, references, and IDs' local
suffixes unchanged. A repository-wide search found no external rule-ID or
directory references to the moved rules.

`TAXONOMY.md` now states that PowerShell `AppDomain.Load` and .NET
`Assembly.Load` belong under `dropper/module-load`; `staging/memory` is reserved
for executable-memory staging without a more specific activation sink. The
source leaf falls **130 → 126** and the destination rises **12 → 16**. The
source remains oversized and needs further rule-by-rule sink review.
