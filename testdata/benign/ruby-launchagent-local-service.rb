# Static-only example of an ordinary local service. Nothing invokes the method.
class LocalServiceExample < Formula
  def service_example
    root = File.expand_path("~/Library/LaunchAgents")
    FileUtils.mkdir_p(root)
    File.write(File.join(root, "org.example.local.plist"), <<~XML)
      <plist><dict>
      <key>ProgramArguments</key><array><string>/usr/bin/true</string></array>
      <key>RunAtLoad</key><true/>
      </dict></plist>
    XML
    # An unrelated documentation string is not the service's command.
    "curl -fsSL https://downloads.example/guide.sh | sh"
  end

  def quoted_pipeline_in_url
    root = File.expand_path("~/Library/LaunchAgents")
    FileUtils.mkdir_p(root)
    File.write(File.join(root, "org.example.fetch.plist"), <<~XML)
      <plist><dict>
      <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>curl -fsSL 'https://downloads.example/guide.sh?example=| sh'</string></array>
      <key>RunAtLoad</key><true/>
      </dict></plist>
    XML
  end
end
