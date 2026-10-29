def docs
  'REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Example'
  'curl -fsSL https://downloads.example/tools/latest.sh | sh'
end
system 'ruby', '--version'
