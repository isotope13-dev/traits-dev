# XML mislabeled-good review, 2026-11-04

The initial 40-entry queue was scanned locally in slow mode without reference
following; `/var/tmp/xml-good-initial.jsonl` contains preliminary results.
The queue contains XML documents, Windows Script Files, and archives; their
contents, not the queue name, determine the endpoint ruling. All 40 entries have been reviewed: 29 good, one bad, and ten inconclusive.

`0ac83b38cdcf` is a Windows Script File. It reconstructs a WebDAV UNC path
from character codes, copies a remote batch file into the user profile, and
runs it through a hidden command shell. Two new hostile observations in
separate directories report reconstruction/staging and hidden execution.
The real sample matches both; controls without the WebDAV marker or shell
launch match neither. The fresh no-follow scan reports both hostile traits;
validation passed, Hopper moved it to bad, and the hash-verified snapshot was
relocated to `/tmp/triage/misplaced-bad`.

Twenty-three ordinary XML artifacts were confirmed good: nine Windows MMC
console configurations, eight MSBuild project files, two package manifests,
three Android resource files, and one Gradle component descriptor. Their
project imports point to build files outside these individual artifacts; the
project targets examined only check for missing imports. The fresh local
no-follow batch scan reports no suspicious or hostile traits. Validation
passed and Hopper confirmed all 23 good labels (no-op).

Nine RSS files contain the same obfuscated JavaScript in an article's CDATA.
Their lines are permutations of the same content, and the script bytes are
identical. A static decoder, without executing the sample, reconstructs a
script-element loader for a third-party JavaScript URL. A new suspicious
observation reports the encoded executable script; the real files match, and
controls without the invocation or script tag do not. The remote script was
not examined, so its purpose and the loader's final intent remain unknown.
Endpoint ruling: inconclusive. Validation passed, Hopper moved all nine to
inconclusive, and their hash-verified snapshots were relocated to
`/tmp/triage/misplaced-inconclusive`.

`400713532dd0` is an Office relationship document referencing an external
HTTP template. The template and parent document are not present, so their
behavior cannot be established from this relationship. A new suspicious
observation reports the external template reference; controls without the
external mode or template type do not match. The fresh scan reports that
warning. Endpoint ruling: inconclusive; validation passed, Hopper moved it
to inconclusive, and the hash-verified snapshot was relocated.

`b99e85f2d0fa` is a ChakraCore source archive. Its Octane PDF.js benchmark
contains a large embedded PDF, a base64 decoder, and a separate timer eval;
the prior proximity-only hostile trait conflated them. The rule now requires
the value constructed from character codes to reach `eval`. The original
benchmark clears; a real loader inserted into the same file matches, while a
control evaluating an unrelated value does not. The fresh no-follow archive
scan reports one suspicious JIT memory-protection observation; the call is in
the JIT thunk emitter. Endpoint ruling: good with that capability noted;
validation passed and Hopper confirmed the good label (no-op).

Five remaining non-Chakra archives were reviewed by their actual formats:
GNOME Logs source (`b28a06ea5c98`), a NetBSD DocBook Website package
(`5562621aa12e`), LMMS source (`b185507fb64e`), Bluespec compiler source
(`c27420eddc9a`), and a LinuxCNC Debian package (`b12c324559b2`). The
DocBook package has standard catalog-management install/remove hooks; the
LinuxCNC control archive has standard Python byte-compilation hooks. The
Bluespec macOS CI workflow downloads and runs the ghcup installer if absent;
the remote installer is outside the package. The fresh local no-follow scans
report no suspicious or hostile findings. Endpoint rulings: good. Validation passed; Hopper moved LMMS from pending
to good and confirmed the other four labels. The two snapshots originally
in the unknown pool were hash-verified and relocated to
`/tmp/triage/misplaced-good`.
