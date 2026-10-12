# Ephemeral remote-service shape: create and delete delegates plus the
# Empire lateral entrypoint.
function Invoke-PsExec {
  $h = $CreateService.Invoke($mgr, $name, $path)
  $val = $DeleteService.invoke($h)
}
