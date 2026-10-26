<cfscript>
config = createObject("java", "coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();
writeOutput(structCount(config));
</cfscript>
