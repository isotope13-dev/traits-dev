def install_tray
  path = File.join(ENV.fetch('APPDATA'), 'tray.js')
  File.write(path, "console.log('Tray app started');")
  target = format('node.exe "%s"', path)
  system('reg', 'add', 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run',
         '/v', 'TrayApp', '/t', 'REG_SZ', '/d', target, '/f')
end
