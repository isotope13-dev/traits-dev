<cfset selected = form.cmd>
<cfset actual = "/usr/bin/uptime">
<cfoutput><input name="cmd"></cfoutput>
<cfexecute name="#actual#"></cfexecute>
