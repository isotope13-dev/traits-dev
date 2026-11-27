# Installer post-step: trust the bundled updater so it can write its own folders.
$app = Join-Path $env:ProgramData "DesktopTools\updater.exe"
Add-MpPreference -ControlledFolderAccessAllowedApplications $app
Start-Process -FilePath $app -WindowStyle Hidden
