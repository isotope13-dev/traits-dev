require 'socket'
require 'open3'
sock = TCPSocket.new('127.0.0.1', 9000)
while message = sock.gets
  Open3.popen2e('/usr/bin/date') do |stdin, output|
    IO.copy_stream(output, sock)
  end
end
