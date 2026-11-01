# Dropper obfuscation and bootstrap review

JavaScript hex/Base64 transformations with file-write and shell-exec evidence
remain file-execution objectives. XOR-decoded curl names, URLs and diagnostic
strings form a suspicious network profile; those strings do not by themselves
establish a download or a write to site-packages. A retry pattern with random or
XOR clues does not establish a dropper, and now has a bounded confidence of
0.9 instead of 4.0. Existing match conditions and downgrade were preserved.
The `misc` file had defaults only and no rules.

The PowerShell bootstrap rules were split into hidden Node process creation,
text and Base64-encoded name observations, and Node or Python construction
profiles. The encoded Python names and web-request text do not establish a
portable interpreter launch. Decryption, Node references and WriteAllText
remain suspicious combined clues without asserting execution. Consumers and
individual conditions were preserved; severities were reduced where the old
claims exceeded their evidence.

The Node bootstrap supporting rules were separated by subject: path and
identifier observations, command-option and archive-password text, decoded
evaluation text, interpreter/stdio and process references, PE and temporary
path clues, and an AWS CDK BuildSpec reference. An archive option and a spawn
call are recorded as clues rather than proof of a 7z extraction; offset reads
and names do not by themselves prove PE-header validation or a random path.
The interpreter-plus-stdin combination remains a probable deployment
capability. Existing consumers and exclusions were updated without changing
match conditions; ordinary password text is now notable.

The final Node bootstrap findings now follow their operations: streamed
network acquisition and launches, interpreter-stdin execution, WSH script
handling, and Startup-folder persistence. Generic detached package install,
ActiveX/stream/shell clues, and Python distribution/API combinations remain
capabilities or profiles. The postinstall-named script is a filename clue,
not proof that a package invokes an install hook; the archive wrapper no
longer carries a supply-chain technique tag on that basis. Existing matches,
scopes and exclusions remain in place.

Nearby event-driven HTTP response evaluation moved to `network/stream`, so the
in-process leaf has room to grow. Its existing rule references were updated;
network-stream evaluation describes response or socket-event handling rather
than requiring a particular language.
