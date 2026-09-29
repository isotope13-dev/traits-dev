<cfset password="example"><cfif enabled><cfoutput>Welcome</cfoutput><cfelseif session.pwd NEQ password><cfoutput>Login</cfoutput></cfif>
