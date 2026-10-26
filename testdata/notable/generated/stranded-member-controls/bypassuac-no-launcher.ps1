# Hijack writer outside the bypass module and without a launcher: no
# BypassUAC conviction.
function Invoke-HijackHelper {
  Write-HijackDll -OutputFile $TempPayloadPath -BatchPath $BatchPath
}
