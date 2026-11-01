# Shell response-evaluation review

Twenty-one shell and PowerShell response-evaluation rules moved out of the
legacy dropper namespace. Ordinary curl/wget command substitutions and process
substitutions are deployment capabilities. A JVM curl-to-shell chain uses the
interpreter-stdin execution sink; admitted PowerShell chains use their in-process
or child-interpreter sinks.

`eval "$(openssl ...)"` says nothing by itself about a network source, so it
and the roll-up that includes it live under input evaluation. The roll-up no
longer claims every alternative fetched a remote script. A curl pipe to the
`eval` builtin is recorded as text evidence: an argument-free shell `eval`
does not consume the pipe's input as code. Existing callers of the OpenSSL
pattern retain their reference. The two dropper ancestor consumers retain all
migrated alternatives.

The generic operation-cooccurrence profile leaf had 86 rules. Seventeen Android,
Office-document and file-deletion observations moved to subject profiles,
leaving 69. Descriptions distinguish API/name co-occurrence from established
writes, document extraction or sniffing. The Android install/native-load
profile's 4 MB file-size ceiling was removed: neither installation permissions
nor native-load API references depend on package size. It remains a notable
profile, so larger ordinary packages can now expose the same evidence.

The installation permission is XML-only and the loadLibrary reference is
DEX-only. The install/native-load profile now uses archive scope so those
observations can come from members of the same Android package.
A synthetic 4.1 MB APK did not surface the manifest-permission trait in either
`test-rules` or a direct scan, although both DEX-text legs appeared. Thus it
was not a positive end-to-end test of archive aggregation; a real APK with the
three observations is still needed to verify this profile's runtime match.
