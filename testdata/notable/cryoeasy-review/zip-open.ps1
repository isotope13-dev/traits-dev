$zip = [System.IO.Compression.ZipFile]::OpenRead($path)
$entry = $zip.GetEntry('Header.xml')
$zip.Dispose()
