#!/bin/sh
# Static control: a guide is written; an unrelated local service is loaded.
cat > "/tmp/service-example.plist" <<'EXAMPLE'
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
<key>Label</key><string>org.example.guide</string>
<key>ProgramArguments</key><array><string>/bin/sh</string><string>-c</string><string>curl -fsSL https://downloads.example.org/guide.sh | sh</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>
EXAMPLE
launchctl load -w "/Library/LaunchDaemons/org.example.local-service.plist"
