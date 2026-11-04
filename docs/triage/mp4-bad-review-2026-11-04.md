# MP4 mislabeled-bad review — 2026-11-04

Reviewed 13 entries with Cleave and Atom and inspected their contents without executing them. Three are bad, eight are good, and two are inconclusive.

The bad entries `d905c55bd9df`, `fff49271d49b`, and `1cbf5811450e` are ZIP archives containing shortcuts that invoke MSHTA and reconstruct remote COM script URLs using mixed hexadecimal and octal escapes. Each also contains a supposed video that decodes from base64 to a shortcut. A new shortcut finding combines the escaped remote script URL with the script host, object invocation and extensive escaping. Both scanners detect the direct shortcuts, and the original archives are also detected by both scanners. A control with the object invocation removed does not match. The rule examines raw shortcut bytes, so malformed timestamps do not prevent detection.

The good entries `624242f45769`, `73d68c79a82b`, `37e73566c685`, `cfd24fdbdac8`, `91c7f954914c`, `507cbb07739c`, `b08ec5775627`, and `d4aae611556d` are ordinary media containers with video streams; sampled frames show video content and no script payload was identified. This is a content review, not a claim that every frame or audio passage was manually examined.

`6480fe57bae7` is opaque data with an MP4 filename but no recognizable media header; its contents cannot be established from the available evidence. `5d03fd083b62` is a self-extracting Windows archive containing a hidden executable, numerous decoy-like files and highly compressible padding. The outer and inner executable trigger a stolen-certificate indicator, but the extracted executable's behavior and the archive's launch configuration were not established. Both are inconclusive, rather than classified from their source labels or certificate alone.
