$url = 'https://updates.example.invalid/package.zip'
Invoke-WebRequest -Uri $url -OutFile $archive
$zip = [System.IO.Compression.ZipFile]::OpenRead($archive)
$entry = $zip.GetEntry('Header.xml')
$zip.Dispose()
