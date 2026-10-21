require 'openssl'
key = OpenSSL::PKey::RSA.new(File.read('public.pem'))
