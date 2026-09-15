# Documentation data only: no file writes, process launch, or lifecycle hook.
def launchd_example
  <<~XML
    <!-- Example location: ~/Library/LaunchAgents/example.plist -->
    <plist><dict>
      <key>ProgramArguments</key><array><string>/usr/bin/true</string></array>
      <key>KeepAlive</key><true/>
      <key>RunAtLoad</key><true/>
    </dict></plist>
  XML
end
