param($records, $log, $OutFile)
$records | Format-List URL, UserName, Password | Out-String
$log | Out-File $OutFile
