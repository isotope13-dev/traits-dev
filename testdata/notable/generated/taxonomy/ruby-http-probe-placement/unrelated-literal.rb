require 'net/http'
request.body = 'account=example'
example = 'account=$(whoami)'
http.request(request)
