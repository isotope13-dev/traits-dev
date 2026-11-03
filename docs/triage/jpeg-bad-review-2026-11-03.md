# JPEG mislabeled-bad review

The source snapshot contains 40 samples. Thirty-eight are under 5 MB and were
initially scanned together; the two larger archives were reviewed separately.
Paths and collection labels are not proof of the content's behavior. The
independent scans used `--follow=none`, so fetched references were not included.
A final Hopper dry run confirmed 36 good, 3 bad, and 1 inconclusive label.

`18a9c4e76fc2602607f214630abd37557a4feeb2fa914cba81cd2dde2f0072c3`
is a VS Code extension archive. The local all-files scan represented all 173
members and reported 74 records with analysis gaps; neither scanner found
suspicious or hostile traits. Hopper moved it to **good**.

`3c883c36bd9a0710952cef53924b57e85a202906dc133cbb71fb995a712eebea`
is a source archive with 5,666 members; the local all-files scan represented
every member and reported 1,694 records with analysis gaps. Both scanners
flag a security-scanner unit test that passes command strings, including an
encoded real-world example, to the scanner under test. The reviewed test
asserts on findings rather than executing those strings. One hostile rule combined
an unbound shell-fetch text observation with an external-IP URL and claimed
execution; it now reports notable co-occurrence, and the underlying
observation describes command text. Fresh scans by both scanners report three
suspicious text observations on this test and no hostile member findings.
The source also contains installation instructions printed to users, configured
service integrations, and tests that pass security examples as data. The
reviewed artifact is **good**; Hopper confirmed its existing label. The three
remaining observations describe actual unusual test strings, not successful
execution, and are retained rather than suppressing unrelated code in the file.
A focused test verifies missing components and separate comment/IP locations;
full uncached validation passes. Cleave represented 5,804 records including
derived layers; Atomscan represented 4,867 and exited 1 after producing JSON.

For the remaining 34 small samples, the revised parser reported JPEG containers
without structural problems, and neither scanner reported suspicious or hostile
traits. The parser does not establish that every pixel decodes. Hopper moved
them to **good**; their hashes and original paths are recorded in
[`jpeg-good-2026-11-03.md`](jpeg-good-2026-11-03.md).

`3697e66e68514208563e5caddd4d9a1a574208a40eb40afe6f0bca08b0035b1d`
is ImageMagick vector text saved with a JPEG extension. Its fill URL contains
a shell pipeline and an interactive TCP shell. Both scanners report the two
hostile observations after the new vector rules; Hopper confirmed **bad**.

`c6a1aed25ee91ec4488f0bf839e5b7d6275c7987d5ad70b0679c12d7a80a1034`
is an XML scriptlet, not a JPEG. It invokes hidden PowerShell containing a
download-and-evaluate expression. Both scanners report the hostile scriptlet
observation; Hopper confirmed **bad**.

`4cdbe81073853188cc68779066251f20fad54d1bf35ccef9fab2e8efe061072c`
has a JPEG COM segment declaring length 1 and a long run of x86 NOP bytes.
The prior parser silently stopped at the invalid length but reported the
container valid. Filefacts now records the short comment length and a media
structure problem; a rule combines that structural fact with the NOP run.
Both rebuilt scanners report the hostile combination; boundary tests cover
valid comments and marker-like bytes inside another segment. Hopper confirmed
the existing **bad** label.

`9e3e56e1cddda63117ef8edf58dd679bff373215b25143f29fe668171e691834`
has HTML containing three zero-height remote iframes after the JPEG end marker.
A suspicious observation now describes the bytes immediately after the JPEG
terminator without asserting that a browser executed them. Both scanners
report this observation. Hopper moved the sample to **inconclusive**: the
iframe destinations' content and the context in which the bytes would be served
are unavailable, so the intent of the appended HTML cannot be established.
