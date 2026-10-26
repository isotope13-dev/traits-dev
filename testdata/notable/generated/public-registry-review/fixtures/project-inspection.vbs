Sub InspectProject()
    count = NormalTemplate.VBProject.VBComponents.Item(1).CodeModule.CountOfLines
    other = ActiveDocument.VBProject.VBComponents.Item(1).CodeModule.CountOfLines
    path = ActiveDocument.FullName
End Sub
