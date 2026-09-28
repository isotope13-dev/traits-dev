Compress-Archive -Path input.txt -DestinationPath cache.zip
$encoded = [Convert]::ToBase64String([byte[]](1, 2, 3))
