param($supplied, $records, $OutFile)
[pscustomobject]@{'Status' = $supplied}
$records | Format-List URL, UserName, Status | Out-File $OutFile
