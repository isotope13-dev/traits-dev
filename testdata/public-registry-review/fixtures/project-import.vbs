Sub InstallTemplateModule()
    Set host = NormalTemplate.VBProject.VBComponents.Item(1)
    host.codemodule.AddFromFile ("C:\TEMP\module.bas")
End Sub
