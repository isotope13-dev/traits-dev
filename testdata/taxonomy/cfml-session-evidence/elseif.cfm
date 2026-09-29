<cfif flag><cfoutput>Other</cfoutput><cfelseif IsDefined("session.flag")><cfoutput>Present</cfoutput></cfif>
