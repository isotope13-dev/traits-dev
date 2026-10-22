param($file)
$content = [System.IO.File]::ReadAllBytes($file.FullName)
for($i=0; $i -le $content.length - 1; $i++) {$content[$i] += 1}
[System.IO.File]::WriteAllBytes($file.FullName, $content)
