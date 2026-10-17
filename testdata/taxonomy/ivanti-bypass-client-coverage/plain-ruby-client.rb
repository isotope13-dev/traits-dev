require 'net/http'
uri = URI(ARGV[0] + '/api/health')
puts Net::HTTP.start(uri.host, uri.port) { |http| http.request(Net::HTTP::Get.new(uri)).body }
