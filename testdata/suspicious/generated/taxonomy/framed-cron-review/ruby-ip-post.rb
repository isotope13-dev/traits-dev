require 'base64'
require 'net/http'
message = Base64.urlsafe_encode64('identity probe')
uri = URI('http://93.184.216.34/')
request = Net::HTTP::Post.new(uri)
request.body = message
