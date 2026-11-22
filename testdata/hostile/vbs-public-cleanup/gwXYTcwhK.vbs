On Error Resume Next
Set WMI = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
Set FSO = CreateObject("Scripting.FileSystemObject")
Set Processes = WMI.ExecQuery("SELECT * FROM Win32_Process WHERE Name ='x%DegLIsyPL0qREbb8u.exe'")
For Each Process in Processes
     Process.Terminate
Next
 WScript.Sleep 5000
If FSO.FileExists("C:\Users\Public\x%DegLIsyPL0qREbb8u.exe") Then
     FSO.DeleteFile "C:\Users\Public\x%DegLIsyPL0qREbb8u.exe"
End If
FSO.DeleteFile "C:\Users\Public\gwXYTcwhK.vbs"
Set FSO = Nothing
Set WMI = Nothing
