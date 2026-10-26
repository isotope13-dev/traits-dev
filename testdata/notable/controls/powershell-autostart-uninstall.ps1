$ShortcutPath = Join-Path ([Environment]::GetFolderPath('Startup')) 'AxonHub.lnk'

function Install-Elevated {
    $scriptPath = $MyInvocation.MyCommand.Path
    $arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`" install-autostart"
    Start-Process PowerShell -Verb RunAs -ArgumentList $arguments
}

function Uninstall-StartupFolder {
    if (Test-Path $ShortcutPath) {
        Remove-Item -Path $ShortcutPath -Force
        Write-Host "Startup shortcut removed"
    }
}
