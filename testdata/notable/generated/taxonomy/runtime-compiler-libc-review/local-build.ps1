$outDir = Join-Path $PSScriptRoot "build"
& $outDir\compiler.tests.exe --shuffle
& "C:\tools\builder.exe" --config Release
