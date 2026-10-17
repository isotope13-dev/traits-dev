PicoScope suite context suppresses protector/imaging conclusions
==================================================================

PicoScope ships obfuscated assemblies whose protector checks .NET profiler
variables, while its interop layer pairs OpenCV imaging pixel reads with
IoC plugin dispatch. `dotnet-profiler-anti-debug` and the bitmap-stego
composites (`dotnet-pixel-channel-decomposition`,
`dotnet-red-channel-byte-collection`, cascading to the staging chains)
therefore fire on vendor protection and oscilloscope imaging.
`picoscope-suite-context` (PicoScope7 build-farm path fragment or Pico
Technology company metadata) suppresses those conclusions; the UI-library
carve-outs on the stego composites share one directory reference so the
lists stay within the suppression budget.

Run `python3 testdata/picoscope-suite-context/verify.py
<scratch-directory>`. Both positives must report; both PicoScope-marked
negatives must not.
