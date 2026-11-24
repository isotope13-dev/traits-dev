# Windows fuzzing bot bootstrap (synthetic regression snippet).
$webClient = New-Object System.Net.WebClient
$domain = 'CLUSTERFUZZ-WIN'
$username = 'clusterfuzz'
$password = $webClient.DownloadString('http://metadata.google.internal/computeMetadata/v1/project/attributes/windows-password')
& NET USER $Username $Password /add /y /expires:never
# Set registry keys.
& reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntispyware /t REG_DWORD /f /d 1
