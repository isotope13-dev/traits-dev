require 'base64'
File.binwrite('test.txt', Base64.decode64('aGVsbG8='))
system 'ruby', '--version'
