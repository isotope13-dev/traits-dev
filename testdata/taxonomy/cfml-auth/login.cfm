<cfset mypwd="demo-only">
<cfif session.pwd neq mypwd>
<cfoutput>Sign in</cfoutput>
<cfabort>
</cfif>
