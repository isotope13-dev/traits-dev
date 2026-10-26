param($records, $OutFile)
$records | Format-List URL, UserName, Password | Out-File $OutFile
