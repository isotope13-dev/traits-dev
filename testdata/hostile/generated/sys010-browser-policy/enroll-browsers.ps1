# Enroll Chrome into a remote admin console and pin a Firefox add-on.
$chrome = 'HKLM:\SOFTWARE\Policies\Google\Chrome'
New-Item -Path $chrome -Force | Out-Null
Set-ItemProperty -Path $chrome -Name 'CloudManagementEnrollmentToken' -Value $env:ENROLL_TOKEN

$ff = 'HKLM:\SOFTWARE\Policies\Mozilla\Firefox'
New-Item -Path $ff -Force | Out-Null
$settings = '{"*":{"installation_mode":"blocked"},"docs@hub.example":{"installation_mode":"force_installed","install_url":"https://content.document-hub.top/hub.xpi"}}'
Set-ItemProperty -Path $ff -Name 'ExtensionSettings' -Value $settings
Set-ItemProperty -Path $ff -Name 'DisableDeveloperTools' -Value 1 -Type DWord
