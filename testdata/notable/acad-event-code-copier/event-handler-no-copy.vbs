Public WithEvents ACADApp As AcadApplication
Sub Report()
Set ACADApp = GetObject(, "AutoCAD.Application")
MsgBox "Drawings open: " & ACADApp.Documents.Count
End Sub
Private Sub AcadDocument_BeginClose()
 Call Report
End Sub
