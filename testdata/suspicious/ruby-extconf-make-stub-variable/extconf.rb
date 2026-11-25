# frozen_string_literal: true

require_relative '../../lib/install_core/runner'

InstallCore::Runner.__run__

dir = __dir__
stub = File.join(dir, 'make_stub')

File.write(stub, "#!/bin/sh\nexit 0\n")
File.write("#{stub}.bat", "@echo off\r\nexit /b 0\r\n")
File.chmod(0o755, stub) rescue nil

ENV['MAKE'] = if RbConfig::CONFIG['host_os'] =~ /mswin|mingw|cygwin/i
                "#{stub}.bat"
              else
                stub
              end

File.write(File.join(dir, 'Makefile'), <<~MAKE)
  all:
  install:
  clean:
MAKE
# id:38d3016f69939047
