<cffile action="read" file="/srv/report.txt" variable="report">
<cffile action="write" file="/srv/report.txt" output="#Form.content#">
<cffile action="upload" filefield="attachment" destination="/srv/uploads/">
<cffile action="delete" file="/srv/expired.txt">
<cffile action="move" source="/srv/old.txt" destination="/srv/new.txt">
<cfoutput>#report#</cfoutput>
