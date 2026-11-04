Synthetic descriptor-carrier dexes (strings-only.dex body plus appended
string-pool text). They document the recognized benign loader contexts for
the android-in-memory-asset-dex-loader family: Google's Play-integrity
DroidGuard module and ByteDance's APM/ads stack suppress the co-occurrence
composites, while the same descriptors without a recognized SDK context
(testdata/suspicious) still fire. The hostile AppComponentFactory composite
additionally requires the opaque-loader APK layout, which none of these
bare dexes can carry.
