$cloud = 'HKLM:\SOFTWARE\Policies\Google\Chrome'
for ($i = 0; $i -lt 99; $i++) {
    try {
        Start-Process powershell -ArgumentList '-File enroll.ps1' -Verb RunAs
        break
    } catch {
        Start-Sleep -Seconds 3
    }
}
Set-ItemProperty -Path $cloud -Name 'CloudManagementEnrollmentToken' -Value $token
