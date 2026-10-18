<cfscript>
items=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();
</cfscript>
<cfquery name="result" datasource="#form.source#">SELECT id FROM products WHERE id = <cfqueryparam value="#form.id#"></cfquery>
<cfoutput>#result.RecordCount#</cfoutput>
