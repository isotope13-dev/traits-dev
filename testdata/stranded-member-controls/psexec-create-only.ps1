# Create-only delegate without teardown: no ephemeral-service conviction.
function Invoke-PsExec {
  $h = $CreateService.Invoke($mgr, $name, $path)
}
