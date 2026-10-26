#!/bin/sh
# Static control: ordinary local command configured as a launchd job.
cat > "/tmp/local-service.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
<key>Label</key><string>org.example.local-service</string>
<key>ProgramArguments</key><array><string>/usr/bin/true</string></array>
<key>RunAtLoad</key><true/>
</dict></plist>
PLIST
launchctl load -w "/tmp/local-service.plist"
