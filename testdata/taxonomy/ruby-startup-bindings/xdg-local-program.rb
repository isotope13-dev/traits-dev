def install_launcher
  payload = <<~ENTRY
    [Desktop Entry]
    Type=Application
    Exec=/usr/bin/clock
    NoDisplay=true
  ENTRY
  folder = File.expand_path('~/.config/autostart')
  target = "#{folder}/background.desktop"
  File.write(target, payload)
end
