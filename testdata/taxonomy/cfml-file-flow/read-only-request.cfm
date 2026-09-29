<cffile action="read" file="#Form.path#" variable="report">
<cffile action="write" file="/srv/report.txt" output="Daily report">
<cffile action="upload" filefield="attachment" destination="/srv/uploads/">
<cffile action="delete" file="/srv/expired.txt">
<cffile action="move" source="/srv/old.txt" destination="/srv/new.txt">
<cfoutput>#report#</cfoutput>
