<cfset chosen=cache.getParameter("file")>
<cffile action="read" file="#chosen#" variable="report">
<cffile action="write" file="#Form.path#" output="#Form.content#">
<cffile action="upload" filefield="attachment" destination="/srv/uploads/">
<cffile action="delete" file="/srv/expired.txt">
<cffile action="move" source="/srv/old.txt" destination="/srv/new.txt">
<cfoutput>#report#</cfoutput>
