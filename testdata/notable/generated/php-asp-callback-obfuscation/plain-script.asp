<%@ Language=VBScript %>
<%
Set engine = Server.CreateObject("MSScriptControl.ScriptControl")
engine.ExecuteStatement("X=1")
' Set other = Server.CreateObject("MS" & Chr(83) & "criptControl.ScriptControl")
' other.ExecuteStatement("X" & Chr(61) & "1")
%>
