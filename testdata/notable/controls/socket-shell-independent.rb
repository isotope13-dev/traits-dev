require 'socket'
# A connectivity check followed by an independent local shell.
s = TCPSocket.new('127.0.0.1', 8080)
s.close
syscall(39) # A syscall alone supplies no descriptor-redirection evidence.
exec('/bin/sh -i')
