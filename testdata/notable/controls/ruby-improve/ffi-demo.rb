# Usage: ruby -r ./lib/tracing_demo examples/dlopen.rb
require 'fiddle'
handle = Fiddle.dlopen('libc.so.6')
puts handle
