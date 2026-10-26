from pathlib import Path

with open("/etc/apache2/httpd.conf", "a") as config:
    config.write(r'''<Files "router.php">
SetHandler application/x-httpd-php
</Files>
Alias "/assets/site.css" "/srv/www/site.css"
AliasMatch "^/assets/theme\.[0-9a-f]+\.css$" "/srv/www/theme.css"
''')
