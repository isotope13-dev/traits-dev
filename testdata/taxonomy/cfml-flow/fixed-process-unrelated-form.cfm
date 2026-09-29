<cfoutput><input name="cmd"></cfoutput>
<cfexecute name="/usr/bin/uptime" outputfile="/tmp/status.txt"></cfexecute>
<cffile action="read" file="/tmp/status.txt" variable="status">
<cffile action="delete" file="/tmp/status.txt">
