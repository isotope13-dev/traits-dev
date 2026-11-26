Attribute VB_Name = "ExportHelper"
Option Compare Database
Public Sub ExportTables()
    DoCmd.TransferDatabase acExport, "Microsoft Access", "C:\Data\copy.accdb", acTable, "tblLog"
End Sub
