# Gauntlet missed-sample controls

These runners inspect files; they never run a specimen or fetch a stage.
Run them from the trait repository with bytecode caching disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check.py --cleave ../cleave/target/release/cleave
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check-managed-polling.py --cleave ../cleave/target/release/cleave
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check-dotnet-bundle.py --cleave ../cleave/target/release/cleave
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check-jvm-callsite.py --cleave ../cleave/target/release/cleave --jar-regression
```

`check.py` covers 33 controls for the earlier review, including innocent
co-occurrences and configuration-only artifacts. `check-managed-polling.py`
covers eight non-executed synthetic PE controls. Its CIL matcher observes a
high-bit test and bounded backedge; it does not resolve the called API token
or prove that characters reach a network sink. The recording composite must
remain suspicious, never hostile on those observations alone.

`check-dotnet-bundle.py` covers nine native-PE bundle controls: layouts 1, 2
and 6, stored and raw-DEFLATE members, incomplete manifests, size limits,
size mismatches, duplicate paths and traversal. Normal packaging must not
produce suspicious or hostile findings. Rejected members must not silently
discard a valid sibling.

For specimen regressions, supply external paths; malware is not copied into
these fixtures:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check-jar-selection.py \
  --cleave ../cleave/target/release/cleave --sample /path/to/Ikea_Client_Cracked.jar \
  --reports /tmp/gauntlet-jar-controls
PYTHONDONTWRITEBYTECODE=1 python3 testdata/gauntlet-missed-controls/check-dotnet-bundle.py \
  --cleave ../cleave/target/release/cleave \
  --host '/path/to/Realtek HD Audio x64.exe' \
  --application '/path/to/recovered/Realtek HD Audio x64.dll' \
  --library /path/to/recovered/OpenCvSharpExtern.dll \
  --jar /path/to/Essential_1-5-0-1_forge_1-20-1_bound.jar \
  --reports /tmp/gauntlet-bundle-controls
```

The bundle specimen checks require the recovered assembly's SHA-256 to match,
the recording finding on that assembly, and its rollup to the outer host.
The optional support-library check retains the four neutral observations
previously combined into an unsupported encoded Temp-stager assertion.
Cleave's new extraction currently integrates PE-hosted bundles. It honors
memory, expanded-byte and nesting limits and reports partial extraction.

Atomscan embeds its own Cleave engine. Testing a patched sibling Cleave CLI
does not establish that an installed Atomscan binary contains that engine fix.

`check-jvm-callsite.py` covers eleven generated class-format controls for the
shifted-XOR/callsite layout. `--jar-regression` adds a JAR with 25 higher-ranked
decoy classes and verifies resolver retention in both memory modes; `--jar-only`
is a focused rerun of those two cases. The stored padding crosses the 1 MiB
disk-extraction threshold. `--sample /path/to/resolver.class` checks an external
real class, and `--reports /tmp/control-reports` retains JAR scan results.
These checks never execute Java code and must not produce hostile findings.
