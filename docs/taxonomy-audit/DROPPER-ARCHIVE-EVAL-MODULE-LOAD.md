# Archive-adjacent eval and module-load audit

Two rules moved out of `dropper/staging/archive` because their required result
is not archive staging:

- `powershell-hidden-remote-instruction-launch` moves to
  `dropper/script-eval`: the matcher requires PowerShell `IEX` alongside
  `Invoke-WebRequest`, hidden-window, and process-start evidence. Its original
  matcher was restored exactly; its old evidence had briefly been folded into
  the archive-extraction aggregate during extraction and is now removed from
  that helper.
- `apk-dalvik-reflection-stager` moves to `dropper/module-load`: it requires a
  Dalvik class-loader descriptor, reflective method lookup, and invocation,
  together with an APK asset/DEX payload. Its opaque-asset helper atoms remain
  in archive staging and are referenced by exact ID. The surveillance
  composite now references the canonical module-load ID.

Neither matcher body nor effective scope changed. The archive-staging source
leaf loses two rules. The split follows the activation sink: remote source
passed to an interpreter is script evaluation, and invoked Dalvik-loaded code
is module loading. Archive-member evidence remains supporting evidence.
