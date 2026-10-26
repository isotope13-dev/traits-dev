#!/bin/sh
# Static control: an example is replaced by a local-only job before loading.
cat > "/tmp/service.plist" <<'EXAMPLE'
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
<key>Label</key><string>org.example.guide</string>
<key>ProgramArguments</key><array><string>/bin/sh</string><string>-c</string><string>curl -fsSL https://downloads.example.org/guide.sh | sh</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>
EXAMPLE
cat > "/tmp/service.plist" <<'LOCAL'
<plist version="1.0"><dict>
<key>Label</key><string>org.example.local-service</string>
<key>ProgramArguments</key><array><string>/usr/bin/true</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>
LOCAL
launchctl load -w "/tmp/service.plist"
