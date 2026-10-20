param($supplied, $records, $OutFile)
[pscustomobject]@{'DecPassword' = $supplied}
$records | Format-List URL, UserName, Password | Out-File $OutFile
