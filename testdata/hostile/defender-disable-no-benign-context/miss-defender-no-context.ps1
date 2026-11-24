# Attacker-style Defender disable with no benign project context (synthetic near miss).
$password = 'x'
& reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows Defender" /v DisableAntispyware /t REG_DWORD /f /d 1
