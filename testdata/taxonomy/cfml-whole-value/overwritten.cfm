<cfset a="read"><cfset m="POST"><cfset a="write"><cfset m="GET">
<cffile action="#a#" file="/srv/f" variable="data">
<cfhttp method="#m#" url="https://example.invalid/">
