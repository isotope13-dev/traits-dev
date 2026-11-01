# .NET file-write evidence review

The legacy runtime staging file included ordinary `System.IO.File` method text and profiles that combine file-write references with Base64 decoding or a VBS filename. The conditions do not tie those observations to a specific file or prove payload staging.

The method observations and their aggregate are now in `metadata/file/profile/file-write-api`; the Base64-and-write and VBS-name-and-write combinations are in `metadata/file/profile/file-write-context`. Descriptions now state the observed references. Their match conditions, scope, confidence and criticality remain unchanged. The inherited T1140/B0030 annotations and the VBS component's T1059.005 annotation were removed because those observations alone do not establish the techniques.

The remaining rules in the runtime staging file need individual review, including their stronger claims about protected resources and payload execution.
