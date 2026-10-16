# CI step re-executes a command string the repo's own earlier step assembled
# (INSTALL_COMMAND from steps.installer.outputs.command). Automation, not an
# environment-staged payload.
$Python = Join-Path $PWD ".venv\Scripts\python.exe"
Invoke-Expression $env:INSTALL_COMMAND
if ($LASTEXITCODE -ne 0) { throw "The locked install failed with $LASTEXITCODE." }
