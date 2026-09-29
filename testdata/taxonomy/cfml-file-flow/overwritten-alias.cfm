<cfset chosen = URL.path>
<cfset chosen = "/srv/report.txt">
<cffile action="read" file="#chosen#" variable="report">
<cffile action="write" file="#chosen#" output="#Form.content#">
<cffile action="upload" filefield="attachment" destination="/srv/uploads/">
<cffile action="delete" file="/srv/expired.txt">
<cffile action="move" source="/srv/old.txt" destination="/srv/new.txt">
<cfoutput>#report#</cfoutput>
