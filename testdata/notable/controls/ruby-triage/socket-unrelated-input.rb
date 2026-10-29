require 'socket'
require 'open3'
sock = TCPSocket.new('127.0.0.1', 9000)
local_command = ARGV.fetch(0)
while message = sock.gets
  Open3.popen2e("#{local_command}") do |stdin, output|
    IO.copy_stream(output, sock)
  end
end
