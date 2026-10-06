# ZCode Pro one-click installer miniature (Windows)
# Installs to %LOCALAPPDATA%\ZCodePro and creates a "ZCode Pro" Start Menu
# shortcut that launches the bundled silent VBS starter. The shortcut
# points at this package's own launcher by design, not hijack.
param(
  [switch]$Desktop,
  [switch]$Uninstall
)
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
$dest = Join-Path $env:LOCALAPPDATA "ZCodePro"
$startMenu = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\ZCode Pro.lnk"

if ($Uninstall) {
  Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
  Remove-Item $startMenu -ErrorAction SilentlyContinue
  Write-Host "[zcode-pro] uninstalled."
  exit 0
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Copy-Item -Recurse -Force "$repo\bin" $dest
$wsh = New-Object -ComObject WScript.Shell
$lnk = $wsh.CreateShortcut($startMenu)
$lnk.TargetPath = "$env:SystemRoot\System32\wscript.exe"
$lnk.Arguments = "`"$dest\bin\zcode-pro.vbs`""
$lnk.WorkingDirectory = "$dest"
$lnk.Description = "ZCode Pro silent starter"
$lnk.Save()
Write-Host "[zcode-pro] installed to $dest"
