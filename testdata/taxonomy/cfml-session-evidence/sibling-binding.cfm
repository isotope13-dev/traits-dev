<cfset name="form.flag"><cfif flag><cfset name="session.flag"><cfelseif IsDefined(name)><cfoutput>Present</cfoutput></cfif>
