Attribute VB_Name = "InstallHelper"
' Adds the team's formatting macros to the user's Normal template.
Sub InstallTeamMacros()
    Dim src As String
    src = "Sub FormatReport()" & vbCr & "    Selection.Style = ""Heading 1""" & vbCr & "End Sub"
    With NormalTemplate.VBProject.VBComponents.Add(1).CodeModule
        .AddFromString src
    End With
    MsgBox "Team macros installed"
End Sub
