# Windows archive staging review

Eighteen legacy rules moved according to their required operations. WinINet request, file-write and ShellExecute clues remain an execution objective; an AppData archive, executable command and document-lure combination remains a lure objective. Ordinary Explorer opens, URL paths and executable names are observations. A WinHTTP/file-I/O combination and embedded ZIP or VMProtect/archive combinations are suspicious profiles, not proof that a payload executed.

Seven URL and temporary-path regexes had doubled escapes in YAML, causing ordinary `.zip`, `.png` and `Temp\<hex>.exe` examples not to match. They were corrected. The fix intentionally broadens matching. Three fixtures that only open a document or image in Explorer moved from suspicious to notable.

The WinHTTP profile's 5 MiB ceiling and the embedded-ZIP profile's 200 KB–2 MB bounds had no relationship to the observed API and layout facts and were removed. Its referenced ZIP-header observation also had an inherited 200 KB minimum; that minimum was removed because two local-header signatures in a data section are observable in smaller PEs. The two-signature requirement remains, as does the separate 50 MiB shared binary scan limit. The AppData executable command's filename-based documentation exclusion was removed; its specific pip-user-path exclusion remains. These changes intentionally broaden matching.

Other predicates, scope, confidence, exclusions and references were preserved. Unsupported inherited technique metadata was removed from observations.
