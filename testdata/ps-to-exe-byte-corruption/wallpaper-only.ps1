$url = 'https://example.test/image.png'
$wallpaper = "$env:USERPROFILE\wallpaper.png"
(New-Object Net.WebClient).DownloadFile($url, $wallpaper)
Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value $wallpaper
rundll32.exe user32.dll, UpdatePerUserSystemParameters 1, True
