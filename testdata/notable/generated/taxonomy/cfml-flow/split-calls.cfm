<cfoutput><input name="cmd"></cfoutput>
<cfexecute name="cmd.exe" arguments="/c echo fixed"></cfexecute>
<cfexecute name="/usr/bin/printf" arguments="#form.cmd#"></cfexecute>
