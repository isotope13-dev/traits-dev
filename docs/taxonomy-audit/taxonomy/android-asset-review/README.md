# Android archive asset review

Nineteen legacy archive-staging rules were reviewed. Package member combinations moved to Android asset facts; archive, HTTP, permission, reflection and sensor combinations moved to specific context profiles. These combinations do not establish a payload, installation, surveillance or a loader solely from filenames or APIs. The APK PAK/XOR/file-stream/package-inspection combination is a suspicious cryptography profile; the reflection/native-load/sensor combination is a suspicious mobile-collection profile.

Twenty existing asset facts were split from the crowded mobile-package leaf into `metadata/package/files/android-assets`. Descriptions now distinguish a filename from the data it may contain: `.bal` alone does not establish Basic4Android, `.p12` does not prove its contents, and a drawable PNG name does not establish size. The eight-match hex/hyphen asset threshold remains, and its description states the count without claiming valid GUIDs. Ordinary numeric, hex and two-level names are notable observations.

The `assets/metadata.dat` fact formerly required the *whole APK* to be at least 8 MB while claiming the asset was large. The unbound size gate was removed, the trait renamed and made notable, and its consumers updated. A 413-byte APK containing that member now matches. This intentionally broadens matching.

All other predicates, scopes, confidence values and references were checked against the prior rules. The mobile-package leaf decreased from 67 to 47 rules; the new asset leaf has 28.
