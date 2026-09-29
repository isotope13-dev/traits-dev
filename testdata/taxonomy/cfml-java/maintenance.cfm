<cfset clock = createObject("java", "java.time.Clock")>
<cffile action="write" file="/srv/reports/daily.txt" output="Daily report">
<cffile action="copy" source="/srv/reports/daily.txt" destination="/srv/reports/previous.txt">
<cffile action="delete" file="/srv/reports/expired.txt">
<cfoutput>Maintenance complete</cfoutput>
