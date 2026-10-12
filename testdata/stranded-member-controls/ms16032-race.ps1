# Minimal MS16-032 race-shape control: the Empire module function plus a
# suspended CreateProcessWithLogonW launch aimed at the LocalSystem token.
function Invoke-MS16-032 {
  $account = 'LocalSystem token'
  $api = 'CreateProcessWithLogonW'
  $flag = 'CREATE_SUSPENDED'
  Write-Output "$account $api $flag"
}
