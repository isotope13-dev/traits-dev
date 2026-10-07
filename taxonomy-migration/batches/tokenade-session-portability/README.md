# Tokenade session portability review

Judgment: BENIGN for both wheels, both cli/session.py members, and the 1.3.0 cookie_crypto.py member.

Both wheels contain pure Python source; their RECORD hashes verify. Reviewed module startup, CLI dispatch, export/import, CDP, keychain/DPAPI/AES cookie processing, subprocess invocations, CI workflow generation, and HTTP/share call sites. Export operates on explicitly selected browsers and writes a local session package. Share operates on a selected session file and password; 1.3.0 uploads PBKDF2/Fernet ciphertext through the documented Supabase service. No covert startup collection or unexplained delivery was identified. Browser fingerprint masking is disclosed dual-use functionality. Broad vendor-evasion claims remain suspicious in 6.3.0.

## Dispositions

See mapping.md for relocated IDs and corpus.md for observed members. Unlisted source IDs retain their original placement and matchers. Effective source type/platform defaults are preserved; neutral observations lose attacker technique mappings. The macOS cookie/HTTP and discovered-CDP observations become notable because neither establishes unauthorized transfer. A separate hostile macOS objective now additionally requires cookie payload construction or file read/upload capability and a dynamic DNS or public tunnel destination. Corpus cookie-stealing fixtures retain hostile coverage; paths plus arbitrary HTTP remain neutral. The redundant multi-vendor solving composite is removed; vendor names and actual solving/evasion claims remain independently detected. OAuth placeholder detection requires a quoted literal, not a variable named secret. Safari path matching no longer downgrades based on the scanned file's incidental name.

Directory consumers of Chromium and DevTools retain explicit migrated observation legs. Generic HTTP 403 references no longer satisfy the webshell-facet selector. Phantom automation references retain their wallet false-positive exclusions. CAB size traits move from naming to archive with unchanged matchers to keep naming within its limit. Tokenade exception recognition requires packager and share-scheme content instead of a filename.

## Controls

Fixtures are copied to a neutral scratch directory before scanning: the repository fixtures path deliberately triggers testing exclusions. CDP discovery with a cookie read matches notable; discovery without a read does not. StartRemoteDebuggingServer plus chrome.exe and Storage.getCookies still matches the hostile in-process cookie-theft objective. A quoted OAuth secret matches; a variable does not. macOS cookie paths and HTTP match notable in source and wheel scope; paths alone do not. Hexadecimal struct.pack matches neutral packing; string packing does not. Browser fingerprint wording matches the browser context atom; cryptographic fingerprint wording does not, while independent spoofing vocabulary can overlap. Both-claim overlap is intentional.

Atomscan's independent ML score remains high for the outer wheel despite corrected trait criticalities. YAML changes do not retrain that classifier.

Cloudflare tunnel host recognition now includes source languages as well as scripts/binaries; the existing matcher is unchanged. Added controls confirm raw cookie payload plus tunnel is hostile and an ordinary destination is not.

Additional transfer coverage recognizes PHP CURLFile constructors through parsed object-creation nodes and embedded curl -T commands in C/C++/Zig source. Python urllib body arguments and Go io.Copy provide file-buffer transfer evidence in the strengthened objective.
