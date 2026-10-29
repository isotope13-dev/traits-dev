require 'net/http'
require 'json'
data = {"tunnelModeTable": {"localVpnIp": "2001:db8::9$(hostname)"}}
uri = URI("http://router.local/api/v1/network/ipsec")
http = Net::HTTP.new(uri.host, uri.port)
req = Net::HTTPGenericRequest.new("PUT", true, true, uri.request_uri)
req.body = JSON.generate({data: data})
http.request(req)
