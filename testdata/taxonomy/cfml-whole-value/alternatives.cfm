<cfif x><cfset a="read"><cfset m="POST"><cfelse><cfset a="write"><cfset m="GET"></cfif>
<cffile action="#a#" file="/srv/f" variable="data">
<cfhttp method="#m#" url="https://example.invalid/">
