# APK member facts belong with package structure

`android-assets.yaml` placed Android package-member path observations under
dropper staging and inherited `T1027.002`/`B0024`. The matchers established
that an APK contained a named asset, resource, DEX file, or nested APK; they did
not establish packing behavior or staging by themselves. These 17 atomic
observations now live in `metadata/package/files/mobile-package/android-apk.yaml`
with explicit Android and APK/ZIP scope. Their matcher bodies, confidence,
criticality, and package-member paths are preserved. The inappropriate
inherited ATT&CK and MBC labels are removed.

Existing composites now consume the canonical metadata IDs. The
`apk-device-admin-lockscreen` conjunction moved to
`objectives/impact/ui/manipulation/harassment/android.yaml`, where its package
layout plus device-admin and lock-screen resource evidence supports the
probable lock-screen manipulation characteristic. This remains an inference
from packaged resources, not a claim that the application executed or locked a
device. The objective keeps its suspicious criticality and confidence.

`apk-dex-drawable-apk-path` and `apk-dex-telephony-sms` remain in archive
staging for now: they match DEX contents, not parsed package-member paths, and
need a separate placement review. The general boundary is documented in
`TAXONOMY.md`: package-specific member facts belong to the package's metadata
subject; generic archive structure belongs to `archive-member`; capability or
objective composites consume those facts when additional evidence supports the
claim.

The same rule applies to 14 more APK member-path facts that had been placed in
`staging/encrypted/android.yaml`: opaque/numeric/GUID assets, obfuscated
resource names, module descriptors, and bundled runtime files. Their exact
member-path matchers and APK-only effective scope are retained in the package
metadata leaf. The staging composites now reference those facts. The
resource-name obfuscation conjunction moved to anti-static archive packing;
non-encrypted opaque-asset staging moved to archive staging; and the two
LibGDX/network-module conjunctions moved to package metadata and now describe
bundled modules rather than claiming active downloader behavior. The genuinely
encrypted-core conjunction remains in encrypted staging.

Soft validation remains **1,837/1,837 fixtures**. Strict validation is back to
the catalog's existing **60 issues**, with **164 over-cap directories**. The
encrypted-staging leaf has fallen from **243 to 223 rules**, but still needs a
technique-level subdivision; this move does not reduce the number of over-cap
directories.
