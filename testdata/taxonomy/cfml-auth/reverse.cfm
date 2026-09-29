<CFSET appPassword="demo-only">
<CFIF appPassword != session.supplied>
<cfoutput>Sign in</cfoutput>
<cfabort>
</CFIF>
