# Native payload staging retirement

The final 24 rules moved from `command-and-control/dropper/staging/native/payload`:

- Likely staged process launches moved to `execution/payload/file-exec` by
  mechanism: native child creation, shell-associated file handlers, or an
  embedded PowerShell download-and-start command. The new `spawn/handler`
  leaf records ShellExecute/OpenAs-style dispatch rather than claiming a
  direct native executable launch.
- An explicit elevated scheduled-task combination moved to persistence;
  WindowsUpdate-style mimicry, a possible decoy dialog and concealed-policy
  acquisition moved to their respective objectives.
- Resource, memory, process, crypto and security API/name combinations that
  do not establish a likely activation step moved to PE profiles. Their
  descriptions and, where appropriate, severity no longer assert a staged
  payload or a linked action. A generic resource/temp API combination remains
  a component and its Elex consumers were redirected.

All 24 original matching conditions, explicit scopes, confidence and
suppressions were preserved. IDs, descriptions, severity and attack
annotations were changed where the evidence warranted it. The native-payload
leaf has no YAML files or live YAML references and was removed.

The adjacent staging-profile directory contained 78 rules. Nine observations
combining download and launch evidence moved to a `download-execution` profile,
leaving 69 staging profiles. Conditions and local scopes are unchanged; seven
consumer files were redirected. A synthetic PE carrying an embedded
PowerShell download/start command matched the moved command objective; an
otherwise identical control with `Write-Output` instead of `Start-Process`
did not. This test does not cover the other migrated composites.
