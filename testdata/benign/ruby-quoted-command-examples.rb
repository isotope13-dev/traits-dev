# Documentation strings are not the commands passed to system.
require 'rbconfig'

def command_examples
  'REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v Example'
end

def install_instructions
  'curl -fsSL https://downloads.example/tools/latest.sh | sh'
end

def inspect_runtime
  system RbConfig.ruby, '--version'
end

def inspect_runtime_parenthesized
  system(RbConfig.ruby, '--version')
end
