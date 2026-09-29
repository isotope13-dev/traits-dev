<cffile action="#'read' & URL.suffix#" file="/srv/f" variable="data">
<cfhttp method="#'POST' & URL.suffix#" url="https://example.invalid/">
