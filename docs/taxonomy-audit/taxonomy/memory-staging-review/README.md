# Memory staging review

Nineteen rules moved from legacy memory staging. HTA reflective assembly
activation moved to module loading; coherent image-carrier and post-quantum
crypto/memory/thread combinations moved to native payload activation; and the
WinInet/GCM/section-mapping combination moved to image mapping. The 7-Zip
overlay/read/RWX-copy combination moved to payload reconstruction. These retain
their hostile classifications as likely behaviors supported by the combined
signals, without asserting a proven data-flow link.

Writable/opaque section and decoder combinations moved to section-packing
evasion. ISO method-name co-occurrence, escaped byte patterns, and generic crypto/memory API combinations moved to profiles; they no longer independently
claim that a payload executed. The SystemFunction033, memory and hashed API-resolution combination remains a
hostile reconstruction objective; the existing RC4 fixture exercises it. The
hidden HTA BinaryFormatter combination is an
unsafe-deserialization behavior, and the corrupted base64 fragments are
encoding evidence. Match conditions, inherited file-size bounds, scopes,
architecture, confidence and downgrade rules were checked against the original
19 rules. The existing 10 MB bound on the Firefox user-agent and native-section
combination remains; no independent evidence here established a safer new
threshold. Exact references were updated, and the broader dropper consumer
retains these historical alternatives pending its separate weak-evidence audit.

The HTTP user-agent directory held 93 rules. Twenty-two hardcoded User-Agent
observations moved to `metadata/file/profile/user-agent`; the original directory
now contains 71 rules, with 35 in the profile directory after the additional
Firefox observation. All 93 original user-agent rules retain their parsed
conditions and metadata. They describe literal evidence rather than necessarily
an HTTP request or client impersonation.
