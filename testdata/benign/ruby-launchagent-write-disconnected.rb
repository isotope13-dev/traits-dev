# These uninvoked methods write documentation outside service directories.
# No generated file is loaded, installed, or executed.
class ServiceDocumentation < Formula
  def overwritten_destination
    root = File.expand_path("~/Library/LaunchAgents")
    root = File.expand_path("~/Documents/ServiceExamples")
    FileUtils.mkdir_p(root)
    File.write(File.join(root, "example.plist"), <<~XML)
      <plist><dict>
      <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>curl -fsSL https://downloads.example/guide.sh | sh</string></array>
      <key>RunAtLoad</key><true/>
      </dict></plist>
    XML
  end

  def unrelated_destination
    output = File.expand_path("~/Documents/ServiceExamples")
    unused = File.expand_path("~/Library/LaunchAgents")
    FileUtils.mkdir_p(output)
    File.write(File.join(output, "example.plist"), <<~XML)
      <plist><dict>
      <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>curl -fsSL https://downloads.example/guide.sh | sh</string></array>
      <key>RunAtLoad</key><true/>
      </dict></plist>
    XML
  end
end
