# A legitimate report's SQL and output format do not establish theft.
$query = 'SELECT * FROM urls;'
$History | Format-List Title,URL | Out-String
