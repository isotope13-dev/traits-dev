<%@ Language=VBScript %>
<%
  Dim oShell
  Set oShell = Server.CreateObject("WSCRIPT.SHELL")
  oShell.Run "notepad.exe", 1, False
%>
