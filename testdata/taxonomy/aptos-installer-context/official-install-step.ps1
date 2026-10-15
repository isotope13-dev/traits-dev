$scriptContent = Invoke-WebRequest -Uri "https://aptos.dev/scripts/install_cli.ps1" -UseBasicParsing | Select-Object -ExpandProperty Content
$argList = @("-f", "-y")
if ("${{ inputs.CLI_VERSION }}" -ne "") {
  $argList += "--cli-version"
  $argList += "${{ inputs.CLI_VERSION }}"
}
$tempScript = Join-Path $env:RUNNER_TEMP "install_cli.ps1"
Set-Content -Path $tempScript -Value $scriptContent
& $tempScript @argList
