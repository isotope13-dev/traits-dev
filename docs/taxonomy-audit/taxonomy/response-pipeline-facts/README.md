# Response-pipeline facts and size-bound review

Forty rules moved out of the 85-rule legacy response-pipeline directory,
leaving 45 composites. Generic source, encoded text, URL, comment, product and
log references now describe their own subjects. JavaScript-spawned PowerShell
fetch-and-evaluate chains moved to the child-interpreter sink; updater and
installer exceptions remain exclusion-only. The two previous dropper ancestor
consumers retain all 38 non-exception alternatives. The hosts-file consumer
uses existing URL-construction and script-transformation selectors only where
their current members were already selected; future additions need review.

Three combinations of IRM-related fragments are suspicious profiles rather
than confirmed ClickFix findings. A generic file-named variable invocation and a `/report` endpoint reference are
notable, and variable dispatch no longer claims to create a process. Generic
facts and exceptions no longer inherit attack labels.

The two exact PowerShell launcher and IRM/eval observations no longer reject
files over 256 bytes. Three composites retain the old implicit proximity with a
256-byte bound between their evidence, while two explicitly tiny composites
retain a 256-byte file limit. Verification-marker composites already had
proximity bounds. Long positive and near-miss PowerShell fixtures exercise the
new boundary. Larger legitimate files can now expose these facts, so their
consumers were reviewed as part of the migration.

All 85 original rules were compared; the intended severity, technique, size and
proximity changes are recorded above. The global directory cap did not change.

The remaining 45 composites have now been reviewed and moved. Direct network
script evaluation, child-interpreter execution, transformed execution, file
execution, managed assembly loading, and local executable-memory activation
have separate homes. The memory-branch description includes a local thread
activating copied executable bytes; it does not claim cross-process injection.

Unbound network, command-property, encoded-string and invocation clues are
profiles or neutral capabilities. The ZoomSDK combinations without a required
malicious action are suspicious clues, not confirmed loaders. A WebClient
upload/download combination no longer claims exfiltration without evidence of
sensitive data. Generic file-named variable dispatch is notable rather than
suspicious. Technique labels were removed from the neutral evidence.

The remaining two 256-byte whole-file limits were replaced by 256-byte
proximity between their evidence, allowing the same patterns in larger files.
The hidden launcher plus bare-domain request is suspicious evidence, and the
bare-domain fetch/eval is a suspicious capability. Additional long fixtures
cover both. Both existing dropper ancestor consumers retain the migrated
alternatives. The hosts-file consumer's pre-existing script-transformation
selector covers the two rules moved there; later additions to that directory
need the same consumer review. The FTP log execution consumer also sees new
file-execution rules through its existing payload file-exec selector, under its
existing FTP-log conditions.
