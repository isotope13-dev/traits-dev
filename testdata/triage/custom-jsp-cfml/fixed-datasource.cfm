<cfscript>
items=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();
</cfscript>
<cfquery name="result" datasource="maintenance">#form.statement#</cfquery>
<cfoutput>#result.RecordCount#</cfoutput>
