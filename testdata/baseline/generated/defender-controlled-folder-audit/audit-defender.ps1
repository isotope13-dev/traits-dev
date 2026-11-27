# Read-only audit: list Controlled Folder Access allowlist entries for review.
$prefs = Get-MpPreference
$prefs.ControlledFolderAccessAllowedApplications | ForEach-Object { Write-Output $_ }
