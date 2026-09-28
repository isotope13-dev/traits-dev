# Dropper activation migration: C# file launch and .NET hex loader

`delivery/execute-download` mixes source APIs, file identity clues, and complete
staging/activation chains. The first C# migration moves the complete source
chain to `dropper/file-exec`, whose classifier is the activation sink: a
staged file is downloaded and launched. Its path does not imply runtime proof;
it records the probable capability supported by the source evidence.

The new rule reuses canonical observations for `WebClient.DownloadFile` and
`Process.Start`, and uses standalone capabilities for reading TEMP/TMP and
setting `UseShellExecute` false. Four local atomics were removed from the old
objective leaf. The existing `UseShellExecute` capability now covers both its
compiled setter token and the source assignment, avoiding a fifth duplicate
rule. The composite requires download and process start plus at least one
staging/launch clue within 512 bytes. This rules out a file that merely
contains those APIs in unrelated methods.

Three FTP-banner composites previously included the old directory, so each now
also references the migrated C# chain explicitly. The old C# process-start atom
was separately referenced by a Base64 shell-loader; that consumer now uses the
canonical `Process.Start` capability. These choices preserve the relevant FTP
member set and replace an objective atom with the operation it actually
measures.

The .NET XOR-loader source had a single atomic matcher combining four unrelated
clues (`Assembly.Load`, `EntryPoint.Invoke`, `Path.GetTempPath`, and
`Process.Start`). Its only other consumer already required `Process.Start`,
which made that part of the marker redundant. The XOR loader now lives under
`dropper/module-load` and requires an assembly-loading clue for its activation
sink. The shared StringBuilder/hex-conversion reference pair moved to
`micro-behaviors/data/decode/hex`, which is its neutral evidence home; the JIT
and loader consumers point to that canonical atom. The component description
now reports the API evidence rather than asserting chunk reassembly.

Focused checks with the current CLI show the positive C# chain matches and the
same download, launch, TEMP, and no-shell clues separated by more than 512 bytes
do not. The existing `.NET Process.Start` and `WebClient.DownloadFile`
capabilities match the positive source. The fixture expectations record both
cases. The old download leaf remains far over cap; this is one migration step,
not a claim that the oversized family is resolved.
