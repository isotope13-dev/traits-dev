@echo off
REM Wipe every fixed volume via diskpart clean all.
for /f "skip=1 tokens=1" %%D in ('wmic logicaldisk get Caption') do (
  echo select volume %%D> "%TEMP%\wipe.txt"
  echo clean all>> "%TEMP%\wipe.txt"
  diskpart /s "%TEMP%\wipe.txt"
)
