<cfset selected = form.cmd>
<cfset selected = "/usr/bin/uptime">
<cfoutput><input name="cmd"></cfoutput>
<cfexecute name="#selected#"></cfexecute>
