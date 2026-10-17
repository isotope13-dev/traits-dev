# Advpack setup engine carries INF section vocabulary
====================================================

`inf-presetup-commands-section` matches the `RunPreSetupCommands` /
`PreSetupCommandsSection` INF vocabulary. The advpack setup engine
(`advpack.dll`, `IEAdvpack.dll`) implements INF-driven installation, so its
own binary embeds that vocabulary next to its exported setup entry points
(`LaunchINFSection*`, `RunSetupCommand`, `ExecuteCab*`). The atomic excludes
binaries exporting those entries
(`micro-behaviors/os/package-manager/install::advpack-setup-entry-exports`); a
binary that merely mentions the vocabulary still matches.

Run `python3 testdata/advpack-setup-vocabulary/verify.py
<scratch-directory>`. The positive and the no-exports control must report
the suspicious atomic; the advpack-engine fixture must not.
