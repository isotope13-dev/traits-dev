# Spray bind loop without lockout tracking: no evasion conviction.
function Invoke-DomainPasswordSpray {
  $entry = DirectoryEntry($Domain,$User,$Password)
  foreach($User in $UserListArray) { $entry.RefreshCache() }
}
